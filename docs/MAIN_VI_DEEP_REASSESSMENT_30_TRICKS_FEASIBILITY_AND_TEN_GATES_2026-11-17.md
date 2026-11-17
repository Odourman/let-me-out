# LET ME OUT! — MAIN VI: fördjupad feasibility-revision, 30 Atari-trick och omarbetad tiogrindsplan
**Datum:** 17 november 2026 (Stockholm). **Klass:** MAIN VI, read-only-källanalys och strategisk planberedning. **Ingen kodauktorisation**, ingen F12, ingen gameplay-/PAL-/mapper-/grafik-/VERIFICATION-order, inget PR-merge och ingen designwaiver. Ingen ROM, DASM eller Stella har körts inom denna nya rapport.

## 0. Utgångsfrågan och skärpt slutsats
Målet är **ett faktiskt spel som bevarar användarens Let Me Out!-idé**, inte en oändlig följd av positiva mikrodemos. Den föregående tiostegsplanen (MAIN_VI_LAST_10_CURRENT_NEXT_10_ROADMAP_2026-11-17.md) var rimlig som grov riktning, men **för linjär och otillräckligt riskstyrd**. Det var fel att låta R2 och R3 komma först efter R1 som om deras resursbehov vore gratis. Den nya ordningen prövar ett **sammanhängande resurskontrakt för R1/R2/R3/R4 redan före ny ROM**, och separerar sedan varje kodleverans.

**Teknisk slutsats:** Det är möjligt att bygga delar av grafiken på standard-Atari 2600/F6, och tidigare research visar fyra olika original-NPC i en särskild samtidig P0/P1-konfiguration. Det är INTE bevisat att vi kan visa sex rättvända, logiskt numeriskt oberoende X/Y-NPC på exakt samma 9-raders rasterband tillsammans med gul spelare, aktivt skott, bruna PF-väggar och senare nyckel/högerdörr. Ingen universell omöjlighetssats finns. Den exakta nuvarande acceptansribban bör klassas **HIGH-RISK/UNPROVEN** snarare än GO eller evigt forskningskrav utan stopptidpunkt. En högre kart-/hårdvaruflexibilitet kräver användarbeslut och skapar inte automatiskt fler TIA-playerkanaler.

## 1. Kontroll av faktisk auktoritet, scope och källtyper
- GitHub main vid start: `165c0d021be9c47ad1ff91a6e8f6041aef4af2d2`; Issue #6 OPEN och gäller **endast auktoriserad v0.18 NTSC R1–R4 diagnostik**. PR #7 OPEN/DRAFT/UNMERGED, head `82667dae033f70570dce903f8e1d4866528be02a`; Issue #8 OPEN men gäller fryst äldre baseline `561d3baf...`, INTE automatiskt F9–F11.
- F9 `c36982aef770af6cd3f68c2da37b8ed14aee2393`: EN 16K F6-ROM med **tre separata BINÄRA** RAM-X och åtta förkompilerade formationer, tre rättvända originalmasker, 144 Stella-bilder och lokal/MAIN pixelgranskning; **inte** fri numerisk X/Y.
- F10 `ef854d7436f1e1650827e2e19cc1b3d33a17f054`: endast källanalys, ingen bevisad sex-fri-X/Y-arkitektur.
- F11 `dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4`: **G0 FAIL, G1 NOT RUN, inga F11 ROM/Stella/DASM**; käll- och START-/GRP-/numerisk-scheduler-hinder för just fyra-P1-scope, inte universellt bevis mot alla P0/P1-varianter.
- Äldre forsknings-R1ba (600 verkliga Stella-rutor) har visats ha fyra stora androidmasker vertikalt felvända vid korrekt originaljämförelse; äldre `600/600 six correct originals` är falskt. Repetera inte det som kanonbevis.
- Ursprungligt 57-beslutspaket och skisser i Drive är ursprungligt användarunderlag. `docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md` förtydligar senare användarbeslut. Maskcanon `design/NPC_REFERENCE_8x9_masks.json`, blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, alltid TOP-DOWN. Sex = M,M,F,F,SM,SF, numeriskt separata X/Y, gul player med hatt/vapen, M0-skott, bruna PF-väggar, endast höger orange port och svart nyckelhål, O1-nyckel, spelregler och RESET-begränsning bevarade.
- Nyare användargodkännande gäller även **luftigare rum som designriktning**. `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json` innehåller **icke-slutgodkända exakta** A/B/C/D-matriser, och de äldre A01/B01/C02/D01 är historisk studiebas. En rasterbudget får inte tyst anta v0.19-matriser som canon eller använda färre väggar som bevis på att R1/R3 är lösta.
- Den 55-sidiga forskningsavhandlingen i projekt-Drive innehåller **52 delvis överlappande teknikmönster, exakt 30 ursprungligen numrerade trick och 67 historiska risker**. De är **inte 82 oberoende tekniska lösningar**. Hela paketet är rådgivande.
- Kontrollernas gräns: denna rapport har läst projekt-/Drive-texter, samtliga 30 tricken, PDF-forskningsatlas/riskgrupper, relevanta frysta originalrapporter och verkligt källpublicerade R1e/f/g-resultat, men har **inte laddat om och självständigt kört om samtliga gamla forsknings-ZIP/ROM-binärrutor**, så påstådd R1g 600/600 står på forskningsrapportens och tidigare lokala evidensens nivå, inte ny E02.

