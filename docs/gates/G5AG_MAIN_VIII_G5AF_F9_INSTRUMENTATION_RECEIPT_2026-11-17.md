# LET ME OUT! – MAIN VIII G5AG: källgranskad mottagning av G5AF LM-D22
**Datum:** 2026-11-17. **Roll:** MAIN VIII (mottagning/källkontroll, INTE oberoende VERIFICATION II).
**Klass:** administrativ mottagning av avgränsat specialistresultat; ingen ny auktorisation, ingen ROM-/kernel-PASS.

## Beslut och avgränsning
- [LM-D22/G5AF bindande ursprungsorder](https://github.com/Odourman/let-me-out/blob/9063a5ad8f725093e57c1a6e5c6848e2a9d60518/docs/gates/G5AF_MAIN_VII_LM_D22_F9_INSTRUMENTATION_ONLY_REPAIR_RETEST_AUTHORIZED_2026-11-17.md), [Issue #14](https://github.com/Odourman/let-me-out/issues/14).
- ROM DEVELOPMENT III fick **endast** reparera Stella/CI/Python-instrumentering och återkontrollera redan fryst F9 F6/NTSC 16 KiB-binär, med högst två Actions-mätkörningar. Ursprungligt rapporterat F9 SHA256: `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`. Ingen ny ASM/BIN/DASM-kompilering, emulatorpatch eller gameplayändring tillåten.
- [Fryst specialist-slutrapport vid c56b522](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/TO_MAIN_G5AF_F9_INSTRUMENTATION.md), [rå-CSV](https://github.com/Odourman/let-me-out/blob/c56b52284e7322fdf1c41812ae407429d8fb0f20/rom/g5af_f9_instrumentation_2026-11-17/G5AF_INSTRUMENTATION_EVIDENCE.csv), [officiell Drive-arkivkopia](https://docs.google.com/document/d/1MvpvQEAwQRlPr_CH2VVy-gY5LYjebzkPxcUDh0Rk71g/edit).

## Faktiskt MAIN VIII-kontrollerat
1. GitHub-branchen `rom-dev-iii/g5af-lm-d22-f9-instrument-only-20261117` pekar på fryst `c56b52284e7322fdf1c41812ae407429d8fb0f20`. GitHub compare mot auktoriserande main `9063a5ad8f725093e57c1a6e5c6848e2a9d60518`: 12 commits ahead, 0 behind, exakt **8 tillagda** workflow-/instrument-/dokumentfiler; inga befintliga filer modifierade. Ingen merge.
2. [Försök 1, Actions 44177844355](https://github.com/Odourman/let-me-out/actions/runs/44177844355) = `failure`, enligt specialist GUI-timeout/parserfel; bevarat som negativt resultat. [Försök 2, Actions 44178247577](https://github.com/Odourman/let-me-out/actions/runs/44178247577) = `success`. I samma andra run var `capture-original-f9` och `verify-preserved-artifact` två **lyckade jobb**, inte ett tredje emulatorprov.
3. Frysta CSV:n innehåller **två** Stella 6.7.1-debuggerstopp: `F9_000_M_RESP1`, PC 61936/`$F1F0`, `_sCycles=21`; `F9_000_F_RESP1`, PC 61944/`$F1F8`, `_sCycles=32`. Båda uppges vid frame 136, scanline 123, bank 0, med verklig numerisk TIA-text och native 320×228-bild. Sessionsfiler uppges ha 1709 respektive 1707 byte. Källrapporterade SHA-256-värden finns i specialistens beviskedja.
4. Drive-leveransens innehåll är åtkomligt och dess Google Drive-metadata visar explicit föräldramapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.
5. MAIN VIII har kontrollerat original GitHub-filer, compare, Actions status/jobstatus och Drive-innehåll. **MAIN VIII har inte fristående laddat ned och omhashat hela binära Actions-zippen, inte återkört Stella och inte utfört oberoende Verification II.** Actions readback-PASS och filhasharna är specialistens egenkontroll, inte nytt fristående bevis från MAIN.

## Saklig mottagning
**G5AF = `INSTRUMENTATION_READY_BOUNDED` som avgränsat utvecklarresultat, källkontrollerat mottaget av MAIN VIII.** Detta avser fungerande loggnings-/artefaktkedja kring fryst F9 och inte exakt RESP-strobe/START-latens, G5AD C0–C4/N1, riktig färgklocktesttid, originalhårdvaru-PASS, H4, full 5-NPC-kernel eller ett nytt spelbygge.
- `G5Z_G0 = INCONCLUSIVE_NO_ROM` kvarstår oförändrat.
- `G5AD = NO_BUILD_INSTRUMENTATION_BLOCKER` kvarstår avslutat historiskt och får inte skrivas om till PASS.
- `G5_FORMAL_OPEN`. `NEW_ROM/G1/G6/F12/H4/S05/FIVE_NPC/NEW_VERIFICATION/PR_MERGE_NOT_AUTHORIZED`.
- **LM-D22 är förbrukad. Inga fler G5AF Actions-mätkörningar eller övergångar får initieras med denna order.**
- GitHub Issue #14 får stängas som **completed: snäv instrumenteringsleverans**, aldrig som tekniskt fullspel-PASS.
- Nästa möjliga aktivitet för MAIN är att dokumentera ett **separat beslut** om ett framtida faktiskt TIA-kalibreringsprov. Specialisten får inte starta det utan ny uttrycklig användarauktorisation. Ingen tredje instrumenteringskörning.

## Historik och navigering
[Löpande auktoritets-/arbetskö-index](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) är navigationspunkt. Äldre G5AF `AUTHORIZED_NOT_YET_RUN`-avsnitt är historiska tidssnitt från tiden före slutleveransen, inte aktiv order. Äldre experiment, blockerare, F9-kod och ROM förblir frysta.
