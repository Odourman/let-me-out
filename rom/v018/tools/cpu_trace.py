"""6502 instruction/cycle model for own engineering preflight, NOT Stella.
Only MOS 6502 instructions in as6502.py are implemented. 6502 documented
cycles, branch/page-cross penalties and WSYNC stalling are accounted for.
Actual TIA pixel output/timing must be checked independently in Stella.
"""
import sys,json,collections,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROM=(ROOT/'dist/LetMeOut_Diagnostic_NTSC_F6_v018.bin').read_bytes()
OP={
0x69:('ADC','#',2,2),0x29:('AND','#',2,2),
0xF0:('BEQ','rel',2,2),0xD0:('BNE','rel',2,2),0x90:('BCC','rel',2,2),0xB0:('BCS','rel',2,2),
0x18:('CLC','',1,2),0xD8:('CLD','',1,2),
0xC9:('CMP','#',2,2),0xC5:('CMP','zp',2,3),0xCA:('DEX','',1,2),0xE6:('INC','zp',2,5),
0xE8:('INX','',1,2),0xC8:('INY','',1,2),0x4C:('JMP','abs',3,3),
0xA9:('LDA','#',2,2),0xA5:('LDA','zp',2,3),0xAD:('LDA','abs',3,4),0xB9:('LDA','absy',3,4),
0xA2:('LDX','#',2,2),0xA0:('LDY','#',2,2),0xA4:('LDY','zp',2,3),
0x4A:('LSR','acc',1,2),0xEA:('NOP','',1,2),0x60:('RTS','',1,6),
0x78:('SEI','',1,2),0x85:('STA','zp',2,3),0x8D:('STA','abs',3,4),
0x95:('STA','zpx',2,4),0x8A:('TXA','',1,2),0x9A:('TXS','',1,2),0x98:('TYA','',1,2),
}
class CPU:
 def __init__(self):
  self.bank=3;self.ram=bytearray(128);self.tia=bytearray(64)
  self.a=self.x=self.y=0;self.sp=255;self.c=self.z=self.n=0
  self.cycles=0;self.pc=self.read(0xFFFC)|(self.read(0xFFFD)<<8)
  self.frames=[];self.writes=[];self.trace=[];self.ws=[];self.stepcount=0
  self.keep_log=False;self.maxwrites=20000;self.sample_frame_indices=set()
 def read(self,addr):
  addr&=0xffff
  if addr>=0xF000:return ROM[self.bank*4096+addr-0xF000]
  if 0x80<=addr<=0xFF:return self.ram[addr-0x80]
  return self.tia[addr&0x3F]
 def nz(self,v):
  self.n=int(bool(v&128));self.z=int((v&255)==0);return v&255
 def put(self,addr,v,pc,at):
  v&=255
  if 0xFFF6<=addr<=0xFFF9:self.bank=addr-0xFFF6;return
  if 0x80<=addr<=0xFF:self.ram[addr-0x80]=v;return
  adr=addr&0x3F
  prev=self.tia[adr];self.tia[adr]=v
  if adr==1 and not (v&2) and (prev&2) and self.frames:
   self.frames[-1].update({'visible_start':at,'scene_visible':int(self.ram[0]),'bank_visible':self.bank,
       'phase':int(self.ram[3]),'key_x':int(self.ram[4]),'key_y':int(self.ram[5]),'key_alive':int(self.ram[6])})
  if adr==0 and (v&2) and not (prev&2):
   self.frames.append({'cycle':at,'scene_on_start':int(self.ram[0]),'bank':self.bank,'pc':pc})
  if adr in (0,1,2,6,7,8,10,13,14,15,16,17,27,28):
   if len(self.writes)<self.maxwrites and (self.keep_log or (len(self.frames)-1) in self.sample_frame_indices):
    self.writes.append({'at':at,'scan':at//76,'cycle':at%76,'reg':adr,'value':v,
        'scene':int(self.ram[0]),'bank':self.bank,'pc':pc})
  if adr==2:
   self.ws.append(at)
   self.cycles=((self.cycles+75)//76)*76
 def step(self):
  pc=self.pc;op=self.read(pc)
  if op not in OP:raise RuntimeError(f'Unknown opcode {op:02X} at {pc:04X} bank{self.bank}, after {self.stepcount}')
  name,mode,size,base=OP[op]
  b1=self.read(pc+1) if size>1 else 0
  b2=self.read(pc+2) if size>2 else 0
  self.pc=(pc+size)&65535
  addr=None;v=None;extra=0
  if mode=='#':v=b1
  elif mode=='zp':addr=b1;v=self.read(addr)
  elif mode=='zpx':addr=(b1+self.x)&255;v=self.read(addr)
  elif mode=='abs':addr=b1+(b2<<8);v=self.read(addr)
  elif mode=='absy':
   ptr=b1+(b2<<8);addr=(ptr+self.y)&65535;v=self.read(addr)
   if (ptr&0xff00)!=(addr&0xff00):extra=1
  elif mode=='rel':v=b1-256 if b1>=128 else b1
  cyc=base
  if name in ('BEQ','BNE','BCC','BCS'):
   take=(name=='BEQ' and self.z==1) or (name=='BNE' and self.z==0) or (name=='BCC' and self.c==0) or (name=='BCS' and self.c==1)
   if take:
    target=(self.pc+v)&65535
    cyc+=1+(int((self.pc&0xff00)!=(target&0xff00)))
    self.pc=target
  elif name=='CLC':self.c=0
  elif name=='AND':self.a=self.nz(self.a&v)
  elif name=='ADC':
   n=self.a+v+self.c;self.c=int(n>255);self.a=self.nz(n)
  elif name=='CMP':
   dif=self.a-v;self.c=int(self.a>=v);self.nz(dif)
  elif name=='DEX':self.x=self.nz(self.x-1)
  elif name=='INX':self.x=self.nz(self.x+1)
  elif name=='INY':self.y=self.nz(self.y+1)
  elif name=='INC':self.put(addr,self.nz(v+1),pc,self.cycles+cyc)
  elif name=='JMP':self.pc=addr
  elif name=='LDA':self.a=self.nz(v);cyc+=extra
  elif name=='LDX':self.x=self.nz(v)
  elif name=='LDY':self.y=self.nz(v)
  elif name=='LSR':self.c=self.a&1;self.a=self.nz(self.a>>1)
  elif name=='STA':pass
  elif name=='TXA':self.a=self.nz(self.x)
  elif name=='TXS':self.sp=self.x
  elif name=='TYA':self.a=self.nz(self.y)
  elif name in ('SEI','CLD','NOP'):pass
  else:raise RuntimeError('Not implemented '+name)
  self.cycles+=cyc
  if name=='STA':self.put(addr,self.a,pc,self.cycles)
  self.stepcount+=1
  return name,pc

def run(frame_count=15):
 cpu=CPU()
 maxsteps=frame_count*12000
 while len(cpu.frames)<frame_count and cpu.stepcount<maxsteps:cpu.step()
 if len(cpu.frames)<frame_count:raise RuntimeError('did not complete frames')
 delta=[(cpu.frames[i+1]['cycle']-cpu.frames[i]['cycle'])/76 for i in range(len(cpu.frames)-1)]
 print('frames',len(cpu.frames),'steps',cpu.stepcount,'bank',cpu.bank)
 print('delta rounded',collections.Counter(round(x,3) for x in delta))
 print('first starts',cpu.frames[:10])
 print('wsync writes',len(cpu.ws),'first writes',cpu.writes[:25])
 return cpu
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 15)
