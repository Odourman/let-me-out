# LET ME OUT! – MAIN VIII G5AT: G5AR ENV-01 fresh Cloud-task specialist-PASS, inväntar originalråbevis

**Datum:** 2026-11-18. **Arbetsorder:** [Issue #19, G5AR ENV-01](https://github.com/Odourman/let-me-out/issues/19). **MAIN:s formella källgranskningsläge:** `G5AR_ENV01_FRESH_TASK_SPECIALIST_PASS_REPORTED_PENDING_RAW_EVIDENCE`. **Specialistens rapporterade klass:** `ENV_INSTALL_ONLY_PASS`; **inte ännu oberoende källbevisat av MAIN**. **Spel-/emulatorstatus:** `G5_FORMAL_OPEN`.

## 1. Kontroll av gällande original

MAIN VIII läste på nytt den [bindande Issue #19](https://github.com/Odourman/let-me-out/issues/19), [ROM DEVELOPMENT IV:s ursprungliga installationsrapport, fullständiga skript och råloggar i kommentar 6976852310](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310), och [MAIN VIII:s tidigare G5AS-delgranskning i kommentar 6976948435](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976948435). Vid ny kontroll innehöll **Issue #19 endast dessa två kommentarer**. Inget nytt rått, maskinläsbart verifieringsblock från den nypublicerade Cloud-tasken, ingen task-ID/cloud-källversionsrevision, ingen 8/8-verifikationslista med faktiska digest-värden fanns där att återläsa från GitHub. Det tidigare [G5AS-mottagningskvittot](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_VIII_G5AR_ENV01_INSTALLED_CURRENT_TASK_AWAITING_CLOUD_REPUBLISH_RECEIPT_2026-11-18.md) förklarar varför **samma-task två identiska prefix** inte var beständighet.

GitHub `main` före detta kvitto: `02e1986b4dc3b05b90cfae6b082e6d8ac177bab6`. Gällande käll- och auktoritetsdokument kontrollerade: [CURRENT STATUS](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md) och [G5 boundary](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md).

## 2. Ny specialistleverans till MAIN VIII – markerad som rapporterad, inte MAIN-observerad

ROM DEVELOPMENT IV:s nya textöverlämning den 18 november 2026 anger:

- En **ny Cloud-task** från den publicerade miljön `let-me-out` för `Odourman/let-me-out` användes.
- Den användarrapporterade terminalutskriften uppges visa att ett verifieringsblock kördes som **första shellkommando**, exitkod `0`, och att fem verktyg var tillgängliga **automatiskt via `/workspace/.g5ar-env01/bin`**.
- Rapporterade versioner: DASM-motor `2.20.14.1`, stock Stella `6.7.1` (metadata, ej emulatorkörning), Xvfb paket `2:21.1.16-1.3+deb13u4`, xdotool `3.20160805.1`, officiell Gopher2600 `v0.57.2`.
- **Åtta av åtta SHA-256-kontroller uppges ha godkänts**, inklusive startskriptet. Stella- och Xvfb-paketmetadata uppges ha kontrollerats i den nya tasken.
- `ROM_BUILD_VERIFIED=NOT_RUN`, `EMULATOR_RUNTIME_VERIFIED=NOT_RUN`; 0 DASM-assembleringar, ROM-byggen, emulator-/TIA-/CPU-mätningar och GitHub Actions enligt specialistens redovisning.

Dessa punkter **motsäger inte** Issue #19:s frysta installationsversioner. En successiv 8/8 SHA-kontroll skulle vara relevant bevis för beständighet. Men MAIN:s nuvarande källåtkomst innehåller endast **specialistens sammanfattning av användarrapporterad terminalutskrift**, inte den råa nya-task-utskriften eller de åtta individuella digesterna. Därför är `ENV_INSTALL_ONLY_PASS` i detta kvitto explicit **`SPECIALIST_REPORTED`** och får inte hävdas vara `MAIN_BYTE_VERIFIED` eller oberoende VERIFICATION II.

## 3. Kort återstående källkrav inom Issue #19 (ingen ny körorder)

För källgranskat slutmottagande: publicera i **samma Issue #19** den redan existerande nya taskens **oförändrade terminalutskrift/kommando**, dess exitkod, version-/PATH-/SHA256-lista (åtta individuella kontroller och förväntade värden), samt tillgänglig konfigurationsrevision/publiceringsidentitet. Redigera inte äldre frysta rapporter; lägg ett nytt kompletterande comment/artefakt. Om terminalutskrift bara finns som bild: lägg bifogad originalbild, markera `USER_REPORTED_SCREENSHOT` och påstå inte fristående loggproveniens. Om konfigurationsrevision saknas: redovisa `REVISION_NOT_EXPOSED`, uppfinn inte ett värde. Inga fler installationer eller nya tasks behövs **om den befintliga råutskriften kan arkiveras**.

Efter denna evidenskomplettering får MAIN göra ett explicit **source-only** slutkvitto och stänga Issue #19 **om** bevisen styrker reportens 8/8 och exaktscope. Det kräver **inte** att oberoende Verification II går igenom verktygsmiljön; ett godkänt toolchain-setup är ändå aldrig en ROM-/emulator-PASS.

## 4. Bindande gränser efter detta mottagande

Den tidigare underlagen dokumenterar installatör och startskript. Miljöinstallationsuppdraget utvidgas **inte**. Ingen Gopher HEADLESS F9-pilot, ingen Stella-debugger-mätning, ingen DASM-kompilering, ROM-/Actions-körning, G6/C0/S05/fem NPC, gameplayförändring eller PR-merge är auktoriserad. Historiska G5AJ/G5AL 2/2 FAIL, G5AH ursprunglig readback hash FAIL, G5AP OFFLINE_SYNTHETIC 98/98 PASS och G5AF bounded F9-instrumentering oförändrade. **`G5_FORMAL_OPEN`.**

**Beslut:** Positivt specialistresultat **mottaget och dokumenterat**. Fullt `MAIN_SOURCE_VERIFIED_ENV_INSTALL_ONLY_PASS` **avvaktar den redan rapporterade nya taskens ursprungliga råbevis i Issue #19**. Issue #19 förblir OPEN i väntan på en ren dokumentationskomplettering.