## 2. Viktigt ytterligare researchspår: P0 OCH P1 tillsammans
**R1e:** Tre vita NPC i P1 samt en fjärde vit i extra P0-wide-copy samtidigt med gul P0-spelare. Fyra olika rättvända originalmasker i en statisk lokal Stella-geometri, medan testskott M0 låg på rasterraden före NPC-bandet och PF-vägg saknades.
https://github.com/Odourman/let-me-out/blob/research/main-ii-r1e-four-originals-p0wide-calibrated-20261116/docs/MAIN_II_R1E_FOUR_DISTINCT_ORIGINALS_STATIC_LOCAL_PASS_2026-11-16.md

**R1f:** Två separata P0 `RESP0` på varje rasterrad (och korrekt `GRP0/COLUP0`-byte) gör att fjärde vita NPC kan flyttas åtminstone mellan två särskilda positioner utan att gul spelares X flyttas; tidigare R1e-wide-copy var annars X-kopplad.
https://github.com/Odourman/let-me-out/blob/research/main-ii-r1f-resp0-independent-fourth-20261116/docs/MAIN_II_R1F_RESP0_BREAKS_FIXED_P0_COPY_X_STELLA_LOCAL_PASS_2026-11-16.md

**R1g:** En ROM med fyra diskreta fjärde-NPC-X-lägen och rapporterade 600/600 korrekta Stella-frames. Alla tre P1-NPC och gul spelare har FAST X; endast fjärde NPC växlar förkompilerade fyralägeskernlar, ingen generaliserad numerisk X-scheduler, inget fullständigt P0/P1-positionskors, inga same-row M0/PF/R2/R3.
https://github.com/Odourman/let-me-out/blob/research/main-ii-r1g-four-X-dynamic-600-20261116/docs/MAIN_II_R1G_FOUR_X_DYNAMIC_600_STELLA_LOCAL_PASS_2026-11-16.md

**Varför det är intressant:** En blandad P0/P1-kernel fördelar bitmaphändelser över två verkliga playerkanaler. Det kan undvika en del av F11:s P1-only `RESP1`-fönsterkonflikter.

**Varför det ännu INTE räddar R1:** P0 måste vara gul för spelaren men vit för vissa NPC, så ordningsbyte X(NPC) <-> X(spelare), sammanfallande pixelpositioner, överlapp och omvänd färg-/GRP-ordning är oprövade. Sex vita NPC + gul spelare är totalt SJU fulla bitmapobjekt på möjliga gemensamma rasterrader, plus M0 och PF; R2 kräver även guld för nyckeln, R3 orange/svart högeröppning. Två playerkanaler är fortfarande bara två playerkanaler. R1g:s fyrlägesval är en diskret speciallösning liknande (men inte identisk med) F9:s profilprincip. Detta får aldrig bokföras som fri X för fyra eller sex.

