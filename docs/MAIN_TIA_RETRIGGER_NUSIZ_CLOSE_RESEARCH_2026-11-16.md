# Let Me Out! – MAIN: NUSIZ-close retriggering som NYTT, snävt testbart R1-spår
**Datum:** 2026-11-16. **Status:** källkritisk teknisk forskningsrapport, EJ ny ROM, EJ Stella-körning, EJ implementationstillstånd och EJ oberoende VERIFICATION. *The Cabin*, *I Love a Fish* och Linear lämnas orörda.

## Sammanfattning

**Ny teknisk distinktion:** De tre misslyckade Venetian-kandidaterna sätter `NUSIZ1=0` och gör en enda `STA RESP1` **per rasterrad**, med `STA GRP1` tidigare på samma rad. Därmed finns ingen nära/mellan-kopia som kan starta på *den aktuella* rasterraden. Med huvudkopian räcker inte reseten för att starta ny P1-ritning omedelbart; den kan börja på **nästkommande linje** och återställas innan den hinner starta av nästa tidiga `RESP1`. Detta passar det tidigare visuella FAIL men kräver fortfarande exakt Stella-spår för *den specifika ROM:ens* rotorsak.

**Tidigare oprövad underfamilj inom användarens trick #01/#02/#10/#15 och teknik T03:** ställ `NUSIZ1` till ett läge med extra kopior, t.ex. **`$01`** för en 'close' sekundärkopia, och gör upprepade `RESP1`-strober **på samma rasterrad**. Den hårdvaruutlösta 'close' kopian startar efter cirka **17 TIA-färgklockor efter en reset** (TIA-fas kan påverka exakta pixlar); 'medium' efter cirka 33. Detta är **inte** samma implementation som Venetian 9/18/VDEL. Den dokumenterade mekaniken utnyttjades i Eckhard Stolbergs `grid2`-demo och har analyserats från TIA-gatelevel.

