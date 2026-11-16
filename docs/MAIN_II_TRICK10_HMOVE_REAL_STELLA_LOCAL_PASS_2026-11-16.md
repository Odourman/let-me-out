# MAIN II – Trick #10 HMOVE Fine Positioning: 4/4 lokala Stella-PASS

**Datum:** 2026-11-16. **Klass:** isolerad rådgivande standard-F6/NTSC-forskning, **inte full R1, inte sex fria NPC och inte oberoende VERIFICATION**.

## Primärkällor och hypotes

Originalpunkt 10 i `main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md` är **HMOVE Fine Positioning**. [Stella Programmer's Guide §8](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) beskriver `HMP0/HMP1/HMM0/HMM1/HMBL` och `HMOVE`: individuella 4-bitars tvåkomplementvärden mellan +7/-8 färgklockor; samtliga objekts förskjutningar verkställs av samma HMOVE-strobe. HMOVE bör följa `WSYNC`, och rörelseregistren får inte ändras 24 CPU-cykler efter stroben.

**Hypotes:** en isolerad `HMP0`-förskjutning kan flytta gul spelare samt vit P0-wide-android-kopia med intakta bitmaps utan att störa P1:s tre andra originalandroidmasker eller M0. Däremot ska detta INTE kunna bryta den fasta P0↔wide-kopia-X-kopplingen på 64 TIA färgklockor.

## Faktiskt, reproducerbart resultat

- **[GitHub Actions run 43813500872 – alla steg SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43813500872)**, testad kodcommit `9fda24794dafc6f4e7b25f3bb1720b324c508a27` på `research/main-ii-26-tricks-hmove10-20261116`.
- Artifact-ID **14201063902**, `main-ii-trick10-hmove-four-original-mask-evidence`. Artefakt-ZIP nedladdad och verifierad `testzip()==None`, 48 filer; 4 autentiska Stella-fasbilder + PC-stopp på `HMOVE`, källkod/list/sym, ROM och `evidence/audit.json`.
- Testad ROM: **16 384 byte standard F6** (4× identiskt 4096-byte-data), SHA256 **`702c5c9534e5486881441a43c60dea85d0ca02093dae4d56d237202f7c6d2c18`**, självständigt kontrollerad efter nedladdning.
- DASM 2.20.14.1; Stella 6.7.1 NTSC under Xvfb. Lokalt testresultat `LOCAL_PASS_HMOVE_P0_PAIRED_4_PHASES`.

| Fas | HMP0 | TIA-X-delta | Gul spelare raw GUI-X | Vit liten kvinna raw GUI-X | Tre P1 NPC-X | M0-X | Exakta maskpixlar + 262 NTSC |
|---:|---|---:|---:|---:|---|---|---|
| 0 | `$00` | 0 | 188 | 316 | 154, 268, 400 | 240–241 | PASS |
| 1 | `$F0` | +1 | 190 | 318 | 154, 268, 400 | 240–241 | PASS |
| 2 | `$D0` | +3 | 194 | 322 | 154, 268, 400 | 240–241 | PASS |
| 3 | `$30` | −3 | 182 | 310 | 154, 268, 400 | 240–241 | PASS |

GUI-X är pixelkoordinater i 1366×900 Stella-debuggerfönstret, två GUI-pixlar per TIA-färgklocka. Rå pixeljämförelse: alla fyra skilda originalandroidernas godkända 8×9-maskdata, den temporära gula spelarens 8×9-mask, exakt M0-testskott och **0 extra vita eller gula pixlar** i nio-radersbandet i samtliga fyra fasbilder. 262 NTSC-rasterlinjer i alla bilder.

**Verklig PC-stoppbild:** `HMoveStrobe` = `STA HMOVE` vid PC `$F07C`, scanline 4, CPU-cykel 0 och bank 0, mätt **före instruktionen**. Anropet står direkt efter `STA WSYNC` under VBLANK innan de synliga figurraderna. `HMP0` förbereds en gång per bildruta under blankning; `HMP1/HMM0/HMM1/HMBL` får uttryckligen noll.

## Slutsats och hård gräns

- **Trick 10: LOKALT DELBEVIS för exakt P0-parets finpositionering**, inklusive oförändrade P1 och M0, utan rasterfel. Det stärker användbarheten av HMOVE som byggsten i framtida lägen.
- **Ingen fri fjärde NPC:** kvinnans position är alltid **64 TIA-färgklockor efter P0**. HMOVE flyttar P0:s båda automatiska kopior lika mycket. Detta löser inte projektets sex oberoende NPC.
- Begränsat mätområde 0/±1/±3 CC; ännu inte hela -8..+7, kantposition, kombination med flera rörliga RESP1, överlappande masker eller 600 kontinuerliga HMOVE-bildrutor.
- M0-skottet ligger fortsatt på föregående rasterrad, inga PF-väggar/dörr, nyckel/O1, AI eller PAL. Koden ingår inte i fullspelet.
- Resultatet är **egenkontroll**; det får inte uppgradera R1 eller oberoende VERIFICATION. `main`, utkast-PR #7 och fryst Issue #8 orörda.

## Status för 26-testserien

Registret är `docs/MAIN_II_26_F6_TRICKS_TEST_REGISTER_2026-11-16.md`. 27–30 uteslutna enligt användaren. Nästa tekniska forskningsgrind: separat tvålinjers-rasterprov (#08) eller PF-resursprov (#05), med **oförändrade godkända masker** och tydligt mått på faktisk raster-/maskkostnad.
