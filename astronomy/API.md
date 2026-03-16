# Astronomy Observation Game — API Reference

A web API game where you operate a telescope craft in a shared solar system.
Submit observations, manage heat and signatures, bank discoveries via uplink,
hunt rival players, and jump between regions.

**Base URL:** `http://localhost:8080`

---

## Quick Start

```bash
# 1. Create a session
curl -s -X POST localhost:8080/v1/sessions | python3 -m json.tool

# 2. Check the system regions
curl -s localhost:8080/v1/system/regions | python3 -m json.tool

# 3. Submit an observation
curl -s -X POST localhost:8080/v1/sessions/{SESSION_ID}/observations \
  -d '{
    "target": {"ra": 38.57, "dec": -7.11},
    "instrument": "imager",
    "filter": "clear",
    "exposure_time": 300,
    "scan_profile": "survey"
  }' | python3 -m json.tool

# 4. Wait, then fetch results
curl -s localhost:8080/v1/sessions/{SESSION_ID}/observations/{JOB_ID} | python3 -m json.tool

# 5. Bank your data via uplink (loud radio event!)
curl -s -X POST localhost:8080/v1/sessions/{SESSION_ID}/uplink \
  -d '{"report_type": "science"}' | python3 -m json.tool

# 6. Jump to a new position
curl -s -X POST localhost:8080/v1/sessions/{SESSION_ID}/jump \
  -d '{"destination_au": {"x": 0.01, "y": -0.02, "z": 0.0}, "charge_profile": "standard"}' \
  | python3 -m json.tool
```

---

## Core Loop

1. **Move** to a solar-system region based on backgrounds, relay access, and targets.
2. **Scan** with an instrument, optionally using a scan profile or active module.
3. **Gain** `data` and `intel` from discoveries (unbanked at first).
4. **Decide** whether to stay dark, keep farming, charge a jump, jam a target, or uplink.
5. **Uplink** to bank data as credits — but uplinking is a loud radio event.
6. **Other players** can detect your signatures and uplink hunting reports against you.

The key tension: the best rewards come from high-output actions, and those actions are noisy.

---

## Session State

Sessions track economy, physical state, signatures, loadout, and jump state.

```json
{
  "session_id": "a1b2c3d4e5f6",
  "telescope": {
    "id": "SCOPE-A1B2C3",
    "position_au": {"x": -0.015, "y": 0.001, "z": 0.003},
    "transmit_power": 0.0
  },
  "region": "quiet-dark",
  "economy": {
    "credits": 15,
    "unbanked_data": 30,
    "intel": 5
  },
  "physical_state": {
    "power_draw": 1.0,
    "stored_heat": 0.12,
    "heat_sink_capacity": 1.0,
    "radiator_mode": "balanced"
  },
  "signatures": {
    "radio_emissions": 5.0,
    "optical_glint": 0.1,
    "jump_charge_emission": 0.0,
    "arrival_bloom": 0.0
  },
  "loadout": {
    "passive_modules": ["cold_baffles"],
    "active_modules": []
  },
  "jump_state": "idle",
  "snr_multiplier": 1.0,
  "observations_submitted": 3,
  "instruments": ["imager", "spectrograph", "radio_receiver"],
  "filters": ["clear", "r_band", "b_band", "h_alpha", "oiii"],
  "scan_profiles": ["low_power", "survey", "boosted", "overclocked"]
}
```

### Currencies

| Currency | Source | Persistence |
|----------|--------|-------------|
| `credits` | Banked via uplink | Permanent |
| `unbanked_data` | Earned from observations | Lost if hunted |
| `intel` | Hunting reports, rare finds | Permanent |

### Physical State

| Field | Meaning |
|-------|---------|
| `power_draw` | Current electrical load (affects timing leakage) |
| `stored_heat` | Accumulated waste heat (must be radiated) |
| `radiator_mode` | `sealed` / `balanced` / `venting` |

### Signatures

Every action has a physical signature cost. Signatures drive detectability:
- **radio_emissions**: leakage + deliberate broadcast + timing noise
- **optical_glint**: aperture reflection + active illumination
- **jump_charge_emission**: broadband field signature during jump charge
- **arrival_bloom**: brief EM/thermal transient after jump

---

