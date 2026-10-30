set -eu
export PATH="$HOME/.local/bin:$PATH"
cd /mnt/d/WebDesign/ManimCEAnimate
session=arcequalf020261028
cleanup() { colab stop -s "$session" || true; }
trap cleanup EXIT
colab new -s "$session" --gpu T4
colab upload -s "$session" ArcDegree/narration_equal_f0/sources.zip /content/arc_sources.zip
colab upload -s "$session" ArcDegree/narration_f0/target.wav /content/tsuda.wav
colab upload -s "$session" ArcDegree/narration_f0/convert_voice_seedvc.py /content/convert_voice_seedvc.py
colab exec -s "$session" --timeout 1200 -f ArcDegree/convert_narration_remote.py || true
colab download -s "$session" /content/arc_converted.zip ArcDegree/narration_equal_f0/converted.zip
