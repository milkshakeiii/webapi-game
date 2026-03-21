"""Load .ncw and .ncwc (compiled) program files for Network CoreWar."""

import struct
from .graph import Cell
from .instruction import parse_line, OPCODES

# Compiled format: 4-byte magic, 1-byte name length, name bytes,
# then per-cell: 1-byte opcode index, 1-byte modes (a<<4 | b), 2 signed shorts (a_val, b_val)
MAGIC = b'NCW\x01'
_OPCODE_LIST = sorted(OPCODES)
_OPCODE_TO_IDX = {op: i for i, op in enumerate(_OPCODE_LIST)}
_IDX_TO_OPCODE = {i: op for i, op in enumerate(_OPCODE_LIST)}
_MODE_TO_IDX = {'#': 0, '$': 1, '@': 2}
_IDX_TO_MODE = {0: '#', 1: '$', 2: '@'}


def load_program(filepath, node_size=128):
    """Load a program from .ncw or .ncwc file. Returns (name, list of Cells)."""
    if filepath.endswith('.ncwc'):
        return load_compiled(filepath, node_size)
    return load_source(filepath, node_size)


def load_source(filepath, node_size=128):
    """Load a program from a .ncw source file. Returns (name, list of Cells)."""
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


def compile_program(filepath, out_path, node_size=128):
    """Compile a .ncw source file to .ncwc binary format."""
    name, cells = load_source(filepath, node_size)
    name_bytes = name.encode('utf-8')[:255]

    with open(out_path, 'wb') as f:
        f.write(MAGIC)
        f.write(struct.pack('B', len(name_bytes)))
        f.write(name_bytes)
        for cell in cells:
            op_idx = _OPCODE_TO_IDX[cell.opcode]
            modes = (_MODE_TO_IDX[cell.a_mode] << 4) | _MODE_TO_IDX[cell.b_mode]
            f.write(struct.pack('BBhh', op_idx, modes, cell.a_value, cell.b_value))


def load_compiled(filepath, node_size=128):
    """Load a compiled .ncwc program. Returns (name, list of Cells)."""
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        if magic != MAGIC:
            raise ValueError(f"Not a compiled NCW file: {filepath}")
        name_len = struct.unpack('B', f.read(1))[0]
        name = f.read(name_len).decode('utf-8')
        cells = []
        while True:
            chunk = f.read(6)
            if len(chunk) < 6:
                break
            op_idx, modes, a_val, b_val = struct.unpack('BBhh', chunk)
            opcode = _IDX_TO_OPCODE[op_idx]
            a_mode = _IDX_TO_MODE[(modes >> 4) & 0xF]
            b_mode = _IDX_TO_MODE[modes & 0xF]
            cells.append(Cell(opcode, a_mode, a_val % node_size, b_mode, b_val % node_size))
    return name, cells
