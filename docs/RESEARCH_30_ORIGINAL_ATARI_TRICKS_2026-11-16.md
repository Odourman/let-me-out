# Bilaga – samtliga 30 ursprungliga programmeringstrick, genomgång för MAIN

**Syfte och avgränsning.** Denna bilaga reproducerar **exakt de 30 trick som tidigare listades i chatten**, i samma ordningsföljd, med en egen teknisk bedömning för *Let Me Out!*. De **52 teknikmönstren i föregående atlas är inte 52 andra trick**: samtliga 30 motsvarar en eller flera befintliga T-poster. Bilagan är ett navigerbart korsindex och en fördjupad prövningsplan, inte 82 unika tekniker eller nytt implementationsmandat.

**Källbedömning.** TIA-/6507-mekanik stöds av [E01]. Historiska spelattributioner (Video Chess, Boxing, Chopper Command, Dragster, flicker) stöds av [E03–E05]. SCABS stöds av [E15]. *Combat* och *Pole Position* stöds av [E18] och ytterligare källor längst ner. En teknik som fungerar historiskt har **inte** därmed visats fungera i vår NTSC-v0.18-ROM. Alla testförslag är uttryckligen rådgivande.

## Snabbindex: alla 30 med korsreferenser till teknikatlasen

| Nr | Ursprungligt trick | Matchning i teknikatlasen | Standard-F6 | Bedömning |
|---:|---|---|---|---|
| 01 | Sprite Multiplexing | `T03/T04/T32` | Ja | Hög – villkorat |
| 02 | Mid-scanline GRP Rewriting | `T02/T01` | Ja | Hög – kritisk kärnteknik |
| 03 | Venetian Blinds | `T06/T07` | Ja | Redan negativt provad |
| 04 | Sprite Flickering | `T05` | Ja | Redan negativt provad |
| 05 | Dynamic Playfield Sprites | `T10/T09` | Ja | Medel – begränsad upplösning |
| 06 | Mid-frame Sprite Resizing | `T15/T01` | Ja | Låg – framtida grafik |
| 07 | Asymmetric Playfield | `T09/T13` | Ja | Hög – R3 |
| 08 | Two-Line Kernel | `T22/T07` | Ja | Medel – rasterutrymme |
| 09 | VDEL / Delayed Graphics | `T07/T08` | Ja | Hög – timingstöd |
| 10 | HMOVE Fine Positioning | `T17` | Ja | Hög – nödvändig byggsten |
| 11 | Late HMOVE Trick | `T18` | Ja | Låg – efter fungerande raster |
| 12 | Raster Color Changes | `T14` | Ja | Medel – kontrast |
| 13 | 48-Pixel / Six-Digit Score Kernel | `T08/T50` | Ja | Medel – användbar princip |
| 14 | Multiple Display Kernels | `T23/T42` | Ja | Hög – arkitektur |
| 15 | NUSIZ Sprite Duplication | `T01` | Ja | Hög – känd gräns |
| 16 | Sprite Reflection (REFP0/REFP1) | `T16` | Ja | Låg – ROM-sparande |
| 17 | Missile and Ball Reuse | `T19/T20` | Ja | Medel – begränsade objekt |
| 18 | Playfield Score Mode | `T11` | Ja | Låg – två PF-färger |
| 19 | Playfield Priority Switching | `T12` | Ja | Medel – occlusion |
| 20 | Hardware Collision Latches | `T21` | Ja | Medel – framtida gameplay |
| 21 | RIOT Timer Scheduling | `T29` | Ja | Medel – stabil bild |
| 22 | Stack/RAM Mirroring | `T36/T34` | Ja | Låg – avancerad minnesdisciplin |
| 23 | Undocumented 6502 Opcodes | `T49` | Tekniskt möjligt | Låg – hög kompatibilitetsrisk |
| 24 | Precomputed Tables and Cycle-Exact Kernels | `T26/T30/T39/T40` | Ja | Hög – bästa arkitekturforskning |
| 25 | Stack-Based TIA Register Tricks | `T35` | Ja | Låg – historiskt specialistknep |
| 26 | Timing-Based Horizontal Scrolling | `T27/T08` | Ja | Låg – ej aktuellt rumsbehov |
| 27 | SCABS – Automatic Bank Switching | `T44/T43` | Nej – specialkassett | Referens, ej v0.18 |
| 28 | Extra Cartridge RAM / Superchip / Supercharger | `T45/T46` | Nej – specialkassett | Referens, ej v0.18 |
| 29 | DPC – Display Processor Chip | `T47` | Nej – specialkassett | Referens, ej v0.18 |
| 30 | DPC+, CDF och ARM-coprocessorer | `T48` | Nej – specialkassett | Referens, ej v0.18 |

