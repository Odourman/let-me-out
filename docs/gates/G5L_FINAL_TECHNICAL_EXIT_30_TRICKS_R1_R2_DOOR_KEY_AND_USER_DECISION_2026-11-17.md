# LET ME OUT! – MAIN VI G5L: slutlig G5-teknikavstämning mot ALLA 30 TRICKS, BERZERK, G4 och R1/R2/R3
**Datum:** 2026-11-17
**Teknisk status:** `G5_TECHNICAL_SOURCE_ONLY_DOSSIER_COMPLETE`.
**Formell grindstatus:** `G5_USER_RENDERING_POLICY_AND_SCOPE_DECISION_PENDING`.
**Följd:** `G6_NOT_AUTHORIZED; G0_PHYSICAL_TIMELINE_NOT_PASSED; NO_ROM; NO_CANON_CUTOVER; NO_VERIFICATION`.

## 0. Varför denna granskning nu, och vilket steg som verkligen gäller
Användaren skrev "om vi är klara med nuvarande steg fortsätt då till nästa. Om inte, så gör klart nuvarande steg. Tänk på vår plan, våra förberedelser, researchen och de 30 tricksen ... Uppdatera Google Drive och GitHub." MAIN får därför **avsluta den tekniska G5-förberedelsen och dokumentera en slutlig beslutsport**, men får INTE upphöja forskningsresultat till godkänd fysisk ROM eller anta ett användarbeslut om fiendernas Y, flimmer eller skymning. G1–G4 färdiga i *source-only/read-only*, G5 tekniskt väl utrett men designauktorisation ej avslutad. G6 kräver **separat explicit uppdragsorder** med förregistrerad G0 före kod.

Befintlig arbetsriktning som användaren uttryckligen har bestämt: Atari 2600 (NTSC/standard F6), **FEM vita fiender** (stor M, stor M, stor F, liten M, liten F), alla **fyra TOPDOWN-originalmasker 8×9**, svart bakgrund, bruna väggar, gul player, ett aktivt skott, guldnyckel och orange ENDAST högerdörr med svart genomskinligt **nyckelhål som del av samma dörrbitmap**, INTE ett särskilt spriteobjekt. Varken 10Hz flicker, 2LK-dubblad maskhöjd, automatiskt dolda fiender, begränsade Y/AI-banor eller nyckelskymningsregel O1 har godkänts som nya canon genom detta.

**Historiska bevis ska vara kvar som original:** äldre v0.18 R1 sex fiender (M,M,F,F,SM,SF) och R2 fem kvar + key används INTE som en ny PASS-bas för femfiendersmålet. En framtida ny fem-C01 och 4+key-C02 kräver separat versionsatt scope/acceptance. R3:s isolerade orange P1-door-TEST är inte R1+R2+R3-integrations-PASS.

## 1. Opartisk status över tre reella framtida produktspår
| Spår | Krav | Fysisk bevisnivå | Produktkonsekvens | G5 beslut |
|---|---|---|---|---|
| **S0: original fem med fritt numeriskt X/Y, alltid full synlighet** | Fungerar även fem NPC i ett enda 9-radersband + full player + shot + PF + ibland orange door/key | G5F/H visar källmaskbelastning 3/3/5/5/5/5/5/5/3, G5H A/B direktsekvens **79/76** för fri stress. Ingen fungerande ny generell kernel; ingen universell omöjlighetssats | Bevarar original rörelse/visuella design, **högrisk, ej produkt-GO** | Får undersökas SOURCE-ONLY utan waivers, men inte bygga större ROM på lösa antaganden |
| **S1: Berzerk-inspirerad fysisk Y-bandsseparation, fri X** | Högst en aktiv vit 8×9-robotband per fysisk scanline, behåll 9 fysiska rader per originalmask, P1 robot normalt; P1 orange door och P0 gul+vit robot under dörr | Pinned original-Berzerk-assembler använder Y-start separerade 10 logiska steg/robot, vertikal grannkontroll, sektioner och P1-robot. Vår G5J/K offline kanalbok max P0 två/P1 en över 176 syntetiska scanlines; 37/47/62c **naiva** direktkostnader, INGEN fysisk G0/Stella | **Stor reduktion av same-Y-kostnad MEN begränsar fienders Y/AI, kan hindra vertikal förföljelse/omkörning**. O1/key-sameY kan bryta schemat även då | **Högsta rimliga 2600-forskning om användaren godkänner en definierad Y-policy** |
| **S2: kontrollerad frame/scanline-multiplex/flicker när samma Y** | Behåll logiska Y/X, tillåt att inte varje fiendebitmap är helt synlig varje frame/row | Atari 2600 multisprite-metoder existerar, men tidigare vår ~10Hz sex-phase var otillräcklig; ingen 5-NPC originalmask-acceptans för visuellt flimmer | Behåller rörelse men avstår från strikt samtidig full grafiksynlighet | **Reserv endast efter användarens synliga exempel och explicit maxflicker-/occlusionpolicy** |

