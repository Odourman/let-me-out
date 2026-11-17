# LET ME OUT! – FEM FIENDER, FRAMTIDA SPELDESIGN OCH KARTOR / V6

**Klass:** godkända framtida användarbeslut med tekniska öppna frågor; inte en godkänd ROM-version, ny mapper eller implementation. Originalpaketet [Master Spec/57 beslut](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view) gäller i andra frågor. Vid konflikt läs de exakta [LM-D12/13](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D14/15/16](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) och [LM-D17/19 kartmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json).

**Statusöversikt (MAIN VIII, 2026-11-17 efter LM-D23/G5AH):** G5Z G0 = `INCONCLUSIVE_NO_ROM`; G5AD/LM-D21 = `NO_BUILD_INSTRUMENTATION_BLOCKER` (C0–C4/N1 ej körda); G5AF/LM-D22 = `INSTRUMENTATION_READY_BOUNDED` (endast F9-instrumenterings-egenkontroll). **NYTT G5AH/LM-D23: `C0_ONLY_AUTHORIZED_NOT_YET_EXECUTED`**. Endast ROM DEVELOPMENT III får göra C0-mätbarhetsförgrind och **vid PASS** bygga **EN** minimal 16 KiB standard-F6/NTSC C0-ROM med numerisk RAM-X 40/104, högst två nya Actions-mätkörningar. **G5 FORMAL OPEN. C1–C4/N1, H4/G1, G6/F12, S05, femfiendersimplementation, oberoende Verification och PR-merge EJ auktoriserade.** [Bindande G5AH-beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AH_MAIN_VIII_LM_D23_C0_ONLY_TIA_MEASUREMENT_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) · [Issue #15](https://github.com/Odourman/let-me-out/issues/15) · [levande statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

## Nu godkänt, inte längre bara förslag

- **Framtida roster LM-D14:** exakt fem fiendeinstanser: **två stora män (M1, M2), en stor kvinna (F), en liten man (SM) och en liten kvinna (SF)**. Bara fyra bitmap-originaltyper, men fem olika individers positioner. Framtida R1 fem NPC, R2 fyra kvarvarande NPC och en fysisk synlig guldkey. 
- **LM-D12/13:** individuell fri logisk X/Y, fyra riktningar, inte fasta Y-banor. Rättvis hot-/key-synlighet; ingen konstant rasterdöljning när NPC eller key inte pixeltäcks.
- **LM-D15:** **-30 poäng per dödad NPC**. Övriga ursprungliga poängregler: **+50 vid pickup**, **+100 vid verklig utgång**, **+15 per levande NPC vid exit**, aldrig score under **0** vid någon händelse. Historiska ROM-/scoretester med -25 skall vara frysta.
- **LM-D16:** fem **olika och korrekt förhandsvaliderade** spawnplatser på per-rum exakt beslutad framtida karta. Endast **en** av fem individuella instanser bär key, likformigt **1/5**, inte modulobias/slump från statisk typ. Nyckeln kommer först efter bärares dödsanimation, på faktisk logisk dödsposition. Exakta pooler och PRNG återstår.
- **LM-D17/19:** de exakta framtida kartlayoutmålen A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01 är nu godkända; ingen renderad ROM-PF eller kartcutover finns.

Bindande källor: [LM-D12/13](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D14/15/16](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md), [LM-D17/19 kartmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json), [K1/E1](https://github.com/Odourman/let-me-out/blob/main/docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md).

## Ny poängmatematik och fallgrop med golv

Vid fem NPC och k dödade, **om inga nollgolv inträffar före exit**, blir framtida rumspott: `Δ=150 + 15*(5-k) - 30*k = 225 - 45*k`. Vid **fem dödade**: `0 netto/rum` efter komplett pickup/exit när startsaldot räcker för alla fem -30-avdragen. Men vid startscore 0 och fem dödade **före** pickup nollklampas varje -30, varefter pickup/exit kan ge **+150**. Det är **avsedd regelkonsekvens att testa**, inte 0 oavsett händelseordning. G5R:s 210-körnings offline-CSV ersätter inte faktisk ROM-verifiering: [G5R](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5R_FIVE_NPC_SCORE_FLOOR_210_CASES_SOURCE_ONLY_2026-11-17.csv).

## Historiskt fryst, inte upphävt i efterhand

| Område | Historisk v0.18 / original | Framtida godkänt mål |
|---|---|---|
| Antal | R1=6 M,M,F,F,SM,SF; R2=5+key | R1=5 M,M,F,SM,SF; R2=4+key |
| Killavdrag | -25 | **-30** |
| Kartor | A01/B01/C02/D01 | A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01, **designbart ännu ej ROM** |
| Spawn | Historiska 2×2-kandidater och S0/S1-filter | Nya fem 8×9-förhandsvaliderade platser per exakt karta (ej valda) |

**Kvar att bevisa:** verklig 8×9 NPC/player/wall-/key-/door-kollision och fria AI-vägar, alla 5 keyholder-fall, K1-pickup först senare tick vid key under spelaren, E1 utgångs-/dödskollision, score 0-golv och extraslivströsklar, riktig samtidig 5NPC/P0/M0/PF och S05. Ingen generell Y-lane/flicker-waiver får införas utan nytt uttryckligt användarbeslut.

**Senare instrumentstatus påverkar inte designen:** G5AF har avslutats med snävt lyckad F9/Stella-instrumenteringskontroll, medan fem-NPC, S05, spawns och verklig kernel ännu saknar ROM-PASS. [MAIN VIII G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) · [aktuell arbetskö](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md). Ingen ny spelregel, Y-lane, flickerwaiver eller kartcutover uppstod genom LM-D20–D23. G5AH gäller bara isolerat C0 och ändrar inte framtida fem-NPC-design.
