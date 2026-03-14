# Astronomy Observation Game — API Reference

A web API game where you operate a telescope, submit observation jobs using
RTML-inspired requests, and receive results in FITS-inspired format. Other
players exist as detectable sources in the shared sky.

**Base URL:** `http://localhost:8080`

---

## Quick Start

```bash
# 1. Create a session (get a telescope)
curl -s -X POST localhost:8080/v1/sessions | python3 -m json.tool

# 2. Submit an observation pointing at the Lyrion Nebula
curl -s -X POST localhost:8080/v1/sessions/{SESSION_ID}/observations \
  -d '{
    "target": {"ra": 42.5, "dec": 15.3},
    "instrument": "imager",
    "filter": "h_alpha",
    "exposure_time": 300
  }' | python3 -m json.tool

# 3. Wait a moment, then fetch results
curl -s localhost:8080/v1/sessions/{SESSION_ID}/observations/{JOB_ID} | python3 -m json.tool
```

---

## Concepts

### RTML-Style Observation Requests

Inspired by the Remote Telescope Markup Language, observation requests specify
*what* to observe rather than *how* the telescope hardware should move. You
provide target coordinates, instrument, filter, and exposure time.

### FITS-Style Responses

Results mirror the FITS (Flexible Image Transport System) structure: a
`headers` block with standard metadata keywords, and a `data` block with
detections or spectral features.

### Async Job Queue

Observations are asynchronous. You submit a job, receive a job ID, and poll
for completion. Processing time scales with exposure duration (longer
exposures take slightly longer to process but detect fainter sources).

### Instruments

| Instrument        | FOV Radius | Wavelength | Best For                        |
|-------------------|------------|------------|---------------------------------|
| `imager`          | 1.5°       | Optical    | Surveying fields, finding sources |
| `spectrograph`    | 0.05°      | Optical    | Classifying individual sources  |
| `radio_receiver`  | 3.0°       | Radio      | Detecting radio-loud sources and player signals |

### Filters (optical instruments)

| Filter    | Throughput | Notes                              |
|-----------|------------|------------------------------------|
| `clear`   | 100%       | Broadband, maximum depth           |
| `r_band`  | 80%        | Red optical                        |
| `b_band`  | 70%        | Blue optical                       |
| `h_alpha` | 30%        | Narrow-band; emission objects glow brighter |
| `oiii`    | 25%        | Narrow-band; emission objects glow brighter |

### Noise Model

- **Optical:** limiting magnitude improves with `2.5 * log10(exposure_time)`
- **Radio:** noise floor (mJy) decreases with `1/sqrt(exposure_time)`
- Longer exposures detect fainter sources at higher SNR
- Player sources have positional jitter that decreases with SNR

### Detecting Other Players

Players appear as sources in the sky:
- **Optical:** faint point sources (magnitude ~18), appear as `kind: "unidentified"`
- **Radio:** weak wideband emitters (~5 mJy baseline)
- **Transmitting players** are much brighter (both optically and in radio)
- **Spectrograph** reveals `"artificial"` spectrum with `"non-thermal"` classification

---

## Endpoints

### POST /v1/sessions

Create a new telescope session. Your telescope is placed at a random position
in the shared sky.

**Request:** empty body or `{}`

**Response (201):**
```json
{
  "session_id": "a1b2c3d4e5f6",
  "telescope": {
    "id": "SCOPE-A1B2C3",
    "position": {"ra": 123.4567, "dec": -45.6789},
    "transmit_power": 0.0
  },
  "observations_submitted": 0,
  "instruments": ["imager", "spectrograph", "radio_receiver"],
  "filters": ["clear", "r_band", "b_band", "h_alpha", "oiii"]
}
```

---

### GET /v1/sessions/{session_id}

Get current session state.

**Response (200):** same shape as session creation response.

---

### POST /v1/sessions/{session_id}/observations

Submit an RTML-style observation request.

**Request:**
```json
{
  "target": {"ra": 42.5, "dec": 15.3},
  "instrument": "imager",
  "filter": "h_alpha",
  "exposure_time": 300,
  "scheduling": {"priority": "medium"}
}
```

| Field               | Type    | Required | Notes                            |
|---------------------|---------|----------|----------------------------------|
| `target.ra`         | float   | yes      | Right ascension, 0–360           |
| `target.dec`        | float   | yes      | Declination, -90 to +90          |
| `instrument`        | string  | yes      | `imager`, `spectrograph`, `radio_receiver` |
| `filter`            | string  | no       | Optical filter (default: `clear`) |
| `exposure_time`     | float   | yes      | Seconds, 1–3600                  |
| `scheduling.priority` | string | no     | `low`, `medium`, `high`, `override` |

