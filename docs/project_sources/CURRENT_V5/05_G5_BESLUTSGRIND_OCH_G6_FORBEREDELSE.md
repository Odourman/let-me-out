# LET ME OUT! – G5-AUKTORISATIONSGRIND, NÄSTA BESLUT OCH G6 / V5

**Klass:** källnavigering och daterad kunskap, inte självständig spelcanon, implementationsorder, ROM-PASS eller oberoende verifiering. Kontrollera alltid relevanta original i GitHub och Google Drive vid ändrad status, beslut eller tekniska påståenden.

**Statusöversikt (MAIN VIII, 2026-11-17 efter G5AG):** G5Z H4-ONE G0 = `INCONCLUSIVE_NO_ROM`; G5AD LM-D21 = `NO_BUILD_INSTRUMENTATION_BLOCKER` (ingen ny ROM eller C0–C4/N1-mätning); G5AF LM-D22 = `INSTRUMENTATION_READY_BOUNDED`, genomfört på oförändrad äldre F9 och mottaget av MAIN VIII endast som utvecklaregenkontroll. **G5 FORMAL OPEN. Ingen ny ROM/H4/G1/G6/F12/S05/femfiender/oberoende Verification/PR-merge auktoriserad.** [MAIN VIII G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) · [levande statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

## Avslutade uppdrag, inte aktiva specialistordrar

| ID | Faktisk slutfas | Fortsätter inte automatiskt |
|---|---|---|
| G1–G4 | Källgranskning och fysiska hypoteser source-only; inte full ROM-PASS | Ingen automatisk G5/G6-implementation |
| G5Z / LM-D20 | H4-ONE G0 source-only, `INCONCLUSIVE_NO_ROM`. [G5AA](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) | Inga G1-/DASM-/Stella-/ROM-pass via G0 |
| G5AD / LM-D21 | En villkorad TIA-mikro-ROM var godkänd men nådde `NO_BUILD_INSTRUMENTATION_BLOCKER`. [G5AE](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) | Ingen ny ROM, inga C0–C4/N1 utförda |
| G5AF / LM-D22 | Reparation av **enbart** F9/Stella-harness; **två Actions-mätkörningar** och slutlig `INSTRUMENTATION_READY_BOUNDED` enligt developer, MAIN VIII mottog som begränsad leverans. [G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) | Ingen tredje F9-run, inget implicit nytt TIA-prov |
| G5T/G5V | Offlinestudier av kartor, separata GRAPHICS-uppdrag avslutade | Ingen Playfield-ROM- eller kollisions-PASS |

## Gällande design och kvarstående stoppspärrar

**Godkända framtida mål:** fem vita NPC M,M,F,SM,SF, fri logisk individuell X/Y och kvalitativt rättvis hot-/key-synlighet; svart bakgrund, brun PF, gul spelare, orange högerdörr med negativt svart nyckelhål; −30/kill och fem godkända spawns samt likformig 1/5-keyholder; exakta framtida 40×22-kartor `A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01`. [Beslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [score/roster/spawn](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [kartmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json).

**Olösta fysiska krav:** fem fulla 8×9-masker med individuellt fri X/Y i same-Y-stressfall, gul spelare, M0/PF, S05 med key+NPC+orange P1-dörr på samma Y, riktig collision, spawns och AI. G5H:s 79/76-cykelutfall under en begränsad naiv direktmodell är inte universellt bevis för omöjlighet; G5AF:s instrumenterings-PASS är inte kernel-PASS. Y-lanes är inte godkända som tyst kompromiss; O1 är bara faktisk key/NPC-pixelöverlapp.

**Formell status:** `G5_FORMAL_OPEN`. **G1/H4 ny ROM, G6/F12, R1–R4 full framtida implementation, S05, ny oberoende VERIFICATION II, PR-merge och vidare Actions-test efter LM-D22 är inte auktoriserade.** [G5 beslutsspärr](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md). [PR #7](https://github.com/Odourman/let-me-out/pull/7) är blockerad draft, [Issue #8](https://github.com/Odourman/let-me-out/issues/8) uppskjuten, [Issue #14](https://github.com/Odourman/let-me-out/issues/14) avslutad som instrumenteringsuppdrag.

## MAIN VIII:s möjliga nästa steg (endast beslutsberedning)

Ett **nytt** snävt TIA-mikroprovsförslag kan behöva precisera faktiska `RESP`-START-, `GRP`-latens-, `NUSIZ0`-P0/M0-kopie- och `ENAM0`-gate-effekter i reproducerbar Stella/Debugger-evidens. Äldre [G5AC](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AC_MAIN_VII_TIA_PHASE_CALIBRATION_DECISION_READY_NOT_AUTHORIZED_2026-11-17.md) var **historisk förberedelse** till den senare LM-D21/G5AD-beställningen; det gamla mandatet **är förbrukat och gav ingen ROM**. G5AF förbättrade enbart instrumenteringen. Därför krävs **ett nytt separat uttryckligt användargodkännande** innan ROM DEVELOPMENT III får exekvera någon ny kod/ROM/Actions-mätning. MAIN får fortsätta med källgranskning, researchplan och saklig beslutsberedning inom tidigare scope; separat Verification får inte utges som gjord.

Vid tveksamhet kontrollera alltid [levande statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [MAIN VIII G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) och gällande användarbeslut. Radera aldrig tidigare negativa resultat eller skriv om historiska ROM-provvärden till PASS.
