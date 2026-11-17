# LET ME OUT! – 30 ATARI-TRICK / PROJECT SOURCES V5

**G5AG – senare faktisk status:** LM-D21/G5AD gav ett enda avgränsat TIA-kalibreringsuppdrag men slutade `NO_BUILD_INSTRUMENTATION_BLOCKER`; de sex C0–C4/N1-proven kördes inte. LM-D22/G5AF tillät endast reparation och två Actions-kontroller på redan fryst F9. ROM DEVELOPMENT III levererade `G5AF_INSTRUMENTATION_READY_BOUNDED` (första Actions-rundan FAIL, andra SUCCESS); MAIN VIII har källgranskat och mottagit som utvecklarinstrumentering, inte oberoende verification. [Specialist-original](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md), [Issue #14 stängt som avgränsat instrumenteringsarbete](https://github.com/Odourman/let-me-out/issues/14). `G5Z_G0=INCONCLUSIVE_NO_ROM`, `G5_FORMAL_OPEN` och alla begränsningar för ny ROM, H4/G1/G6/F12/S05/fem-NPC/Verification/merge kvarstår. Inget nytt tekniskt prov får härledas från detta källpaket.

**G5AG-TIA-gräns:** Den verkliga F9-instrumenteringen har nu två läsbara Stella-debuggerstopp (PC `$F1F0`, `_sCycles=21` och PC `$F1F8`, `_sCycles=32`, båda frame 136/scanline 123) och hashade nativa 320×228-bilder enligt utvecklarens rå-CSV; MAIN VIII kontrollerade GitHub-källor och Actions-success men utförde inte egen fristående råartefaktshashning eller emulering. **Inte** en RESP/GRP/NUSIZ/ENAM0-colorclock-PASS, inte sex genomförda G5AD-kalibreringsfall. [G5AF-data](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/G5AF_INSTRUMENTATION_EVIDENCE.csv).

> **V5-supersession:** Alla daterade formuleringar nedan från V4 som säger att G5AC ännu enbart är ett förslag, att G5AF är `NOT_YET_RUN`, att inga F9-körningar gjorts, eller att MAIN VII fortfarande leder är *historisk V4-status*. De upphäver inte LM-D21/LM-D22 och G5AG. Gamla negativa resultat behålls oförändrade. Hämta gällande originalkällor live.



**LÄSANVISNING V5:** Tidigare versioners källangivelser, gamla GitHub Issues, initiala ROM-beställningar och äldre framtidsförslag är historiska vid sina respektive tidpunkter. Högre auktoritet och senare uttryckliga användarbeslut gäller inom exakt beslutat ämne. Ingen source-only-status är fysisk Atari/Stella-verifiering. Detta källpaket ger ingen ny teknisk auktorisation.

**Klass:** rådgivande forskningssyntes, inte ROM-kod eller fastställt spelbeslut. **V4-status 2026-11-17, efter G5AA:** den enda beställda H4-ONE G0-källanalysen har genomförts och avslutats som **`G0_INCONCLUSIVE_NO_ROM`**, inte tekniskt PASS eller generellt NO-GO. [G5AA senaste mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md). G5 fortsatt OPEN, ny G1/G6/ROM ej auktoriserad. Alla 30 teknikrader nedan är **möjligheter/forskning**, inte etablerad gemensam fem-NPC-renderer.

**Aktuell teknisk status och arbetskö:** [GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) · [Drive](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit). Förberedda G5AC-kalibreringsfall är beslutsunderlag, ännu ingen kodorder.

**Verifiera primärkälla vid användning:** [numrerade 30 trick](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), [G5L:s fulla jämförelse](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md), [55-sidig historisk avhandling](https://drive.google.com/file/d/1IHKg63PZGAYoi3fdJdwmOYsomDxumlIv/view). **30 trick, 52 teknikmönster och 67 riskpunkter överlappar**; räkna dem inte som 149 oberoende lösningar. Berzerks [historiska assembler](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm) använder bl.a. vertikal fördelning av robotar; den bevisar inte fem fria samtidiga 8×9-masker på samma Y.

## Alla trettio tekniker – utan att överdriva bevisvärdet

| Nr | Trick | Relevant roll i femfiendersversionen | Gräns |
|---:|---|---|---|
| 01 | Sprite Multiplexing | P1 återanvänds mellan Y-band | Ingen lösning för fem fulla same-Y-sprites ensam |
| 02 | Mid-scanline GRP Rewriting | Byt bitmaps mellan möjliga startfönster | `GRP/RESP` måste klara exakta START-deadlines |
| 03 | Venetian Blinds | Reserv vid medvetet glesare rastergrafik | 9 fysiska originalrader får inte försvinna tyst |
| 04 | Sprite Flickering | Separat reserv för tidsdelning | Lite tillfälligt flimmer accepterat kvalitativt; ingen godkänd Hz-/andelsgräns; äldre ~10 Hz ej PASS |
| 05 | Dynamic Playfield Sprites | Grova figurer/markörer och geometri | PF är 4 colorclocks per bit, inte 8-bitars humanoid |
| 06 | Mid-frame Sprite Resizing | Eventuella små sekundära effekter | Skapar inte fler individuella objekt |
| 07 | Asymmetric Playfield | Högerdörr och brun vänstervägg | PF-krav bakom svart negativt nyckelhål |
| 08 | Two-Line Kernel | Berzerks förebild för större rastertid | Ändrar fysisk 8×9-maskhöjd om okritiskt överförd |
| 09 | VDEL / Delayed Graphics | Förbered GRP-masker mellan linjer | Ingen extra X-counter eller fritt objekt |
| 10 | HMOVE Fine Positioning | Korrekt X-finskiftning | Kräver fysisk latch och pixelbevis |
| 11 | Late HMOVE | Reserv för särskilda positioner | Risk för artifacts/extra deadline |
| 12 | Raster Color Changes | Gul P0 + vit NPC, P1 orange dörr, guldnyckel | M0 har samma `COLUP0` som P0 |
| 13 | 48-pixel / Six-Digit Score Kernel | Poäng/HUD i separat band | Ger inte fler spelplansaktörer |
| 14 | Multiple Display Kernels | Separera HUD/rum/dörrband | Samtidig Y-konflikt kräver fortfarande hantering |
| 15 | NUSIZ Sprite Duplication | Samma bitmap vid hårdvarans fasta avstånd | Fem numeriskt fria X saknar sådana garantier |
| 16 | Sprite Reflection | Spara omvänd vänster-/högerform | Löser inte vertikalt felvänd R1ba |
| 17 | Missile and Ball Reuse | `BL` som vänster 4CC-vägg, M0 som enda skott | `BL` förbrukad i dörrband, delar `COLUPF`; M0 delar P0-färg |
| 18 | Playfield Score Mode | Möjligen HUD | Skulle ta playerfärger till väggar i spelband |
| 19 | Playfield Priority Switching | Skymning/vägg-nära fiender | Påverkar visuella lager och kollision, inte logisk key |
| 20 | Hardware Collision Latches | Registrera fysisk träff före logisk ID-kontroll | Latch anger inte automatiskt vilken multiplexad NPC som träffades |
| 21 | RIOT Timer Scheduling | Stabil NTSC frame och VBLANK/overscan | Lägger inte till cykler i 76c-linjen |
| 22 | Stack/RAM Mirroring | Möjlig minnesbesparing för händelselista | 128 B RAM och stackkollisioner kvarstår |
| 23 | Undocumented 6502 Opcodes | Ej huvudspår | Kompatibilitet och reproducerbarhet |
| 24 | Precomputed Tables & Cycle-Exact Kernels | **Högsta nyttan:** Y-sort, X-event, PF-mask, bankbudget | Måste klara faktisk CC-tidslinje och RAM/ROM-gränser |
| 25 | Stack-Based TIA Register Tricks | Sent expertalternativ | Får ej räknas som gratis TIA-objekt |
| 26 | Timing-Based Horizontal Scrolling | Låg prioritet i statiska rum | Inte den aktuella flaskhalsen |
| 27 | SCABS | Specialhårdvarualternativ | Inte standard F6, ej auktoriserat |
| 28 | Extra Cartridge RAM / Superchip | Större minnesbudget möjligt | Ej standard F6 och inte extra spelarsprites |
| 29 | DPC | Separat cartridgeteknik | Ej godkänd mapperändring |
| 30 | DPC+/CDF/ARM | Eventuell annan framtida plattform | Kräver nytt scope, löser inte TIA-objectantal automatiskt |

## Fem kombinationshypoteser – ej implementation

- **TK01:** sprite multiplexing + mid-line GRP/RESP + VDEL/HMOVE + exakta tabeller för fria same-Y-objekt. [G5H](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md) visar att vissa förenklade direktscheman kräver 79/76 cykler; det är **inte** universellt NO-GO men ingen G0-PASS.
- **TK02:** reflekterad PF + Ball som vänstervägg + P1-dörr. **3520/3520** historiska kartceller matchade en *offline* PF/BL-modell; ingen fysisk RESBL/ENABL/colorclock-/kollisions-PASS. Inte bevis för nu godkända *framtida* A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01-kartor.
- **TK03:** Berzerk-inspirerade Y-band + dynamisk P0/P1-ägarmodell. [G5K](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md) är en villkorad offlineanalys; Y-begränsning ändrar gameplay och fordrar uttryckligt beslut.
- **TK04:** key+vit fiende+orange dörr på samma rasterhöjd. S05 ger möjlig P0-trippel medan P1 redan är dörr; **O1 tillåter bara skymning vid verklig överlapp**. Ingen godkänd generell key-renderer.
- **TK05:** Venetian Blinds, flimmer och NUSIZ som reserver. Ingen tidigare negativ renderings-/10Hz-/felvänd-mask-test får döpas om till PASS.

**Prioritet vid eventuell separat auktoriserad teknisk studie:** #01, #02, #07, #09, #10, #12, #14, #17, #20, #21, #24. Skriv alltid *vilken* START-, färg-, CC- eller cykelkonflikt tricket skulle lösa; en tekniklista skapar inte en tredje Player-kanal.

## Senaste G0-konsekvensen, inte ett 31:a trick

[G5AA](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) visar att en ofullständig opcodekostnad på **58/68c** (villkorligt **74/79c** med ytterligare registerskrivningar) inte bevisar H4 utan källstyrd **RESP→START, GRP-delay, ENAM0/NUSIZ0-M0-copy** och numerisk X-scheduler. En framtida minimalt instrumenterad TIA-fasmätning är **endast ett förslag**, inte ett beställt experiment.
