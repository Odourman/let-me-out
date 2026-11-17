# LET ME OUT! – MAIN VI: operativ beredskapsplan G1–G10, alternativ A/B/C
**Datum:** 17 november 2026. **Typ:** beredskap, risk- och teknikplan, INTE implementation eller designbeslut. **Källauktoritet:** de verkliga ursprungliga 57 användarbesluten och skisserna, senare uttryckliga användarbeslut, aktuell MAIN-status, v0.18 Issue #6/Scope/Acceptance, frysta käll-/ROM-/Stella-bevis; därefter rådgivande RESEARCH och denna plan. Inga slutsatser får ärvas automatiskt från ChatGPT Memory.

**LÄS FÖRST:** [MAIN VI:s fördjupade genomförbarhetsanalys och reviderade G1–G10](MAIN_VI_DEEP_REASSESSMENT_30_TRICKS_FEASIBILITY_AND_TEN_GATES_2026-11-17.md). Detta dokument är **ett operativt komplement**. Det supersederar INTE canon, det förvandlar INTE grindar till beställningar och det återöppnar INTE F11. Läs alltid live GitHub och Drive innan nästa verkliga steg.

## 0. Ledningsbeslut och riskprinciper

**Syftet är ett färdigt, originellt och spelbart Atari 2600-spel**, inte maximalt antal demonstrations-ROM-filer. Den största blockeraren är att visa sex fullständiga rättvända, distinkta M,M,F,F,SM,SF-masker (8×9 TOP-DOWN) med **sex logiskt numeriskt oberoende X/Y**, gul spelare, aktivt skott och bruna väggar, inklusive samma Y, grann-Y, positionskorsningar och täta X. Senare måste fem NPC och en guldnyckel (O1) samt endast höger orange låst/öppen dörr med svart nyckelhål rymmas i samma teknikbudget. Ingen verifierad full R1-kernel finns. F11: G0 FAIL, G1 NOT RUN, inga nya F11-ROM.

**Tre planvägar för varje grind:**
- **A = huvudväg**, standard-F6/NTSC och oförändrad användarcanon.
- **B = reservväg**, tekniskt annorlunda metod som OCKSÅ måste hålla canon och respektera explicit scope; ett annat ROM-experiment kräver en separat ny order.
- **C = säker stopp-/beslutsväg**, PASS/FAIL/INCONCLUSIVE redovisas, andra steg blockeras. Bara **användaren** kan tillåta designwaiver, nytt cartridgemapperformat eller senare fullspelsutveckling.
Ingen grind är automatiskt auktorisation för nästa. **G1–G4** tillåter nu endast läsning, analys, beredning och dokumentation. **G5** är ett framtida beslutstillfälle. **G6–G9** behöver separata ROM-/verifieringsorder om relevant grind passerats. **G10** kräver nytt uttryckligt användarmandat utanför v0.18.

**Aktuella källfakta vid denna genomgång:** GitHub MAIN var ec1c61b16d0573444d802c78db3d4cee7fe7ca9c före nya dokumentcommits. Issue #6 OPEN (NTSC-diagnostik v0.18 R1–R4), PR #7 OPEN/DRAFT/UNMERGED, Issue #8 OPEN och inriktad på gammal commit 561d3ba, inte ett nytt F9–F11-E02. Förändring av endast dokument i MAIN ändrar inte teknisk baseline. Exakt README/datum i gamla filnamn får inte ersätta HEAD/readback.

**Bevisgränser:** F9 bevisar tre separat RAM-binärt selekterade X, men bara två fasta möjliga X per NPC. R1e/f/g bevisar specialgeometri med högst fyra rättvända originalmasker i forsknings-egenkontroll. R1g:s enda ROM väljer fyra **förkompilerade** kernlar, medan endast den fjärde vita androiden ändrar sin diskreta X; tre andra vita och gul spelare är på fasta X. R1ba äldre 600-rams-PASS för sex rättvända är FEL: de fyra stora masker var felvända i den riktiga originaljämförelsen. F10/F11 är SOURCE-ONLY och inget universellt matematiskt omöjlighetsbevis.

**En ny särskilt viktig risk:** TIA delar färgregistren **COLUP0 mellan P0 och M0**, **COLUP1 mellan P1 och M1**, och **COLUPF mellan PF och BL**. Dual-P0/P1 med gul spelare och vit NPC måste därför också bevara **färg och läsbarhet för samtidigt synlig M0**. Om COLUP0 skrivs vit medan M0-objektet ritas blir det skottet vitt på dessa pixlar; M0 har INTE ett eget färgregister i standard-TIA. Detta följer av Atari Stella Programmer’s Guide och ska ingå i ALLA G3–G9 tester. Ett rent pixelantal utan färg- och registertidsgranskning är otillräckligt.

### 0.1 Hårdvarans verkliga budget
- En NTSC-rasterrad har **228 TIA-colorclocks = 76 CPU-cykler**, varav 68 colorclocks normal HBLANK och 160 synliga. Om 3 CPU-cykler används till STA WSYNC ryms normalt **högst 73 övriga CPU-cykler** i samma fulla WSYNC-ankrade rad; rätt visuella deadlines kan vara snävare. En tabell som bara visar totalen 74/76 kan därför fortfarande fallera om RESP/GRP/PF skrivs för sent.
- **Två 8-bitars players P0/P1**, två enbitsmissiler M0/M1, enbitars ball BL och grovkornigt PF. Sex logiska NPC kan förvaras i RAM men inte gratis som sex parallella TIA-sprites.
- **128B RIOT-RAM** inkluderar tillfälliga händelser/sortdata och stack. **F6 16KB = fyra 4096B-banker med en aktiv bank åt gången**; bankbyte ger inte mer rastertid/RAM/sprites. F6-hotspots 0x1FF6–0x1FF9.
- NUSIZ-kopiors START/latch, RESP återtriggning under aktivt renderfönster, VDEL, HMOVE och GRP/färgbyte måste behandlas som separata tidsvillkor. Stella 6.7.1:s Player::resp har tillståndsberoende renderCounter-effekt. Riktig hårdvarukompatibilitet är inte bevisad endast genom emulator.
- Det finns **ingen medgiven numerisk maxflimmerandel**. Ett tidigare prov med en NPC 100 av 600 frames (ungefär 10 Hz) är underkänt; låg nivå kort flimmer är ett kvalitativt användarbeslut, inte en fri genväg.
- Pixelöverlapp: om två identiskt vita silhuetter ligger på precis samma X/Y kan EN slutlig vit pixelunion inte visuellt visa dem som två separata individer. Detta är skilt från logisk korrekthet och skilt från godkänd nyckel-occlusion O1. Ingen automatisk waiver för NPC/NPC eller NPC/player får införas.

