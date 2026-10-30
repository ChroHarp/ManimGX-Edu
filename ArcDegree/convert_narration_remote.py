"""Colab entry: one loaded F0 model, separate utterances, original selected parameters."""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path('/content/arc_narration')
ROOT.mkdir(exist_ok=True)
OUT = ROOT / 'converted'
OUT.mkdir(exist_ok=True)


def run(args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)


try:
    with zipfile.ZipFile('/content/arc_sources.zip') as z:
        z.extractall(ROOT)
    if not Path('/content/seed-vc/.git').exists():
        run(['git', 'clone', 'https://github.com/Plachtaa/seed-vc.git', '/content/seed-vc'])
    run(['git', 'checkout', '51383efd921027683c89e5348211d93ff12ac2a8'], '/content/seed-vc')
    run([sys.executable, '-m', 'pip', 'install', '-q', 'munch', 'einops', 'descript-audio-codec', 'descript-audiotools', 'huggingface_hub', 'hf_transfer', 'pydub', 'soundfile', 'hydra-core'])
    sys.path.insert(0, '/content')
    import convert_voice_seedvc as vc
    import torch
    import numpy as np
    import soundfile as sf
    import os
    os.chdir('/content/seed-vc')
    models = globals().get('arc_f0_models')
    if models is None:
        models = vc.load_models(vc.SeedVCModelConfig(f0_condition=True))
    records = []
    for f in sorted((ROOT / 'source').glob('*.wav')):
        np.random.seed(42)
        torch.manual_seed(42)
        torch.cuda.manual_seed_all(42)
        dest = OUT / (f.stem + '_vc.wav')
        vc.convert_single_audio(models, str(f), '/content/tsuda.wav', str(dest), f0_condition=True, auto_f0_adjust=False, pitch_shift=0, diffusion_steps=30, inference_cfg_rate=0.7, timbre_blend=1.0)
        info = sf.info(dest)
        records.append({'key': f.stem, 'duration': info.duration, 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
        (OUT / 'progress.json').write_text(json.dumps(records, indent=2))
        print('COMPLETED', f.stem, info.duration, flush=True)
    metadata = {'seedvc_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), 'parameters': {'f0_condition': True, 'auto_f0_adjust': False, 'pitch_shift': 0, 'seed': 42, 'diffusion_steps': 30, 'inference_cfg_rate': 0.7, 'timbre_blend': 1.0}, 'clips': records}
    metadata['target_sha256'] = hashlib.sha256(Path('/content/tsuda.wav').read_bytes()).hexdigest()
    metadata['gpu'] = subprocess.check_output(['nvidia-smi'], text=True)
    metadata['pip_freeze'] = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True)
    metadata['models'] = []
    for base in [Path('/content/seed-vc/checkpoints'), Path.home()/'.cache/huggingface/hub']:
        if base.exists():
            for f in base.rglob('*'):
                if f.is_file() and ('snapshots' in str(f) or 'checkpoints' in str(f)):
                    with f.open('rb') as stream:
                        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                    metadata['models'].append({'path': str(f), 'sha256': digest, 'bytes': f.stat().st_size})
    (OUT / 'conversion.json').write_text(json.dumps(metadata, indent=2))
finally:
    with zipfile.ZipFile('/content/arc_converted.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for f in OUT.iterdir():
            z.write(f, f.name)
