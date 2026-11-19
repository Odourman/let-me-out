"""Real controller-driven cases. POKEs only establish explicitly labelled fixtures."""
import argparse
import re
from pathlib import Path
from time import monotonic

from capture import BIN,Session,record
from replay import frames,peek,FRAME
from pixels import colored,expected_mask,npc_pixels,picture
from audit import GOLD,KEY


def setup(s,x,y,npc_x,npc_y,score):
    values={0x80:x,0x81:y,0xaa:score,0xab:0,0xae:0}
    values.update({0x91+i:v for i,v in enumerate(npc_x)})
    values.update({0x96+i:v for i,v in enumerate(npc_y)})
    for address,v in values.items():
        s.command(f"POKE 0x{address:04x} 0x{v:02x}")
    assert peek(s,values)==list(values.values())
    record("setup",poke=values)


def inp(s,*controls):
    for control in controls:
        s.command(f"STICK LEFT {control}")


def snap(s,n,label,folder):
    result,totals=frames(s,n,label,folder)
    assert set(totals)=={262},(label,totals)
    return result


def score(s):
    a,b=peek(s,[0xaa,0xab])
    return a+256*b


def monitor_key(s,out):
    for index in range(75):
        s.command("STEP FRAME")
        total=int(re.search(FRAME,s.command("TV FRAME"))[3])
        assert total==262
        flag,x,y,queued=peek(s,[0xaf,0xb0,0xb1,0xec])
        target=out/(f"key-lifetime-{index:02}.png" if index in (0,38,39,64)
                    else "key-lifetime.png")
        target.unlink(missing_ok=True)
        s.command(f"SCREENSHOT {target}")
        gold=colored(picture(target),GOLD)
        expected=expected_mask(KEY,x,y+15)
        record("key_lifetime",index=index,scanlines=total,state=flag,x=x,y=y,
               queued=bool(queued&32),key_pixels=len(gold&expected),extra=len(gold-expected),
               npcs=peek(s,[*range(0x91,0x9b),*range(0xa0,0xa5)]))
        if flag==2:
            return
    raise AssertionError("key not collected on the cold-start route")


