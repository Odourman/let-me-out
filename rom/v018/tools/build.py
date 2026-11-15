"""Let Me Out! NTSC v0.18 experiment: source generator + deterministic 6502 build.
All bitmaps are original diagnostic masks, not approved final game art.
Usage: python3 tools/build.py
"""
from pathlib import Path
import sys, hashlib, csv, json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from as6502 import assemble
OUT=ROOT/'dist';SRC=ROOT/'src'

C02='''########################################
#......................................#
#......................................#
#......................................#
#...#########..............#########...#
#...#########..............#########...#
#...##............................##...#
#...##............................##...#
#..........#######....#######..........#
#.......##....................##.......D
#......................................D
#......................................D
#.......##....................##.......D
#..........#######....#######..........#
#...##............................##...#
#...##............................##...#
#...#########..............#########...#
#...#########..............#########...#
#......................................#
#......................................#
#......................................#
########################################'''.splitlines()
assert len(C02)==22 and all(len(row)==40 for row in C02)
assert all(row[0]=='#' for row in C02)
assert all(C02[y][39]=='D' for y in range(9,13))

# 4x9 PLAYFIELD-cell masks: PF resolution is 4 colour clocks per cell.
# Preserves male/female + tall/small variation; this is deliberately a
# coarse 16-colour-clock worst-case diagnostic, not approved final sprite art.
SIL={
 'large_man':['.##.','####','.##.','.##.','.##.','.##.','.#.#','.#.#','.#.#'],
 'large_woman':['.##.','####','.##.','####','####','####','.#.#','.#.#','.#.#'],
 'small_man':['....','.##.','####','.##.','####','.#.#','.#.#','....','....'],
 'small_woman':['....','.##.','####','####','####','.#.#','.#.#','....','....'],
}
assert all(len(p)==9 and all(len(r)==4 for r in p) for p in SIL.values())
PLAYER=['..##....','.####...','######..','..###...','.#####..','..###...','..#.#...','.#..#...','##..##..']
K11=['..####..','.######.','###..###','###..###','.######.','...##...','...###..','...##...','...###..','...##...','....#...']
K09=['..####..','.######.','###..###','.######.','...##...','...###..','...##...','...###..','...##...']
# R3 orange door uses an 8-pixel hardware P1 with transparent (black)
# pixels near centre for keyhole, pending real display verification.
DOOR=['..####..']*32
for i in range(12,20):DOOR[i]='.##..##.' if i<16 else '.###.##.'

ROBOT_CLASSES=['large_man','large_woman','large_man','large_woman','small_man','small_woman']
ROBOT_CENTERS=[4,10,16,22,28,34]
SCREEN_W=40;VISIBLE=192;Y0=80

def blank():return [[False]*40 for _ in range(VISIBLE)]
def room_border(m):
 for row in m:
  row[0]=True;row[39]=True

def put_robot(m,center,name,y0=Y0):
 for j,s in enumerate(SIL[name]):
  for i,v in enumerate(s):
   x=center+i-2;y=y0+j
   if v=='#' and 0<=x<40 and 0<=y<VISIBLE:m[y][x]=True

def put_shot(m,x,y=84):
 for dy in range(3):
  if 0<=y+dy<VISIBLE and 0<=x<40:m[y+dy][x]=True

def pf(pixels):
 assert len(pixels)==40
 left=pixels[:20];right=pixels[20:]
 def encode(a):
  return [sum(int(a[i])<<(4+i) for i in range(4)),
    sum(int(a[4+i])<<(7-i) for i in range(8)),
    sum(int(a[12+i])<<i for i in range(8))]
 return encode(left)+encode(right)

def sprite_table(pattern,y0=Y0):
 vals=[0]*VISIBLE
 for n,row in enumerate(pattern):
  if 0<=y0+n<VISIBLE:vals[y0+n]=int(row.replace('#','1').replace('.','0'),2)
 return vals

def full_tables(bank):
 m=blank();room_border(m)
 g0=sprite_table(PLAYER);g1=[0]*VISIBLE
 if bank==0:
  for x,t in zip(ROBOT_CENTERS,ROBOT_CLASSES):put_robot(m,x,t)
  put_shot(m,37)
 elif bank==2:
  for j,line in enumerate(C02):
   for x,v in enumerate(line):
    for dy in range(8):m[8+j*8+dy][x]=v=='#' # D is open PF; P1 locks it
  g0=[0]*VISIBLE;g1=sprite_table(DOOR,80)
 return [list(v) for v in zip(*[pf(row) for row in m])]+[g0,g1]

