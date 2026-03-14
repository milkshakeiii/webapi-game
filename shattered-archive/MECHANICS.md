# Shattered Archive Synthesis Mechanic

This is the core puzzle system for *Shattered Archive*. The player is not solving a different hand-built puzzle in every room. Instead, each room presents a synthesis problem: make the right magical compound out of the ingredients currently available.

The goal is to keep the system deep enough to be interesting, but small enough that a human can reason about it and an API client can manipulate it cleanly.

## The Basic Idea

Each puzzle starts with:

- a list of available reagents
- a contract describing what the final spell must look like
- a bench with limited space
- a step limit

The player turns reagents into separate magical `threads`, then merges and transforms those threads until only one final thread remains. If that final thread matches the contract, the puzzle is solved.

This means the game is partly about picking the right ingredients, but mostly about combining them in the right order. Order matters because you do not dump everything into one pot at the start. You build intermediate structures and then decide how to join them.

## The Pieces

### Reagents

A reagent is a raw ingredient. It has:

- four essence values
- a set of tags
- a cost
- a limited count

The four essences are:

- `lumen`: light, revelation, ignition
- `echo`: memory, language, spirit
- `motive`: force, motion, activation
- `veil`: concealment, negation, cold

Tags are just labels like `relic`, `ink`, `metal`, or `mineral`. They matter because threads that share tags bind together more cleanly than threads that do not.

### Threads

When you add a reagent to the bench, it becomes its own thread. A thread is a small bundle of:

- essence values
- tags
- `fray`

`Fray` is the main penalty stat. High fray means the thread is unstable. Most contracts cap how much fray is allowed in the final spell.

### Contracts

A contract is the target you are trying to hit. It can specify:

- minimum essence values
- maximum essence caps
- required tags
- forbidden tags
- maximum fray

So a contract might say:

- `lumen >= 6`
- `echo >= 4`
- `veil <= 1`
- must include `relic`
- must not include `spectral`
- `fray <= 1`

That gives you a precise optimization target instead of a vague “make something powerful.”

## The Player Actions

The current prototype has five actions.

### 1. Add

`add(reagent)`

This takes one reagent from the available pool and places it on the bench as a new thread. The bench has a capacity limit, so you cannot keep every ingredient active at once.

### 2. Bind

`bind(thread_a, thread_b, bonus_essence?)`

This merges two threads into one. Their essence values are added together, their tags are combined, and their fray values are added.

If the two threads share a tag, the bind is stable. If they also both have a positive value in the same essence, you can choose one of those shared positive essences and gain a `+1` resonance bonus there.

If the threads do not share any tag, the bind still works, but it adds `+2 fray`.

This is the most important rule in the system. It creates the main puzzle question: which things should be merged early, and which things should be kept apart until later?

### 3. Distill

`distill(thread, essence)`

This pushes one thread harder in a chosen direction.

- `+2` to the chosen essence
- `-1` from every other essence that is currently above `0`
- `+1 fray`

Distill is how you sharpen a nearly-correct thread into the exact shape the contract needs. It is efficient, but it causes wear.

### 4. Reweave

`reweave(thread, from, to, amount)`

This moves `1` or `2` points from one essence to another on the same thread.

It always costs fray:

- `+1 fray` normally
- `+2 fray` when converting across an opposed pair

Opposed pairs are:

- `lumen <-> veil`
- `echo <-> motive`

Reweave is the repair tool. It is useful when a thread has the right total power but the wrong distribution.

### 5. Stabilize

`stabilize(thread, reduce_essence)`

This lowers fray, but at a cost:

- `-2 fray`, minimum `0`
- `-1` from one of the thread's current highest essences

So stabilization is not free cleanup. You can save a thread from breaking, but you must give up some peak output to do it.

## Why This Is More Interesting Than Simple Stat Summing

If every reagent went straight into one shared pool, most puzzles would collapse into “add enough numbers, then clean up the edges.” That is too shallow.

The thread system fixes that. Since reagents begin separately, you care about:

- which ingredients can bind stably
- which ingredients act as bridges between tag families
- when to take a resonance bonus
- when to distill before binding versus after binding
- whether an unstable bind is worth the extra fray

That gives the system local structure. Two solutions that use the same ingredients can still play very differently because their merge tree is different.

## Worked Example

Suppose the contract is:

- `lumen >= 6`
- `echo >= 4`
- `veil <= 1`
- must include `relic`
- `fray <= 1`

And the available reagents are:

- `archive_dust`: good `echo`, tag `ink`
- `catalogue_oil`: some `echo`, some `motive`, tags `ink` and `relic`
- `mirror_dust`: good `lumen`, some `echo`, tags `relic` and `mineral`

One strong line is:

1. `add archive_dust`
2. `add catalogue_oil`
3. `add mirror_dust`
4. `bind archive_dust + catalogue_oil` with an `echo` bonus
5. `bind that result + mirror_dust` with a `lumen` bonus
6. `distill lumen`

Why this works:

- `archive_dust` and `catalogue_oil` share the `ink` tag, so they bind cleanly.
- They also both contribute `echo`, so that bind can take an `echo` resonance bonus.
- The merged result now contains `relic` because of `catalogue_oil`, which lets it bind cleanly with `mirror_dust`.
- That second bind can take a `lumen` resonance bonus.
- The final `distill lumen` pushes the thread over the finish line without exceeding the fray limit.

The nice part is that `catalogue_oil` is doing real work here. It is not just “more stats.” It bridges the `ink` family to the `relic` family, which makes the whole synthesis route viable.

## Where the Optimization Comes From

A puzzle has binary success or failure, but good solutions can still be ranked. The prototype score rewards:

- fewer steps
- lower reagent cost
- lower final fray
- less overproduction beyond the contract minimums

That gives the mechanic a Zachtronics-like feel without needing a spatial board. The player can solve the room once, then come back later and try to solve it more elegantly.

## Why It Fits a Web API Game

This mechanic is well suited to an API format because the full game state is structured and inspectable:

- the reagent pool is explicit
- thread state is explicit
- available actions are explicit
- contract checking is deterministic

That means a human can play it through Codex or Claude Code in a way that feels natural. The agent can track the bench state, search possibilities, and compare solutions, while the human still makes the interesting judgment calls about strategy and tradeoffs.

## Current Prototype Limits

The current version is intentionally narrow:

- one bench
- one final thread
- no randomness inside synthesis
- a short action list
- small integer essence values

That is on purpose. If the base system does not feel good in this constrained form, adding more content will only make it harder to understand.

## What Can Expand Later

If the core holds up, the obvious expansion knobs are:

- catalysts that modify the next action
- contracts that require multiple final compounds
- persistent inventory pressure between rooms
- special reagents with one unusual rule each
- new bench tools that break the normal rules in a controlled way

But the main mechanic should stay recognizable: build threads, manage fray, exploit tag relationships, and hit a precise target.
