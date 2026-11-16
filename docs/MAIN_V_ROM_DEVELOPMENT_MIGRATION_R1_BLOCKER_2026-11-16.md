# LET ME OUT! – MAIN V: ROM DEVELOPMENT-chat migration and frozen R1 blocker intake

**Date:** 2026-11-16. **Cause:** previous ROM DEVELOPMENT conversation reached context length and stopped responding. This file is an operational migration handoff, **not** new authorization to start another implementation step, not independent verification or a design waiver. It preserves the old completed developer R1 result and the previously accepted isolated R3 result.

## 1. Primary source check (MAIN V; read live again)

- Repository: https://github.com/Odourman/let-me-out
- Project Drive folder: https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u
- GitHub Issue #6: https://github.com/Odourman/let-me-out/issues/6 – only v0.18 NTSC R1–R4 diagnostic authorized, standard F6 if justified; issue OPEN.
- Draft PR #7: https://github.com/Odourman/let-me-out/pull/7 – still DRAFT, OPEN, NOT MERGED, last inspected PR head `82667dae033f70570dce903f8e1d4866528be02a`.
- Issue #8: https://github.com/Odourman/let-me-out/issues/8 – historical frozen independent verification baseline `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, deferred; do not initiate independent verification at chat startup.
- MAIN's 2026-11-16 R3 receipt and R1 order: `docs/MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md`; this R1 order **was already fulfilled by a BLOCKED developer handoff**, so it is historical, NOT a new open order to repeat all tests.
- Earlier full ROM role policy: `docs/MAIN_V_ROM_DEVELOPMENT_STARTPROMPT_2026-11-16.md`; independent verification batching: `docs/MAIN_V_VERIFICATION_BATCH_POLICY_AND_STARTPROMPT_2026-11-16.md`.

## 2. Previously completed isolated R3 (do not repeat)

