# Astronomy Game Design Proposal

## Summary

The current astronomy game already has a strong technical fantasy: players submit
observations, wait for async results, and occasionally detect other telescopes as
unidentified sources. What it lacks is stake. Detecting things does not feed a
progression loop, being detected has no real cost, `transmit` is mostly downside,
and there is no meaningful notion of relocation or territory.

This proposal adds four systems that deepen the game without breaking its API-first
shape:

1. A risked-reward progression loop built around unbanked discoveries.
2. A stealth and exposure model where active power creates readable tradeoffs.
3. A contact pipeline that turns player detection into a hunt instead of a novelty.
4. A simple sector-based movement layer that creates route choice without real-time flight.


## Design Goals

- Keep the core verb readable: point, scan, poll, decide.
- Make every high-value action ask, "Is this worth the signature spike?"
- Reward detection of both catalogue objects and rival players.
- Punish exposure in ways that feel sharp but not run-ending.
- Preserve the current instruments and let each one own a distinct PvP/PvE role.
- Add movement as an asynchronous strategic choice, not a piloting minigame.


## Current Gaps

- Observation results are interesting, but they do not create durable progress.
- Detecting another player is flavorful, but there is no bounty, follow-up chain, or consequence.
- `POST /transmit` raises detectability, but it does not unlock a meaningful upside.
- Every player lives in one shared sky, so there is no reason to relocate.
- Instruments differ by field of view and wavelength, but not by tactical role in a larger loop.


## Proposed Core Loop

1. Move to a sector based on concealment, traffic, hazards, and available targets.
2. Scan with an instrument and optionally activate a module to push for more yield.
3. Gain `data` and `intel` from discoveries, but keep them unbanked at first.
4. Decide whether to stay dark, keep farming, chase a contact, or uplink the haul.
5. Each aggressive action raises `exposure`, making later detections more accurate.
6. If another player fully profiles you, or local security reacts to your exposure,
   you lose unbanked value and may be forced to reposition.

The key tension is simple: the best rewards come from high-output actions, and the
best high-output actions are noisy.


## Progression And Economy

### Currencies

- `credits`: banked currency used for module unlocks, loadout slots, and better travel options.
- `data`: unbanked value earned from catalogue scans, anomaly detections, and survey chains.
- `intel`: higher-tier currency earned from fully profiling artificial signals, rival players, or rare anomalies.

### Reward Sources

- First detection of a catalogue object in a session: small `data` reward.
- First high-SNR detection: bonus `data`.
- Spectral classification after detection: medium `data` reward.
- Multi-instrument profile of the same source: `intel` bonus.
- Detection chain on rival players: largest `intel` rewards.
- Sector contracts: directed objectives that reward the player for using different tools.

### Banking

Observations do not directly turn into permanent value. They first become `data`
stored on the ship.

- `data` is safe only after an uplink or bank action.
- Carrying more unbanked `data` should feel profitable and dangerous.
- Losing detection contests should primarily cost unbanked `data`, not long-term unlocks.

This makes stealth matter without making one bad interaction erase permanent progress.

### Diminishing Returns

To avoid solved farming routes:

- Repeated scans of the same static source pay sharply less after first classification.
- Sector contracts rotate.
- Transient anomalies and artificial traces create high-value windows that move players around.


## Exposure, Detection, And Penalties

### Exposure Model

Each session tracks two visible risk channels:

- `radio_exposure`
- `optical_exposure`

Actions add to one or both channels:

- Long exposures: small optical gain.
- Radio scans: small radio gain.
- `transmit` / uplink actions: large radio gain.
- Fast travel: medium radio and optical gain.
- High-power active modules: large gain in the matching channel.

Exposure decays slowly while the player stays quiet or uses low-signature movement.

### Contact States

Player hunting should happen in stages, not from one lucky scan:

1. `contact`: an unidentified source is seen in one band.
2. `track`: repeated detections shrink positional jitter and reveal the current sector.
3. `profile`: multi-band or spectrographic confirmation identifies the target as artificial and awards `intel`.
4. `compromised`: a profiled target that is already running high exposure suffers a penalty event.

This keeps PvP readable and gives the hunted player time to react.

### Penalties For Being Detected

Penalties should be meaningful but recoverable:

- Lose a percentage of unbanked `data`.
- Gain temporary observation jamming, increasing job duration or failure chance.
- Reveal your sector to nearby rivals for a limited time.
- Trigger an emergency relocation if exposure stays above a threshold.

Penalty severity should scale with how compromised the player was when profiled.
One weak sighting should never be enough to wipe someone.


## Instrument Roles In The Deeper Game

The existing tools already map well to a richer loop:

- `imager`: best for precise localization, survey income, and low-drama scouting.
- `radio_receiver`: best for first contact on rivals, sector sweeps, and finding broadcast-heavy targets.
- `spectrograph`: best for converting a track into a profile and claiming the big reward.

That gives each instrument a clear place in both PvE discovery and PvP hunting.


## Stealth Features And Active Modules

The module system should make power explicit. Passive modules improve consistency.
Active modules create spikes in reward and spikes in risk.

### Loadout Structure

- 2 passive slots
- 1 active slot at start
- Additional active slot unlockable later

### Passive Modules

Passive modules shape a playstyle without forcing constant input:

- `cold_baffles`: lower optical exposure gain, but slightly reduce imaging depth.
- `signal_scrubber`: lower radio exposure gain, but increase job processing time.
- `expanded_cache`: hold more unbanked `data`, but gain a larger penalty when compromised.
- `ghost_drive`: reduce exposure from travel, but occupy a slot that could improve scans.

### Active Modules

Active modules should feel tempting because they are strong:

| Module | Benefit | Risk / Cost |
|---|---|---|
| `deep_field_overclock` | Better limiting magnitude or radio sensitivity for one observation | Large exposure spike and longer cooldown |
| `wideband_ping` | Instant weak contacts across the current sector | Massive radio exposure; reveals your own sector |
| `target_illuminator` | Wider spectrograph lock or higher acquisition chance | Optical exposure spike; easier to image by rivals |
| `burst_uplink` | Bank `data` from unsafe space immediately | Huge radio exposure and visible transmission event |
| `decoy_beacon` | Creates a false contact to waste rival scans | Moderate radio exposure and consumable charge |

The important rule is that active modules should never be "free efficiency." If a
module meaningfully improves yield, its detection cost should be legible in the API.

### Scan Profiles

To add nuance without a large item catalog, every observation can also take a
scan profile:

- `silent`: lower exposure gain, lower detection power
- `standard`: baseline
- `focused`: better SNR or contact accuracy, higher exposure
- `aggressive`: strongest result shaping, very high exposure

This creates tactical choice even before a player has many unlocks.


## Movement: Sector-Based Repositioning

Movement should be strategic, asynchronous, and easy to understand.

### World Structure

Replace the single shared sky with a small galaxy map of sectors. Each sector has:

- `concealment`: how quickly exposure decays there
- `traffic`: how likely rival players are to appear
- `hazard`: environmental modifiers to scans
- `content_bias`: what objects, anomalies, or contracts are common there

Players only directly interact with other players in the same sector.

### Travel Modes

- `drift`: slow, low exposure, good for escaping with a full cache
- `burn`: medium speed, medium exposure
- `hot_jump`: fast, high exposure, often used in emergencies

Travel should use the same asynchronous job feel as observations. While moving,
the player cannot observe, but arrival can clear part of their exposure.

### Why Movement Matters

- Lets players leave a dangerous sector instead of waiting to be farmed.
- Creates safer and riskier hunting grounds.
- Gives value to stealth-oriented routes and travel upgrades.
- Prevents the game from collapsing into one solved observation spot.

### Example Sector Themes

- `Dust Veil`: high optical concealment, worse optical depth, strong anomaly rate
- `Relay Spine`: cheap uplinks, excellent radio scans, very dangerous for stealth
- `Quiet Dark`: low traffic, slow progression, best place to cool off exposure
- `Broken Array`: excellent player hunting, frequent jamming hazards


## Contracts And Dynamic Content

Static catalogue objects are a good foundation, but the game needs rotating reasons
to move and take risks.

Add simple contracts such as:

- "Classify any emission object with `h_alpha` in Dust Veil."
- "Profile one artificial source in Relay Spine."
- "Complete an image -> radio -> spectrum chain on a single anomaly."

Also add transient contacts:

- unstable radio bursts
- temporary artificial relays
- rare hidden objects that only appear after overclocked scans

These do not need a huge content system. A small procedural layer on top of the
existing catalogue would already make the game much less static.


## API And Data Model Implications

The design fits the existing HTTP pattern. Most changes are additive.

### Session State

Extend `GET /v1/sessions/{session_id}` with:

- `sector`
- `credits`
- `unbanked_data`
- `intel`
- `radio_exposure`
- `optical_exposure`
- `active_modules`
- `passive_modules`
- `travel_status`

### Observation Request

Extend `POST /v1/sessions/{session_id}/observations` with optional:

- `scan_profile`
- `active_module`

Observation results should include:

- `rewards`
- `exposure_gained`
- `contact_updates`
- `new_contract_progress`

### New Endpoints

- `GET /v1/galaxy/sectors`
- `POST /v1/sessions/{session_id}/move`
- `GET /v1/sessions/{session_id}/contacts`
- `POST /v1/sessions/{session_id}/bank`

`POST /v1/sessions/{session_id}/transmit` can remain, but it should become a more
explicit family of risky actions such as `uplink`, `broadcast`, or `decoy`.

### Model Changes

- `Sky` becomes a `Galaxy` containing sector-local sky states.
- `Session` gains progression, exposure, loadout, and travel fields.
- `PlayerSource` gains sector membership plus explicit signature values.
- Observation processing can return reward and exposure metadata alongside FITS-style results.


## Recommended Implementation Order

### Phase 1: Add Stakes

- Add `credits`, `unbanked_data`, and `intel`.
- Make observations award value.
- Make `transmit` or a new `bank` action convert `unbanked_data` into `credits`.
- Add exposure meters and basic loss on compromise.

This already creates a real loop with minimal surface-area growth.

### Phase 2: Add Contact Depth

- Introduce contact states: `contact`, `track`, `profile`, `compromised`.
- Make instruments contribute differently to player hunts.
- Award `intel` for full player profiles.

### Phase 3: Add Modules

- Add passive and active slots.
- Implement 3-5 modules with very visible risk/reward.
- Surface exposure gain clearly in responses.

### Phase 4: Add Movement

- Split the sky into sectors.
- Add travel jobs and sector modifiers.
- Gate player interaction by sector.

### Phase 5: Add Dynamic Objectives

- Introduce rotating contracts and transient anomalies.
- Use them to prevent static farming and keep sectors alive.


## Balance Guardrails

- Detection should mostly threaten unbanked value and temporary tempo, not permanent unlocks.
- Exposure changes must be transparent in the API response so players can learn the system.
- Stealth play should be slower, not invalid.
- Aggressive play should be more profitable, not strictly better.
- Movement should be an exit valve from pressure, not a chore tax.


## Net Effect

With these changes, the astronomy game becomes a layered hunt-and-survey game:

- PvE scanning builds your haul.
- PvP detection creates high-value hunts.
- Banking turns progress into a risk decision.
- Active modules create real temptation.
- Sector movement makes location matter.

That keeps the current observatory fantasy intact while giving the game the missing
depth, stakes, and replayability.