## 3. Oberoende hårdvarureferenser, inte löften
- Andrew Towers, `TIA Hardware Notes`: https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php — retrigger/start-decodes, counter stop i HBLANK, close/medium/far, risken att andra RESET kommer före START/latch. Inte en allmän garanti för godtyckliga X.
- Stella 6.7.1 versionspinnad primärkod: https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/tia/Player.cxx ; https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx ; https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/CartF6.cxx . `Player::resp` påverkar `myRenderCounter` beroende på `myIsRendering`; decodes offset 12/28/60/156; F6 hotspot 0x1FF6–0x1FF9.
- Atari `Stella Programmer’s Guide`: https://www.atariage.com/2600/programming/2600_101/docs/stella.html — två 8-bitars players, GRP/VDEL, NUSIZ, playfield och CPU-bunden videoutmatning.
- 8bitworkshop 2025 `Versatile Playfield Kernel`: https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html — en enskild valbar TIA-registeruppdatering per två scanlines kan minska PF-bördan men bevisar inte sex same-Y-NPC eller exakt 9-raders original.
- 8bitworkshop 2025 `Three-Stream Versatile Kernel`: https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html — två display-list-streams plus PF; erkänner explicit RAM-, CPU- och sprite-/färguppdateringsbegränsningar, inklusive upp till 32 byte per lista i det schemat. Kan hjälpa Y-separerade objekt eller förberedelse, inte ensam lösa sex same-Y med godtyckliga X.
- Stella debugger: https://stella-emu.github.io/docs/debugger.html — `_scan`, `_sCycles`, `_bank`, TIA `trapWrite` och råpixlar; kontrollera att just använd 6.7.1-versionens debugsyntax/mätpunkt gäller. Nyare onlinehandbok kan avse 7.0, vilket inte uppgraderar gamla Stella-bevis.
- Hårdvarufakta: 228 TIA-colorclocks = **76 CPU-cykler/scanline**, 68 HBLANK + 160 synliga colorclocks. `STA WSYNC` kostar också CPU-tid; generellt finns högst 73 cykler för annat arbete i en 76-cykels WSYNC-ankrad rad. RIOT RAM totalt 128B; vanlig standard-F6 = fyra 4KiB-banker, EN resident bank åt gången. ROM-bankning skapar INGA extra cykler eller sprites. VBLANK/Overscan kan förberäkna men inte ändra synlig pixeldeadline.
- Ingen ny verklig fysisk Atari-konsol-/TV-testning utförd. Vissa avancerade TIA-/HMOVE-trick bör inte byggas enbart på Stella 6.7.1 om fysisk kompatibilitet blir en releasegrind.

