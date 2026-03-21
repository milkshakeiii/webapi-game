"""Instruction parsing and representation for Network CoreWar."""

import re
from .graph import Cell

OPCODES = {'DAT', 'MOV', 'ADD', 'SUB', 'MOD', 'JMP', 'JMZ', 'CMP', 'SEND', 'RECV', 'FORK', 'SCAN'}
MODES = {'#', '$', '@'}


def parse_operand(s):
    """Parse an operand string like '#3', '$-1', '@2', or '3' (default $)."""
    s = s.strip()
    if not s:
        return '$', 0
    if s[0] in MODES:
        return s[0], int(s[1:])
    return '$', int(s)


def parse_line(line):
    """Parse a single instruction line into a Cell. Returns None for comments/blanks."""
    # Strip comments
    line = line.split(';')[0].strip()
    if not line:
        return None

    parts = re.split(r'[\s,]+', line, maxsplit=3)
    if not parts:
        return None

    opcode = parts[0].upper()
    if opcode not in OPCODES:
        raise ValueError(f"Unknown opcode: {opcode}")

    a_mode, a_value = '$', 0
    b_mode, b_value = '#', 0

    if len(parts) >= 2:
        a_mode, a_value = parse_operand(parts[1])
    if len(parts) >= 3:
        b_mode, b_value = parse_operand(parts[2])

    return Cell(opcode, a_mode, a_value, b_mode, b_value)


def cell_to_str(cell):
    """Format a cell as a readable instruction string."""
    return f"{cell.opcode} {cell.a_mode}{cell.a_value}, {cell.b_mode}{cell.b_value}"