## Fullständiga teknikposter 01–30

### Ursprungligt trick 01 – Sprite Multiplexing

**Princip.** Återanvänd en och samma P0/P1-generator för flera figurer på olika rasterhöjder eller genom ny positionering.

**Möjlig nytta för *Let Me Out!*.** Samma P1 kan användas för NPC på åtskilda Y-band; sorterade renderingslistor kan spara objektresurser.

**Begränsning / risk.** Hjälper normalt när Y skiljer sig. Sex självständiga NPC på samma Y kräver en annan, bevisad metod och P0 är upptagen av spelaren.

**F6-status:** Ja. **Forskningsprioritet:** Hög – villkorat. **Teknikatlas:** `T03/T04/T32`. **Relaterade punkter i 67-riskregistret:** 1, 11–13.

**Vad MAIN bör undersöka:** Inventera om R4 har realistisk Y-återanvändning. Testa inte detta som R1-PASS när figurerna ligger på samma rasterband.

**Källstöd:** [E01, E03, E04, P05].

### Ursprungligt trick 02 – Mid-scanline GRP Rewriting

**Princip.** Skriv nya GRP0/GRP1-bitmaps mellan NUSIZ-kopior inom en skärmrad; ett hårdvaruobjekt kan då rita flera OLIKA bitmapmönster.

**Möjlig nytta för *Let Me Out!*.** Space Invaders visar en historiskt fungerande mekanism för en horisontell fienderad med få hårdvarugeneratorer.

**Begränsning / risk.** Kopiorna följer bestämda X-separationer, inte sex godtyckliga koordinater. GRP-deadlines och P0/P1-konflikten är kritiska.

**F6-status:** Ja. **Forskningsprioritet:** Hög – kritisk kärnteknik. **Teknikatlas:** `T02/T01`. **Relaterade punkter i 67-riskregistret:** 1–3, 5, 11–13.

**Vad MAIN bör undersöka:** Mät först en befintlig tvåmaskskernel med verkliga registercykler; pröva därefter varierande X-avstånd utan att byta originalmask.

**Källstöd:** [E01, E06, P03, P11].

### Ursprungligt trick 03 – Venetian Blinds

**Princip.** Fördela flera objekt på olika scanlines i samma visuella höjdband, som i Video Chess.

**Möjlig nytta för *Let Me Out!*.** Historiskt kunde fler skilda objekt urskiljas på samma schackrad än med bara samtidiga spritekopior.

**Begränsning / risk.** Våra 9-, 18- och VDEL-varianter underkändes. Varannan rad i en 9-radersmask lämnar bara 5 respektive 4 originalrader för två figurer.

**F6-status:** Ja. **Forskningsprioritet:** Redan negativt provad. **Teknikatlas:** `T06/T07`. **Relaterade punkter i 67-riskregistret:** 1, 3, 5, 66.

**Vad MAIN bör undersöka:** MAIN bör granska den faktiska radbudgetens konsekvenser; upprepa inte exakt samma ROM-varianter utan en ny, mätbar mekanism.

**Källstöd:** [E03, E05, E21, P03, P07, P12].

### Ursprungligt trick 04 – Sprite Flickering

**Princip.** Visa ett urval av sprites varannan, var tredje eller var sjätte bildruta.

**Möjlig nytta för *Let Me Out!*.** Skapar illusion av fler oberoende objekt i vissa historiska spel.

**Begränsning / risk.** Vår SEX_X_FREE-A visade varje NPC 100/600 frames, fem osynliga i följd (omkring 10 Hz), och blev FAIL.

**F6-status:** Ja. **Forskningsprioritet:** Redan negativt provad. **Teknikatlas:** `T05`. **Relaterade punkter i 67-riskregistret:** 1–2, 13, 66.

**Vad MAIN bör undersöka:** Dokumentera flimmertröskel med video; ingen ny sexfascykel utan annat explicit granskat bildsynlighetsupplägg.

**Källstöd:** [E04, P08, P05].

### Ursprungligt trick 05 – Dynamic Playfield Sprites

**Princip.** Skriv om PF0/PF1/PF2 medan bilden ritas så att playfield fungerar som ytterligare rörligt objekt.

**Möjlig nytta för *Let Me Out!*.** Använt bland annat i Chopper Command för helikopter/laser; kan frigöra playerresurs för andra objekt.

**Begränsning / risk.** Fyra färgklockor per PF-pixel gör ansikten/ben och små detaljer grova; PF används samtidigt till bruna väggar och dörr.