### 0.2 Gemensam ärendegång innan en grind markeras slutförd
1. Kontrollera LIVE GitHub HEAD, PR/Issues, Drive-källor och eventuell senare användarinstruktion; citera specifika ref/hash.
2. Identifiera **fastställt krav**, **kandidat**, **forskningshypotes**, **testbevis**, **framtida scope**. Rätta förväxlingar innan arbete.
3. Utse separat ansvar: MAIN beslutar/koordinerar; RESEARCH II analyserar; ROM DEVELOPMENT III skriver endast särskilt auktoriserad kod; VERIFICATION II är oberoende; GRAPHICS II endast uttrycklig grafikorder.
4. Frys minsta indata/utdata: källref/commit, scripts, ROM-SHA om någon, test-ID, målscen, fysisk koordinatenhet (TIA CC kontra Stella GUI-pixel), version Stella/DASM, resultat PASS/FAIL/INCONCLUSIVE/NOT RUN.
5. Lägg inte till nästa implementationssteg vid ny upptäckt. Stanna, skapa besluts-/riskdelta och begär rätt uttrycklig auktorisation.
6. Spara granskning och beslut i GitHub under docs/ samt Drive i projektmappen, länka från CURRENT_PROJECT_STATE, kontrollera readback. Behåll föregående källor och nederlag; ändra inte fryst original.

## 1. G1 – fastställ revisionsbar krav-, design- och bevisbaseline
**Läge nu:** READ-ONLY. **Ansvar:** MAIN VI. **Mål:** ett entydigt körbart beslutsunderlag innan något tekniskt lösningsförslag blir en arbetsorder.

**Förutsedda risker (G1-R1–R5):** (1) ursprungliga 57 beslut motsägs skenbart av historisk "ROM paused" och senare Issue #6; (2) frysta v0.18-kartor A01/B01/C02/D01 sammanblandas med v0.19 *kandidater* för luftigare 40×22-layout; (3) originalens TOP-DOWN M/F/SM/SF förväxlas med äldre vertikalt omvänd R1ba; (4) grafikskisser/GRAPHICS offlinekandidater upphöjs till bindande ROM-bitmaps; (5) den visuella betydelsen av "alla sex synliga" vid fysisk NPC/NPC-kollision är oklar.

**A – huvudsaklig lösning:** bygg en REQUIREMENTS_REGISTRY med separata ID för canon/acceptans/diagnostik/framtida gameplay; länka original-ZIP + beslutskomplement + aktuella Issue/Scope/Acceptance + exakta källmaskblobben + tre skisser. Markera APPROVED, CANDIDATE, SUPERSEDED, UNKNOWN, BLOCKED och rätt auktoritetsnivå; skriv separata poster för logiskt sex X/Y och faktisk visuell överlappning. Välj INTE exakta v0.19-kartor eller nya maskbytes automatiskt. Gör en tydlig "ingen ändring krävs"-ruta.

**B – reserv:** om någon handling saknas, rekonstruera med oberoende GitHub-blob, Drive-original och tidigare verifierad hash/manifest. Håll oförändrade krav som inte står i konflikt, isolera saknat objekt som INCONCLUSIVE och fortsätt endast med icke-beroende read-only-analys.

**C – stopp/beslut:** om en verklig motsägelse mellan användarbeslut eller olöslig definition av överlappning styr teknikvalet, stoppa just den delen och ställ EN konkret beslutsfråga till användaren med originaltext, konsekvens och rekommenderat oförändrat utgångsläge. Ingen designwaiver får skapas genom tyst "tolkning".

**Preppade leverabler:** G1_REQUIREMENTS_TRACE.md, G1_AUTHORITY_DIFF.md, BASELINE_MANIFEST.json (planerade dokumentnamn, inte redan skapade). **PASS/exit:** varje blockerande acceptans C01–C04, D01–D03, E02 och aktuell designreferens har entydig status och länk. **Fortsättning:** G2 read-only, inte G6-ROM.

## 2. G2 – oberoende proveniensgranskning av befintlig research
**Läge nu:** READ-ONLY. **Ansvar:** RESEARCH II, MAIN som oberoende granskare. **Mål:** veta vilken kod/ROM/evidens vi faktiskt kan bygga vidare på.

**Förutsedda risker (G2-R1–R6):** (1) gamla GitHub Actions-artifacts kan löpa ut; (2) en research-PASS avser bara en specialgeometri; (3) R1ba-pixeloraklet hade vertikal orienteringsbugg; (4) Stella GUI-koordinater behandlas felaktigt som 160 TIA-färgklockor; (5) olika ROM-varianter kallas en dynamisk ROM; (6) developer-lokal mätning misstas för E02 Verification.

**A – huvudsaklig lösning:** skapa EVIDENCE_LEDGER för F2–F11, särskilt F9/F10/F11, och R1e/f/g/R1ba. Kontrollera källa, fryst commit, källmaskens byte/hash, sammanhängande 600 originala frame-index, manifest/ZIP CRC/SHA, .lst/.sym, ROM-hash, verkliga registerfällor och vilka X/Y som faktiskt byts. Granska R1g:s build_dynamic.py: den väljer **en av fyra förkompilerade rasterkernlar med FRAMELO & $30**; bara fjärde NPC X är diskret dynamisk. Märk UNKNOWN där en binär inte faktiskt är tillgänglig.

**B – reserv:** om råarkivet är saknat eller utgånget: korskontrollera exakta GitHub-källblobs, Actions-loggar och äldre hashade Drive-manifest i READ-ONLY. Upprätta en noggrann reproduktionsorder för framtida auktoriserad identisk ombyggnad, men gör **ingen** ny ROM/Stella-testkörning under detta read-only-steg. För jämförelse får källkod inspekteras och begränsningar räknas manuellt.

**C – stopp:** om rapporterade 600/600 inte kan knytas till rätt ROM-SHA eller rättvända originalmasker, klassas testet INCONCLUSIVE/FAIL på sin bevisnivå. Baserad arkitektur får inte lyftas till G4-GO. Ingen retrospektiv efterjustering av förregistrerade positioner.

**Preppade leverabler:** G2_EVIDENCE_LEDGER.csv (status RAW_VERIFIED / SOURCE_ONLY / LOCAL_REPORTED / FAIL / INCONCLUSIVE), G2_OLD_TESTS_NOT_TO_REPEAT.md och G2_SOURCE_HOLES.md. **PASS/exit:** varje kritisk byggsten har uppmätt eller tydligt markerad obevisad omfattning. Viktiga researchkällor: R1e, R1f, R1g och F11 enligt källindex nedan.

