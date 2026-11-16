# LET ME OUT! v0.18 – R3 / C02-högerdörr – utvecklaröverlämning

**Datum:** 2026-11-16. **Roll:** ROM DEVELOPMENT, egenkontroll. **Scope:** enbart isolerad R3/NTSC v0.18. **Ingen** oberoende VERIFICATION, fullspelsacceptans, R1/R2/R4-implementering, PAL, kartcutover eller PR-merge.

## 1. Sammanfattning

En **verklig körbar 16 384-byte F6/NTSC-ROM** reproducerar exakt den av användaren källvalda C02-kartan (40 × 22 celler; 8 rasterlinjer per cellrad) med asymmetrisk playfield. Vänsterväggen hålls stängd i samtliga 22 rader; den enda högra öppningen finns vid x39, y9–12. En **separat orange P1-port** med **transparent utstansat svart nyckelhål** visas i låst tillstånd. När diagnosflaggan byter till öppet tillstånd försvinner både porten och nyckelhålet samtidigt. Låst brun baslinje visas också för färgjämförelse.

De verkliga Stella 6.7.1-bilderna uppfyller map/port-pixelkraven i de fångade tillstånden, och en sammanhängande **600-frame GUI-registrering** visar **262 scanlines på samtliga 600**; bildrutnummer 11–610. Relevanta TIA-skrivningar fångas med verkliga **Stella-debugger-villkorade skrivtraps**, inte bara statiska cykelberäkningar. Dessa resultat är **DEVELOPER_LOCAL_PASS** inom R3:s isolerade delkrav; slutlig v0.18-diagnostik förblir **BLOCKED/NOT ACCEPTED**, och den oberoende granskningen ligger hos separat VERIFICATION när MAIN beställer en fryst batch.

## 2. Källauktoritet och gränser

- Repo: `Odourman/let-me-out`.
- Exakt kartkälla: `design/PLANERADE_RUMSKARTOR_V011.json`, **selected_layout_id=C02**, SHA-256 för källfilens byte `760d77bbb71bfdd0b3020d827ca7874abdcde4e399979289f75719572ee22d4a`.
- Geometrin hämtas från **källans original-JSON**, inte en omskriven v0.19-karta. Källan intakt, 22 vänster `#`, högra `D` endast rader9–12, x38 fritt i portens fyra rader.
- Auktorisation: Issue #6, R3-villkor D01–D03 och A01–A04/B01–B03/E01–E04, under MAIN V:s enda aktiva R3-uppdrag.
- Aktiv separat gren: `rom-dev/v018-r3-c02-20261116`, utgår från historisk draft PR #7-kod vid `82667dae033f70570dce903f8e1d4866528be02a`.
- `main` och draft PR #7 ändras inte av denna leverans; tidigare fryst separat VERIFICATION-baslinje `561d3baf00c6c4c4bd9bc46599a91dc693abdeba` är orörd.

## 3. Byggning och ROM

- Testmiljö: Ubuntu 24.04 GitHub Actions; `dasm 2.20.15~20201109+really2.20.14.1-2` (motor 2.20.14.1); `stella 6.7.1+dfsg-1build2`, Xvfb, ImageMagick, xdotool.
- `bash rom/v018/experiments/r3_c02/build.sh` kör `tools/generate_tables.py` som assert-testar kartgeometrin och genererar 6 × 176 playfieldbytes + 176 P1-nyckelhålsbytes. Det bygger 4096-byte 6502-ROM med riktig DASM, repeterar bankerna fyra gånger i 16 KB standard F6 och kontrollerar `dist/SHA256SUMS.txt`.
- Byte-identiskt original v0.18-baslinjebygge via `baseline_build.sh`: SHA-256 `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`.
- **Ny test-ROM SHA-256:** `991cea24f67accb2128743bba5722a87ee8cec08c00f6e39e4df1e07c3826e9c`; storlek **16 384 byte**. Varje 4KB-bank är identisk; F6 används som kompatibelt format, ingen påstådd extra hårdvaruresurs.
- Byte för genererad tabell/källgeometri och alla levererade bevis finns i separat SHA-256-manifest.

## 4. Verklig Stella – bild och grafik

