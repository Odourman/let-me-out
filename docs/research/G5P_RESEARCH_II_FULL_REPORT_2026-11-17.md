# LET ME OUT! – G5P: RESEARCH II, fördjupad rådgivande analys

**Datum:** 2026-11-17  
**Klass:** `G5P_SOURCE_ONLY_OFFLINE_RESEARCH_COMPLETED_ADVISORY`  
**Mottagare:** MAIN VII / GitHub Issue #9  
**Scope:** fem fiender M,M,F,SM,SF, A01/B01/C02/D01 och separat v0.19-test. **INGEN ROM, ingen G0/G6/F12, ingen canon- eller kartsupersession, ingen oberoende Verification.**

## 1. Slutsats och styrande rekommendation

**Fem individuellt rörliga fiender är rimliga som spelmål men ingen komplett standard-F6-renderer är visad.** I en rättvis offlinejämförelse förbättrar adaptiv eller globalt omplanerad strikt Y-separation NPC-jakt något, men ger fortfarande långvarig fastlåsning. Mjuk/fri Y-jakt förbättrar hotbilden mer, men hårda samtidighetskrav ger mycket stora konflikter för en enkel en-vit-NPC-per-rasterband-ägarmodell. **Rekommenderad fortsatt forskningsriktning:** behåll fri *logisk* X/Y som spelkvalitetsmålet och undersök en **begränsad hybrid med situationsberoende konflikt-/synlighetsplanering**, *utan att införliva eller godkänna* osynlighetsregler. Först krävs både en användarvald kvalitetsgräns och ett verkligt G0-förprov. Alternativt kan en explicit ändrad spelvision med Y-restriktion diskuteras, men den strikta varianten bör **inte** antas fungera bra bara för att dess rasterresurser är lättare att tilldela.

Varken mjuk Y, fri rörelse eller adaptiva lanes har ett fullständigt korrekt, käll-/Stella-bevisat TIA-schema för nyckel+fiende+dörr+spelare+skott i samma band. Forskningsresultatet är en **NO-GO för att nu välja en produktionskernel**, inte ett universellt omöjlighetsbevis om fem fiender på Atari 2600.

## 2. Verifierade original och källauktoritet

Kontrollerat direkt från GitHub under uppdraget, inklusive G5P-order (blob `eb1cfa3b4b70b6865867eca971ac119d4915dd09`), [G5O](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5O_MAIN_VII_STRICT_S1_Y_LANE_DYNAMIC_CHASE_NEGATIVE_SCREEN_2026-11-17.md), [G5O:s tolv CSV-fall](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5O_HARD_LANE_GREEDY_CHASE_12_CASES_SOURCE_ONLY_2026-11-17.csv), [G5N](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5N_MAIN_VII_S1_FIVE_NPC_LANE_START_AUDIT_AND_SCORE_PROPOSAL_2026-11-17.md), [G5K](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md), [G5L/S05](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_SAME_Y_KEY_DOOR_ENEMY_RENDERING_STRESS_2026-11-17.csv), [G5M](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5M_FIVE_NPC_GAMEPLAY_SCORE_KEY_CARRIER_AND_SPAWN_DEPENDENCIES_SOURCE_ONLY_2026-11-17.md), [G5-beslutsspärr](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md) och [MAIN-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md). Läsning gjordes innan rapportskrivningen; ett senare HEAD måste alltid kontrolleras före nya beslut.