**Viktigt:** det är ett metodfel att beskriva S1 som "samma spel men snabbare kernel". S1 ändrar vilka **logiska fiende-Y som tillåts**, inte bara vilka register som skrivs. Berzerks 2LK får INTE följa med, eftersom våra 8×9 inte får bli 8×18 utan ett nytt visuell beslut. S0 är varken bevisat körbart eller allmänt logiskt motbevisat. S2 är ännu inte godkänt.

## 2. Ny slutlig R1/R2/R3-kombinationsstress: 10 fall
Maskinläsbar [G5L 10-falls R1/R2 P0/P1/door/key same-Y-CSV](G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv). Detta är källbaserad **logisk kanalägarräkning med P1=door i dörrbandet, annars P1 högst ett objekt**, INTE en optimal cpu-scheduler och INTE fysiskt ROM-bevis. Spelare antas alltid ha aktiv bitmap. Fler bitmap-"events" än ett per kanal kräver verklig ompositionering, vilket kan vara omöjligt på viss CC-deadline även om totalsumma <76.

| Stress | Samma rasterhöjd | Logisk min-last inkl. P0 player och P1 door där låst | P0/P1-hypotes om P1 högst en |
|---|---|---:|---|
| S01 | 1 vit, ej door | 2 bitmapobjekt | P0=1, P1=1 |
| S02 | 1 vit + låst door | 3 | P0=2 (yellow+white), P1=1 (orange) |
| S03 | guldkey + låst door | 3 | P0=2 (yellow+gold), P1=1 (orange) |
| S04 | 1 vit + gold key, ej door | 3 | P0=2, P1=1, om båda faktiskt behöver visas |
| **S05** | **1 vit + gold key + orange door** | **4** | **P0=3, P1=1** – FÖRREGISTRERAT MOTEXEMPEL mot att Y-lane löser ALL R2 |
| **S06** | **2 vita + orange door** | **4** | **P0=3, P1=1** – visar varför Y-bandbegränsningen är en hård designpremiss |
| S07 | 5 vita, ej door | 6 | P0=5, P1=1 i just denna avgränsade 1-P1-policy (andra alloteringar ännu olösta) |
| S08 | 5 vita + orange door | 7 | P0=6, P1=1 i den prövade policyn |
| S09 | 4 vita + gold key, ej door | 6 | P0=5, P1=1 i den prövade policyn |
| S10 | 4 vita + gold key + orange door | 7 | P0=6, P1=1 i den prövade policyn |

**NY rättelse till tidigare diskussion:** Nyckeln behöver INTE vara på en annan Y än door i allmänhet. Den spawnar på en dödad bärares plats och är stilla tills pickup; om bäraren dör i dörrbandet blir key+door samma-Y. En annan robot kan senare passera key på samma höjd: R2 behöver pröva detta och får inte påstå "guldkey får aldrig behöva en egen grafikhändelse". `docs/KEY_OCCLUSION_LOGIC_V015.md` klassar **O1 som preliminär MAIN-rekommendation, inte godkänt canonbeslut**. O1 får inte tyst användas för att dölja key när den **inte faktiskt är pixeltäckt**. 5 NPC i R1 och 4+key i tänkt R2 löser inte den grafiska extrem-lastens storlek om de alla är same-Y.

