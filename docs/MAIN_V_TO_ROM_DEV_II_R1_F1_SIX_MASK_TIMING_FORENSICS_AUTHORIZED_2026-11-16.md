# LET ME OUT! – MAIN V till ROM DEVELOPMENT II
## R1-F1: Avgörande rotorsaksanalys av sex P1-originalmasker

**Datum:** 2026-11-16. **Status:** NY, separat **MAIN V-arbetsorder** inom den redan uttryckligt användarauktoriserade diagnostiken v0.18 NTSC R1–R4 (GitHub Issue #6). **Detta är inte ett godkännande av ny implementationsfas, fullspel, ny hardware mapper, designwaiver, kombinerad R1+R3-rendering eller oberoende VERIFICATION.** Enbart nedanstående R1-F1 är aktivt.

## 1. MAIN:s beslut efter ROM DEVELOPMENT II:s migrationsrapport

Mottagning/migrering accepterad. Det frysta ursprungliga R1-arbetet är färdigt som **FAIL/BLOCKED på sex fria X/Y**, utan att utesluta att en annan teknik skulle kunna fungera.

ROM DEVELOPMENT II föreslog:
- **A:** NUSIZ1-close, två RESP1 och GRP1-maskbyte på samma rad.
- **B:** en begränsad verklig register- och pixeldeadlineanalys av två av de misslyckade sex-schemana.

**MAIN väljer B, inte A.** Huvudmekaniken i A är redan lokalt bevisad i små, begränsade 2X/2XY-prover; ytterligare samma tvåmaskbevis löser inte sexmask-blockeringen. Prioritet är nu ett kort, avgörande och falsifierbart underlag om **varför** sex originalmasker förstörs vid fysiska TIA-kopie-/grafikdeadlines, trots statisk <76-cykelplan.

## 2. Exakta frysta utgångskällor – kontrollera hash och lämna oförändrade

- Repo: https://github.com/Odourman/let-me-out
- Fryst R1-utvecklargren: `rom-dev/v018-r1-independent-xy-20261116`, HEAD `b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0`.
- [R1-slutrapport](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/TO_MAIN_R1.md), [testmatris](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/TEST_MATRIX_R1_DELTA.csv), [leveranspekare](https://github.com/Odourman/let-me-out/blob/b02ee3fe9e1ffe4bd77460ff43263a35e1f544e0/rom/v018/experiments/r1_free_xy/DELIVERY_POINTERS.md).
- [Google Drive-evidens ZIP](https://drive.google.com/file/d/1j8r7vzgKmx_XiRRzvZKGFZWlJ776t3F1/view), 5 541 354 byte, utvecklarrapporterad SHA256 `68e538758fd4b452f493242a5fb8e86f527cee18b004483825fc3c05cadbc124`, 925 interna SHA-poster.
- Generatorkällor `rom/v018/experiments/r1_free_xy/build_scaling.py` (N=5 referens, N=6 ursprunglig variant 6A), `build_six_sweep.py` (6B–6E), `analyze_six_sweep.py`, `capture_six_sweep.sh` och genererad DASM-listning från rapporterat originalarkiv. Originalmaskerna från `design/NPC_REFERENCE_8x9_masks.json` ska vara oförändrade.
- Mätetablerad tvåmaskreferens: två RESP1 vid scanline 124, c30/c54, GRP1 c35/c57. **Detta är tvåmaskprovens uppmätta cykler – använd dem INTE som sexmask-mätning.**

## 3. Uppdragets exklusiva kärna

**Välj exakt TVÅ representativa, redan misslyckade sexmask-implementationer:**
- **6B:** föreslagen STA RESP1 statisk sekvens c19/28/37/46/56/66; testad 0/16, tidig/sen maskklippning.
- **6C:** föreslagen sekvens c20/29/38/47/57/67; testad 0/16 och oönskat vitt 'ghost' vid vänster x0.

**Ta med EN tidigare positiv kontroll:** N=5 med fasta X från `build_scaling.py` (16/16 enligt utvecklarunderlaget). Den ska användas som referens för hur korrekt grupp-/maskdata ser ut, inte som ny fri-X-PASS.

### 3A. Först: forensisk jämförelse av befintliga data utan nya tusentals bildrutor

För 6B, 6C och N=5 ska du återanvända de frysta källlistningarna, original-ROM/hashar, 16-rutors-evidensen, pixelanalys och befintliga CI-artefakter. Verifiera att generatorkällan, CPU-tidtabellen och ROM-filerna motsvarar verklig commit och inte bara en textförklaring. Dokumentera alla relevanta P1-initieringar, NUSIZ1, GRP1-mönsterbyten, återställningar, WSYNC, färg och P0/M0/PF i en exakt händelsetabell.

Identifiera minst ett eller flera **specifika skadade originalmaskrader** för vardera 6B och 6C, jämför förväntad källbit med faktiskt skärmpixel och ange exakt om förlusten är tidig/sen, 'ghost' vid x0 eller utebliven/sammanblandad kopia. Bildbearbetning är endast analys av verkliga Stella-rutor, aldrig ersättning för dem.

### 3B. Verkligt Stella Debugger-trace för de två felen

Om Github Actions kan köras igen, bygg exakt 6B och 6C med DASM från källor och reproducerbara standard-F6 16KB-ROMs. Kör verklig Stella 6.7.1 med debugger. Rikta mätningen till det relevanta nio-raders originalmaskbandet och ta **ett representativt skadat rasterband/scanline per variant**, inklusive:
- PC, bank, frame-ID, scanline, **uppmätt** CPU-cykelposition och faktisk TIA-registeradress/värde för `RESP1`, `GRP1`, `NUSIZ1`, ev. `HMOVE` och varje avgörande P0/M0/PF-write;
- alla sex RESP1-strober och alla faktiskt utförda GRP1-skrivningar på vald kritisk rasterrad, med tidsordning, pixeldeadline och förväntad/observerad P1-kopieffekt;
- visuell rå bild från samma deterministiskt definierade frame/ROM, jämförd med sex käll-exakta maskers förväntade synliga pixlar.
Skilj **uppmätta trap-händelser** från byteberäknade instruktionscykler och från teoretiskt uppskattad TIA-pixelstart. Ange explicit när en händelse inte kunde fångas eller då följdbevis saknas.

**Viktigt om debugger:** använd fungerande `break + run` / `trapWriteIf` och bekräftat PC/scanline/bank – det gamla mönstret `break; frame; step` gav fel PC. Trap stannar efter skrivinstruktionen. Kör ingen full 600-frame audit bara för denna rotorsaksuppgift.

### 3C. Högst EN riktad falsifierande A/B-mikroprob vid behov

Om, och bara om, 3A/3B ger en tydlig mätbar hypotes som behöver en liten skillnadskontroll får du skapa en **isolerad R1-F1 diagnostisk gren** och göra **en enskild minimal registerordnings-/fasvariant** som jämförs mot en av de två historiska sex-varianterna, med max 16 verkliga bildrutor i det aktuella testläget. Bevara båda bas-ROM:erna, masks, skyltning, NTSC, P0/M0 och PF. Ingen större serie optimeringar, ingen ny sexmask-kernelarkitektur och ingen ändrad design. Negativt resultat är också en godtagbar färdig leverans.

Ingen godkänd tvåmask-studie ska upprepas annat än som direkt källa till referensdata.

## 4. Vad räknas som KLART?

Avsluta som **F1-CAUSE_IDENTIFIED** endast när källbyte, verkliga TIA-write-positioner och Stella-pixelavvikelser tillsammans pekar på en reproducerbar orsak till minst en typ av sexmask-skada som observerats i båda scheman eller tydligt avgränsas per schema. Om en generell orsak inte kan bevisas, redovisa partiell lokalisering plus **F1-INCONCLUSIVE**. Etiketterna gäller **forensikens resultat**, aldrig fullt R1-PASS.

**Stopp:** när båda utvalda käll-/pixelprofilerna och nödvändiga trace-data har granskats och slutsatsen kan försvaras, eller när tillgången till nödvändig verklig Stella-exekvering inte kan ordnas. Vid verktygs-/CI-hinder, skriv blockerarrapport med exakt saknat bevis och möjliga genomförbara testvägar, i stället för att hävda att CPU-teorin är bevisad. Inga stora nya tester efter detta.

**Leverera en samlad `TO_MAIN_R1_F1.md`**, med:
1. fast källcommit, alla ingående ROM SHA-256, testmiljö/versioner, rena DASM-byggen eller explicit NOT_RUN;
2. variant 6B vs 6C vs positiv N5-kontroll, en tabell över planerade och faktiskt uppmätta write-cykler (där de finns), per-kopia/delmask avvikelse och eventuella observerade reset-/deadlines;
3. källhärledda krav och rå autentisk Stella-bildevidens och TIA-debugger-screenshots/loggar, med readback-hashar;
4. slutsats som anger exakt vad som orsakar observerat FAIL, vad som inte har bevisats och vilka tekniska möjligheter som återstår;
5. vid uppnådd målbild: högst två skarpt avgränsade nästa alternativa utvecklaruppdrag, med rekommendation och falsifierbart stoppvillkor.

Följ utvecklarens vanliga egenkontroll utan att kalla detta en ny oberoende VERIFICATION. Batcha material till EN överlämning. Lägg större arkiv i projektets dedikerade Drivefolder och länka via GitHub Issue #6. Om någon ny kod skapas ska den vara i en egen ny branch, aldrig på det frysta originalet eller på main.

## 5. Gränser och ansvar

R1:s sex individuellt X/Y-rörliga originalsilhuetter förblir **FAIL/BLOCKED**. R3:s isolerade lokala PASS kvarstår. R2, R4, R1+R3 same-frame-integration och andra steg är inte beställda. Ingen reducering av antal androider, originalmaskmodifiering, lägre skala, oacceptabelt flimmer, andra spelregler, PAL, v0.19, ny mapper, PR #7 merge, kod på main, och ingen designwaiver. VERIFICATION förblir STANDBY tills MAIN beställer en större fryst batch.

**MAIN:s rekommenderade teknikbeslut:** En kort verklig register-/pixeldeadlineforensik har högre förväntat värde än att demonstrera tvåmaskers close-retrigger på nytt. Lös inte problemet på papper genom att tolka F6-ROM som extra TIA-objekt eller upphäva 76-cykelgränsen. Börja R1-F1 efter att du har läst denna kompletta order.
