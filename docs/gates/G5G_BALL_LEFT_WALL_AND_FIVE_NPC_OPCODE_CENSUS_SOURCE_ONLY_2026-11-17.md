# LET ME OUT! – MAIN VI G5G: BALL SOM VÄNSTER DÖRRVÄGG + EXPLICIT 6507-INSTRUKTIONSBUDGET
**Datum:** 2026-11-17. **Status:** `G5G_SOURCE_ONLY_OFFLINE_PF_BALL_GEOMETRY_PASS_NAIVE_6507_EVENT_MODELS_FAIL_OR_INCOMPLETE_G0_NOT_PASSED`.
**Typ:** fortsatt teknisk MAIN-förstudie enligt användarens "Ok, följ dina egna rekommendationer och fortsätt" efter G5F. **Ingen ny .asm/.bin, ingen Stella, ingen G6/F12-order och ingen ändring av historiska R1/R2-acceptanskriterier/canon.** Fysisk 6507/TIA-schema med verkliga START-/GRP-/BL-/WSYNC-deadlines är **INTE uppnått**; tabellen nedan är en kontrollerad **instruktionskostnadsinventering för direktsekvensen**, inte en fungerande tidsplan. ROM DEVELOPMENT III får inte tolka detta som implementationsauktorisation.

## 1. Nytt tekniskt fynd: TIA Ball ersätter vänstra PF0-pixeln vid den högra dörren
Det tidigare G5F-förslaget utgick från att `CTRLPF.REF=1` speglar väggen och att man, för att hålla vänster x0 stängd medan x39 är svart/öppen, måste skriva **vänster-PF0 på varje ny scanline och ny PF0 på höger del av samma scanline**. Det kostar tid även när övrig PF-data inte ändras.

**Starkare, källgrundad konstruktionshypotes: använd hårdvarans BL (Ball) för en 4-färgklockors brun vertikal vägg vid x0 under dörrbandet.**
- Vanliga kartrader: `CTRLPF` speglat (REF=1), `PF0` har aktiverad yttersta vänsterpixel och därmed samma högerpixel; `ENABL=0`.
- Fyra dörr-celler y9–12 (32 scanlines vid historisk C02 8 rasterlinjer/cell): `PF0=0` vilket släcker både vänster x0 och höger x39 (de övriga tre PF0-cellerna är också tomma). `ENABL=2` aktiverar Ball, redan förpositionerad vid vänster synliga CC0 och bredd 4 CC; `COLUPF` ger samma bruna färg som väggarna. Därmed blir **vänster x0 brun och stängd** genom BL, medan **höger x39 lämnas svart/öppen** genom PF:s frånvaro. Resten av PF1/PF2 förblir symmetriskt. Den gamla P1-bitmapens **orange port med svart transparent nyckelhål** ligger på x38–39 och kräver INGEN separat nyckelhålssprite.
- `COLUBK=svart`; `COLUPF=brun`; `COLUP1=orange` endast för P1-porten på rätt färgklockor; gula P0/white NPC måste hållas skilda i tidsplan.
- `CTRLPF=$21` är en **teoretisk kontrollkod** för REF=1 (D0) + Ball bredd 4 CC (D5,D4=1,0), SCORE=0, PFP=0. Detta måste **mätas/verifieras i riktig Stella och helst originalhårdvara** före godkännande; `BL` måste förpositioneras till **exakt** vänster x0 och `VDELBL=0` (ingen enlinjesförskjutning). Ingen Ball-metod har testats i ROM.
- Ball tar **inte** en P0- eller P1-kanal och färgen är densamma som PF. **Men BL är upptagen** under dörrens rasterband och är alltså inte samtidigt en extra guldnyckel; dess **kollisionslatch** är inte identisk med en PF-kollision. Skulle fiender/skott/nyckel hamna där måste logik och resurskontrakt hantera det separat.

### 1.1 Faktiskt offline-test mot samtliga fyra originalrum: 3520/3520
**Primär data:** `design/PLANERADE_RUMSKARTOR_V011.json`, A01/B01/C02/D01, 40 celler × 22 rader × 4 rum = **3520** celler.

