# LET ME OUT! – MAIN VI: G3 SAMMANHÅLLET R1–R4 TIA- OCH RESURSKONTRAKT
**Datum:** 17 november 2026. **Roll:** MAIN VI, source-only teknikrevision. **Status:** `G3_SOURCE_ONLY_RESOURCE_CONTRACT_COMPLETE_WITH_UNPROVEN_PHYSICAL_SCHEDULE`.

**VIKTIGT:** G3 är ett godkänt *planerings- och källgranskningssteg*, **inte** en godkänd 6507-kernel, inte G4-GO, inte `R1 PASS`, inte E02 och inte en licens att skapa F12/ROM. R1 och full v0.18 förblir `BLOCKED / NOT ACCEPTED`.

## 0. Exakt mandat och källa
Efter fullbordad G2 gav användaren instruktionen "Ok, fortsätt". MAIN VI har därför genomfört **exakt nästa grind G3** i [G1–G10-playbook](../MAIN_VI_G1_G10_CONTINGENCY_PLAYBOOK_A_B_C_2026-11-17.md): sammanför objekt/färgregistrering, **per-rad CPU och fysiska TIA-colorclock-deadlines**, sex separata X/Y, RAM/stack/F6-bank, R2 guldkey/O1 och R3 högerdörr/nyckelhål i EN risk- och acceptansmodell.

