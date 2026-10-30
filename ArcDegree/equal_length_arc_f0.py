"""Final selected F0 narration for the approved light-background scene."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ArcDegree.equal_length_arc_angles import EqualLengthArcAngles


class EqualLengthArcAnglesF0(EqualLengthArcAngles):
    narration_root = Path(__file__).resolve().parent / "narration_equal_f0"
    timeline_root = narration_root