## 4. Bedömning av exakt ALLA 30 ursprungliga trick (mot verkligt behov)
| # | Teknik | Beslut för nästa R1-spår |
|---|---|---|
| 01 | Sprite multiplexing | HÖG: använd på skilda Y, same-Y kräver separat retrigger; ingen gratis tredje sprite |
| 02 | Mid-scanline GRP rewriting | KRITISK: originalmask/färgswitch per korrekt START-fönster |
| 03 | Venetian blinds | EJ huvudväg: 9-/18-raders- och VDEL-specialtester gav förlorade originalrader |
| 04 | Frame-flicker | 1/6-periodiskt 10Hz redan FAIL; mindre/30Hz adaptivt flimmer ENDAST hypotetisk ny användarbedömd kompromiss, ej automatiskt godkänd |
| 05 | Dynamic PF sprites | Ej för fina originalhumanoider: 4 colorclocks/bit och PF upptaget av väggar |
| 06 | Mid-frame sprite resizing | LÅG: extra storlek utan nytt självständigt bitmapobjekt |
| 07 | Asymmetric PF | KRITISK för R3: höger enda öppning, dyr mittlinjebudget |
| 08 | Two-line kernel | VILLKORLIG: mer förberedelsetid men får inte offra verkliga 9 bildrader |
| 09 | VDEL / delayed graphics | VILLKORLIG: värdefull latch-/GRP-timing, ingen extra player |
| 10 | HMOVE fine positioning | VIKTIG för precision; flyttar inte godtyckligt flera kopior individuellt |
| 11 | Late HMOVE | LÅG: fysisk chip-/fasrisk, inte startarkitektur |
| 12 | Raster color changes | HÖG i tvåkanalsspår: P0 gul/vit och senare gold/orange, kräver klockade writes |
| 13 | 48-pixel/six-digit kernel | LÅG för R1, senare HUD; fast kopiegeometri inte sex fri-X |
| 14 | Multiple kernels | HÖG för separata Y-zoner och HUD; samma-radsschemat måste ändå bevisas |
| 15 | NUSIZ duplication | HÖG men begränsad: close/medium/far och färgswitch kan bidra, fasta relationer är ej fri-X |
| 16 | REFP0/REFP1 | LÅG: spegling sparar bitmaps i vissa riktningar, ändrar original utan tillstånd |
| 17 | Missile/ball reuse | MEDEL: M0 reserverad för skott, M1/BL är enbitsresurser, ej 8x9 humanoid |
| 18 | PF score mode | LÅG: påverkar PF-färg via COLUP0/1 och kan skapa vit/gul/brun-konflikt |
| 19 | Playfield priority | MEDEL för O1-skymning, löser inte individidentitet eller knappt bitmappsalternativ |
| 20 | Hardware collision latches | SENARE: latch identifierar inte automatiskt vilken multiplexad NPC som träffats |
| 21 | RIOT timer scheduling | VIKTIG för offscreen-spellogik/262-radsstabilitet, inte fler synliga cykler |
| 22 | Stack/RAM mirroring | LÅG–MEDEL för kompakt minneskarta, inget mer RAM, hög korruptionsrisk |
| 23 | Undocumented opcodes | SISTA UTVÄG, kan spara enstaka cykler, versions-/hårdvarurisk |
| 24 | Precompute/cycle-exact kernels | KRITISK: förbered sort/bitmap/eventplan under VBLANK; 2^N-formationer skalar uselt |
| 25 | Stack-based TIA writes | LÅG: särskilda tidsvinster möjliga, stack-/PC-/hårdvarurisk, löser inte ny grafikkanal |
| 26 | Timing horizontal scrolling | EJ relevant för befintligt statiskt rum |
| 27 | SCABS bank switching | Utanför standard-F6 och aktuell auktorisation |
| 28 | F6SC/Superchip/Supercharger RAM | Utanför standard-F6, hjälper RAM men inte 76 cykler/sprites |
| 29 | DPC | Utanför standard-F6 och aktuell auktorisation; ingen extra TIA player |
| 30 | DPC+/CDF/ARM | Utanför nuvarande F6 och aktuell auktorisation; kräver separat fysisk/ROM-kompatibilitetsprövning |

**Praktisk huvudkombination:** 01+02+09+10+12+14+15+24, med 07+19+21 för R2/R3/övrigt. De 52 T-teknikposterna kompletterar med 2025 års display lists, Y-sorterad renderlista, RAM-overlays, uppdelad AI, banktrampoliner och 2-/3-stream-studier. Inga av dessa får räknas som nya, oberoende bevis för R1.

## 5. 67-riskavhandlingens betydelse för ordningen
- **1–25:** raster-R1/R2, tre samtidiga färgfamiljer, sex maskers position/same-Y, P0/P1, PF, R3, 128B RAM, oberoende evidens/hårdvara. Detta är blockerande arkitektur, inte spelbalans.
- **26–41:** AI, väggblockering, skott och prioriteter, nyckelbärare, K1/E1, spawn, svårighetskurva. Spelkrav som bör modelleras SOURCE-ONLY och implementeras endast efter gameplayauktorisation.
- **42–48:** val av öppna exakta kartmatriser fortfarande ej formellt slutgodkänt; offline geometri är inte TIA-collision.
- **49–58:** poänggolv, extralivspassager, highscore-villkor, HUD, två ljudkanaler, GAME OVER/RESET; reservera RAM/ROM/CPU-platser tidigt men INTE programmera dem ännu.
- **59–67:** felaktig äldre status, PNG-pixelvalidering, käll/ROM/commit-hash, fristående Verification, ingen implicit designwaiver, inget nytt cartridgemapperformat. Dessa kontroller måste finnas i **varje** kommande leverans.
Det saknas anledning att genomföra 67 separata teknikexperiment. De mappas till de nedanstående få hårda grindarna och framtida speltester.