**F6-status:** Ja. **Forskningsprioritet:** Medel – begränsad upplösning. **Teknikatlas:** `T10/T09`. **Relaterade punkter i 67-riskregistret:** 1, 3, 16–19.

**Vad MAIN bör undersöka:** Rita en begränsad rörlig hjälpsymbol och väggen i samma rad, mät alla sex PF-skrivningars deadlines. Behåll godkända NPC-masker som krav.

**Källstöd:** [E04, E01, E07, P08].

### Ursprungligt trick 06 – Mid-frame Sprite Resizing

**Princip.** Ändra NUSIZ medan figuren eller rasterbandet ritas; i Boxing används varierande bredd för att gestalta ett slag.

**Möjlig nytta för *Let Me Out!*.** Kan ge billiga animationseffekter eller olika visuella tillstånd utan full maskomskrivning.

**Begränsning / risk.** Ingen extra självständig 8-bitarsfigur skapas; förvrängd godkänd 8×9-mask är inte automatiskt acceptabel.

**F6-status:** Ja. **Forskningsprioritet:** Låg – framtida grafik. **Teknikatlas:** `T15/T01`. **Relaterade punkter i 67-riskregistret:** 21, 23.

**Vad MAIN bör undersöka:** Jämför visuellt mål och faktisk skala innan övervägande; prioritera inte före fungerande tvåmaskrendering.

**Källstöd:** [E03, E05, E01].

### Ursprungligt trick 07 – Asymmetric Playfield

**Princip.** Skriv vänster och höger PF-halvas registervärden vid olika tidpunkter på samma skärmrad.

**Möjlig nytta för *Let Me Out!*.** Behövs för en öppning enbart på högerkanten, med fortsatt stängd vänster yttervägg.

**Begränsning / risk.** Vänster-/högerbytet har exakta pixeldeadlines och konkurrerar med andra registerskrivningar; svart nyckelhål kräver ytterligare detalj.

**F6-status:** Ja. **Forskningsprioritet:** Hög – R3. **Teknikatlas:** `T09/T13`. **Relaterade punkter i 67-riskregistret:** 7–8, 16–18.

**Vad MAIN bör undersöka:** Kör ett R3-stressfall med låst/öppet x39, full vänsterkant och orange/svart mål; registrera PF0/1/2 per sida i Stella.

**Källstöd:** [E01, E07, E08, P04, P05].

### Ursprungligt trick 08 – Two-Line Kernel

**Princip.** Fördela ett renderingsvarv och dess datauppdateringar över två rasterrader.

**Möjlig nytta för *Let Me Out!*.** Ger mer CPU-tid mellan registeromskrivningar och kan fungera med VDEL.

**Begränsning / risk.** Ändrar normalt vertikalupplösning eller kräver noggrant växelvis förberedda bitmaps; 9-raders originalmasker får inte tyst förändras.

**F6-status:** Ja. **Forskningsprioritet:** Medel – rasterutrymme. **Teknikatlas:** `T22/T07`. **Relaterade punkter i 67-riskregistret:** 1, 5, 11, 21.

**Vad MAIN bör undersöka:** Beräkna cykelplanen för R1/R2 och explicit maskbevarande; testa bara om var och en av nio ursprungsrader syns rätt.

**Källstöd:** [E01, E08, P05].

### Ursprungligt trick 09 – VDEL / Delayed Graphics

**Princip.** Utnyttja TIA:s skugg-/fördröjningsregister VDELP0/VDELP1/VDELBL för att visa förberett innehåll senare.

**Möjlig nytta för *Let Me Out!*.** Kan minska tidspress i 48-pixelkernlar och andra multiplexande rutiner.

**Begränsning / risk.** VDEL är en latch, inte en tredje player. Vårt senaste 9-line VDEL-försök gav bara fragment.

**F6-status:** Ja. **Forskningsprioritet:** Hög – timingstöd. **Teknikatlas:** `T07/T08`. **Relaterade punkter i 67-riskregistret:** 1, 5, 11–13.

**Vad MAIN bör undersöka:** Kartlägg GRP-latcharnas faktiska writes och efterföljande scanlineeffekter i Stella innan ny arkitektur skissas.

**Källstöd:** [E01, E02, E18, P07, P03].

### Ursprungligt trick 10 – HMOVE Fine Positioning

**Princip.** Förbered HMP0/1/HMM0/1/HMBL och stroba HMOVE för finare X-förskjutning än RESP grovposition.

**Möjlig nytta för *Let Me Out!*.** Gör valda positioner mer exakta, bland annat de sex individuella logiska X-värdena.

