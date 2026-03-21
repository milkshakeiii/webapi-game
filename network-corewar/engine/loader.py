"""Load .ncw program files for Network CoreWar."""

from .instruction import parse_line


def load_program(filepath):
    """Load a program from a .ncw file. Returns (name, list of Cells)."""
    name = filepath
    cells = []

    with open(filepath) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith(';name'):
                name = stripped[5:].strip()
                continue
            if stripped.startswith(';author'):
                continue
            cell = parse_line(stripped)
            if cell is not None:
                cells.append(cell)

    return name, cells
