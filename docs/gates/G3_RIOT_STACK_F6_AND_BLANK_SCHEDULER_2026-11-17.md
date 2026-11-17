# LET ME OUT! – MAIN VI G3 – RAM, stack, F6 och schemaläggningskontrakt (SOURCE ONLY)
**Datum:** 2026-11-17. **Typ:** teknisk planeringsrevision av befintlig forskning. Inga nya spelbytes, ROM, DASM, Stella, CI, grafikbeslut eller G4 auktorisation.

## 1. Fast fysisk minnesgräns

| Resurs | Hård fakta | Betydelse |
|---|---|---|
| RIOT RAM | **128 byte** i standard-Atari 2600, logiska `$80..$FF` och speglade adresser | Stackens 6507/6502-sid-1-spegel delar **samma fysiska 128 bytes**, inte 128 extra. |
| Sex NPC-koordinater | Sex individuella 8-bitars X och sex 8-bitars Y = **12 byte** | Nödvändig men långt ifrån tillräcklig; separata X/Y-lagringar är inte fysiska TIA-kopior. |
| Standard-F6 | **16 384 ROM bytes, fyra 4096-byte banker**, exekverar endast **en** bank åt gången | 4K resident code, tabeller och reset/IRQ-vektorer måste faktiskt få plats; inga extra 128 RAM eller extra P0/P1. |
| F6 hotspot | `$1FF6..$1FF9` (motsvarande full adresskod `$FFF6..$FFF9`) | Bankbyte sker på hotspotaccess och måste lämna PC i en giltig fortsättningsinstruktion i **målanvänd bank**. |
| TIA-kernel | 76 CPU-cykler/rad, 228 colorclocks/rad, 160 aktiva CC | Bankbyte i VBLANK eller mellan hela rastersnitt, inte fritt inuti P0/P1-/PF-skrivdeadline. |
| NTSC-blankperiod | 3 VSYNC +37 VBLANK +30 overscan = 70 linjer (typisk 262-profil) | Brutto `70×76=5320` CPU-cykler totalt i dessa perioder om valt frameupplägg följer originalguiden; de används också för VSYNC, RIOT/timer/input och annan logik, alltså **inte** 5320 lediga schemaläggningscykler. |

