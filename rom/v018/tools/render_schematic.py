"""Source-based *schematic* previews, explicitly NOT screenshots from Stella."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import build
O=build.ROOT/'evidence';O.mkdir(exist_ok=True)
S=4
COL={'bg':(5,8,13),'wall':(117,75,43),'brown':(117,75,43),'white':(239,239,234),
     'yellow':(255,225,0),'gold':(236,164,14),'orange':(247,110,18)}
def draw_cell(m,x,y,color):
 if 0<=x<40 and 0<=y<192:
  for xx in range(x*4,x*4+4):m.putpixel((xx,y),color)
def draw_sprite(m,x,y,pat,color):
 for row,line in enumerate(pat):
  for b,v in enumerate(line):
   if v=='#':
    pos=(x+b,y+row)
    if 0<=pos[0]<160 and 0<=pos[1]<192:m.putpixel(pos,color)
def label(im,title,path):
 scaled=im.resize((160*S,192*S),Image.Resampling.NEAREST)
 canvas=Image.new('RGB',(160*S,192*S+110),(26,27,30))
 canvas.paste(scaled,(0,0))
 d=ImageDraw.Draw(canvas)
 d.text((12,192*S+10),title,fill=(255,255,255))
 d.text((12,192*S+42),'SCHEMATIC PREVIEW - NOT STELLA',fill=(255,190,70))
 d.text((12,192*S+68),'Sprite X positions approximate',fill=(210,210,210))
 canvas.save(path)

def full(bank,door='orange'):
 im=Image.new('RGB',(160,192),COL['bg']);tb,_=build.pack(bank)
 for y in range(192):
  # per-line PF geometry reconstructed from build source
  mask=[]
  for k in range(2):
   a,b,c=[tb[k*3+i][y] for i in range(3)]
   mask += [(a>>(4+i))&1 for i in range(4)]
   mask += [(b>>(7-i))&1 for i in range(8)]
   mask += [(c>>i)&1 for i in range(8)]
  for x,v in enumerate(mask):
   if v:draw_cell(im,x,y,COL['white'] if bank==0 and 80<=y<=89 else COL['wall'])
 if bank==0:draw_sprite(im,72,80,build.PLAYER,COL['yellow'])
 if bank==2 and door!='open':draw_sprite(im,150,80,build.DOOR,COL[door])
 return im

def band(bank,phase):
 im=Image.new('RGB',(160,192),COL['bg'])
 for y in range(192):
  draw_cell(im,0,y,COL['wall']);draw_cell(im,39,y,COL['wall'])
 tabs,md=build.band_tables(bank)
 for yy in range(11):
  y=80+yy;k=0x40+phase*0x10+yy
  pf=[tabs[i][k] for i in range(6)]
  cols=[]
  for side in range(2):
   a,b,c=pf[3*side:3*side+3]
   cols.extend((a>>(4+i))&1 for i in range(4))
   cols.extend((b>>(7-i))&1 for i in range(8))
   cols.extend((c>>i)&1 for i in range(8))
  for x,v in enumerate(cols):
   if v:draw_cell(im,x,y,COL['white'])
 draw_sprite(im,72,80,build.PLAYER,COL['yellow'])
 if phase in (0,3):
  key=build.K09 if bank==1 and phase==3 else build.K11
  draw_sprite(im,105,80,key,COL['gold'])
 return im

for bank,phase,name in [
 (0,None,'R1_schematic.png'),(1,0,'R2_key_visible_K11_schematic.png'),
 (1,1,'R2_key_covered_schematic.png'),(1,3,'R2_key_K09_schematic.png'),
 (2,'brown','R3_locked_brown_schematic.png'),
 (2,'orange','R3_locked_orange_schematic.png'),(2,'open','R3_unlocked_schematic.png'),
 (3,0,'R4_phase0_schematic.png'),(3,1,'R4_phase1_schematic.png'),
 (3,2,'R4_phase2_schematic.png'),(3,3,'R4_phase3_schematic.png')]:
 im=full(bank,phase if isinstance(phase,str) else 'orange') if bank in (0,2) else band(bank,phase)
 label(im,name,O/name)
print('Wrote',len(list(O.glob('*schematic.png'))),'schematic images (not Stella)')
