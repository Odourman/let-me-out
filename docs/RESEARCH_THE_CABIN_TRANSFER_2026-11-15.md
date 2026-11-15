# LET ME OUT! — RESEARCH: Överförbara lärdomar från The Cabin

**Datum:** 2026-11-15  
**Roll:** RESEARCH. Analys och rekommendationer till MAIN, utan kodändring eller implementationsmandat.  
**Ingångsarkiv:** `THE_CABIN_ALL_RESEARCH_SAMLADE_KALLOR_2026-11-15.zip` (221 387 157 byte, 350 fysiska toppnivåposter; arkivets egen kontroll redovisar 343 unika källfiler och 65 deduplicerade alias).  
**Avgränsning:** Den här genomgången gäller *Let Me Out!*, inte nytt beslut eller statusändring för *The Cabin*. Ingen ändring har gjorts i något repository.

## 1. Slutsats

Ja, materialet är användbart, men **ingen inkluderad metod är redan bevisad för Let Me Out!:s krav med sex individuellt placerade androider, gul spelare och aktivt skott på samma rasterhöjd**. De bästa överförbara byggstenarna är:

1. **Cyloid:** En tvålinjerskernel med `P0` spelare, `P1` tidsmultiplexade mål, `M0` spelarprojektil och PF-hinder. Konkreta, läsbara 6502-rutiner i arkivet; starkt teknikspår för **renderingskandidat A**, men spelet visar inte sex fria mål samtidigt.
2. **Crystal Castles:** `P1` återanvänds för olika objekt på *olika* vertikala ställen genom objektindex och nästa-grafikpekare. Bra att utnyttja när fienderna inte delar rasterband. Löser inte det obligatoriska same-Y-stressfallet.
3. **AStar:** Exakt planerade asymmetriska PF-skrivningar, förberedda bildmasker och separata spritepositioneringsfaser. Relevant för den speglade rummens vänster/höger-grafik och **renderingskandidat B**. Begränsningen är PF-pixelns fyra färgklockor; den räcker inte automatiskt till originalets 8×9-silhuetter. Källan är GPL-3.0-or-later: studera teknik, kopiera inte kod utan licensanalys.
4. **Tvålinjerskernel/VDEL + förberäknade rasterdata:** Frigör arbetsfaser per par skärmrader, kan göra spriteuppdateringar mer stabila och hålla tung logik utanför ritningen. Skapar **inte** fler TIA-spelarsprites.
5. **Metod från The Cabins PoC och Pachinko:** Verifiera med verklig Stella, pixel-/synlighetsmätning, korrekta registerdeadline, många sammanhängande frames och riktade motexempel; logik-PASS och raster-PASS måste redovisas separat.

**Rekommenderad prioritet:** Lägg ingen tid på att direkt portera The Cabins rankkapning, gröna spetsar, avancerade kartkomprimering eller F6SC-idéer. Lägg tiden på R1/R2:s verkliga X- och spriteflaskhals inom redan auktoriserad v0.18.

## 2. Inspekterat underlag och metod

- Huvudarkivets samtliga toppnivåposter inventerades, CRC-kontrollerades (`ZipFile.testzip(): None`), och alla **111** inre ZIP:ar fick en separat fil-/strukturförteckning. Det stora Pachinko-evidensarkivet innehåller **37 056** inre filer, huvudsakligen råspår; dessa är inventerade, **inte individuellt manuellt lästa**.
- Huvudrapporterna från tidig research, 30-projektsstudien, Atari-manualer, MAIN IV/V, oberoende kernelverifiering, T2-delprov och Pachinko-genomgången studerades. Faktisk assembler från `Cyloid` och `AStar` inspekterades i den arkiverade källkodssamlingen; rapporterna om `Crystal Castles`, `Dark Chambers`, `Pole Position` och `2048-2600` korslästes mot arkivets källkodsinventering.
- Sex PDF:er inventerades och text extraherades när möjligt. `2600_guide.pdf` är bildbaserad; dess 25 sidor har **inte** tolkats som OCR-underlag för slutsatserna. Den särskilt märkta `EJ_FAKTAGRANSKAD`-rapporten behandlas inte som verifierad primärkälla.
- Allt detta är forskning och historiska experiment; 2026-11-12-kopior av The Cabins Project Sources är inte live-kanon för Let Me Out!.
- För Let Me Out! lästes följande **aktuella GitHub-dokument** via det anslutna verktyget 2026-11-15: `docs/CURRENT_PROJECT_STATE_2026-11-15.md`, `docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md`, `docs/ROM_GATE_V018_SCOPE.md`, `docs/ROM_GATE_V018_ACCEPTANCE.md`, `planning/ROM_GATE_V018_TEST_MATRIX.csv`, `docs/ROM_GATE_V018_BLOCKERS.md`, `docs/MAIN_SPRITE_FEASIBILITY_V018_2026-11-15.md`, `docs/MAIN_RASTER_DELTA_V018_2026-11-15.md`, `docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md` och `docs/MAIN_PLAYER_SCALE_V018_2026-11-15.md`. Detta är en lässnapshot, inte någon garanti om framtida HEAD.