Originalkartor i kodblobs:
- [v0.11 A01/B01/C02/D01](https://github.com/Odourman/let-me-out/blob/main/design/PLANERADE_RUMSKARTOR_V011.json) – blob `820a74e5fb77c818ffb1286c5b23698d4374e771`.
- [v0.19 exakta öppna kandidater](https://github.com/Odourman/let-me-out/blob/main/design/OPEN_ROOMS_V019_40x22_CANDIDATES.json) – blob `0e449f97f87bd9b403476fd1435398042eaee285`, **ej kartcanon**.
- [8×9-maskoriginal](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json) – blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`.

Från officiell [Drive-mapp](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u) hämtades **ursprungliga 21-filsarkivet med Master Spec och 57 beslut**, SHA-256 `f291d07af34e12866cd9785387e8ba1d320aa341b70e9646c28e3e0a78896ff4`, ZIP CRC PASS. Originalets `03_DECISIONS.csv` lästes direkt: relevanta 008,019–025,032–034,042–047,051/052 och 057. Senare uttryckt mål om fem M,M,F,SM,SF åsidosätter sex som önskad *framtida* inriktning, men **inte** historisk R1=6/R2=5+key-acceptans eller redan frysta resultat. O1 har redan giltig begränsad tillåtelse för faktisk android/key-pixelöverlappning; inga senare forskningsformuleringar ändrar det.

Extern teknikgranskning: [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) (register och färgdelning), [Stella Debugger](https://stella-emu.github.io/docs/debugger.html) (framtida mätmetod), [historisk Berzerk-assembler, fast commit](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm) och projektets redan granskade [G5J](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md). AtariAge [multisprite-diskussion](https://forums.atariage.com/topic/347667-multi-sprite-kernel-strategies-or-examples/) och [flicker-erfarenheter](https://forums.atariage.com/topic/347643-flickering-sprites-is-there-more-than-one-way-to-do-this/) ger konstruktionsvarningar, inte mätbevis för vårt spel. Ingen källkod har kopierats från dessa externa spel.

## 3. Modell, reproducerbarhet och begränsningar

**Körning:** `python3 g5p_offline.py` följt av `python3 g5p_global_control.py` (endast Python-standardbibliotek). Programmet kan köras i ren katalog utan GitHub/Drive under körning. **Mapdata har kodats förlustfritt som 40-bitars hexrader direkt ur de två ursprungliga 40×22-JSON-filerna**, med deras kandidatlistor och dokumenterade spawnankare; de kompletta officiella originalkartorna ändras inte. `#` är vägg, `.` fri, `D` låst högerdörr (räknas som stängd). Fotankare är 2×2 *gridceller*, fyra grannar och BFS. Ett rutsteg i Y motsvarar i preview-modellen åtta scanlines; 9-originalradsband överlappar därför vid `|delta-y|<2` ankarrader. Alla NPC:er har samma 2×2-kollisionsbegränsning i **alla de nya jämförelsekörningarna**. Ingen NPC får dela eller delvis överlappa en annan NPC:s 2×2-fot, inte heller i fri referensmodell. Spelar-NPC-överlapp är däremot en *förenklad kontaktexponering*, inte verklig spelarhitbox/dödslogik.

Fyra v0.11 och fyra separata v0.19-kartor, tre deterministiska femstartsgrupper per karta (G5N:s originalstarter för v0.11 som grupp 0 samt två extragrupper valda ur karta-/kandidatfiltret), sju spelarskript `static_left`, `static_middle`, `static_right`, `horizontal`, `vertical`, `escape_door`, `walls`; **180 ticks**; **fyra huvudmodeller**, totalt **8×3×7×4 = 672 körningar** och 120 960 modell-ticks, slumpfrö `20261117`. `horizontal/vertical/escape_door/walls` är BFS-vägpunktsskript som rör spelaren med ett ankarrutsteg per två NPC-ticks, inte en responsiv människa. Alla nya NPC-modeller uppdateras i roterande ordning `(j+tick)%5`; varje NPC högst ett fyrgrannesteg/tick.

- **Strikt girig:** per-NPC-steg måste minska *obehindrat* statiskt BFS-avstånd till aktuell spelare, uppfyller alltid `|delta-y|>=2`, och NPC-2×2-kollision.
- **Strikt adaptiv:** 9 stegs statisk grannlookahead med NPC-2×2 och strikt Y; första steg på bästa nåbara delväg får temporärt öka avståndet. Kan inte låta NPC:er byta vertikal inbördes ordning.
- **Mjuk Y:** fri numerisk grid-Y under NPC/NPC-kollision. En **konservativ, syntetisk** displayägarmodell väljer med roterande prioritet högst EN vit 8×9-NPC inom överlappande Y-band och räknar hela andra band som bortfall. Det är **inte** uppmätt bildflimmer i Hz eller källbevis att P0/P1 inte kan avlasta.
- **Fri X/Y:** identisk kollisionsriktig jakt som mjuk Y, men ingen renderingswaiver/visibility-tilldelning påstås. Räknar behov av överlappande Y-band och hardware-NOT-PROVEN.

**Separat känslighetskontroll:** `g5p_global_control.py` ersätter 9-stegsfönstret med komplett BFS i den tillfälligt blockerade, strikt Y-separerade NPC-grafen. 8×3×7 = **168 ytterligare körningar**; därmed **840 nya rättvisa scenarier** totalt. Detta är fortfarande *inte* en samordnad, global AI med omflyttning av alla fem som grupp; statiska andra-NPC-hinder under individens planering orsakar bland annat lokala dödlägen. Exakta råsekvenser och samtliga 840 utfall finns som CSV.

Mått: `unique_threats` är antalet *unika* NPC med BFS-distans **högst 2** till spelarmålet någon gång under 180 ticks; `first_threat_tick` första sådana tidpunkt; `stalled_npcs_30` NPC som i något sammanhängande 30-ticks-intervall inte flyttade trots kvarvarande distans **mer än 3** vid aktuell position; `movement_rate` faktiskt godkända steg / fem update-försök per tick; `y_overlap_frames` rasterbandskonflikt i modellen, `soft_hidden_npc_ticks` sammanlagda NPC×tick-bortfall i konservativ syntetisk kö; `key_to_door` BFS-potential efter ett syntetiskt key-drop vid tick90 och *inte* faktiskt genomspelad dödsanimation. Statistik från 84 fall per kartgeneration/strategi, inga sannolikhetsbaserade populationspåståenden.

## 4. Reproduktion och omtolkning av G5O

Samtliga 12 historiska fall reproducerades: **samma slutpositioner, fem slutavstånd, lane_moved, blocked/total gradient requests och `near<=1`** som originalets CSV; `g5o_replay.csv` innehåller originalets kolumnlayout. Exempel historiska B01 med stilla spelare (2,10): lane=0/5, `moved=15`, `blocked=885/900`, slut `8:6|13:8|30:12|8:14|35:16`. Sammanlagt i originalmodellen **8 513 blockerade av 9 126 upprepade avståndsminskande förfrågningar**; detta är ett *tickmått*, inte 8 513 oberoende NPC-möten.

**G5O:s gamla 5/5-fri-referens var ogiltig som spelkollisionsbaseline**, eftersom fem NPC kunde stå i samma fotankare. Och när `|delta-y|>=2` tillåts är högst två nära ett fixerat mål inom abstrakta BFS-avstånd <=1 geometriskt möjliga (i praktiken ofta en). Därför är G5O:s 1/5 ingen självständig bevisning för dålig upplevelse. Den verkliga negativa signalen är upprepade AI-stopp och utebliven förföljelse, som nu prövats med rättvis NPC/NPC-kollision och rörliga mål. Original-G5O och dess raw-CSV har **inte ändrats**.

## 5. Resultat – 672 huvudkörningar

| Kartset/84 fall per mode | Mode | Unika hot-NPC (0–5) | Första hot-tick, givet hot | Move-andel | Fall med 30-ticks-stall | Y-konfliktrutor (medel/180) | Syntetiska osynliga NPC×ticks /900 |
|---|---|---:|---:|---:|---:|---:|---:|
| **v0.11** | strikt girig | 2,869 | 9,85 | 11,8% | **84/84** | **0** | 0 |
| v0.11 | strikt adaptiv | 3,155 | 10,06 | 17,0% | **84/84** | **0** | 0 |
| v0.11 | mjuk | **4,048** | 8,21 | 21,2% | 67/84 | **170,3** | **498,6** |
| v0.11 | fri | **4,048** | 8,21 | 21,2% | 67/84 | **170,3** | Ej renderad |
| **v0.19 kandidater** | strikt girig | 3,060 | 8,85 | 13,9% | **84/84** | 0 | 0 |
| v0.19 kandidater | strikt adaptiv | 3,119 | 8,89 | 17,6% | **84/84** | 0 | 0 |
| v0.19 kandidater | mjuk | **3,881** | 7,45 | 21,3% | 71/84 | **178,2** | **597,4** |
| v0.19 kandidater | fri | **3,881** | 7,45 | 21,3% | 71/84 | **178,2** | Ej renderad |

Mjuk-modellens 498,6/900 respektive 597,4/900 NPC×ticks motsvarar **55,4% / 66,4% syntetisk bortprioritering** under den antagna en-vit-NPC-displaymodellen, *inte* faktisk TIA-flicker eller en garanterad fysisk förlustandel; ändrad kanalägarmodell kan reducera konflikter i vissa Y-bilder. Den extrema frekvensen är dock tydlig varningssignal: att kalla modellen "lite tillfälligt flimmer" utan empiriskt accepterade exempel vore fel.

**Global-sök kontroll:** v0.11 `unique_threats=3,321`, move-rate `18,8%`, stall **84/84**; v0.19 `3,226`, `19,5%`, stall **84/84**. Globalt individ-BFS undviker ett antal niostegslokala fällor men **löser inte** det sociala vertikala låset. I den förregistrerade B01, spawn0, spelare (2,10), förbättrar adaptiv 9-steg från 0 till 2 unika hot jämfört med strikt girig, men mjuk ger 3; enskilda andra B01-startuppsättningar ger fortfarande 0 vid strikta policyer. Alla numeriska mått gäller här exakt de publicerade offlinealgoritmerna, inga statistiska generaliseringar.

### 5.1 Om start, karta och spelare

Tre initiala femstartsuppsättningar användes per karta; de två extra kommer från explicita kandidatlistor och är reproducerbara via seed. Den här selectionen täcker **inte alla** möjligheter eller variationer. B01 har trånga noder och lägre spelbarhet i flera exempel; i B01 spawn0+static_left ger strikt girig 0 av fem hotande under alla 180 tick, adaptiv 2 och mjuk 3. I B_OPEN_01 spawn0+static_left ger både strikta modeller endast 1, mjuk 2; de luftigare kartorna är alltså inte en universell AI-lösning. Flera `walls`-banor gör omvägar; `escape_door` utgår från BFS-väg till nära högerdörren, men **ingen faktisk låsning/utgång eller dödshantering utförs**.

### 5.2 Konkret spelarutnyttjande och avspärrning

Y-separering håller NPC-ordningen fixerad och skapar utrymmen mellan grupper där spelaren kan stå utan att samtliga fem samtidigt kan komma nära. Det kan vara avsedd taktik i ett annat spel, men inte en bevisad godkänd effekt här. `stalled_npcs_30` signalerar långvarigt stillastående i alla 84/84 strikta fall, även efter förbättrad planering; spelaren kan i modellen röra sig horisontellt mellan Y-låsta grupper och ibland nå höger utan att alla NPC kan följa. Att ange "passade utgången" vore fel: det finns ännu ingen faktiskt spelad nyckel/door/AI-regel, bara BFS-vägpotential. Snapshot med andra NPC som 2×2-blockerare hindrade en hypotetisk spelarväg till nyckel/utgång i vissa fall trots tom kart-BFS. Det bekräftar att framtida gameplay kräver **dynamisk dörrblockering/kollisionstest**, inte bara kartans öppna geometri.

## 6. Nyckeln och dörren – separat S05 med riktig bitmasköverlappning i OFFLINE-modellen

Två förregistrerade syntetiska scener (se `s05_logical_stress.csv`), med stor M-originalmask 8×9 och **preliminära K09-R-nyckelkandidatmasken** (inte beslutad slutmask). Samma nio rasterrader, gul spelare i samma Y, bruna PF-väggar, aktivt möjligt M0-skott, P1 reserverad för orange högerdörr med svart *transparent hål i dörrens egen bitmap*:

| Fall | Vit M X_CC | Key X_CC | Faktisk bitpixelöverlappning | Redan godkänd O1 tillåter att NPC skymmer key? |
|---|---:|---:|---:|---|
| S05-A | 60 | 60 | **13 källmaskpixlar** | **Ja**, endast där pixlar överlappar, temporärt |
| S05-B | 60 | 74 | **0** | **Nej**, key skall visas trots samma raster-Y |

Båda fallen kräver i enkel G5K-modell **P0=player + white NPC + gold key** medan **P1=door**; aktivt M0 delar P0:s färg `COLUP0`, och PF/BL delar `COLUPF`. Det saknas fungerande timing/GRP/RESP/START/cycle-plan för tre separata färgade P0-händelser inom den relevanta pixelraden. A:s faktiska överlappning kan ibland utnyttja O1 men *inte* för att dölja hela key när endast delar sammanfaller, och hjälper inte B. Att flytta key eller låta den försvinna enbart av samma-Y vore förbjuden regeländring. **O1-logisk koordinat, upplockning och K1:s fördröjda pickup förblir oförändrade**.

I huvudsimulationen har key hypotetiskt släppts efter dödsanimation vid positionen för var och en av de fem möjliga bärarna vid tick90, med val **1/5 per bärare som kontrafaktisk lista, inte ny godkänd PRNG**. Alla fem droppunkter hade väg via tom karta till dörren; med övriga fyra NPC tillfälligt stationära vid snapshot fanns i v0.11 medelvärde **4,14–4,58 /5** möjliga key-till-dörr-vägar beroende på policy, för v0.19 **4,68–4,96 /5**. Detta är *ögonblicklig pathfindingpotential*, inte en genomspelad session, garanti mot permanent NPC-blockering eller konfirmerad faktisk nyckelsprite. Dörr- och nyckelhålens rasterpass och korrekt COLUBK-svart är fortfarande fysisk G0-fråga.

## 7. TIA-/6507-arkitektur – exakt vad varje teknik kan och inte kan göra

**Fysik:** 76 CPU-cykler = 228 CC/NTSC-rad, varav 160 synliga CC; 128 byte RIOT RAM med stack. Standard-F6 har 16 KiB ROM fördelat på fyra banker, men bara en 4 KiB-bank aktiv i ett ögonblick. `P0/M0` delar `COLUP0`; `P1/M1` delar `COLUP1`; `PF/BL` delar `COLUPF`. Två spelarsprites med åtta bitar var; M0/M1/Ball är smalare objekt och kan inte utan förlust ersätta samtliga fyra 8×9-NPC-bitmappar. Den orange R3-dörren har separat *developer-local* historisk ROM, inte full integrerad R1/R2/R3.

| Metod | Löser exakt | Löser inte / visuell kostnad | Ställning |
|---|---|---|---|
| Y-sprite-multiplexning | P1 kan återanvändas på andra 9-radersband | Låser eller omplanerar logiskt Y, npc får inte passera varandra fritt, dörr/key och P0-färg kvar | Villkorad hårdvarukandidat, AI-risk hög |
| G5K dynamiskt P0/P1-ägarskap | P1 orange låst högerdörr i dörr-Y, P0 kan ta player + en vit NPC | P0 två fria X, gul/vit färg, M0 samtidigt, och S05 tre P0-händelser återstår | Source-only logisk 176-raders resursallokering, inget G0 |
| Mid-scanline GRP/RESP | Flera originalbitmappar på spridda X på en rad | Kräver START-/counter-, GRP-latch- och pixeldeadlines; F11 blockerades, G5H direktfall 79/76 | Ej validerad allmän lösning |
| NUSIZ/VDEL/HMOVE | Kopior, eventuella fördröjda GRP-faser, global X-finjustering | Fixerade NUSIZ-avstånd, ingen femfaldig oberoende X/Y-klocka | Endast bit-tekniker, inte full arkitektur |
| Playfield/asymmetri/Ball | Vägggeometri och svart transparent keyhole kan modelleras i separat lager; BL kan bidra vänstergräns | PF har 4CC-bitar, BL delar PF-färg, register-write vid mittlinje och vägg-/dörrkonflikter | G5G 3520/3520 **offline**, BL fysiskt inte bevisad |
| Venetian Blinds / two-line | Kan dela ett överbelastat rasterband mellan objekt i olika linjer | Av nio ursprungsrader kan bara 5/4 återstå per figur vid 1:1-varannan-rad, alternativt dubbel höjd; äldre negativa prover | Svag reserv; kräver explicit kvalitetspolicy |
| Kontrollerat flimmer | Fyra/fem fiender kan fortsätta röra sig logiskt även när färre visas per frame | Synlighetsandel/detektionsrisk, 10Hz-historiskt negativt, osynligt hot eller key får inte införas | Ej godkänt, huvudrisk enligt vår offlinekö |
| Precompute + olika kernels | Sortera X/Y i VBLANK, välj specialiserat dörr-/HUD-band, minska runtime-kostnader | Banker skapar inte rastertid/objekt; exakta färg- och START-deadlines kvarstår | Nyttigt endast efter en riktig G0-schemahypotes |
| F6SC/DPC/CDF/ARM | Mer RAM/förarbete beroende på hårdvara | Fler TIA-spritekanaler skapas inte automatiskt; ändrad cartridge kräver nytt användarbeslut | Utanför nuvarande standard-F6-scope |

Den publicerade Berzerk-disassemblyn använder nio-raders robotband och vertikalt fördelade robotstarter med egna begränsningar vid närhet; den bevisar ett **fungerande annat spels begränsade rörelsepolicy**, inte våra fem fria M/M/F/SM/SF med key/door/M0. Berzerks trick kan inspirera men får inte kopieras som godkänd spelcanon eller licensfri spelkod.

**Förhandskontroll för möjligt framtida test** ska inte bara jämföra summan av instruktioner med 76: den måste ange *för varje kritisk rasterrad* WSYNC, exakta färgklockor, P0-/P1-RESP/START, GRP-latch, COLUPx, ENAM0, PF0–PF2, CTRLPF, eventuellt RESBL/ENABL och bildexakta deadlines samt 128B/stack/banklayout. Det finns i dag inget sådant komplett G0-godkänt schema för S05 eller fem generellt numeriska fria X/Y.

## 8. Jämförelsematris och konsekvens för beslutad spelvision

| Spår | Offline-jakt | Hardware/G0 | Key/door S05 | Visuell förlust | Beslutspåverkan / risk |
|---|---|---|---|---|---|
| G5-S0 fri numerisk X/Y | Starkast i vår enkla chase-modell (4,05 unika hot/v011) | **Högsta same-Y-risk, EJ G0** | Olöst | Ingen avsiktlig | Bevarar gameplaykrav, teknisk risk **mycket hög** |
| G5-S1a strikt adaptiv Y | 3,16 hot; global BFS 3,32; lång stall i **alla** fall | En NPC per Y-band mer plausibel men G5K P0/door oprövad | Olöst | Ingen med antagen 9r-bandpolicy | **Ändrar verklig jakt/vertikal ordning**; spelkänslerisk **hög** |
| G5-S1b mjuk/dynamisk Y | 4,05 hot | Överlapp vid ~170 av 180 frames/v011; fizisk render ej visad | Olöst | Kräver explicit konfliktbeslut | Mindre AI-ändring, men render-risk **mycket hög** |
| G5-S2 synlighetsrotationsmodell | Samma AI som mjuk | En-vit-pipeline är bara syntetisk gräns; ~499/900 NPC-ticks bortprioriterade | O1 räcker inte för S05-B | Potentiellt oacceptabelt långvarigt flimmer/osynlighet | Kräver uttrycklig **kvantifierad** kvalitets-/flicker-/priority-waiver |

**I nuläget föreslås ingen G5-S1/S2 som färdig produkt.** Själva spelbarheten måste visas med adaptiv NPC-gruppinteraktion och verklig spelarkontroll; varken offline-score, stationär mål-BFS eller en enstaka Berzerk-referens ger ett speltest-PASS. Alternativet *mjuk Y utan acceptabel visningspolitik* löser inte problemet, det flyttar det från AI till TIA.

## 9. Exakta frågor för MAIN VII – användaren beslutar, inte RESEARCH II

**A. Rendering/rörelse (egen beslutspunkt):** Ska fienderna kunna röra sig fritt logiskt i Y även när flera delar rasterhöjd? I så fall vilken **mätbar** synlighetsgaranti behövs per NPC (minsta andel synliga frames, högsta kontinuerliga frånvaro, prioritet för farlig/närbelägen fiende, nyckel synlig i icke-överlapp) eller får spelet ändra mekaniken till uttrycklig Y-arbitrering trots den observerade AI-stallrisken? Högupplösta offlineillustrationer kan visas rådgivande *innan* användaren binder sig. O1 vid faktisk pixelöverlapp är **redan beslutad** och ska inte frågas om igen.

**B. Femfienders-rebaseline (eget versionsbeslut):** Fastställ framtida **R1 fem** (M,M,F,SM,SF) och **R2 fyra + key**, men märk de äldre R1 sex/R2 fem+key som historiska, inte ersatta testbevis. Bevara alla fyra originalmasker, gul spelare, svart bakgrund/bruna PF, orange högerdörr med utskuret svart hål; inga tysta bytes av färg eller kartposition.

**C. Poängsystem (separat från rendering):** 57-beslut 042–047 ger i långtidssaldo med fem och originalets -25 per fiende **+25 netto/rum** vid all-kill (när nollgolvet inte aktiveras), i konflikt med avsikten att all-kill inte skall vara highscorestrategi. Endast användaren får välja att acceptera detta eller t.ex. -30 per fiende (G5N-förslag, **inte godkänt**), särskilt all-kill-avdrag eller annan dokumenterad ändring.

**D. Spawn och key-bärare (separata beslut):** Fem särskilt validerade startankare, 1/5 uniform bärare, faktisk efter-dödsanimation-dropposition, K1/O1 och nåbarhet; nytt PRNG-/spawnval krävs. Ingen ändring av originalets key/drop/hämtning genom vår offlinejämförelse.

**E. Kartbas (eget beslut):** Godkänd luftig *riktning* ersätter inte automatiskt de fyra historiska exakta v0.11-kartorna med v0.19 A/B/C/D_OPEN_01. Om kartbyte önskas behövs separat användaraccept och fysisk PF/door-kontroll.

**F. Ny kodgrind (separat auktorisation):** G5P avslutar endast research; ingen kod-/ROM-/G0-/G6-/F12-/Verification-order kan utläsas ur rapporten eller dessa beslut. MAIN behöver dokumentera en separat tillåten mikrogrind innan ROM DEVELOPMENT III får göra något.

## 10. Minsta framtida falsifierbara hårdvaruprov – EJ STARTAT

Först efter ovanstående relevanta design-/kvalitetsbeslut och en **egen uttrycklig MAIN/användarauktorisation**:

1. **G0 SOURCE-ONLY HARD STOP**: en enda standard-F6/NTSC-kandidat med låsta originalmasker, en gul P0-spelare, en korrekt vit original-NPC, M0-skott, bruna PF och svart BK på samma nio-radersband, två numeriskt dynamiska X-ordningar (player-vänster respektive NPC-vänster). Register-, färg- och CC-deadlines samt RAM/stack och 4 KiB aktiv ROM-bank ska gå ihop. **Vid första G0-brist: STOPP, ingen ROM.**
2. Endast om G0 passerar och ett senare uttryckligt ROM-order följer: maximalt den separat beställda diagnostik-ROM, faktiskt DASM-objekt och Stella-råpixlar/scanline/cycle/mask/visningsfraktion, inklusive båda X-ordningarna. Detta är *inte* ett G5P-test och inget kodat förslag.
3. S05 är **separat framtida obligatoriskt integrationstest**: P1 orange låst högersidedörr och svart *transparent* hål, samtidigt P0 gul spelare/white NPC/guldkey i både A med verklig bitöverlappning och B med enbart same-Y (ingen O1-bortskymning). Aktivt M0, PF/BL vänstervägg, nyckel-/door-X och K1/logic underlåtna från hårdvarugrinden. Om fri key försvinner i B, färgen blir fel eller originell sprite förvrängs: FAIL. Uppfyllda G0-tidskrav och testade råpixlar krävs; ingen simulation kan ersätta dem.

## 11. Filer, reproduktion och granskning

- `g5p_offline.py` – hela huvudexperimentet, inbyggda lossless källkarthexdata, frö, scenarier, närhets-/stall-/occupancy-logik, G5O-replay och S05-bitöverlapp.
- `g5p_global_control.py` – global BFS-känslighetskontroll med samma kollisions-/Y-invariant.
- `g5o_replay.csv` – 12 case med G5O:s ursprungliga kolumner; reproducerad.
- `g5p_scenarios.csv` – samtliga 672 resultat, varje enskild spawn och slutposition.
- `g5p_global_control.csv` – ytterligare 168 strikta global-sök-fall.
- `g5p_traces.csv` – förregistrerade tidsrader för B01/C02/B_OPEN_01, historiska starter, stillastående och dörrflykt, alla fyra huvudmodeller.
- `g5p_summary.csv` – jämförande avgränsade aggregat.
- `s05_logical_stress.csv` – två pixelöverlapptest och namngivna TIA-resursblockerare.
- `RUN_METADATA.json` – kartblob IDs, frö, antal tester och SHA256 för råfiler.

**Begränsningar och absoluta icke-PASS:** inga riktiga 6507-instruktioner kördes, ingen Stella-, ROM-, timing-, nyckelavfyrning-, dödsanimation-, riktig 8×9-kollisions-, mänsklig spelbarhets- eller verklig flickerfrekvensmätning. Två-gridraders Y-kriterium är exakt inom preview-modellen men inte en generaliserad kernel. Dynamic soft prioritization är en medvetet hård syntetisk gräns. AI-policy och storyboard, liksom v0.19-kartor, är rådgivande. **G5 FORMAL USER DECISION PENDING; G6/F12 NOT AUTHORIZED.**
