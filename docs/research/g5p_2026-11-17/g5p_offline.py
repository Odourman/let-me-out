#!/usr/bin/env python3
"""G5P advisory offline grid/AI and render-demand study. No DASM, ROM or Stella."""
import csv, json, random, collections, statistics, itertools, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MAPDATA={
'A01':('ffffffffff 8000000001 8000000001 8000000001 87f0000fe1 8600000061 8600000061 860781e061 8000000001 8000000000 8000000000 8000000000 8000000000 8000000001 860781e061 8600000061 87f0000fe1 8000000001 8000000001 8000000001 8000000001 ffffffffff',[[14,3],[19,3],[24,3],[9,6],[29,6],[14,9],[19,9],[24,9],[34,9],[9,12],[29,12],[14,15],[19,15],[24,15],[4,18],[9,18],[29,18],[34,18],[35,4],[35,13]]),
'B01':('ffffffffff 8000000001 8000000001 870e0070e1 870e6670e1 870e6670e1 870e6670e1 87000000e1 8000000001 8038001c00 8038001c00 8038001c00 8038001c00 8000000001 87000000e1 870e6670e1 870e6670e1 870e6670e1 870e0070e1 8000000001 8000000001 ffffffffff',[[9,3],[19,3],[29,3],[14,9],[19,9],[24,9],[34,9],[9,15],[19,15],[29,15],[35,4],[35,13],[35,17]]),
'C02':('ffffffffff 8000000001 8000000001 8000000001 8ff8001ff1 8ff8001ff1 8c00000031 8c00000031 801fc3f801 80c0000300 8000000000 8000000000 80c0000300 801fc3f801 8c00000031 8c00000031 8ff8001ff1 8ff8001ff1 8000000001 8000000001 8000000001 ffffffffff',[[14,3],[19,3],[24,3],[9,6],[29,6],[14,9],[19,9],[24,9],[34,9],[14,15],[19,15],[24,15],[4,18],[9,18],[29,18],[34,18],[6,13],[31,13]]),
'D01':('ffffffffff 8000000001 80007e0001 80387e1c01 87387e1ce1 87387e1ce1 87007e00e1 87007e00e1 80007e0001 8000000000 8000000000 8000000000 8000000000 80007e0001 80007e0001 87007e00e1 87387e1ce1 87387e1ce1 87387e1ce1 80007e0001 8000000001 ffffffffff',[[14,3],[24,3],[9,6],[29,6],[14,9],[19,9],[24,9],[34,9],[9,12],[29,12],[14,15],[24,15],[35,4],[35,13],[35,17]]),
'A_OPEN_01':('ffffffffff 8000000001 8000000001 8000000001 8080000101 8080000101 8080000101 80fc003f01 8000000001 8000000000 8000000000 8000000000 8000000000 8000000001 80fc003f01 8080000101 8080000101 8080000101 8000000001 8000000001 8000000001 ffffffffff',[[14,3],[19,3],[24,3],[14,9],[19,9],[24,9],[34,9],[9,12],[29,12],[14,15],[19,15],[24,15],[4,18],[9,18],[29,18],[34,18],[35,4],[35,13]]),
'B_OPEN_01':('ffffffffff 8000000001 8000000001 8030000c01 8030000c01 8030000c01 8030000c01 8030000c01 8030000c01 8000000000 8000000000 8000000000 8000000000 8030000c01 8030000c01 8030000c01 8030000c01 8030000c01 8030000c01 8000000001 8000000001 ffffffffff',[[19,3],[14,9],[19,9],[24,9],[34,9],[19,15],[35,4],[35,13],[35,17]]),
'C_OPEN_01':('ffffffffff 8000000001 8000000001 8000000001 8000000001 87fe007fe1 8006006001 8006006001 8006006001 8000000000 8000000000 8000000000 8000000000 8006006001 8006006001 8006006001 87fe007fe1 8000000001 8000000001 8000000001 8000000001 ffffffffff',[[14,3],[19,3],[24,3],[9,6],[29,6],[14,9],[19,9],[24,9],[34,9],[19,15],[4,18],[9,18],[29,18],[34,18],[6,13],[31,13]]),
'D_OPEN_01':('ffffffffff 8000000001 8000000001 8000000001 8018001801 8018001801 8018001801 8018001801 801fc3f801 8000000000 8000000000 8000000000 8000000000 801fc3f801 8018001801 8018001801 8018001801 8018001801 8000000001 8000000001 8000000001 ffffffffff',[[14,3],[24,3],[9,6],[29,6],[14,9],[19,9],[24,9],[34,9],[9,12],[29,12],[14,15],[24,15],[35,4],[35,13],[35,17]])
}
HIST_START={
'A01':[(14,3),(9,6),(14,9),(9,12),(14,15)],
'B01':[(9,3),(14,9),(35,13),(9,15),(35,17)],
'C02':[(14,3),(9,6),(14,9),(14,15),(4,18)],
'D01':[(14,3),(9,6),(14,9),(9,12),(14,15)]}
DIRECTIONS=((0,-1),(0,1),(-1,0),(1,0)) # UP DOWN LEFT RIGHT: historical G5O tie-breaking
TICKS=180
SEED=20261117

