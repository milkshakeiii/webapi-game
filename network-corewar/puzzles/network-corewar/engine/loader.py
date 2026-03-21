"""Load .ncw program files for Network CoreWar."""

from .instruction import parse_line


def load_program(filepath, node_size=128):
    """Load a program from a .ncw file. Returns (name, list of Cells).

    All cell values are wrapped mod node_size to prevent out-of-range exploits.
    """
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
                cell.a_value = cell.a_value % node_size
                cell.b_value = cell.b_value % node_size
                cells.append(cell)

    return name, cells
