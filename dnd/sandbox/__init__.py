"""Sandbox layer: castles, world, deployments, the tick worker.

Sits on top of the rules engine in ``dnd.engine`` (which is
mode-agnostic). The sandbox owns the persistent shared world and
the patron-facing HTTP surface.
"""