## 3. Prioriterad teknisk fyndmatris

| Prioritet | Fynd | Exakt källspår i arkivet | Tillämpning i Let Me Out! | Gräns / bevisläge |
|---|---|---|---|---|
| P0 | Cyloid 2-line, P0/P1/M0/PF, målflimmer | `02_KALLOR_MANUALER/Atari2600_Spelkallkod_Samling_2026-11-04.zip` → `.../keithadler/cyloid/game.asm`, särskilt rader 10–32, 791–815, 1679–1758 | Jämförelsebas för renderingskandidat A; bevara spelaren och skottet | En P1-målfigur väljs i kodens flimmerloop; sex samhöjda originalandroids är inte bevisade |
| P0 | Crystal Castles P1-objektschemaläggning | `01_TIDIG_RESEARCH_DRIVE/TheCabin_Kallkodsanalys_2026-11-04.md`, §3; `02_KALLOR_MANUALER/atari-2600-source.zip` → `Crystal Castles.zip` → `CCKRN.MAC.1` | Dynamisk vertikal återanvändning när objektband skiljer sig | Same-Y kräver annan metod; inga fria sex X bevisade |
| P0 | AStar timed asymmetric PF | 30-projektsrapport §2.3, arkiverad `astar-free/kernel.asm` rader 57–75; faktiska PF1/PF2 stores med c19/c34/c41/c48 | Högerdörrens asymmetri och PF/TIA-hybrid | PF 4 färgklockor/bit, 8×9-identitet fortfarande blockerad; GPL-3.0+ |
| P0 | 2-line + VDEL | `01_TIDIG_RESEARCH_DRIVE/TheCabin_Research_AtariAge_Manualer_2026-11-04.md`, §3A; `00_RABBIT_HOLE_HUVUDRAPPORT.md`, §4 | Omplanera registerskrivningar, förebered spritebyte på föregående rad | Fler CPU-möjligheter, inga extra fysiska sprites |
| P0 | Kritiskt pixel-/rastertest från The Cabin | `05_TEKNISKA_PROV_OCH_VERIFIERINGSUNDERLAG/TheCabin_KernelPoC_Oberoende_Rapport_Till_MAIN_2026-11-05.md` | Kräv hårda same-Y test, skärmradscykler, pixelmål, loggar | Historiskt delprov: combined PASS men färgkanter 4/30 PASS och inline c115/358 VSYNC-rader FAIL |
| P0 | Pachinko: population, riktade motexempel, återspelning | `08_PACHINKO_2026_11_12/THE_CABIN_PACHINKO_REPORT_TO_MAIN_2026-11-12.md` | Utforska fiendespawns, X-ändring, lås/nyckel/occlusion och kollisionsgränser i framtida behörigt test | Testade Cabin-ROM, inte Let Me Out!; botutfall är inte mänsklig spelbarhet |
| P1 | Förberäkna PF per rum/band | Dark Chambers `MAZE.S` och `EQUATES.S` enligt `TheCabin_Kallkodsanalys`, §2; `astar-free` map loader | Rummens speglade/bruna väggar kan vara relativt statiska. Förbered maskbyte *före* synlig kernel och undersök om väggskrivningar kan minskas | **Egen arkitekturinferens för Let Me Out!**, inte mätt i dess ROM; ingen säker besparing tills band-/pixelkrav provats |
| P1 | 2048-2600 interleaved sprites | 30-projektsrapport §2.4, `2048-2600/2048.asm` och `graphics.asm` | Jämför exakt vad NUSIZ-/midscanline-byte medger för olika figurer och HUD | Fasta avstånd/skrivdeadlines, inte ett bevis för 6 godtyckliga X |
| P1 | M0 som skott | Cyloid `game.asm` rader 10–15, 1719–1755 | Låt P0 vara gul spelare, M0 skott, P1 i första hand NPC | M0 delar färg med P0 och har smal geometri; testa hur testsymbolen får se ut |
| P1 | Spelvärld skild från ritad bild | `TheCabin_Research_AtariAge_Manualer...`, §3G; 30-projektsrapport §4.5 | Alla sex androider logiskt aktiva varje frame även när vissa ritas med flimmer; K1/E1/O1 oberoende av spriteval | Rätt händelseordning måste styras av Let Me Out!:s egna godkända regler |
| P1 | RIOT-RAM overlays och bankdisciplin | 30-projektsrapport §2.4/§2.6; Dark Chambers; 2048-2600; Wordle | Separata X/Y-/typ-/statusbyte för sex NPC, återanvänd *scratch* i icke överlappande faser | Vanlig F6 ger bara 4×4 KB ROM och 128 B RIOT-RAM; overlays sparar inte persistent NPC-state |
| P2 | Hud separat från spelarena | Pole Position multi-GRP-siffror; 2048-2600 siffror | Framtida poäng/livband på separat rasterhöjd | Inte inom nuvarande R1–R4-kodscope |
| P2 | Långsam AI-jobbdelning | Dark Chambers frame-interleaving; Cyloid even/odd logik | Senare: budgetera patrull/jakt per tick, men behåll omedelbar kollisionskontroll | Ej tillåtet att börja implementera AI inom nuvarande R1–R4 |
| P2 | Kreativa display-list-kernels | Rabbit-hole §3.1–3.3: Steven Hugg 2025 | Idé för schemalagd uppdatering av PF och sprites, kan inspirera kandidat B | Demonstrationerna har kraftiga händelse-/RAM-begränsningar; ingen evidens för sex humanoider |