Jag har med direkt källfilsextraktion modellerat varje cell på följande sätt (inte via omritad handkarta):
```text
for each room, y:
  left_20 = grid[y][0..19] transformed "#":1, ".":0
  if y in 9..12: left_20[x=0] = 0    // PF0 bit D4 cleared on both halves
  PF40 = left_20 + reverse(left_20)    // CTRLPF REF=1
  BALL40[x=0] = 1 if y in 9..12 else 0  // width 4 color clocks
  visible_brown = PF40 OR BALL40
  required_brown = (grid[y][x] == "#")   // "D" is no PF: orange P1 overlay when locked
  assert visible_brown == required_brown for x in 0..39
```
**Resultat:** A 880/880, B 880/880, C 880/880, D 880/880, **TOTAL 3520/3520 matchande bruna/vägg- och öppna/kartceller**, 0 mismatch. Detta är exakt **bitmodell för PF+BL**, **inte** bevis på Ball:s fysiska x/4CC, P1:s orange genomskinlighet, timings, skott/NPC, låst passage, 600 frames eller oberoende verifiering. `D` tolkas korrekt som **ingen PF-vägg bakom P1-porten**. Logiskt är dörren ändå låst tills nyckeln används.

### 1.2 Instruktioner endast vid dörrbandets gränser – hypotetisk minimal delrutin
Följande är **opcode-/cykelräkning för en liten registerövergång**, inte en fysisk fullscanline-kernel. TIA-register ligger i zero page. `CTRLPF=$21`, `COLUPF` brown, Ball x0, `VDELBL=0` och `COLUBK` black måste redan vara satta i säker tidigare fas.

| Övergång | Opcode-typ | 6507-cykler | Kumulativt sedan senaste WSYNC (om rutinen börjar c0) |
|---|---|---:|---:|
| Första dörr-rasterrad | `LDA #$00` | 2 | 2 |
|  | `STA PF0` | 3 | 5 |
|  | `LDA #$02` | 2 | 7 |
|  | `STA ENABL` | 3 | **10** |
| Efter sista dörr-rasterrad, inför vanlig väggrad | `LDA #$10` | 2 | 2 |
|  | `STA PF0` | 3 | 5 |
|  | `LDA #$00` | 2 | 7 |
|  | `STA ENABL` | 3 | **10** |

Det här **lägger 10 c på respektive gränsrad**, i stället för två PF0 color/kartbyteskrivningar (ca 10 c) på **var och en av 32 dörrrader** i den enklare PF0-only-planen. Potentiellt ca 30 × 10 = **300 c per 32-linjers dörrband** sparade av just dessa datawrites, i ett enkelt idealiserat jämförelseschema; detta inkluderar **INTE** extra BL-positionering eller faktisk kernelfördelning. Jämförelsen antar korrekt PF0-restaurering på varje tidigare door-rad. NUSIZ och registerfärg påverkas inte av Ball i denna hypotes.

**Stoppspärr:** Door-entry-raden kan även innehålla en faktisk ny PF1/PF2-mönsterändring, aktivt skott samt fem-NPC same-Y; gränskostnaderna måste kombineras med **den dyraste** film-/radräknaren, inte flyttas till fristående test för att skapa falskt PASS.

## 2. Reproducerbar instruk­tionskostnad: konkret 6507-direktsekvens, A/B/C
**Primär offentlig CPU-referens:** NMOS 6502/6507 `LDA #imm=2c`, `STA TIA zp=3c`, `STA WSYNC zp=3c`. Extra `LDA ROM table,Y=4–5c`, `LDA RAM zp=3c`, grenar/sort/positionsfaser har **inte** räknats in. Ett objekt som skrivs direkt på en rasterrad enligt **en illustrativ minimal händelsegrupp** `LDA #bitmap; STA GRPx; STA RESPx` kostar **2+3+3 = 8 cykler**. OBS: detta innebär **inte** att objektet fysikaliskt börjar ritas vid önskad X; `RESPx`-registerskrivningar och TIA START kräver egna fysiska rasterdeadlines, och vissa NUSIZ-copyfönster är avgörande. Vi har tidigare G0 F11 FAIL med färre numeriskt fria P1-objekt.

**Färglogik per STADIG samma-Y dörr-rad, upprepat för varje scanline:**
- A: P0 ritar gul spelare och en vit NPC, så övergången från föregående rads avslut till nästa rads start och mellan två aktörer ger **normalt två `COLUP0`-färgskrivningar**, i den raka per-linjens modellen; á `LDA #imm`2 + `STA COLUP0`3 = 5c, totalt 10c.
- P1 ritar fyra vita NPC och en orange dörr. Mellan dörr-orange sist på raden och första white NPC nästa rad, samt white→orange på dörrens X, krävs **två `COLUP1`-färgskrivningar à 5c**, totalt 10c. Detta förutsätter en color order W...W,O och korrekt faktisk färgklocka; om NPC korsar/överlappas kan det bli värre.
- B: P0 ritar gul spelare + två vita NPC, P1 tre vita + orange. I en upprepad vertikal rad är antalet **minst två** P0-färgväxlingar i den tvåfärgade cykliska sekvensen, utom när separata renderingsfönster är fysiskt planerade på annat sätt. En viss X-sort kan kräva komplicerad timing men vår förenklade modell tar 10c.
- C: P0 enbart gul player, P1 fem vita NPC + orange dörr. Färgbudgeten är lägre men P1 måste då avbilda **sex olika 8-bitars bitmaphändelser samma Y** med fristående numeriska X, långt förbi vad F11 ens klarade source-only.