def band_tables(bank):
 # Indexed by Y = 0x40 + phase*0x10 + line (0..10)
 # Four 11-scanline phases, no high-level per-pixel software rendering.
 arrays=[[0]*256 for _ in range(8)]
 metadata=[]
 for phase in range(4):
  # R2: 5 androids, third/later mover travels across the fixed key x.
  # R4: 6 androids; 4 deterministic horizontal/vertical patterns.
  if bank==1:
   centers=[4,10,16,22,[24,27,27,30][phase]]
   classes=ROBOT_CLASSES[:5]
   ys=[0,0,0,0,[0,0,0,1][phase]]
   covered=phase in (1,2)
  else:
   centers=[4+phase%2,10-phase%2,16,22+(phase%2),[24,27,27,30][phase],34-phase%2]
   classes=ROBOT_CLASSES
   ys=[0,phase%2,0,1-phase%2,0,phase%2]
   covered=phase in (1,2)
  m=[[False]*40 for _ in range(11)]
  for row in m: row[0]=row[39]=True
  for x,t,offset in zip(centers,classes,ys):
   for j,s in enumerate(SIL[t]):
    y=j+offset
    if 0<=y<11:
     for i,c in enumerate(s):
      k=x+i-2
      if c=='#' and 0<=k<40:m[y][k]=True
  shotx=[37,35,33,36][phase]
  for offset in range(3):m[4+offset][shotx]=True
  p0=PLAYER+['........','........']
  key=(K11 if phase==0 or bank==3 else (K09+['........','........'])) if phase in (0,3) else ['........']*11
  for j in range(11):
   yy=0x40+phase*0x10+j
   vals=pf(m[j])+[int(p0[j].replace('#','1').replace('.','0'),2),int(key[j].replace('#','1').replace('.','0'),2)]
   for k,v in enumerate(vals):arrays[k][yy]=v
  metadata.append({'phase':phase,'frame_lo_range':[phase*64,phase*64+63],
      'android_count':len(classes),'centers':centers,'y_offsets':ys,
      'key_x_cell':27,'key_y_scanline':80,'covered':covered,'shot_x_cell':shotx})
 return arrays,metadata

