#!/usr/bin/env python3
"""Report only measured pixels from unedited Stella 6.7.1 X11 screenshots.

This is a scoped R1 feasibility tool. A single pixel group is not a human-figure PASS.
Only 2 scenes at each source configuration are sampled; no 600-frame claim.
"""
from pathlib import Path
from hashlib import sha256
from PIL import Image
import numpy as np
import json, sys
root=Path(sys.argv[1])
rows=[]
ref=None
for variant in ('vb_9_interleave','vb_18_doubled','vb_9_vdel'):
 for frame in (13,18):
  p=root/'evidence'/variant/f'frame_{frame}'/'stella_full.png'
  im=Image.open(p).convert('RGB')
  assert im.size==(1366,900), (p,im.size)
  scanline_roi=im.crop((660,92,692,109))
  hudhash=sha256(scanline_roi.tobytes()).hexdigest()
  if ref is None:ref=hudhash
  # Full display region excludes the tan lower console border.
  a=np.array(im)[66:294,103:424,:]
  mx=a.max(axis=2); mi=a.min(axis=2)
  white=(mi>200)&((mx-mi)<35)
  yellow=(a[:,:,0]>160)&(a[:,:,1]>140)&(a[:,:,2]<120)
  wy,wx=np.where(white)
  yy,xx=np.where(yellow)
  out={
   'variant':variant, 'debugger_frame_label':frame,
   'raw_screenshot':str(p.relative_to(root)),
   'raw_screenshot_sha256':sha256(p.read_bytes()).hexdigest(),
   'display_resolution':[321,228],
   'stella_scanline_hud_matches_calibrated_262':hudhash==ref,
   'hud_sha256_rgb':hudhash,
   'white_pixel_count':int(white.sum()),
   'white_scanlines':int(white.any(axis=1).sum()),
   'white_x_range_gui':[int(wx.min()+103),int(wx.max()+103)] if len(wx) else None,
   'white_y_range_gui':[int(wy.min()+66),int(wy.max()+66)] if len(wy) else None,
   'white_pixels_right_half_of_test_playfield':int(white[:,170:].sum()),
   'yellow_scanlines':int(yellow.any(axis=1).sum()),
   'yellow_x_range_gui':[int(xx.min()+103),int(xx.max()+103)] if len(xx) else None,
   'two_distinct_independent_8x9_silhouettes_verified':False,
  }
  rows.append(out)
assert len(rows)==6
(root/'VENETIAN_MEASUREMENTS.json').write_text(json.dumps({'source':'Actual Stella GUI (X11) screenshots', 'calibration':'262 text visually confirmed in the reference screenshot; comparison is full ROI byte matching, not OCR', 'calibrated_262_hud_sha256_rgb':ref,'observations':rows},indent=2)+'\n')
for x in rows:
 print(x['variant'],x['debugger_frame_label'],'white_rows',x['white_scanlines'],'white_px',x['white_pixel_count'],'xrange',x['white_x_range_gui'],'262',x['stella_scanline_hud_matches_calibrated_262'])
