# LET ME OUT! – GRAFIKARKITEKTUR, RASTER OCH TESTFALL / V5

**Klass:** källnavigering och daterad kunskap, inte självständig spelcanon, implementationsorder, ROM-PASS eller oberoende verifiering. Kontrollera alltid relevanta original i GitHub och Google Drive vid ändrad status, beslut eller tekniska påståenden.

**Statusöversikt (MAIN VIII, 2026-11-17 efter G5AG):** G5Z H4-ONE G0 = `INCONCLUSIVE_NO_ROM`; G5AD LM-D21 = `NO_BUILD_INSTRUMENTATION_BLOCKER` (ingen ny ROM eller C0–C4/N1-mätning); G5AF LM-D22 = `INSTRUMENTATION_READY_BOUNDED`, genomfört på oförändrad äldre F9 och mottaget av MAIN VIII endast som utvecklaregenkontroll. **G5 FORMAL OPEN. Ingen ny ROM/H4/G1/G6/F12/S05/femfiender/oberoende Verification/PR-merge auktoriserad.** [MAIN VIII G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) · [levande statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

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
| G5AF | Fungerande utvecklarinstrumentering på fryst F9: två numeriska Stella-stopp och nativa TIA-bilder, [mottagna av MAIN VIII](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) | Inte exakt `RESP1` write/START-fas, C0–C4/N1, H4, originalhårdvara eller oberoende Verification |
| R3 | Isolerat orange P1-högerdörrprov med svart genomskinligt keyhole | S05 med gold key/white NPC/yellow player/M0/PF på samma rasterhöjd |

## Olösta kritiska belastningar

**H4-ONE** = en gul diagnostisk P0-player + en vit original M på P0, P1 vita original F/SM, **exakt en** M0 på **samma aktiva nio rasterrader**, två verkliga bruna PF-väggkanter, BÅDA horisontella P0-aktörsordningarna och numeriska RAM-X. [G5Z order](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Z_MAIN_VII_ROM_DEVELOPMENT_III_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_2026-11-17.md) / [G5AA slutbedömning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md). **G0 avslutad INCONCLUSIVE; H4-ROM ej byggd.** H4 har **tre** vita NPC, inte fem.

**Fem-NPC fullspel** = fem vita M,M,F,SM,SF + gul player och projektil, fria logiska X/Y med tillåtna samma-Y-stresspositioner, rättvända nio maskrader, riktiga tvåsidiga väggar och ibland orange P1-dörr. Inga Y-lanes eller generell same-Y-osynlighet godkända. [G5H](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md).

**S05** = gul player + vit NPC + guldkey + orange högerdörr med transparent svart keyhole, samtidigt M0 och brun PF. Key måste vara synlig vid **0 faktisk pixelöverlapp**, och får skymmas endast tillfälligt vid *verklig* överlapp. [G5Y separat testplan](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Y_MAIN_VII_FALSIFIABLE_HARDWARE_TEST_PLAN_H4_ONE_S05_FIVE_NPC_NOT_AUTHORIZED_2026-11-17.md).

## Nästa tekniska frågeställning, ännu inte godkänd som arbetsorder

G5AD:s planerade separata C0–C4/N1-kalibreringsfall av `RESP/GRP/NUSIZ0/M0/ENAM0` har **inte exekverats** på grund av det historiska G5AD-förbyggsstoppet. G5AF bevisar att en begränsad F9-instrumenteringskedja kan fungera, inte att den nya kalibrerings-ROM som då var planerad har byggts eller är auktoriserad igen. Ett nytt tids-/rasterprov fordrar en separat, specificerad användarorder med förregistrerande stimuli och exakta stopp. Ingen full H4-ONE, fem-NPC, S05 eller G6 får startas automatiskt. [G5AE](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) · [G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md).
