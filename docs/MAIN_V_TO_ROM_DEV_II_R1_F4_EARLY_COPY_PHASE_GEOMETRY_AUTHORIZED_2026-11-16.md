# LET ME OUT! – MAIN V → ROM DEVELOPMENT II
## R1-F4 – EARLY-COPY PHASE GEOMETRY: kontrollerad andra-individ X-fas

**Datum:** 2026-11-16. **Status:** UTTRYCKLIG NY, SNÄVT AVGRÄNSAD MAIN V-ARBETORDER inom användarens sedan tidigare auktoriserade **v0.18 NTSC R1-diagnostik** (GitHub Issue #6). **Inte** R2/R4, fullspel, mapperbyte, spelskärmsimplementation, PAL, R1+R3, nykälla-canon, fri sex-X/Y-acceptans eller oberoende VERIFICATION. Denna order får genomföras autonomt inom sin hårda gräns, även om första sonden fallerar.

### 1. DEN ENDA nya frågan

Kan vi, med samma **pixelkorrekta fasta 6B-sex-android-NTSC-kernel** och redan visad F2-rörlighet för **index2**, få en **annan separat ursprungsfigur index0** att ändra sin *faktiskt synliga* X genom att ändra timingen/fasen hos **dess första P1-close-retrigger / `RESP1`**, *utan* att de andra fem figurerna, någon originalmask, den gula P0-spelaren, det aktiva M0-skottet eller de bruna PF-väggarna ändras?

**BEGRÄNSNING:** Detta F4-uppdrag ska bara identifiera en fungerande **en-figur-förflyttningsgeometri** för index0. **Ingen två-individers dynamisk RAM-styrd runtime-ROM byggs i F4, även om en geometriprobe PASS.** I sådant fall rapportera vilket konkret nästa separat beslut skulle behövas.

### 2. Frysta källor och källens varning

Läs live och kontrollera SHA:
- [MAIN:s F3-mottagning / personligt verifierade negativa Stella-pixlar](MAIN_V_R1_F3_RECEIPT_AND_PHASE_BLOCKER_2026-11-16.md).
- [Fryst ROM DEVELOPMENT F3 slutrapport](https://github.com/Odourman/let-me-out/blob/65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F3.md) och generator `r1_f3_build.py`.
- F3 fryst **`65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190`**. Skapa **NY isolerad branch** från exakt den commiten, t.ex. `rom-dev/v018-r1-f4-early-copy-phase-20261116`; skriv F4 endast till `r1_f4_*`-filer, inga bakåtändringar av F3 eller F2.
- F2 fryst `485a6c10047fb9b41e589ac3df724c1bc70f0283` och fungerande **EN** RAM-styrd `index2`-X `129↔135`; F2-F6-ROM SHA `941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b`.
- Pixelkorrekt original-6B-ROM SHA `36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4`, sex positioner **[43,75,129,183,243,303]** i 900×300 Stella-debuggercrop (två screenshot-pixlar per TIA pixel).
- [Original fyra NPC 8×9](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json), blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, låsta typer index0/1 stor man, 2/3 stor kvinna, 4 liten man, 5 liten kvinna; **9 källrader inklusive tre tomma för små**, data bytes får aldrig justeras.
- Standard F6 16 KiB/NTSC, bank 0 kernel, DASM 2.20.14.1, Stella 6.7.1 med råa autentiska debuggerbilder. P0 gul originalspelarproxy, M0 aktivt skott, brun PF. NUSIZ1 ursprungligt `$01` och HMOVE endast under den redan använda blankningen. Inga extra TIA-objekt, inget Playfield-spelrum, inget R3-dörrprojekt.
- Hårdvarukällan [Andrew Towers – TIA Hardware Notes / retriggering](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) är **rådgivande hypotes**. `RESP1` ändrar en intern positionsräknare, inte nödvändigtvis en huvudkopias synliga X i samma rasterrad. Studera exakt close-start och andra resetens c28-gräns, men behandla inte dokumentet som PASS på vår ROM.

### 3. G0 – obligatorisk SOURCE-only preflight utan nya ROM

Gör en tabell över exakt nio källrader, första och andra `RESP1`, första `GRP1`, P0/M0 och sista `GRP1/WSYNC`. Frysta förstacase:
- baseline 6B `RESP1[0] c19` ger **renderat X=43**.
- fryst F3 `RESP1[0] c20` ger **renderat X=43 (GEOMETRY_FAIL)**, fast att `PC=$F1D1`, scan123 och cycle20 faktiskt mättes.
- andra figuren `RESP1[1] c28` måste hållas orörd. F2:s index2 c37 som fast i F3. Sista `GRP1 c69`, `WSYNC c72` är tidigare **statiska** envelope, inte ny F4 uppmätt garanti.

**F4:s två konkreta fasidéer är `c18` (en cykel tidigare än bas) och `c21` (två cykler senare än bas)**, inte godtycklig serie. Före kompilering måste ROM DEV visa att timingen kan framställas med 6502/DASM **utan** att index1 c28, index2 c37, övriga tre fasta X, maskbyte, NUSIZ/HMOVE eller PF/P0/M0-skrivningar förändras. **Om fasen inte kan byggas utan olaglig cykel-/registerkostnad: SOURCE_ONLY_INFEASIBLE**, ingen tillåtelse att göra en större unrolled-kernel-refaktorering, använda självmodifierande ROM eller byta till specialmapper.

### 4. G1 – upp till TVÅ små, förkompilerade F6/NTSC geometrier

**Max två nya diagnostiska F6-binärer för hela F4, var och en gäller EN konkret första `RESP1`-fas på exakt nio rader**. Prioriterad ordning:
1. Först `c18` om G0 visar genomförbart; annars explicit `SKIPPED_SOURCE_INFEASIBLE`, gå vidare enbart om `c21` source-styrt är möjligt.
2. En andra prob `c21` är tillåten ENDAST om första c18-varianten har **alla sex oförändrade fulla källmasker, fem andra X exakt oförändrade**, men index0 **står kvar** på x43. Alternativt om c18 inte gick att bygga över huvud taget. Vid **x-förflyttning PASS** i första prob: stoppa efter EN prob och begär ett separat MAIN-beslut för RAM-kombination med index2. Vid mask-ghost, klippt rad, överlapp, fel P0/M0/PF, fel 262 NTSC, ändrade andra fem X eller att cpu/scanline-schemat förlorats: STOPP (FAIL), **inget** försök med `c21` som skyddad extra gren.

För varje körd ROM: oförändrad bas i exakt **en och samma** assemblerkernel på alla nio rader; 16 KiB standard F6 (fyra byteidentiska 4KiB-bankkopior), anteckna hel ROM SHA-256, DASM list/sym, faktisk `RESP1` target/cycle och valt index0 förväntat pixel-X. **Förregistrera det begärda X** före råbildsanalys – härled inte `requested_X` från det i efterhand observerade `rendered_X`. Verklig kopie-fas kan avvika från enkel 6 crop-pixel/cykel-linjär modell; enbart CPU-cykelvariation är inte ett pixel-PASS.

**Evidenskrav för varje faktiskt byggd prob:**
- **16 konsekutiva, oförändrade, verkliga Stella 6.7.1-råbilder** efter stabil init, exakt fil-SHA per bild, hela original-CROP, användbar oklippt debuggerbild med **262 NTSC** och autentiska färger. **Inte** en syntetiskt genererad screenshot.
- **MAIN-kompatibel men oberoende ny pixelunion-checker** av varenda vit P1-pixel på alla nio rasterrader för varje av sex originalmasker. Kontrollera `P0_yellow`, `M0_active`, `PF_brown_left/right`, 0 saknade/extra vita, inga x0 ghostpixlar. Ta med två separata checkerkodvägar, eller återanvänd F3:s två oberoende vägar samt minst en riktad falsifieringsmutant. Särskilj verklig råimage och märkt syntetisk mutation.
- **Faktiskt Stella trap** för första `STA RESP1` (`PC, bank, scanline, CPU cycle, TIA color-clock, A/X/Y`) och dess `STA GRP1`, andra `RESP1` c28, tredje c37 samt `WSYNC` eller omätbarhetsrapport. För instruktioner som endast beräknats ur DASM-listningen, skriv **STATIC_ONLY**, inte mätt.
- Bevara den REDA negativa F3 c20-körningen/commit oförändrad, och F2 enindivid X. En ny CI SUCCESS på F4 **får inte** skriva över F3:s autentiska G0 FAILURE.
- **Pixel-PASS för F4:** index0 byter faktiskt observerat X jämfört med baseline **x43** och den nya faktiska platsen är källkorrekt i alla nio rader och alla 16 frame; **de andra fem förblir X [75,129,183,243,303]**. X-förflyttning behöver inte följa en linjär TIA-modell, men måste mätas och kopplas till förregistrerad korrekt diagnostisk målposition. Ett korrekt men stillastående X är **`F4_NO_SECOND_X_PHASE_RESPONSE`**, inte pass.

### 5. STANNA efter max två prober – ingen RAM runtime och ingen ny arkitekturfamilj

F4 har status `F4_INDEX0_PHASE_GEOMETRY_LOCAL_PASS / FAIL / SOURCE_ONLY_INFEASIBLE / INCONCLUSIVE`. Oberoende två-RAM-X-runtime **`NOT_RUN`** och full R1 **`BLOCKED / NOT ACCEPTED`** även vid F4-partial-PASS. Inga nya 600-frame-, HMOVE-fine-sweeps, index1-varianter, v0.19-rum, nyskriven lookahead-kernel eller PAL. Ett isolerat c18/c21-prob säger inte att sex fria X eller varierande Y är lösta.

Leverera en fryst, reproducerbar `rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F4.md`, exakt F4 branch/commit, registrerad testmatris med källa, begärd X/uppmätt X per figur, DASM + Stella versioner, eventuella nya F6-ROM/sha, 16 autentiska PNG/sha per prob, source- och Stella-traps, tydliga röda/gröna CI-run-id och verklig Google Drive-evidens-ZIP med faktisk SHA256+CRC/filindex. Rapportera en kort teknisk orsaksavgränsning och högst **TVÅ** tänkbara nästa huvudbeslut – utan att själv börja F5, R2/R4, andra TIA-objekt, PAL, produktionskod eller fullspel.

**Main, PR#7, Issue #8, originalmasker, SCORE/HUD, GRAPHICS avslutat, GAME OVER, nyckel och alla tidigare frysta brancher förblir orörda. VERIFICATION inväntar en separat större fryst batch.**

**Påbörja enbart detta enda F4-diagnosuppdrag efter att ha kontrollerat aktuell commit/scope.** Om testerna kräver oväntad designwaiver eller kodfamilj: STOPP och rapportera till MAIN V.
