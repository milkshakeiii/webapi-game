"""Process (warrior thread) management for Network CoreWar."""


class Process:
    """A single execution thread belonging to a player."""

    __slots__ = ('player_id', 'node_id', 'pc', '_fork_payload', '_fork_target')

    def __init__(self, player_id, node_id, pc=0):
        self.player_id = player_id
        self.node_id = node_id
        self.pc = pc
        self._fork_payload = None
        self._fork_target = None

    def __repr__(self):
        return f"Process(p{self.player_id}, node={self.node_id}, pc={self.pc})"
