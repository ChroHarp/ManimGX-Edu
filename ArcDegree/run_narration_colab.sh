set -eu
export PATH="$HOME/.local/bin:$PATH"
cd /mnt/d/WebDesign/ManimCEAnimate
session=arcdegreef020261028
cleanup() { colab stop -s "$session" || true; }
trap cleanup EXIT
colab status
colab usage
# Session is created after checking account status; reuse this task's session.
colab upload -s "$session" ArcDegree/narration_f0/arc_sources.zip /content/arc_sources.zip
colab upload -s "$session" ArcDegree/narration_f0/target.wav /content/tsuda.wav
colab upload -s "$session" ArcDegree/narration_f0/convert_voice_seedvc.py /content/convert_voice_seedvc.py
colab exec -s "$session" --timeout 1800 -f ArcDegree/convert_narration_remote.py || true
colab download -s "$session" /content/arc_converted.zip ArcDegree/narration_f0/arc_converted.zip
