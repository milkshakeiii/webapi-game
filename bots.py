"""Example bots for Flag Football."""

import random


class AlwaysPlantBot:
    """Always plants the same challenge, accepts everyone. Naive and exploitable."""

    def plant(self, results):
        return "hello friend"

    def respond(self, flags):
        return ["I am your friend" for _ in flags]

    def judge(self, responses):
        return [True] * len(responses)


class RandomBot:
    """Plants sometimes, responds sometimes, accepts randomly."""

    def plant(self, results):
        if random.random() < 0.5:
            return f"random challenge {random.randint(0, 1000)}"
        return None

    def respond(self, flags):
        return [
            f"random response {random.randint(0, 1000)}" if random.random() < 0.5 else None
            for _ in flags
        ]

    def judge(self, responses):
        return [random.random() < 0.5 for _ in responses]


class CautiousBot:
    """Plants every round. Only accepts responses that echo back the challenge."""

    def plant(self, results):
        return "echo this back to me"

    def respond(self, flags):
        return [flag for flag in flags]

    def judge(self, responses):
        return [r == "echo this back to me" for r in responses]
