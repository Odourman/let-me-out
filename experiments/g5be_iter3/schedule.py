"""G5BE deterministic 6507 instruction packing. Store windows are empirical bounds."""
import json
from pathlib import Path

import z3

X = [127,19,73,100,46]
Y = [73,72,73,71,72]
ORDER = sorted(range(5), key=X.__getitem__)
CLOCK = [(X[i]+48)//3 for i in ORDER]
LIMIT = 15000


def search(family, packet=False, omitted=None, clocks=CLOCK, fetch=None, limit=71):
    solver = z3.Solver()
    solver.set(timeout=LIMIT, random_seed=0)
    events, uses = {}, {}

    def instruction(name, cycles, earliest=2, latest=limit, wide=False):
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
            load(f"m{i}", fetch if fetch is not None else (2 if packet else 4))

    if family in ("late-p0", "late-p0-relaxed"):
        instruction("reset_p0", 3, 24, 24, wide=True)
        # c22 at X19 is the P1 +16 copy. P0 single uses the primary.
        reset = clocks[2] + 5
        instruction("move_p0", 3, reset, reset, wide=True)
        load("white", 2)
        load("yellow", 2)
        write("colup0_white", "white", (32,reset+2))
        write("grp0_f", "m2", (32,reset+5))
        write("colup0_yellow", "yellow", (reset+6,73))
        for i,span in {0:(12,27),1:(30,36),3:(42,55),4:(58,64)}.items():
            strobe(i)
            if family.endswith("relaxed"):
                span = (span[0]-4, span[1]+4)
            write(f"grp1_{i}",f"m{i}",span)
    elif family in ("all-p1", "all-p1-calibrated"):
        for i,span in {0:(12,27),1:(30,36),2:(37,clocks[2]+5),
                       3:(42,55),4:(58,64)}.items():
            reset=strobe(i)
            if family == "all-p1-calibrated" and i==0:
                span=(span[0],25)
            write(f"grp1_{i}",f"m{i}",span)
            if family == "all-p1-calibrated" and i==2:
                solver.add(reset<=events[f"grp1_{i}"][0])
    else:
        raise ValueError(family)

    intervals=list(events.values())
    for i,(a,u) in enumerate(intervals):
        for b,v in intervals[i+1:]:
            solver.add(z3.Or(a+u<=b,b+v<=a),a+u+1!=b,b+v+1!=a)
    for a,u in intervals:
        solver.add(a!=3,a+u!=limit-1)
    for name,(end,reg,readers) in uses.items():
        assert readers
        for other,(after,other_reg,_) in uses.items():
            if other!=name:
                solver.add(
                           z3.Or(reg!=other_reg,after<=end,z3.And(*(r<=after for r in readers))))

    result=solver.check()
    record=dict(family=family, packet=packet,fetch=fetch,deadline=limit,omitted=omitted,status=str(result), clocks=clocks,
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
    for family in ("late-p0","late-p0-relaxed","all-p1","all-p1-calibrated"):
        for x in (73,67,76,82,64):
            for fetch in (3,2):
                record=search(family,fetch=fetch,limit=73,clocks=[21 if family.startswith("late") else 22,31,(x+47)//3,49,58])
                print(json.dumps(dict(record,x=x)),flush=True)
