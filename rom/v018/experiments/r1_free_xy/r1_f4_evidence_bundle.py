#!/usr/bin/env python3
"""R1-F4 READ-ONLY evidence packaging. No DASM or Stella.
Input: original downloaded GitHub Actions c18/c21 successful artifacts.
Output: standalone two-probe evidence directory with every raw image,
source/list/ROM, checksum manifest and per-file machine-readable index.
"""
from pathlib import Path
import hashlib,json,shutil,os,sys
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_one(root,phase,expected_sha):
    base=root/'rom/v018/experiments/r1_free_xy'
    assert base.is_dir(),(root,'artifact layout')
    stem=f'r1_f4_6B_I0_C{phase:02d}_I2_FIXED'
    rom=base/'dist'/f'{stem}_F6.bin'
    assert rom.stat().st_size==16384 and sha(rom)==expected_sha
    binary=rom.read_bytes()
    assert all(binary[i*4096:(i+1)*4096]==binary[:4096] for i in range(4))
    assert (base/'dist'/f'{stem}.lst').exists()
    assert (base/'dist'/f'{stem}.sym').exists()
    assert (base/f'{stem}.asm').exists()
    raw=base/'evidence'/f'r1_f4_c{phase:02d}'
    audit=json.loads((raw/'STRICT_16_FRAME_PIXEL_AUDIT.json').read_text())
    assert len(audit['real_stella_frames'])==16
    assert all(v['both_independent_masks_exact'] for v in audit['real_stella_frames'])
    assert audit['classification'] in ('F4_NO_SECOND_X_PHASE_RESPONSE','F4_INDEX0_PHASE_GEOMETRY_LOCAL_PASS')
    for d in ('raw','raw_full'):
        files=sorted((raw/d).glob('frame_*.png'))
        assert len(files)==16,(phase,d,len(files))
        import struct
        for file in files:
            data=file.read_bytes()[:24]
            assert data[:8]==bytes([137,80,78,71,13,10,26,10])
            width,height=struct.unpack('>II',data[16:24])
            assert (width,height)==((900,300) if d=='raw' else (1366,900))
    # Each raw pair and each trap image must match its independently
    # recorded SHA-256: all names are paths from base, NOT from sum-file dir.
    for f in ('RAW_CROP_SHA256SUMS.txt','RAW_FULL_SHA256SUMS.txt','traps/REAL_TIA_TRAP_PNG_SHA256.txt'):
        sums=(raw/f).read_text().splitlines()
        assert len(sums)==(6 if 'trap' in f.lower() else 16),(f,len(sums))
        for line in sums:
            expected,filename=line.split('  ',1)
            p=base/filename
            assert p.exists() and sha(p)==expected,(phase,filename)
    for file in (raw/'traps').glob('*/stella_full.png'):
        assert file.stat().st_size>8000,(file,'possibly black')
    assert len(list((raw/'traps').glob('*/stella_full.png')))==6
    assert (raw/'MUTANT_NEGATIVE_SYNTHETIC_NOT_STELLA').exists()
    assert (raw/'initial_full.png').exists() and (raw/'final_full.png').exists()
    return {'phase':phase,'ROM_SHA256':expected_sha,'ROM_bytes':16384,
            'real_raw_crop_frames':16,'real_full_debugger_frames':16,
            'register_trap_screenshots':6,'all_shas_checked':True,
            'pixel_classification':audit['classification'],
            'actual_X0':audit['actual_position_set'],
            'no_additional_emulator_execution':True}
def main():
    assert len(sys.argv)==4,'usage: script c18_source c21_source combined_out'
    src18,src21,out=map(Path,sys.argv[1:])
    assert not out.exists(),('will not overwrite evidence',out)
    a=check_one(src18,18,'d06fa761ddcc4756fbb2b9b2d72bbe49cc4ec5146a04c8e5e4ff8483dfd9f15d')
    b=check_one(src21,21,'fc3e3622e155c3faded0d91e12f2889c24d0c9eb16822bbef58a4d7cdd6d704f')
    out.mkdir(parents=True)
    for src,folder in ((src18,'C18_REAL_STELLA'),(src21,'C21_REAL_STELLA')):
        shutil.copytree(src,out/folder)
    own=Path(__file__).resolve().parent
    extra=out/'REPRO_SOURCE_F4'
    extra.mkdir()
    for name in ('r1_f4_source_preflight.py','r1_f4_build.py','r1_f4_audit.py',
                 'r1_f4_capture.sh','r1_f4_trace.sh','r1_f4_evidence_bundle.py'):
        shutil.copy2(own/name,extra/name)
    status={'type':'R1-F4 READ_ONLY EVIDENCE BUNDLE, NO DASM/STELLA',
        'probes':[a,b],
        'FR_F3_FROZEN_SHA':'65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190',
        'FR_F2_FROZEN_SHA':'485a6c10047fb9b41e589ac3df724c1bc70f0283',
        'mask_Git_blob':'058800a4c1904d1ff289e7e61b3902aa111ba16d',
        'all_16_per_phase_original_PNG_hashes_checked':True,
        'no_two_individual_dynamic_runtime':True,
        'FULL_R1':'BLOCKED_NOT_ACCEPTED'}
    (out/'BUNDLE_VALIDATION.json').write_text(json.dumps(status,indent=2)+'\n')
    entries=[]
    for f in sorted(out.rglob('*')):
        if f.is_file():
            entries.append({'path':f.relative_to(out).as_posix(),
                            'bytes':f.stat().st_size,'SHA256':sha(f)})
    (out/'EVIDENCE_FILE_INDEX.json').write_text(json.dumps(entries,indent=2)+'\n')
    (out/'MANIFEST_SHA256SUMS.txt').write_text(''.join(
         item['SHA256']+'  '+item['path']+'\n' for item in entries))
    print('F4_COMPLETE_EVIDENCE_READONLY_VALIDATED',len(entries),'files',
          'real debugger images',44,'one F4 ROM each phase',
          'status',a['pixel_classification'],b['pixel_classification'])
if __name__=='__main__':main()
