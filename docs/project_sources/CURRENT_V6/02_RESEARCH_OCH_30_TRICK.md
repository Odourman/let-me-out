# LET ME OUT! – 30 ATARI-TRICK OCH FORTSATT RESEARCH / V6

**Klass:** research-index, inte spelcanon, komplett TIA-kernel eller implementationsorder. [De 30 ursprungligen numrerade teknikerna](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md) och [G5L:s tekniska jämförelse](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md) är original. 30 teknikrubriker, 52 teknikmönster och 67 riskpunkter **överlappar**, inte 149 separata lösningar.

**Statusöversikt (MAIN VIII, 2026-11-17 efter LM-D23/G5AH):** G5Z G0 = `INCONCLUSIVE_NO_ROM`; G5AD/LM-D21 = `NO_BUILD_INSTRUMENTATION_BLOCKER` (C0–C4/N1 ej körda); G5AF/LM-D22 = `INSTRUMENTATION_READY_BOUNDED` (endast F9-instrumenterings-egenkontroll). **NYTT G5AH/LM-D23: `C0_ONLY_AUTHORIZED_NOT_YET_EXECUTED`**. Endast ROM DEVELOPMENT III får göra C0-mätbarhetsförgrind och **vid PASS** bygga **EN** minimal 16 KiB standard-F6/NTSC C0-ROM med numerisk RAM-X 40/104, högst två nya Actions-mätkörningar. **G5 FORMAL OPEN. C1–C4/N1, H4/G1, G6/F12, S05, femfiendersimplementation, oberoende Verification och PR-merge EJ auktoriserade.** [Bindande G5AH-beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AH_MAIN_VIII_LM_D23_C0_ONLY_TIA_MEASUREMENT_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) · [Issue #15](https://github.com/Odourman/let-me-out/issues/15) · [levande statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

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

## Status efter G5AF och nya G5AH

G5AF reparerade bara logg-/bildkedjan med en **oförändrad fryst F9-ROM**: två olika Stella `RESP1`-debuggerstopp i samma frame/rad (PC `$F1F0`, `_sCycles=21`; PC `$F1F8`, `_sCycles=32`) och hashade native TIA-bilder **enligt specialistens egenkontroll**. [Fryst rapport](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md). Dessa stopp är inte exakta `STA RESP`-slutcirklar eller intern TIA-START-kalibrering. G5AD:s sex TIA-fall förblir ej körda.

**C0 är nu separat beställt:** [G5AH/LM-D23](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AH_MAIN_VIII_LM_D23_C0_ONLY_TIA_MEASUREMENT_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) med hård förgrind. C1–C4/N1 och kombinationstricken har inte fått ny implementationstillåtelse.

**Forskningsprioritet utanför C0 vid ett separat framtida beslut:** isolera fysisk `RESP/GRP/NUSIZ0/ENAM0`-timing och färg-/M0-kopieringskonflikter innan någon ny fullskalig renderingsfamilj prövas. Detta är en *rekommendation utanför C0-only*, inte en tredje F9-run eller full H4/G6-övergång. [G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md).
