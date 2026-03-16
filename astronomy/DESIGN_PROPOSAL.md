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
2. A simulated signature model where power draw, waste heat, and active emissions
   naturally make you easier to detect.
3. A guess-and-uplink loop that turns player detection into an astrometric hunt
   instead of a novelty.
4. A jump-drive movement layer that eliminates dead transit time while making
   charge signatures and arrival blooms major tactical events.


## Design Goals

- Keep the core verb readable: point, scan, poll, decide.
- Make every high-value action ask, "What physical signature am I creating to get this result?"
- Reward detection of both catalogue objects and rival players.
- Use one physical detection model for stars, anomalies, and players.
- Avoid hidden threat meters; detectability should come from heat, radio leakage, light, and motion.
- Never auto-reveal "this is a player"; make identification a matter of interpreting evidence and submitting reports.
- Keep the setting to one solar system so light-time delays remain playable and physically coherent.
- Preserve the current instruments and let each one own a distinct PvP/PvE role.
- Avoid dead movement downtime; jump prep should remain playable.
- Add movement as an asynchronous strategic choice, not a piloting minigame.


## Current Gaps

- Observation results are interesting, but they do not create durable progress.
- Detecting another player is flavorful, but there is no bounty, follow-up chain, or consequence.
- `POST /transmit` raises detectability, but it does not unlock a meaningful upside.
- Player detectability is mostly hand-authored instead of emerging from power use, heat, and emissions.
- The game does not yet turn uncertain observation data into a skill-based inference and reporting loop.
- Every player lives in one shared sky, so there is no reason to relocate.
- Instruments differ by field of view and wavelength, but not by tactical role in a larger loop.


## Proposed Core Loop

1. Move to a solar-system region based on local backgrounds, relay access, hazards, and available targets.
2. Scan with an instrument and optionally activate a module to push for more yield.
3. Gain `data` and `intel` from discoveries, but keep them unbanked at first.
4. Decide whether to stay dark, keep farming, start charging a jump, jam a target, or uplink the haul.
5. Each aggressive action draws more power, dumps more waste heat, or emits more
   radio and optical signature, making later detections more accurate.
6. If another player uplinks an accurate fix on you, especially while you are doing
   something loud like an uplink, radiator flare, or jump charge, you lose unbanked
   value and may be forced to reposition.

The key tension is simple: the best rewards come from high-output actions, and the
best high-output actions are noisy.


## Progression And Economy

### Currencies

- `credits`: banked currency used for module unlocks, loadout slots, and mobility upgrades.
- `data`: unbanked value earned from catalogue scans, anomaly detections, and survey chains.
- `intel`: higher-tier currency earned from successful artificial-source reports,
  accurate trajectory predictions, rival-player fixes, or rare anomalies.

### Reward Sources

- First useful detection or reacquisition of a target in a session: small `data` reward.
- Improving a hidden-state estimate such as position, spin, thermal state, or outgassing: core `data` reward.
- Spectral, thermal, or material classification after detection: medium `data` reward.
- Accurate uplinked position reports on rival players: largest `intel` rewards.
- Correctly predicting a target's current position from stale data: extra `intel`.
- Regional contracts: directed objectives that reward the player for using different tools.

### Banking

Observations do not directly turn into permanent value. They first become `data`
stored on the ship.

- `data` is safe only after an uplink action.
- Carrying more unbanked `data` should feel profitable and dangerous.
- Losing detection contests should primarily cost unbanked `data`, not long-term unlocks.

This makes stealth matter without making one bad interaction erase permanent progress,
especially because cashing out is itself a loud, physically detectable action.

### Diminishing Returns

To avoid solved farming routes:

- Same target, same question, same geometry, same time window should pay sharply less.
- Better precision on the same question should still pay, but with diminishing returns.
- New questions on the same target, or the same question after the target has physically changed, should restore value.
- Regional contracts rotate.
- Transient anomalies and artificial traces create high-value windows that move players around.

### Target Types

The baseline economy should come from targets that can be monitored, modeled, and
re-observed over time. The farmable thing is not the object itself. It is the hidden
state of the object.

#### Baseline Monitoring Targets

These are the steady, low- to medium-risk targets that keep the economy running:

- catalogue asteroids and minor moons
- comets and outgassing bodies
- dust bands, debris clusters, and ring features
- derelicts, old probes, and public relays

They should pay for solving questions such as:

- current position and orbit refinement
- spin period and attitude state
- thermal inertia, surface heating, or cooling behavior
- albedo, composition, or spectral class
- beacon drift, power cycle, or relay sideband pattern

#### Opportunity Targets

These are temporary or changing events that create higher-value work and pull players
around the system:

- impact plumes
- eclipse exits and thermal blooms
- solar-storm disturbances
- temporary relay bursts
- unusual debris heating events
- occultations and line-of-sight alignments

These should pay more because they are time-limited, harder to revisit, and often
require players to accept louder signatures or worse geometry.

#### Rival Targets

Rival players are the highest-risk, highest-reward targets. They should not be the
baseline farm. They are the jackpot layer on top of the normal monitoring economy.

They use the same core loop as PvE targets:

- gather uncertain observations
- infer what the source probably is
- estimate current position and jump state
- uplink the best report you can justify

That keeps the game coherent. A comet, a drifting relay, and a rival craft are all
solved through observation and inference. The difference is only what hidden state
you are trying to recover and how much risk the target creates in return.


## Physical Signatures, Detection, And Penalties

### One Detection Model

Catalogue objects, anomalies, and player craft should all be simulated as sources
with band-specific output. The telescope should not ask "is this a player?" first.
It should measure flux, spectra, motion, periodicity, and temporal changes. Players
stand out because their signatures change with behavior: radiators warm, comms burst,
drives flare, and apertures glint.

### Simulated Signature Components

Each player should maintain a small set of physical state values that directly feed
detectability:

- `power_draw`: electrical load from sensors, cooling, comms, and propulsion.
- `stored_heat`: waste heat buffered in the hull and heat sinks.
- `radiator_output`: how much heat is being rejected now, which drives infrared brightness.
- `radio_emissions`: deliberate broadcast plus leakage from timing, shielding, and high-power electronics.
- `optical_glint`: reflected starlight or active illumination from open apertures and guidance systems.
- `jump_charge_emission`: broadband field signature produced while charging a jump.
- `arrival_bloom`: brief EM and thermal transient produced when a jump completes.

Behavioral consequences should fall out of these numbers:

- Long imaging runs gradually warm sensors and electronics, increasing infrared output.
- Overclocked detectors or cryocoolers improve results but create more waste heat.
- Uplinks and pings are loud radio events.
- Jump charging creates a rising broadband artificial signature whose duration scales with jump distance.
- Jump arrival produces a short, bright bloom that can be seen if someone is already watching the destination.
- A quiet player can stay hard to see, but only by accepting lower throughput or downtime to cool.

### Heat Rejection And Thermal Debt

The core emergent tradeoff should be thermal management:

- Heat can be buffered in sinks for a while.
- Eventually it must be dumped through radiators or cooling blooms, making the craft bright in infrared.
- Players can delay that dump to stay hidden, but then risk degraded sensor performance, module lockouts, or longer job times.
- Local conditions change the answer: dust may hide a radiator flare, while empty cold space may improve observing but make active heat rejection obvious.

This creates a natural push, hide, cool, and bank rhythm without needing an abstract
`exposure` variable.

### Range, Inverse Square, And Light-Time

Long-range interaction should be limited mostly by physics:

- Every optical, infrared, and radio signature falls off with distance by the inverse square law.
- As range increases, signal-to-noise drops, astrometric uncertainty grows, and classification gets weaker.
- Information is also stale by the time light reaches you. A contact at 1 AU is already about 8 minutes old; at 5 AU it is about 41 minutes old.

In practice, that means bright events can be noticed from far away, but precise
player hunting requires repeated observations, better baselines, and often getting
closer before you uplink a report. Movement matters partly because it changes your
viewing geometry: observing the same source from a different location or after a
jump can give you parallax and a much better 3D fix.

### Inference Instead Of Labels

Observation outputs should never directly say "player detected." They should return
measurements, not conclusions:

- position plus uncertainty ellipse
- flux in each observed band
- spectral features
- motion fit or acceleration hint
- catalogue cross-match confidence

An uncatalogued source with narrowband radio leakage, periodic thermal cycling, and
non-Keplerian motion might be a player, a relay, a decoy, or a strange anomaly. The
player's job is to interpret that evidence. Confirmation should come only from
successful reports, not from automatic UI labels.

### Uplink Reports, Accuracy Scoring, And Consequences

Uplinking is how the player cashes out both science and hunting. For rival hunting,
an uplink is a report to a beacon that says, in effect, "I believe there is an
artificial craft here, at this position."

A hunting report should include:

- estimated current position
- classification guess
- references to the supporting observations

Scoring should compare the report against hidden truth at beacon receipt time, not
at observation time. That matters because distant observations are stale.

- Rewards should fall off sharply with position error so random guessing is worthless.
- A weak approximate report might earn almost nothing.
- A tight fix on a currently active or jump-charging target should earn a large `intel` payout.
- Correctly recovering a target's current location from stale observations should be rewarded naturally through the same accuracy curve.

The target's penalty should use the same accuracy curve:

- poor fix: little or no consequence
- good fix: meaningful loss of unbanked `data`
- excellent fix: large data loss, disrupted uplink, or temporary relay scrutiny

This replaces abstract contact states with a concrete report loop based on actual
measurement quality.

### Jamming, Shadowing, And Counterplay

Jamming should be active denial, not magic invisibility.

- A directional jammer raises the local radio noise floor near a target or beacon, degrading their astrometry, making their uplinks less reliable, and corrupting jump navigation if they commit under interference.
- Because of the inverse square law, jamming is strongest at close range. That supports a shadowing playstyle where you creep in, jam a target's charge window or uplink path, and refine your own fix while theirs gets worse.
- Jamming is itself a loud emission. It may prevent a target from fixing you cleanly, but it can still reveal a bearing or approximate range to others.

That creates two valid hunting routes:

- pure stealth: stay passive, manage heat, solve the target from repeated measurements, then uplink from safety
- aggressive shadowing: jam, stay nearby during the charge window, force bad data on the target, and cash out a high-precision fix

