import os
import sys
sys.path.insert(0, '/content')
import convert_voice_seedvc as vc
os.chdir('/content/seed-vc')
arc_f0_models = vc.load_models(vc.SeedVCModelConfig(f0_condition=True))
print('ArcDegree F0 models ready', flush=True)