## 3. De 30 ursprungliga tricksen mot G5:s aktuella fysiska flaskhals
Nedan granskas exakt den fulla ursprungliga listan 01–30 ur [RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md](../RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), inte 30 nyuppfunna eller 30 lösningar som man redan bevisat fungerar. Kompletterande [korsobjektsmatris](../MAIN_VI_30_TRICKS_CROSS_OBJECT_REASSESSMENT_2026-11-17.md).

| # | Trick | Konkret roll i G5 S0/S1/S2 | Stoppspärr eller falsk genväg |
|---:|---|---|---|
| 01 | Sprite Multiplexing | S1 återanvänder P1 på skilda Y; under dörrbyte används P0 | Löser inte 5 fri-same-Y med ett register |
| 02 | Mid-scanline GRP rewriting | S0-kärnproblemet; S1 P0 under dörr där player+white | Fysiskt GRP/START-latch krävs, äldre F11 G0 FAIL |
| 03 | Venetian Blinds | Endast reserv för key/dörr eller frivillig visuell policy | Tappar originalrader; key och door är inte garanterat samma/different Y |
| 04 | Sprite Flickering | S2 kontroll­spår med synlig testvideo | Tidigare sex-phase ~10Hz ej acceptansbar utan user-waiver |
| 05 | Dynamic PF Sprites | PF kan rita grov nyckel/dörr/markering eller x0-vägg | PF är 4 CC/bit, ger inte 8bitars humanoid |
| 06 | Mid-frame Sprite Resizing | Eventuell framtida tillämpning dörr/HUD | Ej allmän färg-/kanalbudget |
| 07 | Asymmetric PF | R3 original högeröppning; S1 spegla + Ball(x0) | Underliggande brun PF får inte fylla svart keyhole |
| 08 | Two-Line Kernel | Berzerk historisk 2LK för bytes/cykler | Dubblar fysisk höjd för 8×9 om ospecificerat |
| 09 | VDEL/delayed graphics | S1 fasbyte och forberedelse per band | Inte ett tredje fritt sprite-X |
| 10 | HMOVE | S1 förpositionering vid Y-band/gräns | Inte oberoende X-counter per kopia |
| 11 | Late HMOVE | Kan finjustera först efter G0/physically allowed | HMOVE artifacts/late deadline |
| 12 | Raster color changes | White/Yellow P0 under door, orange P1, gold key vid Y | M0 delar `COLUP0` och Key kan hamna nära player/shot |
| 13 | 48pixel score kernel | Separat HUD-band, ingen R1-resurskonflikt om zonat | R1+key fortfarande olöst |
| 14 | Multiple display kernels | Styckar Y i room, door, HUD, key | Samma scanline konflikt försvinner inte utan ägarplan |
| 15 | NUSIZ copies | Två identiska stora M på vissa X-avstånd | Fasta 16/32/64 CC räcker inte fria individuella X |
| 16 | REFP0/1 | Horisontell spegling silhuett vid behov | Reparerar inte felvänd vertikal R1ba TOPDOWN |
| 17 | Missile/Ball reuse | **Ball=brun x0-vägg** i door-y, M0 enda skott | BL upptagen under door, delar COLUPF; M0 delar P0-color |
| 18 | PF SCORE mode | HUD endast i separat y-band | Gör väggar gul/orange i spelrum om aktiverat där |
| 19 | PF priority switching | Rums-/android-/nyckel-occlusion-prover | PF/BL som väggar byter collision/overdraw-känsla |
| 20 | Hardware collision latches | Kombinera P0/P1/M0/PF/BL med logisk per-NPC hit | BL-väggens collision är inte automatisk PF-kollision |
| 21 | RIOT timer | stabil 262 scanline/WSYNC och VBLANK budget | Timer ger inte fler än 76 CPU/line |
| 22 | Stack/RAM mirroring | Eventlist-storage vid 128B RIOT | Kan orsaka stack/underrun; ingen RAM-magi |
| 23 | Undocumented opcodes | Ej rekommenderade i fysikpreflight | Kompatibilitetsrisk, ej påstådd +3 cycles |
| 24 | Precompute/Exact Tables | Mest lovande: prepare Y-sorted events, X coarse/fine, PF masks i blanking | 128B/4KB per aktiv bank, event updates / scanline måste bevisas |
| 25 | Stack TIA writes | Eventuell specialistoptimering efter fysisk G0 | Inte en ny bildresurs |
| 26 | Timing horizontal scroll | Senare polering ej statiska rum | Ej relevant G5-beslut |
| 27 | SCABS bankswitch | EJ standard F6, ur scope | Kräver annan cartridge |
| 28 | Superchip/extra RAM | EJ standard F6, ur scope | Mer RAM betyder inte fler TIA-kanaler |
| 29 | DPC processor | EJ standard F6, ur scope | Hårdvaruändring kräver nytt userbeslut |
| 30 | DPC+/CDF/ARM | EJ standard F6, ur scope | ARM/coprocessor hjälper logic, inte två P1-hårdvaruportar per pixel |