def run(s, case, out, key_lifetime=False, pixel_stride=0):
    for _ in range(24):
        s.command("STEP FRAME")
    if case=="patrol":
        a=peek(s,range(0x91,0x9b))
        snap(s,45,"peaceful-patrol",out)
        b=peek(s,range(0x91,0x9b))
        assert all(a[i]!=b[i] or a[i+5]!=b[i+5] for i in range(5))
        assert peek(s,[0x88,0xac])==[0,3]
        return
    if case=="controls":
        directions=(("RIGHT",),("RIGHT","UP"),("UP",),("LEFT","UP"),
                    ("LEFT",),("LEFT","DOWN"),("DOWN",),("RIGHT","DOWN"))
        targets=((76,82),(76,81),(75,81),(74,81),(74,82),(74,83),(75,83),(76,83))
        for i,(buttons,end) in enumerate(zip(directions,targets)):
            setup(s,75,82,(91,92,93,94,95),(22,42,102,132,152),0)
            inp(s,"NOLEFT","NORIGHT","NOUP","NODOWN",*buttons)
            assert snap(s,1,f"direction-{i}",out)[:2]==list(end)
        inp(s,"NODOWN","FIRE")
        snap(s,4,"shot-east",out)
        inp(s,"NOFIRE")
        snap(s,1,"rearm-while-active",out)
        inp(s,"NORIGHT","DOWN","FIRE")
        snap(s,1,"second-press-blocked",out)
        assert peek(s,[0x84,0x87])==[1,8]
        return
    if case=="npc-obstacles":
        setup(s,12,82,(24,95,101,115,75),(40,58,100,118,152),0)
        s.command("POKE 0x00a6 0x00")
        s.command("POKE 0x009b 0x00")
        snap(s,2,"npc-wall-turn",out)
        assert peek(s,[0x91,0x96])==[24,41]
        setup(s,12,82,(64,72,101,115,75),(80,80,100,118,152),0)
        s.command("POKE 0x00a6 0x00")
        s.command("POKE 0x009b 0x00")
        snap(s,2,"npc-neighbor-turn",out)
        assert peek(s,[0x91,0x96])==[64,81]
        return
    if case=="unseeded":
        # Cold NTSC Gopher start with the observed deterministic seed.
        # This test uses the actual controller path from boot, without POKE.
        carrier=peek(s,[0xae])[0]
        assert carrier==4 and peek(s,[0x96+carrier])[0] in range(149,159)
        inp(s,"DOWN")
        snap(s,72,"unseeded-south-corridor",out)
        inp(s,"NODOWN","RIGHT","FIRE")
        snap(s,1,"unseeded-first-fire",out)
        for step in range(110):
            s.command("STEP FRAME")
            total=int(re.search(FRAME,s.command("TV FRAME"))[3])
            record("flight",n=step,scanlines=total)
            assert total==262
            if peek(s,[0xaf])[0]==1:
                break
        assert peek(s,[0xaf,0xac])==[1,3]
        snap(s,1,"unseeded-key-floor",out)
        inp(s,"NOFIRE","NORIGHT","DOWN")
        assert snap(s,5,"unseeded-south-alignment",out)[:2]==[12,159]
        inp(s,"NODOWN","RIGHT")
        if key_lifetime:
            before=peek(s,[0x80])[0]
            monitor_key(s,out)
            after=peek(s,[0x80])[0]
            east_frames=136-(after-before)
        else:
            east_frames=136
        assert snap(s,east_frames,"unseeded-east-corridor",out)[:2]==[148,159]
        assert peek(s,[0xaf,0xac])==[2,3] and score(s)==50
        inp(s,"NORIGHT","UP")
        assert snap(s,79,"unseeded-door-approach",out)[:2]==[148,80]
        inp(s,"NOUP","RIGHT")
        snap(s,1,"unseeded-door-unlock",out)
        assert peek(s,[0xb2,0xb3])==[1,0]
        snap(s,12,"unseeded-exit",out)
        assert peek(s,[0xb2,0xb3,0xac])==[1,1,3] and score(s)==210
        return
    if case=="soak":
        actions=(("RIGHT","NODOWN"),("NORIGHT","DOWN","FIRE"),("NOFIRE",),
                 ("NODOWN","LEFT"),("NOLEFT","UP"),("RIGHT","NOUP"))
        for i in range(600):
            if i%100==0:
                inp(s,*actions[i//100])
            if pixel_stride and (i+1)%pixel_stride==0:
                # The screenshot is the completed picture, before the subsequent
                # overscan update reflected in RAM at the STEP FRAME boundary.
                inputs=peek(s,[*range(0x91,0x9b),*range(0xa0,0xa5)])
            s.command("STEP FRAME")
            total=int(re.search(FRAME,s.command("TV FRAME"))[3])
            stamp=s.command("TV").decode().strip()
            omitted,eligible,rendered,assist,px,py=peek(s,[0xdc,0xde,0xec,0xf5,0x80,0x81])
            record("soak",n=i,scanlines=total,tv=stamp,omitted=omitted,eligible=eligible,rendered=rendered,assist=assist,player=[px,py])
            assert total==262
            if (pixel_stride and (i+1)%pixel_stride==0) or i%100==99:
                target=out/f"frame-{i+1:03d}.png"
                s.command(f"SCREENSHOT {target}")
                if pixel_stride:
                    objects,extra=npc_pixels(target,inputs[:5],inputs[5:10],inputs[10:])
                    record("soak_pixels",n=i,objects=objects,unattributed_white=extra)
        return
    if case=="door-held-open":
        setup(s,148,80,(80,122,94,92,72),(20,45,118,151,165),0)
        s.command("POKE 0x00af 0x02")  # establish collected-key fixture
        inp(s,"RIGHT")
        snap(s,1,"unlock-input",out)
        assert peek(s,[0xb2,0xb3])==[1,0]
        inp(s,"NORIGHT")
        assert snap(s,6,"open-before-passage",out)[:2]==[148,80]
        assert peek(s,[0xb2,0xb3])==[1,0] and score(s)==0
        return
    if case=="door-locked":
        setup(s,148,80,(80,122,94,92,72),(20,45,70,118,151),0)
        inp(s,"RIGHT")
        assert snap(s,12,"door-without-key",out)[:2]==[148,80]
        assert peek(s,[0xaf,0xb2,0xb3])==[0,0,0] and score(s)==0
        return
    if case=="wall":
        setup(s,20,40,(80,122,94,92,72),(20,47,75,115,151),0)
        inp(s,"RIGHT")
        assert snap(s,12,"inside-wall-stop",out)[:2]==[24,40]
        inp(s,"FIRE")
        snap(s,15,"shot-stopped-at-wall",out)
        assert peek(s,[0x84,0x85])==[0,32]
        return
    if case in {"touch","priority"}:
        setup(s,62,60,(62,91,102,88,73),(60,22,112,136,153),10)
        if case=="touch":
            s.command("POKE 0x0088 0x01")
            snap(s,2,"hunting-contact",out)
            assert peek(s,[0xac])==[2]
            return
        inp(s,"RIGHT","FIRE")
        snap(s,2,"same-update-shot-wins",out)
        assert peek(s,[0xac,0xa0])==[3,7] and score(s)==0
        return
    setup(s,62,60,(80,91,102,88,73),(60,22,112,136,153),40)
    inp(s,"RIGHT","FIRE")
    snap(s,1,"shot-start",out)
    assert peek(s,[0x84,0x88])==[1,1]
    snap(s,13,"projectile",out)
    for i in range(10):
        s.command("STEP FRAME")
        if peek(s,[0xa0])[0]!=255:
            break
    assert 0<peek(s,[0xa0])[0]<255 and score(s)==10
    assert peek(s,[0xaf])==[0]
    snap(s,1,"android-death",out)
    snap(s,8,"key-on-floor",out)
    assert peek(s,[0xaf])==[1]
    inp(s,"NOFIRE")
    snap(s,20,"key-pickup",out)
    assert peek(s,[0xaf])==[2] and score(s)==60
    inp(s,"NORIGHT","DOWN")
    assert snap(s,20,"door-approach",out)[1]==80
    inp(s,"NODOWN","RIGHT")
    x=peek(s,[0x80])[0]
    snap(s,148-x+1,"door-unlocked",out)
    assert peek(s,[0xb2,0xb3])==[1,0] and score(s)==60
    snap(s,12,"actual-exit",out)
    assert peek(s,[0xb2,0xb3])==[1,1] and score(s)==220
    snap(s,5,"exit-bonus-once",out)
    assert score(s)==220


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("out",type=Path)
    p.add_argument("case",choices=("patrol","wall","touch","priority","key-door","soak","unseeded","controls","npc-obstacles","door-locked","door-held-open"))
    p.add_argument("--key-lifetime",action="store_true")
    p.add_argument("--pixel-probe",action="store_true")
    p.add_argument("--pixel-stride",type=int,default=0)
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(a.rom.resolve())],a.case) as s:
        s.receive(monotonic()+30)
        s.command("VERSION REVISION")
        s.command("CARTRIDGE MAPPER")
        run(s,a.case,a.out.resolve(),a.key_lifetime,a.pixel_stride or (10 if a.pixel_probe else 0))
        record("result",case=a.case,status="PASS")
