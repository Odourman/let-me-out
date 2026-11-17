# LET ME OUT! – MAIN VI – OMPRÖVNING AV ALLA 30 ATARI-TRICK PER SPELOBJEKT
**Datum:** 2026-11-17. **Status:** `ADVISORY_CROSS_OBJECT_REASSESSMENT_ALL_30_SOURCE_ONLY`. **Mandat:** användaren: "Det är precis sådana här lösningar, Venetian Blinds, som jag ville att du skulle komma på när du kollade igenom de 30 tricksen. Kan du kolla igenom dom igen?" Ingen canonförändring eller G6/ROM-/GRAPHICS-implementation är auktoriserad.

**Verifierad primär projektkälla:** [exakt de 30 ursprungliga tricksen](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), SHA1 blob `99227686412d5d6cff475cfe97680f478719b71e`. Hela 30/30 lästa igen mot [G2 negativa bevis](gates/G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md), [G3 TIA budget](gates/G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md) och [femandroids-/Berzerk-/Video Chess idén](MAIN_VI_FIVE_ANDROID_BERZERK_VIDEO_CHESS_RESEARCH_DIRECTION_2026-11-17.md). Filen är **en ny tvärfunktionell revision**, inte omredigerad ursprungsresearch från RESEARCH II.

## 1. Grundläggande metodfel som nu rättas
Tidigare klassade vi flera trick nästan uteslutande efter frågan "Kan det lösa sex original-NPC fritt rörliga på samma Y?". Då kunde negativt android-Venetian-kernel-prov felaktigt sänka **alla** tänkbara användningsfall för Venetian. Samma sak riskerar ske med **dynamic PF (#05), M1/BL (#17), rasterfärger (#12), score mode (#18) och flera display kernels (#14)**. Man måste skilja ett visst register-/pixel-/scenprov från teknikens generella tillämpbarhet. Formulera alltid **vilket objekt, vilken Y-band-/CC-fördelning och vad som faktiskt kan falsifiera idén**.

**Korrigering av förra assistentens optimism:** "Venetian för nyckel + dörr" är en **hypotes och reserv**, INTE nödvändigtvis den bästa grundlösningen. Det enklaste är **samma sprite återanvänd i olika Y-band**; om dörren kan kodas med PF bör P1 kanske inte alls belasta dörren, och om K1/K2 ligger samma Y interleava först då. Video Chess bevisar att tekniken existerar, **inte** att key/door samtidigt har samma grafikkrav. TIA har fortfarande 2 players, 76c/line, 128B RAM, delade färger.

## 2. Riktigt nytta i Let Me Out! – omvärdering av precis 30/30
| **01** | Sprite Multiplexing | Androider vid olika Y; återanvänd P1 även för key/door när band ej överlappar | HÖG | Hårda same-Y-fall kvar; tids-/Y-scheduler krävs |
| **02** | Mid-scanline GRP Rewriting | Flera olika vita maskrader inom P1-kopior; möjlig X-sortordning | HÖG | Effektiv START/GRP-deadline, cykelkostnad och verkligt numerisk X måste bevisas |
| **03** | Venetian Blinds | Reserv för key+door vid verkligt gemensamma rasterrader; adaptiv interleave för sällsynta objektkonflikter | HÖG NY KORSANVÄNDNING | Tidigare FAIL gäller androidmaskerna, inte key+door; halv vertikal upplösning, key kan bli oläslig |
| **04** | Sprite Flickering | Nödlägesvisning av en överlappande extra NPC, inte för spelare/skott | LÅG/USER-GATED | Historiskt 1/6 av frames (=ca 10 Hz) FAIL; 50%-visning saknar användaracceptans och måste videogranskas |
| **05** | Dynamic Playfield Sprites | Statisk dörr eller enkel pickup-symbol via PF, alternativt dekorativ rörlig indikator | HÖG FÖR DÖRR | PF 4CC/bit och brun väggkanal; detaljerat guldnyckelhål knappast naturlig utan kombinering |
| **06** | Mid-frame Sprite Resizing | Begränsad animation/händelseeffekt, t.ex. dörrblink, eventuell framtida spelaranimation | LÅG | Ändrar storlek/silhuett; skapar ingen tredje 8-bitars NPC |
| **07** | Asymmetric Playfield | Stäng vänster ytterkant, skapa enbart höger utgång och eventuell portform | MYCKET HÖG | Frysta R3 vänster/höger PF-writes 7/15/22 och 37/45/52 i separat ROM, ej integrerat R1 |
| **08** | Two-Line Kernel | Dela tunga PF-, NPC-, key-/dörrskrivningar över två rader | MEDEL/HÖG OM MASKLÅSNING | Ofta halverad vertikal bildsampling. 9 individuella originalrader får inte tyst utgå |
| **09** | VDEL / Delayed Graphics | Förbered spelare/NPC-grupp och/eller BL-del mellan rader, hjälp tvålinjersschema | MEDEL/HÖG | Kan ordna latched GRP, men ger ingen extra TIA-kanal; frysta fragmentförsök FAIL för 9rad |
| **10** | HMOVE Fine Positioning | Finjustera X för två P0-roller, skott och M1/BL-nyckel | HÖG | HMOVE påverkar flera objekt samtidigt och ger ej fler retriggerfönster |
| **11** | Late HMOVE Trick | Polera vänsterkant-/HMOVE-bara när en kernel i övrigt fungerar | LÅG | Timingkänslig mellan TIA-versioner; inte en räddning av 76c/objektantal |
| **12** | Raster Color Changes | PF brun→orange nära höger dörr; eventuellt gul key i tomt PF-/P1-fönster | MYCKET HÖG | Färg delas: PF+BL, P0+M0, P1+M1; byte måste ske före riktiga CC |
| **13** | 48-Pixel / Six-Digit Score Kernel | Isolerad HUD/siffror, visning nyckelstatus ovanför spelplanen | HÖG FÖR HUD | Fast geometri och separat kernel; löser inte fem frirörliga NPC i spelplanen |
| **14** | Multiple Display Kernels | Separata HUD, vägg/room, tät NPC-zon, dörrsektion; ev. VBLANK-förval | MYCKET HÖG | Separata zoner löser INTE samtidigt belägna NPC+door+key; bankändring före zon med korrekt jumps |
| **15** | NUSIZ Sprite Duplication | Kopiera 2–3 vita masker med separata GRP-rader till låsta X-separationer | HÖG BEGRÄNSAD | Stort historiskt spawn-gap; NUSIZ0 påverkar M0-kopior och kan duplicera skottet |
| **16** | Sprite Reflection | Spara mask-/animationsdata när masken faktiskt kan speglas utan figurbyte | MEDEL SENARE | Kan ändra originalidentitet/ansikte; ej spriteantal eller fria X |
| **17** | Missile and Ball Reuse | M1 eller BL som tunn guldkey, key-stam/skott, nyckelhålsdetalj eller dörrstreck | MYCKET HÖG NY KORSANVÄNDNING | M1 delar COLUP1 med vita P1-NPC och kopiemode; BL delar COLUPF med bruna PF |
| **18** | Playfield Score Mode | Separat HUD med två färger; kanske färgfall vid dörr under mycket korta intervall | MEDEL/LOW FÖR DÖRR | PF färgas COLUP0/1 och kolliderar med gul spelare/vit NPC; inte brunt PF i spelzonen gratis |
| **19** | Playfield Priority Switching | Vägg framför aktörer, visuell nyckelskymning/dörrlager som kombination | MEDEL | PFP är globalt lagerbyte för PF/BL och inte key/NPC objekt-ID; O1 kräver logik |
| **20** | Hardware Collision Latches | Hjälp för skott/vägg och aktör/rum; kombinera med mjukvaruhitboxar | HÖG FÖR GAMEPLAY | Återanvända P1/M1 ger inte vilken av 5 NPC som träffats |
| **21** | RIOT Timer Scheduling | VBLANK: sortera X/Y, räkna fas- och registerevents, bygga rullande kö; AI i overscan | HÖG INFRA | Ger inte mer än 76c synlig rad, och CPU-tid i VBLANK är begränsad |
| **22** | Stack/RAM Mirroring | Kompakta specialrutiner eller överlagrad RAM-livstid i kärnan | LÅG | Hög stackkorruptionsrisk; skapar inte extra RAM |
| **23** | Undocumented 6502 Opcodes | Eventuellt rädda några verifierade cykler i kritisk innerloop | LÅG SIST | Kompatibilitet/revisioner; kan inte lösa färg-/pixelkonflikt |
| **24** | Precomputed Tables and Cycle-Exact Kernels | Sortera riktiga numeriska X/Y till per-rad eventköer före visning; uppdatera bara icke-noll originalmaskrader | MYCKET HÖG | 128B RAM/stack och aktiv F6-bank, fysiska START faser; inte 2^N unrolled specialprofiler |
| **25** | Stack-Based TIA Register Tricks | Enstaka snabb TIA-registerskrivning om faktiskt sparade 6507-cykler | LÅG SISTA RESORT | Stackpekare/stackbus påverkar register, stor korrumperingsrisk; ingen extra sprite |
| **26** | Timing-Based Horizontal Scrolling | Eventuellt framtida rumseffekt; inte vår nuvarande statiska kartlayout | LÅG | Ingen ny oberoende NPC-kanal, ingen ny dörrfärg |
| **27** | SCABS – Automatic Bank Switching | Historisk idé om programmerbar bankning | EJ TILLÅTEN F6 | Specialkassett, ej v0.18 eller vanlig F6, ingen ny TIA-sprite |
| **28** | Extra Cartridge RAM / Superchip / Supercharger | Extra RAM skulle förenkla scenqueue/AI om format särskilt auktoriseras | EJ TILLÅTEN F6 | Extra cartridge-RAM/Supercharger bryter standard-F6 och eliminerar inte 76c |
| **29** | DPC – Display Processor Chip | Historisk snabb datamatning/ljud som kontrafaktisk jämförelse | EJ TILLÅTEN F6 | Särskild kassett, inte våra fysiska playerkanaler |
| **30** | DPC+, CDF och ARM-coprocessorer | Framtida separat hårdvarustudie om användaren uttryckligen vill | EJ TILLÅTEN F6 | Kräver specialhårdvara, inte lösningen när standard-F6 är målet |

## 3. Kombinationspaket som de enskilda 30 tabellposterna MISSAR

### A. Högst potential: "R1 utan sex-sprite-retorik" (#01 + #02 + #09 + #10 + #14 + #15 + #21 + #24)
Bygg en **Y-/X-sorterad renderingsplan före aktiva bildrader**, inte 2^5/2^6 förkompilerade helkernlar. Samla varje 8x9 originalmaskrad; där en sprite har radbyte 00 behövs ingen bitmap på just den raden (men maskens ursprungliga nio radpositioner måste vara intakta). Rendera vita M/M/F/SM/SF på P1 och/eller låt P0 växla mellan gul player och vit NPC via exakt färg-/RESP-fas. **Villkor:** för varje source-RAM-X/Y, realtid behöver utföra riktig numerisk sortering och fysisk TIA-start före pixeldeadline. 5 same-Y kan ha fem nonzero maskrader och är fortfarande blockerande med endast två playerströmmar. Den här kombon är möjlig att KÄLLPRÖVA, inte redan visad.

### B. Störst "missad möjlighet": dörr utan hel P1 (#05 + #07 + #12 + #14 + #19 + #24)
För den **stationära endast-högerdörren** pröva att:
1. Håll verkliga bruna asymmetriska PF-väggpixlar och stängd vänsterkant.
2. På dörrens Y-rader, forma orange port vid **sista högra PF-cellerna** genom sen `COLUPF`-växling eller annan spårbar PF-färglivstid, *om* ingen annan aktiv väggcell felaktigt färgas orange på vägen.
3. Gör svart nyckelhål som **negativt utrymme** genom att inte tända relevanta orange registerpixlar så att svart `COLUBK` faktiskt syns. När P1-overlay är genomskinligt måste **PF bakom också vara 0** eller kan ytan bli brun, inte svart. PF bitbredd 4 CC kan göra exakt K11-nyckelhålsform omöjlig; kräver pixelmåttsgranskning. Om PF-cellen vid låst dörr rensas kan orange barriär ändå visuellt blockera och spellogik blockera, men det är ett separat acceptans-/maskbeslut.
4. **R3 fryst** var isolerad högerdörr med P1-orange-nyckelhåls-overlay och PF-skrivningar upp till c52, P1 runt c62; detta är INTE tidigare bevis för PF-baserad orange port. Om ingen giltig PF-fas finns, behåll P1 men reservera bara ett selektivt dörrband.
Vinsten om detta fungerar är att **spara P1** just där en gul player/vita NPC annars kolliderar med dörren – en mycket större vinst än att pressa in ytterligare en android i 76c.

### C. Guldnyckeln utan en 8bitars P-sprite (#17 + #12 + #19 + #09 + #24)
Föreslagen geometrisk nyckel som bygger på **enbitars M1 eller BL** vars position/enable/width varierar över flera rasterrader; möjligen hjälp av VDEL/hållna latchar. **M1 tar COLUP1 från vit P1-NPC, BL tar COLUPF från brun PF.** Guld under samtidig vit NPC/brun vägg kan inte uppstå gratis genom att ge nyckeln en egen färg. Source-only jämför:
- M1-guld **i fria colorclock-fönster** där vit P1 inte måste visas i samma pixelintervall; `COLUP1` ändras till guld och återställs till vit med deadlines. Kom ihåg att NUSIZ1-kopior också kan påverka M1.
- BL-guld **mellan PF-väggars aktiva färgklockor** med tillfälligt `COLUPF` och återställning, men kantväggar får inte färgas guld samtidigt; risken är hög.
- Om användarens befintliga **O1** tillåter att NPC skymmer den logiskt fastplacerade nyckeln skall renderern kunna undertrycka synligheten vid konkret overlap och sedan återställa samma X/Y. **O1 ger ingen generell licens att låta nyckeln försvinna alltid.**
- En liten nyckel med flera utskjutande tänder kräver kanske mer bitmapdetalj än 1bitars M1/BL klarar. Pröva faktisk K09/K11 originalform utan att ändra den.

### D. Venetian Blinds på rätt plats (#03 + #01 + #08 + #09 + #14)
Använd först **K1 vanlig Y-separerad reuse** för nyckel/door om möjligt. Om de verkligen delar rasterband, pröva **K2 adaptiv/avgränsad Venetian**: låt endast de berörda objektens pixelrader alterna under faktiska same-Y-konflikter, inte en global varannan-linje-effekt som förvränger alla original 8x9 androider. Testa både samma frame (4/5 av nio rader blir synliga) och eventuella växlande frames med tydligt skimmer. **K2 kan vara sämre än K3 PF-door + enkel P1/M1-key**. Ingen antagen PASS av hela originalnyckeln eller orange keyhole förrän användaren ser autentisk bild/video.
Ett tidigare T06/T07-FAIL för 9-raders NPC har **ingen allmän evidens mot** att K2 kan användas i dekorativa/static/pickup-roller, men alla verkliga fysik-/cykelkonflikter kvarstår.

### E. Låg risk som bör separeras: HUD (#13 + #14 + #18 + #21 + #24)
48-pixel/six-digit score-kernel och `CTRLPF SCORE` kan fungera i en **egen HUD-zon utan aktiva NPC**. Där spelar det mindre roll att PF är färgat efter COLUP0/1 eftersom vi inte samtidigt kräver brun vägg, gul player och vit P1 i samma rasterband. Detta är ett positivt sätt att kombinera trick som tidigare avfärdats på grund av spelplanskonflikt. Det **löser inte** R1/R2, men gör score, liv, nyckelstatus billigare i speldelen.

### F. Begränsad prioriterad spritesynlighet istället för 10Hz (#04 + #19 + #20 + #24)
Undersök per-objekt och per-scanline prioritet **endast om användaren separat överväger explicita visuella kompromisser**. Rotera belastning över rader istället för alltid att en av sex är synlig endast 1/6 frame. Jämför i verklig video vid värsta overlap om hoten alls går att läsa och om spelare/skott alltid syns. Detta är INTE tyst acceptans för förlorade masker eller flicker.

## 4. Föreslagen strikt prioritetsordning (RESEARCH, ingen implementation)
**Prioritet 1:** B, PF-dörr och negativt svart keyhole. Analysera faktisk 40x22-karta C02, dörrens exakta källmask och CC-krav. Fråga om P1 kan frigöras i dörrbandet, INTE bara om R3 separat kan upprepas.
**Prioritet 2:** C, M1/BL-nyckel och deras färgkonflikter (gärna O1 som exakt scene-conditioned skjul; inte generell försvinnande symbol). Testa faktiskt 8x9/K09/K11 key silhouette kontra endimensionella register.
**Prioritet 3:** D, key/door Venetian bara i verklig register-/Y-konflikt; kolla om den över huvud taget behövs eller skapar mer randartefakter än nytta.
**Prioritet 4:** A, fem-NPC datastyrd Y-/X-scheduler jämförd med Berzerk-källarkitektur. Det är dyrast och störst risk; gör först source-only beräkning med 5 same-Y nonzero originalrader, P0 gul + skott, P1/PF och 76c worst case. **Ingen F12/G6-ROM utan ny order.**
**Prioritet 5:** E, separat HUD-kernel som lågriskdel, men inte före grundläggande användarbeslut.
**Prioritet 6:** F är val av synlighets-/designwaiver som ENBART användaren kan ge.

**Måste fortfarande prövas:** ett verkligt avståndsfritt RAM-X-scenario, inte NUSIZ-only med spawn-gaps; P0+M0 färgkonflikt vid samma pixel; verkliga PF-datum/door form; originalmask topdown-orientering; 128B RIOT plus stack; 4KB aktiv F6; 76c på exakt samma skannrad. Befintliga G1–G5 statusar, sex-NPC-canon och blockerad R1 ändras inte.

## 5. Källor och bevisstatus
- Ursprungliga 30: [RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md); den här filen lägger **inte** till eller tar bort något nummer.
- [G2 negativa körningar](gates/G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md); [G3 hårdvarukontrakt](gates/G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md); [G4 förregistrerad hypotetisk mikro](gates/G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md).
- [Femandroider, Berzerk och Video Chess – dokumenterad kandidat, ej godkänd canon](MAIN_VI_FIVE_ANDROID_BERZERK_VIDEO_CHESS_RESEARCH_DIRECTION_2026-11-17.md).
- [Original Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) för COLUP0/COLUP1/COLUPF/CTRLPF/PF/Mx/BL/NUSIZ/76c.
- [1983 års samtidshistoriska Video Chess-källa](https://www.atariage.com/2600/archives/design_case.html): Bob Whitehead delade 8 pjäser över växlande rasterrader, med synliga ränder. Detta är ett historiskt faktum, ingen verifierad key/door-integrationslösning.
- [Atari 2600 Programming for Newbies, tvålinjers-kernel](https://cdn.hackaday.io/files/1646277043401568/Atari_2600_Programming_for_Newbies_Revised_Edition.pdf): motiverar varför tvålinjersschema inte kan antas bevara nio unika pixelrader.
- Framtida officiell forskningsgranskning kan läsa [Berzerk reverse-engineering-disassembly översikt](https://awesomerea.org/resources/berzerk-atari-2600-disassembly-case/); vår rapport har **inte** genomfört oberoende byteidentiskt Berzerk-kodrevision.

**Auktoritetsgräns:** detta är MAIN VI:s rådgivande återgranskning och förbättrade forskningsprioritering efter användarens kritik, **inte** RESEARCH II:s implementation eller VERIFICATION II:s oberoende E02. Inget G6-, F12-, byte-/layout-/kassett-/mapper-, gameplay- eller designwaiver-beslut fattat.
