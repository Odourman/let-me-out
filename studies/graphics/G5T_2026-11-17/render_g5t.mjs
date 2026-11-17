// Reproduces all 18 SVG images from original JSON in the repository. Node 18+
// Usage from repository root: node studies/graphics/G5T_2026-11-17/render_g5t.mjs [output-dir]
import {readFileSync,writeFileSync,mkdirSync} from "node:fs";
const HIST=JSON.parse(readFileSync("design/PLANERADE_RUMSKARTOR_V011.json","utf8"));
const NEXT=JSON.parse(readFileSync("design/OPEN_ROOMS_V019_40x22_CANDIDATES.json","utf8"));
const CELL=16,COL={"bg":"#080808","page":"#141619","wall":"#82512d","door":"#f3982e","white":"#f3eee6","muted":"#aeb7c0","cyan":"#64d9e9","red":"#f47c88","gold":"#e7bd82"},W=760,H=455,GAP=25,PW=1545,PH=540;
function esc(t){return String(t).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");}
function wrapSvg(width,height,body){return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}"><style>text{font-family:Arial,sans-serif}.h{font-size:26px;font-weight:bold;fill:${COL.white}}.l{font-size:20px;font-weight:bold;fill:${COL.white}}.n{font-size:20px;font-weight:bold;fill:${COL.gold}}.d{font-size:13px;fill:${COL.muted}}</style><rect width="${width}" height="${height}" fill="${COL.bg}"/>${body}</svg>\n`;}
function panel(m,overlay,excluded){
 let v=`<rect width="${W}" height="${H}" fill="${COL.page}"/><text class="h" x="44" y="31">${esc(m.id)}</text>`;
 const ox=48,oy=51;
 v+=`<rect x="${ox-2}" y="${oy-2}" width="644" height="356" fill="${COL.white}"/><rect x="${ox}" y="${oy}" width="640" height="352" fill="${COL.bg}"/>`;
 for(let y=0;y<22;y++){let row=m.grid[y];for(let x=0;x<40;){let ch=row[x],k=x+1;while(k<40&&row[k]===ch)k++;if(ch!=="."&&ch!=="#"&&ch!=="D")throw Error("Invalid cell "+ch);if(ch!==".")v+=`<rect x="${ox+x*CELL}" y="${oy+y*CELL}" width="${(k-x)*CELL}" height="${CELL}" fill="${ch==="#"?COL.wall:COL.door}"/>`;x=k;}}
 for(const x of [0,10,20,30,39])v+=`<text class="d" text-anchor="middle" x="${ox+(x+.5)*CELL}" y="${oy+22*CELL+25}">${x}</text>`;
 for(const y of [0,9,12,21])v+=`<text class="d" text-anchor="end" x="${ox-8}" y="${oy+(y+.7)*CELL}">${y}</text>`;
 if(overlay){
  const points=m.candidate_positions??m.reusable_old_S0_candidates_for_geometry_only;
  for(const [x,y] of points){const cx=ox+(x+.5)*CELL,cy=oy+(y+.5)*CELL;v+=`<circle cx="${cx}" cy="${cy}" r="5.3" fill="none" stroke="${COL.cyan}" stroke-width="2.2"/><circle cx="${cx}" cy="${cy}" r="1.4" fill="white"/>`;}
  for(const [x,y] of excluded){const cx=ox+(x+.5)*CELL,cy=oy+(y+.5)*CELL;v+=`<path d="M${cx-6} ${cy-6}l12 12m-12 0l12 -12" stroke="${COL.red}" stroke-width="2.2"/>`;}
 }
 return v;
}
function makeFiles(historic,candidate){
 const left=Object.fromEntries(historic.rooms.map(m=>[m.selected_layout_id,{...m,id:m.selected_layout_id}]));
 const right=Object.fromEntries(candidate.maps.map(m=>[m.id,m])); const output={};
 const pairs=[["A01","A_OPEN_01"],["B01","B_OPEN_01"],["C02","C_OPEN_01"],["D01","D_OPEN_01"]];
 for(const m of Object.values({...left,...right}))output[m.id+".svg"]=wrapSvg(W,H,panel(m,false,[]));
 function pair(a,b,overlay){
  const o=left[a],n=right[b],lost=overlay?o.candidate_positions.filter(([x,y])=>!n.reusable_old_S0_candidates_for_geometry_only.some(z=>z[0]===x&&z[1]===y)):[];
  return `<text class="h" x="20" y="36">${a} vs ${b}</text><text class="l" x="20" y="70">HISTORICAL v0.11</text><text class="n" x="${W+GAP}" y="70">NOT APPROVED CANDIDATE v0.19</text><g transform="translate(0,87)">${panel(o,overlay,[])}</g><g transform="translate(${W+GAP},87)">${panel(n,overlay,lost)}</g><text class="d" x="20" y="${PH-11}">OFFLINE SOURCE GRID, NOT STELLA. x right, y down; all cell positions exact.</text>`;
 }
 for(const [a,b] of pairs){
 output[`${a}_vs_${b}.svg`]=wrapSvg(PW,PH,pair(a,b,false));
 output[`${a}_vs_${b}_spawns.svg`]=wrapSvg(PW,PH,pair(a,b,true));
 }
 let overview=`<text class="h" x="18" y="35">LET ME OUT! / G5T / FOUR EXACT ROOM MAP PAIRS</text><text class="d" x="18" y="62">Brown wall | black open | orange right-door cell | all map grid geometry direct from JSON | no ROM</text>`;
 let overlay=`<text class="h" x="18" y="35">LET ME OUT! / G5T / GEOMETRIC START CANDIDATES</text><text class="d" x="18" y="61">Cyan = source candidate  |  red X = historic anchor excluded by v0.19 source filter</text><text class="d" x="18" y="79">NOT five prevalidated spawn locations. No actual sprite/AI/key/collision tests.</text>`;
 for(let i=0;i<pairs.length;i++){overview+=`<g transform="translate(0,${86+i*PH})">${pair(...pairs[i],false)}</g>`;overlay+=`<g transform="translate(0,${102+i*PH})">${pair(...pairs[i],true)}</g>`;}
 output["G5T_ALL_FOUR_PAIRS.svg"]=wrapSvg(PW,86+4*PH,overview);
 output["G5T_SPAWN_CANDIDATES_ALL_FOUR.svg"]=wrapSvg(PW,102+4*PH,overlay);
 return output;
}
const output=process.argv[2]||"/tmp/let-me-out-G5T-svg";mkdirSync(output,{recursive:true});
const files=makeFiles(HIST,NEXT);for(const [name,body] of Object.entries(files))writeFileSync(output+"/"+name,body,"utf8");
console.log("Created",Object.keys(files).length,"source-only SVG files in",output);