## 4. Huvudhindret i siffror: varför NUSIZ inte räcker

Let Me Out!:s aktuella design kräver **sex logiskt oberoende X-positioner** och fyra läsbara 8×9-originalsilhuetter (2 stora män, 2 stora kvinnor, 1 liten man, 1 liten kvinna), plus lika stor gul spelare och skott. `P0` och `P1` är två sprites, inte åtta. `NUSIZ` ger kopior på vissa **fasta** avstånd. Tvåsilhuettsprovet visade stor man och stor kvinna vid 32/64 färgklockors avstånd i verklig Stella, men detta är en begränsad teknikdemonstration.

MAIN:s direkta offlinegranskning för Let Me Out! (`docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md`) räknade **64 045** historiska möjliga sexkombinationer. **44 191** saknar *något enda par* på de i teknikprovet verifierade NUSIZ-avstånden. Det är **inte** en sannolikhet för fel i spelet: spawnpoolerna varierar per karta, och försöket gäller en abstrakt X-projektion, inte spelraster. Det falsifierar däremot idén att bara låsa fienderna i de avstånden utan att ändra deras fria placering.

**Mest relevanta testfallet:** sex androiders start-X `[16,36,56,76,96,116]` i färgklockor på samma rasterhöjd, sedan egna X-ändringar under 600 verkliga Stella-bildrutor. Testa både närhet och särskilt de fyra godkända originalmaskerna. Ingen fiende får bli logiskt passiv för att den inte tecknas en viss frame.

**Resursförslag, endast teknikmodell:** `P0` = spelare, `M0` = testskott, `P1` = prioriterad androidrendering, `PF` = väggar och eventuellt grov grafisk hjälpinformation. Eventuella `M1`/`BL`-objekt är en hypotes, inte hela humanoider; färgregistren delas. R2:s nyckel och R3:s orange dörr/nyckelhål behöver egen, faktiskt mätt resursplan.

