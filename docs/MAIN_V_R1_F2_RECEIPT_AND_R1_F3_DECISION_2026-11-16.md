# LET ME OUT! – MAIN V: R1-F2 mottagen, tekniskt besked och nästa val

**Datum:** 2026-11-16. **Typ:** MAIN-käll- och autentisk bildevidensgranskning, **inte oberoende VERIFICATION eller fullt R1-godkännande**.

## Fryst F2 och kontrollnivå

- [ROM DEVELOPMENT II slutrapport](https://github.com/Odourman/let-me-out/blob/485a6c10047fb9b41e589ac3df724c1bc70f0283/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F2.md), branch `rom-dev/v018-r1-f2-independent-x-20261116`, HEAD `485a6c10047fb9b41e589ac3df724c1bc70f0283` (kontrollerad via GitHub). F1-basen `ea1c09f865c6ec5e3ecd984138a9631a0fb7c82a` är bevarad.
- Äkta [G0/G1 Stella ZIP](https://drive.google.com/file/d/1sWmbMhqS2LrsZ-o7dj-B9M4yCEqyukgh/view), exakt 476 677 byte, SHA-256 `8c5d7a35d9fa5553fcf49c2a792e6f05c891c4e30f631640b56bd917e50bedca`; 48 äkta råbilder, 16 per bas/M2/P1. Två 16 KiB F6-prober SHA256 `6ad0ac15acfb159f1412ca186545e7f9ab684847025dc3b467f82f81ca4792b1` respektive `39be11a80342d9881db90054b32717b1f128ffd1040f57e4e1dc918ceeeb38d2`.
- Äkta [G2 runtime ZIP](https://drive.google.com/file/d/1rG35l_rhdit-XfFmAvE3Xq5KOw-cf3So/view), 531 840 byte, SHA-256 `6f41cbaa38206e86a3671667469bb11ad8c3878ed392ab05ef80c628ba702836`; 32 råbilder, riktig Stella-Debuggertrap, ROM 16 384 byte, SHA256 `941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b`.
- [Korrigerat enbart läsande auditor-arkiv](https://drive.google.com/file/d/1DqAKKsKgjcF_es28QscTB9_b_YS0Psbf/view), 5 494 byte, SHA256 `dcc2a52b661db1c39f550cc75b9620cff348b41f9eff4b1234fa7efe6ab1f541`.
- MAIN laddade själv ned alla tre Drive-arkiv och kontrollerade faktiska ZIP-storlekar, SHA-256, ZIP-CRC, RAM-/ROM-källkod, 16 KiB F6-binärers filhashar och att alla fyra 4 KiB-banker i varje F2-ROM är byteidentiska. **Ingen ny emulatorstart eller oberoende clean DASM-rebuild har gjorts i MAIN.**
- MAIN analyserade även **alla 32 äkta G2-råbilder** direkt med en **annan egen Python/Pillow-pixelrutin**, från de fyra exakta originalmaskerna i `design/NPC_REFERENCE_8x9_masks.json` (Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`). Resultat **32/32 fullständig maskpixelunion exakt**; förväntade sex maskers sammanlagda **348 vita screenshotpixlar** varje bild; 16 rutor vardera för bild-X `129` och `135` för index 2; **8** faktiska lägesväxlingar. De fem andra maskernas vita pixelsiluetter och alla RGB-pixlar i den övriga synliga spelplancropen var oförändrade mellan typiska två lägen; endast x=129–150/y=96–104 påverkades. Normaliserade ursprungsformsiluetter identiska i alla 32 bilder. Därmed är bildresultatet inte enbart en grön etikett från utvecklarens egen audit.
- Observerade sex requested/rendered start-X i 900×300 debuggercrop: `43,75,129|135,183,243,303`; verkliga vita förstaspriter för de små med inledande tomma kolumner börjar två screenshotpixlar senare än geometriskt mask-start-X.
- F2-ASM `r1_f2_build_runtime.py` läser `FRAMELO` bit2 en gång utanför kernel; `CPX/BNE` får tredje `RESP1` c37/c38, komplementär `BEQ` håller fjärde `RESP1` c46; **EN** utrullad niolinskod, inte full sexformationsväxling. Denna **binära, periodiska en-koordinatsstyrning är inte generell koordinat-/NPC-motor**. Sista GRP1 c69 och WSYNC c72 enligt rapporterad statisk deadline, bara 4 cyklers beräknad marginal.

## CI-evidens utan överdrift

- [G1 rikta Stella run 43926065656](https://github.com/Odourman/let-me-out/actions/runs/43926065656): **SUCCESS**, developer/CI.
- [G2 riktad Stella run 43926447975](https://github.com/Odourman/let-me-out/actions/runs/43926447975): **FAIL** vid `REAL Stella G2`-steget, men innehåller faktiskt **32 riktiga rutor** och registertraps samt reproducerbart byggd runtime-ROM. Original-checkern relaterade visat *föregående* frame till debuggerns *nästa* frame-label och flaggade fel förväntad x-fas. Dess bildkostnader och P0/M0/PF/262-status var genomgående korrekta. Röd status tas inte bort.
- [Read-only re-audit 43927249076](https://github.com/Odourman/let-me-out/actions/runs/43927249076): **SUCCESS**, men steglistan visar att den **laddar ned redan insamlade PNG** och **inte kör DASM eller Stella igen**. F2-filens rapport-HEAD `485a...` är en efterföljande dokumentcommit, inte exakt samma som de tidigare testspecifika Actions-HEAD.
- MAIN:s pixelkontroll stärkte de råa bildresultaten, men omfattar inte full oberoende runtime-exekvering eller all maskpixelanalys för generella NPC-collisioner.

## Mottagning och kvarstående risk

**MAIN mottar och avslutar R1-F2 med `F2_GEOMETRY_LOCAL_PASS` och `F2_LIMITED_RUNTIME_SINGLE_X_PASS`, alltid med etiketten `DEVELOPER_LOCAL`.** Detta är ett verkligt mikroframsteg: EN originalandroid kan ändra X med **en CPU-cykels** tidsstyrning i **samma** ROM, samtidigt som fem andra står kvar och alla originalmasker finns kvar. Det är inte en fri tvådimensionell positions-/AI-motor.

**Fullt R1 för sex individuella X/Y = BLOCKED/NOT ACCEPTED.** R3 är isolerad lokal PASS med P1-port/resurskonflikt, R2/R4 och R1+R3 inte beställda, PR #7 draft och omergerad, Issue #8 fryst, VERIFICATION STANDBY. Inga grafiska kompromisser eller äldre konstituerade tester blir implicit PASS.

**Beslut:** Nästa enda användbara forskningsfråga inom redan auktoriserat v0.18 R1 är om **ytterligare EN android** kan få en **separat** runtime-X-väljare samtidigt som index2 fortsätter ha sin. Se separat [avgränsad R1-F3-order](MAIN_V_TO_ROM_DEV_II_R1_F3_TWO_INDEPENDENT_X_RUNTIME_FEASIBILITY_AUTHORIZED_2026-11-16.md). Detta dokument ensamt är en mottagning, inte en ROM-kodorder; F3-dokumentet är arbetsordern.