Counterplay should include burst observing between jam cycles, changing geometry,
aborting a charge, cold-spooling from a cleaner geometry, using decoys, or moving to stronger relay coverage before uplinking.


## Instrument Roles In The Deeper Game

The existing tools already map well to a richer loop:

- `imager`: best for precise astrometry, survey income, and spotting glints or hot radiators once infrared-capable filters are unlocked.
- `radio_receiver`: best for first contact on rivals, wide-area sweeps, and catching uplinks or leakage.
- `spectrograph`: best for turning a suspicious source into stronger evidence by distinguishing artificial continua, engineered materials, or waste-heat patterns from natural ones.

That gives each instrument a clear place in both PvE discovery and PvP hunting.
To make thermal stealth real, the first equipment expansion should add at least one
`ir_band` or thermal imaging mode to the imager path.


## Stealth Features And Active Modules

The module system should change physical behavior, not add or subtract hidden
detection percentages. Passive modules reshape how power, heat, and leakage behave.
Active modules buy performance by producing louder signatures.

### Loadout Structure

- 2 passive slots
- 1 active slot at start
- Additional active slot unlockable later

### Passive Modules

Passive modules shape a playstyle without forcing constant input:

- `cold_baffles`: reduce aperture glint and stray light, but trap more heat and slow cooldown.
- `signal_scrubber`: reduce radio leakage and sidebands, but draw extra power and warm the bus.
- `phase_change_sink`: store more heat before you must radiate it, but once full it forces a long cooldown window.
- `expanded_cache`: hold more unbanked `data`, but lose more if an uplink or cache operation is disrupted.
- `ghost_drive`: reduce jump-charge signature and arrival bloom brightness, but increase charge time.

### Active Modules

Active modules should feel tempting because they are strong:

| Module | Benefit | Risk / Cost |
|---|---|---|
| `deep_field_overclock` | Better limiting magnitude or radio sensitivity for one observation | Big power draw, rapid heat buildup, and extra timing leakage |
| `wideband_ping` | Instant weak contacts across the current region or nearby orbital volume | Obvious wide-area radio flash |
| `directional_jammer` | Degrades a nearby target's radio astrometry and uplink quality | Loud, directional emission that can itself be detected and geolocated |
| `target_illuminator` | Wider spectrograph lock or higher acquisition chance | Emits a bright guide source in optical and near-IR |
| `burst_uplink` | Bank `data` from unsafe space immediately | High-gain radio beam that can be detected, traced, and jammed |
| `decoy_beacon` | Creates a false heated or transmitting source | Consumes inventory and can be disproved by careful follow-up |

The important rule is that active modules should never be "free efficiency." If a
module meaningfully improves yield, its physical signature cost should be legible
in the API.

### Scan Profiles

To add nuance without a large item catalog, every observation can also take a
scan profile:

- `low_power`: lower detector bias and smaller signatures, but lower sensitivity
- `survey`: baseline
- `boosted`: better SNR or contact accuracy, but more heat and bus noise
- `overclocked`: strongest result shaping, high thermal debt, and obvious timing leakage

This creates tactical choice even before a player has many unlocks.

### Thermal Posture

Players should also be able to control how aggressively they reject heat:

- `sealed`: minimize heat rejection, stay dim in infrared, accumulate heat quickly
- `balanced`: steady-state cooling
- `venting`: dump heat aggressively, recover faster, glow brightly in infrared

This makes stealth a matter of thermal posture rather than an abstract stealth mode.


## Movement: Jump-Based Repositioning

Movement should be strategic, asynchronous, and fully playable while it happens.

### World Structure

Replace the single shared sky with one playable solar system divided into named
regions such as planetary orbits, Trojan clusters, belts, relay corridors, and
outer-system shadows. These regions are not hard PvP shards. They are useful
labels for local background conditions, beacon coverage, and likely content.

Each region has:

- `ir_background`: how much infrared clutter or dust glow is in the area
- `radio_noise`: ambient interference from natural or artificial sources
- `dust_opacity`: how much the region blocks or blurs optical observations
- `solar_flux`: how much passive heating and glint pressure players take on
- `relay_coverage`: how easy it is to uplink or navigate with low power
- `typical_range_scale`: how far apart contacts usually are inside that region

Players can detect or infer other players across regions if the signatures are bright
enough, but high-precision interaction should depend on actual range and light-time,
not a hard map rule.

Movement is also how you improve a track. Reobserving a source after a jump can
give you a better baseline for parallax and motion fitting, which is exactly what a
guess-based scoring system needs.

### Jump Phases

Movement happens in two discrete phases:

1. Charge in place.
2. Commit or abort.

During the charge phase, the player remains at their current position and can keep
submitting observation jobs. That removes the dead-time problem entirely. The tradeoff
is that jump charging is the loudest thing the ship can do:

- power draw spikes
- stored heat climbs quickly
- a broadband electromagnetic signature blooms
- longer jumps produce longer and more obvious charge curves

If another player sees an uncatalogued broadband source with a rising power curve,
they have a window to refine their fix, uplink a report, jam the charger, or reposition
to watch likely destinations.

