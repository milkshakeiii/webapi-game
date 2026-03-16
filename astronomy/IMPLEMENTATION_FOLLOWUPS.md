# Astronomy Implementation Follow-Ups

This document turns the current code review into a concrete follow-up plan.
It is not a rehash of the design proposal. It is a targeted list of changes
needed to make the first implementation line up with the intended gameplay.

The priorities below assume the current direction is:

- hunting reports are guess-only
- players may use external tooling to interpret observations
- jump charging should stay playable
- jamming should degrade the target's radio play rather than merely exposing them


## Priority Order

1. Hunt reports: make them explicitly guess-only
2. Jump timing: fix charged-hold timing
3. Jamming: make it inject target noise rather than target emissions
4. Broadcast state: fix `broadcast_power` so bursts are transient
5. Track output: expose enough geometry for external triangulation
6. Reward economy: add diminishing returns to raw observation rewards
7. Modules: wire declared module effects into runtime behavior
8. Science scoring: clean up freshness and payout semantics


## 1. Hunt Reports Should Be Guess-Only

### Current State

`_process_hunt_uplink()` currently expects `evidence_job_ids`, and contains a
partial evidence gate:

- fewer than 2 evidence jobs is rejected unless one cited job has `snr >= 50`
- 2 or more evidence IDs pass without further validation

Affected code:

- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L416)

### Agreed Direction

Hunt reports should not be server-authorized by evidence. The evidence is for the
player, not the rules engine. What matters is whether the submitted guess is right.

That means the server should score:

- submitted classification guess
- submitted position guess
- target truth at scoring time

and nothing else needs to be mandatory.

### Required Change

Remove evidence as a gating rule for hunt reports.

Possible v1 approaches:

- Preferred: remove `evidence_job_ids` from hunt scoring entirely and treat it as
  optional metadata for the client
- Acceptable: keep the field in the payload for future UI/debug use, but do not
  require or validate it

### Why This Matters

The current implementation sits in an awkward middle ground:

- it looks like evidence is required
- but the server does not actually bind the report to the evidence

That creates complexity without creating integrity.

If the real rule is "make a good call," the API should say that clearly.

### Acceptance Criteria

- A hunt report can be submitted with only:
  - `report_type`
  - `classification_guess`
  - `predicted_position_au`
- Hunt scoring outcome is unchanged by adding or omitting `evidence_job_ids`
- API docs describe hunting as a guess submission, not an evidence-validated claim

### Suggested Tests

- Hunt uplink succeeds without `evidence_job_ids`
- Hunt uplink with `evidence_job_ids` produces the same result as the same guess
  without them


## 2. Fix Charged-Hold Timing

### Current State

Jump charge completion is currently materialized inside `check_jump()`.

Affected code:

- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L120)
- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L585)

Right now:

- `start_jump()` creates the charge job
- the session stays in `jump_charging`
- the first later call to `check_jump()` flips state to `jump_charged`
- `charged_at` is set to that poll time

This lets a player delay the first poll and effectively delay the start of the
charged-hold timeout window.

### Required Change

State transitions should happen in `_tick()`, not in the status endpoint.

Implementation change:

- when `now >= started_at + charge_duration_sec`, transition to `jump_charged`
- set `charged_at = started_at + charge_duration_sec`
- `check_jump()` should only report the current state
- auto-abort should measure hold time from the real completion instant

### Why This Matters

This is a real gameplay bug, not a design question.

The current behavior means the 30-second hold limit is not actually 30 seconds
from charge completion. It is 30 seconds from the first status poll.

### Acceptance Criteria

- If a charge should have completed 45 seconds ago, the session is already either
  `jump_charged` or auto-aborted before the player polls
- Poll timing does not alter hold duration
- `check_jump()` is read-only with respect to jump-state progression

### Suggested Tests

- Charge completes without calling `check_jump()`
- Auto-abort triggers based on real completion time, not first poll time
- `check_jump()` after a long idle period reports an already-expired charged state
  correctly


## 3. Rework Jamming Semantics

### Current State

The current jam implementation mainly:

- makes the jammer louder, which is correct
- adds `js * 0.5` to the target's `radio_emissions`, which is not correct
- stores jam strength for jump navigation scatter during charge

Affected code:

- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L731)
- [telescope.py](/Users/henry/Documents/github/webapi-game/astronomy/telescope.py#L412)

### Agreed Direction

Jamming should:

- make the jammer easier to detect
- inject noise into the target's radio environment
- degrade the target's radio observations and uplink quality
- degrade jump arrival precision if they commit under jam

It should not work by making the target emit more.

### Required Change

Replace "jam increases target radio emissions" with temporary jam state on the
target session/player.

Recommended v1 model:

- jammer action computes `jam_strength` against targets in cone
- target session receives a temporary jam effect with:
  - magnitude
  - expiry timestamp
- radio observation path adds jam strength to the target observer's radio noise floor
- hunt/science uplinks can optionally suffer reduced reliability, extra delay, or
  outright disruption when jammed
- jump commit uses jam strength to increase arrival sigma

### Suggested Data Model

Session-side fields:

- `radio_jam_until`
- `radio_jam_strength`

Optional if you want multiple overlapping jammers:

- a list of active jam effects with independent expiry

### Why This Matters

The current behavior inverts the intended gameplay. The target becomes more
visible, but not more confused.

The intended fantasy is:

- "I am shouting to ruin your measurements"

not:

- "I pressed jammer, therefore you now shout louder."

### Acceptance Criteria

- Using the jammer increases the jammer's own detection risk
- A jammed target gets worse radio observation quality
- A jammed target gets worse uplink quality and/or jump precision
- Jamming does not directly increase the target's emitted radio signature

### Suggested Tests

- Jammer activation raises jammer radio signature
- Jammed target sees higher effective radio noise floor on subsequent radio jobs
- Jammed jump commit produces larger navigation error than unjammed commit
- Jammed target is not made intrinsically easier to detect just by being jammed


## 4. Fix `broadcast_power`

### Current State

`broadcast_power` is a standing player field used for deliberate transmitting.

Affected code:

- [sky.py](/Users/henry/Documents/github/webapi-game/astronomy/sky.py#L109)
- [sky.py](/Users/henry/Documents/github/webapi-game/astronomy/sky.py#L296)
- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L260)
- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L315)
- [telescope.py](/Users/henry/Documents/github/webapi-game/astronomy/telescope.py#L461)
- [telescope.py](/Users/henry/Documents/github/webapi-game/astronomy/telescope.py#L510)

Current problems:

- `uplink()` raises it like a temporary radio spike
- `transmit()` sets it deliberately
- nothing decays or expires it
- radio and even optical detection treat it as a persistent contribution

### Agreed Direction

There are two different concepts mixed together:

- sustained deliberate broadcasting
- brief uplink bursts

They should not share the same permanent field.

### Required Change

Split these concepts.

Recommended v1 model:

- keep `broadcast_power` only for a deliberate, sustained `/transmit` mode
- add a short-lived uplink burst state for `uplink()`, for example:
  - `radio_burst_power`
  - `radio_burst_until`

At minimum:

- `uplink()` should create a burst with expiry
- `tick_player()` should clear expired bursts
- `_player_optical_brightness()` should stop adding radio broadcast power into optical flux

### Why This Matters

The current implementation turns "I just uplinked" into "I remain a beacon until
something manually overwrites the field."

That is almost certainly a bug, not a balancing choice.

### Acceptance Criteria

- Uplink creates a temporary radio signature window
- That window decays automatically
- Manual sustained transmit remains possible only if explicitly intended
- Radio broadcast does not directly inflate optical brightness

### Suggested Tests

- Uplink burst is detectable immediately after submit
- Uplink burst expires after its intended duration
- Optical detection is unchanged by radio-only burst state


## 5. Support External Triangulation

### Current State

Track files currently summarize apparent RA/Dec evidence and flux summary, but
they do not expose enough raw geometry to cleanly support external solving.

Affected code:

- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L186)
- [tracks.py](/Users/henry/Documents/github/webapi-game/astronomy/tracks.py#L75)

### Agreed Direction

Players may use external tooling, including AI tooling, to infer target position.
That is acceptable and may even be part of the fun.

The server therefore does not need to provide solved 3D tracks. It does need to
provide enough measurement geometry for a solver to work.

### Required Change

Expose per-evidence geometry cleanly in track files or observation outputs.

Minimum useful fields per evidence item:

- observation epoch
- observer position at observation time
- apparent RA
- apparent Dec
- uncertainty
- instrument

Helpful optional additions:

- region at observation time
- noise floor
- scan profile
- light-time estimate

### Why This Matters

If the game expects inference, then the raw measurements have to be portable.
Otherwise the player is asked to solve a problem without being given the data in a
reusable form.

### Acceptance Criteria

- A client can reconstruct the observation geometry for each track evidence point
- Track files remain inference-oriented and do not reveal hidden truth
- No server-side automatic "this is the right 3D answer" is required

### Suggested Tests

- Track file output includes observer position and observation epoch for each evidence item
- Track file output still excludes hidden labels or truth coordinates


## 6. Add Diminishing Returns To Raw Observation Rewards

### Current State

Observation rewards are still mostly per-detection flat payouts.

Affected code:

- [telescope.py](/Users/henry/Documents/github/webapi-game/astronomy/telescope.py#L228)
- [telescope.py](/Users/henry/Documents/github/webapi-game/astronomy/telescope.py#L429)
- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L186)

This means repeated catalogue sweeps can still farm `data` without requiring new
questions or materially better measurements.

### Required Change

Move novelty logic into the raw observation reward path as well.

Possible v1 rule:

- first useful detection of target in session: full reward
- reacquisition of same target: reduced reward
- same target with materially better precision: partial reward
- same target with new modality or new question opened: moderate reward
- repeated identical sweep: near-zero reward

This can remain much simpler than the science-report scoring model, but it should
not be flat.

### Why This Matters

Without this, the economy still trends toward static farming, even if the later
science-uplink scoring is smarter.

### Acceptance Criteria

- Repeating the same easy scan path yields sharply declining `data`
- Better precision or new information can still pay
- Opportunity targets and changing sources remain worth revisiting

### Suggested Tests

- identical repeat scan yields less `data` than the first
- improved SNR or new target question yields more than a stale repeat


## 7. Wire The Declared Module System Into Runtime Behavior

### Current State

Module definitions are present, but most effects are not actually applied.

Affected code:

- [modules.py](/Users/henry/Documents/github/webapi-game/astronomy/modules.py#L19)
- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L550)
- [telescope.py](/Users/henry/Documents/github/webapi-game/astronomy/telescope.py#L120)

Right now:

- `ghost_drive` is partly wired in
- `directional_jammer` is wired in
- `target_illuminator` partly affects spectrograph FOV
- most other passive/active effects remain declarative only

### Required Change

Implement or cut incomplete module effects.

Short version:

- if a module exists in the public API, it should have clear gameplay impact
- if not implemented yet, remove it from the exposed loadout list until ready

Most important missing passive behavior:

- `cold_baffles`
- `signal_scrubber`
- `phase_change_sink`
- `expanded_cache`

Most important missing active behavior:

- `wideband_ping`
- `burst_uplink`
- `decoy_beacon`

### Why This Matters

Right now the module list implies more tactical depth than the runtime actually has.
That creates confusion during testing and balancing.

### Acceptance Criteria

- every exposed module has a real, testable effect
- or it is removed from the exposed API until implemented


## 8. Clean Up Science Scoring Semantics

### Current State

Science uplinks broadly work, but there are two semantic issues:

- freshness is computed as `now - receipt_time`, which will usually be negative
- scored science reports currently pay directly into `credits`/`intel`, which may
  not match the intended `data -> uplink -> credits` economy cleanly

Affected code:

- [sessions.py](/Users/henry/Documents/github/webapi-game/astronomy/sessions.py#L331)

### Required Change

Clarify the intended science economy:

- If science uplinks are the banking action, make the rewards land in the intended
  post-uplink currency path
- If science reports are meant to generate `data` first, preserve that distinction

Also fix freshness to use an actually meaningful staleness measure.

Examples:

- time since observation
- time since target truth moved materially
- age of the estimate relative to receipt time

### Acceptance Criteria

- freshness decreases as reports get older, not the other way around
- science payout semantics match the intended economy model


## Recommended First Patch Group

The most valuable first implementation pass is:

1. remove hunt evidence gating
2. fix charged-jump timing
3. rework jamming into target noise instead of target emissions
4. fix `broadcast_power` by separating sustained transmit from short radio bursts

That patch group closes the biggest gameplay mismatches without reopening the whole
economy or content model.


## Notes On Scope

Not every item here needs to land before playtesting continues.

The hard blockers for a coherent stealth-hunt loop are:

- item 2: charged-jump timing
- item 3: jamming semantics
- item 4: radio burst persistence

Items 5 through 8 are important, but they are closer to "make the loop robust and
deep" than "make the loop conceptually correct."