**Response (202):**
```json
{
  "job_id": "abc123def456",
  "status": "processing",
  "estimated_completion_secs": 5.0,
  "request": { ... }
}
```

---

### GET /v1/sessions/{session_id}/observations/{job_id}

Poll for observation results.

**While processing (200):**
```json
{
  "job_id": "abc123def456",
  "status": "processing",
  "progress": 0.65,
  "retry_after_secs": 1.75
}
```

**When complete (200):**
```json
{
  "job_id": "abc123def456",
  "status": "completed",
  "result": {
    "headers": {
      "SIMPLE": true,
      "TELESCOP": "SCOPE-A1B2C3",
      "INSTRUME": "Wide-Field Imager",
      "RA": 42.5,
      "DEC": 15.3,
      "EXPTIME": 300,
      "FILTER": "H_ALPHA",
      "DATE-OBS": "2026-03-14T04:22:00Z",
      "FOV-RAD": 1.5,
      "BUNIT": "mag"
    },
    "data": {
      "type": "image",
      "noise_floor_mag": 26.19,
      "fov_radius_deg": 1.5,
      "n_sources": 2,
      "detections": [
        {
          "source_id": "ngf-2",
          "name": "Kael's Star",
          "kind": "star",
          "ra": 42.8,
          "dec": 15.1,
          "magnitude": 4.1,
          "snr": 100.0,
          "offset_deg": 0.3285
        }
      ]
    }
  }
}
```

---

### GET /v1/sessions/{session_id}/observations

List all observations for this session.

**Response (200):**
```json
{
  "observations": [
    {
      "job_id": "abc123def456",
      "status": "completed",
      "instrument": "imager",
      "target": {"ra": 42.5, "dec": 15.3},
      "exposure_time": 300,
      "has_result": true
    }
  ]
}
```

---

### POST /v1/sessions/{session_id}/transmit

Broadcast a signal, making yourself more detectable to other players.

**Request:**
```json
{
  "power": 5.0
}
```

| Field   | Type  | Notes                     |
|---------|-------|---------------------------|
| `power` | float | 0.0 (silent) to 10.0 (max) |

**Response (200):**
```json
{
  "transmit_power": 5.0,
  "note": "Broadcasting increases your radio and optical detectability to other players."
}
```

---

### GET /v1/catalogue

Browse the public sky catalogue (fictional objects).

**Response (200):**
```json
{
  "objects": [
    {
      "id": "ngf-1",
      "name": "Lyrion Nebula",
      "kind": "nebula",
      "ra": 42.5,
      "dec": 15.3,
      "description": "A sprawling emission nebula..."
    }
  ]
}
```

---

## Data Types

### Image Detection
```json
{
  "source_id": "ngf-1",
  "name": "Lyrion Nebula",
  "kind": "nebula",
  "ra": 42.5,
  "dec": 15.3,
  "magnitude": 8.2,
  "snr": 45.3,
  "offset_deg": 0.0
}
```

### Radio Detection
```json
{
  "source_id": "ngf-3",
  "name": "Vorantis Pulsar",
  "kind": "pulsar",
  "ra": 128.7,
  "dec": -44.2,
  "flux_mJy": 850.0,
  "snr": 72.1,
  "offset_deg": 0.15,
  "periodic": true
}
```

### Spectrum Result
```json
{
  "type": "spectrum",
  "target_acquired": true,
  "source_id": "ngf-2",
  "name": "Kael's Star",
  "kind": "star",
  "spectrum_class": "G",
  "snr": 55.0,
  "features": {
    "lines": ["Ca II H&K absorption", "Fe I absorption", "H-alpha absorption"],
    "continuum": "solar-type, peak ~550nm",
    "snr_quality": "excellent"
  }
}
```

### Player Detection (via spectrum)
```json
{
  "type": "spectrum",
  "target_acquired": true,
  "source_id": "UNK-A1B2C3",
  "kind": "artificial",
  "spectrum_class": "non-thermal",
  "snr": 12.0,
  "features": {
    "lines": ["unidentified narrow emission"],
    "continuum": "flat, non-stellar",
    "classification_hint": "Possible artificial origin",
    "broadcast_detected": true
  }
}
```
