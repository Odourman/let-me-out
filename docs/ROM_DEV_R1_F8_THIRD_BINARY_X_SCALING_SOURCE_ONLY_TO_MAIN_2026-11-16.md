# LET ME OUT! – ROM DEVELOPMENT II → MAIN V
## R1-F8 – THIRD ORIGINAL NPC + THIRD INDEPENDENT BINARY X – SOURCE-ONLY SCALING GATE

**Datum:** 2026-11-16  
**Slutklass:** **`F8_THIRD_BINARY_X_SOURCE_FEASIBLE_WITH_PRE_REGISTERED_EIGHT_STATES` – endast en källbaserad, falsifierbar teknisk möjlighet. INGEN ny ROM, DASM, Stella, CI eller assembler-/maskändring.**  
**Projektgrind:** `ARBITRARY_THREE_X_NOT_PROVEN / SIX_FREE_XY_NOT_PROVEN / FULL_R1_BLOCKED_NOT_ACCEPTED`.

### 1. Bindande auktorisation, primära källor och exakt bevisgräns

1. [MAIN V:s uttryckliga F8 SOURCE-ONLY-order](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F8_THREE_INDEPENDENT_X_SCALE_SOURCE_ONLY_2026-11-16.md), Git blob `18ecd6f21626304a74e9d462194f71952b18cb32`, kräver **enbart denna Markdown-rapport på en separat branch** från exakt F7 `c8dc8b35f4bb652e3920b70882f8cc1fb84125d3`.
2. [MAIN V:s självständiga F7-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F7_RECEIPT_AND_THREE_X_SCALE_DECISION_2026-11-16.md), blob `2b4e8f2cd62ab28f5d524c5146055b6c869e03e3`; fryst [F7-slutrapport](https://github.com/Odourman/let-me-out/blob/c8dc8b35f4bb652e3920b70882f8cc1fb84125d3/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F7.md), Git blob `b3afd8e1fae89f3612541ab7f966422c0ad126df`. F7:s **verkliga, redan utförda** 160/160 Stella-rutor och 16 traps bevisar endast två binära oberoende X-väljare.
3. **Faktiska, redan arkiverade F7-primärbytes** lästes **READ ONLY** ur [F7 ORIGINAL-evidens på Drive](https://drive.google.com/file/d/116aehSuMbRltvLm0DI68xvtiBQ30SVXT/view), vars SHA256 enligt MAIN är `da6f4ef206e608dbf92749d65e053d27eed4aa2f512e13dc125369766fddb29f`: `r1_f7_2x2_independent_RAM_X_ONE_ROM.asm`, dess verkliga `dist/r1_f7_2x2_independent_RAM_X_ONE_ROM.lst` samt `.sym`. Även [fryst GitHub-bygggenerator](https://github.com/Odourman/let-me-out/blob/c8dc8b35f4bb652e3920b70882f8cc1fb84125d3/rom/v018/experiments/r1_free_xy/r1_f7_build.py) och [förregistrerad G0](https://github.com/Odourman/let-me-out/blob/c8dc8b35f4bb652e3920b70882f8cc1fb84125d3/rom/v018/experiments/r1_free_xy/r1_f7_preflight.py) lästes. **Ingenting har körts, kompilerats, ändrats eller återtestats för F8.**
4. [Låst TOP-DOWN NPC-canon](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json), Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. [C01/C04/B02/E02-gates](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md) och [MAIN:s sex separata X-krav](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md) är **inte** genomförda.
5. Extern *kretsteori, inte ROM-bevis*: Andrew Towers, [Atari 2600 TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), avsnitten `Player Position Counters`, `Player Graphics Scan Counters`, `The Re-trigger Trick`, `CPU Clock to Player Pixel Table`. Towers skiljer CPU:s RESP-write från intern 4-färgklockors reset, separata START-decodes och latchfördröjning; pixelutdata kan överleva senare reset när START redan kommit fram. Dessa internsignaler har **inte** uppmätts i F7 och får inte behandlas som faktiskt F8-resultat.

F7 och F8 använder samma **ENDA fysiska P1**, `NUSIZ1=$01`, återutlöst flera gånger på **samma scanline**. Ett enda fungerande tredje RETRIGGER-fönster betyder inte tre fristående TIA-sprites.

### 2. Exakta tre låsta källmaskerna och 9-radersdataberoenden

Alla nio rader går **uppifrån och ned utan omvändning**; inledande och avslutande `00` i small_male är **obligatoriska riktiga blankrader**, inte möjlighet att förskjuta eller komprimera masken.

| Top-down rad `y` | Stor man M | Stor kvinna F | **Liten man SM, tredje mask** | Gul P0 | M0 enable |
|---:|:---:|:---:|:---:|:---:|:---:|
| 0 | `3C` | `3C` | **`00`** | `3C` | 0 |
| 1 | `3C` | `3C` | **`00`** | `7E` | 0 |
| 2 | `18` | `18` | `3C` | `18` | 0 |
| 3 | `FF` | `FF` | `3C` | `7E` | 0 |
| 4 | `18` | `3C` | `18` | `1E` | **2** |
| 5 | `24` | `7E` | `7E` | `3C` | 0 |
| 6 | `24` | `7E` | `18` | `18` | 0 |
| 7 | `42` | `24` | `24` | `24` | 0 |
| 8 | `42` | `24` | **`00`** | `42` | 0 |

Källplanen avser **exakt dessa 3 masker samtidigt på samma 9 scanlines**, oförändrad P0/M0/speglad brun PF, HMOVE i VBLANK, 262 NTSC och standard-128-byte RIOT. F7:s P0 skriver `GRP0` på c5; M0 `ENAM0` på c10; första M-byte är inläst vid c12. Samtliga dessa existerande moment ska ligga kvar på sina ursprungliga cykler. Tredje `LDA #SM[y]` kan utföras **medan F fortfarande ritas**, eftersom en ren ackumulatorladdning inte skriver TIA:s `GRP1`. Däremot måste den nya `STA GRP1` för SM ske **EFTER F:s sista synliga pixel**, men FÖRE SM:s eget START-fönster. Att skriva SM:s `00` till `GRP1` för tidigt skulle kunna släcka F.

### 3. Den fysiska klocklinjen: F7-fakta och F8:s två nya förregistrerade startfaser

**Exakt F7-fakta från ASM, DASM .lst och historiskt autentiska Stella-traps:**

| Åtgärd på varje av nio F7-rader | `X0=0,X1=0` | `X0=1,X1=0` | `X0=0,X1=1` | `X0=1,X1=1` |
|---|---:|---:|---:|---:|
| Första `RESP1` M (CPU-end / TIA CC) | c21 / 63 | c23 / 69 | c21 / 63 | c23 / 69 |
| `GRP1` M | c24 / 72 | c26 / 78 | c24 / 72 | c26 / 78 |
| Andra `RESP1` F | c32 / 96 | c32 / 96 | c33 / 99 | c33 / 99 |
| `GRP1` F | c35 / 105 | c35 / 105 | c36 / 108 | c36 / 108 |
| **Redan verkligt uppmätt F7 X M/F** | **39,99** | **45,99** | **39,105** | **45,105** |
| F7 källa `WSYNC` c, rad0–7 | 38 | 38 | 39 | 39 |
| F7 källa `JMP + WSYNC` c, rad8 | 41 | 41 | 42 | 42 |

Stella-croppen 900×300 har **2 horisontella bildpunkter per TIA-pixel**, med kalibreringen `cropX=9+2*(TIA-CC-68)` för dessa tidigare rättvända F7-masker. F7 M börjar därför ungefär CC83/86, med sista av sina 8 pixlar CC90/93. F börjar **CC113** (`X=99`) eller **CC116** (`X=105`), med sista av sina 8 pixlar **CC120/123**. Den senare är **senaste verkligt belagda F7-slutpunkt**; de horisontella start-/slut-CC är bakåträknade ur **verkliga** F7-pixlar och 68-CC-HBLANK, **inte interna TIA-latchtraps**. `STA GRP1` för F avslutas CC105/108, 8 CC före hennes observerade start.

**Nya, i F8 på papper förregistrerade hypotetiska tredje P1-RESP-par:**
- `X2_SELECT=$A4` bit0=0 → **SM `RESP1` c48, `GRP1` c51**, CPU-write CC144, databytet finns vid CC153, **förväntad** SM START ~CC161, **crop-X ~195**.
- `X2_SELECT=$A4` bit0=1 → **SM `RESP1` c50, `GRP1` c53**, CPU-write CC150, databytet finns vid CC159, **förväntad** SM START ~CC167, **crop-X ~207**.

Båda faserna måste vara **samma nominella c48/c50 oberoende av de två tidigare bitarna**. Den empiriskt F7-kalibrerade sena c32/c33-RESP-responsen ger ~6 crop-pixlar per +1 CPU-cykel, varför c48→c50 på papper motsvarar **+12 crop-pixlar**. `(195,207)` är **F8-källhypoteser, INGA mätningar**. Det är inte tillåtet att senare ändra dem i efterhand för att rädda hypotestestet.

**Maskfönster, strikt åtskilda på papper:**

| P1-fas | Tidigaste START i relevant tidigare/möjlig modell | Senaste synliga 8-pixelsluttid | Senaste GRP1-write | Nästa RESP1-write |
|---|---:|---:|---:|---:|
| Första M, F7-bevisad | CC83 eller CC86 | CC90/93 | CC72/78 | F c32/c33 = CC96/99 |
| Andra F, F7-bevisad | CC113 eller CC116 | **CC120/123** | CC105/108 | **SM c48/c50 = CC144/150** |
| Tredje SM, **endast hypotes** | **CC161 / CC167** | **CC168 / CC174** | **CC153 / CC159** | nästa scanlines första M = CC63/69 (se separat risk nedan) |

M/F-data ska inte skrivas över medan M/F fortfarande utmatar sista pixeln. Här ligger SM:s **tidigaste nya RESP1-write minst 21 CC efter** F:s senast synliga pixel (CC123); SM:s `STA GRP1` kommer ännu senare men 8 CC före nominell SM START. Riktigt F7-mellanrum för de två tidigare kopiorna behålls oförändrat. En global 76-cykelsbudget och enbart dessa källförhållanden garanterar emellertid **inte** att nästa TIA `START` överlever intern reset/latch; det är den uttryckliga framtida falsifieringsrisken.

**Särskild wrap-/nästa-rad-risk:** en sen SM-RESP vid CC144/150 kan lägga P1:s `main`-wrapdecode ca 160 CC senare på **nästa** scanline, omkring CC76/82 före extra utgångslatch. Nästa rad börjar visserligen med F7:s första M-RESP vid CC63/69, vars interna reset normalt bör avbryta denna återkomst, men just signalracet får **inte** antas vara faktiskt bevisat från källan. Om extra vita pixlar/spöken uppstår vid vänsterkanten är den enkla tre-RESP-arkitekturen inte godkänd, även om den nya kroppen SM syns.

### 4. CPU-cykler och exakta 72 källkombinationer (8 × 9 rader)

**F8-kandidatinstruktioner efter F7:s andra `STA GRP1` och före nästa `WSYNC`**, med `X=0` redan säkrat i F7-dispatch före synlig bandstart:

| F7:s andra RESP | Ny SM-fas | `LDA #SM[y]` | Padding efter LDA | `STA RESP1` | `STA GRP1` | Nästa `WSYNC` |
|---|---|---:|---|---:|---:|---:|
| c32 → `GRP1` c35 | **c48** | c37 | 4× `NOP`, 8 cykler | **3-cyklers zero-page**, c48 | c51 | c54 |
| c32 → `GRP1` c35 | **c50** | c37 | 5× `NOP`, 10 cykler | **3-cyklers zero-page**, c50 | c53 | c56 |
| c33 → `GRP1` c36 | **c48** | c38 | 3× `NOP`, 6 cykler | **4-cyklers zero-page-indexerad `STA RESP1,X`**, c48 | c51 | c54 |
| c33 → `GRP1` c36 | **c50** | c38 | 4× `NOP`, 8 cykler | **4-cyklers `STA RESP1,X`**, c50 | c53 | c56 |

Alla fyra varianter har **identiskt fullständigt synligt SM-byte per rad**, utan `VDEL1`, R1ba `[::-1]` eller släckt F. Tabellen ovan är en **källkalkyl**, aldrig en ny .asm eller DASM .lst.

**Åtta kompletta 2×2×2-RAM-sanningstillstånd:**

| RAM `X0 X1 X2` | M / F / SM `RESP1` CPU c | M / F / SM `GRP1` CPU c | Förregistrerat crop-X (M,F,SM), **ENDAST tredje källhypotes** | Source `WSYNC` rad0–7 | Source `JMP+WSYNC` rad8 | Marginal mot 76, rad8 |
|---|---|---|---|---:|---:|---:|
| `000` | **21 / 32 / 48** | 24 / 35 / 51 | **(39,99,195)** | 54 | 57 | 19 |
| `001` | **21 / 32 / 50** | 24 / 35 / 53 | **(39,99,207)** | 56 | 59 | 17 |
| `010` | **21 / 33 / 48** | 24 / 36 / 51 | **(39,105,195)** | 54 | 57 | 19 |
| `011` | **21 / 33 / 50** | 24 / 36 / 53 | **(39,105,207)** | 56 | 59 | 17 |
| `100` | **23 / 32 / 48** | 26 / 35 / 51 | **(45,99,195)** | 54 | 57 | 19 |
| `101` | **23 / 32 / 50** | 26 / 35 / 53 | **(45,99,207)** | 56 | 59 | 17 |
| `110` | **23 / 33 / 48** | 26 / 36 / 51 | **(45,105,195)** | 54 | 57 | 19 |
| `111` | **23 / 33 / 50** | 26 / 36 / 53 | **(45,105,207)** | 56 | 59 | 17 |

**Full 72-cells radgranskning utan hopslagna eller saknade source-rader:** Varje cell nedan anger `RESP1 SM / GRP1 SM / nästa WSYNC`, beräknat utifrån precis det tillhörande original-8×9-byteparet plus tredje byte i avsnitt 2. De två tidigare RESP/GRP-faserna är **identiska per kolumn med 8-lägestabellen ovan** på varje rad, och P0/M0/medfört kolumninnehåll följer masktabellen ovan. Sista raden har den nödvändiga `JMP F8AfterRows` på 3 CPU-cykler, som i verklig F7-listning.

| Nio källrader `y` | `000` | `001` | `010` | `011` | `100` | `101` | `110` | `111` |
|---:|---|---|---|---|---|---|---|---|
| 0, SM `00` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| 1, SM `00` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| 2, SM `3C` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| 3, SM `3C` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| 4, SM `18` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| 5, SM `7E` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| 6, SM `18` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| 7, SM `24` | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 | 48/51/54 | 50/53/56 |
| **8, SM `00`, JMP+WSYNC** | **48/51/57** | **50/53/59** | **48/51/57** | **50/53/59** | **48/51/57** | **50/53/59** | **48/51/57** | **50/53/59** |

Detta är en **planerad 72-row/state source-tabell** från F7:s **uppmätta befintliga registersekvens och verkliga .lst-instruktionsstorlekar**, **inte** 72 körda bilder, färdig assembler eller bevisade interna TIA-cycles. `WSYNC` c54/c56 och c57/c59 är CPU-källpositioner. Minsta marginal **17 CPU-cykler** vid den nionde radens sista skrivinstruktion. Ingen originalmaskbyte får falla bort.

### 5. Verklig RIOT RAM-plan och oberoende selector API – utan att ändra F7

**Befintlig F7 ASM/.sym:** `FRAMELO=$80`; två X-selektorer `X0_SELECT=$A0`, `X1_SELECT=$A1`; teststeg `F7_SEQ_STEP=$A2`; hållräknare `F7_HOLDCOUNT=$A3`; också `MALE_DELAY=$81`, `FEMALE_DELAY=$82`, `MALE_REQ_X=$90`, `FEMALE_REQ_X=$91`, `PLAYER_REQ_X=$92`, `SHOT_REQ_X=$93`.

**F8:s enbart hypotetiska extra RIOT-byte:** `X2_SELECT=$A4`, inom 128-byte zero-page-spegeln **$80–$FF**, inte överlappande något av föregående. `X0` respektive `X1` har kvar exakt sina två faser c21/c23 respektive c32/c33; den tredje byte ska uppdateras via **egen** `LDA desiredX2[index]`, `CMP X2_SELECT`, `BEQ keepX2`, `STA X2_SELECT`. Varje tidigare selector har fortfarande egen CMP/STA; det får inte ersättas med en enda ihopkopplad 8-profil-ID utan individuella RAM-värden.

**En 3-bit Gray-sekvens som deterministisk framtida testkontrakt (inte körd):**

`000 → 001 → 011 → 010 → 110 → 111 → 101 → 100 → 000`.

Alla **åtta** lägen förekommer; varje steg ändrar **endast en av de tre lagrade RAM-väljarna** och lämnar de andra två byte oförändrade. `F7_SEQ_STEP=$A2` kan hypotetiskt ha åtta steg i stället för sju och dess tre separata desired-tabeller är vardera **8 byte**. `F7_HOLDCOUNT=$A3` håller exempelvis 16 frames per läge. Oavsett tabellens existens måste faktisk kod läsa **A0, A1 och A4** vid synlig bandstart och välja motsvarande en av åtta rasterkernlar. Ett enda profilindex som inte stöds av egna uppdaterbara RAM-byte är diskvalificerat.

**Ingen extra VBLANK-scanline krävs enligt instruktionstabellen:**
- Blank-slot A: den redan befintliga `DEC HOLDCOUNT`/villkorliga stegökningen kan använda `CMP #8` i stället för `CMP #7`; samma instruktionslängder och max under 76 cykler (nytt beslut krävs för faktisk kodändring).
- Blank-slot B: `LDX F7_SEQ_STEP` (3 cykler); för **varje** av tre separata tabeller gäller `LDA table,X` (4), `CMP zp` (3), `BEQ keep` (2 ej tagen/3 tagen), `STA zp` (3 enbart vid byteändring). En konservativ övre gräns även om **samtliga tre** skulle skriva RAM samma frame: `3 + 3×(4+3+2+3) + 2` för slutlig `LDX #28` = **41 CPU-cykler** före ordinarie nästa WSYNC. Gray-stegen ändrar faktiskt högst en byte, där en stramare maxbedömning blir `3+12+10+10+2=37` cykler. Det ligger under 76 i samma tidigare blank-slot; de efterföljande **28** tidigare WSYNC-tillfällena finns kvar.
- Efter sista `TopBlank`: 3-bitars branch-/nära JMP-väljning beräknas hypotetiskt till **mindre än 30 CPU-cykler före rad0:s befintliga STA WSYNC**, och måste ligga i föregående rad, inte i den synliga radens kritiska schema. Realtidskod/proveniens och branch-räckvidd får bara bekräftas av framtida separat auktoriserat steg. Ingen extra WSYNC/scanline är tillåten.

**RIOT RAM:** den **extra** selector-storleken är **1 byte**. Med tre separata X-bitar, de två kontrollräknarna och F7:s övriga ovan angivna RAM-byte ligger denna isolerade användning tryggt inom $80–$FF. Detta bevisar inte att ett senare fullspel med sex godtyckliga numeriska X/Y ryms utan konflikt med resten av gameplay-minnet.

### 6. Bank-/kodstorlek – verklig F7 .lst, åtta källvarianter och exakt kapacitetsbudget

**Faktiskt arkiverad F7-DASM-listning, aldrig omkompilerad under F8:** `F7_00_Row00=$F0FF`, `F7_10_Row00=$F1F5`, `F7_01_Row00=$F2E2`, `F7_11_Row00=$F3D8`, `F7AfterRows=$F4CE`, `SetHorizPos` RTS på `$F504`, nästa kodadress `$F505`. Synlig 4-kernelsektion från `$F0FF` till `$F4CD` är **975 bytes**, övrig programkod **$505 − 975 = 310 bytes**. F7 originaldatatabeller från `ORG $F800` till sista byte `$F868` är **105 bytes**, med tre 16-byte gamla positionstabellfamiljer, originalmasker och två 7-byte RAM-desired-tabeller. Historisk käll-.lst och .sym finns byte-exakt i det redan mottagna Drive-arkivet.

**Exakt per tidigare F7 fyra varianter**, inklusive den sista radens extra `JMP`:
- M21/F32: **246 bytes**; M23/F32: **237 bytes**; M21/F33: **246 bytes**; M23/F33: **246 bytes**; summa **975 bytes**.
- Dubblering till åtta (två hypotetiska X2-värden per var och en av fyra F7-kombinationer): **1 950 bytes** enbart F7-basernas rasterkod.
- Ett SM `LDA #imm`, de explicita `NOP` och en `STA RESP1`/ `STA GRP1` per rad ger **extra byte per rad:** F32+SM48 **10**, F32+SM50 **11**, F33+SM48 **9**, F33+SM50 **10**. Varje F-kombination förekommer med **bägge X0-värdena**, alltså total **`2 × 9 × (10+11+9+10) = 720 bytes`**.
- **Åtta nio-raderskärnor = 1 950 + 720 = 2 670 bytes**, räknat på de **riktiga F7-instruktionsstorlekarna** plus F8:s specificerade hypotetiska instruktioner, inte gissad läsaruppskattning.
- Konserverad F7 annan körbar kod: **310 bytes**. Ge ny 3-bit-dispatch, 1 extra init-store, 1 extra RAM-compare/store och relaterade branch/JMP-mellanhopp en **konservativ, designbegränsande tilläggsreserv om 128 bytes**. Denna 128 är en **övre budgetallokering, inte en uppmätt verklig assemblerlängd**. Den föreslagna tre-tabbsläsningen med direkt branch-/JMP-väljning ska hållas under detta tak eller F8:s bankbudgetomdöme tas om.
- **Max planerad programkod under uttryckligt 128-byte-extra-tak: `2 670 + 310 + 128 = 3 108 bytes`**. En möjlig hypotetisk `ORG $FE00` för data lämnar **3 584 bytes** åt kod från $F000 genom $FDFF, alltså **minst 476 bytes** marginal inom den delen. Det kräver **flytt av datatabellernas ORG inuti SAMMA standard-4KiB-bank**, eftersom F7:s historiska `ORG $F800` annars **överlappar den större exekverbara koden**. Detta är en konkret source-only nödvändig framtida kodlayoutändring, **inte** gjord nu och inte ett byte av kerneltyp/bankformat.
- Original F7 tabeller **105 bytes**, ersätt två 7-byte desired-arrayer (=14) med tre 8-byte (=24) → **115 databytes** vid hypotetisk `$FE00..$FE72`, vilket inte berör vektorer `$FFFA..$FFFF` (sex byte). Totalt planerat faktisk innehåll under dessa villkor **`3 108+115+6=3 229 bytes` i EN 4KiB-bank**, med reserver/gap men utan bytekod efter `$FFFF`.

**Viktiga hårda reservationer:** Detta är en **manuell source-only byte- och cykelkalkyl**, inte en ny DASM-listning; vi har inte bevisat slutlig länkad branchoffset eller att en framtida genomförd dispatch faktiskt håller 128-byte-budgeten. Vid en framtida separat implementation måste den kontrolleras mot **verklig assemblerlistning och 4×4KiB standard-F6** innan en enda ROM anses giltig. I F7 var alla fyra 4KiB-banker identiska; ett F8-förslag räknar **fortfarande endast en tillgänglig 4KiB exekveringsbank för dessa kritiska scanlines**. Bankbyte mitt i synlig 9-radskernel antas inte. F6-bankswitching ger inte fler TIA-objekt, fler CPU-cykler eller RAM-byte.

**Asymptotisk kostnad om samma naiva unrolled-lösning skalas:**

| Antal separata binära X | Förberedda kombinationer | R1-arkitektureffekt |
|---:|---:|---|
| 2, F7 bevisad | **4** | Verkligt positiv tvåmaskerstest; **inte** numerisk fri-X |
| 3, **F8 endast hypotetisk** | **8** | Pappersbudget 2 670 rasterbytes + övrigt; **ingen Stella-acceptans** |
| 4 | **16** | **Naiv dubblering av F8:s åtta trespritekärnor: minst `2×2 670=5 340` rasterbytes**, redan över 4 096 byte *före* fjärde sprites ytterligare instruktioner, dispatcher och data. Den **här rena unrolled-metoden i EN 4KiB-bank skalar därför inte** utan arkitektur-/bankomläggning. Detta är inte ett bevis mot alla möjliga optimerade kernels |
| 5 | **32** | Exponentiell minst fördubbling, redan bortom 4KiB per kritisk bank, ingen fri tids-/objektbudget |
| 6 | **64** | Minst 64× nio på varandra följande kopie-/datasekvenser, ROM-, CPU-, P1- och oberoende Y-krav saknar lösning med oförändrad F7-unrolled-layout |

Även om fyra bankar teoretiskt ger 16KiB ROM, blir de **inte** en enda sammanhängande 16KiB kernel utan verklig bankswitch/dispatch och strikt cykelbevis. Multiplicera `2^n` löser dessutom **inte** kravet på sex godtyckligt numeriska, rörliga X/Y.

### 7. Falsifierbara framtida grindar, källbegränsning och rekommendation

**Det källbaserade positiva delresultatet är NOGA begränsat:**
- Precis **två nya hypotesfaser c48/c50**, identiska nominella resetklockor oberoende av de tidigare två bitarna.
- De åtta synliga M/F-X-paren är **oförändrade F7-utfall** och den tredje X = **195 eller 207 croppixlar** är **uttryckligt ännu omätt**.
- Hela den avgränsade 8×9×8-rad/cykelmatrisen har `WSYNC≤59`, 17 cykler marginal, oförändrade tidiga RESP/GRP, samt en kontrollerbar intern 4KiB-plan. Tredje RAM-byte och 3× CMP/STA är åtskilda i denna framtida designhypotes.
- Den **första obevissade fysiska grinden** är inte CPU-klockbudgeten, utan att **TIA verkligen latchar en ny SM START efter c48/c50 och visar tredje rättvända masken i samtliga sex icke-nollrader**, utan att förstöra någon av de två tidigare maskerna, utan extra kopia vid nästa scanline och med oförändrade P0/M0/PF/262. Här är Towers kretsteori stöd, men inte faktisk Stella-evidens. Ingen sådan undersökning är genomförd.

**Om MAIN V i framtiden uttryckligen väljer ett separat nytt tekniskt steg** vore den minsta diskriminerande fysiska kontrollen: **en enda ny** standard-F6/NTSC-ROM med **åtta** förregistrerade bitkombinationer, 3 separata RAM-byte och riktiga Stella-bilder/traps för första, andra och tredje `RESP1/GRP1`, direkt nio-raders TOP-DOWN set+bitmap-kontroll av **samtliga tre** originalmasker inklusive **SM:s 00-rader**, både P0/M0/PF/262 och wrap-sökning på följande scanline. Vid X2-miss/falska kopior måste metoden få NEGATIV gate; **inga automatiska c46/c52-svep, NUSIZ-ändringar eller fler ROM-varianter** följer av denna rapport.

Om den fysiska grinden fallerar krävs separat MAIN-beslut om en **annan** renderer, t.ex. en kontrollerad re-trigger-/NUSIZ-kopiegruppkernel med omplanerad GRP1-datalatch och verklig TIA-synlighetsaudit. Äldre R1ba:s `NUSIZ1=$03` är bara rådgivande: MAIN har bevisat att dess fyra stora masker är **uppochned** i 600/600 trots forskningsauditor-pass; dess grupper har dessutom **kopplade X**. Den är **inte** en färdig ersättningsbas och ingen R1ba-reparation får göras under F8.

**Kostnadsskillnad, utan överdriven tolkning:**
1. **3 individuella RAM-bitar × 2 nominella kopiestarter** = 8 diskreta val, med efterföljande visuellt utfall **ännu obekräftat**.
2. **3 fritt numeriska X-värden** kräver minst tre numeriska koordinatlagringar samt en kernel som mappar *godtyckliga* positioner till säkra on-the-fly TIA-resets; detta bevisas **inte** av åtta förkompilerade fall.
3. **6 fria X/Y** kräver sex logiskt individuella X/Y (12 koordinatvariabler), samtliga sex låsta originaltyper, både **same-Y** och förskjutna rasterband enligt C01/C04, synlighet och kollisioner. `2^6=64` låsta bitprofiler är **inte** en ersättning.
4. **Riktig integrerad R1/R3/R2/R4** behöver därutöver spelare/skott, karta, verklig dörr/nyckel, tidsbudgeten, PAL när separat godkänt, gameplay och **oberoende Verification E02**. Detta F8-papper bevisar inget av dessa integrationskrav.

### 8. HÅRT STOPP OCH SLUTKLASS

`F8_THIRD_BINARY_X_SOURCE_FEASIBLE_WITH_PRE_REGISTERED_EIGHT_STATES` betyder **bara** att den specificerade 3×binära 8-lägeshypotesen ryms **på papper** inom föreskriven CPU- och bankbudget och har två förregistrerade X2-faser. **Det är inte ens en enda verifierad tredje P1-kopia**. De två redan bevisade F7-X-väljarna förblir historiskt positiva; ett nytt faktiskt tredje X får aldrig hävdas innan MAIN uttryckligen auktoriserar och självständigt mottar en framtida testleverans.

**Leverans:** exakt EN ny Markdown-fil `docs/ROM_DEV_R1_F8_THIRD_BINARY_X_SCALING_SOURCE_ONLY_TO_MAIN_2026-11-16.md` på ny isolerad branch från fryst F7. **Inga** nya ASM/DASM/ROM/Stella/screenshots/CI/Python auditer/ZIP, inga ändringar i canon/F7/main/PR#7, ingen oberoende VERIFICATION, inget F9, R2/R3/R4, PAL, grafik eller fullspel. ROM DEVELOPMENT II stoppar efter denna rapport och Issue #6-handoff.

**Full R1 är fortsatt `BLOCKED / NOT ACCEPTED`.**