ASM=r'''
; Let Me Out! v0.18 ROM DEVELOPMENT diagnostic, independently written 6502.
; 16K F6: four identical 6502 kernels with distinct data banks.
; Main starts in last F6 bank, switches banks by write to $FFF6..$FFF9.
; Timing: 3 VSYNC + 37 VBLANK + 192 visible + 30 overscan = 262.
; The playfield is updated asymmetrically: left PF0..2 then right PF0..2.
VSYNC = $00
VBLANK = $01
WSYNC = $02
NUSIZ0 = $04
NUSIZ1 = $05
COLUP0 = $06
COLUP1 = $07
COLUPF = $08
COLUBK = $09
CTRLPF = $0A
PF0 = $0D
PF1 = $0E
PF2 = $0F
RESP0 = $10
RESP1 = $11
GRP0 = $1B
GRP1 = $1C
SCENE = $80
FRAMELO = $81
FRAMEHI = $82
PHASE = $83
KEY_X = $84
KEY_Y = $85
KEY_ALIVE = $86
DOORCOLOR = $87
ORG $F000
Reset:
 SEI
 CLD
 LDX #$FF
 TXS
 LDX #$00
 TXA
ClearPage:
 STA $00,X
 INX
 BNE ClearPage
 LDA #$00
 STA SCENE
 LDA #$FE
 STA FRAMELO
 LDA #$FF
 STA FRAMEHI
 LDA #27
 STA KEY_X
 LDA #80
 STA KEY_Y
 LDA #1
 STA KEY_ALIVE
 LDA #$02
 STA VBLANK
Frame:
 LDA #$02
 STA VSYNC
 STA WSYNC
 STA WSYNC
 STA WSYNC
 LDA #$00
 STA VSYNC
 LDA #$02
 STA VBLANK
 ; line 3: 600-frame deterministic scene advance
 INC FRAMELO
 BNE CountReady
 INC FRAMEHI
CountReady:
 LDA FRAMEHI
 CMP #2
 BNE KeepScene
 LDA FRAMELO
 CMP #88
 BNE KeepScene
 LDA #0
 STA FRAMELO
 STA FRAMEHI
 INC SCENE
 LDA SCENE
 AND #3
 STA SCENE
KeepScene:
 STA WSYNC
 ; line 4: F6 bank switch; all bank kernel bytes are identical
 LDA SCENE
 BEQ UseBank0
 CMP #1
 BEQ UseBank1
 CMP #2
 BEQ UseBank2
 STA $FFF9
 JMP BankSelected
UseBank0:
 STA $FFF6
 JMP BankSelected
UseBank1:
 STA $FFF7
 JMP BankSelected
UseBank2:
 STA $FFF8
BankSelected:
 STA WSYNC
 ; line 5: phase index 0x40/0x50/0x60/0x70
 LDA FRAMELO
 AND #$C0
 LSR A
 LSR A
 CLC
 ADC #$40
 STA PHASE
 ; set P1 color ahead of time, so the VBLANK line 8 never overflows
 LDA #$2C
 STA DOORCOLOR
 LDA SCENE
 CMP #2
 BNE DoorColorChosen
 LDA FRAMELO
 CMP #85
 BCC ColorBrown
 CMP #170
 BCC ColorOrange
 LDA #0
 STA DOORCOLOR
 JMP DoorColorChosen
ColorBrown:
 LDA #$64
 STA DOORCOLOR
 JMP DoorColorChosen
ColorOrange:
 LDA #$3C
 STA DOORCOLOR
DoorColorChosen:
 LDX #9
 STA WSYNC
 ; line 6: player P0 coarse horizontal positioning
P0Delay:
 DEX
 BNE P0Delay
 STA RESP0
 LDA SCENE
 CMP #2
 BEQ PositionDoor
 LDX #11
 JMP PositionP1
PositionDoor:
 LDX #14
PositionP1:
 STA WSYNC
 ; line 7: P1 horizontal positioning. 14*5-1+STA+WSYNC <=76 cycles
P1Delay:
 DEX
 BNE P1Delay
 STA RESP1
 STA WSYNC
 ; line 8: scene colors and independently programmable right half
 LDA #$00
 STA COLUBK
 STA PF1
 STA PF2
 STA GRP0
 STA GRP1
 LDA #$10
 STA PF0
 ; CTRLPF reflect=0: the right half is independently loaded after the midpoint.
 ; Reflect=1 would reverse the byte order of the intended right-half map.
 LDA #0
 STA CTRLPF
 LDA #$1E
 STA COLUP0
 LDA #$0E
 STA COLUPF
 LDA DOORCOLOR
 STA COLUP1
 STA WSYNC
 ; line 9 + thirty WSYNC lines = line 39, still VBLANK
 LDX #30
BlankFill:
 STA WSYNC
 DEX
 BNE BlankFill
 LDY #64
 LDA #0
 STA GRP0
 STA GRP1
 ; release VBLANK only near end of line 39 (in horizontal blank)
'''
ASM+='\n'.join(' NOP' for _ in range(24))+'\n'
ASM+=r'''
 STA VBLANK
 STA WSYNC
 ; line 40: first visible scanline is border, remaining 191 drawn below.
 LDA SCENE
 CMP #1
 BEQ BandRenderer
 CMP #3
 BEQ BandRenderer
 LDY #65
 JMP FullLoop

; Bank 1 and 3 stress renderer; 80 top + 11 stress + 101 bottom lines.
BandRenderer:
 LDX #79
BandTop:
 STA WSYNC
 DEX
 BNE BandTop
 LDA #0
 STA CTRLPF
 LDA #$0E
 STA COLUPF
 LDY PHASE
 LDA P0DATA,Y
 STA GRP0
 LDA P1DATA,Y
 STA GRP1
 LDX #11
BandLoop:
 STA WSYNC
 LDA LEFT0,Y
 STA PF0
 LDA LEFT1,Y
 STA PF1
 LDA LEFT2,Y
 STA PF2
'''
ASM+='\n'.join(' NOP' for _ in range(4))+'\n'
ASM+=r'''
 LDA RIGHT0,Y
 STA PF0
 LDA RIGHT1,Y
 STA PF1
 LDA RIGHT2,Y
 STA PF2
 INY
 LDA P0DATA,Y
 STA GRP0
 LDA P1DATA,Y
 STA GRP1
 DEX
 BNE BandLoop
 ; line 131: first lower half line
 STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
 STA PF1
 STA PF2
 LDA #$10
 STA PF0
 LDA #1
 STA CTRLPF
 LDA #$64
 STA COLUPF
 LDX #100
BandBottom:
 STA WSYNC
 DEX
 BNE BandBottom
 JMP EndVisible

; Banks 0/2: one inactive top line + 191 rendered scanlines.
FullLoop:
 STA WSYNC
 LDA #0
 STA CTRLPF
 LDA LEFT0,Y
 STA PF0
 LDA LEFT1,Y
 STA PF1
 LDA LEFT2,Y
 STA PF2
'''
ASM+='\n'.join(' NOP' for _ in range(4))+'\n'
ASM+=r'''
 LDA RIGHT0,Y
 STA PF0
 LDA RIGHT1,Y
 STA PF1
 LDA RIGHT2,Y
 STA PF2
 INY
 LDA P0DATA,Y
 STA GRP0
 LDA P1DATA,Y
 STA GRP1
 TYA
 BNE FullLoop
EndVisible:
 STA WSYNC
 LDA #2
 STA VBLANK
 LDX #29
Overscan:
 STA WSYNC
 DEX
 BNE Overscan
 STA WSYNC
 JMP Frame
; Tables begin at fixed $F400 in every bank. Unused bytes read as $FF.
ORG $F400
'''

