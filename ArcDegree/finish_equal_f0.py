"""Keep raw conversion and create normalized delivery clips."""
import json
import subprocess
import wave
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
dest = root / 'narration_equal_f0'
raw = dest / 'converted'
raw.mkdir(exist_ok=True)
(dest / 'final').mkdir(exist_ok=True)
with zipfile.ZipFile(dest / 'converted.zip') as archive:
    archive.extractall(raw)
manifest = json.loads((root / 'narration_edge_equal/manifest.json').read_text(encoding='utf-8'))
for clip in manifest['clips']:
    key = clip['key']
    source = raw / (key + '_vc.wav')
    assert source.exists(), f'Missing converted clip: {key}'
    output = dest / 'final' / (key + '.wav')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(source), '-af', 'loudnorm=I=-18:TP=-2:LRA=9', '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', str(output)], check=True)
    with wave.open(str(output)) as f:
        clip['duration'] = f.getnframes() / f.getframerate()
    print(key, clip['duration'])
manifest['stage'] = 'Selected Seed-VC F0; source is approved Edge-TTS audio'
(dest / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