## 5. Konkret rekommendation inom redan auktoriserade v0.18/R1–R4

Behandla dessa som **delprov inuti de två redan tillåtna kandidaterna**, inte nya fasmandat.

### Kandidat A – tidsmultiplexning med Cyloid/Crystal Castles som mönster

- Börja med en mätbar P0-spelare, M0-skott, P1-mask för stor man/kvinna med oberoende X, reproducerbar tvålinjers-/VDEL-plan.
- Återanvänd P1 i skilda vertikala band när det faktiskt fungerar; jämför detta med alla sex på *samma* band.
- Vid tidsmultiplexning, logga synlighet **per individ** över 600 frames: antal synliga frames, maximal följd av osynliga, scen-/frame-ID och X. Värdera om spelaren faktiskt kan uppfatta fienderna. Sex faser och endast en fiende per frame ger teoretiskt ca 10 visningar/sekund per fiende vid 60 Hz, **inte** ett accepterat flimmer-PASS.
- Inga kodändringar får tvinga ihop de sex X-koordinaterna eller byta originalmasker tyst.

### Kandidat B – PF/TIA-hybrid med AStar/2048 som principer

- Förbered vänster-/höger-PF-masker för ett 40×22-rum och undersök en rasterplan som uppdaterar endast när det behövs, med separat högerdörr-PF0-behandling.
- Pröva om PF kan bära väggar och billig komplementgrafik medan P0/P1 ger exakt läsbara mänskliga konturer. Jämför *riktiga pixelmål* för alla fyra originalmaskerna, inte bara sex vita rektanglar.
- Visa explicit vilken upplösning varje figur skulle få. PF:s 4 färgklockor per bit innebär att en 8-kolumners bitmap inte direkt är en 8 färgklockor bred PF-mask.
- Testa R2 med fem överlevande androider + guldnyckel + spelare + skott, inklusive O1, utan att flytta eller förstöra den logiska nyckeln.

### Gemensamma beviskrav

- För varje belastad rasterrad: assemblerinstruktion, faktisk CPU-cykel, TIA-register, pixeldeadline, bank och scen.
- Logga 600 sammanhängande verkliga Stella-frames per R1/R2/R4 och samtliga avvikelser från föreslagna 262 scanlines. Registrera inga automatiska PASS på saknade spår.
- Byggrecept med DASM, SHA-256 och korrekt loadade Stella-script/listing/symbolfiler; oförändrade fullständiga debuggerbilder samt tydligt märkta beskärningar.
- Redovisa T01–T16 i det befintliga `planning/ROM_GATE_V018_TEST_MATRIX.csv`. ROM DEVELOPMENT:s egenkontroll är inte oberoende VERIFICATION.
- Om båda kandidaterna saknar rimlig lösning: överlämna ett tekniskt FAIL/BLOCKED till MAIN. Ändra inte sex NPC, deras individuella X, grafikkrav, poäng/AI eller andra spelregler utan separat användarbeslut.

## 6. Positiva och negativa historiska bevis att inte förväxla

**Cyloid:** Den faktiska arkiverade assemblerkoden avsätter separata renderingsobjekt, en tvålinjerskernel och en roterande P1-målselector. Källans egna cykelkommentarer anger maximalt 61/71 cykler i respektive radtyp. Dessa värden **har inte ommätts för Let Me Out!**; spelets logiska frame-interleaving får inte automatiskt föras över till vår omedelbara kontakt- och skottlogik.

**The Cabins oberoende kernel-PoC:** 35 assemblerade ROM-varianter återbyggdes i Stella. En syntetisk kombinerad scen gav lokalt pixel-PASS och 71/68 cykler i alternerande radtyper. Men av 30 riktade färgkantfall passerade **bara 4**, och inline-avkodningen använde **115 cykler** och gav **358 rader per ROM-VSYNC-period**, vilket underkändes. Lärdom: en snyggt renderad scen eller en bra nominell cykelsumma räcker inte.

