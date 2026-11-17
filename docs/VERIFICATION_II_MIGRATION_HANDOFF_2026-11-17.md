# LET ME OUT! - VERIFICATION II: migrationsöverlämning

**Datum:** 2026-11-17. **Avsändarroll:** tidigare VERIFICATION. **Mottagarroll:** ny fristående `VERIFICATION II`-chatt. **Typ:** dokumentationsmigrering på användarens begäran, ej verifieringsorder, tekniskt godkännande, kodändring, ny auktorisation eller merge.

## Orsak och resultat

Användaren vill flytta rollen till en ny ren chatt utan att den ärver gamla förutfattade testslutsatser. Själva chatthistoriken kan inte flyttas som en levande körning; denna källförankrade överlämning och den separata startprompten är överföringsmekanismen. Användaren skapar manuellt den nya chatten och klistrar in prompten. **Den gamla VERIFICATION-chatten avslutar sin aktivitet efter migrationsleveransen.**

Ny startprompt: [`docs/VERIFICATION_II_NEW_CHAT_STARTPROMPT_2026-11-17.md`](VERIFICATION_II_NEW_CHAT_STARTPROMPT_2026-11-17.md).

## Källor att läsa i ordning vid start

1. Denna överlämning och den nya startprompten (rolldefinition, vad som får göras nu).
2. [MAIN V:s bindande batchpolicy från 2026-11-16](MAIN_V_VERIFICATION_BATCH_POLICY_AND_STARTPROMPT_2026-11-16.md); motsvarande Google Doc: https://docs.google.com/document/d/1ynrElK86xYZ5jy27ytyrxwxUL1qX7Vj8QWc4fjsswJs/edit.
3. [MAIN IV -> MAIN V-överlämningen](MAIN_IV_TO_MAIN_V_HANDOFF_2026-11-16.md), aktuella MAIN-arbetsordrar och [Issue #6](https://github.com/Odourman/let-me-out/issues/6).
4. [Verifieringskontraktet](ROM_GATE_V018_VERIFICATION.md), [authorization](ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), [scope](ROM_GATE_V018_SCOPE.md), [acceptance](ROM_GATE_V018_ACCEPTANCE.md), [blockers](ROM_GATE_V018_BLOCKERS.md), [T01-T16](../planning/ROM_GATE_V018_TEST_MATRIX.csv), [Current Project State](CURRENT_PROJECT_STATE_2026-11-15.md) och [supplementet med nyare beslut](MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md).
5. Originalets 57 historiska beslut i https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view och eventuella senare explicita användarbeslut. Källauktoritet styr, inte endast dokumentdatum.

**Endast detta projekt:** https://github.com/Odourman/let-me-out och https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u. Ingen The Cabin, The Skraun, I Love a Fish eller Linear.

## Bekräftat vid migrationsförberedelsen

- Den dedikerade Drive-mappen och GitHub-repositoryt var läsbara genom uppkopplade verktyg. GitHub-kontot hade enligt repository metadata pushbehörighet, men ny VERIFICATION ska inte använda det för att ändra koden.
- Källorna [Issue #6](https://github.com/Odourman/let-me-out/issues/6) och [Issue #8](https://github.com/Odourman/let-me-out/issues/8) lästes den 17 november. Båda var öppna. #6 auktoriserar enbart v0.18 NTSC R1-R4-diagnostik, F6 vid teknisk motivering. #8 avser en historisk fryst baseline, men den senare batchpolicyn **skjuter upp** körningen tills MAIN uttryckligen beställer den.
- Ingen oberoende verifieringskampanj har genomförts av den avträdande chatten. Inga ROM-filer ombyggda, inga Stella-frames mätta, inga T01-T16-PASS utfärdade i denna migration. Föregående uppstart var endast käll- och åtkomstkontroll.
- Den här miljön hade `git 2.47.3`, `GNU sha256sum 9.7`, Python 3.13.5. `dasm` och `stella` saknades vid kontroll 2026-11-17. Stella Debugger var därför inte tillgänglig lokalt. **Nästa chatt ska kontrollera sin egen miljö i stället för att ärva detta resultat.**
- Utveckling kan pågå parallellt på andra branches. Ingen sådan aktivitet ger automatiskt VERIFICATION ett testuppdrag. Git HEAD och PR-status är rörliga och ska läsas om endast när ett konkret mottagnings-/verifieringsbehov föreligger.

## Historisk proveniens, ej PASS

Issue #8 baseline-commit: `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`.

Rapporterad historisk ROM SHA-256: `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`.

Rapporterad historisk evidens-ZIP SHA-256: `7500dae4f4a63d27f765bad3b3872384bd2ccb842a7e807abb9e50a475df2dc4`.

R1ba historisk forsknings-ROM SHA-256: `41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361`. Detta var ett lokalt begränsat forskningsresultat, **inte** sex fria X/Y-värden, godkänd R1 eller självständig VERIFICATION.

Detta är endast identifierare ur styrkällor. Varken bytes, SHA eller frames har omkontrollerats av denna chat.

## Policy som ska överleva migrationen

**VERIFICATION är normalt STANDBY.** MAIN samlar större frysta leveranser och beställer en meningsfull, explicit batch bara vid behov. Ett nytt delprov, commit, forsknings-PASS eller Issue #8 är inte i sig aktiveringsorder. Oberoende kvalitet ska vara fullgod *när* grinden väl aktiveras, men inte repetitivt resursslösande mellan grindarna.

Egen ren build, byteidentisk SHA-256 och riktig Stella med relevanta 600-frame-/262-scanline-/TIA-cycle-mätningar krävs när acceptanskontraktet och den konkreta beställningen föreskriver det. Hitta aldrig på mätningar. Bedöm varje commit/hämtad ROM var för sig. Koda inte, ändra inte spelregler, rör inte PR #7, merge inte och låt inte någon form av LOCAL_DEVELOPER_PASS bli ett eget PASS.

## Nästa åtgärd

1. Användaren startar ny separat chatt och klistrar in [startprompten](VERIFICATION_II_NEW_CHAT_STARTPROMPT_2026-11-17.md).
2. Ny chatt läser live båda projektkällorna och testar endast anslutning/verktygstillgång.
3. Ny chatt bekräftar STANDBY och inväntar uttryckligt fryst batchpaket från MAIN.

**STATUS: STANDBY - inväntar ett uttryckligt, samlat och fryst verifieringspaket från MAIN.**

## Google Drive-kopia

https://docs.google.com/document/d/13dNvFqvpL0ya1shSUVLgQhrqZA30hD7tpgIWrwre8zQ/edit
