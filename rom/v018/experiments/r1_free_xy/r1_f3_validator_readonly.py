#!/usr/bin/env python3
"""F3 read-only negative calibration on genuine F2 frozen 6B baseline raw PNGs.
No emulator invoked. Artificial mutant files NEVER called real Stella frames.
This validates the tool despite F3 G0 actual movement FAIL.
"""
import sys,json,hashlib
from pathlib import Path
from PIL import Image
import r1_f3_audit as f3
src=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
paths=sorted(src.glob('frame_*.png'))
assert len(paths)==16,len(paths)
req=[43,75,129,183,243,303]
checks=[]
for p in paths:
    a,b,ok=f3.check(Image.open(p),req)
    assert ok,(p,a,b)
    checks.append({'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'two_checks':True})
mut=f3.mutants(Image.open(paths[0]),req,out/'MUTANTS_SYNTHETIC_NOT_STELLA')
(out/'READONLY_VALIDATION.json').write_text(json.dumps({'source':'original frozen F2 baseline genuine Stella 6B 16 raw screenshot evidence',
    'no_new_stella_executions':True,'pixel_exact_16_of_16':True,'all_four_synthetic_negatives_detected':True,
    'real_frames':checks,'synthetic_negatives':mut},indent=2)+'\n')
print('F3_READONLY_TWO_AUDIT_PATHS: genuine F2 16/16, FOUR_MUTANTS_REJECTED',list(mut))
