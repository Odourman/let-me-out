# LET ME OUT! – MAIN V: R1-F11 G0 HARD STOP mottagning inför MAIN VI

**Datum: 2026-11-17.** **Beslut:** F11:s frysta SOURCE-ONLY G0-FAIL har **MOTTAGITS och STÄNGTS SOM SCOPE-KORREKT STOPPLEVERANS**, klass `F11_SOURCE_ONLY_INFEASIBLE`. Det är **inte** en verifierad Atari-fysikalisk omöjlighetssats eller oberoende E02 VERIFICATION. **G1 NOT RUN – 0 nya F11-ROM, 0 F11-Stella-frames och 0 nya F11-DASM-/CI-/PNG-/ZIP-artefakter.** Full R1 **BLOCKED / NOT ACCEPTED**.

## Kontrollerad primärproveniens

- Utvecklarens original [fryst R1-F11 TO_MAIN](https://github.com/Odourman/let-me-out/blob/dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F11.md) på **commit `dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4`**, Git blob **`a9c67b0ed3822dc218e435d76719f8f431c37de1`**, isolerad branch `rom-dev/v018-r1-f11-g0-hard-stop-source-only-20261117`.
- Jämförelse direkt i GitHub mot fryst F10 `ef854d7436f1e1650827e2e19cc1b3d33a17f054`: **ahead=1 / behind=0**, exakt **EN NYTILLAGD Markdownfil** `rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F11.md`; inga ändringar av tidigare ASM, ROM, originalmasker, grafik, CI, main eller PR#7.
- [Formell specialistöverlämning i Issue #6](https://github.com/Odourman/let-me-out/issues/6#issuecomment-6946394788) är faktiskt mottagen; [F11 MAIN-auktorisation](MAIN_V_TO_ROM_DEV_II_R1_F11_FOUR_NUMERIC_X_P1_DIAGNOSTIC_ONE_ROM_AUTHORIZED_2026-11-17.md) var uttryckligen G0 före högst EN ROM. Specialistens STOPP vid G0 respekterar arbetsordern.
- Tidigare fryst F9 ROM SHA `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b` med TRE **BINÄRA** separata RAM-X och 144/144 Stella-PNG för tre rättvända originalmasker kvarstår ett historiskt **DEVELOPER_LOCAL/M AIN-avläst pixelbevis**, inte en fyrmaskig numeric-X-ROM.
- [PR #7](https://github.com/Odourman/let-me-out/pull/7) vid denna MAIN-kontroll **OPEN/DRAFT/UNMERGED** (HEAD `82667dae033f70570dce903f8e1d4866528be02a`), [Issue #8](https://github.com/Odourman/let-me-out/issues/8) separat historiskt VERIFICATION-uppdrag ej startat.

## Sakligt G0-hinder: förregistrerade mål och datastyrd positionering

F11 beställde **FYRA olika, rättvända 8×9-originalmasker M/F/SM/SF**, EN fysisk P1, gul P0, M0, bruna PF, 76 CPU-cykler/scanline och exakt två runtime-stimuli för numeriskt lagrade RAM-X i fysisk synlig TIA-CC: **A=[16,36,56,76]** och **B=[19,36,56,76]**. B ska flytta endast M med +3 CC; detta är INTE F9:s 2^n binära modekatalog.

F11:s source-only G0 kunde **inte** visa en konsekvent generell CPU-register-/TIA-counter-/START-/GRP1-deadlineplan för dessa exakta pixelpositioner. Rapporten visar två *villkorliga* och avgränsade blockerare:
1. För den F9-använda enkla `NUSIZ1=$01` close-copy-modellen med nominellt **17 CC** latens kräver exakt X-placering orealiserbara fraktionella CPU-skrivcykler **22⅓,29,35⅔,42⅓** (B först 23⅓), eftersom 6507:s registerskrivningar ligger på ett gitter om **3 TIA CC**. Olika interna fas-/START-latenser eller finjusteringsmekanismer skulle kunna ändra detta, men sådan *kontrollerbar individuell* mekanism finns inte styrkt för den begärda kandidaten. Det är **inte** generellt bevis mot all P1-timing.
2. För på varandra följande kopiestarter med **20 CC gap** (B:s första endast 17 CC) måste nästa `RESP1` nominellt skrivas omkring 17 CC före sin kopiestart, alltså **medan föregående åttapixelmönster fortfarande ritas**. Stella `Player::resp/tick` visar risk att det enda render-/sample-countertillståndet påverkas. Den konservativa säkerhetsmodellen `gap>=17+8=25 CC` är **ett tillräcklighetsvillkor för enkel ostörd sekvens, INTE universellt nödvändig TIA-gräns**.
3. En illustrativ fast opcodeplan kunde ge `WSYNC c50` eller `c53` och ändå ligga under 76, men den **läser inte fyra numeriska RAM-X för att välja generella X-tider**; den skulle vara två hårdkodade formationer och bryta uttryckligt F11-krav. G0-FAIL är därför **inte** bara "alla cykler tog slut".
4. F11 har ingen actual ROM/START-/GRP-latch-mätning för dessa fyra positioner och ingen godkänd ny kvantiserings-/occlusion-/mapperwaiver. Fulla, top-down M/F/SM/SF kan inte antas möjliga från F9:s tre binära originalmasker.

## Beslut och tydlig gräns vid migration

**MAIN V accepterar F11:s beslutsriktiga STOPP och källbaserade negativa utfall som avslutad auktoriserad G0-leverans**, utan att hävda att all numerisk fyra-X-geometri på Atari är omöjlig. Den fastställda tekniska huvudblockeringen efter F11 är fortfarande **R1 sex numeriskt individuellt fria X/Y med rättvända orörda ursprungsmasker, same-Y/shifted-Y och full P0/M0/PF-belastning**.

**INGEN F12, ny testvariant, reviderade fasvärden, ny F6SC/ARM/mapper, designwaiver, sex-NPC-ROM, R2/R3/R4-integration, PAL, gameplay, PR#7 merge eller oberoende VERIFICATION är utfärdad vid överlämningen.** Arbetet med F11 är **stoppat**. MAIN VI får först kontrollera **den faktiska** F11-källrapporten och MAIN:s mottagning, därefter utvärdera strategiska beslut inom godkänd NTSC v0.18 R1–R4-auktorisation, med eventuell ny, separat dokumenterad order endast när en relevant och hållbar källgrund föreligger. Om ett design- eller hardware-waiver faktiskt krävs ska användaren få ett precist beslutsunderlag; inget får smyginföras.