## 3. G3 – gemensamt R1–R4 objekt-, färg-, CPU-, RAM- och bankkontrakt
**Läge nu:** SOURCE-ONLY. **Ansvar:** RESEARCH II/MAIN, senare ROM DEVELOPMENT III teknisk rådgivning om särskilt ombedd. **Mål:** innan en enda ny registersekvens prövas veta den maximala samtidiga resursbelastningen.

**Förutsedda risker (G3-R1–R8):** (1) två playerkanaler räcker inte för sju godtyckligt ordnade åttabitarsaktörer på samma Y; (2) P0 gul/vit och M0 gul/vit delar exakt COLUP0 – även en visuellt korrekt gul player kan ge VITT skott; (3) P1 vita NPC och eventuellt M1 delar COLUP1; (4) nyckelns guldfärg och dörrens orange/svarta detaljer ökar färgskrivningar; (5) R3 asymmetrisk PF behöver vänster-/högerskrivningar i rätt fönster; äldre R3 lokal källbudget nådde cirka 74/76 cykler ensam, inte inklusive sex-NPC; (6) 128B RAM kan överskridas av sex X+sex Y, typ/active-index, Y-sort, display lists, stack och AI-reservationer; (7) F6-bankskifte mitt i rad förstör PC/fortsättning, aktiv bank bara 4K; (8) 262 NTSC-rader hjälper inte om GRP/RESP skrivs efter avsedd pixeldeadline.

**A – huvudsaklig lösning:** gör en tabell för R1, R2, R3 och R4 PER KRITISK RASTERLINJE: X/Y/objekt-ID, exakt kopieordning, P0/P1/GRP/COLUP/NUSIZ/RESP, M0/M1/BL/PF, avsedd färg vid respektive colorclock, deadline, registrens livstid, HMOVE/VDEL/copy START. RESERVERA R2-guld-/R3-door-kostnader redan i R1-arkitektur. Schemalägg actor-sortering, statisk lookup och objekt-lista i VBLANK/overscan; mät övre RAM/stack- och per-bank-gräns även för gameplay-reserv. Bevisa **både CPU-totalen och när varje TIA-register har effekt**, inte bara <76c. Pröva åtminstone nära-X [40,44,48,52,56,60], luftig same-Y [16,36,56,76,96,116], skilda Y=[96,97,98,99,100,101], player/NPC-X-sortbyte, aktiv M0 som korsar vit-P0-färgband, R2 key och R3 högerkant.

**B – reserv:** om en enda allmän kärna inte ryms, utvärdera **flera bildzonskernlar eller adaptiv aktörslista per rad**, medan varje faktisk same-Y-rad fortfarande ska kunna hantera maximala fallet. Alternativ A/B får inte vara tio ROM-profiler för utvalda X; det ska fortfarande finnas logiskt fria numeriska RAM-X/Y. De två displaylistströmmarna i modern Three-Stream är ett **RAM-/registertradeoff**, inte extra TIA-kanaler. Använd resultat för statiskt vs rörligt PF och data-cache; markera vilka detaljer som saknas innan implementation.

**C – stopp:** vid en bevisat oåtgärdbar förväntad fysisk konflikt (t.ex. COLUP0 behövs samtidigt gul för M0 och vit för NPC med överlappande X/colorclock) utan en accepterad alternativ ritordning, dokumentera exakt scen och aktuellt bitmappsmässigt no-go. Prioritera inte ny ROM på chans; gå till G5 för användarbeslut ENDAST om nödvändigt. Ingen tyst konvertering av skott till en annan färg eller enbits-NPC.

**Preppade leverabler:** G3_TIA_OBJECT_OWNERSHIP.csv, G3_COLOR_CLOCK_DEADLINES.csv, G3_CYCLE_LEDGER.csv, G3_RIOT_STACK_BANK.md, G3_R1_R4_MAX_STRESS.csv. **PASS/exit:** minst en plausibel kompletterad resurskontraktshypotes OCH en explicit lista av risker som bara verklig Stella kan avgöra. Om ej: NO-GO/INCONCLUSIVE till G4/G5.

## 4. G4 – minsta falsifierbara källplan och GO/NO-GO
**Läge nu:** SOURCE-ONLY beslut; **INTE** ett nytt F12-prov. **Ansvar:** MAIN med RESEARCH II och eventuellt ROM DEVELOPMENT III som läsande teknisk rådgivare.

**Förutsedda risker (G4-R1–R6):** (1) F11 upprepas: kravet på full sex-NPC-bevisning på papper blockerar varje verklig fysikmätning; (2) den föreslagna tekniken är bara en ny modeprofil med två fasta X; (3) 3 colorclocks per CPU-cykel missar avsedda absoluta X med 1–2 CC; (4) TIA START/GRP-effekt härleds från grov modell snarare än faktisk renderCounter och latch; (5) bruttocykler ryms men M0/PF/färg gör det inte; (6) modellerad randfallsscen är inte den svåraste.

**A – huvudsaklig lösning:** undersök MIXAD P0/P1 med äkta numeriska RAM-X och P0-korsning. Beskriv en *minimal* plausibel TIA-händelseordning som skiljer:
  (i) gul P0-spelare till vänster om vit P0-NPC;
  (ii) vit P0-NPC till vänster om gul P0-spelare;
  (iii) samma/små X-gap;
  (iv) aktiv M0 på samma Y under växlande COLUP0;
  (v) två P1-originalmasker och bruna PF samtidigt.
  Definiera ett enda observerbart okänt beteende (t.ex. andra RESP0 under aktivt P0-renderfönster) som en framtida fysik-ROM kan falsifiera. **GO här betyder endast GO till ETT separat auktoriserat litet experiment**, inte GO till sex fulla NPC och inte E02.

**B – reserv:** om dual-kanalens färg-/timingkonflikt blir för snäv: återvärdera NUSIZ/VDEL/HMOVE med EN annan konkret, originalmaskbevarande eventlayout, eventuellt byta val av vilka NPC som tilldelas P0/P1 baserat på aktuell X-sortering. Välj bara om samma kriterier kan beskrivas utan orimlig RAM/ROM-profil-explosion. Ingen odefinierad hypotes med "beror på emulatorn" som förutsätter en godkänd fysikplan.

**C – stopp:** om den minimala P0/P1-korsningen saknar plausibelt 76c-/colorclockfönster eller färgkravet för samtidigt M0 är självmotsägande, redovisa NO_GO_SOURCE_ONLY / INCONCLUSIVE_NEEDS_PRIMITIVE med exakt motexempel och två val. Skicka INTE ett godtyckligt tidsfas-svep till ROM-utveckling.

