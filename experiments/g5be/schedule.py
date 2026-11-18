"""G5BE deterministic 6507 instruction packing. Store windows are empirical bounds."""
import json
from pathlib import Path

import z3

X = [127,19,73,100,46]
Y = [73,72,73,71,72]
ORDER = sorted(range(5), key=X.__getitem__)
CLOCK = [(X[i]+48)//3 for i in ORDER]
LIMIT = 15000


def search(family, packet=False, omitted=None, clocks=CLOCK):
    solver = z3.Solver()
    solver.set(timeout=LIMIT, random_seed=0)
    events, uses = {}, {}

    def instruction(name, cycles, earliest=2, latest=71, wide=False):
        start = z3.Int(name)
        if wide:
            cycles = cycles+z3.If(z3.Bool("absolute_"+name),1,0)
        events[name] = (start, cycles)
        solver.add(start>=2, start+cycles>=earliest, start+cycles<=latest)
        return start+cycles

    def load(name, cycles):
        done = instruction("load_"+name,cycles)
        reg = z3.Int("r_"+name)
        solver.add(reg>=0,reg<=1)
        uses[name] = (done,reg,[])
        return done

    def write(name, value, span):
        end = instruction(name,3,*span,wide=True)
        done,_,readers = uses[value]
        solver.add(done<=events[name][0])
        readers.append(end)
        return end

    def strobe(i):
        return instruction(f"resp{i}",3,clocks[i],clocks[i],wide=True)

    load("p0",4)
    p0 = write("grp0_p0","p0",(6,22))
    for i in range(5):
        if i!=omitted:
            load(f"m{i}", 2 if packet else 4)

    if family == "p1-shadow":
        preceding = None
        for i in range(5):
            strobe(i)
            # The first transfer may be the ordinary P0 drawing write.
            new = write(f"new{i}",f"m{i}",(3,64))
            old = p0 if i==0 else write(f"old{i}","p0",(clocks[i-1]+10,clocks[i]+6))
            solver.add(new<=old-3)
            if preceding is not None:
                solver.add(preceding<=new-3)
            preceding=old
    elif family=="p1-window":
        # Same physical P1 family with a targeted delayed SF/F window.
        load("on",2)
        load("off",2)
        on=write("vdel_on","on",(32,37))
        off=write("vdel_off","off",(50,55))
        for i in range(5):
            strobe(i)
        sf=write("sf_new","m1",(27,34))
        sf_old=write("sf_old","p0",(33,37))
        f=write("f_new","m2",(35,43))
        f_old=write("f_old","p0",(42,46))
        solver.add(sf<=events["sf_old"][0],sf_old<=events["f_new"][0],
                   f<=events["f_old"][0],on<=sf_old,f_old<=off)
        for i,span in ((0,(14,27)),(3,(50,55)),(4,(60,64))):
            done=write(f"grp1_{i}",f"m{i}",span)
            if i==3:
                solver.add(off<=events["grp1_3"][0])
    else:
        load("off",2)
        load("white",2)
        load("yellow",2)
        off=write("enam0_off","off",(25,43))
        white=write("colup0_white","white",(32,45))
        f=write("grp0_f","m2",(32,46))
        yellow=write("colup0_yellow","yellow",(51,68))
        on=write("enam0_on","yellow",(51,71))
        solver.add(p0<=f-3, off<=white-3, white<=yellow-3, yellow<=on-3)
        for i,span in {0:(14,27),1:(32,37),3:(42,clocks[3]+6),4:(clocks[3]+11,64)}.items():
            if i!=omitted:
                strobe(i)
                write(f"grp1_{i}",f"m{i}",span)

    intervals=list(events.values())
    for i,(a,u) in enumerate(intervals):
        for b,v in intervals[i+1:]:
            solver.add(z3.Or(a+u<=b,b+v<=a),a+u+1!=b,b+v+1!=a)
    for a,u in intervals:
        solver.add(a!=3,a+u!=70)
    for name,(end,reg,readers) in uses.items():
        assert readers
        for other,(after,other_reg,_) in uses.items():
            if other!=name:
                solver.add(
                           z3.Or(reg!=other_reg,after<=end,z3.And(*(r<=after for r in readers))))

    result=solver.check()
    record=dict(family=family, packet=packet,omitted=omitted,status=str(result), clocks=clocks,
                solver=z3.get_version_string(), timeout_ms=LIMIT)
    if result==z3.sat:
        model=solver.model()
        record["instructions"]=sorted(
            [model.eval(start).as_long(),name,model.eval(z3.IntVal(cycles) if isinstance(cycles,int) else cycles).as_long(),
             model.eval(uses[name[5:]][1]).as_long() if name.startswith("load_") else None]
            for name,(start,cycles) in events.items()
        )
        record["registers"]={name:model.eval(reg).as_long() for name,(_,reg,_) in uses.items()}
    if result==z3.unknown:
        record["reason"]=solver.reason_unknown()
    return record


if __name__=="__main__":
    for family in ("p1-shadow","p0-share"):
        for packet in (False,True):
            print(json.dumps(search(family,packet)),flush=True)
    for shifted in (48,50):
        print(json.dumps(search("p0-share",True,clocks=[22,31,40,shifted,58])),flush=True)
    for packet in (False,True):
        print(json.dumps(search("p1-window",packet)),flush=True)
