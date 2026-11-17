# LET ME OUT! – AUKTORITET OCH NULÄGE / MAIN VIII V5

**Klass:** källnavigering och daterad kunskap, inte självständig spelcanon, implementationsorder, ROM-PASS eller oberoende verifiering. Kontrollera alltid relevanta original i GitHub och Google Drive vid ändrad status, beslut eller tekniska påståenden.

**Statusöversikt (MAIN VIII, 2026-11-17 efter G5AG):** G5Z H4-ONE G0 = `INCONCLUSIVE_NO_ROM`; G5AD LM-D21 = `NO_BUILD_INSTRUMENTATION_BLOCKER` (ingen ny ROM eller C0–C4/N1-mätning); G5AF LM-D22 = `INSTRUMENTATION_READY_BOUNDED`, genomfört på oförändrad äldre F9 och mottaget av MAIN VIII endast som utvecklaregenkontroll. **G5 FORMAL OPEN. Ingen ny ROM/H4/G1/G6/F12/S05/femfiender/oberoende Verification/PR-merge auktoriserad.** [MAIN VIII G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) · [levande statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

## Direkta beslut och deras omfattning

| Område | Gällande beslut för framtida spel | Gräns |
|---|---|---|
| Ursprung | [Originalpaket: Master Spec + 57 beslut](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view) och [G1-källgranskning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G1_AUTHORITY_DIFF_2026-11-17.md) | Historiska ursprungsfiler ändras inte retroaktivt |
| Färger och dörr | Svart spelbakgrund, bruna väggar, gul spelare, vita människolika NPC, guldnyckel; orange ENDAST högerdörr med svart utskuret nyckelhål i **dörrens bitmap**, ingen ny nyckelhålssprite | Färg-/registertiming inte fullständigt TIA-verifierad |
| LM-D06/O1 | Tillfällig skymning av nyckeln tillåten **vid faktisk NPC/key-pixelöverlapp** | Ingen allmän same-Y-osynlighet eller 10Hz-waiver |
| LM-D12–13 | Fem NPC individuellt fri logisk X/Y, fyra riktningar, begriplig fara och key-synlighet. [Beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) | Inga permanent tvingade Y-banor, inga dolda rendererkompromisser |
| LM-D14 | Fem: **M,M,F,SM,SF**; framtida R1 fem NPC, R2 fyra överlevande + nyckel efter dödsanimation. [Beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) | Ingen ny implementerad femfienders-ROM |
| LM-D15 | **−30 per död fiende**, poänggolv 0 per event, +50 key pickup, +100 exit och +15 per levande NPC vid exit. [Beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) | Historisk sexfiendersspec −25 inte omskriven |
| LM-D16 | Fem olika, förhandsvaliderade NPC-starter per rum och en likformigt slumpad key-bärare (1/5 per individ). [Beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) | Exakta koordinater, pooler och PRNG återstår |
| LM-D17/19 | Exakta framtida 40×22-kartor **A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01**. [Manifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) | Designgodkännande, ingen ROM-kartcutover |

## Tekniskt bevisläge

| Prov | Faktiskt resultat | Begränsning |
|---|---|---|
| F9 | Tre korrekt vända originalmasker med tre **binära** X-selectorval i en historisk ROM och Stella | Inte tre valfria numeriska X eller full fem-NPC-kernel |
| R1ba | Historisk positiv rapport; senare käll-/pixelrevision fann felvända stora maskformer | Inte rättvänd full R1 |
| F11 | G0 FAIL för just fyra numeriska P1-X i dåvarande schemat; **ingen** F11-ROM | Inte universellt NO-GO för Atari |
| R3 | Isolerad orange P1-dörr med negativt svart nyckelhål demonstrerad | Inte integrerad S05 |
| G5Z/LM-D20 | 72 källrader analyserade; `G0_INCONCLUSIVE_NO_ROM`. [MAIN mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) | Ingen fysisk H4-plan eller ny ROM |
| G5AD/LM-D21 | Körd förbyggsgrind slutade `NO_BUILD_INSTRUMENTATION_BLOCKER`. [G5AE](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) | Ingen ny kalibrerings-ROM, ingen C0–C4/N1 mätning |
| G5AF/LM-D22 | Två Stella/Actions-försök på fryst F9; sista lyckad med två numeriska debuggerstopp och TIA-bilder. [G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) | **Bara instrumenterings-egenkontroll**, ingen oberoende pixel-/START-/H4-VERIFICATION |

**Fortfarande olöst:** fem samtidiga fria 8×9-NPC med gul spelare, projektil och Playfield på överlappande Y; S05 med key, vit NPC och orange dörr samma Y; exakt 8×9-kollision, AI och framkomliga spawns på de nya kartorna. G5 är fortfarande **öppen**. [Aktuell arbetskö](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

Historiska v0.11 A01/B01/C02/D01, v0.18 R1 sex/R2 fem+nyckel och tidigare -25/kill är fortsatt autentiska **historiska** käll- och testversioner. Godkänd framtida design är ingen retroaktiv test-PASS.

**Aktuella ärenden:** [Issue #14](https://github.com/Odourman/let-me-out/issues/14) stängd som instrumentering, [Issue #13](https://github.com/Odourman/let-me-out/issues/13) stängd efter förbyggsstopp, [Issue #8](https://github.com/Odourman/let-me-out/issues/8) endast uppskjuten, [PR #7](https://github.com/Odourman/let-me-out/pull/7) öppen blockerad draft.
