# LET ME OUT! – MAIN V: R1-F5 source-only korsgranskning av HBLANK, 30 trick och R1ba

**Datum:** 2026-11-16. **Klass:** MAIN:s **forskningskomplettering**, inte ROM DEVELOPMENT II:s F5-slutrapport, inte oberoende VERIFICATION, ingen implementation, ingen ny R1-fas eller ändrad canon. **F5-order oförändrad:** [MAIN_V_TO_ROM_DEV_II_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_2026-11-16.md](MAIN_V_TO_ROM_DEV_II_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_2026-11-16.md). Full R1 är fortsatt **BLOCKED/NOT ACCEPTED**. Denna rapport är läsunderlag till F5, inte nytt mandat.

## 1. Gällande authority och källor

**Gällande MAIN V state:** [CURRENT_PROJECT_STATE_2026-11-15.md](CURRENT_PROJECT_STATE_2026-11-15.md), med R1-F4 fryst FAIL, F5 **source-only** aktiv, GRAPHICS avslutat och PR#7 draft/omerget. **Exakta originalmasker:** [design/NPC_REFERENCE_8x9_masks.json](../design/NPC_REFERENCE_8x9_masks.json), Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. **Kriterier:** [ROM_GATE_V018_ACCEPTANCE.md](ROM_GATE_V018_ACCEPTANCE.md) C01/C04, B02/E02, samt [MAIN_SIX_INDEPENDENT_X_V018](MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md). Sex enskilda NPC-X/Y får inte ersättas av fasta par utan nytt användarbeslut.