When the charge completes, the player chooses whether to commit or abort:

- `commit`: instant relocation to the destination coordinates
- `abort`: no movement, but the thermal debt and signature cost are still paid

Abort is important because it lets a player react to new information without the game
forcing them into a bad jump they started earlier.

### Arrival Bloom And Recalibration

Jumping is not silent at the destination.

- arrival produces a brief EM and thermal bloom
- anyone already observing the destination can see the transient
- the ship enters a short recalibration period after arrival

Recalibration should degrade SNR for a few seconds, not lock the player out of play.
That prevents jump-and-immediately-uplink cheese while keeping the game active.

### Charge Profiles

Charge profile becomes the main movement-mode choice:

| Profile | Charge Time | Signature | Thermal Debt | Best For |
|---|---|---|---|---|
| `cold_spool` | longest | low at first, only obvious late in the charge | moderate | escaping without drawing immediate attention |
| `standard` | medium | clearly a jump charge to anyone watching | high | normal repositioning |
| `emergency` | shortest | massive and obvious across the region | very high | running from an active hunter |

### Why Movement Matters

- Lets players leave a dangerous region instead of waiting to be farmed.
- Creates safer and riskier hunting grounds based on real background conditions.
- Turns movement into a tense decision point instead of a transit lockout.
- Gives value to stealth-oriented routes, charge profiles, and jump-related upgrades.
- Prevents the game from collapsing into one solved observation spot.

### Example Region Themes

- `Dust Veil`: high infrared background and heavy optical attenuation; good for hiding radiator output and late-stage cold-spool signatures, worse for fine imaging
- `Relay Spine`: excellent comm coverage and cheap uplinks, but full of listeners that punish loud radio behavior
- `Quiet Dark`: superb passive observing and low natural heating, but any radiator flare, jump charge, or uplink stands out sharply
- `Broken Array`: cluttered radio reflections, debris shadows, and strong opportunities for jump-arrival ambushes


## Contracts And Dynamic Content

Static catalogue objects are a good foundation, but the game needs rotating reasons
to move and take risks.

Add simple contracts such as:

- "Classify any emission object with `h_alpha` in Dust Veil."
- "Uplink a high-confidence artificial-source fix in Relay Spine."
- "Catch a target during its jump arrival bloom in Broken Array and uplink a precise fix."
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

- `region`
- `position_au`
- `credits`
- `unbanked_data`
- `intel`
- `power_draw`
- `stored_heat`
- `heat_sink_fill`
- `radiator_mode`
- `current_signatures`
- `active_modules`
- `passive_modules`
- `jump_status`
- `recalibration_remaining_sec`
- `observation_snr_multiplier`

### Observation Request

Extend `POST /v1/sessions/{session_id}/observations` with optional:

- `scan_profile`
- `active_module`
- `radiator_mode`

Observation results should include:

- `rewards`
- `signature_report`
- `track_file_updates`
- `light_time_sec`
- `new_contract_progress`

Observation jobs should remain available while `jump_status` is `jump_charging` or
`jump_charged`. During `recalibrating`, the server should still accept
observations, but apply a temporary SNR penalty instead of locking the player out.

### New Endpoints

- `GET /v1/system/regions`
- `POST /v1/sessions/{session_id}/jump`
- `GET /v1/sessions/{session_id}/jump/{job_id}`
- `DELETE /v1/sessions/{session_id}/jump/{job_id}`
- `POST /v1/sessions/{session_id}/jump/{job_id}/commit`
- `GET /v1/sessions/{session_id}/track-files`
- `POST /v1/sessions/{session_id}/uplink`
- `POST /v1/sessions/{session_id}/radiators`
- `POST /v1/sessions/{session_id}/jam`

`POST /v1/sessions/{session_id}/transmit` can remain, but it should become a more
explicit family of risky actions such as `uplink`, `broadcast`, or `decoy`.

`POST /v1/sessions/{session_id}/uplink` should support both science cash-out and
hunting reports. Hunting payloads should include:

- `classification_guess`
- `predicted_position_au`
- `evidence_job_ids`

### Model Changes

- `Sky` becomes a `SystemMap` containing region-local backgrounds, relay and beacon topology, and source populations.
- `Session` gains progression, power, heat, loadout, jump-state, and position fields.
- `PlayerSource` gains region membership, position data, and simulated infrared, radio, optical, jump-charge, and arrival-bloom signatures derived from actual activity.
- Observation processing can return uncertainty-bearing measurements, reward data, and signature metadata alongside FITS-style results.


## Recommended Implementation Order

### Phase 1: Add Stakes And Signatures

- Add `credits`, `unbanked_data`, and `intel`.
- Give players physical state: power draw, stored heat, radiator mode, and radio emissions.
- Make observations award value and alter those physical states.
- Make `transmit` or a new `uplink` action convert `unbanked_data` into `credits`.
- Add natural consequences for traced uplinks and thermal saturation.

This already creates a real loop with minimal surface-area growth.

### Phase 2: Add Inference And Hunting

- Remove automatic source labels and expose richer raw measurements instead.
- Add guess-based uplink scoring using predicted position.
- Add range- and light-time-dependent report difficulty.
- Add jamming and anti-jamming play.
- Make instruments contribute differently to player hunts.
- Award `intel` for accurate artificial-source and rival-player fixes.

