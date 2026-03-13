# Flag Football — Game Design

## Overview

A turn-based trust game where players write code (bots) that plant flags, capture flags, and try to distinguish teammates from opponents through anonymous data exchange.

## Players

- Each player writes a bot independently and submits it
- Teams are assigned randomly after submission
- Players do not know who their teammates are when writing their code
- No pre-game coordination is possible

## Core Rule

Exchanges are **anonymous**. You don't know who planted a flag or who responded to yours. You can *claim* an identity in your message content, but claims can be lies. Trust must be built through content, not server-enforced identity.

## Turn Structure

Each round has three phases:

### Phase 1 — Plant
Each bot may plant a flag. A flag is a **challenge message** (arbitrary string), visible to all bots.

### Phase 2 — Capture
Each bot that didn't plant may send a **response** (arbitrary string) to any one planted flag. Multiple bots can respond to the same flag.

### Phase 3 — Judge
Each planter reviews the responses to their flag and decides **accept** or **reject** for each one.

### Phase 4 — Results
Each flag's net score is announced publicly. (e.g., "Flag A: +4, Flag B: -1"). Flags are anonymous — the score is tied to the challenge text, not the planter's identity.

## Scoring

| Outcome | Planter | Capturer |
|---|---|---|
| Accept teammate | +2 | +2 |
| Accept opponent | -3 | +5 |
| Reject (anyone) | 0 | 0 |

(Numbers are placeholders — need to balance incentives.)

## Bot Interface

A bot implements 3 endpoints:

```python
class Bot:
    def plant(self, results: dict[str, int]) -> str | None:
        """Return a challenge string to plant a flag, or None to not plant.
        results contains last round's public flag scores (challenge -> net score).
        Empty on the first round."""
        pass

    def respond(self, flags: list[str]) -> list[str | None]:
        """Given all planted flags this round, return a response for each.
        None to skip a flag. A bot can respond to multiple flags."""
        pass

    def judge(self, responses: list[str]) -> list[bool]:
        """Accept or reject each response to your flag."""
        pass
```

A bot can both plant and respond in the same round.

## What Bots Know

- Their own team assignment
- Number of bots and teams in the game
- All planted flags each round (challenge messages are public)
- History of their own interactions (what they sent/received, accept/reject outcomes)
- Their own score
- Round number

## What Bots Don't Know

- Who planted which flag
- Who sent which response
- Other bots' team assignments
- Other bots' source code

## Open Design Questions

1. **What prevents degenerate strategies?** E.g., never planting (safe but scoreless), or always rejecting. Need incentive design that rewards risk-taking.

2. **How long is a game?** Fixed rounds (e.g., 50-100)? Until a score threshold?

3. **Is source code visible?** If yes, the game becomes about writing verification logic that works even when readable.

4. **Score visibility?** Can bots see the full scoreboard or only their own score?