**Prioriterad kombination inom standard-F6 för en senare explicit minimal testorder:** `01+02+07+09+10+12+14+17+20+21+24`; #08 ENDAST om användaren godkänner höjdpolicy, #03/04/19 ENDAST efter exakt förhandsgodkänd visuell occlusion/flicker. Ingen av punkterna gör S0 automatiskt genomförbar.

## 4. Nästa tekniska test som redan är förberett, men inte auktoriserat
G5:s testplan måste härifrån skilja på **fysikprimitive** och **spelbar version**:
1. **H4-ONE/G6-minimal P0 gul+vit X-korsning**: spelares numeriska X passerar en originalvit 8×9 NPC, inklusive omvänd X-ordning; ett M0 på **samma Y**; faktisk brown PF, 76 CPU och korrekt COLUP0/mask/färg vid pixelclock, både rapporterade och holdout X. Även om P0+M0 fungerar, är det ingen full R1.
2. **S1-lanemekanism separat framtida test**: 1 vit P1 utanför door; under dörr används P0 player+white och P1 orange mask+black negative hole; Ball x0 mot svart bakgrund, exakt en högeröppning. NPC och door 9 samtidiga 8×9-rader måste provas; O1/key var för sig i andra test.
3. **R2-key stress**: key på samma Y som door och robot, både verklig skymning och endast Y-överlapp utan pixel-överlapp; key skall återkomma på exakt samma logiska X/Y, ev. väntande O1 användarval före rendering. Skott-/kollisionregler separat.
4. **S0/no-waiver alternativ**: preflight med 5 fria numeriska X/Y och 1 aktiv M0, maskrad 6 samt door/Y och key stress. Om G0 kan inte ges för något sammanhängande START/färgplan är detta fortfarande `HOLD`, inte fler falska 600/600-klipp.

**Fysisk G0 PRE-build kräver:** komplett 6507 opcode-lista per värsta rasterrad, TIA register write c+colorclock/START, numeriska RAM-X/Y och Y-sortering, originalmaskrader 0–8, M0 same-Y och P0-color, PF+BL/collision, 128B stack/RAM, aktiv F6-bank under 4096 byte, frysta test-och-kontrollscener, stopp vid första fail. Ingen .asm/.bin/Stella eller oberoende VERIFICATION får bokföras från denna källdokumentation.

