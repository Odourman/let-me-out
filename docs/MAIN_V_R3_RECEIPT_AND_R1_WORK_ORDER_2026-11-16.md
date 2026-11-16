# LET ME OUT! – MAIN V: R3/C02 mottagning och nästa ROM DEVELOPMENT-uppdrag R1

**Datum:** 2026-11-16. **Scope:** endast redan auktoriserad v0.18 NTSC-diagnostik enligt Issue #6. Detta är MAIN:s projektledning och teknisk leveransmottagning, **inte** oberoende VERIFICATION, full v0.18-acceptans, spelcanonförändring, designwaiver eller mergeauktorisation.

## 1. MAIN:s dokumentgranskning av fryst R3/C02-utvecklarleverans

- Source branch `rom-dev/v018-r3-c02-20261116`, HEAD/leveranscommit `000b6f2a579e4aa96995229b2174884fb7c565e2`, avskild från draft PR #7 (`82667dae033f70570dce903f8e1d4866528be02a`), vilken alltjämt är open/draft/unmerged.
- [Utvecklarens fullständiga R3-rapport](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md), [leveranspekare](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/DELIVERY_POINTERS.md), [16-falls delmatris](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TEST_MATRIX_R3_DELTA.csv), [TIA-skrivlogg](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/R3_REAL_TIA_REGISTER_TIMING.csv).
- Test-ROM: 16 384 byte F6, rapporterad SHA256 `991cea24f67accb2128743bba5722a87ee8cec08c00f6e39e4df1e07c3826e9c`. Fyra bankkopior av en och samma 4KB-programbank, ej bevis för full F6-bankswitchingarkitektur. Historisk rebuild jämfördes enligt rapport med `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`.
- Google Drive [slutligt utvecklararkiv](https://drive.google.com/file/d/1AXuFOA1yRm6KwVGVrz8VfkaIgO5_yqK8/view), exakt metadata verifierad av MAIN: 3 420 134 byte, ZIP i rätt projektmapp. Utvecklaren rapporterar SHA256 `4b4c7325f0ea17b2f48c936164bbefae0ceac5bd6e32dfaad510b54558307113` och 729/729 interna manifestmatchningar. **MAIN har kontrollerat GH-rapporter och Drive-metadata men inte utfört en separat binär SHA-/Stella-rebuild av detta paket**. Dessa byte- och testpåståenden förblir utvecklarens evidens.
- Utvecklartester R3: enligt reproducerbar rapport exakt C02-vänstervägg 22/22 och högeröppning y9–12; 7040/7040 PF-samplingar; orange P1-overlay och 23 transparenta svarta keyhole-bitmapbitar; 466 pixeländringar inom x406–421; 600 kontinuerliga frame-ID 11–610 med 262 scanlines i GUI-HUD; minimal positionslogik inklusive negativ låst-right; 7 faktiska registertraps på scanline 134 (`PF0,PF1,PF2` vänster cykler 7,15,22, höger 37,45,52, `GRP1` cykel 62). Källberäknad värsta linje 74/76, **inte generell uppmätt worst-case över alla scener och frames**.
- Testmatris T09–T12,T14,T16 `DEVELOPER_LOCAL_PASS`; T01,T07 `INCONCLUSIVE` globalt; övriga åtta `NOT_RUN`. Nyckelhålets slutliga visuella läsbarhet får enskild oberoende bedömning i senare batch.

**MAIN-beslut:** R3/C02 är **MOTTAGEN SOM AVSLUTAD ISOLERAD UTVECKLAREGENKONTROLL** på fixerad commit, med separat behållna integrationsrisker. R3 markeras inte som oberoende PASS, och v0.18 i sin helhet fortsätter **BLOCKED / NOT ACCEPTED**. Ingen kod från R3-grenen mergeas till PR #7 eller main nu. Issue #8:s frysta historiska baslinje förblir vilande. Ingen VERIFICATION beställs för R3 ensamt enligt användarens 2026-11-16-policy.

## 2. NY SEPARAT ROM DEVELOPMENT-ARBETORDER: R1 sex individuellt placerbara androidsilhuetter, NTSC

**Order utfärdad av MAIN V 2026-11-16 inom befintlig Issue #6-auktorisation.** Detta är nästa och ENDA aktiva utvecklingsuppdrag efter avslutat R3/C02. ROM DEVELOPMENT får arbeta självständigt genom interna iterations-/teststeg men inte påbörja R2, R4, integrerad R1+R3 eller senare ROM-steg utan MAIN:s separat utfärdade order.

### 2.1 Teknisk målsättning
Visa i en **enda körbar, källreproducerbar v0.18 NTSC-diagnostik-ROM**, utan oönskad turnering/blinkning, följande på samma eller direkt överlappande rasterhöjder:
- **Exakt sex vita androider**: 2 stora män, 2 stora kvinnor, 1 liten man, 1 liten kvinna, med källbyte-exakta godkända 8×9-originalmasker och tydligt identifierbar kategori;
- sex självständigt begärda och individuellt uppdaterbara X-positioner och även prövade individuellt olika Y-positioner. Färdiga tre kopplade X/Y-profiler uppfyller INTE detta mål; ingen måste ha full AI eller joystickstyrd NPC-logik, förprogrammerade deterministiska banor räcker som diagnostik;
- en synlig fullstor **gul P0-spelare** och ett aktivt, synligt **M0-testsymbolskott** som inte systematiskt försvinner;
- två källspårbara bruna PF-väggkanter som testunderlag. Ingen öppningsbar dörr eller key/O1 i detta uppdrag, men dokumentera hur PF/P1/CPU-resursallokering påverkar senare same-frame R3-integration.

### 2.2 Riskstyrd intern arbetsordning (inom ETT R1-uppdrag)
1. **Käll-/felanalys** av historiska R1ba (tre kopplade profiler, 600/600), SEX_X_FREE A (100/600 per NPC, oacceptabelt flicker), SEX_X_FREE B (PF-grova maskliknelser), Venetian A1/A2/VDEL (ofullständig originalmask), RESP1-rotorsak och den ännu oprövade NUSIZ1-close-retriggering-hypotesen. Läs faktiskt källfiler och råa Stella-bevis, och sammanfatta varför de visade delresultaten inte räcker.
2. **Mät först den avgörande primitiva begränsningen:** i verklig Stella Debugger skapa giltig `STA RESP1`/NUSIZ/GRP1/HMOVE/VDEL-trace med exakta PC, bank, scanline och CPU-cykler; prova två **olika fullständiga original 8×9-masker** på samma höjd och med två **fritt valda X** i en och samma bildruta, plus gul P0 och M0. Om relevant, testa särskilt NUSIZ1-close retriggering som hypotes, inte som förmodat färdigt svar.
3. Först efter ett verkligt läsbart positivt 2-NPC-försök: 3→6 NPC med sex oberoende X och därefter flera **oberoende Y-banor** och minst två belastningsprofiler (exakt samma Y samt delvis angränsande/överlappande Y), inklusive korsningar/överlappning som diagnostik. Om två inte fungerar efter rimliga alternativa verkliga försök: dokumentera **FAIL/BLOCKED** tydligt i stället för att fejka sex-PASS.
4. Pröva/rapportera hela synliga scengruppen med P0+M0+PF, 600 följande frames när relevant T01 kräver, 262 NTSC scanlines, faktisk GUI-grafikgranskning per mask/individ, verkliga TIA-write traps och cykelbudget på värst belastade linjer. Verifiera objektens uppmätta synlighet/rytmiska blinkning och källmaskpixelintegritet. Målsättningen får INTE räddas genom ändrad figurform, färre figurer, 1/6-bildruteflimmer eller statiska kopplade koordinatprofiler.

### 2.3 Tekniska begränsningar och integrationslogik
- Använd en isolerad NY R1-gren/underkatalog; PR #7, R3-grenen, historical Issue #8 och `main` orörda.
- Nya assemblerstrategier och minitester inom NTSC v0.18/standard F6 får utforskas fritt, men inga extra TIA-objekt, RAM-banker eller 76-cykelundantag får antas. 16KB med fyra upprepade 4KB-banker tillför inte faktisk bankswitchingkapacitet.
- **Särredovisa P1-risk**: R3-port/nyckelhål använde P1 och källberäknad 74/76 rastercykler. R1 får inte påstå att samvisning med R3 är bevisad. Avsluta med ett konkret resurs-/scanline-gränssnitt för en senare explicit beställd integration; skriv inte sådan integration nu.
- Ingen oberoende VERIFICATION efter varje steg. Bevara egna negativa tester och ge MAIN EN samlad utvecklaröverlämning när R1 är löst eller tekniskt blockerad.
- Inga visuella designwaivers, inga ändrade antal/silhuetter/spelregler, ingen fullspelsutveckling, PAL, v0.19-kartcutover, ny mapper eller merge.

### 2.4 Leverans och testkrav
En källfryst Git-commit med körbar ROM och SHA256, reproducerbar DASM-build, riktig Stella-version och testrecept, originalmaskreferenser/hashes, 600-frame GUI-bevis där krav och resultat motiverar det, riktiga TIA-/CPU-cykelmätningar på kritiska horisontella/vertikala belastningar, per-individ synlighets-/maskpixeltest, status T01/T02/T04/T07/T14/T16 och motiverad NOT_RUN för övriga T01–T16, bildexempel samt historik över negativa tester. Skilj konsekvent `DEVELOPER_LOCAL_PASS`, `FAIL`, `INCONCLUSIVE` och `NOT_RUN`. Rapport `TO_MAIN_R1.md` med högst två val för MAIN om ett avgörande hinder kvarstår.

**Ingen VERIFICATION är beställd. Slutlig v0.18 fortsatt BLOCKED / NOT ACCEPTED.**
