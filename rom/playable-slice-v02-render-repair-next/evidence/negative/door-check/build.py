"""Build the isolated A_OPEN_01 prototype as a standard 16 KiB F6 cartridge."""
import argparse
from collections import deque
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SPAWNS=((79,20),(90,40),(71,62),(111,86),(95,111),(70,137),(101,153))


def emit(name,values):
    return name+":\n"+"\n".join(" byte "+",".join(str(a) for a in values[i:i+16]) for i in range(0,len(values),16))+"\n"


def generate():
    data=json.loads((ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())
    grid=next(m["grid"] for m in data["maps"] if m["id"]=="A_OPEN_01")
    assert len(grid)==22 and all(len(r)==40 for r in grid)
    assert all(r.replace("D","#")==r.replace("D","#")[::-1] for r in grid)
    bits=[[c!="." for c in row] for row in grid]
    def clear(x,y):
        return (0<=x<=152 and 0<=y<=167 and
                not any(bits[y0//8][x0//4] for y0 in (y,y+8) for x0 in (x,x+4,x+7)))
    reached={(12,82)}
    pending=deque(reached)
    while pending:
        x,y=pending.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if (nx,ny) not in reached and clear(nx,ny):
                reached.add((nx,ny))
                pending.append((nx,ny))
    assert all(spawn in reached for spawn in SPAWNS)
    assert all(abs(ax-bx)>=8 or abs(ay-by)>=9 for i,(ax,ay) in enumerate(SPAWNS)
               for bx,by in SPAWNS[i+1:])
    seed=1
    seen=set()
    for _ in range(255):
        assert seed and seed not in seen
        seen.add(seed)
        seed=(seed>>1)^(0xb8 if seed&1 else 0)
    assert seed==1 and all(sum(v%5==k for v in seen)==51 for k in range(5))
    pack=lambda cells,order: sum(1<<b for b,wall in zip(order,cells) if wall)
    video=[]
    for i,(lo,hi,order) in enumerate(((0,4,range(4,8)),(4,12,range(7,-1,-1)),(12,20,range(8)))):
        padding=(" include \"key_bridge.inc\"\n ds PFData0+80-*,0\n" if i==0
                 else " include \"key_bridge_append.inc\"\n include \"key_assist_select.inc\"\n ds PFData1+80-*,0\n" if i==1
                 else " include \"assist_window.inc\"\n include \"key_assist_install.inc\"\n ds PFData2+80-*,0\n")
        data=emit(f"MapColumn{i}",[pack(bits[y//8][lo:hi],order) for y in range(176)]) if i else (
            "MapColumn0:\n byte 240\n include \"prepare_key_assist.inc\"\n include \"door_cutout_probe.inc\"\n")
        video.extend((" ALIGN 256\n",f"PFData{i}:\n",padding,data))
    # Hold the PF registers across identical tiles. Keep the two P1 setup
    # lines and the preceding dispatcher clear of actual PF state changes.
    transitions={y for y in range(8,176,8) if grid[y//8].replace("D","#")!=grid[y//8-1].replace("D","#")}
    protected=transitions | {104}
    split_rows={69,129,136,156}
    recommended=[]
    for y in range(176):
        candidate=y
        while any(candidate+offset in protected for offset in (-1,0,1)):
            candidate-=1
        recommended.append(candidate)
    (HERE/"schedule.inc").write_text(" ALIGN 256\n"+emit("AllowedSetup",recommended))
    video.extend((" ALIGN 256\nRoomFlags:\n include \"key_assist_raster.inc\"\n ds RoomFlags+80-*,0\n",
                  emit("MapFlags",[131 if y in (86,87,88) else 133 if y in (89,90,91) else 135 if y==92 else 129 if y==104 or y in split_rows
                                   else 128 if 72<=y<104
                                   else pack(bits[y//8][:4],range(4,8))>>1 if y in transitions else 0 for y in range(176)])))
    masks=json.loads((ROOT/"design/NPC_REFERENCE_8x9_masks.json").read_text())["sprites"]
    video.append(" ds 175,0\n")
    for i,key in enumerate(("large_male","large_female","small_male","small_female")):
        video.extend((emit(f"Mask{i}",[int(b,2) for b in masks[key]])," ds 175,0\n"))
    (HERE/"video.inc").write_text("".join(video))
    logic=(emit("Collision",[pack(row[j:j+8],range(8)) for row in bits for j in range(0,40,8)]),
           emit("RowOffset",[y//8*5 for y in range(176)]),
           emit("ColumnByte",[x//32 for x in range(160)]),
           emit("ColumnMask",[1<<(x//4%8) for x in range(160)]),
           emit("SpawnX",[x for x,_ in SPAWNS]), emit("SpawnY",[y for _,y in SPAWNS]),
           emit("SpawnDir",[i%4 for i in range(len(SPAWNS))]))
    (HERE/"collision.inc").write_text("".join(logic))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--dasm",default="/workspace/.g5ar-env01/bin/dasm")
    a=parser.parse_args()
    generate()
    banks=[]
    for bank in range(2):
        name=("video","logic")[bank]
        subprocess.run([a.dasm,"game.asm",f"-DLOGIC={bank}","-f3",f"-o{name}.bank",
                        f"-s{name}.sym",f"-l{name}.lst"],cwd=HERE,check=True)
        data=(HERE/f"{name}.bank").read_bytes()
        assert len(data)==4096
        banks.append(data)
    (HERE/"let-me-out-v02-render-repair-next.bin").write_bytes(banks[0]+banks[1]+banks[0]*2)



if __name__=="__main__":
    main()