### Phase 3: Add Modules And Posture

- Add passive and active slots.
- Implement 3-5 modules with very visible risk/reward.
- Add scan profiles and radiator modes.
- Surface signature changes clearly in responses.

### Phase 4: Add Movement

- Split the sky into solar-system regions with distinct physical backgrounds and relay coverage.
- Add jump-charge jobs, explicit commit/abort, arrival blooms, and recalibration.
- Allow normal observation during charge jobs.
- Limit interaction quality by distance, SNR, and light-time rather than a hard region wall.

### Phase 5: Add Dynamic Objectives

- Introduce rotating contracts and transient anomalies.
- Use them to prevent static farming and keep regions alive.


## Balance Guardrails

- Detection should mostly threaten unbanked value and temporary tempo, not permanent unlocks.
- There should be no abstract exposure meter; if detectability changes, the API should explain it in terms of heat, radio, light, or motion.
- The same detection pipeline should evaluate catalogue objects, anomalies, and players.
- Normal observation results should never inject metaknowledge by labeling a source as a player.
- Random guessing should be effectively worthless because score falls off steeply with position error.
- Range and light-time should naturally limit what a player can do to distant contacts.
- Stealth play should be slower, not invalid.
- Aggressive play should be more profitable, not strictly better.
- Thermal management should create pacing, not housekeeping busywork.
- Movement should be an exit valve from pressure, not a chore tax or a dead-time lockout.

### Known Gaps

- The hunting loop currently depends on other players being online. With zero or
  few concurrent rivals, the signature model, jamming, track files, and hunting
  reports become elaborate infrastructure with no targets. A future phase should
  add NPC craft — automated science drones, rogue relays, or smuggler bots — that
  use the same signature model and can be hunted with the same tools. This would
  also serve as a training layer before real PvP.


## Net Effect

With these changes, the astronomy game becomes a layered hunt-and-survey game:

- PvE scanning builds your haul.
- PvP detection creates high-value hunts.
- Uplinking turns progress into a risk decision.
- Active modules create real temptation by making you physically louder.
- Solar-system movement makes location, range, and timing matter.

That keeps the current observatory fantasy intact while giving the game the missing
depth, stakes, and replayability.


## Implementation Appendices

### Appendix A: Scoring And Uplink Rules

This appendix turns the high-level report loop into a concrete v1 scoring model.
The exact constants can be tuned later, but the formulas and required fields should
stay stable.

#### Common Constants

- `LIGHT_TIME_SEC_PER_AU = 499.004784`
- `SIGMA_PLAYER_POS_AU = 0.0002`
- `CHARGING_WINDOW_FACTOR = 1.25`
- `RECALIBRATION_WINDOW_FACTOR = 1.10`
- `SCIENCE_UPLINK_COOLDOWN_SEC = 30`
- `HUNT_UPLINK_COOLDOWN_SEC = 90`

`SIGMA_PLAYER_POS_AU` is about 30,000 km. That is intentionally tight enough that
random guessing inside a large uncertainty volume is worthless.

#### Science Report Scoring

Each non-rival report should target a specific hidden-state question.

Each question definition needs:

- `question_id`
- `truth_fn(t)`
- `scale`
- `halflife_sec`
- `base_data_reward`
- `base_intel_reward`

Use the following v1 formulas:

```text
scalar normalized_error = abs(estimate - truth) / scale
vector normalized_error = norm(estimate - truth) / scale
enum accuracy_score = 1.0 if estimate == truth else 0.0

accuracy_score = exp(-(normalized_error ^ 2))   # scalar/vector only
freshness_factor = exp(-ln(2) * staleness_sec / halflife_sec)
novelty_factor = 1 / (1 + successful_reports_by_session_for_same_target_question_window)
reward_factor = accuracy_score * freshness_factor * novelty_factor

data_reward = round(base_data_reward * reward_factor)
intel_reward = round(base_intel_reward * reward_factor)
```

`question_window` should remain open until the hidden state changes enough to matter:

- position/orbit: until the target moves by more than one `scale`
- spin/attitude: until phase error exceeds one `scale`
- thermal state: until the heating or cooling state changes band
- transient event: until the event expires

This is what makes the economy farmable without being degenerate. You can keep
working a target, but only by improving precision or answering a genuinely new
question.

#### Rival Hunting Report Scoring

Hunting reports should be evaluated against the hidden truth state of the nearest
rival craft at beacon receipt time. If no rival is within `3 * SIGMA_PLAYER_POS_AU`
of the submitted position, the report is treated as a miss.

For v1, the hunting payload should use:

- `classification_guess`: `natural` or `artificial`
- `predicted_position_au`: `{x, y, z}`
- `evidence_job_ids`: list of supporting jobs

Use the following formulas:

```text
d_pos = norm(predicted_position_au - true_position_au(t_receipt))
position_score = exp(-((d_pos / SIGMA_PLAYER_POS_AU) ^ 2))

class_factor = 1.0 if classification_guess == "artificial" else 0.0
window_factor =
    CHARGING_WINDOW_FACTOR if target_state(t_receipt) == "jump_charging"
    else RECALIBRATION_WINDOW_FACTOR if target_state(t_receipt) == "recalibrating"
    else 1.0

hit_score = class_factor * position_score
effective_hit_score = min(1.0, hit_score * window_factor)
intel_reward = round(100 * effective_hit_score)
```

Target consequences should use that same `effective_hit_score`:

```text
data_loss_fraction = 0.5 * (effective_hit_score ^ 1.5)
relay_scrutiny_sec = 0 if effective_hit_score < 0.25 else round(180 * (effective_hit_score ^ 2))
uplink_disrupted = target_is_uplinking and effective_hit_score >= 0.60
uplink_delayed = target_is_uplinking and 0.30 <= effective_hit_score < 0.60
```

Interpretation:

- `effective_hit_score < 0.02`: zero reward, zero practical target effect
- `effective_hit_score ~= 0.10`: weak report, almost no payout
- `effective_hit_score ~= 0.50`: meaningful rival fix
- `effective_hit_score >= 0.80`: excellent fix, large payout and strong disruption

This gives the design the steep falloff it needs. If the position guess is sloppy,
the reward collapses fast.

#### Anti-Spam And Report Gating

Random guessing only stays worthless if uplinks are constrained. Use all of these
rules in v1:

- Every hunting uplink triggers `HUNT_UPLINK_COOLDOWN_SEC` on that session's relay access.
- Every science uplink triggers `SCIENCE_UPLINK_COOLDOWN_SEC`.
- A hunting uplink must cite at least 2 evidence jobs from distinct observation times, unless one cited job has `snr >= 50`.
- A second hunting uplink on the same track file must include at least one evidence job that was not used in the previous hunting uplink on that same track.
- Reports with `effective_hit_score < 0.02` still consume cooldown and still emit their radio signature.

The design should not charge an abstract report fee in v1. The anti-spam pressure
should come from cooldown, evidence requirements, and the physical risk of making
another uplink.


### Appendix B: V1 Simulation Model

This appendix picks a concrete simulation model that is physically flavored but
still buildable in a small codebase. The main v1 simplification is that players
are always at a real position. They stay at their current coordinates while a jump
charges, then relocate on commit; there is no simulated mid-transit state.

#### V1 Scope

V1 should simulate one operational theater inside a solar system, not the entire
solar system at once.

Recommended scope:

- one continuous map volume
- several named regions inside that volume
- active distances on the order of light-seconds to light-minutes, not many AU

The broader solar system can still exist in fiction and contracts, but the playable
space should stay small enough that light-time is noticeable and movement remains a
real decision instead of a multi-day wait.

#### Coordinates And Truth State

Store all truth state in system-centric Cartesian coordinates measured in AU:

- `position_au = {x, y, z}`
- `velocity_au_per_day = {x, y, z}` for naturally moving sources
- `region_id`
- `signature_state`

Region labels are metadata on top of continuous space. They are not separate maps
and they should not gate interaction by themselves.

To minimize API churn, v1 can keep observation pointing in apparent sky coordinates
from the observer's frame. Internally:

- the observer has a truth position and velocity
- each source has a truth position and velocity
- the observation job converts those into apparent direction, flux, motion hint, and uncertainty

#### Source Motion Classes

Use only four motion classes in v1:

1. `orbiting_body`
   Defined by circular orbit radius, phase, period, and optional inclination.

2. `relay_or_derelict`
   Defined by an orbit plus a simple power-cycle or attitude-cycle script.

3. `transient_event`
   Defined by a source position, spawn time, lifetime, and decay curve.

4. `player_craft`
   Defined by a fixed position plus a jump state machine.

The player model is intentionally simpler than real orbital mechanics. A player sits
at one position while idle, charge builds there, and the commit step relocates them
instantly to a new position. That is good enough for:

- light-time
- inverse-square falloff
- parallax
- distinct charge and arrival events
- precise origin/destination hunting

without requiring a full orbital integrator or any dead transit state.

#### Player Jump State Machine

Each player session should be in exactly one of these movement states:

1. `idle`
   Position is fixed. Full observation capability.

2. `jump_charging`
   Position is still fixed. Observation remains available. Jump signatures and heat climb while the charge job runs.

3. `jump_charged`
   Position is still fixed. Commit or abort is available. Observation remains available, but heat continues to accumulate slowly.

4. `recalibrating`
   Position is fixed at the jump destination. Observation remains available, but SNR is temporarily degraded while the bus settles.

#### Observation Time And Light-Time

Use these rules in v1:

- `observation_epoch = job.completed_at`
- `exposure_time` affects SNR, motion blur, and heat generation
- `exposure_time` does not advance the whole simulation by minutes or hours in wall-clock time

For each observed source:

```text
t_obs = observation_epoch
t_emit_0 = t_obs
d_0 = norm(source_position(t_emit_0) - observer_position(t_obs))
t_emit_1 = t_obs - d_0 * LIGHT_TIME_SEC_PER_AU
```

One backward iteration is enough for v1 because source speeds are tiny relative to
light speed over the playable map size.

For uplinks:

```text
t_submit = uplink_submit_time
t_receipt = t_submit + norm(player_position(t_submit) - nearest_beacon_position) * LIGHT_TIME_SEC_PER_AU
```

Scoring always uses `t_receipt`, not `t_submit`.

#### Jump Model

Jumping should use distance-scaled charge times. The player remains at `p0` during
charge and only moves to the destination when the jump is committed.

Use these starting constants:

- `BASE_JUMP_CHARGE_SEC = 20`
- `JUMP_CHARGE_SEC_PER_AU = 2400`
- `MAX_CHARGED_HOLD_SEC = 30`
- `BASE_JUMP_NAV_SIGMA_AU = 0.00002`
- `ARRIVAL_BLOOM_SEC = 8`

Charge profiles:

| Profile | Charge multiplier | Signature multiplier | Thermal multiplier | Navigation sigma multiplier |
|---|---|---|---|---|
| `cold_spool` | 1.8 | 0.7 | 0.8 | 0.8 |
| `standard` | 1.0 | 1.0 | 1.0 | 1.0 |
| `emergency` | 0.55 | 1.8 | 1.5 | 1.8 |

For a jump from current position `p0` to destination `p1`:

```text
jump_distance_au = norm(p1 - p0)
base_charge_sec = BASE_JUMP_CHARGE_SEC + JUMP_CHARGE_SEC_PER_AU * jump_distance_au
charge_duration_sec = base_charge_sec * profile_charge_multiplier

charge_emission_power = (0.5 + 12 * jump_distance_au) * profile_signature_multiplier
thermal_debt_gain = (0.15 + 4 * jump_distance_au) * profile_thermal_multiplier
```

`cold_spool` should not just scale the whole curve down linearly. Its signature should
start ambiguous and become obvious late in the charge. A simple v1 visibility curve is:

```text
cold_spool_visibility(progress) = 0.35 + 0.65 * progress ^ 2
```

Commit and abort rules:

```text
if abort:
    position stays at p0
    stored_heat += thermal_debt_gain
    jump_state = idle

if commit:
    nav_sigma_au = BASE_JUMP_NAV_SIGMA_AU * profile_nav_sigma_multiplier * (1 + jump_nav_jam_strength)
    arrival_offset = isotropic_gaussian(nav_sigma_au)
    position = p1 + arrival_offset
    stored_heat += thermal_debt_gain
    jump_state = recalibrating
    recalibrating_until = now + ARRIVAL_BLOOM_SEC
```

Charged jumps should not be held forever in v1:

```text
if jump_state == jump_charged and charged_hold_time > MAX_CHARGED_HOLD_SEC:
    auto_abort()
```

Observation rules by jump state:

- `idle`: normal observations
- `jump_charging`: normal observations, plus jump-charge signatures
- `jump_charged`: normal observations, plus elevated heat and signature
- `recalibrating`: observations allowed with temporary `snr_multiplier` rising from `0.65` back to `1.0`

This is what fixes the unplayable dead-time problem. Charging is tense, not inert.

#### Jamming Model

Jamming should reuse the same signal model as everything else. It is not a status
effect. It is a local radio emitter.

For a jammer at distance `d_au` from a target:

```text
jam_strength = jammer_output / max(d_au, 0.00001) ^ 2
effective_radio_noise = base_radio_noise * (1 + jam_strength)
jump_nav_jam_strength = jam_strength
```

In v1, jamming should only affect:

- radio observations
- radio-derived astrometry
- uplink reliability
- jump arrival precision if a target commits while jammed

It should not magically blind optical or thermal observations.


### Appendix C: Target Matrix And Payload Shapes

#### V1 Target Matrix

| Target class | Core hidden-state questions | Primary instruments | Typical change cadence | V1 reward bias |
|---|---|---|---|---|
| Asteroid / minor moon | position, orbit refinement, spin period, albedo, thermal inertia | imager, IR-capable imager, spectrograph | hours to days | steady `data` |
| Comet / outgasser | position, plume vector, outgassing state, volatile lines | imager, spectrograph, IR-capable imager | minutes to hours | medium `data` |
| Dust / debris feature | density peak, occultation timing, heating curve | imager, IR-capable imager, radio for reflective clutter | minutes to hours | steady `data` |
| Relay / derelict / probe | drift, attitude, power cycle, sideband pattern | radio_receiver, imager, spectrograph | minutes to hours | higher `data`, occasional `intel` |
| Transient event | center point, decay curve, material class, event timing | any mix depending on event | seconds to hours | high `data`, occasional `intel` |
| Rival craft | current position, jump-charge state, arrival state, artificial classification | imager, radio_receiver, spectrograph, jamming support | always changing | highest `intel` |

#### Observation Payload Principles

All payloads should follow the same rule:

- return measured values
- return uncertainties
- return catalogue match information
- do not return hidden truth labels like `"player"` or `"rival"`

#### Example Image Result