**Preppade leverabler:** G4_PREREGISTERED_HYPOTHESIS.md, G4_REGISTER_TIMELINE.csv, G4_ONE_EXPERIMENT_GO_NOGO.md. **PASS/exit:** en fysisk variabel och ett kontrolltest är falsifierbara utan efterhandsändrade mål, och MAIN har ett separat risk- och beställningsunderlag. G4 är inte auktorisation för G6.

## 5. G5 – beslut om teknisk väg, nödvändiga avsteg eller stopp
**Läge:** FUTURE DECISION. **Ansvar:** MAIN lägger fram; **användaren** beslutar om varje design-/hårdvarukompromiss.

**Förutsedda risker (G5-R1–R6):** (1) en forskningsteknik uppfattas som definitiv; (2) användaren får otydliga val som "bättre prestanda" utan konkret silhuett-/färgförlust; (3) byte till F6SC/ARM föreslås som magisk lösning men påverkar inte TIA:s antal sprites; (4) man gör om kartor/spawn för att undvika värstafallen utan beslut; (5) "lite flimmer" felaktigt tolkas som godkänt 1/6-visande; (6) man kompromissar bort spelkänslan för att få en grön teknikrapport.

**A – huvudväg:** om G1–G4 ger en plausibel oförändrad F6/NTSC-väg, behåll ALLA låsta spelkrav och överväg separat, mycket snäv G6-fysikorder. Gör ett binärt dokumenterat beslut från MAIN med ordalydelsen "tillstånd till EN särskild diagnostisk ROM, inte en ny spelversion".

**B – reserv:** om bara ett väldefinierat villkor är blockerande, presentera **högst två** för användaren jämförbara design-/hårdvaruförslag med: exakt ändring, vilken originalskiss/mask/acceptans det påverkar, visuell konsekvens, teknisk kvarstående risk och vad som inte löses. Exempel på möjliga men **inte godkända** beslutskategorier: definierad NPC/NPC-occlusion/visuell prioritet; accepterat kortvarigt flimmer i specifik belastning; bevarade sex fria logiska X/Y men viss animation/färgförenkling; annat kassettformat. Ingen sådan kompromiss får införas utan uttryckligt ja till exakt text.

**C – stopp:** om det inte finns ett försvarbart tekniskt spår utan att bryta flera centrala krav, håll diagnosen BLOCKED och presentera att tekniken inte är bevisad inom givna villkor. Bevara projektet och fråga om användaren vill prioritera absolut hårdvarutrogenhet eller en uttryckligen ändrad produktvision. "Nästa tio steg" stannar då här, inte en falsk färdig roadmap.

**Preppade leverabler:** G5_DECISION_BRIEF.md med två jämförbara scenarier, G5_AUTHORIZATION_BOUNDARY.md, beslutsdatum/ordagrant svar. **PASS/exit:** ett entydigt huvudbeslut med oförändrad eller explicit ändrad canon. Ingen implicit user-approval.

## 6. G6 – EN minimal P0/P1-fysik- och korsprövning
**Läge:** **INTE AUKTORISERAD**. Kräver ett eget skriftligt, snävt MAIN-utvecklingsuppdrag inom Issue #6 (bara om G4/G5 tillåter). **Ansvar:** ROM DEVELOPMENT III producerar; MAIN granskar developer-local.

**Förutsedda risker (G6-R1–R9):** (1) fixad gul P0, vit P0 går att rita till höger men inte till vänster; (2) en andra RESP0 gör att föregående 8 pixlar avbryts; (3) GRP0-latch blir en rad sen och vänder små maskrader; (4) färgswitch P0 vit byter M0-skott till vitt; (5) P1 framträdande kopia ghostas; (6) PF-väggskrivning kolliderar med P0/P1-byte; (7) siffer-X har bara hard-coded två lägen; (8) Stella trap visar cykel EFTER write-instruktionen och tolkas som write-start; (9) genererad ROM fyller aktiv 4K-bank eller bryter 262 NTSC-rader.

**A – huvudväg:** en separat förhandsregistrerad standard-F6/NTSC-programversion med exakt originalbitmaps och tydliga RAM-byte för numeriska X/Y. Minsta kritiska fall: gul fullstor spelare + EN vit originalandroid på P0 som i samma ROM byter X-ordning med spelaren + minst TVÅ olika vita originalmasker på P1 + verkligt aktiv M0 i samma relevanta 9-radersband + faktiskt brunt PF. Ändra EN numerisk X-position oberoende av de andra; pröva båda X-sortordningar, och färg M0 = gul vid varje M0-pixel. Tillåt ett enda förregistrerat alternativt kernelmönster om absolut nödvändigt men **inte** 2^N positions-profiler. Kräv G0 källa/cykelplan före ROM, G1 DASM/.lst/.sym/PC/trapWrite/2600-scan/frames, verkliga rå-PNG och per-pixel TOP-DOWN/färg-orakel.

**B – reserv:** om A:s primära P0-crosstiming faller men G4 identifierat en *annan enskild* specifik kopie-/NUSIZ-/HMOVE-mekanism, begär en **NY separat snäv order** för en alternativ enda fysisk hypotes. Återanvänd observerad negativ evidens och oförändrade stresstester. B får inte fortsätta inuti A:s order om stoppregel redan slagit till och får inte skala till sex NPC.

**C – stopp:** vid fel fysisk X, saknad originalpixel, vit M0, felaktig P0-player, >76 CPU, PF-brist, NTSC-linjefel eller saknad råevidens: markera per-fail orsak och STOPP. Förhindra att en konstgjord pixelunion eller en ny förprogrammerad X-tabell marknadsförs som "NUMERIC FREE X". Ingen G7 utan nytt MAIN-beslut och positivt värdefullt mikrofysikresultat.

**Preppade leverabler:** ett framtida G6_WORK_ORDER_DRAFT.md, G6_PRE_REGISTERED_SCENES.csv (båda P0-ordningarna, M0 över vitaktigt band, PF), G6_EXPECTED_PIXELS.md, G6_TIMER_TRACE.csv, G6_SHA256_MANIFEST.txt, TO_MAIN_G6.md. **PASS/exit:** numerisk RAM-X har en verklig ortogonal effekt med P0 crossing, originalmasker, gul spelare och skott, utan förlorade PF-/färgpixlar. Detta är bara en byggsten, INTE R1-PASS och INTE independent E02.

