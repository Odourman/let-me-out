"""Deterministic self-contained MOS 6502 assembler, v0.18a (subset only).
Supports ORG, BYTE, WORD, labels, constants, and opcodes used by diagnostic.
Does not silently replace DASM/Stella validation.
"""
import re
from pathlib import Path

OP={
'ADC':{'imm':0x69},'AND':{'imm':0x29},'BEQ':{'rel':0xF0},'BNE':{'rel':0xD0},
'BCC':{'rel':0x90},'BCS':{'rel':0xB0},'CLC':{'imp':0x18},'CLD':{'imp':0xD8},
'CMP':{'imm':0xC9,'zp':0xC5},'CPY':{'imm':0xC0},'DEX':{'imp':0xCA},
'INC':{'zp':0xE6},'INX':{'imp':0xE8},'INY':{'imp':0xC8},'JMP':{'abs':0x4C},
'LDA':{'imm':0xA9,'zp':0xA5,'abs':0xAD,'absy':0xB9},
'LDX':{'imm':0xA2},'LDY':{'imm':0xA0,'zp':0xA4},'LSR':{'acc':0x4A},
'NOP':{'imp':0xEA},'ORA':{'imm':0x09},'RTS':{'imp':0x60},
'SEI':{'imp':0x78},'STA':{'zp':0x85,'abs':0x8D,'zpx':0x95},'TXA':{'imp':0x8A},
'TXS':{'imp':0x9A},'TYA':{'imp':0x98},
}
BRANCH={'BEQ','BNE','BCC','BCS'}

def resolve(expr,symbols):
    expr=expr.strip()
    if expr.startswith('#'):expr=expr[1:]
    # only symbol [+/- integer] and hexadecimal/decimal integers, no Python eval
    m=re.fullmatch(r'([A-Za-z_][\w]*|\$[0-9a-fA-F]+|[0-9]+)(?:\s*([+-])\s*(\$[0-9a-fA-F]+|[0-9]+))?',expr)
    if not m:raise ValueError(f'Bad expression {expr!r}')
    def atom(t):
        if t.startswith('$'):return int(t[1:],16)
        if t[0].isdigit():return int(t)
        if t not in symbols:raise KeyError(t)
        return symbols[t]
    v=atom(m[1]);return v+(1 if m[2]=='+' else -1)*atom(m[3]) if m[2] else v

def assemble(source):
    lines=[];symbols={};pc=0;occupied={}
    for line_no,line in enumerate(source.splitlines(),1):
        s=line.split(';',1)[0].strip()
        if not s:continue
        if ':' in s:
            label, s=s.split(':',1);label=label.strip();
            if label in symbols:raise ValueError(f'duplicate {label}')
            symbols[label]=pc;s=s.strip()
            if not s:continue
        if ' = ' in s:
            k,e=s.split(' = ',1)
            symbols[k.strip()]=resolve(e,symbols);continue
        parts=s.split(None,1);op=parts[0].upper();arg=parts[1].strip() if len(parts)>1 else ''
        if op=='ORG':pc=resolve(arg,symbols);continue
        if op in ('BYTE','WORD'):
            vals=arg.split(',');n=len(vals)*(1 if op=='BYTE' else 2)
            lines.append((pc,line_no,op,arg,n));pc+=n;continue
        if op not in OP:raise ValueError(f'{line_no}: unsupported op {op}')
        if op in BRANCH: mode='rel'
        elif not arg:mode='imp'
        elif arg.upper()=='A':mode='acc'
        elif arg.startswith('#'):mode='imm'
        elif arg.endswith(',Y'):mode='absy'
        elif arg.endswith(',X') and arg.startswith('$') and len(arg)==5:mode='zpx'
        elif arg.startswith('$') and len(arg)==3:mode='zp'
        elif arg in symbols and symbols[arg]<256:mode='zp'
        else:mode='abs'
        if mode not in OP[op]:raise ValueError(f'{line_no}: unsupported {op} {mode} / {arg}')
        n={'imp':1,'acc':1,'imm':2,'zp':2,'zpx':2,'rel':2,'abs':3,'absy':3}[mode]
        lines.append((pc,line_no,op,(mode,arg),n));pc+=n
    for addr,lineno,op,arg,n in lines:
        def put(at,v):
            if at<0xF000 or at>0xFFFF:raise ValueError(f'{lineno}: out of 4K bank {at:04X}')
            if at in occupied:raise ValueError(f'{lineno}: collision {at:04X}')
            occupied[at]=v&255
        if op in ('BYTE','WORD'):
            for i,ex in enumerate(arg.split(',')):
                v=resolve(ex,symbols)
                if op=='BYTE':
                    if not 0<=v<=255:raise ValueError(f'byte out of range {v}')
                    put(addr+i,v)
                else:
                    put(addr+2*i,v);put(addr+2*i+1,v>>8)
            continue
        mode,operand=arg;put(addr,OP[op][mode])
        if n>1:
            value=resolve(operand[:-2] if mode in ('absy','zpx') else operand,symbols)
            if mode=='rel':
                d=value-(addr+2)
                if not -128<=d<=127:raise ValueError(f'{lineno}: branch range {d}')
                value=d&255
            put(addr+1,value)
            if n==3:put(addr+2,value>>8)
    data=bytes(occupied.get(x,0xFF) for x in range(0xF000,0x10000))
    return data,symbols,lines

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);d,s,_=assemble(p.read_text())
    target=Path(sys.argv[2]);target.write_bytes(d)
    print(f'{p.name}: {len(d)} bytes / symbols={len(s)} -> {target}')
