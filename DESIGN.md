# Flag Football — Game Design

## Overview

A turn-based trust game where players write code (bots) that plant flags, capture flags, and try to distinguish teammates from opponents through data exchange.

## Players

- Two teams (e.g., 3v3 or 5v5)
- Each player writes a bot — a program that implements a simple interface
- Bots are the players' avatars in the game

## Turn Structure

Each round, every bot can take one action:

1. **Plant a flag** — make yourself available for interaction
2. **Capture a flag** — initiate an exchange with a bot that has a flag planted

When a flag is captured, a **handshake** occurs:

1. The flag-planter sends a **challenge** (arbitrary data)
2. The flag-capturer sends a **response** (arbitrary data)
3. The flag-planter decides: **accept** or **reject**

## Scoring

| Outcome | Planter | Capturer |
|---|---|---|
| Accept teammate | +2 | +2 |
| Accept opponent | -3 | +5 |
| Reject (anyone) | 0 | 0 |

(Numbers are placeholders — need to balance incentives to plant flags vs. play it safe.)

## Bot Interface

```python
class Bot:
    def action(self, game_state) -> Action:
        """Choose to plant a flag or capture someone else's flag."""
        pass

    def challenge(self, capturer_id) -> bytes:
        """Generate a challenge for someone who captured your flag."""
        pass

    def respond(self, planter_id, challenge) -> bytes:
        """Respond to a challenge when you capture someone's flag."""
        pass

    def judge(self, capturer_id, response) -> bool:
        """Decide whether to accept or reject based on the response."""
        pass
```

## What Bots Know

- Their own team assignment
- The IDs of all bots in the game (but NOT which team they're on)
- History of their own past interactions (who they exchanged with, what was sent, accept/reject outcomes)
- The current scoreboard
- Round number

## What Bots Don't Know

- Other bots' team assignments
- Other bots' private interaction histories
- Other bots' source code

## Open Design Questions

1. **Can bots communicate outside of flag exchanges?** If yes, teammates could coordinate protocols. If no, they have to develop trust from scratch.

2. **Are bot IDs persistent?** If IDs shuffle each round, reputation tracking becomes impossible. If persistent, trust networks emerge naturally.

3. **Can bots see who planted flags?** If yes, they can choose who to interact with. If no, captures are random/blind.

4. **What prevents degenerate strategies?** E.g., never planting a flag (safe but scoreless), or always rejecting (also safe but scoreless). Need incentive design that rewards risk-taking.

5. **How long is a game?** Fixed rounds? Time-based? Until a score threshold?

6. **Is source code visible?** In a coding competition, source might be submitted and visible to opponents. This changes the game dramatically — it becomes about obfuscation vs. reverse engineering.

7. **Multiple flags per round?** Can a bot plant multiple flags or capture multiple flags per round?