**The Cabins Pachinko-rapport:** 24 fria policykörningar över 28 800 Stella-bildrutor gav 65 registrerade snitt, med separat deterministisk referens. Ytterligare riktade tester fångade svåra rot-/mitt-/spetsfall; i vissa specialfall uppstod 304–477 rader mellan synkpulser trots logiskt korrekta resultat. För Let Me Out! är metoden överförbar: kombinera variationsrika, seedade botspår med *avgränsade riktade scenbevis*. Implementera inte The Cabins botlogik i spel-ROM:en.

## 7. Lärdomar som i nuläget INTE bör överföras

- **Vinrankornas T2-masker, suffixkapning, packade svängar, 4×2-områdeskartor och grön spetsfärg:** mycket specialiserade för The Cabin och saknar direkt koppling till sex humanoider i Let Me Out!.
- **128 byte extra Superchip-RAM, F6SC, odokumenterade 6502-instruktioner, externa AtariVox-funktioner:** inget som kan antas ingå i auktoriserad standard-F6-diagnostik. Större ROM eller RAM löser inte TIA:s spriteantal eller 76-cykelgräns.
- **Monsterspecifik yxa, automatisk attack, rankfångst, dörrtimers i The Cabin:** inte Let Me Out!:s spelregler.
- **Licensierad kod:** flera GitHub-källor i arkivet är MIT, några GPL och historisk kommersiell Atari-kod har andra rättighetsvillkor. Analys av idéer tillåter inte kopiering till spelets release utan korrekt licensspårning.
- **Forskningsrapporter som skrevs före senare beslut:** ingen får ersätta Let Me Out!:s nuvarande MAIN-beslut. Just nu är **endast NTSC-diagnostik v0.18/R1–R4** auktoriserad. Draft PR #7 är inte full R1 PASS; VERIFICATION #8 gäller fryst baseline och får inte ärvas av ny kod.

## 8. Sammanfattad handoff till MAIN

**Forskningsrekommendation:** Behåll den beslutade designen och de befintliga två teknikkandidaterna. Be ROM DEVELOPMENT pröva främst (A) Cyloid/Crystal Castles-inspirerad P1-tidsdelning med P0-spelare och M0-skott, och (B) AStar-inspirerad, förberäknad asymmetrisk PF/TIA-hybrid. Provet ska visa **sex individuella X och fyra ursprungsmasker på gemensam rasterhöjd**, 600 verkliga Stella-frames med per-android-synlighet, cykel-/registerdeadlines samt R2-konflikten med nyckeln. Inga nya steg, spelregler, designwaivers, PAL eller fullspel påbörjas genom denna rapport.

### Källfiler som är viktigast att överlämna tillsammans med rapporten

1. `01_TIDIG_RESEARCH_DRIVE/TheCabin_30Projekt_Samlad_Analys_2026-11-04.md`
2. `01_TIDIG_RESEARCH_DRIVE/TheCabin_Kallkodsanalys_2026-11-04.md`
3. `01_TIDIG_RESEARCH_DRIVE/TheCabin_Research_AtariAge_Manualer_2026-11-04.md`
4. `01_TIDIG_RESEARCH_DRIVE/00_RABBIT_HOLE_HUVUDRAPPORT.md`
5. `03_MAIN_IV_RESEARCH/TheCabin_RESEARCH_LOSNINGAR_2026-11-07.md` (främst L04, L07, L09–L11, L19–L20)
6. `05_TEKNISKA_PROV_OCH_VERIFIERINGSUNDERLAG/TheCabin_KernelPoC_Oberoende_Rapport_Till_MAIN_2026-11-05.md`
7. `08_PACHINKO_2026_11_12/THE_CABIN_PACHINKO_REPORT_TO_MAIN_2026-11-12.md`
8. `02_KALLOR_MANUALER/Atari2600_Spelkallkod_Samling_2026-11-04.zip` (Cyloid, AStar, 2048-2600, relevanta licenser)
9. `02_KALLOR_MANUALER/atari-2600-source.zip` (Crystal Castles och Dark Chambers, som *historisk teknikresearch*, inte fri kodimport)

**Slutsatsens säkerhet:** Hög att mönstren existerar i det inspekterade materialet och att NUSIZ inte automatiskt ger sex oberoende X. Medel att de sparar relevant rastertid för Let Me Out!. Okänd tills kod och Stella bevisar fullständiga R1/R2 med godkända silhuetter.