**Authority:** ursprungligt 57-beslutsarkiv / efterföljande uttryckliga användarbeslut > befintligt [Issue #6 v0.18 NTSC diagnostiksammanhang](https://github.com/Odourman/let-me-out/issues/6) och [acceptanskriterier](../ROM_GATE_V018_ACCEPTANCE.md) > verifierade käll- och frysta ROM-bevis > teknisk forskning. [G1](G1_COMPLETION_RECEIPT_2026-11-17.md) är avslutad, [G2](G2_COMPLETION_RECEIPT_AND_FEASIBILITY_BOUNDARY_2026-11-17.md) bevarar bytekontrollerade historiska original. **De exakta fyra v0.19 OPEN-rummatriserna är kandidater**, inte ny spelcanon; C02 är spårbar planerad v0.11-bas där R3 historiskt kördes. Den 8×9 TOP-DOWN-maskfil som används som teknisk jämförelse har SHA-bundna Git-blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`.

**Nya G3-leveranser:** [TIA ägarkarta](G3_TIA_OBJECT_OWNERSHIP_2026-11-17.csv), [per-cykel/colorclock-karta](G3_COLOR_CLOCK_DEADLINES_2026-11-17.csv), [CPU-/F6-budget](G3_CYCLE_AND_F6_BYTE_LEDGER_2026-11-17.csv), [RAM/F6/stack/blanking](G3_RIOT_STACK_F6_AND_BLANK_SCHEDULER_2026-11-17.md), [R1–R4 scenstress](G3_R1_R4_MAX_STRESS_MATRIX_2026-11-17.csv). Varje tal är märkt **historiskt Stella-rapporterat**, **fryst källkod**, **villkorlig beräkning**, **framtida hypotes** eller **inte mätt**.

## 1. Varför R1–R4 måste vara ett enda resurskontrakt
| Scen | Logiska objekt som måste samverka på kritiskt Y | Särskilt fysiskt problem | Evidens hittills |
|---|---|---|---|
| **R1/C01/C04** | 6 individuellt numeriska X/Y vita original-NPC M,M,F,F,SM,SF + fullstor gul P0-spelare + aktiv M0-projektil + brunt PF | **7 fulla 8-bitars människor på bara 2 TIA playerströmmar**, plus M0 delar P0-färg; varierande X-ordning och samma/angränsande nio raders höjd | F9 3 binära X på en P1; R1g 3 statiska P1 + en 4-läges P0; båda **andra ROM** |
| **R2/C02/O1** | 5 vita NPC + guldnyckel + gul P0 + M0 + brunt PF | Nyckelns guld och hål kräver ytterligare färg/mask, får inte flyttas logiskt under androidskymning | Inga integrerade positiva bevis med 5 NPC; key/door former ej slutliga TIA-bitmapbeslut |
| **R3/D01–D03** | Vänster yttervägg alltid fast, enda högra öppning x39 y9–12; orange markör + svart nyckelhål; samtidigt kan R1/R2-objekt stå på dessa rasterrader | Isolerad R3 använder **P1 för orange/black-transparent door** samtidigt som R1 P1 används för vita NPC; sex PF-skrivhändelser + P1 runt c62 | R3 local historiska TIA-traps, källestimerad worst line **74/76**; ingen integrerad R1/R3 |
| **R4** | Alla ovan i ordningsväxling, Y-skift och 600 på varandra följande bildrutor | X/Y-eventsort, START-/GRP-latch, färg-/PF-deadline, identifierbar mask, deterministisk key-occlusion | Inget fullständigt R4/independent E02 |

**Varning:** vi kräver inte att "sex NPC plus nyckel" ritas i samma R2-scen: R1 har sex, R2 har fem och nyckel. Vi kräver däremot att **fem+nyckel** inte av misstag räknas som en gratis extra TIA-kanal. Kart-/högerdörrsintegration får inte anta att spelaren/NPC aldrig befinner sig i samma Y-zon som dörren.

## 2. Hårdvarufakta: antal, färgkoppling, gränser
- NTSC en rasterrad: **228 TIA-colorclocks / 76 CPU-cykler; 68 CC HBLANK +160 synliga CC**, 3 CC per CPU-cykel. Ett register `STA` skrivs vid sin effektiva CPU-slutcykel, men själva **internt renderade START-/kopielatch-tidpunkten** har egen offset. `Scn Cycle=c` och nominellt `3c` är **inte** fullständigt bevisad TIA-START.
- Två 8bitars spelare **P0/P1** (med NUSIZ-repetition), enbitsmissiler **M0/M1**, enbitsball **BL**, och grovkornigt PF (40 horisontella bitar, normalt 4 CC/bit). PF kan inte godtyckligt återskapa alla fyra 8x9-små originalhumanoider på 1CC-nivå.
- Fyra färgregistersströmmar: **`COLUP0` färgar P0 OCH M0**, **`COLUP1` P1 OCH M1**, **`COLUPF` PF OCH BL**, och `COLUBK` bakgrunden. De delade färgerna är per faktiskt bildpixelmoment; registerbyte gäller båda inom samma colorclock, inte separata "objektfärger". **Gult M0 i forsknings- och regressionstest är historisk testfärg, inte ett självständigt nytt användarbeslut om slutskottets exakta palettkod.**
- `CTRLPF` score-mode skulle kunna använda P0/P1-färger för PF-halvor och därmed bryta kravet på bruna väggar; det är ingen fri guldnyckel-/hudkanal. `REFP0/REFP1` är horisontell spegling, INTE vertikal reparation av R1ba.
- `NUSIZ` autokopior har hårdvarubundna avstånd; `RESP0/RESP1` kan återutlösa en spelare men måste undvika att kapa föregående aktiva renderfönster; `VDEL` kan flytta graphics-latch till annan rad men gör inte fler samtidiga P1-kopior; `HMOVE` justerar objektets positionsräknare, inte varje auto-kopia oberoende. Extra 4KB F6-bank innebär **inte** mer TIA eller 128B RAM.

Källor: [Atari Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html), [Andrew Towers TIA Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), **versionspinnad historiskt använd Stella 6.7.1** [Player.cxx](https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/tia/Player.cxx), [DrawCounterDecodes.cxx](https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx), [CartF6.cxx](https://raw.githubusercontent.com/stella-emu/stella/6.7.1/src/emucore/CartF6.cxx).

## 3. Den förstklassiga nya G3-observationen: en konkret P0/M0-färgkonflikt
**Fysisk samtidighet är ANNAN dimension än CPU-budget.** I en tänkt, källoriginal-rättvänd R1-scen ritas **stor manlig vit android** på P0 med maskrad **3 = `11111111`** (TOP-DOWN) vid synliga färgklockor X40..47. Föreställ aktiv M0-projektil med önskat gult pixelspann X43..44 på samma rad, en gul P0-spelare på annat X, och bruna PF-väggar.

Vid **CC43** behöver *denna konkreta allokering* samtidigt `COLUP0=vit` för vit P0-mask och `COLUP0=gul` för M0. **En fysisk COLUP0 kan inte ha två värden vid samma färgklocka.** Även om en källrad har 30 lediga CPU-cykler är detta en simultan register-/färgkonflikt. Den kan bara undvikas om *någon* pixel flyttas till en annan legitim renderingskanal, en annan fysisk presentation/occlusion definieras eller testkravet ändras genom explicit auktoriserat beslut.

**EXAKT BEGRÄNSNING:** Det är en **villkorlig motexempelscen för den utpekade P0-vit+M0-gul-allokeringen**, **INTE** ett universellt omöjlighetsbevis för alla tänkbara TIA-kernlar (annan P1/PF-användning, CPU-fas eller visuellt godkänd occlusion kan eventuellt lösa just den). Ingen ny Stella-bild har producerats och G3 har ingen rätt att hävda en generell TIA-no-go.

**Forskningens verkliga lucka:** R1g:s M0-testobjekt ritades **rasterraden före hela NPC-9-radersbandet**, vilket *undviker* just G3:s samtidigt vit/gul skottproblem; R1f gjorde likadant. Att 600/600 bilder varit riktiga ändrar inte att korskombinationen aldrig prövats. **G4 skall börja med den här konflikttypen**, inte ännu ett enkelt fjärde-X-läge.

## 4. Egentliga CPU- och fysiska deadlines – vad vi vet och INTE vet

### 4.1 F10:s P1-ensam-fördelning är en UNDRE, villkorlig gräns
Den frysta F10-modellen med sex unika separata P1-kopior, statisk gul P0 och statisk M0 räknar:
`6×STA RESP1=18` + `6×STA GRP1=18` + `6×LDA #maskbyte=12` + `LDA/STA GRP0=5` + `LDA/STA ENAM0=5` + `STA WSYNC=3` = **61/76 CPU-cykler**. Bara **15** finns kvar, före numeriskt X/Y, aktörssortering, dynamisk Y-bytehämtning, händelseväntan, PF, färgändringar och key/door. Bytehämtning från RAM i stället för immediate ger typiskt **67/76**, tabelluppslag runt **73/76**, fortfarande utan de utelämnade kraven. Dessa är **hypotetisk F10-P1-only-stil**, inte nedre gränsen för ALLA framtida adaptiva P0/P1-alternativ.

Om samma rad också måste göra **sex separata PF-registerskrivningar** minst `6×3=18` *ytterligare* direkta TIA STA för dessa PF-värden blir den obearbetade schematiska summan **61+18=79/76**, trots att mask-/PF-byte redan måste vara korrekt förberedda. Om varje PF kräver eget `LDA #data; STA PFx` blir **61+30=91/76**. Detta **falsifierar append-only-varianten som måste skriva alla sex PF på samma rad**, inte en design som kan låta PF ligga kvar, sprida skriverier mellan band eller använda annan teknisk kernel. Varken 79 eller 91 är faktisk Stella-körning för ett nytt program.

### 4.2 F9 kan inte vara en genväg till en integrerad kernel
Fryst F9: M `RESP1 c21/23 → GRP1 c24/26`, F `RESP1 c32/33 → GRP1 c35/36`, SM `RESP1 c48/50 → GRP1 c51/53`; källschemats sista rad `WSYNC c57/c59`, vilket innebär högst **17 CPU-cykler** tidsrest före 76 i *denna* inkrementella modell. Det är åtta förkompilerade modekernlar med **tre enbitars separata RAM-X** (144 historiskt råverifierade korrekta frames); ingen dynamisk allmän sex-NPC-kernel.

Sex extra minimala PF-`STA` =18 överstiger append-only-marginalen 17. Efter `WSYNC` kan inga extra rasterinstruktioner "läggas på" i den raden; riktig integration måste **omforma och tidigarelägga** befintliga händelser. F9:s `c` är frysta schema-/Stella-trappunkter, inte bevis att alla interna player-START-ögonblick har modellerats.

### 4.3 R3:s exakta tidigare TIA-traps – en ANNAN ROM
I det [frysta R3/C02-försöket](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md), på historiskt fångad Stella 6.7.1 **frame90, scanline134**, har `PF0_LEFT c7`, `PF1_LEFT c15`, `PF2_LEFT c22`, `PF0_RIGHT c37`, `PF1_RIGHT c45`, `PF2_RIGHT c52`, orange P1-dörr `GRP1 c62`. Den historiska R3-källans worst-case sista rad cirka **74/76 CPU-cykler**; bara 2 kvar i det specifika schemat.

- F9 behöver vita P1 `GRP1` runt c35/36, c51/53 medan R3 skriver höger-PF c37 och c52. Samma CPU kan inte göra två oberoende `STA` på en och samma c, utan en ny instruction scheduling och bibehållna pixeldeadlines.
- R3:s P1 orange-/transparent svarta dörrdel använder redan **samma P1/GRP1/COLUP1** som flera vita NPC i R1/F9, så inte ens en 76-cykelvinst bevisar att båda bitmapströmmarna får korrekt start/latch och färg.
- Det svarta hålet i den historiska R3-lösningen är transparent mask som avslöjar svart bakgrund; om PF fortfarande är brun bakom "hålet" blir det brunt. `PF`-geometri och P1-dörr måste alltså planeras *tillsammans*.
- `74 + 3 =77` visar att man inte ens kan klistra på en extra `STA zp` efter samma R3-worst-row-exit utan att omdesigna. **Detta är INTE en fysikbevisad gräns för all R3-integration**.

**INGA av ovanstående F9-, F10- och R3-scheman är samma ROM.** G3 räknar deras konflikter och registerlivstider, **inte** en adderad, genomförbar "kombination".

## 5. Y-konflikten är även bevisad av originalmaskernas byte
De godkända diagnostiska 8×9-mönstren är TOP-DOWN enligt [NPC_REFERENCE](../../design/NPC_REFERENCE_8x9_masks.json). **SM och SF har tomma rader 0,1,8, men dessa rader ingår fortfarande i 9-raders geometrin.**

Välj sex separata start-Y `[96,97,98,99,100,101]`, ordning `M,M,F,F,SM,SF`. En enkel **källbyte-beräkning, INTE Stella-prov**, visar på rasterlinjer:
- y101: sex logiska 9-radersband aktiva, men bara **fyra** icke-tomma källmaskrader;
- y102: sex logiskt aktiva, **fem** icke-tomma;
- **y103 och y104: alla SEX har icke-tomma bitmaprader** samtidigt;
- y105: fem logiska och fem icke-tomma.

Därmed kan inte "sprid Y-positionerna lite" antas ge lätt last i allmänhet. G3:s 23-scenmatris innehåller även de exakta sex bitmapbyten på y100–104, plus SAME-Y-täta `X=[40,44,48,52,56,60]`, där individuell identitet kontra faktisk slutlig vit pixelunion är en separat ännu oavgjord visuell acceptansfråga. **O1-occlusion gäller nyckeln under android, inte automatiskt två samtidiga vitvita NPC-överlagringar.**

## 6. 128B RIOT, aktiv 4KiB standard-F6-bank och blankning
Se [det detaljerade RAM-/bankkontraktet](G3_RIOT_STACK_F6_AND_BLANK_SCHEDULER_2026-11-17.md). Kärnresultat:
- Endast sex numeriska (X,Y) = **12 byte**. F10:s illustrativa fulla diagnostikbudget blir **117/128 inklusive 24 bytes stackreserv**, vilket lämnar 11 *teoretiskt*. Det finns ingen verklig assembler-allokering eller uppmätt stack-high-water för full R1.
- Naiv lagring av `6×9=54` maskbyte +54 färdiga per-rad händelsetider +12 koordinatbyte +24 stackbytes = **144**, alltså redan 16 över 128 innan övriga objekt. En **rullande** händelsekö/blanking-precompute behövs i så fall.
- F9:s aktiva bank: **3019 program +115 tabeller +6 vektorer =3140/4096**, nominellt 956 byte kvar; säkert 952 med hotspotmarginal enligt F10. R3:s helt andra ROM genererar **6×176 PF-tabellbytes +176 keyhole-bytes =1232 bytes**. Ren `3140+1232=4372` överstiger **en** aktiv bank med **276 bytes** men betyder inte att en optimerad kombinerad layout är omöjlig: annan bank, tabellkompression eller omskrivning kan hjälpa *lagringen*, inte TIA-cyklerna.
- Bankbyte via `$1FF6..$1FF9` omdisponerar kod mellan **fyra ×4096**. Bankbyte kostar exekveringsinstruktioner och kräver säker mål-PC/trampolin; inte ett sätt att få sex samtidiga spritekanaler.
- Vilande `VBLANK/overscan` kan utnyttjas för X-/Y-sort, per-rad mask-/PF-händelsekompilering i begränsad RAM. Men `70×76=5320` brutto CPU-cykler per typiskt NTSC-frame är INTE allokerade enbart till det – timer/input/VSYNC/gameplay tar också tid. **Ingen aktuell sourceplan visar att sex data-driven X/Y kan exekveras i rätt fysiska fas.**

## 7. Vilka av de 30 originaltricken hjälper G3 – och var gränsen går
| Trick | Relevant, användbart | Vad det INTE löser utan nytt bevis |
|---|---|---|
| **01 Sprite Multiplexing, 02 Mid-Scanline GRP Writes, 15 NUSIZ Copy Modes** | Starkast faktiska mikro-P1/P0-kopior (F9 3; R1g 4 begränsade) | Sex numeriskt oberoende X/Y, tillfälligt tät 8-CC-kollision, P0-sortkorsning |
| **09 Vertical Delay, 10 HMOVE, 24 Precomputed Cycle-Exact Kernels** | Minska viss deadline-/maskhämtkostnad, finjustera hel P0/P1-position | Ingen ny oberoende TIA-kopia eller extra dynamisk tid; kontrollera R1ba orientering |
| **07 Asymmetric PF, 19 Priority** | R3 tekniska högerdörren, O1 möjliga skymning/visuell prioritet | Löser inte vit P1 + orange P1 samtidigt eller guldnyckelns logiska X/Y |
| **14 Multiple Kernels, 21 RIOT Timer** | Olika y-zoner/bankar och blanking-dataplanning | Kritisk same-Y-rad måste fortfarande uppfylla 76 CPU/korrekta effektiva deadlines |
| **03 Venetian Blinds, 04 Flickering, 08 Two-Line Kernel** | Diagnostiska kontrollidéer | Förlorade/mellanlagda masker, 10 Hz-android eller saknade ursprungliga nio rader är INTE godkänt |
| **17 Missile/Ball Reuse, 18 PF Score Mode** | Stöd och färgtrick i begränsade zoner | M0 upptagen av skott, M1/BL enbitars, delade färger med P1/PF, bruna väggar |
| **27–30 SCABS/F6SC/DPC/DPC+/CDF** | Kan vara framtida separata formatstudier efter explicit användarbeslut | **Inte** inom standard-F6 och tillför inte TIA playerströmmar; kan inte tyst ingå |

**Endast ursprungliga 30 numrerade trick räknas som 30.** Atlasens 52 mönster och 67 riskposter är stöd, INTE 52 ytterligare "trick".

## 8. G3-beslut: Plan A, B och C – vad nästa analys bör försöka lösa

### Plan A – rekommenderad source-only huvudväg (INTE en kodplan som redan fungerar)
- **Mixed P0/P1 actor scheduler**, med F9:s P1 tre-masker som begränsad positiv fysikreferens och R1f/R1g:s dubbla P0 `RESP0`/gul-vit som en annan positiv fysikreferens. Båda måste omräknas till EN verklig dynamisk register-/mask-/färgsekvens, inte sömmas ihop som separata binärdelar.
- Sex permanenta NPC-ID med individuella numeriska X/Y; sortera händelser i blankning, rullande radmask/händelsebuffer, källa-/maskfel som R1ba förbjuds. Varje renderad rad kontrolleras både för **76c sum** och `RESP/GRP/COLUPx/NUSIZ/PF`-effekter vid avsedda **fysiska färgklockor**.
- **PF förbereds på y-zongränser** endast där faktiskt kartdata är konstant, inte som generell waiver för väggar. Reservera R2 guldkey + R3 P1 orange/black och same-Y-M0 redan i registerägarkontraktet.
- Ta fram **en** G4 SOURCE-ONLY minsta P0/player↔vit-original korsningsplan med M0 på samma Y, minst två P1 original, och brun PF. Det är en fysisk hypotes att bedöma, **inte** redan förregistrerad exekverbar ROM.

### Plan B – om A:s första schema saknar fysisk timingmarginal
- Utvärdera EN alternativ, konkret `NUSIZ0/1`-/`HMOVE`-/`VDEL`-arbetsordning för P0/P1 med samma **verkliga input-data**, inte ännu fler hårdkodade fjärde-X-lägen. Låt PF ligga kvar på rader med konstant geometri och använd olika zonkernlar där korrekt mask/Y tillåter. Skild roll/P1 door-fönster måste ändå vara förenligt med aktiva vit-NPC på samma rasterrader.
- Standard-F6 annan aktiv bank kan organisera färre kodduplikat med säker banktrampolin i VBLANK, men **är sekundär till fysikskrivsekvensen**. Ett test av bara fler banker skulle inte avgöra R1.
- Om nyckel, BL, M1 eller PF föreslås som alternativ ritkanal måste maskens hela bit-/färgpresentation och bruna väggar **källkontrolleras**. Ingen tyst ersättning av 8bitars humanoider med PF eller 1bitars missile.

### Plan C – hårt stopp eller användarbeslut
- Om samma P0/M0 colorclock kräver skilda färger utan en annan renderingsägare i **konkret** scenario, eller `RESP/GRP` START omtriggning kapar rättvänd originalbitmap, redovisa `NO_GO_FOR_THIS_EVENT_ALLOCATION` och minimalt motexempel, inte en universell omöjlighetssats.
- Om 76c/128B/4KiB spräcks även efter dokumenterad kompression och korrekt per-rad deadlineplan, lämna `INCONCLUSIVE/NO_GO_SOURCE_ONLY`, behåll FULL R1 BLOCKED och ge användaren högst två **uttryckliga** möjliga kompromissförslag om det till slut behövs i G5.
- **Ingen** designwaiver, F12, ny ROM/Stella, annan mapper, PAL, gameplay, PR7-merge eller E02 genom G3.

## 9. Matrisens pass/fail och rekommenderat nästa beslut
G3:s planeringsgrind bedöms på **korrekt komplett ägarskap och transparens om det som saknas**, inte på ännu icke existerande fungerande sex-NPC-kod.

| Kontrollpunkt | G3-källresultat |
|---|---|
| Aktörantal och original TOP-DOWN, R1–R4 scenkrav | **TRACE PASS:** 23 stresstest inklusive y103/104 sex icke-tomma maskrader |
| TIA objekt och alla färgkopplingar | **CONTRACT PASS:** ägarkarta R1/R2/R3/R4 och konkret P0/M0 kollisionsvittne |
| Source-pinnade F9 och R3 CPU-/PF-/GRP-event | **EVIDENCE CLASSIFIED:** historiska c21..59 respektive R3 c7..62, inte en ny integrerad mätning |
| P1-only F10 lower bound, ny PF-append och R3 naiv append | **ARITHMETIC PASS:** 61/76, +6PF min→79, R3 c74+3→77; **gäller endast angivna källschema** |
| F6 aktiv 4K och 128B + stack | **CONTRACT PASS:** 117B hypotetisk budget och 144B naiv fail, bankresidens separat |
| Fysiskt korrekt P0↔vit-NPC crossed X i båda ordningarna | **UNPROVEN – G4 SOURCE QUESTION** |
| Same-Y aktiv M0 gul färg när P0 vit renderas | **UNPROVEN/HARD COLOUR CONFLICT IN CURRENT P0 ASSIGNMENT** |
| Alla sex numeriskt oberoende X/Y, källkorrekta maskrader | **NOT PROVEN – FULL R1 BLOCKED** |
| R2 guldkey/O1 och R3 orange svart i SAMMA integrerade kernel | **NOT PROVEN – R2/R3 INTEGRATION BLOCKED** |
| E02 oberoende körbar verifiering | **NOT RUN – rätt verifieringsroll får senare egen order** |

**Slutligt G3-beslut:** `G3_SOURCE_ONLY_RESOURCE_CONTRACT_COMPLETE_WITH_UNPROVEN_PHYSICAL_SCHEDULE`. Nästa naturliga sak är **G4:s separata SOURCE-ONLY GO/NO-GO för EN minimalt falsifierbar fysisk P0/P1-M0-PF-hypotes**, inte en F11-repetition och inte G6-build. Om ingen konkret fysikplan för den minsta scenen är plausibel ska G4 säga NO-GO och föreslå stopp/G5-beslut, inte skapa generiska fler-ROM-svep.

## 10. Proveniens, integrationsregler och slutattest
- Detta G3 skapade **enbart** Markdown-/CSV-dokument på `main` med källhänvisningar. Ingen data från ett separat spelprojekt, ingen kod i `rom/`, ingen exekverad Stella, ingen senare implementation.
- [R1-F9 rapport (fryst commit)](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md), [R1-F10 source (fryst)](https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md), [R1-F11 source G0 FAIL (fryst)](https://github.com/Odourman/let-me-out/blob/dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F11.md).
- [R1g 600 (R1 mixed-channel but 4 special positions)](https://github.com/Odourman/let-me-out/blob/research/main-ii-r1g-four-X-dynamic-600-20261116/docs/MAIN_II_R1G_FOUR_X_DYNAMIC_600_STELLA_LOCAL_PASS_2026-11-16.md), [R3 historisk originalrapport med faktisk PF-/P1-traps](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md), [G2 16-bevisregister](G2_EVIDENCE_LEDGER_2026-11-17.csv).
- MAIN VI:s signatur avser källgranskning och projektledning. VERIFICATION II:s oberoende underskrift kan aldrig ersättas av en positiv MAIN-studie. **G4 har inte påbörjats.**