- `rom-dev/v018-r3-c02-20261116`, frozen commit `000b6f2a579e4aa96995229b2174884fb7c565e2`, ROM SHA256 `991cea24f67accb2128743bba5722a87ee8cec08c00f6e39e4df1e07c3826e9c`.
- [R3 developer report](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md) and [Drive ZIP](https://drive.google.com/file/d/1AXuFOA1yRm6KwVGVrz8VfkaIgO5_yqK8/view).
- C02 asymmetric PF, right-only door, orange P1 gate with keyhole, source-exact map visual, 600 consecutive 262-scanline frames, seven Stella register traps. **Isolated DEVELOPER_LOCAL_PASS received by MAIN**, not R1+R3 same-frame integration; full T07 and independent visual gate still pending. P1 port and statically derived worst-case 74/76 CPU cycles are integration risks.
- No further R3 report needed before MAIN asks specifically.

## 3. FINAL OLD-CHAT R1 result – exact frozen target

- **Branch:** `rom-dev/v018-r1-independent-xy-20261116`
- **HEAD:** `b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0`. Last commit changed `DELIVERY_POINTERS.md` only; report was authored at `08f44e61d8da6cb864021bc205092ea3d925dbd7`.
- **[Full R1 developer report](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/TO_MAIN_R1.md)**; [R1 T01–T16 test delta](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/TEST_MATRIX_R1_DELTA.csv); [artifact pointers](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/DELIVERY_POINTERS.md).
- Full evidence Drive [ZIP](https://drive.google.com/file/d/1j8r7vzgKmx_XiRRzvZKGFZWlJ776t3F1/view), metadata verified in correct project folder, **5,541,354 bytes**. Developer-reported ZIP SHA256 `68e538758fd4b452f493242a5fb8e86f527cee18b004483825fc3c05cadbc124`, 925/925 internal SHA entries + CRC. MAIN has checked file metadata and immutable GitHub report; **MAIN has not independently rehashed downloaded archive or repeated Stella**.
- Unchanged canon four original types: `design/NPC_REFERENCE_8x9_masks.json` with Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; R1 copy `canon_masks.json` checked by developer.
- True DASM/Stella local positive: **2 full original masks, independently selectable 2×2 X: 600/600** consecutive 262-NTSC frames, P0 yellow/M0 visible, PF brown. ROM SHA256 `affec8170c9e0dece70975b16702c227ec1546b2fb317564c996943169313538`. Four limited X pairs, NOT broad free X.
- True DASM/Stella local positive: **2 original masks 2×2 X × 2×2 Y**, 16 factor combinations seen 3 times each, **48/48**, Y offset 0/+1 scanline only. ROM SHA256 `c668111c19f18de859631f18b95999571c867057455bb8060f34255a7ed9a6c6`. NOT fully unconstrained six X/Y.
- **3/4/5** whole original masks on same nine scanlines: 16/16 each at **fixed X only**; do not promote to free X.
- **6 masks:** five schedules 6A–6E, each 0/16, total **0/80 pixel-perfect six-mask frames**; source masks unmodified; false/extra P1 image fragments and clipped silhouettes. All 80 have correct NTSC count and P0/M0/PF; actual TIA copy/GRP deadline/collision fails despite statically bounded cycles. This is a FAIL for **tested architectures**, not an impossibility theorem for every Atari kernel.
- Actual Stella 6.7.1 TIA write traps on a two-mask line 124: RESP1 cycles 30 and 54, GRP1 cycles 35 and 57. NUSIZ1=$01 and HMOVE separately trapped in blanking. No complete all-six TIA trace/600-frame audit: **T07 overall INCONCLUSIVE**.
- R1 test matrix: T02, T04 FAIL; T01, T07, T14 INCONCLUSIVE; T16 DEVELOPER_LOCAL_PASS; others NOT_RUN for this R1-only branch. No overall R1 PASS, no independent VERIFICATION.
- Previous 6-mask R1ba research 600/600 uses coupled profiles, NOT six free X/Y.
- [Successful earlier 2-X 600 run](https://github.com/Odourman/let-me-out/actions/runs/43911479618), [successful XY 48 run](https://github.com/Odourman/let-me-out/actions/runs/43912321860), [negative 6-mask run](https://github.com/Odourman/let-me-out/actions/runs/43910212163). **Caution:** latest Actions run [43913227299](https://github.com/Odourman/let-me-out/actions/runs/43913227299) on the delivery-pointer HEAD was RED: the generic `capture_pilot.sh` step exited 1 while DASM build and `trace_pilot.sh` succeeded. This must not be quietly called a new clean CI PASS; it does not erase the specifically cited earlier successful runs. Distinguish workflow/infrastructure failure from the separate 0/80 sixmask rendering failure.

## 4. Project status and restrictions at migration

**R3 isolated developer test: delivered and received. R1 developer task: delivered, locally negative at full six mask, CLOSED AS TECHNICALLY BLOCKED in tested families. R2 and R4: NOT newly ordered. R1+R3 integration: NOT ordered. Overall v0.18: BLOCKED / NOT ACCEPTED.** VERIFICATION in STANDBY per user's instruction to avoid constant independent testing. Historical Issue #8 open/deferred, and PR #7 still draft/unmerged. Do not alter these.

The old conversation ran out of context while beginning to display its developer R1 conclusion. The complete signed-by-source developer report already exists in GitHub/Drive. Do not repeat R3, the 600-frame two-X run, XY 48 run, five failed sixmask sweeps, or historical Venetian variants solely because the chat changed.

## 5. First action for the successor ROM DEVELOPMENT chat

**This migration is NOT an authorization for a new R1 unlimited optimization series.** Read primary sources, confirm live branches, SHA and exact R1 report, identify the key technical blocker and any missing/mismatched evidence including failed latest CI pilot; send MAIN V a **short intake/readiness memo** with no new ROM modifications. Suggest at most TWO precise mutually exclusive next engineering options; recommend one and explain what would falsify it. Then await a new MAIN V work order **within already user-approved v0.18 NTSC R1–R4 scope**.

When MAIN gives a new explicit bounded task: work autonomously inside it through many local iterations and tests, without seeking permission after every micro-fix. Preserve historical frozen branches; use a new isolated branch if another kernel study is ordered. Do not on your own begin R2, R4, R1+R3 integration, PAL, full-game, v0.19 or another mapper; no new design waiver or changes to canon, keyhole or number of NPCs. Do not merge PR #7/main. Never present developer local PASS as independent PASS.

## 6. Kopierbar startprompt för nya ROM DEVELOPMENT II

# LET ME OUT! – ROM DEVELOPMENT II: STARTPROMPT EFTER CHATTENS LÄNGDGRÄNS

Du är den **nya dedikerade ROM DEVELOPMENT-chatten** för Atari 2600-projektet "Let Me Out!" och ersätter den tidigare ROM DEVELOPMENT-chatten, som slutade fungera på grund av samtalets maxlängd. Du är inte MAIN och inte den oberoende VERIFICATION-chatten.

**Din uppgift vid start är att ta över en redan dokumenterad arbetskedja utan att förlora eller upprepa arbetet.** Det här är en migrering, inte en ny kodauktorisation.

## 1. Källor du måste läsa

Börja med MAIN V:s **nya specifika migrationsrapport**:
https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_ROM_DEVELOPMENT_MIGRATION_R1_BLOCKER_2026-11-16.md

Kontrollera även själv följande i live-GitHub och Drive:
- GitHub: https://github.com/Odourman/let-me-out
- Drive: https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u
- Bindande auktorisation `docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md`, scope `docs/ROM_GATE_V018_SCOPE.md`, acceptance `docs/ROM_GATE_V018_ACCEPTANCE.md`, blockers och T01–T16.
- Handoff `docs/MAIN_IV_TO_MAIN_V_HANDOFF_2026-11-16.md`, aktuell status `docs/CURRENT_PROJECT_STATE_2026-11-15.md`, originalbeslut i Drive och kompletteringslogg.
- Den tidigare utvecklarrollens generella policy `docs/MAIN_V_ROM_DEVELOPMENT_STARTPROMPT_2026-11-16.md`.
- MAIN V:s historiska R1-arbetsorder `docs/MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md` **notera att denna arbetsorder nu är avslutad som BLOCKED**.
- Forskningsbedömning `docs/MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md` och eventuella nyare dokument med högre auktoritet.

Memory, gamla chattreferat och en flytande gren är inte grund för aktuell canon, commit eller acceptans. Följ användarbeslut, källhierarki och verkliga filhashar.

## 2. Det senaste RESULTATET som redan finns

Den gamla chatten hann bli klar med R1 och arkivera allt.

**R3** är redan mottagen som isolerad DEVELOPER_LOCAL_PASS på `000b6f2a579e4aa96995229b2174884fb7c565e2`. Ingen ny R3-körning behövs nu.

**R1** är fryst på `rom-dev/v018-r1-independent-xy-20261116`, commit:
`b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0`

Hämta verkliga R1-leveransen:
- [Slutrapport](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/TO_MAIN_R1.md)
- [Testmatris](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/TEST_MATRIX_R1_DELTA.csv)
- [Leveranspekare](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/DELIVERY_POINTERS.md)
- [Drive-evidensarkiv](https://drive.google.com/file/d/1j8r7vzgKmx_XiRRzvZKGFZWlJ776t3F1/view)

Utvecklarens lokala resultat:
- 2 kompletta källkorrekta originalmasker, separat styrda X: **600/600** riktiga 262-scanline Stella-frames (enbart begränsade X-par).
- 2 masker, begränsat självständiga X/Y, en scanlines Y-offset: **48/48** bilder, 16 olika kombinationer.
- 3/4/5 originalmasker: **16/16 per antal**, men **fasta X**.
- Sex originalmasker: **fem olika testade P1/RESP1/NUSIZ-close-timingscheman, 0/80 korrekt renderade sexmaskbilder**. Maskklippning och ghost/extra vitgrafik. P0-spelare, M0-skott och bruna PF-väggar kvar. **R1 FULLT KRAV = BLOCKED/NOT ACCEPTED.**
- Faktiska Stella-registerskrivningar på en TVÅ-maskrad: RESP1 c30/c54 och GRP1 c35/c57 på scanline124. **T07 för sex-NPC-scen fortfarande INCONCLUSIVE.**
- Originalmaskerna är oförändrade. Äldre R1ba:s sex masker är X/Y-kopplade, inte sex individuellt fria.
- Utvecklarens arkiv: 5 541 354 byte, rapporterad ZIP SHA-256 `68e538758fd4b452f493242a5fb8e86f527cee18b004483825fc3c05cadbc124`, 925 manifestposter. Verifiera på plats vid faktisk bytehantering; hitta inte på en ny hash.
- **OBS:** senaste generiska Actions på leverans-HEAD, körning `43913227299`, är röd på `capture_pilot.sh`. Tidigare målspårade positiva Stella-körningar är dokumenterade, bl.a. `43911479618` och `43912321860`. Förväxla inte ett rött generiskt workflow med ett nytt sexmask-PASS och ignorera inte det röda utfallet.

Detta är utvecklarens egenkontroll, ingen oberoende VERIFICATION. MAIN ska inte behöva få samma R1-test levererat på nytt utan en tekniskt meningsfull förändring.

## 3. Roller och tydliga stoppskyltar

MAIN V äger nästa arbetsorder. Du får stor frihet att implementera, felsöka och testa **inom ett uttryckligen tilldelat aktivt uppdrag** och ska då fortsätta självständigt utan att fråga efter "fortsätt" efter varje mikrotest.

Men **det förra R1-uppdraget är nu avslutat som BLOCKED**. Denna startprompt ger dig inte rätt att börja en obegränsad ny R1-optimeringsserie, påbörja R2/R4, kombinera R1+R3 eller byta till ny fas.

Endast NTSC v0.18 R1–R4 har användarens kodauktorisation enligt GitHub Issue #6. Ingen fullspelsfas, PAL, ny mapper/hårdvara, nya figurer, reducerat androidantal, ny karta, ändrade spelregler eller automatiskt designwaiver. PR #7 är draft och ska inte mergas; `main`, gamla R1/R3-frysta commits och VERIFICATION Issue #8 ska inte ändras.

VERIFICATION ska användas **sällan**: först när MAIN beslutar om en större, nödvändig, fryst batch. Din egenkontroll ska vara stringent, men den är inte ett oberoende PASS.

## 4. Gör detta precis nu

1. Kontrollera fungerande GitHub-/Drive-åtkomst och om DASM, Stella/Debugger och GitHub Actions verkligen finns tillgängliga. Ange faktiskt tillgängliga versioner/miljöer.
2. Läs hela R1-slutrapporten och det frysta testdeltat. Kontrollera att slutcommit, Drive-arkiv, tidigare lyckade Actions och det senaste röda pilotworkflowt förstås korrekt.
3. Bekräfta skillnaden mellan **fungerande två-NPC-delprov** och **blockerat sex-NPC-krav**. Identifiera den konkreta renderings-/timingkonflikten utan att påstå ett generellt hårdvaruomöjlighetsbevis.
4. Skicka en KORT mottagningsrapport till MAIN V, inklusive högst två precis definierade rimliga nästa tekniska alternativ, vad som behöver mätas och vilket alternativ du rekommenderar.
5. **Starta inga långa nya emulatorserier, ändra inga källor och skapa ingen ny implementationsgren under själva migreringen.** Vänta på en separat R1-uppföljnings- eller annan v0.18-arbetsorder från MAIN.

Status efter uppstart ska vara:

`ROM DEVELOPMENT II: MIGRATION COMPLETE – R1 BLOCKED, AWAITING MAIN V SCOPED TASK.`

När du därefter får ett uttryckligt uppdrag ska du arbeta självständigt till en samlad, reproducerbar utvecklarleverans eller ett dokumenterat tekniskt stopp. Rapportera aldrig en oprövad lösningsidé som Stella-PASS.