**F4-primärdata:** [fryst utvecklarrapport](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F4.md), [MAIN:s mottagning](MAIN_V_R1_F4_RECEIPT_AND_NEXT_DIAGNOSTIC_DECISION_2026-11-16.md), [F4 combined ZIP](https://drive.google.com/file/d/1ELlpy5rlXrgtW-flmKT7sUpZXKGj3LMJ/view). I F4 NUSIZ1=$01, **sex** RESP1/scanline, index0 c18 och c21 geometriskt FAIL, c19 6B och c20 F3 också x43. F2 en senare kopia c37/c38 flyttar x129↔135. F4 index1 c28, index2 c37, index3 c46, index4 c56, index5 c66. Alla 32/32 ursprungscropbilder sourcepixelkorrekta. **Ingen andra fri runtime-X**.

**Tidigare forskningskällor:** [exakt de 30 ursprungliga tricken](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), [MAIN:s 30-trick-applikationsöversikt](MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md), [HBLANK-hypotes efter F4](MAIN_V_POST_F4_RESEARCH_30_TRICKS_HBLANK_COPY_CAUSE_2026-11-16.md). Teknikatlasens 52 mönster överlappar, är inte 52 nya trick.

**Extern primär hårdvaruresurs:** Andrew Towers, *Atari 2600 TIA Hardware Notes* (2003), https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php, särskilt avsnitten `Player 0 and Player 1 Horizontal Position Counters`, `The Re-trigger Trick` och `CPU Clock to Player Pixel Table`. Atari *Stella Programmer's Guide* ger grundregler för RESP/HBLANK och NUSIZ: https://www.digitpress.com/library/techdocs/2600_Stella_Guide_12-3-79_reformatted.pdf. Källornas kretsmodeller är inte mätningar av vår ROM.

## 2. F4: HBLANK-hypotes stark, men intern signalproveniens fortfarande olöst

TIA har 228 CC per scanline, normalt 68 CC blank + 160 synliga, och positionsräknarna står stilla under HBLANK men räknar i synlig rastertid. `NUSIZ1=$01` close-kopian startar nominellt omkring 17 CC efter **motsvarande effektiva** reset, inklusive reset-/START-latch-faser. Alla fyra första F2–F4-skrivtidpunkter inträffar före normal HBLANK-slut:

| Första RESP1 CPU | Färgklocka nominellt `3*c` | Bild-crop-X observerat | Evidens |
|---:|---:|---:|---|
| c18 | 54 | **43** | F4 autentisk 16/16 |
| c19 | 57 | **43** | ursprunglig 6B/F1 |
| c20 | 60 | **43** | F3 autentisk 16/16 |
| c21 | 63 | **43** | F4 autentisk 16/16 |

Tidigare kalibrerad **observationsmodell**, `cropX = 9 + 2*(17+max(0,3*c-68))`, reproducerar samtliga befintliga x43/x75/x129/x135/x183/x243/x303-värden för just de frysta proverna. **Offset `+9` är en screenshot-kalibrering, INTE en dokumenterad TIA-latch**. Modellen är **förenlig** med HBLANK-låsning, men dess perfekta matchning bevisar inte unikt vilken kopia eller vilken signal som faktiskt utlöser index0.

**VIKTIG FÖRTYDLIGANDE KORRIGERING AV FÖREGÅENDE RESEARCH:** Det tidigare resonemanget att c23 (cc69) skulle förlora en första close-kopia därför att andra `RESP1 c28` kommer cc84, innan den idealiserade första START cc86, är **inte ett bevisat omöjlighetsresultat**. Towers beskriver **ungefär 4 CC för positionsreset**, START-decode-fördröjning/latch, samt upp till cirka 3 CC extra fördröjning eller tappad startsignal när två resetrutiner sammanfaller med dekodern. Den andra skrivningens **effektiva** counter-reset behöver därför inte redan ha tagit effekt exakt när CPU-skrivningen syns på cc84. Detta förklarar varför en strikt `write_cc < start_cc`-jämförelse är för grov även för det befintliga F4-fallet c18..21 följt av c28 (dess idealiserade första close-start omkring cc85 ändå har en faktiskt synlig mask). Inga c23/c28 eller c24/c28 ROM-prov finns i F4, och ingen får påstå deras pixelutfall utan separat faktiskt Stella-bevis.

**Konsekvens för F5:** analysera tre separata händelser i källmodellen: CPU:s `STA RESP1` **registerskrivning**, intern effekt på tvåfas-/positionsräknare, och **START-decode→latch→GRP1-utdata**. Skriv `UNKNOWN/HYPOTHESIS` för osedda internsignaler; om en race-modell förutsäger två utfall vid olika faser, avgränsa exakt vad som skulle särskilja dem.

## 3. VIKTIGT NYTT SOURCE-ONLY UNDERLAG: MAIN IV:s isolerade R1ba

Det finns redan en **separat researchbranch, inte MAIN V:s aktiva ROM DEV-spår**:
[research/main-iv-r1ba-integrated-xyz-pf-20261116](https://github.com/Odourman/let-me-out/tree/research/main-iv-r1ba-integrated-xyz-pf-20261116). [R1ba-rapport](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ba-integrated-xyz-pf-20261116/docs/MAIN_IV_R1BA_INTEGRATED_X_Y_PF_SIX_ORIGINALS_600_STELLA_2026-11-16.md), också synligt som historisk [MAIN IV checkpoint i main](MAIN_IV_CHECKPOINT_2026-11-16.md). Här **byts kopieschema**, inte originalbitmappar:

| Egenskap | F4 (misslyckad enskild index0-X) | R1ba (historisk lokal research PASS) |
|---|---|---|
| `NUSIZ1` | **`$01`**, close-kopievariant | **`$03`**, close + medium kopiemöjligheter |
| `RESP1` per kritisk 9-rads-scanline | **Sex:** c18/19/20/21, 28, 37, 46, 56, 66 | **Fyra:** typiskt c28, c40 eller 42, c56, c66 (source-only cykeluppgifter, inte full trap) |
| Sex originalmasker | Ja vid fasta X (MAIN F4 bild-PASS) | Ja vid **tre** redan förberedda X/Y-lägen enligt 600-frame CI-egenkontroll |
| Första android | x43, i tidig HBLANK-klamp | första **M/M**-kopiegrupp x75/x107 i referensläge, båda efter senare c28, med fast intern inbördes separation |
| X-frihet | F2 bara index2 c37↔38; F3/F4 extra index0 FAIL | X-grupper delvis valbara mellan **tre prekompilerade profiler** men inom stora M/M och F/F är två X ihopkopplade; små X fasta |
| Y-frihet | ingen fri sex-Y | tre SM/SF-höjdprofiler **kopplade till X-profilen**, inga fria kombinationer |
| P0/M0/PF | gul spelare, skott och bruna väggar i F4 | gul spelare, **statiskt** skott, **speglade** bruna sidoväggar; INTE höger-only dörr/R2/O1 |
| Acceptans | full R1 BLOCKED | också full R1 BLOCKED, inga oberoende sex-X/Y eller Verification |

### MAIN:s egen direkta kontroll av forskningsarkivets verkliga bytes

[Drive-original `LET_ME_OUT_MAIN_IV_R1BA_XY_PF_600_STELLA_2026-11-16.zip`](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view), original i projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u` har faktiskt:
- **3 930 298 byte**, hela ZIP SHA256 **`f8dd41e62939aa1699d80f70df0c5b5081b87441a1e2c740ff2786139908f325`**, **622 poster**, CRC `ZipFile.testzip()==None`.
- **600 verkliga `evidence_600/raw/frame_0001.png` till `frame_0600.png`**, fyra av dessa inspekterades direkt för 900×300 storlek/palettläge och totalt 602 PNG inklusive debuggerbilder.
- **Körbar 16 384-byte ROM** i arkivet `evidence_600/proof.bin` SHA256 **`41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361`**, fyra byteidentiska 4KiB-banker, byggkälla och DASM-listning finns.
- Faktisk `evidence_600/frames_600.csv` har 600 rader och sammanfattningsfilen `summary.json` redovisar 600/600 262 NTSC samt exakt sex originalmasker + P0/M0 + speglade PF; rapporterade X-profilantal A **297**, B **151**, C **152**, och inga saknade/extra vita enligt **forskarens** originalauditor.
- **MAIN har INTE** här individuellt återkört Stella eller gjort en full oberoende 600×9-scanline-pixelverifiering. Därför betecknas `600/600 mask exact` som **lokalt researchresultat** på läst ursprunglig artifacts, inte ny oberoende organisatorisk Verification.

R1ba är **inte** ett auktoriserat ersättningsbygge för F4. Det visar dock en viktig, redan fungerande alternativ renderingprincip: använd **flera NUSIZ-kopieringsmöjligheter per ompositionering** och placera *första* synliga NPC-gruppen efter HBLANK. Undvik då att förlita dig på en separat fri första HBLANK-position. **Detta byter problem från "kan x43 flyttas genom c18..21?" till "kan de fasta kopieparen frikopplas utan att originalmasker/P0/M0/PF tappas?"**

## 4. Vad 30-tricksen faktiskt tillför efter F4 + R1ba

- **#02 `GRP1` mid-scanline:** byte-identiska ursprungsmasker kan bytas mellan verkliga NUSIZ-startfönster, men varje faktiskt tänkt pixelstart måste ha korrekt latched mask. R1ba visar sex utan individuella fria X.
- **#15 NUSIZ kopior + #01 multiplex:** skilj `$01` sex manuella resetter (F4) från `$03` fyra resetter plus automatkopior (R1ba); detta är nu den praktiskt mest relevanta jämförelsen.
- **#24 cycle-exact/tables:** R1ba väljer tre **förkompilerade**, tidsidentiska 9-radskernels utanför kritisk raster; ger några gruppval men är inte fri sex-X och kostar ROM.
- **#09 VDEL** kan möjligen hjälpa GRP-latch men tidigare Venetian/VDEL källmaskfragment var negativt; ingen positiv, ny VDEL-signal i R1ba.
- **#10 HMOVE** är finjustering av P1-räknaren/gruppen, inte gratis oberoende flytt för en P1-kopia inom samma counter.
- **#03 Venetian, #04 sex-frame-flicker, #05 PF-humanoid** tidigare konkret grafiskt otillräckliga för användarens låsta 8×9-former. #07 PF, #13 score, #14 separat kernel, #19 prioritet, #27–30 ny cartridge är inte lösningar på det första fria X-hindret.
- F6-bankswitching i dessa bevisfiler är **4× samma 4KiB** och medger ingen extra TIA-kopiestart, fler RAM-byte eller CPU-klockor.

## 5. Källbaserade beslutspunkter inuti REDAN utställd F5

**F5 ska, utan att ändra sin avgränsning, redovisa två väl skilda frågor i EN rapport:**
1. **Förklara F4:s tidiga X-låsning kausalt:** F4 NUSIZ `$01`, HBLANK mot c18..21, c28, resetpipeline, startlatch och faktiskt GRP-värde på varje kopias 9 rader. F2:s c37/c38-rörlighet är referens för kopia efter HBLANK.
2. **Jämför med R1ba SOURCE ONLY:** `$03`, fyra senare resetter med förstagrupp c28, close/medium-kopior som parvis delar positionsräknare, source-konstant GRP-radplan, P0/M0/PF-data; varför tre växlade profillägen **inte** löser sex individuella fri-X/Y.

**Möjligt falsifierbart framtida test, INTE beordrat:** en minsta geometrisk jämförelse där första reset-effektivitet skjuts över HBLANK och andra reset/latch läggs så att första START kan hinna synas, med `requested_X` för två maskernas synliga start förregistrerat, samt en variant som provar att frikoppla ett NUSIZ-pardubbel i forskningskopieschema. Båda kräver **ny separat uttrycklig ROM-order**, och en lyckad 2-mask-pixelplacering är fortfarande inget sex-X/Y PASS. Om source-schemat inte kan visa hur båda X är fria under 76 CPU-cykler per rad: rapportera `F5_CAUSE_NOT_ISOLATED` eller `CAUSE_EXPLAINED_BUT_NO_INDEPENDENT_X_GEOMETRY`, föreslå arkitekturrevision, inte ett nytt blint c23..c30-svep.

**STOPP**: ingen ny ASM, DASM/Stella, CI-workflow, ROM, PR-merge, PAL/F6SC/DPC/ARM, nyckel-/HUD-/GAME OVER-implementation eller ny GRAPHICS. F5:s ordinarie ansvarsroll ROM DEVELOPMENT II får avsluta sin enda read-only-rapport på separat analysbranch; MAIN kan värdera den därefter. Inget R1-PASS eller designwaiver följer av forskningen.
