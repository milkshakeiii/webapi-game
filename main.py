"""Run a Flag Football game."""

from game import Game
from bots import AlwaysPlantBot, RandomBot, CautiousBot

team_a = [AlwaysPlantBot(), RandomBot(), CautiousBot()]
team_b = [AlwaysPlantBot(), RandomBot(), CautiousBot()]

game = Game(team_a, team_b)
game.run(rounds=20)
