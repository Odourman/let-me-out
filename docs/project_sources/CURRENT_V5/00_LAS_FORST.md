# LET ME OUT! – STARTA HÄR / PROJECT SOURCES V5

**Aktuell reviderad källguide:** MAIN VIII, 2026-11-17 efter G5AG. **Klass:** källnavigering och daterad kunskap, inte självständig spelcanon, implementationsorder, ROM-PASS eller oberoende verifiering. Kontrollera alltid relevanta original i GitHub och Google Drive vid ändrad status, beslut eller tekniska påståenden.

**Statusöversikt (MAIN VIII, 2026-11-17 efter G5AG):** G5Z H4-ONE G0 = `INCONCLUSIVE_NO_ROM`; G5AD LM-D21 = `NO_BUILD_INSTRUMENTATION_BLOCKER` (ingen ny ROM eller C0–C4/N1-mätning); G5AF LM-D22 = `INSTRUMENTATION_READY_BOUNDED`, genomfört på oförändrad äldre F9 och mottaget av MAIN VIII endast som utvecklaregenkontroll. **G5 FORMAL OPEN. Ingen ny ROM/H4/G1/G6/F12/S05/femfiender/oberoende Verification/PR-merge auktoriserad.** [MAIN VIII G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) · [levande statusindex](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md).

## Var du hittar originalkällorna

| Fråga | Primär originalkälla |
|---|---|
| Senaste status, öppna uppdrag och spärrar | [GitHub status och arbetskö](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) · [Google Drive-status](https://docs.google.com/document/d/13ROb1ZXjPjQh7g6xDSGfxIrquhD6xtWI-LCloF9BMPA/edit) |
| Högsta spelbesluten | [Ursprunglig Master Spec / 57 beslut](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view) · [G1 authority diff](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G1_AUTHORITY_DIFF_2026-11-17.md) |
| Individuellt fri X/Y, synlighet, O1 | [LM-D12/13](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) · [O1-beslutsregister](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md) |
| Fem fiender, poäng och spawn | [LM-D14/15/16](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md) |
| Fyra framtida exakta kartor | [G5X källpinnat kartmanifest](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) |
| Negativ G0 och därefter G5AD förbyggsstopp | [G5AA](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) · [G5AE](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AE_MAIN_VII_G5AD_NO_BUILD_INSTRUMENTATION_BLOCKER_RECEIPT_AND_STELLA_SAVESES_SOURCE_REVIEW_2026-11-17.md) |
| G5AF utförd instrumentering | [MAIN VIII G5AG](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AG_MAIN_VIII_G5AF_F9_INSTRUMENTATION_RECEIPT_2026-11-17.md) · [fryst ROM DEVELOPMENT III](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md) |
| G5 grundläggande gate och beslutshistorik | [G5 beslutsspärr](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md) |
| 30 originaltrick | [Research: exakt numrerade 30](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md) |

## Dessa sex Project Sources

- `00_LAS_FORST.md`: ingång, auktoritet och länkregister.
- `01_AUKTORITET_OCH_NULAGE.md`: aktuella beslut kontra historiska tekniska bevis.
- `02_RESEARCH_OCH_30_TRICK.md`: tidigare teknikspår och begränsningar.
- `03_GRAFIKARKITEKTUR_OCH_TESTFALL.md`: TIA-konflikter och falsifierbara testfall.
- `04_FEM_FIENDER_SPELDESIGN_DELTA.md`: fem-NPC-design, poäng, spawn, kartor.
- `05_G5_BESLUTSGRIND_OCH_G6_FORBEREDELSE.md`: aktuellt stopp och vad som kräver nytt beslut.

## Auktoritets- och rollprincip

För spelcanon gäller direkta ursprungliga användarbeslut, giltig Master Spec och **senare uttryckliga beslut endast i det område de ersätter**. För uppnådd teknisk funktion gäller verkliga frysta ROM-filer, rå Stella/Debugger-evidens, en utvecklares egenkontroll och separat oberoende VERIFICATION, utan att förväxla nivåerna. Research, offlinegrafik och dessa sex filer är rådgivande. ChatGPT Memory/Library är aldrig projektsanningen.

**MAIN VIII** leder, samordnar och mottagningskontrollerar. **ROM DEVELOPMENT III** programmerar enbart godkänt scope. **RESEARCH II** utreder, **GRAPHICS II** förbereder grafik inom order, **VERIFICATION II** granskar fristående efter separat auktorisation och **ART/PACKAGING & MANUAL II** hanterar omslag och manual. GitHub-Issues startar inte separata chattar automatiskt.

**Undvik ID-kollisioner:** `K1` = key-pickup-regel, `TK01–TK05` = teknikfamiljer; gamla `S0/S1` = spawnfilter, `G5-S0/G5-S1/G5-S2` = renderingsval; `G4-A1` ≠ `G5Q A1`.

**Versionsregel:** GitHub och Drive uppdateras inte automatiskt i ChatGPT Project Sources. Ladda upp exakt sex aktuella filer, inte dubbletter eller äldre V2/V4-paket. Gamla rapporter behålls som historiska dokument, men får inte användas som dagens arbetsorder.
