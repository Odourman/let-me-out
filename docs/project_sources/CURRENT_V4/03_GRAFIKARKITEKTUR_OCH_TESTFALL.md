# LET ME OUT! – GRAFIKARKITEKTUR OCH TEKNISKA TESTGRÄNSER / V4


**LÄSANVISNING V4:** Tidigare versioners källangivelser, gamla GitHub Issues, initiala ROM-beställningar och äldre framtidsförslag är historiska vid sina respektive tidpunkter. Högre auktoritet och senare uttryckliga användarbeslut gäller inom exakt beslutat ämne. Ingen source-only-status är fysisk Atari/Stella-verifiering. Detta källpaket ger ingen ny teknisk auktorisation.

**Läs alltid aktuell status:** [GitHub](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) · [Drive](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit).

**Klass:** tekniskt käll- och experimentsindex. **Inte** bevisad kernel, ROM-implementationsorder eller PASS.

## TIA-kontrakt att respektera

- NTSC **76 CPU-cykler/scanline = 228 TIA colorclocks**; 68 CC HBLANK och 160 synliga CC. Verklig pixel-START och fördröjda registereffekter måste analyseras, inte förväxlas med `STA`-cykeln.
- Bara två 8-bitars player-kanaler: **P0/M0 delar `COLUP0`, P1/M1 `COLUP1`, PF/BL `COLUPF`**. `NUSIZ0` påverkar både P0 och M0 och kan skapa oönskade missilkopior. VDEL skapar inte en tredje playercounter.
- Standard-F6: 16KiB ROM fördelat på fyra 4KiB-banker; **128B RIOT RAM inklusive stack**. Extra ROM-banker löser inte TIA:s simultana färg-/bitmap-/cykelbegränsningar.
- Fyra originalmasktyper **M/F/SM/SF 8×9 TOP-DOWN** (två stora M-instansers bitmapp är identisk men har individuella logiska positioner). [Frysta originalmasker](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json).
- Framtida rumskartor är **40×22 data** i [G5X](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json); de är inte färdigt Playfield-registerschema eller verifierad 8×9-kollision.

## Riktig evidens kontra frestande felaktiga slutsatser

| Prov | Bevisat inom sitt scope | EJ bevisat |
|---|---|---|
| R1f/R1g | Historiska P0-kopior/specialkernlar, somliga verkliga pixelbilder | Numerisk fri X i båda identitetsordningar och **same-Y M0**. M0 låg på y−1. |
| F9 | 3 TOP-DOWN-originalmasker med 3 **binära** X-väljare i en ROM och Stella | 3 helt fria numeriska X; gemensam fem-NPC-kernel |
| F11 | G0 käll-Fail för 4 numeriska P1-aktörer i specifik allokering | Global Atari-omöjlighet |
| G5H | Naiv fem-NPC-direktsumma 79/76 worst och 74/76 gynnsamt (före extra kostnader) | H4 påvisad omöjlig / 5NPC möjlig |
| G5T/G5V | Offline-kartvisualisering och 2×2-nåbarhet, MAIN återkörd | Riktig PF-bild, collision, fem spawns, AI och Stella |
| **G5Z G0** | **72/72** mask-/CC-källrader korrekt och villkorlig **58/68c** opcodebudget | Komplett TIA START/GRP/RESP/NUSIZ/M0/PF-schema; slutklass **`G0_INCONCLUSIVE_NO_ROM`** |
| R3 | Isolerat orange P1-högerdörrprov med svart genomskinligt keyhole | S05 med gold key/white NPC/yellow player/M0/PF på samma rasterhöjd |

## Olösta kritiska belastningar

**H4-ONE** = en gul diagnostisk P0-player + en vit original M på P0, P1 vita original F/SM, **exakt en** M0 på **samma aktiva nio rasterrader**, två verkliga bruna PF-väggkanter, BÅDA horisontella P0-aktörsordningarna och numeriska RAM-X. [G5Z order](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Z_MAIN_VII_ROM_DEVELOPMENT_III_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_2026-11-17.md) / [G5AA slutbedömning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md). **G0 avslutad INCONCLUSIVE; H4-ROM ej byggd.** H4 har **tre** vita NPC, inte fem.

**Fem-NPC fullspel** = fem vita M,M,F,SM,SF + gul player och projektil, fria logiska X/Y med tillåtna samma-Y-stresspositioner, rättvända nio maskrader, riktiga tvåsidiga väggar och ibland orange P1-dörr. Inga Y-lanes eller generell same-Y-osynlighet godkända. [G5H](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md).

**S05** = gul player + vit NPC + guldkey + orange högerdörr med transparent svart keyhole, samtidigt M0 och brun PF. Key måste vara synlig vid **0 faktisk pixelöverlapp**, och får skymmas endast tillfälligt vid *verklig* överlapp. [G5Y separat testplan](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Y_MAIN_VII_FALSIFIABLE_HARDWARE_TEST_PLAN_H4_ONE_S05_FIVE_NPC_NOT_AUTHORIZED_2026-11-17.md).

## Vad som rimligen kan bli nästa test – EJ BESTÄLLT

En **enskilt instrumenterad minimal TIA-fas-/kopie-kalibrering** av underbyggda luckor **`RESP0` under aktiv rendering, `GRP` latch/fördröjning, `NUSIZ0=$02` påverkan på P0/M0 och exakt en M0 med tidsstyrd `ENAM0`-gate** kan eventuellt minska osäkerheten. **Det är ett förslag enligt G5AA, inte ett H4-PASS eller order att skapa en ROM**. Ingen G1/G6/F12, assemblerändring eller Verification får ske utan ett separat precist användarbeslut.

Se [G3 resurser](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md), [G2 negativa resultat](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md), [G5Z fryst utvecklaroriginal](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md).