### Oberoende, konkreta källor
1. Andrew Towers, *TIA Hardware Notes*, 6 March 2003: https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php ; "The Re-trigger Trick" och "CPU Clock to Player Pixel Table". Dokumenterar main-copy på följande linje, `close` ~17 CC och `medium` ~33 CC efter reset, flera `RESP`-strober per rad, subtil fasfördröjning vid omkring 18/33 CC. Det är hårdvaru-/demoanalys, INTE ett Let Me Out!-PASS.
2. Stella 6.7-dokumentation (rätt versionsfamilj) https://repo.caluette.com/software/Games/Emulators/Atari/Stella-6.7/docs/debugger.html och officiell debugger https://stella-emu.github.io/docs/debugger.html . Breakpoints ska verkligen nå mål-PC, med `break` + `run`/kontrollerad `runToPc`, inte `break; frame #1; step`; `trapWrite` stannar efter skrivning.
3. [MAIN:s tidigare RESP1-felsökning](MAIN_RESP1_ROOT_CAUSE_ANALYSIS_2026-11-15.md) och [Venetian rapport](https://github.com/Odourman/let-me-out/blob/rom-dev/v018-ntsc-diagnostic/rom/v018/experiments/venetian_blinds/TO_MAIN_VENETIAN_BLINDS_2026-11-15.md).

## Källkodsgranskning – varför det är en separat mekanism

I `rom/v018/experiments/venetian_blinds/vb_9_interleave.asm`, `vb_9_vdel.asm`:

- Init: `LDA #0; STA NUSIZ0; STA NUSIZ1`, alltså **ingen extra P1-kopia**.
- På varje av nio linjer: `STA WSYNC; LDA #mask; STA GRP1; LDX MALE_DELAY eller FEMALE_DELAY; ...; STA RESP1; LDA #player; STA GRP0`.
- En P1-positionsstrobe per scanline, inte två på samma rad. `MALE_REQ_X` och `FEMALE_REQ_X` lagras i RAM men avgör **inte direkt** de synliga `RESP1`-skrivningarna (här väljs fördröjningsbytes).
- STATIC `CYCLE_PLAN.csv`: `RESP1` c30/35 på manliga rader och c50/55 på kvinnliga. Detta är **beräknad CPU-timing**, inte emulatormätt TIA.
- Den lokala 9-line Venetian-modellen delar ut fem respektive fyra av nio rader till två olika NPC. Den är **inte** en fullständig original-8×9-lösning ens om positioneringen rättas.

### Förväntad kopieposition (enbart förenklat räkneexempel, INTE skärmmätning)

Ta 68 färgklockor horisontell blanking, tre färgklockor per CPU-cykel, och `close` cirka +17 färgklockor från `RESP1`.

| Nominell STA RESP1-CPU-cykel | P1 'main' på nästa rad: X≈3c−68+5 | P1 'close' samma rad: X≈3c−68+17 |
|---:|---:|---:|
| 30 | 27 | 39 |
| 35 | 42 | 54 |
| 50 | 87 | 99 |
| 55 | 102 | 114 |

Detta förutsätter referensfas/tid utan extra HMOVE och inga upprepade strober i mittenskiftet. Tabellen **bevisar ingenting om ett faktiskt kört program**, men visar att den nya kopieutlösaren har ett helt annat rasterfönster. Särskilt: två olika `RESP1`-strober på **samma** rad skulle kunna utlösa två nära-kopior, där den gamla en-strobe-per-rad-kerneln aldrig gjorde samma prov.

## Snäv föreslagen forsknings-/diagnosordning (INGEN ny implementeringsauktorisation)

**R0: kalibrera instrumentering först**
- Välj den av ROM DEVELOPMENT levererade oförändrade `vb_9_interleave.F6.bin`; verifiera DASM `.lst`, `.sym`, ROM SHA och vilken bank som exekveras.
- Undvik globalt gammalt `autoexec.script` som annars kan påverka testerna. I Stella 6.7.1 GUI: navigera till testbildruta, sätt breakpoint vid faktisk `STA RESP1` med `break $f0a8` (endast om exakt adress är bekräftad i aktuell listning), verifiera `listBreaks` och tryck GUI **Run** eller kör `run`. Kräv synligt PC `$F0A8`, bank och `_scan/_sCycles`. En `step` därefter ger eftervärdet; alternativ `trapWrite` på `$11` stoppar **efter** skriver. Logga båda. Separat breakpoint för `$F0BD`.
- Vid felaktig PC/bank/spegeladress eller saknat loggspår: **INCONCLUSIVE**. Ingen grafikteori får ersätta själva mätningen.

**R1a: prova utlösaren, enbart en teknisk positioneringskontroll**
- Kontrafaktisk, originalskriven minimal standard-F6/NTSC 6502-prob: P0 är fortfarande gul originalspelare; M0 aktivt skott. Välj **`NUSIZ1=$01`** och skriv `RESP1` **två gånger på en och samma rasterrad** med stor separation (exempelvis nominella CPU-cykel 30 och 50).
- Första kalibreringen kan avsiktligt rita samma enkla P1-bitmönster i de båda P1-kopiorna. Målet här är **enbart att verifiera två oberoende lägen**, INTE original-NPC-PASS.
- Fotografera rå, obeskuren Stella-bild, logga faktiska observerade X för båda kopior, PC/bank/cykel för båda stroberna. Skillnad mellan kopieutlösare och huvudkopia från föregående scanline måste särskiljas.

**R1b: två OLIKA originalmasker, full 8×9-höjd**
- Först om R1a faktiskt visar separata kopior, byt i denna specifika tekniska PROB de enkla bitmapvärdena mot två olika oförändrade original-8×9-masker och skriv vid rätt `GRP1`-deadlines **mellan kopiorna**, så att båda får sin egen form **på alla nio ursprungliga rasterlinjer**.
- Prova både bredare och smalare X-avstånd, förändra dem oberoende mellan bildrutor. Utför pixelmatch i Stella på varje maskrad, bedöm om kopior klipps av / blandas av registerbyte; håll P0/M0 synliga.
- **Viktig begränsning:** NUSIZ ger en kopieutlösare men inte mer GRP1-bandbredd. Sex distinkta figurer över 160 färgklockor plus sex PF-skrivningar, P0/M0 och deras deadlines är mycket hårt. Även R1b på två NPC är **ett delbevis**, inte R1 full PASS.

**R1c: hållbarhets- och fullscen-grind endast efter delbevis och med täckande explicit mandat**
- Pröva successivt 3→6 NPC, dynamiska sex-X, kollision/nära och same-Y, samtidigt med P0/M0 och vägg-/dörrbudgeten. Planera R2 med fem + guldnyckel/O1.
- Ett läge med sex fasta kopior eller sex identiska GRP1-bitmappar är **inte** sex fritt placerade originalmasker.
- Vid missade originalrader, positionskoppling eller obrukbar P0/M0: tydligt **FAIL**, ingen tyst waiver.
- Separat VERIFICATION kopplad till exakt ny ROM/commit och SHA, **inte** äldre Issue #8-baslinje.

## Ytterligare avgörande risk: kopiorna är inte samma som fria sprites

`NUSIZ1=$01` ger extra utlösning efter RESP-tidpunkt, men antal/avstånd är kopplade till *när* varje reset sker. För godtyckliga sex X kan reset-/GRP-skrivningar hamna för tätt för att passa 76-cykel- och pixeldeadlines. Dessutom kan en senare `GRP1`-skrivning påverka tidigare kopia om den ligger mitt i dess 8-pixelklocksekvens. Denna teknik kan alltså vara reproducerbar för en statisk formation men misslyckas helt för fritt rörliga androidsilhuetter. **Det måste avgöras i Stella, inte antas från grid2-demot.** Låt även oberoende verifierare jämföra ren P1 nära-kopia mot P1-huvudkopia på följande rad.

## Status och auktorisationsgrind

- [PR #7](https://github.com/Odourman/let-me-out/pull/7) var **DRAFT**, ej merge, HEAD vid forskningskontroll `82667dae033f70570dce903f8e1d4866528be02a`.
- Tidigare tre Venetian ROM:er R1 **FAIL/BLOCKED**, T07 **INCONCLUSIVE**, R2–R4 ej retestade. Den här rapporten innehåller **ingen ny Stella-körning och ingen ny binär**. Inget nytt PASS.
- [Kodauktorisation](ROM_GATE_V018_AUTHORIZATION_2026-11-15.md) gäller endast NTSC v0.18 R1–R4. ROM DEVELOPMENT rapporterade STOPP för tidigare techfamiljer; MAIN:s forskningsrapport är **inte** en ny separat, uttrycklig ROM-kodorder. Begär sådan om nytt test går utöver aktuell konkret kodauktorisation.
- Inget fullspel, PAL, ny kartcutover, F6SC/DPC+/ARM, designwaiver eller PR-merge. *The Cabin*, *I Love a Fish* och Linear orörda.

**MAIN-bedömning:** Detta är det skarpaste nya, historiskt dokumenterade teknikdeltat att värdera efter de negativa Venetian-försöken: *same-line `NUSIZ1 close` retriggering*, inte ännu mer vanlig RESP utan kopieläge. Samma-Y-fri-X-maskbevis saknas fortfarande.