# IMPORTANT: FullLoop CTRLPF must be moved outside the 76-cycle scanline budget;
# per-scanline 2+3 extra cycles would cause right PF1 late. Inbank scene setup
# has CTRLPF=0 for bank0/2. R2/4 set 1 before band (BandRenderer sets 0).
ASM=ASM.replace('FullLoop:\n STA WSYNC\n LDA #0\n STA CTRLPF\n','FullLoop:\n STA WSYNC\n')
# Ensure full render bank0/2 uses no PF reflection, by adjusting scene setup.
ASM=ASM.replace(' LDA #$01\n STA CTRLPF\n LDA #$1E', ''' LDA SCENE
 CMP #1
 BEQ SetReflect
 CMP #3
 BEQ SetReflect
 LDA #0
 JMP ReflectSet
SetReflect:
 LDA #1
ReflectSet:
 STA CTRLPF
 LDA #$1E''')

# line8 route can exceed a raster line in worst R3. this gets measured in
# the independent interpreter and no timing claim is made until then.

def pack(bank):
 if bank in (0,2):return full_tables(bank),[]
 return band_tables(bank)

def lines_byte(values):
 return '\n'.join(' BYTE '+','.join('$%02X'%v for v in values[i:i+16]) for i in range(0,len(values),16))+'\n'

def render_bank_asm(bank):
 tables,metadata=pack(bank)
 sections=['LEFT0','LEFT1','LEFT2','RIGHT0','RIGHT1','RIGHT2','P0DATA','P1DATA']
 # first 64 positions unused for full table: stable 256 byte arrays permit Y rollover
 blocks=[]
 for name,values in zip(sections,tables):
  if len(values)==VISIBLE: values=[0]*64+values
  assert len(values)==256
  blocks.append(f'{name}:\n'+lines_byte(values))
 # tables will be exactly 2048 bytes in $F400-$FBFF
 return ASM+'\n'.join(blocks)+'ORG $FFFC\n WORD Reset,Reset\n',metadata

def main():
 OUT.mkdir(exist_ok=True);SRC.mkdir(exist_ok=True)
 parts=[];labels=[];md={}
 for b in range(4):
  source,metadata=render_bank_asm(b)
  (SRC/f'bank{b}.asm').write_text(source,encoding='utf-8')
  blob,sym,lines=assemble(source)
  parts.append(blob);labels.append(sym);md[f'R{b+1}']=metadata
  print('bank',b,'code ends near:',hex(max(pc+n for pc,_,op,arg,n in lines if pc<0xF400)),'len',len(blob))
 # F6 hotspots require kernel addresses identical across all banks
 for addr in range(0x0000,0x0400):
  if len({p[addr] for p in parts})!=1:
   raise AssertionError(f'bank kernel not identical at $F{addr:03X}')
 assert all(p[0xFFC:0x1000]==parts[0][0xFFC:0x1000] for p in parts)
 rom=b''.join(parts)
 assert len(rom)==16384
 (OUT/'LetMeOut_Diagnostic_NTSC_F6_v018.bin').write_bytes(rom)
 (OUT/'symbols.json').write_text(json.dumps(labels[0],indent=2,sort_keys=True)+'\n')
 (OUT/'phases.json').write_text(json.dumps(md,indent=2)+'\n')
 (OUT/'rom_sha256.txt').write_text(hashlib.sha256(rom).hexdigest()+'  LetMeOut_Diagnostic_NTSC_F6_v018.bin\n')
 print('ROM SHA256',hashlib.sha256(rom).hexdigest())

if __name__=='__main__':main()