## 6. De fyra scenfamiljerna måste alla räknas in FÖRE nya ROM-beslut
| Test | Aktuellt resursbehov | Otillåten genväg | Planerad fråga |
|---|---|---|---|
| R1 | 6 original-NPC på same-Y och angränsande Y, gul spelare, aktiv M0, bruna PF | tre förkompilerade X-bitar, sex fixed formationer, 1/6 frames, inverterade stora | Kan varje NPC behålla numeriskt separat X/Y och korrekt mask i samma kärna? |
| R2 | 5 NPC, guldnyckel, gul spelare, aktiv skott, väggar, O1 | osynlig key trots ej skymd, underförstått delad X med white NPC | Var skapas GOLD-fönstret och vilken kanal ritar varje objekt? |
| R3 | låst/öppet endast höger; orange port svart hål; vänster solid + möjliga NPC | R3 isolerad local PASS i egen P1-/PF-kernel får inte räknas som integrerad | Finns PF-/player-fönster kvar när farliga figurer samtidigt befinner sig vid dörrens Y? |
| R4 | Y-offset, 6→5 antal, X-sortbyten, crossing, när-X, player/shot/key | alltid visa en luftig formation, eller justera förvald spawn för grafikens skull | Är raster/objektidentitet stabil vid varje tillåten rörelse? |

**Oundviklig pixelgeometri:** Om två vita 8x9-silhuetter delar samma X/Y kan en enda slutlig pixelmatris inte visuellt avslöja två fullständigt skilda vita objekt. Lika färg och faktiskt överlapp ger visuellt sammanflytande former även på kraftigare hårdvara. Kräv därför en explicit definition av vad som räknas som **logiskt korrekt överlapp/occlusion** kontra **otillåten rendering som tappat en NPC**. Det är ett framtida klargörande från användaren om en acceptanskonflikt kvarstår, inte ett antaget tillstånd att gömma fiender. O1 reglerar specifikt android/nyckel, inte automatiskt android/android.
**Timing:** `RESP`-registerwrite, TIA counter reset, START decode, 8-pixel patternlatch, nästa `GRP`, färgbyte, M0 och PF-side-write är olika deadlines; enbart totalsumma <76 räcker inte.
**Minne:** Sex logiska X+sex Y = minst 12 bytes innan player/shot/key/state/sort/stack. Naiv full 9-raders aktörssortering av sex IDs = 54 ytterligare bytes; full eventdata+times kan överskrida 128. En riktig RAM-livstids-/stackplan krävs; 4 × 4KB F6 är ROM, inte RAM.
**VBLANK:** kan beräkna actor sort och händelser på förhand, men löser inte midscanline deadline. 76-cykelgränsen kvarstår även för ARM/dyr mapper, eftersom TIA inte ändras.
**Färgkonflikt:** P0:s vit/gul-retrigger fungerar hittills bara med låst vänster-/högerordning. Player–NPC-korsning måste förregistreras och bevisas; senare GOLD-key och orange dörr kan kräva ännu fler färgbyten.

## 7. Korrigerade NÄSTA TIO: grindar, inte tio utlovade implementationssteg
Alla punkter är **beredda beslut/arbetsmoment**. Endast 1–4 är rimliga att göra nu som read-only-källarbete. För 5–10 gäller villkor; de kan **aldrig** utföras bara därför att de finns här. På NO-GO avslutas planen, övriga punkter utförs inte.