## 7. G7 – full sex-original-NPC R1 med sex numeriskt oberoende X/Y
**Läge:** **INTE AUKTORISERAD**. Kräver PASS G6 och nytt separat MAIN ROM-mandat. **Ansvar:** ROM DEVELOPMENT III, MAIN audit.

**Förutsedda risker (G7-R1–R9):** (1) växande per-scanline events för 6 NPC = över 76 cykler; (2) ROM-explosion när X/Y-kombinationer förkompileras; (3) 128B RAM-livstidskonflikt mellan actor coords och sort-/maskstabeller; (4) samma-Y fungerar men Y-förskjutna maskrader läses fel och ritas uppochned; (5) X-sortändring ger spökbilder/byte av fiende-ID; (6) överlappande 8x9 måste representeras med tydlig policy och korrekt logiska ID; (7) P0 cross M0-färg går sönder när fler vita finns; (8) en "grön" automatisk checker använder inverterat original igen; (9) spriteantalet gör R2 och R3 omöjliga, trots isolerad R1.

**A – huvudväg:** dynamisk per-frame aktörs-/Y-sort med RAM-X/Y som verklig numerisk data och en noggrant beräknad händelsetabell eller begränsat antal allmänna timingklasser. Använd lookup/PF-planering i VBLANK och separata Y-zonkernlar där det faktiskt finns tid; same-Y ska fortfarande fungera. Pre-registrera S1 sex same-Y X=[16,36,56,76,96,116], S2 när-X=[40,44,48,52,56,60], S3 Y=[96,97,98,99,100,101], S4 X-korsningar, S5 player/M0/PF och 6→5 vid key. Kontrollera sex separata RAM-X/Y och enskilda perturbationer där de fem andra är oförändrade, 9 rättvända rader och individuell identitet. Låt orakel skilja COMPOSITE pixelunion och logiskt objektantal.

**B – reserv:** adaptiva rasterklasser baserat på verklig per-rads-objektbelastning, NUSIZ-kopior för tillfälligt kompatibla X-paret, annars P0/P1-retrigger; zonbyte sker när högsta objektaktivitet kräver. Detta är godtagbart endast om det kan hantera alla förregistrerade numeriska X/Y-fall, inte koppla NPC-rörelse till 16/32/64-CC-avstånd och inte offra originalmasker eller otillåtet flimmer. En alternativ kompression av eventsekvens är möjlig, men inte godtyckliga 2^6 hela ROM-formationer.

**C – stopp:** om S2/samma-Y, full 8x9, gul player/M0/PF eller separat numerisk X/Y fallerar, klassificera R1 som BLOCKED/FAIL och dokumentera avvikelsen. Om pixelperfekt two-NPC-overlap innebär odefinierbar synlighet ställ endast den preciserade acceptansfrågan till användaren före nästa teknikförsök. Ingen automatisk reducering av antal eller skriftligt "PASS_WITH_WAIVER" utan uttryckligt godkännande.

**Preppade leverabler:** G7_R1_SCENE_MATRIX.csv, G7_COORD_ORTHOGONALITY.csv, G7_NPC_IDENTITIES_AND_OCCLUSION.md, G7_600_FRAME_INDEX.csv, G7_PIXEL_AUDIT_ORACLE.md, G7_CYCLE_LEDGER.csv, G7_M0_COLOR_CROSSING.csv. **PASS/exit:** uppmätt R1 C01/C03/C04 och B01/B02/B03 i fryst riktig ROM, no after-the-fact position tweaks, 600 sammanhängande 262-scanline frames enligt rätt profil, inga förväxlade GUI-X kontra CC. Developer-local PASS blir EJ independent E02.

## 8. G8 – separat R2/O1-nyckel och R3/right-only dörr, sedan integration
**Läge:** **INTE AUKTORISERAD**. Kräver R1-PASS och separata snäva ROM-ordrar; inte ny fullspelsfunktion.

**Förutsedda risker (G8-R1–R9):** (1) R2 key i guld kräver raster-/färgskrivning som stjäl P0 från spelare/NPC och M0; (2) fem kvarvarande NPC varierar i Y så "fri slot" finns inte varje rad; (3) O1 skymning döljer key längre än avsett eller flyttar logisk X/Y; (4) utvecklare råkar implementera verklig key-carrier/drop/score fast tillstånd är diagnostik; (5) nyckel K09/K11 respektive K09-R-kandidat blandas ihop som slutcanon; (6) R3-PF högra port speglas på vänstersidan; (7) svart keyhole använder P1 som redan bär vita originalmasker; (8) orange dörr kräver färgbyte inom maxad cykelbudget; (9) R3 isolerad 74/76-budget misstas för integrerad PASS.

**A – huvudväg:** R2 diagnostisk nyckel som separat logiskt (X,Y) och en explicit **raster-visibility state**; ingen logisk teleport under O1. Först pröva guld/key när det inte är skymt och när alla fem vita originalmasker + gul player + M0 + PF finns i samma relevanta band; sedan kort/lång skymning och samma plats efteråt. R3: håll den vänstra väggen solid, höger only-port låst/öppen, orange port och svart keyhole som skilda verifieringsmål; rita varken porten eller hålet genom att ta bort en nödvändig NPC-kopia. Verifiera R1/R2-figurer samtidigt vid samma högerdoor-Y. Avläs C02, D01, D02, D03 separat. Ingen full gameplay-nyckel eller animation i v0.18.

**B – reserv:** innan ny kod, om sprite-resurs saknas: analysera annan timing i PF-asymmetri/BL/M1/NUSIZ, eller olika kernels över faktiskt lediga Y-zoner. Detta är bara användbart om **originalets nyckel- och dörrform faktiskt kan återskapas** och M0-skott/white NPC/gul P0 inte störs. BL/M1 är 1-bitarsobjekt och kan inte obemärkt ersätta full detaljerad key/keyhole. Om svart hål är enda fail måste D03 särskiljas från D01/D02 i status och användaren ges konkret alternativ, inte en tyst brun permanent ersättning.

**C – stopp:** vid förlorad key-visibility när inte skymd, förskjuten O1-nyckel, vänster öppning, bortfall av orange/svart, förlorat skott eller >76 c: markera respektive acceptanskriterium FAIL/INCONCLUSIVE och pausa integrationen. En isolerad korrekt högeröppning kan vara en teknisk delvinst men aldrig hel v0.18 PASS.