```json
{
  "type": "image",
  "observation_epoch": "2026-03-16T20:14:00Z",
  "detections": [
    {
      "detection_id": "det-img-001",
      "apparent_ra_deg": 42.5031,
      "apparent_dec_deg": 15.2912,
      "uncertainty_arcsec": {
        "major": 12.4,
        "minor": 7.1,
        "pa_deg": 33.0
      },
      "flux": {
        "optical_mag": 18.2,
        "ir_mag": 15.6
      },
      "shape_hint": "point",
      "motion_hint": {
        "streak_angle_deg": null,
        "angular_rate_arcsec_per_hr": 4.3
      },
      "catalogue_matches": [
        {
          "target_id": "ast-204",
          "confidence": 0.18
        }
      ]
    }
  ]
}
```

#### Example Radio Result

```json
{
  "type": "radio_map",
  "observation_epoch": "2026-03-16T20:14:12Z",
  "detections": [
    {
      "detection_id": "det-rad-014",
      "apparent_ra_deg": 42.49,
      "apparent_dec_deg": 15.28,
      "uncertainty_arcmin": 3.8,
      "flux_mJy": 21.4,
      "bandwidth_hz": 1800,
      "spectral_slope": -0.2,
      "burstiness": 0.71,
      "catalogue_matches": []
    }
  ],
  "noise_floor_mJy": 2.3
}
```

#### Example Spectrum Result

```json
{
  "type": "spectrum",
  "observation_epoch": "2026-03-16T20:14:30Z",
  "target_acquired": true,
  "source_ref": "det-img-001",
  "continuum_fit": "flat-to-rising infrared",
  "line_features": [
    "narrowband emission at 1420.4 MHz equivalent",
    "broad thermal continuum"
  ],
  "material_hints": [
    "painted metal or composite panel",
    "heated radiator surface"
  ],
  "catalogue_matches": []
}
```

#### Example Track File

Track files should be player-visible aggregation objects created from repeated
observations. They should summarize evidence without converting it into hidden truth.

```json
{
  "track_id": "trk-0091",
  "source_status": "provisional",
  "evidence": [
    {"job_id": "job-101", "detection_id": "det-rad-014"},
    {"job_id": "job-108", "detection_id": "det-img-001"}
  ],
  "state_estimate": {
    "fit_epoch": "2026-03-16T20:15:00Z",
    "position_au": {"x": 0.8421, "y": -0.1143, "z": 0.0062},
    "position_sigma_au": {"x": 0.0011, "y": 0.0006, "z": 0.0008}
  },
  "motion_hypothesis": "stationary_or_low_drift",
  "catalogue_match": {
    "best_target_id": null,
    "confidence": 0.07
  },
  "signal_summary": {
    "optical_mag": 18.2,
    "ir_mag": 15.6,
    "radio_flux_mJy": 21.4,
    "narrowband_fraction": 0.82,
    "thermal_cycle_sec": 3600,
    "broadband_charge_curve_score": 0.68
  },
  "notes": [
    "no confident catalogue match",
    "rising broadband emission inconsistent with local debris drift"
  ]
}
```

#### Example Science Uplink Payload

```json
{
  "report_type": "science",
  "target_id": "ast-204",
  "question_id": "spin_period_sec",
  "estimate": 14310,
  "evidence_job_ids": ["job-120", "job-121"]
}
```

#### Example Hunting Uplink Payload

```json
{
  "report_type": "hunt",
  "classification_guess": "artificial",
  "predicted_position_au": {"x": 0.8420, "y": -0.1142, "z": 0.0060},
  "evidence_job_ids": ["job-101", "job-108", "job-113"]
}
```

#### Example Hunting Uplink Result

```json
{
  "report_id": "rep-77a1",
  "status": "accepted",
  "report_type": "hunt",
  "receipt_time": "2026-03-16T20:15:09Z",
  "score": {
    "position_error_au": 0.00008,
    "classification_match": true,
    "effective_hit_score": 0.84
  },
  "rewards": {
    "intel": 84
  },
  "target_effect": {
    "data_loss_fraction": 0.39,
    "relay_scrutiny_sec": 127,
    "uplink_disrupted": true
  }
}
```

#### Example Jump Request

```json
{
  "destination_au": {"x": 0.8400, "y": -0.1100, "z": 0.0100},
  "charge_profile": "standard"
}
```

#### Example Jump Status

```json
{
  "job_id": "jmp-1138",
  "status": "charging",
  "charge_remaining_sec": 45,
  "abort_available": true,
  "observations_allowed": true,
  "signature_report": {
    "jump_charge_power": 0.72,
    "stored_heat_gain_rate": 0.14
  }
}
```

#### Example Charged Jump Status

```json
{
  "job_id": "jmp-1138",
  "status": "charged",
  "commit_available": true,
  "abort_available": true,
  "hold_remaining_sec": 19,
  "observations_allowed": true
}
```

#### Example Jump Commit Result

```json
{
  "job_id": "jmp-1138",
  "status": "jumped",
  "new_position_au": {"x": 0.83998, "y": -0.10995, "z": 0.01003},
  "arrival_bloom_sec": 8,
  "recalibration_remaining_sec": 8,
  "observations_allowed": true,
  "snr_multiplier": 0.68
}
```

#### Example Jump Abort Result

```json
{
  "job_id": "jmp-1138",
  "status": "aborted",
  "position_au": {"x": 0.8120, "y": -0.0870, "z": 0.0090},
  "thermal_debt_retained": 0.44,
  "observations_allowed": true
}
```
