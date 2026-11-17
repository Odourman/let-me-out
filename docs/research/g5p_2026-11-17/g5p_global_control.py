#!/usr/bin/env python3
"""Supplement: global detour-aware static-NPC lane graph, same scenario parameters."""
import g5p_offline as q, csv, collections, statistics
from pathlib import Path

def global_step(m,pos,i,goal):
    p=pos[i]; d=m.distances(goal)
    # Every reachable cell in this fixed snapshot, no 9-step truncation.
    fifo=collections.deque([p]); seen={p}; prev={p:None}; depth={p:0}
    best=(d.get(p,9999),0,p)
    while fifo:
      u=fifo.popleft()
      for v in m.adj[u]:
       if v in seen or q.violation(pos,i,v,True):continue
       seen.add(v);depth[v]=depth[u]+1;prev[v]=u;fifo.append(v)
       sc=(d.get(v,9999),depth[v],v)
       if sc<best:best=sc
    goalpos=best[2]
    if goalpos==p:return p
    while prev[goalpos] is not None and prev[goalpos]!=p:goalpos=prev[goalpos]
    return goalpos

def main():
 q.step_adaptive=global_step
 vals=[]
 for name in q.MAPDATA:
  m=q.Map(name)
  for si in range(3):
   spawns=q.choose_spawns(m,si);q.spawns_index[(name,tuple(spawns))]=si
   for scen in ('static_left','static_middle','static_right','horizontal','vertical','escape_door','walls'):
    d,_=q.trial(m,spawns,scen,'strict_adaptive')
    d['mode']='strict_global';vals.append(d)
 with (q.ROOT/'g5p_global_control.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(vals[0]),lineterminator='\n');w.writeheader();w.writerows(vals)
 for typ in ['v011','v019_candidate']:
  x=[a for a in vals if a['map_set']==typ]
  print(typ,'count',len(x),'unique',round(statistics.mean(a['unique_threats'] for a in x),3),'rate',round(statistics.mean(a['movement_rate'] for a in x),3),'stall',sum(a['stalled_npcs_30']>0 for a in x),'y-overlap',max(a['y_overlap_frames'] for a in x),'zero-threat',sum(a['unique_threats']==0 for a in x))

if __name__=='__main__':main()