## Instruments

| Instrument | FOV | Wavelength | Role |
|------------|-----|------------|------|
| `imager` | 1.5° | Optical | Survey, astrometry, spotting radiators |
| `spectrograph` | 0.05° | Optical | Classification, material identification |
| `radio_receiver` | 3.0° | Radio | First contact, wide-area sweeps, leakage detection |

## Filters

| Filter | Throughput | Notes |
|--------|------------|-------|
| `clear` | 100% | Broadband, maximum depth |
| `r_band` | 80% | Red optical |
| `b_band` | 70% | Blue optical |
| `h_alpha` | 30% | Narrow-band; emission objects glow brighter |
| `oiii` | 25% | Narrow-band; emission objects glow brighter |

## Scan Profiles

| Profile | SNR | Power | Heat | Leakage |
|---------|-----|-------|------|---------|
| `low_power` | 0.7x | 0.5x | 0.4x | 0.3x |
| `survey` | 1.0x | 1.0x | 1.0x | 1.0x |
| `boosted` | 1.4x | 1.8x | 2.0x | 1.5x |
| `overclocked` | 1.8x | 3.0x | 4.0x | 3.0x |

## Radiator Modes

| Mode | Heat Rejection | IR Signature |
|------|---------------|--------------|
| `sealed` | Very slow | 0.2x (dim) |
| `balanced` | Steady-state | 1.0x |
| `venting` | Fast dump | 3.5x (bright) |

---

## Endpoints

### POST /v1/sessions

Create a new telescope session. Your craft spawns in a region.

**Response (201):** Session state (see above).

---

### GET /v1/sessions/{session_id}

Get current session state with ticked physics.

---

### POST /v1/sessions/{session_id}/observations

Submit an observation. Generates heat and adjusts power draw.