**Begränsning / risk.** Ger inte fler sprites eller gratis RESP-omstarter. HMOVE påverkar alla fem objekt och är timingkänsligt.

**F6-status:** Ja. **Forskningsprioritet:** Hög – nödvändig byggsten. **Teknikatlas:** `T17`. **Relaterade punkter i 67-riskregistret:** 1, 5, 11–13.

**Vad MAIN bör undersöka:** Knyt begärd X till faktiskt observerad X per objekt; prova kantpositioner, page crossings och skott samtidigt.

**Källstöd:** [E01, E24, P03, P11].

### Ursprungligt trick 11 – Late HMOVE Trick

**Princip.** Lägg HMOVE-strobe vid särskilt vald sen cykel för att i vissa lägen slippa typiska HMOVE-bars.

**Möjlig nytta för *Let Me Out!*.** Kan minska mörka vänsterkantartefakter och förbättra slutlig bildrenhet.

**Begränsning / risk.** Sen HMOVE och RESP-kombinationer har kända race conditions och kan skilja mellan TIA-varianter.

**F6-status:** Ja. **Forskningsprioritet:** Låg – efter fungerande raster. **Teknikatlas:** `T18`. **Relaterade punkter i 67-riskregistret:** 5, 20, 25.

**Vad MAIN bör undersöka:** Använd aldrig som genväg för misslyckad huvudpositionering; kontrollera flera TIA-varianter i Stella och riktig konsol.

**Källstöd:** [E19, E02, E24].

### Ursprungligt trick 12 – Raster Color Changes

**Princip.** Byt COLUP0/COLUP1/COLUPF/COLUBK per rasterrad för fler färgband än en enda stillastående objektfärg.

**Möjlig nytta för *Let Me Out!*.** Historiskt användbart för flerfärgade figurer och bakgrundseffekter; kan hjälpa gul spelare, bruna väggar och orange dörr.

**Begränsning / risk.** Ingen ny objektkanal tillkommer; färgskrivningar förbrukar rastercykler och kan konkurrera med GRP/PF.

**F6-status:** Ja. **Forskningsprioritet:** Medel – kontrast. **Teknikatlas:** `T14`. **Relaterade punkter i 67-riskregistret:** 8, 20, 24.

**Vad MAIN bör undersöka:** Ta fram regionkorrekta färgprov och mät om färgskrivningarna ryms i R3-kerneln utan pixelglapp.

**Källstöd:** [E01, E03, E04, P05].

### Ursprungligt trick 13 – 48-Pixel / Six-Digit Score Kernel

**Princip.** Kombinera P0/P1, kopior, GRP-buffertar och cykelprecisa byten till en bred sammanhängande bitmaprad.

**Möjlig nytta för *Let Me Out!*.** Bevisar hur mycket grafisk detalj som kan matas ut på en rad och ger senare kompakt poäng-HUD.

**Begränsning / risk.** Historiska 48-pixel-kernlar har normalt fast geometri och prioriterar en sammanhängande bitmap, inte sex fria android-X.

**F6-status:** Ja. **Forskningsprioritet:** Medel – användbar princip. **Teknikatlas:** `T08/T50`. **Relaterade punkter i 67-riskregistret:** 1, 5, 53.

**Vad MAIN bör undersöka:** Studera exakt assembler-tid och registerplan för 48px; tillämpa först på lågrisk HUD eller diagnostisk bitmap, inte full R1 som om den vore löst.

**Källstöd:** [E01, E17, E18].

### Ursprungligt trick 14 – Multiple Display Kernels

**Princip.** Rita olika skärmzoner med olika rutiner; välj eventuellt olika bankvisa kernels före aktiv bild.

**Möjlig nytta för *Let Me Out!*.** Kan ge skilda optimala rutiner för spelplan, HUD och specialscener R1/R2/R3.

**Begränsning / risk.** En separat R3-diagnosbank bevisar inte att dörr och androids ritas ihop i verkliga spelet. Samma-Y i en zon kvarstår.

**F6-status:** Ja. **Forskningsprioritet:** Hög – arkitektur. **Teknikatlas:** `T23/T42`. **Relaterade punkter i 67-riskregistret:** 1, 4, 15–19, 53.

**Vad MAIN bör undersöka:** Rita ett adress- och resurskontrakt med rätt fortsättningskod efter F6-hotspots, samt hela spelplanens R1/R2-vägg-/dörrkrav.

**Källstöd:** [E01, E08, E09, P02, P05].

### Ursprungligt trick 15 – NUSIZ Sprite Duplication

**Princip.** Duplicera player-objekt två eller tre gånger och välj olika fasta separationer med NUSIZ0/NUSIZ1.

