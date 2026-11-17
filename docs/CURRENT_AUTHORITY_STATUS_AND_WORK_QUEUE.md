# LET ME OUT! – CURRENT AUTHORITY, STATUS & WORK QUEUE

## 0. SENARE BESLUT LM-D21 – G5AD enda TIA-kalibrerings-ROM uttryckligen godkänd (2026-11-17)

**NYTT OCH AKTUELLT:** Användaren citerade MAIN:s rekommendation om **ett enda instrumenterat TIA-mätprov** av `RESP`, `GRP`, `NUSIZ0`, `M0` och `ENAM0`, och svarade **"Gör så"**. Detta är ett **uttryckligt positivt LM-D21-beslut** som supersederar de äldre globala formuleringarna `NEW_ROM_NOT_AUTHORIZED` **endast för en separat G5AD-diagnostik-ROM**. [G5AD komplett bindande arbetsorder](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) · [sex förregistrerade mätfall](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_TIA_CALIBRATION_PREREGISTERED_CASES_2026-11-17.csv) · [GitHub Issue #13 till ROM DEVELOPMENT III](https://github.com/Odourman/let-me-out/issues/13) · [arkivkopia i Drive](https://docs.google.com/document/d/163Xtt4ygxQD7eM4AfPwZgAN6JktF8DcEQjKK43JNF-g/edit).

**Aktuell orderstatus: `G5AD_SINGLE_TIA_MEASUREMENT_ROM_AUTHORIZED_NOT_YET_RUN`.** Specialist får bygga **en** 16 KiB standard-F6 NTSC diagnos-ROM på isolerad branch och köra DASM/Stella/Debugger för C0–C4/N1, sedan lämna råa CPU-/TIA-/colorclock-/pixelbevis och stoppa. Detta **är inte full H4 G1**, inte S05/fem NPC och inte ny spelversion. `G5Z_G0=COMPLETE_INCONCLUSIVE_NO_ROM` förblir oförändrat. **`G5_FORMAL_OPEN`**, `FULL_H4/G6/F12/S05/FIVE_NPC_IMPL/INDEPENDENT_VERIFICATION/PR_MERGE=NOT_AUTHORIZED`.

**Övriga historiska avsnitt längre ned** talar om läget före LM-D21 och är inte ett upphävande av denna enskilda beställning. GitHub-issue kan inte automatiskt starta en separat specialistchatt.


**PROJECT SOURCES CURRENT V4:** [Sex verifierade Markdown-filer + SHA-manifest i GitHub](https://github.com/Odourman/let-me-out/tree/main/docs/project_sources/CURRENT_V4) · [officiell Drive-guiden](https://docs.google.com/document/d/19EU_PLT5fDXI41u4kA3rWMU6FOVKPjsAYCwbvVLRlpA/edit). Användaren måste manuellt ersätta de sex faktiskt anslutna V2 Project Sources. **Äldre V1/V2/V3 och en historisk Drive-ZIP märkt FINAL är ARKIV, inte aktiva källfiler.** GitHub-ärendena #3 (historiska spawns) och #6 (v0.18 order) är nu administrativt **CLOSED/not_planned** som supersederade, utan att gamla ROM-prov godkänts. Issue #8 är fortsatt **OPEN men DEFERRED** enligt batchpolicyn.

**Aktuell MAIN VII-ingång · upprättad 2026-11-17 efter G5AA.** Detta är en **daterad, versionskontrollerad navigations- och statusguide**, inte en ersättning för användarens originalbeslut, Master Spec, frysta ROM/bytefiler eller oberoende verifiering. **Kontrollera GitHub/Drive live vid framtida beslut.** Bevara och citera originalkällorna när en konflikt uppstår.

## 1. Läsordning och auktoritet
1. **För spelregler/canon:** ursprungligt användarbeslut/57 beslutsrader i [ursprunglig Master Spec/handoff](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view) + [G1 auktoritetsgranskning](gates/G1_AUTHORITY_DIFF_2026-11-17.md); sedan **senare uttryckligt användarbeslut som ersätter exakt det området**, t.ex. LM-D12..20. Ingen källa nedan får tyst överrida en högre.
2. **För utfört tekniskt resultat:** fryst faktiskt ROM-bygge, källcommit, rå Stella/Debugger med rätt scenario och fristående VERIFICATION II. En specialistegenkontroll, offlinegrafik eller beräknad cykelbudget får inte beskrivas som sådant bevis.
3. **För aktuell projektordning:** detta index och [MAIN:s kronologiska beslutssupplement](MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md), [G5:s kronologiska auktorisationsgräns](gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), [MAIN:s historiska projektlogg](CURRENT_PROJECT_STATE_2026-11-15.md). I äldre dokument är tidigare uttryck som "nu", "aktivt" och "enda rekommenderade" **tidsbundna**. Läs inte ett äldre avsnitt som aktuellt bara för att det ligger nära början.
4. **Project Sources 00–05:** en kort synkroniserad källguide, inte canon eller en live ansluten repository-state. ChatGPT Memory/Library inte auktoritet.

## 2. Aktiva, senare direkt användargodkända framtida mål
| Fråga | Aktuellt giltigt beslut | Exakt original |
|---|---|---|
| NPC-rörelse och synlighet | LM-D12/A1: fri logisk individuell X/Y, fyra riktningar, ingen obligatorisk hård Y-lane; LM-D13/B1: hot/nyckel ska inte döljas av enbart same-Y | [G5Q](gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Framtida fem NPC | LM-D14/C1: **M, M, F, SM, SF** = fem individer, fyra visuella typmasker; R1 fem, R2 fyra kvar + guldnyckel efter bärares dödsanimation | [G5S](gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Poäng och spawn | LM-D15/D1: **−30 per dödad NPC**, scoregolv 0 per event, +50 key-pickup, +100 exit, +15 per överlevare; LM-D16/E1: 5 olika förhandsvaliderade startpositioner per rum, individuell key-holder likformigt **1/5**; **inte** exakta godkända koordinater eller PRNG | [G5S](gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Exakta framtida 40×22 rum | LM-D17 och LM-D19: `A_OPEN_01`, `B_OPEN_02`, `C_OPEN_01`, `D_OPEN_01`. **Endast framtida designlayouter**, ej ROM-byte/cutover eller 8×9-kollisionstest. | [G5X beslut](gates/G5X_MAIN_VII_B_OPEN_02_EXACT_USER_APPROVAL_AND_FOUR_MAP_BASELINE_DECISION_2026-11-17.md), [fryst source manifest](gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) |
| Nyckelskymning | LM-D06/O1: kortvarig key-skymning får endast ske vid **faktiskt synlig NPC/key-bitpixelöverlapp**; ingen ny general same-Y/osynlighets- eller 10Hz-waiver | [MAIN status och användarbeslut](MAIN_STATUS_NEXT_10_2026-11-15.md), [K1/E1](APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md) |

**Historiska referenser som fortsatt måste bevaras:** v0.11 valda `A01/B01/C02/D01`, v0.18 R1 sex/R2 fem+key och −25/kill, tidigare faktiska ROM-/Stella-tester inklusive felaktiga/negativa utfall. En senare *framtida* designomläggning retroaktivt gör inte ett äldre test till PASS, och tar inte bort originalfilens historiska värde.

## 3. Tekniskt bevisläge
- [G5AA MAIN:s mottagningsrapport](gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) och [fryst G5Z originalcommit](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md): **LM-D20:s enda särskilt auktoriserade H4-ONE source-only G0 är färdiglevererad `G0_INCONCLUSIVE_NO_ROM`**, [Issue #12](https://github.com/Odourman/let-me-out/issues/12) stängd. 72/72 analyserade originalmask-/nominell CC-rader ≠ exekverbar kernel. **Ingen G0_SOURCE_PLAUSIBLE, ingen full H4-fysik, ingen ny ROM/Stella/CI** i uppdraget.
- H4-ONE med P0 gul+vit, två vita P1-masker F/SM, exakt en same-Y M0 och verkligt PF: ännu inte källvisat genomförbar. Historisk F9 bevisade endast tre separata **binära** X-val; F11 specifikt `G0 FAIL`; G5H direkt fem-NPC-cykelscenario `79/76` i en snäv modell. Inget universalbevis för Atari-omöjlighet, men **betydande produktionsrisk**.
- **Separat S05**: gul player, vit NPC, gold key, orange högerdörr på P1 med svart genomskinligt keyhole, en M0 och bruna PF på samma raster-Y saknar fysisk lösning. Framtida fem fria 8×9-NPC + egen AI-/spawn-/kollisionslogik obevisade.
- Grafiska små figurers gång och player V03_B:s 8×9-vapenläsbarhet, HUD, ljud och en del förpacknings-/manualbeslut är fortfarande studier/visuella riktningar, **inte fulla ROM-PASS**. Se [G5AB helhetsrevision](project_sources/PROJECT_SOURCES_MAIN_VII_V3_CURRENT_AUDIT_AFTER_G5AA_2026-11-17.md).

## 4. Faktiskt aktivt arbete / ej auktoriserad nästa fas
| Arbete/ärende | Nu-status och innebörd |
|---|---|
| G5 designval | Framtida spel- och kartmål är till stor del fastställda; **G5_FORMAL_OPEN** på grund av teknisk avsaknad av full bevisning |
| G5Z/LM-D20 | **SLUTFÖRD / INCONCLUSIVE / NO_ROM**, order förbrukad och inte kvar som aktivt utvecklaruppdrag |
| [G5AC instrumenterad TIA-kalibrering](gates/G5AC_MAIN_VII_TIA_PHASE_CALIBRATION_DECISION_READY_NOT_AUTHORIZED_2026-11-17.md) | **FÖRSLAG / SOURCE-ONLY BEREDSKAP – EJ beställd**. Eventuellt ett enda framtida småskaligt ROM-/Stella-prov av RESP/START/GRP/NUSIZ0-M0/ENAM0; kräver separat uttryckligt användargodkännande |
| [PR #7](https://github.com/Odourman/let-me-out/pull/7) | Äldre **OPEN DRAFT BLOCKED**, **ej mergad**, negativa rendererresultat bevaras |
| [Issue #8](https://github.com/Odourman/let-me-out/issues/8) | **OPEN MEN DEFERRED / HISTORISKT** enligt användarens batchpolicy, inte aktiv Verification-åtgärd och inget oberoende PASS |
| [Issue #5](https://github.com/Odourman/let-me-out/issues/5) | Framtida key/door-verifieringsgrind **inte** en aktuell ROM-kodorder |
| [Issue #3](https://github.com/Odourman/let-me-out/issues/3) | **CLOSED/not_planned – HISTORISK** v0.11 sex-NPC S0/S1-kandidat, ersatt som framtida speltest; inga nya prov körda |
| [Issue #6](https://github.com/Odourman/let-me-out/issues/6) | **CLOSED/not_planned – HISTORISK** v0.18 6/5-diagnostikorder och tidigare delresultat. Ingen ny fem-NPC-kodorder; inte full v0.18 PASS |

**Grindspärr:** `G5_FORMAL_OPEN`; `G1/G6/F12/NEW_ROM/FIVE_NPC_IMPL/S05_IMPL/NEW_INDEPENDENT_VERIFICATION/PR_MERGE=NOT_AUTHORIZED`. User requests such as "fortsätt" authorize **continued MAIN documentation/research/decision preparation** only within prior scope, never specialist ROM/cutover.

## 5. Projektrollen och nulägeskontroll
MAIN VII samordnar, gör egen mottagnings-/källkontroll, låser endast riktiga användarbeslut. ROM DEVELOPMENT III får implementera endast separat uttryckligen beordrat scope. RESEARCH II är rådgivande. GRAPHICS II gör endast särskilt beställda visuella studier. VERIFICATION II granskar oberoende efter separat batchorder. ART/PACKAGING & MANUAL II skapar omslag/manual, inte ROM-canon.

[GitHub huvudrepo](https://github.com/Odourman/let-me-out), [officiell Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u), [G5AB inventory/method](project_sources/PROJECT_SOURCES_MAIN_VII_V3_CURRENT_AUDIT_AFTER_G5AA_2026-11-17.md). Vid varje faktisk status- eller versionfråga: **fetch latest GitHub HEAD, originaldokument/branch/issue och relevanta Drive-original**. Detta index får uppdateras för korrekt navigering, men inga äldre omstridda källor ska skrivas om som om ett historiskt FAIL aldrig hände.