**Request:**
```json
{
  "target": {"ra": 38.57, "dec": -7.11},
  "instrument": "imager",
  "filter": "clear",
  "exposure_time": 300,
  "scan_profile": "boosted",
  "scheduling": {"priority": "medium"}
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `target.ra` | float | yes | Right ascension, 0–360 |
| `target.dec` | float | yes | Declination, -90 to +90 |
| `instrument` | string | yes | `imager`, `spectrograph`, `radio_receiver` |
| `filter` | string | no | Default: `clear` |
| `exposure_time` | float | yes | 1–3600 seconds |
| `scan_profile` | string | no | Default: `survey` |
| `scheduling.priority` | string | no | `low`, `medium`, `high`, `override` |

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

Poll for observation results. Results include detection IDs, uncertainty,
light-time delay, catalogue cross-matches, and rewards.

**Image detection:**
```json
{
  "detection_id": "det-img-a1b2c3",
  "source_id": "ngf-2",
  "name": "Kael's Star",
  "kind": "star",
  "apparent_ra_deg": 38.57,
  "apparent_dec_deg": -7.11,
  "uncertainty_arcsec": 0.3,
  "flux": {"optical_mag": 4.1},
  "snr": 100.0,
  "light_time_sec": 7.42,
  "catalogue_matches": [{"target_id": "ngf-2", "confidence": 1.0}]
}
```

**Player detection (no catalogue match, no label):**
```json
{
  "detection_id": "det-img-d4e5f6",
  "apparent_ra_deg": 42.51,
  "apparent_dec_deg": 15.29,
  "uncertainty_arcsec": 12.4,
  "flux": {"optical_mag": 18.2},
  "shape_hint": "point",
  "snr": 2.4,
  "catalogue_matches": [],
  "motion_hint": {"broadband_charge_detected": true}
}
```

**Radio detection:**
```json
{
  "detection_id": "det-rad-a1b2c3",
  "apparent_ra_deg": 338.87,
  "apparent_dec_deg": -18.32,
  "uncertainty_arcmin": 0.5,
  "flux_mJy": 714675.97,
  "snr": 100.0,
  "bandwidth_hz": 2000,
  "spectral_slope": -0.5,
  "burstiness": 0.0,
  "catalogue_matches": [{"target_id": "ngf-3", "confidence": 1.0}]
}
```

---

### POST /v1/sessions/{session_id}/uplink

Bank data or submit a hunting report. **Loud radio event.**

**Science uplink** (bank unbanked_data → credits):
```json
{"report_type": "science"}
```

**Hunting uplink** (guess a rival's position):
```json
{
  "report_type": "hunt",
  "classification_guess": "artificial",
  "predicted_position_au": {"x": 0.842, "y": -0.114, "z": 0.006}
}
```

**Hunting response:**
```json
{
  "report_id": "rep-77a1",
  "status": "accepted",
  "report_type": "hunt",
  "score": {
    "position_error_au": 0.00008,
    "classification_match": true,
    "effective_hit_score": 0.84
  },
  "rewards": {"intel": 84},
  "target_effect": {
    "data_loss_fraction": 0.39,
    "relay_scrutiny_sec": 127,
    "uplink_disrupted": true
  }
}
```

Anti-spam: cooldowns (30s science, 90s hunt) and steep Gaussian position-error falloff.

---

### POST /v1/sessions/{session_id}/radiators

Set thermal posture.

```json
{"mode": "venting"}
```

---

### POST /v1/sessions/{session_id}/loadout

Equip passive and active modules.

```json
{
  "passive_modules": ["cold_baffles", "signal_scrubber"],
  "active_modules": ["directional_jammer"]
}
```

**Passive modules:** `cold_baffles`, `signal_scrubber`, `phase_change_sink`, `expanded_cache`, `ghost_drive` (max 2)

**Active modules:** `deep_field_overclock`, `wideband_ping`, `directional_jammer`, `target_illuminator`, `burst_uplink`, `decoy_beacon` (max 1, upgradable to 2)

---

### POST /v1/sessions/{session_id}/jump

Start charging a jump to a new position. **Loudest thing the ship can do.**

```json
{
  "destination_au": {"x": 0.01, "y": -0.02, "z": 0.0},
  "charge_profile": "standard"
}
```

| Profile | Charge Time | Signature | Thermal | Nav Sigma |
|---------|-------------|-----------|---------|-----------|
| `cold_spool` | 1.8x | 0.7x | 0.8x | 0.8x |
| `standard` | 1.0x | 1.0x | 1.0x | 1.0x |
| `emergency` | 0.55x | 1.8x | 1.5x | 1.8x |

Observations remain available during charge. Players can abort at any time.

---

### GET /v1/sessions/{session_id}/jump/{job_id}

Check jump charge status.

---

### POST /v1/sessions/{session_id}/jump/{job_id}/commit

Commit the jump. Instant relocation with arrival bloom and recalibration period.

---

### DELETE /v1/sessions/{session_id}/jump/{job_id}

Abort the jump. Thermal debt is still paid.

---

### POST /v1/sessions/{session_id}/jam

Activate the directional jammer (requires module equipped).

```json
{"target_ra": 42.5, "target_dec": 15.3}
```

---

### POST /v1/sessions/{session_id}/transmit

Legacy broadcast signal endpoint.

```json
{"power": 5.0}
```

---

### GET /v1/sessions/{session_id}/track-files

List aggregated track files for this session.

---

### GET /v1/system/regions

List solar system regions with physical backgrounds.

```json
{
  "regions": [
    {
      "id": "quiet-dark",
      "name": "Quiet Dark",
      "description": "Open space far from clutter...",
      "ir_background": 0.05,
      "radio_noise": 5.0,
      "dust_opacity": 0.02,
      "solar_flux": 0.15,
      "relay_coverage": 0.4,
      "center_au": {"x": -0.02, "y": 0.015, "z": 0.005},
      "radius_au": 0.02
    }
  ]
}
```

---

### GET /v1/catalogue

Browse the public sky catalogue.

---

## Detection Model

All sources (catalogue objects, anomalies, players) use one detection pipeline:

1. Compute apparent position from observer's 3D location
2. Check if within instrument FOV
3. Apply inverse-square flux falloff with distance
4. Compare against noise floor (modified by region, dust, radio noise)
5. Apply scan profile SNR multiplier and recalibration penalty
6. Return measurements with uncertainty — never labels

Player detection relies on interpreting evidence:
- No catalogue match → unknown source
- Non-thermal spectrum → possible artificial origin
- Broadband charge signature → possible jump charging
- Narrowband radio → possible deliberate transmission

Identification is the player's job, not the API's.