**Råskärmbilder** `evidence/new_brown/stella_full.png`, `new_orange`, `new_open` och motsvarande `old_*` finns i paketet, liksom 600 verkliga bildrutecrops och TIA-traps.

- **C02 playfield-karta:** Faktisk GUI-provpixel i var och en av **176 fysiska linjer × 40 celler = 7040/7040** matchar originalets vägg/öppen-data. Alla 22 vänsterceller stängda; högra `x39` endast öppet när C02 anger D på y9–12.
- **P1-bitmap:** Orange port vid fysiska GUI-koordinater x406–421, y161–192, motsvarar ett 8-färgklockorsbrett × 32-scanlines högt överlägg vid högra porten. **256/256** jämförda bitmapbitar återges enligt assemblergenererade källdata; **233 orange** och **23 transparenta svarta** bitmapbitar bildar rund topp och avsmalnande axel.
- Verklig NTSC-färgpixel i Stella GUI: orange `(239,162,91)`, brun teknisk bas `(174,72,30)`. Det är emulatorns RGB-värden, inte en officiell slutlig färgpalett-/CRT-garanti.
- **Orange låst → öppen:** exakt **466 ändrade GUI-pixlar**, och varje ändring ligger inom portens lilla högerområde; **0** förändringar utanför x406–421/y161–192. Svart nyckelhål försvinner med porten. Inga vänsterkantspixlar ändras.
- Obs: dörrporten är ett **P1-overlay över de två högra färgklockornas sista källceller**; kartmatrisen förändras inte. Minimal logisk passageregel hålls separat från PF/P1.
- Full R3-testet visar en isolerad diagnostic, inte färdig figur-/collision-kernel för R1/R2.

## 5. Kontinuerlig NTSC-kontroll

Verifierade per-frame-data från **600 individuella Stella Debugger `Ctrl+F`-steg** och råa X11 GUI-crops `evidence/sequence_600/raw/frame_0001.png`–`frame_0600.png`:

| Mått | Utfall |
|---|---:|
| Sammanhängande frame-ID | 11–610, 600/600 |
| HUD 262 scanlines | 600/600 |
| Färgfaser identifierade i faktiska pixelvärden | Brun låst 231, orange låst 189, öppen 180 |
| Sluten vänsterkant 22/22 cellrader | 600/600 |
| Höger kant stängd i alla 18 icke-port-rader | 600/600 |
| Okända/ogranskade pixelbaserade dörrtillstånd | 0 |

Analys `tools/analyze_600.py`, utdata `R3_FRAMES_600.csv`, `R3_FRAMES_600_SUMMARY.json`. Stellas **faktiskt visade** scanlinevärde klassas via exakt GUI-pixelmall (`04f59d7f...`), inte antas från skriptets avsikt. Bildrutorna är uppmätta, men detta är *inte* i sig en komplett individuell TIA-register-/CPU-trace.

## 6. Minimal passage, inte gameplay

Logiskt portläge `$83 DOOR_OPEN`: 0 när brun/orange låst, 1 vid upplåst. Ingångspunkten tillåts endast om `DOOR_OPEN=1`, `TEST_X=39` och `TEST_Y ∈ {9,10,11,12}`. Vänster blir aldrig öppet. Stella RAM `$84–$87` i råbild på exakt frame:

| Frame | Läge | Begärd X,Y | TEST_PASS | Resultat |
|---:|---|---|---:|---|
| 150 | Upplåst | 39,10 | 1 | DEVELOPER_LOCAL_PASS |
| 151 | Upplåst | 0,10 | 0 | DEVELOPER_LOCAL_PASS |
| 152 | Upplåst | 39,8 | 0 | DEVELOPER_LOCAL_PASS |
| 153 | Upplåst | 39,13 | 0 | DEVELOPER_LOCAL_PASS |

**Låst-right negativkontroll:** Stella frame 89, `TEST_X=39`, `TEST_Y=10`, `DOOR_OPEN=0`, `TEST_PASS=0`: `evidence/new_locked_right_denied/stella_full.png`. Samma passage blir tillåten när öppen vid frame 150. Detta bevisar att endast portens status låser upp passagen. Det finns ingen rumsprogression, fullständig kollision, scoring, AI eller nyckeljakt.