### G1. Lås en revisionsbar baseline för krav, läge och bevis
**Ansvar:** MAIN. **Scope nu:** READ-ONLY. **Indata:** original 57 beslut + skisser, beslutskomplement, R1–R4-scope, acceptans C01–C04/D01–D03/E02, v0.19-luftiga kandidatkartor, F2–F11, PR/Issues. **Leverans:** auditmatris med krav-ID, source ref/commit/hash, status BINDANDE/KANDIDAT/HISTORISK, okända val, separat definition av rasterhöjdsöverlapp och fysiskt pixelöverlapp. **PASS:** inga gamla 2026-11-15-snapshots eller research upphöjs till ny canon.
### G2. Reproducera forskningsförutsättningarna före ny hypotes
**Ansvar:** RESEARCH II/MAIN read-only. **Indata:** R1e/f/g original-RAM/ROM/.lst/.sym/PNG-index, F9 originalarkiv, F10/F11, R1ba-korrigeringen, alla 30+52+67. **Leverans:** per-arkitektur evidensskala och tabell med faktiskt antal rörliga NPC, deras X-domän, Y, M0-samma-rad, PF, P0-color, byte-/cykelmarginal. **PASS:** R1g betecknas endast en fjärde NPC i fyra diskreta X och kan reproduceras/inställningar/hashes separat; källor bekräftade. **Om arkiv saknas:** INCONCLUSIVE, ingen anpassad PASS.
### G3. Gör ett gemensamt R1–R4 resurs-/rasterkontrakt
**Ansvar:** RESEARCH II/MAIN, SOURCE-ONLY. **Leverans:** tabell per kritisk scanline över P0/P1/M0/M1/BL/PF/GRP/COLU/NUSIZ/RESP/START, spelarsprite/fyrtypsmasker, R2 nyckel, R3 PF/högerport; 76c, 4KiB aktiv bank, 128B RAM/stack, VBLANK-precompute; definierad logisk RAM-scheduler, scanline ordningsbyte och passagen över spelarens X. Jämför P1-only, dual P0/P1, NUSIZ hybrid, optimerad PF, display lists och EVENTUELL kontrollerad flicker som hypotes (ej godkänd). **PASS:** inga gömda omritningar eller "efterföljande steg fixar resursen"-antaganden.
### G4. Falsifierbar SOURCE-ONLY GO/NO-GO
**Ansvar:** MAIN efter RESEARCH II, ROM DEVELOPMENT III eventuellt som läsande teknisk rådgivare utan ROM. **Förprov:** sex same-Y separerade [16,36,56,76,96,116]; sex täta [40,44,48,52,56,60]; Y=[96,97,98,99,100,101]; X-ordningsinversion och player–NPC korsning; R2 GOLD och R3 PF i samma budget. **GO till ETT avgränsat fysikprov, inte GO för full R1:** minst EN sammanhängande, källmotiverad minimal P0/P1-numerisk-X-mekanism med föreslagna instruktions-, START-/GRP- och färgtidsfönster samt ett **tydligt falsifierbart okänt hårdvarubeteende**; reserverad övre CPU/RAM/ROM-kostnad och dokumenterad värsta-fall-gap-lista för återstående R1/R2/R3. **Det vore orimligt att kräva en fullt bevisad sex-NPC-programsekvens innan den avgörande P0/P1-fysiken ens är testad.** **NO-GO:** ingen sammanhängande plausibel ens liten P0/P1-mekanism efter verklig researchrevision, eller redan uppenbar fysikalisk register-/deadlinekonflikt. **INCONCLUSIVE:** då behåll HOLD och avgränsa högst en fysisk signaldetalj, inte en svepserie.
### G5. Beslutsgrind om arkitekturen eller acceptans förutsätter kompromiss
**Ansvar:** MAIN presenterar underlag, **ENDAST ANVÄNDAREN får ge grafiska/hårdvarurelaterade waivers**. Vid GO med obruten canon: MAIN får separat besluta om eventuell v0.18 R1-avgränsad kodorder. Vid NO-GO: presentera högst två tydliga alternativa vägar (ex. behåll exakt 2600/F6/canon och stoppa, eller explicit be om justerad flimmer-/occlusion-/X-domän/kassett-hårdvarupolicy). **Inte** automatisk minskning till fyra NPC, ändrad grafik, PAL/fullspel eller nytt mapperformat.
### G6. Endast efter separat ROM-auktorisation: minimal fysisk falsifiering
**Ansvar:** ROM DEVELOPMENT III, EGENKONTROLL; MAIN beställer explicit. **Scopeförslag (INTE beställt):** EN källreproducerbar NTSC standard-F6-fysik-ROM, som prövar **den minsta äkta sammanhängande kritiska P0+P1-kombinationen**: en gul P0-spelare vars numeriska X korsar minst EN vit originalmask i samma P0-band, samtidigt med minst två olika rättvända P1-originalmasker, en aktiv M0-projektil i det relevanta samma-Y-bandet och verklig brun PF-belastning. Om källbudgeten uttryckligen medger det används samtliga fyra M/F/SM/SF, annars är den fjärde masken **nästa grind och får inte ge positivt G6-bevis**. Förregistrera exakt X-ordningsbyte, STA RESP0/1/GRP0/1/COLUP0 deadlines, 9 korrekta källrader, RAM-inmatat NUMERISKT X, samma-ROM-kontrollfall, och stopp vid första pixel-/cycle-fail; ingen 2^N-modekatalog eller utvidgad svepserie. Syftet är att falsifiera en saknad F11/R1g-fysikpremiss, **INTE** att utge tre/fyra specialplacerade NPC som full R1. Först statisk G0 med hardware START/latch-plan, sedan G1 verkligt DASM/Stella med PC/_scan/_sCycles/trapWrite plus råpixel. **STOPP** om första falsifieringsgrinden misslyckas. F11 tidigare fel får inte döljas med nytt etikettnamn.
### G7. Endast efter positiv G6 och separat scope: R1 sex fria numeriska X/Y
**Ansvar:** ROM DEVELOPMENT III. **PASS**: sex låsta TOP-DOWN M,M,F,F,SM,SF, gul player full storlek, aktiv M0, PF väggar, alla C01/C04-fall; minst 600 sammanhängande bildrutor, 262-radersprofil och 76c-kontroll, sex individuella logiska X/Y och dokumenterade verkliga pixlar i samma körbar ROM, även när två X eller Y korsar varandra. Occlusion-policy måste redan vara definierad; aldrig 600/600 via inverterade stora masker eller 3 kopplade XY-profiler. MISS = STOPP, inte kosmetisk fix.
### G8. Endast efter positiv R1 och separata order: R2 och R3 resursintegration
**Ansvar:** ROM DEVELOPMENT III, MAIN sekvenserar. **R2:** fem NPC+nyckel+spelare+aktiv M0+PF, O1/key logisk oförändrad under kort/lång skymning, guldnyckel i korrekta rader; skild från gameplay-fullkey. **R3:** faktisk högeröppning i en laglig källspårbar karta, vänster kant solid, port orange och nyckelhål svart som två mål, R1/R2-objekt får finnas i dörrens Y. Separata tekniska subgrindar föregår integration; ett fristående R3-local-PASS är inte integrerat PASS. Om exakt v0.19-karta behövs begär separat användarbeslut.
### G9. Endast efter positiv R1+R2+R3 och separat order: R4/E02
**Ansvar:** ROM DEVELOPMENT III för deterministisk R4-rörelse och reproducibel v0.18-artefakt. **VERIFICATION II oberoende** först vid separat uttrycklig uppdragsorder på *exakt rätt fryst commit* med 16 T01–T16, byteidentisk rebuild/SHA, 600 följande rutor per kontrakt, verklig registertiming, distinkta FAIL/INCONCLUSIVE, inga lånade developer-PASS. Test på verklig 2600/hårdvaruvariationsstrategi rekommenderas separat före release, kan inte automatiskt räknas som E02 framgång. PR #7 draft tills rätt mottagning/merge-beslut.
### G10. Framtida spelbar vertikal slice endast efter helt NY användarauktorisation
**Ansvar:** MAIN begär scope; ROM DEVELOPMENT III implementerar enbart godkända delsteg. **Beredningsordning:** rörelse och 8-vägssikte/ett skott per knapptryckning; patrull/jakt som utlöses av första verkliga skottet; individuella träffar/8 riktningar; slumpad key-bärare/dödsanimation/O1/K1; låst/öppnad orange högra dörr + E1; poäng −25/+50/+100/+15 och liv/extraliv; HUD, GAME OVER endast RESET; fyra godkända riktiga rum och speltest/balans; ljud; PAL och manual/release separat. Inget av detta påbörjas inom Issue #6-diagnostiktillståndet. Step G10 är STARTPUNKT för en ny spelutvecklingsplan, inte löfte om att ett komplett spel uppstår där.

