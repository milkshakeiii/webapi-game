"""Flag Football game engine."""

import random


class Game:
    def __init__(self, team_a: list, team_b: list):
        """Each team is a list of Bot instances."""
        self.bots = []
        for bot in team_a:
            self.bots.append({"bot": bot, "team": "A", "score": 0})
        for bot in team_b:
            self.bots.append({"bot": bot, "team": "B", "score": 0})
        random.shuffle(self.bots)
        self.results = {}  # last round's public flag scores

    def run(self, rounds=50):
        for round_num in range(1, rounds + 1):
            self.play_round(round_num)
        return self.scores()

    def play_round(self, round_num):
        # Phase 1 — Plant
        flags = []  # (bot_index, challenge_string)
        for i, entry in enumerate(self.bots):
            challenge = entry["bot"].plant(self.results)
            if challenge is not None:
                flags.append((i, challenge))

        flag_strings = [challenge for _, challenge in flags]

        # Phase 2 — Respond
        # responses_per_flag[flag_idx] = [(bot_index, response_string)]
        responses_per_flag = [[] for _ in flags]
        for i, entry in enumerate(self.bots):
            responses = entry["bot"].respond(flag_strings)
            for flag_idx, response in enumerate(responses):
                if response is not None:
                    responses_per_flag[flag_idx].append((i, response))

        # Phase 3 — Judge
        self.results = {}
        for flag_idx, (planter_idx, challenge) in enumerate(flags):
            responders = responses_per_flag[flag_idx]
            if not responders:
                self.results[challenge] = 0
                continue

            response_strings = [r for _, r in responders]
            judgments = self.bots[planter_idx]["bot"].judge(response_strings)

            flag_score = 0
            for (responder_idx, _), accepted in zip(responders, judgments):
                if accepted:
                    same_team = self.bots[planter_idx]["team"] == self.bots[responder_idx]["team"]
                    if same_team:
                        self.bots[planter_idx]["score"] += 2
                        self.bots[responder_idx]["score"] += 2
                        flag_score += 2
                    else:
                        self.bots[planter_idx]["score"] -= 3
                        self.bots[responder_idx]["score"] += 5
                        flag_score -= 3

            self.results[challenge] = flag_score

        # Print round summary
        print(f"Round {round_num}: {len(flags)} flags, results: {self.results}")

    def scores(self):
        team_scores = {"A": 0, "B": 0}
        for entry in self.bots:
            team_scores[entry["team"]] += entry["score"]
        print(f"\nFinal scores — Team A: {team_scores['A']}, Team B: {team_scores['B']}")
        return team_scores