**Möjlig nytta för *Let Me Out!*.** Två originalsilhuetter med olika bitmapdata och 32/64 färgklockors separation har visats i ett av våra smala delprov.

**Begränsning / risk.** NUSIZ låser kopiepositionernas relationer; 44 191 av 64 045 historiska spawnkombinationer saknar par på just de provade separationerna.

**F6-status:** Ja. **Forskningsprioritet:** Hög – känd gräns. **Teknikatlas:** `T01`. **Relaterade punkter i 67-riskregistret:** 1–3, 12–13.

**Vad MAIN bör undersöka:** Behåll X-frihet som hårt krav. Lista exakt vilka X-arrangemang NUSIZ kan stödja och vilka den omöjligen kan stödja ensam.

**Källstöd:** [E01, E06, P11].

### Ursprungligt trick 16 – Sprite Reflection (REFP0/REFP1)

**Princip.** Spegelvänd åttabitars player-uppsättning i hårdvara utan att lagra ett andra bitmapmönster.

**Möjlig nytta för *Let Me Out!*.** Sparar ROM för riktning/animation där en spegelvänd mask är visuellt godtagbar.

**Begränsning / risk.** Godkända olika människoformer och figurer ska inte ändras tyst, och spegling löser inte objektantal eller X.

**F6-status:** Ja. **Forskningsprioritet:** Låg – ROM-sparande. **Teknikatlas:** `T16`. **Relaterade punkter i 67-riskregistret:** 14, 21.

**Vad MAIN bör undersöka:** Jämför original- och spegelvänd mask pixelför-pixel i ett rådgivande offline-prov innan integration.

**Källstöd:** [E01].

### Ursprungligt trick 17 – Missile and Ball Reuse

**Princip.** Låt M0/M1 eller BL rita ett annat objekt än en projektil; Adventure använder BL som spelarfigur och andra sprites för föremål.

**Möjlig nytta för *Let Me Out!*.** Kan potentiellt frigöra P1 eller avlasta skott/markörer med smala objekt.

**Begränsning / risk.** M0/M1/BL är inte 8-bitars människosprites; vår spelare ska fortfarande vara gul och fullstor i v0.18-diagnosen.

**F6-status:** Ja. **Forskningsprioritet:** Medel – begränsade objekt. **Teknikatlas:** `T19/T20`. **Relaterade punkter i 67-riskregistret:** 1, 4, 12, 18–19.

**Vad MAIN bör undersöka:** Inventera resurser per R1/R2 inklusive skott, nyckel, dörr och dess svart hål; mät konflikt innan resursomfördelning.

**Källstöd:** [E01, E03, P13].

### Ursprungligt trick 18 – Playfield Score Mode

**Princip.** Sätt CTRLPF SCORE för att färgsätta vänster respektive höger playfieldhalva via COLUP0/COLUP1.

**Möjlig nytta för *Let Me Out!*.** Kan ge skilda halffärger eller enkla HUD-effekter utan extra PF-färgregister.

**Begränsning / risk.** Delar färg med players, vilket kan krocka med vita androiders/bruna väggars/gul spelares färgkrav.

**F6-status:** Ja. **Forskningsprioritet:** Låg – två PF-färger. **Teknikatlas:** `T11`. **Relaterade punkter i 67-riskregistret:** 16, 20, 53.

**Vad MAIN bör undersöka:** Kontrollera explicit om andra färgkällor eller objektprioriteter redan använder dessa register; lämna R1/R2 utanför tills konfliktfri färgplan finns.

**Källstöd:** [E01].

### Ursprungligt trick 19 – Playfield Priority Switching

**Princip.** Sätt CTRLPF PFP för att låta playfield få prioritet framför playerbilder (eller tvärtom).

**Möjlig nytta för *Let Me Out!*.** Kan stödja väggskymning och visuellt lagerbeteende kring rummet.

**Begränsning / risk.** Det avgör inte logisk nyckelposition och bör inte automatiskt ersätta O1; PF-androider och PF-väggar delar kanal.

**F6-status:** Ja. **Forskningsprioritet:** Medel – occlusion. **Teknikatlas:** `T12`. **Relaterade punkter i 67-riskregistret:** 4, 16, 37.

**Vad MAIN bör undersöka:** Prova O1 med stillastående nyckel på exakt samma X/Y under överlappning; kontrollera att prioriteten inte gömmer spelare/skott.

**Källstöd:** [E01, P05].

### Ursprungligt trick 20 – Hardware Collision Latches

**Princip.** Läs TIA:s kollisionsflaggor som samlar pixelöverlappningar och nollställ med CXCLR.