def decode(data):
    r,c=data
    grid=[''.join('#' if (int(s,16)>>(39-x))&1 else ( 'D' if x==39 and y in (9,10,11,12) else '.') for x in range(40)) for y,s in enumerate(r.split())]
    assert len(grid)==22 and all(len(row)==40 for row in grid)
    return grid,[tuple(t) for t in c]

class Map:
 def __init__(self,name):
    self.name=name
    self.grid,self.candidates=decode(MAPDATA[name]); self.nodes=set()
    for y in range(21):
      for x in range(39):
       if all(self.grid[y+dy][x+dx]=='.' for dy in (0,1) for dx in (0,1)):
        self.nodes.add((x,y))
    self.adj={p:[(p[0]+dx,p[1]+dy) for dx,dy in DIRECTIONS if (p[0]+dx,p[1]+dy) in self.nodes] for p in self.nodes}
    self.cache={}
    assert (2,10) in self.nodes
 def distances(self,p):
    if p not in self.cache:
      d={p:0}; q=collections.deque([p])
      while q:
        u=q.popleft()
        for v in self.adj.get(u,[]):
         if v not in d:d[v]=d[u]+1;q.append(v)
      self.cache[p]=d
    return self.cache[p]
 def route(self,start,goal,blocked=()):
    if goal not in self.nodes:return None
    b=set(blocked); b.discard(start); b.discard(goal)
    q=collections.deque([start]); prev={start:None}
    while q:
      u=q.popleft()
      if u==goal:break
      for v in self.adj.get(u,[]):
       if v not in prev and not any(overlap(v,ob) for ob in b):prev[v]=u;q.append(v)
    if goal not in prev:return None
    r=[];p=goal
    while p is not None:r.append(p);p=prev[p]
    return r[::-1]

def overlap(a,b):return abs(a[0]-b[0])<2 and abs(a[1]-b[1])<2

def choose_spawns(m,si):
 if si==0 and m.name in HIST_START:return HIST_START[m.name]
 choices=[p for p in m.candidates if p in m.nodes and p in m.distances((2,10))]
 sets=list(z for z in itertools.combinations(choices,5) if all(abs(a[1]-b[1])>=2 for a,b in itertools.combinations(z,2)))
 if not sets:raise ValueError('No 5-y-separated candidate set for '+m.name)
 rng=random.Random(SEED+1000*list(MAPDATA).index(m.name)+si)
 if m.name in HIST_START:
  sets=[s for s in sets if set(s)!=set(HIST_START[m.name])]
 return list(sets[rng.randrange(len(sets))])

def nearest(m,p):
 if p in m.nodes:return p
 return min(m.nodes,key=lambda q:(abs(q[0]-p[0])+abs(q[1]-p[1]),q[1],q[0]))

