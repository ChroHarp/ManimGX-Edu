"""Synchronize existing animation sections to measured converted audio durations."""
import json
from pathlib import Path

import manimgx as m
from manimgx_tw_helper import TWScene

ROOT = Path(__file__).resolve().parent / "narration_f0"


class NarratedScene(TWScene):
    narration_root = ROOT
    timeline_root: Path | None = None

    def begin_narration(self, layout: str, number: int) -> None:
        self.end_narration()
        key = f"{layout}_{number:02d}"
        manifest = json.loads((self.narration_root / "manifest.json").read_text(encoding="utf-8"))
        text = next(c["text"] for c in manifest["clips"] if c["key"] == key)
        sound = m.Sound(self.narration_root / "final" / f"{key}.wav")
        self.add_sound(sound)
        self.add_subcaption(text, duration=sound.duration)
        self._narration_key = key
        self._narration_layout = layout
        self._narration_start = self.time
        self._narration_end = self.time + sound.duration

    def end_narration(self) -> None:
        end = getattr(self, "_narration_end", self.time)
        if end > self.time:
            self.wait(end - self.time)
        key = getattr(self, "_narration_key", None)
        if key is not None:
            timeline = getattr(self, "_narration_timeline", [])
            timeline.append({"key": key, "start": self._narration_start,
                             "audio_end": end, "section_end": self.time})
            self._narration_timeline = timeline
            ((self.timeline_root or self.narration_root) / f"{self._narration_layout}_timeline.json").write_text(
                json.dumps(timeline, indent=2), encoding="utf-8")
            self._narration_key = None
        self._narration_end = self.time