**Preppade leverabler:** G8_R2_KEY_OCCLUSION.csv, G8_KEY_RESOURCE_SCHEDULE.csv, G8_R3_RIGHT_LEFT_PIXEL_TABLE.csv, G8_BLACK_KEYHOLE_SEPARATE_GATE.md, G8_R1_R3_SAME_Y_STRESS.csv. **PASS/exit:** R2 C02/O1 och R3 D01/D02, med D03 korrekt explicit redovisad; allt i en reproducerbar integration där inga andra C01/C03/B02 regressions uppstår. D03 FAIL får inte döljas.

## 9. G9 – R4 rörelsestress, oberoende VERIFICATION II och PR-val
**Läge:** **INTE AUKTORISERAD**. Kräver föregående grindar och separata uppdrag, Verification helt fristående.

**Förutsedda risker (G9-R1–R9):** (1) 600 snygga stillbilder med fixed formationer misstas för äkta rörelse; (2) oförändrad ROM-hash kan inte reproduceras på ren maskin; (3) CI-logg mäter fel PC eller trap-position; (4) ZIP-arkiv och Actions-evidens försvinner; (5) 262 skärmlinjer uppstår bara i vissa scener, frame varieras; (6) label "independent" men utvecklare kör egen verifiering; (7) Issue #8 har ett annat äldre fryst mål än aktuell kod; (8) PR #7 är gammal draft baseline och ska inte mergas bara för att annan experimentgren passerat; (9) flimmerprocent mäts tekniskt men användarens visuella tolerans är fortfarande ej automatiskt uppfylld.

**A – huvudväg:** ROM DEVELOPMENT III får separat R4-order för deterministiska scripts: same-Y→skiftad-Y, X-sortbyten, player crossing, M0/key/PF/door, sex→fem, varje case rå 600 sammanhängande frames (eller rätt explicit Acceptansprofil), 262 NTSC, register-/cycletrap och färg. Frys käll- och binärhash, DASM/Stella/version, .lst/.sym, test-ID T01–T16, ZIP/manifest i GitHub/Drive. MAIN granskar utviklingens egenkontroll och utfärdar **helt separat** oberoende E02-uppdrag till VERIFICATION II för **exakt commit och SHA**, utan att VERIFICATION ändrar koden.

**B – reserv:** om verifieraren finner en skillnad från ROM DEVs bilder, gör en reproducerbar discrepancyrad med råbild/framestart/reg/traps och fryspunkter; en felaktig timerfälla eller debugbersionsskillnad får utredas **avskilt** från källbeteendet. Ny programmering/remediering sker endast med separat ROM-uppdrag och nytt fryst kandidatpaket; Verification II ska aldrig själv reparera eller omdöpa resultat till PASS.

**C – stopp:** vid SHA-mismatch, mask-/färg-/flimmer-/262-/76-/O1-/D01-/D02-fail eller INCONCLUSIVE bevis: INTE E02-PASS, INTE PR-merge, INTE G10. Frys motexempel och besluta om riktad rework eller ändrad design via användaren. Om full teknisk PASS: PR-beslut görs separat från E02 och beaktar att PR #7 kan ha föråldrad och blockerad baseline. Ingen implicit automerge.

**Preppade leverabler:** G9_E02_RECEIVER_BRIEF.md, G9_INDEPENDENT_TEST_MATRIX_T01_T16.csv, G9_SHA_CHAIN.md, G9_NEGATIVE_TESTS.md, G9_PR_DECISION.md. **PASS/exit:** oberoende byggt exakt binärt matchande resultat och separat signerat utlåtande; inte enbart källanalys eller developer-local bilder.

## 10. G10 – första riktiga spelbara vertikala slice, ny användarauktorisation
**Läge:** FRAMTIDA. **Issue #6 omfattar uttryckligen INTE full gameplayutveckling**. Kräver R1–R4 teknikgrind och nytt uttryckligt användarmandat. **Ansvar:** MAIN beslutar scope; ROM DEVELOPMENT III implementerar beordrat; GRAPHICS II bereder endast godkänd grafik; VERIFICATION II fristående.

**Förutsedda risker (G10-R1–R10):** (1) E02-teknisk PASS feltolkas som färdigt spel; (2) dynamiska R1-figurer och AI delar RAM och VBLANK-tid som inte budgeterats; (3) 8-riktningsskott och joystick ett skott per knappnedtryckning ger edge-triggerfel; (4) första skottet måste starta omedelbar jakt, inte när fiende senare ser skottet; (5) kollision/logiskt objekt-ID sammanblandas med multiplexad TIA latch; (6) key carrier/slump/dödsanimation/O1/K1 ger dubbel eller för tidig nyckel; (7) poäng −25/+50/+100/+15, min 0, extraliv vid 500/1500/2500... kan upprepas vid poängoscillation; (8) högerutgång och kollision samma tick ger fel prioritet E1; (9) GAME OVER kan råka återstartas av FIRE i stället för konsol-RESET; (10) v0.19 kandidatrum och grafiska V03_B/K09-R/G2/H1 kan blandas in utan slutgodkännande.

**A – huvudväg:** med NYTT användarbeslut föreslås först en **liten spelbar vertikal slice inom EN godkänd rättvänd scen och EN godkänd karta** med P0-spelarrörelse och 8 riktningar, exakt ett M0-skott per nytt tryck, sex logiska NPC och synlig originalraster, en key-carrier som släpper nyckel EFTER dödsanimation, låst/öppen högra dörren, poäng/liv och GAME OVER som endast startas om via RESET. Behåll första skottet som exakt trigger för chase. Alla regler görs till deterministiska tick-testfall med resultat som kan inspekteras separat från visuella rasterbevis. Detta är bara ett **framtida förslag**, inte nuvarande order.

**B – reserv:** dela senare gameplay i **flera särskilt auktoriserade tekniskt frysta delsteg** med en per-funktion gate (input/skott → AI/kollision → nyckel/dörr → score/lives → HUD/sound → room rotation) men **utan** att skapa separata synligt oförenliga ROM-funktioner som aldrig kan kombineras. Kör automatisk regression av R1–R4/TIA/canon efter varje integration. Planera AI, kolllisioner och renderobjekt som oberoende logiska system, så att optimeringar kan ske under VBLANK/overscan och inga grafiska maskbyten uppstår.

**C – stopp:** om fullspel med canon inte ryms i 128B RAM/76c per synlig rad/16KB standard-F6 eller blir ospelbart, håll renderings-/diagnostikleveransen fryst och ge användaren högst två exakta val för nytt mandate. Ingen fullspelspromotering, PAL, ljud, release, nytt mapperformat eller ändrad fiendekvantitet utan separat beslut. Ett projekt kan vara arkiverat med tydlig blockerare utan att falskt kallas klart.

