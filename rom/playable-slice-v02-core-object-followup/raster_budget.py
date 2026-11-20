"""Describe register deadlines for the frozen stress-fixture geometry."""
import json

from pixels import masks_for_project


def runs(bits, origin):
    """Report inclusive visible spans from an eight-bit TIA graphics byte."""
    spans=[]
    for offset in range(8):
        if bits & (0x80 >> offset):
            x=origin+offset
            if spans and spans[-1][-1]+1==x:
                spans[-1][-1]=x
            else:
                spans.append([x,x])
    return spans


def window(spans):
    return [spans[0][0]+68,spans[-1][1]+68] if spans else None


def report():
    names=("M0","M1","F","SM","SF")
    origins=(20,44,68,92,116)
    masks=masks_for_project()
    same_y=[]
    for row in range(9):
        actors=[]
        for name,x,mask in zip(names,origins,masks):
            spans=runs(mask[row],x)
            if spans:
                actors.append(dict(actor=name,spans=spans,clocks=window(spans)))
        for left,right in zip(actors,actors[1:]):
            # The gap excludes the final old and initial new lit pixel.
            left["free_clocks_to_next"]=right["clocks"][0]-left["clocks"][1]-1
        same_y.append(dict(y=86+row,actors=actors))
    key_rows=(0,0x70,0x50,0x7e,0x24,0x04)
    key=[]
    for row,bits in enumerate(key_rows):
        if not bits:
            continue
        sm_row=5+row
        sm=runs(masks[3][sm_row],59) if sm_row<9 else []
        gold=runs(bits,85)
        key.append(dict(y=153+row,sm=window(sm),gold=window(gold),
                        gold_spans=gold))
    return dict(same_y86=same_y,key_player_band=key,
                r3={f"${byte:02x}":runs(byte,153) for byte in (0x3c,0x66,0x76)},
                direct_zero_page_write_cycles=3)


if __name__=="__main__":
    print(json.dumps(report(),indent=2))