**Möjlig nytta för *Let Me Out!*.** Sparar vissa enkla överlappningstester och är relevant för skott/spelare/vägg.

**Begränsning / risk.** Latchen svarar inte på vilken av flera återanvända NPC som träffades; logiska K1/E1-regler behöver fortfarande objekt-ID och händelseordning.

**F6-status:** Ja. **Forskningsprioritet:** Medel – framtida gameplay. **Teknikatlas:** `T21`. **Relaterade punkter i 67-riskregistret:** 26–39.

**Vad MAIN bör undersöka:** Planera separat kombination av hårdvarulatchar och mjukvaruhitboxar, utan att implementera gameplay före auktorisation.

**Källstöd:** [E01, P17].

### Ursprungligt trick 21 – RIOT Timer Scheduling

**Princip.** Använd TIM64T eller annan 6532-timer för att styra arbetspass och synkning i VBLANK/overscan.

**Möjlig nytta för *Let Me Out!*.** Kan ge reproducerbar frame-timing för förberedda grafiktabeller och senare AI.

**Begränsning / risk.** Ger inte fler än 76 cykler på en synlig scanline; timerövervakning kostar själv CPU-cykler.

**F6-status:** Ja. **Forskningsprioritet:** Medel – stabil bild. **Teknikatlas:** `T29`. **Relaterade punkter i 67-riskregistret:** 5, 11, 25, 64.

**Vad MAIN bör undersöka:** Kartlägg var vår kod väntar på WSYNC eller timer; verifiera faktisk 262-scanline-stabilitet i Stella.

**Källstöd:** [E01, E02].

### Ursprungligt trick 22 – Stack/RAM Mirroring

**Princip.** Utnyttja att 6507:s/RIOT:s adresspegling låter stack- och zero-page-adresser nå samma interna RAM eller vissa register.

**Möjlig nytta för *Let Me Out!*.** Kan spara adresseringsbyte och ge kompakta specialrutiner.

**Begränsning / risk.** Skapar inte mer än 128 byte RIOT-RAM och kan orsaka stackkorruption/skrivning till TIA vid fel stackpekare.

**F6-status:** Ja. **Forskningsprioritet:** Låg – avancerad minnesdisciplin. **Teknikatlas:** `T36/T34`. **Relaterade punkter i 67-riskregistret:** 14, 64.

**Vad MAIN bör undersöka:** Dokumentera exakt minneskarta och livstider i statisk revision; använd inte innan vanliga RAM-overlayalternativ är prövade.

**Källstöd:** [E01, E18, P02].

### Ursprungligt trick 23 – Undocumented 6502 Opcodes

**Princip.** Utnyttja odokumenterade instruktioner på NMOS-6502/6507, exempelvis LAX för att kombinera vissa operationer.

**Möjlig nytta för *Let Me Out!*.** Kan i vissa fall spara kod eller cykler.

**Begränsning / risk.** Alla odokumenterade varianter är inte stabila över chip/revisioner eller emulatorinställningar; källkodsportabiliteten minskar.

**F6-status:** Tekniskt möjligt. **Forskningsprioritet:** Låg – hög kompatibilitetsrisk. **Teknikatlas:** `T49`. **Relaterade punkter i 67-riskregistret:** 5, 11, 25.

**Vad MAIN bör undersöka:** Beakta bara vid uppmätt, kritiskt kodbehov och verifiera på riktig 6507; kan inte rädda strukturell brist på sprites.

**Källstöd:** [E18, E01].

### Ursprungligt trick 24 – Precomputed Tables and Cycle-Exact Kernels

**Princip.** Förbered bitmapvärden, registersekvenser och adressindex i ROM eller under VBLANK för extremt kort synlig rendering.

**Möjlig nytta för *Let Me Out!*.** Kan utnyttja de 1 557 oallokerade ROM-bytena per bank och låta den kritiska kerneln bara hämta redan klara värden.

**Begränsning / risk.** Dynamiska sex-X-kombinationer får inte antas kunna täckas av en liten förberäknad tabell; de 128 RAM-bytena är en separat flaskhals.

**F6-status:** Ja. **Forskningsprioritet:** Hög – bästa arkitekturforskning. **Teknikatlas:** `T26/T30/T39/T40`. **Relaterade punkter i 67-riskregistret:** 1, 5, 11, 14–16.

**Vad MAIN bör undersöka:** Utforma två cykelplaner: befintlig fast tabell och föreslagen förberäknad plan; mät TIA-deadlines och VBLANK-arbetskostnad.

**Källstöd:** [E07, E08, E09, P02, P05].