**Testbudgeterna finns maskinläsbart i** [G5G cycle census CSV](G5G_DIRECT_EVENT_CPU_CYCLE_CENSUS_2026-11-17.csv). Det är dessa direkta instruktioner, med metadata och uttryckliga exklusioner, som ger följande totalsummor:

| Scenario | Grafikhändelser P0+P1 inkl. orange door | COLUP0 (c) | COLUP1 (c) | PF/BL (c) | WSYNC (c) | TOT (c) | Enkel direktsekvens |
|---|---:|---:|---:|---:|---:|---:|---|
| A: fem NPC + gul player, normal konstant speglad PF | 6 × 8 = 48 c | 10 | 0 | 0 | 3 | **61/76** | 15 c aritmetisk marginal, EJ fysikpass |
| A: samma under en väggradbyte 3 nya PF0/PF1/PF2 | 48 c | 10 | 0 | 15 | 3 | **76/76** | 0 c för dynamik, gren, M0 etc.; EJ fysikpass |
| A: fem NPC + player + orange P1-door med PF0-toggle varje rad | 7 × 8 = 56 c | 10 | 10 | 10 | 3 | **89/76** | **FAIL** för just denna naiva sekvens |
| **A: samma door med Ball-left-wall och PF latched** | 56 c | 10 | 10 | 0 | 3 | **79/76** | **FAIL** för naiv sekvens, sparar 10c mot PF0-only |
| A: Ball-door ingångsraden (PF0 clear+ENABL on) | 56 c | 10 | 10 | 10 | 3 | **89/76** | **FAIL** direktsekvens, gränsrader svårare |
| B: P0=spelare+2 white, P1=3 white+door, BL left | 56 c | 10 | 10 | 0 | 3 | **79/76** | **FAIL** direktsekvens, nya tre-RESP0/GRP0-krav |
| C: P0 endast spelare, P1=5 white+door, BL left | 56 c | 0 | 10 | 0 | 3 | **69/76** | 7 c teoretisk marginal; **6 fri P1 X är inte fysikbevisad** |

Denna SUMMA är **inte ett universellt omöjlighetsbevis** för Ball-lösningen eller ett helt Atari 2600-spel: automatkopior (NUSIZ) med verkligt kompatibla avstånd, pre-positioned aktörer, effektivare GRP-latchning, registernyttjande och förberäknade event kan korta sekvensen. **Men dessa är ännu inte visade med fritt numeriskt X/Y och maskrättvändhet.** Det vore fel att sätta G0 PASS genom att bara subtrahera 3 cykler utan en verklig körbar/statiskt listad instruk­tionsplan och START-pixelbevis.

### 2.1 Exakta återstående fysiska gränser – som måste lösas INNAN ny ROM
1. **Ball x0:** Exakt `RESBL`/HMBL/HMOVE-start och 4CC bredd, ingen enradsskugga, exakt 32 dörrlinjer och inga andra ballpixels. Fritt käll-/pixelbevis saknas.
2. **Per-linje ompositionering:** kan en av P0/P1-startpositionerna verkligen hållas redan på plats mellan raderna, eller kan NUSIZ autokopior spara fysiskt korrekt per-linje-STA RESP? Om detta inte kan demonstreras med **nya numeriska RAM-X** är 79c-läget ändå inte löst.
3. **Färg och skott:** P0 gul/white delar COLUP0 med M0; en M0-projektil vid en vit P0-pixel kan inte samtidigt ha annan färg. P1 vit/orange måste ha rätt CC under samma Y. Det krävs exakt EN missile och fungerande originalmasker även vid motexempel, inte M0 på en tidigare rad som i R1g.
4. **Tabellkostnad:** de **8c/figur** är ett **optimistiskt direktmode** med konstant immediate maskbyte, inte 5 fritt rörliga sprites från separata RAM koordinater och per-Y bitmapmask. RAM- eller indexed-ROM-laddningar, grenar, event sort och masktabell livslängd är inte inkluderade. F6:s 4KB aktiv bank samt RIOT 128B ska verifieras när exakt mekanism finns.
5. **Door P1 vs white P1:** orange vid far höger måste samsas med white NPC som får röra sig nära samma x; samtidigt samma pixel med P1 kan inte vara två separata färger med ett enda `COLUP1`. Denna konflikt kvarstår även om Ball ersätter vänsterväggen.
6. **BL-reservation:** under dörrbandet är BL upptaget som vänstervägg. En guldnyckel kan enligt befintlig key-drop- och occlusion-logik hamna på vilken logisk fallplats som helst; **user's informella "nyckel och dörr inte på samma rad" får inte antas som universellt förbud** om inte senare godkänd canon säger det. Om nyckeln behöver samma Y finns inget gratis BL, och key sprite/guld färg måste fortfarande planeras.

