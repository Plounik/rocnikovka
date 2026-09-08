"""Convert the scanner's face readings to a Kociemba facelet string.

The scanner reports each face in this order::

    center, far edge, corner, edge, corner, edge, corner, edge, corner

The six faces must be supplied in U, F, R, B, L, D order.  Kociemba expects
the faces in U, R, F, D, L, B order, with each face written row by row.
"""

from ast import literal_eval
from collections import Counter
import sys


SCANNED_FACE_ORDER = ("U", "F", "R", "B", "L", "D")
KOCIEMBA_FACE_ORDER = ("U", "R", "F", "D", "L", "B")

# For each face, raw index -> conventional 3x3 face-grid index.
# The face-grid indices are row-major:
#
#     0 1 2
#     3 4 5
#     6 7 8
#
RAW_TO_GRID = {
    "U": (4, 1, 2, 5, 8, 7, 6, 3, 0),
    "F": (4, 7, 6, 3, 0, 1, 2, 5, 8),
    "R": (4, 5, 8, 7, 6, 3, 0, 1, 2),
    "B": (4, 5, 8, 7, 6, 3, 0, 1, 2),
    "L": (4, 5, 8, 7, 6, 3, 0, 1, 2),
    "D": (4, 5, 8, 7, 6, 3, 0, 1, 2),
}


def _as_face_mapping(scanned_faces):
    """Return the scan as a mapping keyed by U/F/R/B/L/D."""
    if hasattr(scanned_faces, "keys"):
        missing = [face for face in SCANNED_FACE_ORDER if face not in scanned_faces]
        if missing:
            raise ValueError("Missing scanned face(s): " + ", ".join(missing))
        return {face: list(scanned_faces[face]) for face in SCANNED_FACE_ORDER}

    faces = list(scanned_faces)
    if len(faces) != len(SCANNED_FACE_ORDER):
        raise ValueError("Expected exactly six faces in U, F, R, B, L, D order")
    return dict(zip(SCANNED_FACE_ORDER, (list(face) for face in faces)))


def _validate_scan(scan):
    for face in SCANNED_FACE_ORDER:
        values = scan[face]
        if len(values) != 9:
            raise ValueError(
                "Face {} has {} values; every face must have exactly 9".format(
                    face, len(values)
                )
            )
        if any(not isinstance(value, str) or not value for value in values):
            raise ValueError("Face {} contains an empty or non-text color".format(face))

    center_colors = [scan[face][0] for face in SCANNED_FACE_ORDER]
    if len(set(center_colors)) != 6:
        raise ValueError("The six center colors must be distinct: {}".format(center_colors))

    counts = Counter(
        color for face in SCANNED_FACE_ORDER for color in scan[face]
    )
    expected = {color: 9 for color in center_colors}
    if counts != expected:
        details = ", ".join(
            "{}={}".format(color, counts.get(color, 0))
            for color in center_colors
        )
        raise ValueError(
            "Invalid color totals (expected 9 of each center color; got {})".format(
                details
            )
        )


def convert_to_kociemba(scanned_faces, validate=True):
    """Convert scanner readings to Kociemba's 54-character facelet string.

    ``scanned_faces`` may be either:

    * six lists/tuples in U, F, R, B, L, D order; or
    * a mapping with keys U, F, R, B, L, D.

    The center colors are used to identify Kociemba's face letters, so the
    cube does not need to use the color orientation assumed by the scanner
    movement code.
    """
    scan = _as_face_mapping(scanned_faces)
    if validate:
        _validate_scan(scan)

    color_to_face = {
        scan[face][0]: face for face in SCANNED_FACE_ORDER
    }
    grids = {}
    for face in SCANNED_FACE_ORDER:
        grid = [None] * 9
        for raw_index, grid_index in enumerate(RAW_TO_GRID[face]):
            grid[grid_index] = scan[face][raw_index]
        grids[face] = grid

    try:
        return "".join(
            color_to_face[color]
            for face in KOCIEMBA_FACE_ORDER
            for color in grids[face]
        )
    except KeyError as error:
        raise ValueError(
            "Color {!r} does not match any face center".format(error.args[0])
        )


def _parse_input_line(line, expected_face):
    """Parse either a pasted Python list or ``U: [...]`` line."""
    text = line.strip()
    if ":" in text:
        label, payload = text.split(":", 1)
        if label.strip().upper() in SCANNED_FACE_ORDER:
            if label.strip().upper() != expected_face:
                raise ValueError(
                    "Expected face {}, received {}".format(
                        expected_face, label.strip().upper()
                    )
                )
            text = payload.strip()

    try:
        values = literal_eval(text)
    except (SyntaxError, ValueError) as error:
        raise ValueError(
            "Could not parse {}; paste a Python-style list such as "
            "['Y', 'O', ...] ({})".format(expected_face, error)
        )

    if not isinstance(values, (list, tuple)):
        raise ValueError("{} must be a list or tuple of 9 colors".format(expected_face))
    return list(values)


def main():
    print("Paste one scanner list for each face in U, F, R, B, L, D order.")
    scanned_faces = []
    try:
        for face in SCANNED_FACE_ORDER:
            scanned_faces.append(_parse_input_line(input(face + ": "), face))
        facelets = convert_to_kociemba(scanned_faces)
    except (EOFError, ValueError) as error:
        print("Invalid scan: {}".format(error), file=sys.stderr)
        return 1

    print("Kociemba facelets:")
    print(facelets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