### Ursprungligt trick 25 – Stack-Based TIA Register Tricks

**Princip.** Ändra stackpekaren så att PHA/BRK:s stackskrivningar träffar speglade TIA-register med särskild timing.

**Möjlig nytta för *Let Me Out!*.** Combat använder PHA för missile-enable; Pole Position ett BRK-relaterat reset-trick enligt kommenterad teknikstudie.

**Begränsning / risk.** Extremt cykel- och stackkänsligt: BRK skriver flera stackbyte och påverkar exekveringsflöde; inga fria sprites skapas.

**F6-status:** Ja. **Forskningsprioritet:** Låg – historiskt specialistknep. **Teknikatlas:** `T35`. **Relaterade punkter i 67-riskregistret:** 5, 11, 14, 25.

**Vad MAIN bör undersöka:** Dokumentera exakt busstransaktioner och minnesadresser som ett teoretiskt registertrick; prioritera endast vid bevisad cykelvinst.

**Källstöd:** [E18, E01].

### Ursprungligt trick 26 – Timing-Based Horizontal Scrolling

**Princip.** Skjut en omfattande grafiksekvens horisontellt genom mycket precisa rastertider, känt från David Cranes Dragster.

**Möjlig nytta för *Let Me Out!*.** Kan skapa breda högupplösta föremål och scrollning utan en vanlig framebuffer.

**Begränsning / risk.** Skapar inte självständiga extra humanoidkanaler. Spelets aktuella öppna statiska rum kräver inte sådan scrollning.

**F6-status:** Ja. **Forskningsprioritet:** Låg – ej aktuellt rumsbehov. **Teknikatlas:** `T27/T08`. **Relaterade punkter i 67-riskregistret:** 1, 11, 45.

**Vad MAIN bör undersöka:** Bevara som historisk metod; värdera bara mot framtida bildpresentation, inte som ny R1-lösning.

**Källstöd:** [E03, E05, E18].

### Ursprungligt trick 27 – SCABS – Automatic Bank Switching

**Princip.** Activisions Subroutine Controlled Automatic Bank Switching använde kassetthårdvara för att byta bank i samband med subrutinanrop.

**Möjlig nytta för *Let Me Out!*.** Illustrerar hur hårdvara kan göra bankanrop enklare och mindre kostsamma.

**Begränsning / risk.** Finns inte i vanlig F6; en sådan teknik vore nytt kassettformat, och fler banker skulle fortfarande inte ge fler TIA-sprites.

**F6-status:** Nej – specialkassett. **Forskningsprioritet:** Referens, ej v0.18. **Teknikatlas:** `T44/T43`. **Relaterade punkter i 67-riskregistret:** 15, 67.

**Vad MAIN bör undersöka:** Notera konceptet för framtida långtidsstudie; ingen migration utan uttryckligt formatbeslut.

**Källstöd:** [E15, E10].

### Ursprungligt trick 28 – Extra Cartridge RAM / Superchip / Supercharger

**Princip.** F6SC/SARA ger 128 byte extra kassett-RAM; Starpath Supercharger erbjuder omkring 6 KB RAM via helt annan hårdvara.

**Möjlig nytta för *Let Me Out!*.** Kan möjliggöra mer staging av registerhändelser, komprimerade sprites och speldata.

**Begränsning / risk.** Inte kompatibelt med vanlig F6, inte en lösning på 76 cykler eller TIA:s antal playergeneratorer.

**F6-status:** Nej – specialkassett. **Forskningsprioritet:** Referens, ej v0.18. **Teknikatlas:** `T45/T46`. **Relaterade punkter i 67-riskregistret:** 14–15, 67.

**Vad MAIN bör undersöka:** Kvantifiera exakt vilket RAM-problem som finns innan MAIN ens tar upp ett nytt mapperformat.

**Källstöd:** [E15, E10, E03].

### Ursprungligt trick 29 – DPC – Display Processor Chip

**Princip.** Extra specialchip i Pitfall II som stödjer datamatning, musik/ljud och andra hårdvarufunktioner.

**Möjlig nytta för *Let Me Out!*.** Kan underlätta repetitiva tabellhämtningar och vissa uppgifter utan lika mycket 6507-kod.

**Begränsning / risk.** Kräver DPC-kompatibel cartridge och utvecklingsmiljö; det skapar inte fyra nya åttabitars-TIA-sprites.

**F6-status:** Nej – specialkassett. **Forskningsprioritet:** Referens, ej v0.18. **Teknikatlas:** `T47`. **Relaterade punkter i 67-riskregistret:** 5, 14–15, 67.

