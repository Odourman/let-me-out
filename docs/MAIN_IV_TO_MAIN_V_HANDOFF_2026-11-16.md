# Let Me Out! – MAIN IV till MAIN V: verifierad överlämning 2026-11-16
**Status:** MAIN IV överlämnar ledningsansvaret. Detta är ett DATUMSTÄMPLAT statusdokument och skapar inte ny auktorisation, nytt gameplay eller oberoende VERIFICATION.

## Sammanfattning för nästa huvudchat
Skapa tre separata chattar: `MAIN V` (ledning), `LET ME OUT! – ROM DEVELOPMENT` (DASM/6502/Stella-kod och egenkontroll), `LET ME OUT! – VERIFICATION` (självständig ombyggnad och bedömning). MAIN V ska inte själv agera kodare eller verifierare; rollerna överlämnar artefakter via GitHub/Drive. Färdiga prompttexter ligger i [MAIN V startprompt](MAIN_V_STARTPROMPT_2026-11-16.md) och [rom-/verifieringsprompter](MAIN_V_ROM_DEV_AND_VERIFICATION_STARTPROMPTS_2026-11-16.md). Användaren måste själv skapa chattarna; detta är bara förberedda instruktioner.

## Ground truth kontrollerat direkt vid handoff
- Projekt: **endast** `Odourman/let-me-out` och [Atari 2600 – Let Me Out!-mappen i Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Inga andra projekt, ingen Linear.
- GitHub `main`-HEAD före detta handoffs nya dokumentcommits: `9b76623c2b06a43dd79f49479ca7382eca8ef683`. **Läs om aktuell HEAD vid start**, eftersom denna rapport i sig kräver nya dokumentcommits.
- [Draft PR #7](https://github.com/Odourman/let-me-out/pull/7): öppen, draft, `rom-dev/v018-ntsc-diagnostic` HEAD `82667dae033f70570dce903f8e1d4866528be02a`; EJ mergad.
- [Issue #6 / auktorisation](https://github.com/Odourman/let-me-out/issues/6): enbart **v0.18 NTSC diagnostik R1–R4, 16 KB F6 om motiverat**. Detta tillstånd är senare än vissa gamla formuleringar `inte auktoriserad` i historiska Drive-dokument. Varken andra scenfamiljer, fullspelsimplementering, PAL, ny mapper eller grafisk waiver har auktoriserats.
- [Issue #8](https://github.com/Odourman/let-me-out/issues/8) är äldre, ännu inte genomförd **oberoende** VERIFICATION av fixerad commit `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`. Inte samma som modern research-ROM.
- [MAIN IV 2026-11-16 checkpoint](MAIN_IV_CHECKPOINT_2026-11-16.md) + [Current Project State](CURRENT_PROJECT_STATE_2026-11-15.md) + [11 extra beslut](MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md) + originalets 57 beslut i [Drive-handoff](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view?usp=drivesdk) bildar orienteringskedja. Vid källkonflikt gäller användarbeslut/högre bindande källa före senare eller lättare dokument.

## R1a–R1ba forskningsstatus – lokal, inte accepterad produktions-R1
**R1ba senaste positiva kombinerade teknikprov:** [Actions 43884511590](https://github.com/Odourman/let-me-out/actions/runs/43884511590), en och samma standard F6/NTSC-prototyp `16,384` byte, originala sex 8×9 NPC-masker (M,M,F,F,SM,SF), gul P0 och ett M0-testsymbolskott, **tre kopplade runtime-X/Y-lägen**, **två speglade bruna sidoväggar**, exakt 262 scanlines och noll saknade/extra vita pixlar: **600/600 lokalt PASS**. ROM SHA256 `41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361`. [Teknisk handoff](https://github.com/Odourman/let-me-out/blob/research/main-iv-r1ba-integrated-xyz-pf-20261116/docs/MAIN_IV_R1BA_INTEGRATED_X_Y_PF_SIX_ORIGINALS_600_STELLA_2026-11-16.md). [Drive ZIP](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view?usp=drivesdk), 3 930 298 byte, 600 autentiska Stella PNG. ZIP SHA256 `f8dd41e62939aa1699d80f70df0c5b5081b87441a1e2c740ff2786139908f325`, verifierat i MAIN IV:s ZIP-integritetskontroll.
**VIKTIGT:** De stora paren är NUSIZ-kopplade och X/Y-profilerna är 3 ihopkopplade lägen, inte **sex individuellt fria X/Y**; ingen full R1, ingen full R4 och ingen oberoende VERIFICATION. De fyra F6-bankerna är upprepningar av samma 4K kod; detta bevisar inte verkligt full-game-bankswitching.
**R1ax:** [Actions 43883269341](https://github.com/Odourman/let-me-out/actions/runs/43883269341) hade ett 600/600 lokalt positivt sidoväggsjobb men total workflowstatus `failure` på grund av två avsiktliga negativa kontrollfall. Skilj dessa vid mottagningsgranskning.
**R3:** [källgranskning](MAIN_IV_R3_RIGHT_DOOR_SOURCE_AUDIT_2026-11-16.md): v0.18 PR#7 innehåller asymmetrisk `CTRLPF=0`-idé, separata LEFT/RIGHT-PF-skrivningar och P1-portfärg. Äkta Stella D01–D03 (stängd vänster, enbart höger öppnar, orange port, svart tydligt nyckelhål) **inte verifierat**.

## Bindande testkrav och kvarvarande blockerare
[Scope](ROM_GATE_V018_SCOPE.md), [acceptans A01–E04](ROM_GATE_V018_ACCEPTANCE.md), [testmatris T01–T16](../planning/ROM_GATE_V018_TEST_MATRIX.csv), [stopp](ROM_GATE_V018_BLOCKERS.md), [Verifiering](ROM_GATE_V018_VERIFICATION.md).
- R1 sex androider, spelare, skott på samma Y-band: **sex individuellt rörliga X** och tillräckligt fri Y, korrekt ursprunglig silhuett, faktisk CPU/TIA-budgetsbevisning **ej löst** trots positiva delprov.
- R2 fem NPC + gul guldnyckel + P0 + M0, O1 med oförändrad key-X/Y och synlig återkomst: **ej visat**.
- R3 ensidig högerdörr, orange streck och **svart nyckelhål separat** i riktig ROM: **ej godkänt**.
- R4 täta förflyttningar/överlappar och korrekta NTSC-frames, register-timing: **ej fullt genomfört**.
- Oberoende ren rebuild, ändlig 16-test-gate/VERIFICATION/T14–T15: **saknas**.
**Övergripande status: v0.18 BLOCKED / NOT ACCEPTED.** Inga senare implementeringsfaser eller PR-merger.

## Rollgränser
- **MAIN V**: läser primärkällor, kontrollerar access och HEAD, prioriterar *ett* isolerat uppdrag åt gången, granskar ROM DEVELOPMENT:s mottagna leveranser och kontrollerar att VERIFICATION oberoende gjort egen rebuild. Håller status-/beslutsregister i GitHub **och** Drive. Endast faktisk användare beslutar designwaiver/utvidgat scope.
- **ROM DEVELOPMENT**: utveckling i eget begränsat branch-/PR-scope inom beviljad v0.18, kör DASM och Stella, source/ROM/frames/logs/SHA, märker `DEVELOPER_LOCAL_PASS` eller FAIL. Börja med en **R3 isolerad högerdörrdiagnostik** enligt källgranskning när MAIN V lämnar uppdraget; därefter R1 individuellt fria X, R2 nyckel/O1, R4.
- **VERIFICATION**: använd separat chat, egna verktyg och kodfryst baseline; börja med Issue #8 exakt commit; inga kodpatchar i den kod som verifieras, inga ärvda PASS från researchgrenar. Senare ny fixerad leverans kräver nytt oberoende test.

## Färdig uppstart
- [MAIN V startprompt](MAIN_V_STARTPROMPT_2026-11-16.md)
- [Separata ROM DEVELOPMENT och VERIFICATION startprompter](MAIN_V_ROM_DEV_AND_VERIFICATION_STARTPROMPTS_2026-11-16.md)
- [Google Drive projektmapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Kopia av denna handoff och uppstartsprompter i Drive ska läsas tillbaka efter skrivning.
**MAIN IV upphör att vara aktiv projektledare när MAIN V-chattens källkontroll är klar.**