**Primärt källstöd:** [Atari Stella Programmer's Guide, HTML](https://www.atariage.com/2600/programming/2600_101/docs/stella.html), [Stella 6.7.1 CartF6.cxx](https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/CartF6.cxx), [F10 source-only](https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md). Senare emulatorversioner får inte automatiskt ersätta exakta historiska 6.7.1-fasrapporter.

## 2. F10:s redan publicerade HYPOTETISKA RAM-budget, återanvänd utan att upphöja till mätt kartläggning

| Ändamål | Föreslagna bytes | Summerat |
|---|---:|---:|
| Sex numeriska X och sex Y | 12 | 12 |
| NPC typ/ID/status/animation/HP/facing | 18 | 30 |
| Sex sortindex plus sex tvåbyte mask/radpekare | 18 | 48 |
| Aktuella sex maskbytes plus sex RESP-/delayvärden | 12 | 60 |
| P0 spelare, M0 projektil position/state | 7 | 67 |
| Key, door, room, lock | 6 | 73 |
| PF vänster/höger scratch | 6 | 79 |
| Frame/timer/line/mode counters | 6 | 85 |
| Kollisions-/händelseflaggor och ID-nycklar | 8 | 93 |
| Konservativ stackreserv | 24 | **117** |
| **Ej allokerade återstående bytes i denna MODELL** | **11** | **128** |

**Kritisk markering:** Detta är F10:s illustration, **inte** ett RAM-överlägg från körbar fungerande sex-NPC-assembler. Det finns inget bevis att 11 bytes faktiskt är fria när stack-high-water, faktisk VBLANK-sort och gameplay-AI läggs till. F9:s faktiska `$A0/$A1/$A4`-positioner används som enbits-modevärden i en annan fryst ROM, inte som dynamiska numeriska koordinater. F11:s `$A0..$A3`-förslag kompilerades aldrig. R3:s `$83`-dörrstatus är branchlokal, inte en kollisionsfri adressplan ihop med F9.

### 2.1 Bevisligen ohållbar naiv fullbandspreparation
Om varje av sex NPC kräver per-scanline förberedda 8bitars maskdata `6×9 = 54 bytes` och separat positionerings-/händelsetid `6×9 = 54 bytes`, blir dessa två arrayer **108 bytes**. Bara sex numeriska X/Y ytterligare **12** och en konservativ **24-byte stackreserv** ger **144 >128 bytes**, redan **16 bytes över gränsen** innan typ, spelare, key, PF eller timer. Det falsifierar DENNA fullständigt materialiserade form, **inte** all streaming/eventkompression.

### 2.2 Huvudväg A – rullande events, aldrig per-CC full framebuffer
- Ha `x[6]`, `y[6]`, beständiga NPC-ID och typ i RIOT; sortera X/Y/aktiva scanline-objekt under VBLANK eller översynligt y-block när det finns mätt tid.
- Förbered endast de maskbytes och rasterhändelser som verkligen behövs för nästa synliga linje/delband, med kontrollerade återanvändningslivstider. C04 har 6 faktiskt icke-tomma originalmaskbytes på y103–104 i den valda spridda Y-konstellationen, trots att SM/SF har tomma rader på andra linjer.
- Använd ROM-lookup av original-masktabeller och kart-/PF-byte när det sparar RAM, men räkna `LDA abs,X`/page-cross etc och GRP-/RESP-skrivdeadline i varje rad. ROM-tabeller ersätter **inte** datastyrd exekvering eller output-register.
- RESERVERA säker stack och ev. JSR/RTS-/NMI-disciplin; inga stack/RIOT-spegeltrick som låtsas ge extra RAM.

### 2.3 Reservväg B – kod-/databankspecialisering endast när det verkligen hjälper
- Om en universell 9-raderskod inte ryms i 4K, dela **mellan frysta kodvägar** på komplett Y-zon och välj bank i blankning. Håll säker trampolin och same-PC-återgång; verifiera 4×vektorer; tilldela all data med minne för bankhotspots.
- Separera statiska PF-/kartanalyser från 8bitars-aktörkerneln endast om samma-rad-pixelresultatet fortfarande korrekt. En dörr i annan bank kan **inte** bokas in samtidigt med en NPC i första bank utan verklig fram-/returhändelse under samma rad.
- Mät objektens önskade X/Y innan bankval; använd **inte** `2^6=64` förprogrammerade scenkernlar för de sex NPC:erna. F9:s 8-lägeskod är 2670 bytes: ren skalillustration 16 lägen ≈5340 (>4K) och 64 lägen ≈21360 (>16K), redan före full R1/R3.
- Isolerat R3 bygger **6×176 byte PF-tabeller +176 byte P1-nyckelhål = 1232 bytes**. F9 har separat 3019 program +115 tabell +6 vektorer =3140 bytes i sin aktiva bank. Naivt samtidigt resident `3140+1232=4372` är **276 över 4096**, men gäller två inkompatibla källbyggen; det är **ingen** bevisad storlek hos en optimerad kombinerad kernel.

### 2.4 Plan C – stopp innan en falsk arkitektur-PASS
Om worst-case bandkontrakt kräver >128 fysiska RIOT-byte efter konkret livstidsdelning, eller om eventuell kod i EN aktiv bank måste vara >4096 bytes, dokumentera minsta motexempel och kandidatoptimering. **F6SC/Superchip (extra RAM), DPC/DPC+/CDF (hjälpkrets/ARM), SCABS eller PAL är INTE del av standard-F6-bevis**. Sådan ny hårdvara eller användarkompromiss kräver separat explicit beslut; extra RAM/bank skapar inte extra TIA-färgregistret.

## 3. Exakt status för G4:s möjliga mikroprov
F9 och R1g är positiva fragment, men olika ROM-kernlar. Inget käll-/minneskonto för en F6-ROM som tillsammans ritar 6 fritt numeriskt X/Y originalmasker, gul spelare, aktiv M0 **i samma 9-radersband** och PF är ännu uppmätt. Detta G3-dokument skapar en **kapacitetsram och kontrollkriterier**. G4 måste SOURCE ONLY identifiera en enda fysikfråga kring P0+vit NPC-/M0-färg, P1 vita mask och PF, samt kunna säga `GO_TO_ONE_AUTHORIZED_MICROTEST` eller `NO_GO/INCONCLUSIVE` utan att kräva full sex-NPC-pappersbevisning.

**Arkivera inte detta som `RAM_ALLOCATION_PASS`, `F6_BANK_SWITCH_PASS` eller `R1_INTEGRATED`.**