def path(m,scenario):
 st=(2,10)
 if scenario=='static_left':return [st]*TICKS
 if scenario=='static_middle':return [nearest(m,(19,10))]*TICKS
 if scenario=='static_right':return [nearest(m,(34,10))]*TICKS
 # Move at one anchor per two NPC ticks. Player waypoints loop or hold.
 if scenario=='horizontal':points=[(2,10),(34,10),(2,10)]
 elif scenario=='vertical':points=[(19,3),(19,18),(19,3)]
 elif scenario=='escape_door':points=[(2,10),(19,10),(37,10)]
 elif scenario=='walls':points=[(4,3),(34,17),(4,17),(34,3)]
 else:raise ValueError(scenario)
 steps=[nearest(m,points[0])]
 for q in points[1:]:
  rr=m.route(steps[-1],nearest(m,q))
  if rr:steps+=rr[1:]
 moving=[]
 for t in range(TICKS):
  moving.append(steps[min(t//2,len(steps)-1)])
 return moving

def violation(pos,i,q,hard):
 for j,r in enumerate(pos):
  if j==i:continue
  if overlap(q,r):return True
  if hard and abs(q[1]-r[1])<2:return True
 return False

def step_greedy(m,pos,i,goal,hard,allow_npc_collision=False):
 p=pos[i]; d=m.distances(goal); old=d.get(p,9999)
 options=[q for q in m.adj[p] if d.get(q,9999)<old and (allow_npc_collision or not violation(pos,i,q,hard))]
 if options: return min(options,key=lambda q:(d.get(q,9999),abs(q[1]-goal[1]),m.adj[p].index(q)))
 return p

def step_adaptive(m,pos,i,goal):
 # A 9-step lookahead (limited A* search), allows sidesteps / increases in shortest path;
 # hard Y separation and NPC 2x2 collisions enforced for each candidate position.
 p=pos[i]; dist=m.distances(goal)
 allowed=lambda q: not violation(pos,i,q,True)
 q=collections.deque([(p,0,p)])
 seen={p};best=(dist.get(p,999),0,0,p)
 while q:
   u,depth,first=q.popleft()
   if depth>=9:continue
   for v in m.adj[u]:
     if v in seen or not allowed(v):continue
     seen.add(v); nd=depth+1; f=v if depth==0 else first
     # Prefer lower distance; break ties by shorter plan/ movement, then stable ordering.
     score=(dist.get(v,999),nd,abs(v[1]-goal[1]),f)
     if score<best:best=score
     q.append((v,nd,f))
 return best[3]

def band_overlaps(pos):
 return sum(abs(a[1]-b[1])<2 for a,b in itertools.combinations(pos,2))

def synthetic_visibility(pos,t):
 # Conservative idealized one-white-P1-lane per shared Y band, NOT physical TIA/G0.
 order=sorted(range(len(pos)), key=lambda i:( (i+t)%len(pos)))
 kept=[]
 for i in order:
  if all(abs(pos[i][1]-pos[j][1])>=2 for j in kept):kept.append(i)
 return kept

def trial(m,spawns,scen,mode,trace=False):
 pos=list(spawns); player=path(m,scen)
 assert all(q in m.nodes for q in pos)
 moved=attempted=collision_blocked=0; stalls=[0]*5;stalled_30=[False]*5
 first_threat=None;threats=set(); hidden=0;hidden_by=[0]*5; conflict_frames=0; max_pair_overlap=0; snapshot=None
 traj=[]; start_overlap=sum(overlap(a,b) for a,b in itertools.combinations(pos,2))
 for t in range(TICKS):
  goal=player[t]; dist=m.distances(goal)
  ids=[(j+t)%5 for j in range(5)]
  for i in ids:
   attempted+=1
   q=step_adaptive(m,pos,i,goal) if mode=='strict_adaptive' else step_greedy(m,pos,i,goal,mode=='strict_greedy')
   if q!=pos[i]:pos[i]=q;moved+=1;stalls[i]=0
   else:
    stalls[i]+=1
    if mode=='strict_greedy' and any(dist.get(v,9999)<dist.get(pos[i],9999) for v in m.adj[pos[i]]): collision_blocked+=1
   if stalls[i]>=30 and dist.get(pos[i],9999)>3:stalled_30[i]=True
  near=[i for i,p in enumerate(pos) if dist.get(p,9999)<=2]
  if near and first_threat is None:first_threat=t+1
  threats.update(near)
  overlap_pairs=band_overlaps(pos);max_pair_overlap=max(max_pair_overlap,overlap_pairs)
  if overlap_pairs:conflict_frames+=1
  if mode=='soft':
   keep=synthetic_visibility(pos,t); hidden+=(5-len(keep))
   for i in range(5):
    if i not in keep:hidden_by[i]+=1
  if t==89:snapshot=(pos.copy(),goal)
  if trace and (t<16 or t%10==9 or t==TICKS-1):
   traj.append(dict(tick=t+1,player_x=goal[0],player_y=goal[1],npc_positions='|'.join('%d:%d'%p for p in pos),near_count=len(near),y_conflicting_pairs=overlap_pairs,shown='|'.join(str(x) for x in synthetic_visibility(pos,t))))
 door=(37,10)
 # Snapshot potential after carrier death: counterfactual each of five held static at its prior location.
 # A logical drop is fixed. Reachability measured with and without other NPC blocking at t=90.
 reach_empty=reach_occ=0
 for i,k in enumerate(snapshot[0]):
  p=snapshot[1]
  a=m.route(p,k)
  b=m.route(p,k,[q for j,q in enumerate(snapshot[0]) if j!=i])
  if a and m.route(k,door):reach_empty+=1
  if b and m.route(k,door,[q for j,q in enumerate(snapshot[0]) if j!=i]):reach_occ+=1
 # Potential door path when NPCs still occupy positions, no key pickup simulation.
 door_open= m.route(snapshot[1],door) is not None
 door_blocked= m.route(snapshot[1],door,snapshot[0]) is None
 return dict(map=m.name,map_set='v011' if '_OPEN_' not in m.name else 'v019_candidate',seed=SEED,spawn_index=spawns_index.get((m.name,tuple(spawns)),-1),spawn_positions='|'.join('%d:%d'%x for x in spawns),scenario=scen,mode=mode,ticks=TICKS,first_threat_tick=first_threat if first_threat is not None else -1,unique_threats=len(threats),moved=moved,attempts=attempted,movement_rate=round(moved/attempted,4),strict_blocked_gradients=collision_blocked,stalled_npcs_30=sum(stalled_30),y_overlap_frames=conflict_frames,max_y_overlapping_pairs=max_pair_overlap,soft_hidden_npc_ticks=hidden,soft_max_individual_hidden_ticks=max(hidden_by),logical_key_to_door_5_carriers_no_occupancy=reach_empty,logical_key_to_door_5_carriers_with_snapshot_occupancy=reach_occ,door_empty_reachable=int(door_open),door_snapshot_blocked=int(door_blocked),initial_npc_footprint_overlaps=start_overlap,final_positions='|'.join('%d:%d'%x for x in pos)),traj

spawns_index={}

def legacy(m,goals):
 # Historical G5O mathematical replay: no NPC/NPC collision for the unrestricted comparison.
 results=[]
 for gx,gy in goals:
  goals=(gx,gy); old=m.distances(goals)
  for typ in ('lane','unrestricted'):
   pos=HIST_START[m.name][:];moves=0;block=0;requests=0
   for t in range(180):
    for j in range(5):
     i=(j+t)%5;p=pos[i];startd=old.get(p,999)
     options=[q for q in m.adj[p] if old.get(q,999)<startd]
     if not options:continue
     requests+=1
     allowed=[q for q in options if typ=='unrestricted' or all(abs(q[1]-pos[k][1])>=2 for k in range(5) if k!=i)]
     if not allowed:block+=1;continue
     q=min(allowed,key=lambda q:(old.get(q,999),abs(q[1]-gy),m.adj[p].index(q)))
     pos[i]=q;moves+=1
   near=sum(old.get(q,999)<=1 for q in pos)
   results.append((m.name,gx,gy,typ,near,moves,block,requests,'|'.join('%d:%d'%p for p in pos),'/'.join(str(old.get(p,999)) for p in pos)))
 return results

def g5o_reproduce():
 header='room,target_x,target_y,steps_per_npc,lane_near_at_end,unrestricted_near_at_end,lane_moved,lane_blocked_gradient_requests,lane_total_gradient_requests,lane_remaining_BFS_distances,lane_final_positions'.split(',')
 rows=[]
 for n in ('A01','B01','C02','D01'):
  m=Map(n); cs=legacy(m,[(2,10),(19,10),(34,10)])
  for z in range(0,len(cs),2):
   a,b=cs[z:z+2];rows.append([n,a[1],a[2],180,a[4],b[4],a[5],a[6],a[7],a[9],a[8]])
 with (ROOT/'g5o_replay.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(header);w.writerows(rows)
 return rows

def key_s05():
 # Logical models: two horizontally aligned 8-bit masks, no TIA timing proof.
 male=[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
 key =[0x3c,0x66,0x66,0x66,0x3c,0x18,0x1c,0x18,0x1c] # provisional K09-R ONLY
 result=[]
 for label,dx in [('same_pixels',0),('same_raster_without_x_overlap',14)]:
  count=0
  for y in range(9):
   for x in range(8):
    if (male[y]>>(7-x))&1:
     key_x=x-dx
     if 0<=key_x<8 and ((key[y]>>(7-key_x))&1):count+=1
  o1=count>0
  result.append(dict(scene=label,white_x_cc=60,key_x_cc=60+dx,y_grid=10,bitmap_pixel_overlaps=count,approved_O1_occlusion_allowed=o1,required_bitmap_events='player+white+key+lockeddoor',p1_reserved_for_orange_door=True,p0_nominal_bitmap_events=3,key_logical_position_fixed=True,door_hole_must_remain_black=True,hardware_result='NOT_TESTED_G0'))
 with (ROOT/'s05_logical_stress.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=result[0],lineterminator='\n');w.writeheader();w.writerows(result)
 return result

def main():
 rows=g5o_reproduce()
 cases=[];traces=[]
 for name in MAPDATA:
  m=Map(name)
  for si in range(3):
   spawns=choose_spawns(m,si);spawns_index[(name,tuple(spawns))]=si
   for scen in ('static_left','static_middle','static_right','horizontal','vertical','escape_door','walls'):
    for mode in ('strict_greedy','strict_adaptive','soft','free'):
     d,tr=trial(m,spawns,scen,mode,trace=si==0 and name in ('B01','C02','B_OPEN_01') and scen in ('static_left','escape_door'))
     cases.append(d)
     for t in tr:traces.append({**{k:d[k] for k in ('map','scenario','mode','spawn_index')},**t})
 for file,data in [('g5p_scenarios.csv',cases),('g5p_traces.csv',traces)]:
  with (ROOT/file).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
 summary=[]
 for typ in ('v011','v019_candidate'):
  for mode in ('strict_greedy','strict_adaptive','soft','free'):
   vals=[x for x in cases if x['map_set']==typ and x['mode']==mode]
   summary.append(dict(map_set=typ,mode=mode,n=len(vals),mean_unique_threats=round(statistics.mean(x['unique_threats'] for x in vals),3),zero_threat_cases=sum(x['unique_threats']==0 for x in vals),first_threat_not_seen=sum(x['first_threat_tick']<0 for x in vals),mean_first_threat_given_seen=round(statistics.mean(x['first_threat_tick'] for x in vals if x['first_threat_tick']>0),2) if any(x['first_threat_tick']>0 for x in vals) else '',mean_move_rate=round(statistics.mean(x['movement_rate'] for x in vals),3),cases_with_30tick_stall=sum(x['stalled_npcs_30']>0 for x in vals),mean_y_overlap_frames=round(statistics.mean(x['y_overlap_frames'] for x in vals),1),mean_soft_hidden_npc_ticks=round(statistics.mean(x['soft_hidden_npc_ticks'] for x in vals),1),mean_key_carriers_reachable_without_occupancy=round(statistics.mean(x['logical_key_to_door_5_carriers_no_occupancy'] for x in vals),2),mean_key_carriers_reachable_with_occupancy=round(statistics.mean(x['logical_key_to_door_5_carriers_with_snapshot_occupancy'] for x in vals),2),door_blocked_snapshots=sum(x['door_snapshot_blocked'] for x in vals)))
 with (ROOT/'g5p_summary.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(summary[0]),lineterminator='\n');w.writeheader();w.writerows(summary)
 s05=key_s05()
 # manifest covers direct original map git blob names but input hex is our own encoding.
 manifest={'tested_maps':list(MAPDATA),'map_sha_github_blob':{'v011':'pending_external','v019':'pending_external'},'seed':SEED,'ticks':TICKS,'scenario_count':len(cases),'g5o_replay_rows':len(rows),'model':'2x2 anchor approximation','modes':['strict_greedy','strict_adaptive','soft','free'],'scenario_names':['static_left','static_middle','static_right','horizontal','vertical','escape_door','walls'],'source_file_hashes':{}}
 for p in [ROOT/'g5o_replay.csv',ROOT/'g5p_scenarios.csv',ROOT/'g5p_traces.csv',ROOT/'g5p_summary.csv',ROOT/'s05_logical_stress.csv']:
  manifest['source_file_hashes'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
 (ROOT/'RUN_METADATA.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print('G5O_REPLAY')
 for r in rows:print(','.join(map(str,r)))
 print('SUMMARY')
 for r in summary:print(json.dumps(r,ensure_ascii=False))
 print('S05',json.dumps(s05,ensure_ascii=False))

if __name__=='__main__':main()