## 5. G5 final EXIT-rapport och enda kvarvarande beslut
- **Färdigställt inom ramen för MAIN:s read-only/source-only uppdrag:** status & authority recheck; exakt de 30/30 tricken bedömda mot den nya femfiendersversionen; jämförelse S0/S1/S2 med extern original-Berzerk-källa; 10-falls R1/R2/R3 key/door/same-Y matris; falsifierbara framtida microtest; korrekt skillnad mellan offline PASS och verklig Stella/G0.
- **Inte uppnått och får inte hävdas:** G5 bindande acceptans-/designbeslut, 5-NPC ROM eller source G0 pass, nyckelrendering vid O1, fysisk Ball x0, TIA owner colorclock timing, 600 fysiska frames med originalmasker.
- **EXAKT återstående USER-ägt G5-val:** Ska fem fiender fortsatt få ha **helt oberoende Y och kunna trängas på samma nio fysiska rasterrader**, eller får deras **ömsesidiga Y-rörelse begränsas ungefär Berzerk-likt** för att hålla högst en aktiv vit robotband per rasterlinje (utan att reducera fem logiska fiender eller originalmasker)? Om fri Y kvarstår behövs en *ännu ej hittad* S0-kernel eller ett separat framtida godkännande av flimmer. Om Y-arbitrering godkänns måste dessutom exakta AI-rörelseregler, passager, key-skymning och all visuell acceptans separat versionssättas, eftersom Y-lane skulle ändra gameplay.
- **MAIN:s rekommendation för en Atari 2600-produktion:** S1 som **conditional first candidate**, INTE som beslut. Den har en faktisk 1982 originalkällan som inspiration och betydligt mindre ägarlast än S0, men med märkbar spel-/designkostnad och fortfarande P0/M0/key/door risk. För en spelare som prioriterar full vertikal rörelse är S0 fortsatt mål, men tekniken är ej klar för G6-produktionsstart.
- **Stopp:** G5 `TECHNICAL_COMPLETE_FORMAL_PENDING`, G6 `NOT_AUTHORIZED`, G7–G10 `BLOCKED`. Avsluta **inte** denna granskning med fler självupprepande 79/76-cykeltabeller; enda meningsfulla nästa steg är det **verkliga användarvalet** eller en *helt ny konkret* extern kernelarkitektur som source-only kan falsifiera S0:s blockering.

## 5A. Fullständig arkivkopia i officiell Google Drive
- [Google Drive – G5L hela slutliga G5-teknikrapporten med 30/30-trick, 10-case-CSV och exakt öppen användarfråga](https://docs.google.com/document/d/1zbusyasMrLlO4zIp3iq8iplr8cvjvlAvbcgkDATOi38/edit), native Google Doc som skapades i den officiella projektmappen `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`, lästes tillbaka och kontrollträffade fullständig trickpost 30, scen S05, O1-beslutsgräns, G5 pending/G6 spärr och CSV:s fullständiga rubriker. Denna GitHub-fil är versionsstyrt källoriginal; Drive är läsbar kopia.
- [GitHub full original-CSV med samtliga 10 testscenarier](G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv). Inga ROM-/designfiler har ändrats.

## 6. Käll- och registermanifest
1. [Ten-Gate-ledningsplan G1–G10](../MAIN_VI_DEEP_REASSESSMENT_30_TRICKS_FEASIBILITY_AND_TEN_GATES_2026-11-17.md), [G1–G10 detailed playbook](../MAIN_VI_G1_G10_CONTINGENCY_PLAYBOOK_A_B_C_2026-11-17.md), [G5 boundary](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md).
2. [Originals 30 techniques](../RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), [all30 object cross-eval](../MAIN_VI_30_TRICKS_CROSS_OBJECT_REASSESSMENT_2026-11-17.md).
3. [G5H mask/X worst-case](G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md), [G5G Ball door wall](G5G_BALL_LEFT_WALL_AND_FIVE_NPC_OPCODE_CENSUS_SOURCE_ONLY_2026-11-17.md), [G5J true Berzerk original kernel](G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md), [G5K 176-raster door/key owner](G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md).
4. [v0.13 key hole sprite target](../KEY_AND_DOOR_VISUAL_TARGET_V013.md), [v0.15 O1 expressly NOT canon](../KEY_OCCLUSION_LOGIC_V015.md), [old R1/R2/R3 acceptance](../ROM_GATE_V018_ACCEPTANCE.md), [R3 pinned isolated source](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/r3_door.asm).
5. [Extern original Berzerk assembler, pinned](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm); [TIA original online Stella guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html); [Three-stream versatile kernel 2025](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html).
6. G5L 10-case source-only CSV [direkt i GitHub](G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv).

**Arkivprincip:** GitHub-väg med blob/SHA som versionsoriginal; fulltextkopian i officiella Drive och statusregister pekar mot detta. Inga gamla source-/ROM-binarier raderas eller omskrivs.