**Vad MAIN bör undersöka:** Studera för framtida jämförelse av dataflöden, inte som tillåten ändring av nuvarande F6-ROM.

**Källstöd:** [E15, E10].

### Ursprungligt trick 30 – DPC+, CDF och ARM-coprocessorer

**Princip.** Modern homebrew med extra processor, mer RAM och skräddarsydd datamatning till en vanlig Atari 2600.

**Möjlig nytta för *Let Me Out!*.** Kan flytta omfattande spel- och databearbetning från 6507 till cartridge-processor.

**Begränsning / risk.** Kräver särskilt cartridgeformat och support på faktisk hårdvara/emulator; även ARM skapar inte fler inbyggda TIA-objekt.

**F6-status:** Nej – specialkassett. **Forskningsprioritet:** Referens, ej v0.18. **Teknikatlas:** `T48`. **Relaterade punkter i 67-riskregistret:** 1, 11, 14–15, 67.

**Vad MAIN bör undersöka:** Skissa först en kontrafaktisk kapacitetsjämförelse och ge MAIN beslutsunderlag; kod inte i annat format utan tillstånd.

**Källstöd:** [E10, E15].

## Källor som kompletterar rapportens ordinarie källregister

- **N01 – IEEE Spectrum (1983):** samtidshistorisk dokumentation av Venetian Blinds, Chopper Command, Boxing, flicker, färgbyten och Dragster. [Originalartikel](https://spectrum.ieee.org/atari-2600/atari-s-competition).
- **N02 – Atari Compendium, Subroutine Controlled Automatic Bank Switching:** historisk SCABS-förklaring och intervju med David Crane. [Teknisk artikel](https://www.ataricompendium.com/archives/articles/longevity/longevity.html).
- **N03 – Combat originalkod och stacktricket:** register- och instruktionsexempel. [AtariAge arkiv](https://www.atariage.com/2600/archives/combat_asm/index.html).
- **N04 – Pole Position BRK-tricket:** kommenterad 6502-teknikförklaring. [6502 Ponderables](https://gist.github.com/qalle2/27465ba4d3e11c724ca5839f4e924d05).
- **N05 – 48px scorekernel:** praktiskt exempel och diskussion av VDEL och GRP-kopior. [Bumbershoot Software](https://bumbershootsoft.wordpress.com/2018/09/24/atari-2600-a-48px-kernel/).
- **N06 – Adventure med BL-objektet:** källkritisk historisk beskrivning. [Atari Archive](https://www.atariarchive.org/blog/adventure-march-1980/).
- **N07 – Late HMOVE:s timingrisker:** AtariAge-community och tester. [Diskussion](https://forums.atariage.com/topic/336441-boom-atari-2600/).
- **N08 – Stella Debugger:** verktygsreferens för verkliga TIA-skrivningar och breakpoints. [Officiell dokumentation](https://stella-emu.github.io/docs/debugger.html).

## MAIN:s granskning av samtliga 30 – föreslagen arbetsordning

1. **Enbart forsknings- och källrevision:** använd detta 30-index för att bekräfta historiskt belagda registereffekter, externa källor, licenser och tekniker som inte fungerar i vanlig F6. Räkna inte historiska spel som *Let Me Out!*-PASS.
2. **Först uppmätt registerposition:** kontrollera `STA RESP1` med verklig PC/bank/scanline/cykel enligt MAIN:s senaste felanalys. Utan detta har trick 01–03, 09–10 och 15 för osäker praktisk grund.
3. **Sedan nödvändigt delbevis:** två olika original-8×9-NPC på faktisk fri X i samma höjdband samtidigt med fullstor gul P0-spelare och M0-skott. Jämför trick 02, 08–10, 13–15, 24. Stanna vid FAIL.
4. **Därefter endast vid explicit auktoriserad fortsättning:** fullt R1 sex NPC, sedan R2 nyckel och R3/R4 utan nya grafiska kompromisser. Testa inklusive PF-väggar och nyckel/svart nyckelhål, inte fristående demonstrationer.
5. **Separata eller senare ämnen:** trick 20–23 avser främst spellogik/minnesdisciplin; 27–30 kräver specialcart eller ny arkitektur. Inga sådana kartbyten eller fullspelssteg följer av denna rapport.

**Beslutsgräns.** R1 är fortfarande FAIL/BLOCKED i rapporterade prover. Venetian och SEX_X_FREE är negativ evidens för sina specifika varianter, inte ett generellt omöjlighetsbevis. Forskningsbilagan ändrar inte användarbeslut, slutliga grafikmasker, tillåten ROM-scope eller oberoende VERIFICATION. [P01, P04–P10, P12]
