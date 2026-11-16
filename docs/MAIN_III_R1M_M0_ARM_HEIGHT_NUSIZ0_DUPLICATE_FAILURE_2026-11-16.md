# LET ME OUT! – MAIN III R1m: M0-förflyttning mot armhöjd och NUSIZ0-konflikt

**Datum:** 2026-11-16. **Status:** `RESEARCH_FAIL`, strikt avgränsad skotthöjdskorrigering **INTE GODKÄND**. R1k fem originalandroider står kvar som senast lokal PASS för sin egen separata test-ROM. Full R1 fortfarande FAIL/BLOCKED.

## Användarens visuella anmärkning

"Skottet ser ut att komma från huvudet på spelaren. Skottet borde komma från armhöjd."

Den tidigare R1k-test-ROM:en hade:
- Temporär gul spelarsilhuett på GUI **y162–170**; utsträckta armar framträder cirka **y165**.
- M0 på GUI **x240–241, y160**, alltså **två rasterrader OVANFÖR spelarens huvud**, inte armhöjd.
- M0 utgjorde en diagnostisk testsymbol på egen rasterrad, inte accepterad gameplayfunktion.

Detta är ett verkligt presentations- och spelproblem och får inte beskrivas som en färdig fungerande skottrutin.

## R1m: faktisk teknisk provning

[Forskningsgren `research/main-iii-r1m-arm-height-m0-20261116`](https://github.com/Odourman/let-me-out/tree/research/main-iii-r1m-arm-height-m0-20261116).

[Actions #43831966155](https://github.com/Odourman/let-me-out/actions/runs/43831966155) – skärminspelning 600/600, fail-closed pixelaudit **FAIL**. [Evidensartefakt #14208674140](https://github.com/Odourman/let-me-out/actions/runs/43831966155/artifacts/14208674140), totalt 622 poster och 600 riktiga Stella-PNG, CRC-giltig ZIP SHA256 `b102234550811364b34fec82644f27c312b22610287a065a45162bb333aab499`.

Efter rättning av en analysbugg (den gamla auditens krav på exakt två gula pixlar på en rad där **också spelaren** nu syns) kördes [Actions #43832299232](https://github.com/Odourman/let-me-out/actions/runs/43832299232), exakt commit `d7b9e12edaa403671ccc99d2283a9a59f4909955`. Resultat: **FAIL, denna gång på verklig grafisk avvikelse**.

ROM: **16 384 byte NTSC standard F6** och SHA256 `2ea0317c862570d6ed44ae7bfde37a16cbc192bbed80520db7e7b7edcae5fec7`. Referens är tidigare R1k 5-NPC lokalt PASS SHA256 `99c2cc160713899a8662508a4eeafec956b3d9b4825668e66b135404ec79f2a7`.

Metoden: fjärde NPC:s redan laddade vita originalbitmönster ligger i X (`LDX SmallFemaleRows,Y`). Dess bit 1 är satt **endast** på dess top-down-rad 5 (= GUI y167). Ersätt R1k-kernelns enda trecykels `BIT FRAMELO` med trecykels `STX ENAM0` på samtliga nio rader, och släck M0 på den tidigare fristående y160-raden. Därmed belastas inte den kritiska rasterloopen med extra cykler och ingen av de fyra **olika** godkända vita originalbitmaptabellerna ändras.

### Uppmätt ny scen

- 600/600 konsekutiva Stella 6.7.1 NTSC 262-linjers frames.
- Fem hela vita ursprungliga NPC-instansmasker bevarade **600/600**.
- Det gamla gula M0-skottet vid **y160 är borta** 600/600.
- Nytt gult M0-skott vid GUI **x240–241, y167**, i samma figurband 600/600. Men **y167 är närmare spelarens midja/undre kropp än armraden y165**; alltså inte exakt den begärda justeringen.
- Varje frame har dessutom **två extra vita pixlar vid GUI x304–305, y167**. Totalt **1 200 icke godkända vita extrabildpunkter** över 600 frame. Detta är inte ett analytiskt falsklarm: råbilden visar dessa pixlar.
- Orsak: `NUSIZ0=$02` krävs för P0:s andra vita androidkopia. Detta TIA-läge ger också **en extra M0-missilkopia 32 TIA-färgklockor senare**. Den första M0-kopian är gul eftersom `COLUP0` ännu är gult; den senare kopian blir vit efter `STA COLUP0` ändrat P0 till vitt. Därför x240–241 gul, x304–305 vit.
- Pixelauditens `white_ghost_gui_pixels_total = 1200`, `yellow_ghost_gui_pixels_total=0` och `status=FAIL_OR_INCONCLUSIVE` är korrekt. Att fem NPC-masker ser korrekta ut är **inte tillräckligt** för godkännande.

Källor om TIA-hårdvaran: [Stella Programmer's Guide, kap. 6.1](https://www.atariage.com/2600/programming/2600_101/docs/stella.html): `ENAM0` styr missil, `NUSIZ0` styr både P0:s kopior och dess missilstorlek/antal. 

## MAIN III:s tekniska bedömning

**Skotthöjden är INTE löst i accepterad forskning**. Den första ändringen avlägsnar skottet ovanför spelarhuvudet, men levererar en **för låg skottlinje** plus ett grafiskt fel. Att flytta den andra M0-kopian så att den visuellt göms bakom en android är **ingen robust lösning**: hårdvarukollisioner kan ändå registrera en falsk träff, särskilt när NPC:erna rör sig. Undvik därför att kalla en dold spökprojektil "godkänd".

Korrekt uppföljande avgränsning:
1. Skottets start-Y bör motsvara **den faktiska arm-/mynningsraden i den slutligt valda spelarmasken** (nuvarande temporära testspelare ungefär y165). Skottets X ska också starta direkt från spelarens hand, inte 8+ GUI-pixlar därifrån.
2. Användaren har begärt armhöjd. Det är ett **visuellt krav för spelaren**, men inget godkännande att förvanska eller förenkla de **fyra godkända NPC-maskerna**.
3. Välj en renderer för skottet som **inte dubbleras av NUSIZ0/1** eller inför en korrekt, cykelmätt rastermaskering av just M0 i övrigt belastat band. Om det inte går inom R1k måste konflikten uttryckligen redovisas som teknisk gate; ingen ny mapper eller förändrad NPC-canon får smygas in.
4. Granska rörelse och kollisionskonsekvenser, inte enbart snygg testbild. Oberoende VERIFICATION måste senare granska samma ROM-hash.

**Inget från R1m är mergat till `main` eller ROM DEVELOPMENT:s draft PR #7.** R1k:s fem-NPC-forskning är opåverkad; dess skott vid y160 ska dock uttryckligen märkas diagnostiskt felplacerat.