## 7. CPU/TIA-uppmätt bevis och rasterbudget

Riktig **Stella Debugger 6.7.1 conditional TIA-write trap** vid `frame #90`, raster **scanline 134**, bank3 visade:

| Register | Faktisk skrivcykel | Evidens |
|---|---:|---|
| PF0 (vänster) | 7 | `evidence/register_traps/left_pf0/trace_full.png` |
| PF2 (höger) | 52 | `evidence/register_traps/right_pf2/trace_full.png` |
| GRP1 (P1 port) | 62 | `evidence/register_traps/keyhole_grp1/trace_full.png` |
| PF1 (vänster) | 15 | `evidence/register_traps/left_pf1/trace_full.png` |
| PF2 (vänster) | 22 | `evidence/register_traps/left_pf2/trace_full.png` |
| PF0 (höger) | 37 | `evidence/register_traps/right_pf0/trace_full.png` |
| PF1 (höger) | 45 | `evidence/register_traps/right_pf1/trace_full.png` |

Dessa värden visas i de **råa Stella-skärmbilderna** under `Scn Cycle`, `Scn Ln` och registerfältet `Dest`. De får därmed beskrivas som uppmätta för just denna rasterlinje. Samtliga sex PF-skrivplatser och P1-skrivplatsen (sju totalt) har fångats i samma slutliga trap-protokoll. Registerspåret är fortfarande en **kritisk-scanline-sticka**, inte en generell frame-/bankövergripande profil. Källberäknad värsta bildlinje är 74/76 CPU-cykler; detta är statiskt, inte uppmätt i Stella. Skrivdeadlines måste därför respekteras. Ungefärliga pixeldeadlines, härledda från TIA:s 3 färgklockor per CPU-cykel, redovisas i `R3_REAL_TIA_REGISTER_TIMING.csv`. Full timingacceptans av samtliga R1–R4 kan inte ärvas från detta delprov.

## 8. Utvecklingshistorik, avvikelser och stopp

1. Första nya ROM-provet: **263 scanlines** och P1 wrapping till vänster efter 14-loop för horizontal position. FAIL; kod och Actions-run 43901492277 bevaras.
2. Korrigering till 13-loop: **262 scanlines**, men porten låg ~7 colorclocks för långt in. PARTIAL; Actions-run 43902036341 bevaras.
3. Med `HMP1=$90` + HMOVE: orange port exakt på avsedd högerplats, 262 scanlines, black keyhole. LOCAL_PASS på individuella R3-bildkrav; Actions-run 43902456630.
4. 600 verkliga Stella-bildrutor och faktisk TIA-write trap; Actions-run 43903046099 och senare utökat slutligt passage-/registerbevis.

Den visuella slutbedömningen av svart nyckelhåls igenkännbarhet är **utvecklarens**; oberoende verifiering och MAIN:s designbedömning kvarstår. Ingen acceptans för R1 (sex självständigt rörliga androider), R2 (fem + nyckel) eller R4 (rörelsestress) följer av R3-resultatet. Den övergripande v0.18-grinden är alltjämt **BLOCKED / NOT ACCEPTED**.

## 9. Överlämning och källor

- GitHub-gren: [rom-dev/v018-r3-c02-20261116](https://github.com/Odourman/let-me-out/tree/rom-dev/v018-r3-c02-20261116).
- Officiell ny R3-ROM och byteidentisk historisk baslinje: `dist/LetMeOut_v018_R3_C02_F6_NTSC.bin` och `dist/historical_v018_F6.bin`.
- Reproduktion: `build.sh`, `baseline_build.sh`, `capture.sh`, `capture_600.sh`, `trace_tia.sh` och `tools/analyze_*`; full käll-/dataartefakt och övriga Python-filer medföljer paketet.
- Ny slutlig commit SHA, ZIP SHA och Drive-länk finns i `DELIVERY_POINTERS.md` när sista paketet arkiverats. MAIN ska granska dessa och sedan bestämma nästa utvecklingsuppdrag; ROM DEVELOPMENT fortsätter **inte** automatiskt med R1/R2/R4.