## 8. Föreslagen redovisningsform för ett konkret, framtida G2–G4 read-only underlag
1. `EVIDENCE_MATRIX`: source URL, commit SHA, actual ROM SHA, Stella version, unmodified original mask, actor count, independent X/Y, screenshot IDs, INCONCLUSIVE markers.
2. `RESOURCE_MATRIX`: R1/R2/R3/R4, per-linje/P0/P1/M0/M1/BL/PF, color switches, LATENCY, object IDs, occlusion, owner.
3. `CYCLE_LEDGER`: för varje WSYNC-ankrad rad: opcode, adresseringsläge, CPU start/end, TIA CC, GRP/RESP/START/latch/deadline och eventuella crossings. Enbart summering till 73 eller 76 räcker inte; G0 ska skilja CALL/setup och active screen band. Blotta statiska opcodeplaner utan numerisk datahärledning räcker inte.
4. `RAM_BANK_STACK`: budget 128B med alias/livslängd/stack highwater, aktiv bank max 4096B, bankhotspots/trampolin; VBLANK och overscan reserv för verklig AI/score senare.
5. `ADVERSARIAL_SCENES`: sex same-Y luftig/tät, staggered Y, player byter ordning, två NPC same pixel, R2 key/occlusion, R3 högerport och full PF, framtida 600 konsekutiva frames.
6. `GATE_DECISION`: `GO_SOURCE_ONLY` / `NO_GO_SOURCE_ONLY` / `INCONCLUSIVE_NEEDS_PRIMITIVE`; tydligt vilken EN minimal hypotetisk mask-/X-/färgfråga en ROM skulle falsifiera, alternativ och exakt authorization boundary.
7. `CANON_DELTA`: **tom** om inga direkta användarbeslut, inte automatiskt ifyllnad med gamla forskningsantaganden.