## 3. Rätt status och beslut
**Source-audit av grafikgeometri: PASS i strikt 3520/3520-cellsbitmodell.**
**Direkt-sekvens 6507-budge­t för A/B door+BL: FAIL (79/76 på stadig rad, 89/76 på gränsrad i den angivna förenklade modellen).**
**Fysisk integrerad G0 med samtliga TIA registerinstruktioner och dynamisk X/Y: NOT PASSED / INCOMPLETE.**
**Stella/ROM/independent VERIFICATION: NOT RUN.**

**Rekommendation MAIN VI:** Den nya `REF + BL vänster 4CC + PF0=0 i dörrband + svart BK + gamla orange P1 door`-lösningen är en **starkare SOURCE-ONLY-arkitekturkandidat** än PF0-toggle på var och en av 32 rader, just för att det bevarar alla fyra faktiska rum utan att byta grafiskt designmål. **Nästa steg bör vara en enda separat source-only fysisk START/GRP-/Ball-x0-tidslinje** som antingen visar verklig tidsvinst genom att ta bort något av de 7 `RESP/GRP`-händelseparen per rad, eller tydligt slår fast stoppspärr. Villkorlig framtida faktisk ROM-beställning får bara komma efter explicit användarbeslut och G0 med verkliga opcodes/deadlines; inte från denna analys.

## 3A. Google Drive-kopia och versionsstyrd CSV
- [Officiell Drive: hela G5G-rapporten plus CSV-bilagan](https://docs.google.com/document/d/14sNkAi8gdLqz2wo6OtR9jrpTggrcXB0cv-BCO3onaWY/edit), lagrad i projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`. Native-dokumentet skapades, flyttades och lästes tillbaka. 3520/3520, 79/76, 89/76, status och full CSV-bilaga verifierades.
- [Cykel-CSV i GitHub](G5G_DIRECT_EVENT_CPU_CYCLE_CENSUS_2026-11-17.csv) är maskinläsbar kontroll av denna direktsekvenskostnad, med alla antaganden explicit.

## 4. Beviskällor / versionskontroll
- [G5F tidigare femfiendersförstudie](G5F_FIVE_ANDROID_REFLECTED_PF_DOOR_SOURCE_ONLY_ARCHITECTURE_2026-11-17.md), originalkartor och NPC-masker på `main`.
- [R3 isolated original code, pinned commit, R3 JSON all bytes](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/r3_door.asm): faktiskt `CTRLPF=0`, **sex PF-table writes per rasterrad** samt P1 `GRP1` door; full R3 är ej ny kombination.
- [Stella Programmer's Guide HTML](https://www.atariage.com/2600/programming/2600_101/docs/stella.html), [AtariAge PF-bitmap timing source](https://forums.atariage.com/topic/29205-session-17-asymmetrical-playfields-part-1/).
- [Stella Guide: ball BL shares PF color, ENABL, width 1/2/4/8, vertical delay](https://alienbill.com/2600/101/docs/stella.html), [Atari 2600 code reference CTRLPF=$21 for 4CC Ball](https://www.randomterrain.com/bb_files/atari-2600-memories-batari-basic-commands.html).
- [NMOS 6502 explicit opcode instruction timing](https://www.retroisle.com/atari/vcs/Technical/Firmware/cyclecountingon6502.php), [TIA player reset/copy counter](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php).
- [G3 cycle ledger](G3_CYCLE_AND_F6_BYTE_LEDGER_2026-11-17.csv), [G3 clock deadlines](G3_COLOR_CLOCK_DEADLINES_2026-11-17.csv), [G4 preregistered hypothesis](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [v0.18 acceptance unchanged](../ROM_GATE_V018_ACCEPTANCE.md).

**Scope-/beslutsgräns:** Ingen ändring av 6-NPC historiska testcanon C01/C02, slutlig 5-NPC cutover kräver spårbart användarbeslut och reviderade kriterier. Svart bakgrund och enmaskigt nyckelhål bevaras. Detta är inte produktions- eller G6-implementation, ingen PR-merge, ingen ändring av spelets övriga regler, och en annan VERIFICATION II måste godkänna framtida faktiska ROM.
