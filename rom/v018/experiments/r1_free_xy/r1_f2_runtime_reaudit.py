#!/usr/bin/env python3
"""R1-F2: corrected READ-ONLY audit of frozen 32 genuine Stella raw PNGs.
The first CI checker read FRAMELO using the debugger's NEXT-frame label.
At a frame boundary, Stella's screenshot still displays the previous completed
frame; that frame was rasterized using FRAMELO = displayed_debugger_frame - 2.
This script performs NO Stella run and creates NO emulator pixel data.
"""
import argparse,csv,hashlib,io,json,zipfile
from collections import Counter
from pathlib import Path
from PIL import Image
from r1_f2_checker import audit_image,BASE,EXPECTED
p=argparse.ArgumentParser()
p.add_argument('zip_archive',type=Path)
p.add_argument('--csv',type=Path,required=True)
p.add_argument('--json',type=Path,required=True)
a=p.parse_args()
assert a.zip_archive.exists()
prefix='rom/v018/experiments/r1_free_xy/evidence/r1_f2_runtime/raw/'
records=[]
with zipfile.ZipFile(a.zip_archive) as z:
    assert z.testzip() is None
    names=sorted(n for n in z.namelist() if n.startswith(prefix+'frame_') and n.endswith('.png'))
    assert len(names)==32,(len(names),'wrong number of genuine captured frames')
    for k,name in enumerate(names,1):
        dbg_frame=10+k
        # Source-relevant FRAMELO during the COMPLETED visual frame shown here.
        completed_frame_ram_value=dbg_frame-2
        bit2=completed_frame_ram_value & 4
        requested=EXPECTED['P1'] if bit2 else BASE
        raw=z.read(name)
        result=audit_image(Image.open(io.BytesIO(raw)),requested)
        record=dict(capture_index=k,debugger_frame_label=dbg_frame,
                    completed_frame_FRAMELO=completed_frame_ram_value,
                    FRAMELO_bit2=bit2,
                    requested_X=requested,source_mask_types=['large_male','large_male','large_female','large_female','small_male','small_female'],
                    png_sha256=hashlib.sha256(raw).hexdigest(),
                    observed_X=result.get('rendered'),nine_rows_mask_costs=result.get('mask_row_costs'),
                    exact=result.get('exact'),P0_yellow=result.get('P0_yellow'),
                    M0_active=result.get('M0_active'),PF_brown_left=result.get('PF_brown_left'),
                    PF_brown_right=result.get('PF_brown_right'),
                    NTSC_262=result.get('ntsc262'),raw_png_in_zip=name)
        records.append(record)
        print('R1_F2_G2_READONLY',dbg_frame,bit2,requested,result.get('rendered'),result.get('exact'))
assert sum(r['exact'] for r in records)==32
assert Counter(r['FRAMELO_bit2'] for r in records)==Counter({0:16,4:16})
assert all(r['observed_X'][i]==BASE[i] for r in records for i in range(6) if i!=2)
assert all(r['nine_rows_mask_costs']==[[0]*9]*6 for r in records)
assert sum(records[i]['FRAMELO_bit2']!=records[i-1]['FRAMELO_bit2'] for i in range(1,32))>=7
a.csv.parent.mkdir(parents=True,exist_ok=True);a.json.parent.mkdir(parents=True,exist_ok=True)
with a.csv.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
a.json.write_text(json.dumps({'original_emulator_zip_sha256':hashlib.sha256(a.zip_archive.read_bytes()).hexdigest(),
          'no_new_emulator_executions':True,'exact_32_of_32':True,'phase_calibration':'Stella debugger frame boundary shows most recently completed frame; source FRAMELO for that image = debugger label - 2',
          'frames':records},indent=2)+'\n')
print('F2_LIMITED_RUNTIME_SINGLE_X_PASS',len(records),'source_exact_no_ghost',True)
print('RE_AUDIT_SHA256_CSV',hashlib.sha256(a.csv.read_bytes()).hexdigest())
print('RE_AUDIT_SHA256_JSON',hashlib.sha256(a.json.read_bytes()).hexdigest())