## 9. Aktuellt MAIN VI-beslut
**Godkänd arbetsprioritet nu:** användarens begärda källforskning har genomförts i denna rapport; nästa möjliga read-only underlag är G1–G4, särskilt original-R1e/f/g kontra exakta F11-START-fönster och en combined R1/R2/R3/R4 CPU/TIA-budget. **Ingen F12 eller ny kodorder**, inga ändrade kanonmasker/spelregler/kartor, inga andra projekt. Om SOURCE-ONLY visar NO-GO: presentera tydligt för användaren och lämna frågan vid G5 i stället för att påstå att G6–G10 automatiskt väntar.

## 10. Källindex
- Nuvarande MAIN: https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md
- Senaste tidigare tio-stegsplan: https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_VI_LAST_10_CURRENT_NEXT_10_ROADMAP_2026-11-17.md
- MAIN VI föregående granskningsbeslut: https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_VI_INITIAL_R1_FEASIBILITY_REVIEW_AND_HOLD_DECISION_2026-11-17.md
- Canon: https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md
- Scope/acceptance: https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_SCOPE.md ; https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md ; https://github.com/Odourman/let-me-out/blob/main/planning/ROM_GATE_V018_TEST_MATRIX.csv
- F9 frozen: https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md
- F10 frozen: https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md
- F11 frozen: https://github.com/Odourman/let-me-out/blob/dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F11.md
- 30 original tricks: https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md
- 52 technique atlas + 67 risks + 30 tricks 55-page PDF in project Drive: https://drive.google.com/file/d/1IHKg63PZGAYoi3fdJdwmOYsomDxumlIv/view
- Research archive ZIP in Drive: https://drive.google.com/file/d/1JgLBpjUIVRQegVUFVNn3DoZpxguDqSs4/view
- Original 57 decision + user sketches Drive ZIP: https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view
- Official v0.18 Issue: https://github.com/Odourman/let-me-out/issues/6 ; draft PR: https://github.com/Odourman/let-me-out/pull/7 ; older Verification Issue: https://github.com/Odourman/let-me-out/issues/8