**Preppade leverabler:** FUTURE_GAMEPLAY_AUTHORIZATION_DRAFT.md, GAME_STATE_MACHINE.md, SCORE_EVENT_TABLE.csv, INPUT_FIRE_EDGE_MATRIX.csv, K1_E1_COLLISION_PRIORITY.csv, KEY_ANIMATION_O1_TESTS.csv, RESET_GAMEOVER_TESTS.md, ROOM_CANDIDATE_DECISION.md, REGRESSION_GATE.md. **PASS/exit:** det första framtida spelbara, användarauktoriserade vertikala delmålet har både korrekta spelregler och oförstört R1–R4-raster. PAL/fysisk release/manuallayout/marknadsföring fortfarande separat efterföljande projektsteg.

## 11. Färdig scenario- och felmatris som MÅSTE ingå i framtida order

| Scenario-ID | Pre-registrerat indata | Vad kan fallera? | Mätbart resultat | Tidigaste grind |
|---|---|---|---|---|
| SC01 | R1 sex same-Y, X CC [16,36,56,76,96,116], M,M,F,F,SM,SF | NUSIZ upprepade identiska kopior eller kopie-START-miss | Exakt 9 rättvända rasterrader, sex numeriska X, brun PF, gul P0, aktiv M0 | G3 budget/G7 ROM |
| SC02 | R1 sex täta X [40,44,48,52,56,60], Y=96 | En TIA player kan inte hålla två skilda överlappande bitmappsfönster samtidigt; odefinierad occlusion | Separata logiska ID och korrekt composite och synlighetspolicy; ej maskbortfall | G1 policy/G3/G7 |
| SC03 | Sex med Y=[96,97,98,99,100,101] | M/F 9-radersbyte, småmaskens tomrader, fel orientering | Per-NPC rad 0..8 match TOP-DOWN, alla same-scanline events korrekt | G3/G7 |
| SC04 | Två NPC X [60,64]→[66,58] under ändrad ordning | Sort-id byts, regressionsspökbild | NPC-identiteter och alla andra X/Y består, inga extra pixlar | G4/G7/G9 |
| SC05 | Gul P0-spelare byter sida om en vit P0-NPC, samtidigt P1 M/F | P0 gul/vit COLUP0/GRP0/RESP0 konflikt | Gul player, vit NPC, korrekt X båda ordningarna | G4/G6 |
| SC06 | Aktivt M0-skott på SAMMA pixelrader som P0 vit NPC; M0 X före/under/efter COLUP0-switch | M0 blir vitt eller försvinner | Faktiskt M0 gult med rätt X och längd i varje relevant frame | G3/G6/G7 |
| SC07 | Bruna PF-väggar både vänster/höger plus samtidigt P0/P1/M0 | PF half writes passerar pixeldeadlines | Left/right brunt enligt aktuell auktoriserad kart-/diagnosmodell | G3/G6/G7 |
| SC08 | R2 fem NPC + key guld + player + shot same-Y, uncovered | Gold används via fel P0/P1-fönster eller offscreen | Key synlig enligt korrekt nyckelmask/färg; fem NPC och shot intakta | G3/G8 |
| SC09 | R2 key (X,Y) under NPC kort, långt, sedan uncovered | O1 flyttar key eller den återkommer aldrig | Exakt samma logiska X/Y före/under/efter, visuell occlusion förklarad | G8/G9 |
| SC10 | R3 högerdörr locked→open, vänster closed | Speglad PF öppnar vänster, keyhole uteblir | D01/D02/D03 var för sig; orange/svart test med intakta NPC | G3/G8 |
| SC11 | Styrd runtime enskild NPC X+3 CC, övriga fem fasta | Hårdkodat modebyte i stället för NUMERIC RAM-X | Allmän RAM-X påverkar exakt en fysisk originalmask, andra fem oförändrade | G4/G6/G7 |
| SC12 | 600 konsekutiva NTSC frames med rörelse, crossings, R1→R2→R3 | 262-skanningsfel, stack/rombank, frame-affekt | Varje frame skärmlinjer, per-case pixelhash/trap och manifest | G7/G9 |
| SC13 | Nyckelbärare dör → animation → key spawn | Key syns innan animation eller dubbelspawn | En key, exakt efter animation, oförändrad O1 och K1 | G10, ej v0.18 |
| SC14 | Första avfyrade skott, håll FIRE, release/ny press | Chase startar för sent; multi-bullet från håll | Chase omedelbart efter första skott, högst en bullet per press | G10 |
| SC15 | Poänggräns och nyckel/exit samma tick | Negativ poäng/duplicerad bonus/extraliv | 0-golv, en gång per 500/1500/2500..., E1-prioritet | G10 |
| SC16 | GAME OVER: FIRE vs konsol RESET | FIRE återstartar felaktigt | Endast RESET börjar nytt spel | G10 |

**Scenarioenheter:** X-värden i SC01–SC04 och SC11 är TIA-colorclocks i förregistrerat abstrakt prov; Stella GUI kan rapportera 2 skärmpixlar per TIA-clock och offset som måste mätas, inte antas. Y-värden är logiska käll-/diagnosrasterrader; karta 40×22 är en annan upplösningsmodell och ska inte förväxlas. SC02 med verklig bildöverlappning är blockerad på policy om separata visuellt läsbara individuella silhuetter begärs på exakt samma pixel.

## 12. Tidiga beslutsträd och kommunikationsregler

### 12.1 Om G1–G4 fallerar
- **Felaktig/inaktuell källhänvisning:** sök rätt Google Drive original/frozen commit och markera korrigering, inte spriteexperiment.
- **Saknat råarkiv:** säkra källhash och dokumentera reproduktionslucka; inga efterhandsfantiserade 600 ramar.
- **Ofullständig P0/P1-fasplan men plausibel unik TIA-fråga:** G4 kan rekommendera en enda framtida miniprovorder **efter** separat beslut, utan krav på komplett sex-NPC-pappersbevis.
- **Bevisad COLUP0/M0 eller RESP/GRP/START-konflikt utan tillåtet schema:** NO_GO för just familjen; välj högst ett alternativ eller gör G5-beslut. Ingen oändlig serie.
- **Det enda problemet är 4K aktiv ROM-bank:** gör separat källa-/banklayoutstudie inom standard-F6 och data-dekomposition; F6 bankbyte skapar inte mer CPU/TIA och måste ske i tillåtet fönster.
- **Det enda problemet är RIOT-RAM:** visa mätt RAM-/stackbudget och livstidsdelning innan ens övervägande av superchip. F6SC skulle kräva separat uttryckligt formatbeslut och är ingen spritesolution.

