// Node 18+ reproducible G5V SVG / map renderer, source-only, NOT APPROVED.
// Run from Odourman/let-me-out checkout root:
// node studies/graphics/G5V_B_OPEN_02_2026-11-17/render_g5v.mjs [output-directory]
import {readFileSync,writeFileSync,mkdirSync} from "node:fs";
import {createHash} from "node:crypto";
const sourceCommit="80bf072ee0e8a9a84905a29d70771a7cc6be7820", shaOld="820a74e5fb77c818ffb1286c5b23698d4374e771",shaOpen="0e449f97f87bd9b403476fd1435398042eaee285";
const oldPath="design/PLANERADE_RUMSKARTOR_V011.json",openPath="design/OPEN_ROOMS_V019_40x22_CANDIDATES.json";
function gitBlob(data){return createHash("sha1").update("blob "+Buffer.byteLength(data)+"\0").update(data).digest("hex");}
const oldText=readFileSync(oldPath,"utf8"),openText=readFileSync(openPath,"utf8");
if(gitBlob(oldText)!==shaOld||gitBlob(openText)!==shaOpen)throw Error("Original source Git blob mismatch: use the recorded pinned source");
const old=JSON.parse(oldText).rooms.find(x=>x.selected_layout_id==="B01");
const prior=JSON.parse(openText).maps.find(x=>x.id==="B_OPEN_01");
function fnv32(t){let h=2166136261>>>0;for(let i=0;i<t.length;i++)h=Math.imul(h^t.charCodeAt(i),16777619)>>>0;return h.toString(16).padStart(8,"0");}
function derive(open){
 const grid=open.map(row=>row.split(""));
 for(let y=1;y<=20;y++)for(let x=1;x<=38;x++)grid[y][x]=".";
 const rects=[["upper posts",11,12,3,7],["upper inward shelves",13,16,5,5],["upper outward steps",9,10,7,7],["lower posts",11,12,14,18],["lower inward shelves",13,15,15,15],["lower outward steps",8,10,17,17],["top central islet",19,19,7,8],["bottom central islet",19,19,13,14]];
 for(const [label,x0,x1,y0,y1] of rects)for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++)for(const xx of new Set([x,39-x]))grid[y][xx]="#";
 return {grid:grid.map(x=>x.join("")),rects};
}
function cellsCheck(grid) {
 if(grid.length!==22||grid.some(x=>x.length!==40))throw Error("dimension mismatch");
 for(let y=0;y<22;y++){const r=grid[y];if(r[0]!=="#"||r[39]!==(y>=9&&y<=12?"D":"#"))throw Error("door or left wall");for(const c of r)if(!"#.D".includes(c))throw Error("symbol");}
 if(grid[0]!=="#".repeat(40)||grid[21]!=="#".repeat(40))throw Error("top/bottom");
 for(let y=1;y<=20;y++)for(let x=1;x<=38;x++)if(grid[y][x]!==grid[y][39-x])throw Error("interior mirror");
 for(let y=9;y<=12;y++)for(let x=1;x<=38;x++)if(grid[y][x]!==".")throw Error("center");
}
function checkModel(grid,oldpositions){
 const valid=new Set(),key=(x,y)=>x+","+y;
 for(let y=0;y<21;y++)for(let x=0;x<39;x++)if([0,1].every(dy=>[0,1].every(dx=>grid[y+dy][x+dx]===".")))valid.add(key(x,y));
 const moves=[[1,0],[-1,0],[0,1],[0,-1]], start="2,10", seen=new Map([[start,0]]),q=[[2,10]];
 if(!valid.has(start))throw Error("invalid player");
 for(let i=0;i<q.length;i++){let [x,y]=q[i],d=seen.get(key(x,y));for(const [dx,dy] of moves){let nx=x+dx,ny=y+dy,k=key(nx,ny);if(valid.has(k)&&!seen.has(k)){seen.set(k,d+1);q.push([nx,ny]);}}}
 const goals=[[37,9],[37,10],[37,11]],gdist=Math.min(...goals.filter(([x,y])=>seen.has(key(x,y))).map(([x,y])=>seen.get(key(x,y))));
 const anchors=oldpositions.filter(([x,y])=>seen.has(key(x,y))).map(z=>z.slice());
 const neighbors=({x,y})=>moves.map(([dx,dy])=>[x+dx,y+dy]).filter(([i,j])=>valid.has(key(i,j)));
 let time=0;const disc=new Map(),low=new Map(),parent=new Map(),art=new Set();
 function dfs(x,y){const u=key(x,y);disc.set(u,time);low.set(u,time++);let count=0;for(const [nx,ny] of neighbors({x,y})){let v=key(nx,ny);if(!disc.has(v)){parent.set(v,u);count++;dfs(nx,ny);low.set(u,Math.min(low.get(u),low.get(v)));if(parent.has(u)&&low.get(v)>=disc.get(u))art.add(u);}else if(v!==parent.get(u))low.set(u,Math.min(low.get(u),disc.get(v)));}if(!parent.has(u)&&count>1)art.add(u);}
 for(const k of valid){if(!disc.has(k)){const [x,y]=k.split(",").map(Number);dfs(x,y);}}
 return {interior_walls:grid.slice(1,21).reduce((n,row)=>n+row.slice(1,39).split("").filter(v=>v==="#").length,0),free_2x2_anchors:valid.size,reachable_2x2_anchors:seen.size,unreachable_2x2_anchors:valid.size-seen.size,articulation_2x2_anchors:art.size,player_exit_approach_steps:gdist,reusable_historic_B01_candidates:anchors.length,retained_candidate_coords:anchors};
}
function svgEscape(t){return String(t).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");}
const COLORS={"#":"#906040",".":"#070A0C","D":"#F5A436"};
function drawGrid(map){let out=`<rect width="560" height="528" fill="${COLORS["."]}"/>`;for(let y=0;y<22;y++){const row=map[y];let x=0;while(x<40){const ch=row[x];let e=x+1;while(e<40&&row[e]===ch)e++;if(ch!==".")out+=`<rect x="${x*14}" y="${y*24}" width="${(e-x)*14}" height="24" fill="${COLORS[ch]}"/>`;x=e;}}return out;}
function svgWrap(w,h,inside){return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><style>text{font-family:Arial,Helvetica,sans-serif}.heading{fill:#edf0f3;font-size:27px;font-weight:bold}.name{fill:#edf0f3;font-size:24px;font-weight:bold}.label{fill:#b9c0c9;font-size:17px}.gold{fill:#F5A436}.mini{fill:#b9c0c9;font-size:13px}</style><rect width="${w}" height="${h}" fill="#13181e"/>${inside}</svg>\n`;}
function triple(entries){
 let result=`<text class="heading" x="35" y="37">LET ME OUT!  G5V  –  ROOM B: THREE EXACT 40 x 22 MAPS</text><text class="label" x="35" y="71">Offline graphics study. Source geometry preserved; B_OPEN_02 NOT APPROVED. NOT STELLA.</text>`;
 const statuses=["HISTORICAL v0.11","OLDER CANDIDATE v0.19","NEW CANDIDATE — NOT APPROVED"];
 for(let i=0;i<3;i++){const [name,map,metrics]=entries[i],px=35+i*620;result+=`<text class="${i===2?"name gold":"name"}" x="${px}" y="111">${statuses[i]}</text><text class="name" x="${px}" y="143">${name}</text><g transform="translate(${px},160)">${drawGrid(map)}</g><text class="label" x="${px}" y="721">Walls ${metrics.interior_walls}/760; Open ${(100*(760-metrics.interior_walls)/760).toFixed(1)}%</text>`;}
 return svgWrap(1890,775,result);
}
function overlay(map,positions,chosen){
 let v=`<text class="heading" x="25" y="39">B_OPEN_02 — POSSIBLE 2x2 ANCHORS ONLY</text><text class="label" x="25" y="74">Cyan: historical B01 anchors reusable in B_OPEN_02. Gold: five illustration choices.</text><text class="mini" x="25" y="96">Yellow P: player anchor (2,10). NOT 8x9 collision, AI, key or spawn validation.</text><g transform="translate(40,115)">${drawGrid(map)}`;
 for(const [x,y] of positions){const cx=(x+.5)*14,cy=(y+.5)*24;v+=`<circle cx="${cx}" cy="${cy}" r="6" fill="none" stroke="#67dcec" stroke-width="2.8"/>`;}
 for(let i=0;i<chosen.length;i++){const [x,y]=chosen[i],cx=(x+1)*14,cy=(y+1)*24;v+=`<circle cx="${cx}" cy="${cy}" r="11" fill="#f5a436" stroke="#fff" stroke-width="2"/><text text-anchor="middle" x="${cx}" y="${cy+5}" font-size="14" font-family="Arial" font-weight="bold" fill="#0f141a">${i+1}</text>`;}
 const cx=3*14,cy=11*24;v+=`<circle cx="${cx}" cy="${cy}" r="11" fill="#f6ef63" stroke="#fff" stroke-width="2"/><text text-anchor="middle" x="${cx}" y="${cy+5}" font-size="14" font-family="Arial" font-weight="bold" fill="#0f141a">P</text></g>`;
 v+=`<text class="label" x="40" y="682">13/13 historic B01 candidates reusable in this approximate 2x2 grid model.</text><text class="mini" x="40" y="710">A future 5-NPC spawn pool must be separately validated and authorized.</text>`;
 return svgWrap(640,742,v);
}
function diffSvg(a,b){
 let v=`<text class="heading" x="40" y="38">B_OPEN_01 → B_OPEN_02 | WALL CELL DIFFERENCE</text><text class="label" x="40" y="76">Green: newly added wall | Pink: removed wall | Brown: unchanged wall | Orange: door</text><g transform="translate(40,103)"><rect width="560" height="528" fill="${COLORS["."]}"/>`;
 let added=0,removed=0;
 for(let y=0;y<22;y++)for(let x=0;x<40;x++){
  const was=a[y][x],now=b[y][x];let col=COLORS[now];if(was==="."&&now==="#"){col="#91d69c";added++;}else if(was==="#"&&now==="."){col="#ff7789";removed++;}
  if(col!==COLORS["."])v+=`<rect x="${x*14}" y="${y*24}" width="14" height="24" fill="${col}"/>`;
 }
 v+=`</g><text class="label" x="40" y="671">Added walls: ${added}; removed walls: ${removed}; door: four unchanged D cells.</text>`;
 if(added!==48||removed!==24)throw Error("diff mismatch");
 return svgWrap(650,714,v);
}
const {grid,rects}=derive(prior.grid);cellsCheck(grid);
const mOld=checkModel(old.grid,old.candidate_positions),mPrior=checkModel(prior.grid,old.candidate_positions),mNew=checkModel(grid,old.candidate_positions);
if(fnv32(grid.join("\n"))!=="c9e29f45"||mNew.interior_walls!==72||mNew.free_2x2_anchors!==565||mNew.reachable_2x2_anchors!==565)throw Error("B_OPEN_02 reproduction mismatch");
const chosen=[[9,3],[29,3],[19,9],[9,15],[29,15]];
const proposed={"project":"LET ME OUT!","study_id":"G5V","map_id":"B_OPEN_02","room":"B","status":"GRAPHICS_SOURCE_ONLY_CANDIDATE_NOT_APPROVED_NOT_STELLA_NOT_ROM","date":"2026-11-17","source_commit":"80bf072ee0e8a9a84905a29d70771a7cc6be7820","sources":[{"path":"design/PLANERADE_RUMSKARTOR_V011.json","git_blob_sha":"820a74e5fb77c818ffb1286c5b23698d4374e771"},{"path":"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json","git_blob_sha":"0e449f97f87bd9b403476fd1435398042eaee285"}],"derived_from":"B_OPEN_01 (room B, v0.19 JSON); changed only the new in-study candidate matrix","coordinate_system":{"origin":"top-left","x":"right","y":"down","columns":40,"rows":22,"symbols":{"#":"wall",".":"open","D":"right-door marker"},"preview_cell_colorclocks":4,"preview_cell_scanlines":8},"design_note":"Four mirrored staggered posts with unequal inward/outward short shelves, plus two tiny central islands. Center rows 9..12 kept completely open. Left-right mirror preserved; top-bottom intentionally varied. 2x2 geometry only; no AI / ROM.","player_start_anchor":[2,10],"door":{"x":39,"rows":[9,10,11,12],"marker":"D","lock_visual":"orange with negative black keyhole is separate future graphic target, not a map glyph"},"grid":["########################################","#......................................#","#......................................#","#..........##..............##..........#","#..........##..............##..........#","#..........######......######..........#","#..........##..............##..........#","#........####......##......####........#","#..................##..................#","#......................................D","#......................................D","#......................................D","#......................................D","#..................##..................#","#..........##......##......##..........#","#..........#####........#####..........#","#..........##..............##..........#","#.......#####..............#####.......#","#..........##..............##..........#","#......................................#","#......................................#","########################################"],"geometry_only_reusable_B01_candidates":[[9,3],[19,3],[29,3],[14,9],[19,9],[24,9],[34,9],[9,15],[19,15],[29,15],[35,4],[35,13],[35,17]],"geometry_only_illustrative_five_anchors":[[9,3],[29,3],[19,9],[9,15],[29,15]],"not_validated":["actual 8x9 sprites","5 NPC dynamic collisions","AI/pathfinding","key-carrier drops","NTSC TIA PF/BL/P1 timing","ROM","Stella","independent verification"]};
if(JSON.stringify(proposed.grid)!==JSON.stringify(grid))throw Error("Frozen JSON disagrees with regenerated grid");
const files={
 "B_OPEN_02.json":JSON.stringify(proposed,null,2)+"\n",
 "B_OPEN_02.grid.txt":grid.map((s,i)=>String(i).padStart(2,"0")+" "+s).join("\n")+"\n",
 "B01.svg":svgWrap(560,528,drawGrid(old.grid)),
 "B_OPEN_01.svg":svgWrap(560,528,drawGrid(prior.grid)),
 "B_OPEN_02.svg":svgWrap(560,528,drawGrid(grid)),
 "G5V_B_TRIPTYCH.svg":triple([["B01",old.grid,mOld],["B_OPEN_01",prior.grid,mPrior],["B_OPEN_02",grid,mNew]]),
 "G5V_B02_START_ANCHORS.svg":overlay(grid,mNew.retained_candidate_coords,chosen),
 "G5V_B_OPEN_01_TO_02_DELTA.svg":diffSvg(prior.grid,grid)
};
const folder=process.argv[2]||"/tmp/let-me-out-G5V-reproduced";mkdirSync(folder,{recursive:true});
for(const [name,data] of Object.entries(files))writeFileSync(folder+"/"+name,data,"utf8");
console.log("G5V reproduced",Object.keys(files).length,"source-only files; B02 72 interior wall cells, 565/565 2x2 anchors connected. Output:",folder);
