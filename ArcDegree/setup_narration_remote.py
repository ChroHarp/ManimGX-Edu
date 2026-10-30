import subprocess
import sys

subprocess.run(['git', 'clone', 'https://github.com/Plachtaa/seed-vc.git', '/content/seed-vc'], check=True)
subprocess.run(['git', 'checkout', '51383efd921027683c89e5348211d93ff12ac2a8'], cwd='/content/seed-vc', check=True)
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'munch', 'einops', 'descript-audio-codec', 'descript-audiotools', 'huggingface_hub', 'hf_transfer', 'pydub', 'soundfile', 'hydra-core'], check=True)