### 12.2 Om ett framtida ROM-test fallerar
1. Klassificera först **logikdatafel**, **maskbyte/orientering**, **colorclock/START/GRP**, **P0/M0 färg**, **PF-deadline**, **ROM-bank/stack**, **bristande evidens** eller **exakt occlusionpolicy**.
2. Behåll råa originalfiler och SHA; ändra INTE testets X/Y efter granskning.
3. Ingen teknisk kapacitetsökning från separata F9/F11/R1g-beståndsdelar får deklareras utan samma körbara integrerade ROM.
4. Endast ett välmotiverat minimalt alternativ kan prövas med separat order. Flera misslyckade fassvep betyder ingen automatisk rätt att testa allt.
5. Användaren får bara en verklig fråga om ett objektivt designbeslut behövs; annars handlägg MAIN intern read-only riskanalys.

### 12.3 Leveransstruktur för alla framtida grindar
- **Cover:** Scope-ID, roll, auktorisation/url, aktuellt MAIN-beslut, korrekt testversion, freeze-commit.
- **Evidence:** fryst src+build+ROM SHA, exakt scenuppsättning inklusive X/Y/objekttyper, originalmaskhash, 262-scanline-/76-cykelbevis, PC/scan/_sCycles/RESP/GRP/COLUPx/M0/PF, original-PNG/video med frame-ID, hashat manifest.
- **Risk:** vad uppmättes, vad är bara modell/hypotes, vad avviker från canon/acceptans, vilka redan negativa test har INTE upprepats.
- **Decision:** PASS/FAIL/INCONCLUSIVE/NOT_RUN per test-ID, explicit STOPP och eventuellt förslag på EN nästa beställning, aldrig "MAIN approved" av utvecklaren.
- **Source integrity:** endast detta Atari 2600-projekt, inga tredjepartsspelbinärer/disassemblies, The Cabin/Skraun/ILAF orörda, readback på GitHub och projekt-Drive. En separat, oberoende VERIFICATION får inte använda developer-local check som egen slutsats.

## 13. Nyttiga resurser och primärkällor (länkar med provenance)
1. Den nuvarande högre nivån: [CURRENT_PROJECT_STATE](CURRENT_PROJECT_STATE_2026-11-15.md), [MAIN VI deep reassessment](MAIN_VI_DEEP_REASSESSMENT_30_TRICKS_FEASIBILITY_AND_TEN_GATES_2026-11-17.md).
2. Canon och tekniska villkor: [MAIN_DECISION_LEDGER_SUPPLEMENT](MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md), [ROM_GATE_V018_SCOPE](ROM_GATE_V018_SCOPE.md), [ROM_GATE_V018_ACCEPTANCE](ROM_GATE_V018_ACCEPTANCE.md), [ROM_GATE_V018_BLOCKERS](ROM_GATE_V018_BLOCKERS.md), [T01–T16 matris](../planning/ROM_GATE_V018_TEST_MATRIX.csv), [låsta original-8x9-masker](../design/NPC_REFERENCE_8x9_masks.json).
3. Fryst utveckling: [F9](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md), [F10](https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md), [F11](https://github.com/Odourman/let-me-out/blob/dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F11.md).
4. Forskningsoriginal: [R1e](https://github.com/Odourman/let-me-out/blob/research/main-ii-r1e-four-originals-p0wide-calibrated-20261116/docs/MAIN_II_R1E_FOUR_DISTINCT_ORIGINALS_STATIC_LOCAL_PASS_2026-11-16.md), [R1f](https://github.com/Odourman/let-me-out/blob/research/main-ii-r1f-resp0-independent-fourth-20261116/docs/MAIN_II_R1F_RESP0_BREAKS_FIXED_P0_COPY_X_STELLA_LOCAL_PASS_2026-11-16.md), [R1g](https://github.com/Odourman/let-me-out/blob/research/main-ii-r1g-four-X-dynamic-600-20261116/docs/MAIN_II_R1G_FOUR_X_DYNAMIC_600_STELLA_LOCAL_PASS_2026-11-16.md), [R1g faktiskt build_dynamic.py](https://github.com/Odourman/let-me-out/blob/research/main-ii-r1g-four-X-dynamic-600-20261116/rom/v018/experiments/main_ii_r1g_dynamic/build_dynamic.py).
5. Alla 30 numrerade trick: [30 original tricks](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md) och [historisk forskningsrapport](research/ATARI_30_ORIGINAL_TRICKS_HISTORICAL_2026-11-16.md). 52 teknikmönster + 67 risker + 30 original: https://drive.google.com/file/d/1IHKg63PZGAYoi3fdJdwmOYsomDxumlIv/view; historiskt research ZIP https://drive.google.com/file/d/1JgLBpjUIVRQegVUFVNn3DoZpxguDqSs4/view.
6. Primär Atari-hårdvaru- och emulatorinfo: Atari Stella Programmer’s Guide https://www.atariage.com/2600/programming/2600_101/docs/stella.html (explicit COLUP0=P0+M0, COLUP1=P1+M1, COLUPF=PF+BL); Stella 6.7.1 Player.cxx https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/tia/Player.cxx ; DrawCounterDecodes.cxx https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx ; F6 bank https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/CartF6.cxx ; Andrew Towers TIA Hardware Notes https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php ; Stella Debugger https://stella-emu.github.io/docs/debugger.html (online-handboken kan avse senare 7.0, så 6.7.1-syntax kontrollera mot riktiga försök); 8bitworkshop Three-Stream https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html (3 registerskrivningar/line, 32B/list i det specifika exemplet, inte sex free-X); 8bitworkshop Versatile PF https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html.
7. Exakt scope/ägarskap: https://github.com/Odourman/let-me-out/issues/6; PR #7 https://github.com/Odourman/let-me-out/pull/7; äldre E02 Issue #8 https://github.com/Odourman/let-me-out/issues/8; projektets Drive-mapp https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u; det ursprungliga 57-beslutsarkivet https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view.

## 14. Arkiverings- och ansvarskvitto
Denna beredskapsplan gäller **planering** och inte kod. Läs den tillsammans med aktuell MAIN-status, jämför verkliga HEAD/Issues efter datum och märk avvikelser innan ny aktivitet. Den rekommenderade ordningen G1–G10 är fortfarande **villkorad**: G1–G4 måste ge vägval, G5 kan stoppa projektet och G6–G10 får inte startas utan särskilt uttryckligt mandate. Vid ny teknisk upptäckt ändras denna plan som daterat nytt tillägg, inte genom att tyst omskriva historiska F9/F11-rapporter eller användarens canon.
