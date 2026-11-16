# LET ME OUT! – Deep research: Berzerk + alla 30 ursprungliga Atari 2600-trick

**2026-11-16. Avsändare RESEARCH till MAIN. ADVISORY – ingen ändring av gameplaycanon eller implementationsscope.** Ingen formell oberoende VERIFICATION. F6/NTSC och originalmasker behandlas som krav, inte ändringsbara kompromisser.

## 0. Direkt svar

**Ja, vi kan inspireras kraftigt av Berzerk, men inte genom att kopiera dess visningskernel.** Berzerk separerar **logisk projektilposition och livstid** (RAM) från **vertikal ON/OFF via data-pointer** och **horizontal coarse+HMOVE** i blankning. Det löser flera problem på spellogiksnivå. Däremot använder Berzerk i vanligt gameplay `NUSIZ0=ONE_COPY` och multiplexar robot-P1 mellan **olika Y-sektioner**. Våra fem bevisade NPC-instansmasker ligger på **samma Y**, och vår P0 används med `NUSIZ0=$02` för kopior, inklusive gul player. Dessa är *mätbara arkitekturskillnader*, inte rena assembleroptimeringar.

**Två separata hårdvaruhinder kräver olika lösningar:**
1. **Rendering:** en enda M0 ska vara gul, synlig vid x286–300, inte dubbleras, samtidigt som alla ursprungliga vita/gula P0-masker överlever; varje scanline bara 76 CPU-cykler.
2. **Objektfrihet:** fem nu, sex krävs, alla sex logiska NPC:er måste kunna röra sig individuellt över X på samma Y. NUSIZ-fasta avstånd och 6507:s 2 hardware players ger inte automatiskt sex fri-X. Detta är **en separat R1-blockerare**.

## 1. Evidens som inte får blandas ihop

| Isolerad forskningsprototyp | Strikt 600 äkta Stella frames | Vad bevisas/underkänns |
|---|---:|---|
| **R1x** [Actions #43847949395](https://github.com/Odourman/let-me-out/actions/runs/43847949395) | **600 PASS** | 5 hela original-NPC-maskinstanser i 14-radvisning, fyra fjärde-P0-X, båda dörrlägen, **en gul M0 x268–282**, riktig `CXM0P` när andra stora P1-kvinnan träffas |
| **R1y** [Actions #43848364350](https://github.com/Odourman/let-me-out/actions/runs/43848364350) | **474 PASS, 126 FAIL** | M0 saknas i D/x378-läget på x288–300 för att `ENAM0` släcks för tidigt |
| **R1z** [Actions #43850116022](https://github.com/Odourman/let-me-out/actions/runs/43850116022) | **456 PASS, 144 FAIL** | senare avstängning räddar missil-enable men tidigare `COLUP0` vitfärgar M0; 108 extra vita pixlar |
| **R1aa** [Actions #43851081064](https://github.com/Odourman/let-me-out/actions/runs/43851081064) | **456 PASS, 144 FAIL** | `NUSIZ0=ONE_COPY` på D-raden räddar **600 gula M0**, men utan återställning förlorar efterföljande P0/NPC-rader kopior; 2 628 vita ghost-pixlar och felmasker |
| **R1ab** [Actions #43852230740](https://github.com/Odourman/let-me-out/actions/runs/43852230740) | **PÅGÅENDE – resultat inte känt i denna anteckningsversion** | exakt registeråterställning `NUSIZ0=$02` vid beräknad 76-cykelsgräns med särskild första efterföljande D-rad; strikt audit utan ändrat maskkrav |

OBS: detta är *lokala research-pass* och fail-closed emulatortester, inte independent VERIFICATION. R1x är sista fullt PASS, men **full R1 är fortfarande FAIL/BLOCKED**.

## 2. Alla 30 ursprungliga trick – beslutsmatris

Index och namn följer **exakt** befintliga `LET_ME_OUT_30_URSPRUNGLIGA_ATARI_TRICK_MAIN_2026-11-16(3).md` (30, inte 52 eller 82). Tabellen är en *ny analys av deras praktiska betydelse efter R1x–R1aa*, inte en ersättning av originalbilagan.

| Nr | Trick | Nästa användning / risk |
|---:|---|---|
| **01** | Sprite Multiplexing | **Research hög för sex-NPC**, men Berzerks Y-multiplex fungerar ej automatiskt när alla sex står på samma Y. |
| **02** | Mid-scanline GRP Rewriting | **Kritisk**: registerwrites kan servera olika godkända masks före varje fysisk sprite-copy. Får inte bara öka pixelmaskfel. |
| **03** | Venetian Blinds | **Ej förnyad utan nytt maskbevarande bevis**: 9-/18-/VDEL-varianter tidigare FAIL; begränsad originalradupplösning. |
| **04** | Sprite Flickering | **Nedprioriterad**: sexfasprov gav 100/600 synlighet per NPC, 10 Hz effektivt; uppfyller inte samma-bild-kravet. |
| **05** | Dynamic Playfield Sprites | Reservväg för enkla detaljer, **inte** 8-pixel-originella människosilhuetter med PF-vägg och dörr i samma kanal. |
| **06** | Mid-frame Sprite Resizing | Inte relevant för fem/sexfri-X eller missilens rätta färg; risk maskdeformation. |
| **07** | Asymmetric Playfield | Rätt teknik för högersidig dörr + vänster yttervägg; **inte** lösning på M0/P0-konflikten. |
| **08** | Two-Line Kernel | **Sekundär kandidat** ihop med #09: skapa mer instruktionstid utan att förlora ursprungliga 8×9-maskernas synliga mönster; kräver nytt auditupplägg. |
| **09** | VDEL / Delayed Graphics | **Sekundär kandidat**: latch kan schemalägga GRP-buffertar, men är ingen tredje sprite; tidigare 9-raders test FAIL. |
| **10** | HMOVE Fine Positioning | **Redan bevisad** i R1t–R1x för närliggande åtta X-lägen; behövs ihop med grovpositionering för hela spelplanen. |
| **11** | Late HMOVE Trick | Låg, timingartefakter/hårdvaruvariation; löser inte strömbit, färg, antal kopior. |
| **12** | Raster Color Changes | **Kritisk konfliktyta**: `COLUP0` färgar M0 **och** P0. R1z FAIL visar denna begränsning konkret. Kan användas för kontrollerat färgbyte, inte vid fel tidpunkt. |
| **13** | 48-Pixel / Six-Digit Score Kernel | Idé om hårt schemalagda GRP-latchar, men fast geometri och HUD, inte sex oberoende godtyckliga X. |
| **14** | Multiple Display Kernels | **Högst prioritet för full M0-räckvidd**: välj kernel efter projektilens horisontella region/fjärde P0-X, VBLANK gör uppdelning och förberedelser. |
| **15** | NUSIZ Sprite Duplication | **Dubbel roll**: ger våra P0-kopior men duplicerar samtidigt M0. R1aa visar att ONE_COPY på specialraden ger rätt missil men kan förstöra maskerna efteråt. **R1ab testar återställning på linjegräns.** |
| **16** | Sprite Reflection | ROM-sparande för spelarriktning efter maskgodkännande; löser inte skottposition eller antal figurer. |
| **17** | Missile and Ball Reuse | Färsk alternativhypotes: prova M1/BL som projektillager; **M1 delar NUSIZ1/COLUP1 med vita P1**, BL delar färg med PF-vägg. Ingen godkänd drop-in-ersättning. |
| **18** | Playfield Score Mode | Låg: fler PF-halvfärger men delar P0/P1-färg, kan förvärra färgkonflikten. |
| **19** | Playfield Priority Switching | Stöd för korrekt vägg-/nyckelskymning senare, inte logisk target-ID eller M0:s färg. |
| **20** | Hardware Collision Latches | **Delbevisad R1w/R1x:** verklig `CXM0P` bit7 svarar på P1-kontakt. Men latchen ger **inte** logisk fiende-ID för flera P1 på samma Y. |
| **21** | RIOT Timer Scheduling | Bra för framebudget och stabil VBLANK/Overscan; **ger inte >76 CPU-cykler per synlig scanline**. |
| **22** | Stack/RAM Mirroring | Låg: RAM-överlägg när bullet-state behövs, men kräver strikt stackägar- och säkerhetsanalys; ingen fler sprite. |
| **23** | Undocumented 6502 Opcodes | Undvik tills all stabil officiell 6507-kod är uttömd; kompatibilitetsrisk. |
| **24** | Precomputed Tables and Cycle-Exact Kernels | **Högst prioritet** ihop med #14/#15: beräkna layout, X-regioner, registerdeadlines och färg-/maskfas innan skärmen börjar ritas. |
| **25** | Stack-Based TIA Register Tricks | Sista utväg för 1–2 cykler vid uppmätt brist; farlig stack- och busstiming, inte fri sprite. |
| **26** | Timing-Based Horizontal Scrolling | Ej relevant för statiska rummet / same-Y skott. |
| **27** | SCABS Automatic Bank Switching | **Utanför standard F6**, kräver ny cartridge; inte en extra TIA-player. |
| **28** | Extra Cart RAM / Superchip / Supercharger | **Utanför standard F6**, kan ge RAM för state men inte lösa pixeldeadlines eller spriteantal. |
| **29** | DPC Display Processor Chip | **Utanför F6**, snabbare datakällor men inte fler TIA-sprites. |
| **30** | DPC+ / CDF / ARM Coprocessors | **Utanför F6**, får inte antas vara auktoriserat; kan ändra beräkningskapacitet, inte TIA:s fysiska spritegeneratorer. |

## 3. Konkreta förslag, sorterade efter sannolik teknisk vinst

### A. En-kopietrick + SNABB ÅTERSTÄLLNING (mest direkt falsifierbart)

R1aa visar en gul M0 i alla 600 riktiga frames även i D, men 144 trasiga D-androidlägen på efterföljande rader. Hypotesen **R1ab** är att hålla `NUSIZ0=ONE_COPY` från D:s c53 bara till linjeslut, stänga `ENAM0`, samt sätta `NUSIZ0=$02` **exakt på nästa 76-cykelgräns**; därefter ritas nästa rad utan inledande `STA WSYNC`, via en separat första efterföljande D-kernel. 6502-matrisen ska pixeltestas i Stella. Även om detta reparerar nedre maskerna kan den *aktuella skottraden* ha förlorat en P0-kopia genom byte vid c53; sådana bitmapfel måste fortsätta vara FAIL.

**Stoppa här om R1ab FAIL:** vi har då ett direkt bevis för att minst en separat P0-rekonstruktion eller annan regionkernel behövs, inte en passande linjegränsfix.

### B. Skillnad mellan TIA:s fysiska missile-kopia och logiskt bullet-state

Kombinera Berzerks verkliga skott-RAM `x,y,direction,lifetime` och positionsrutiner med ett **val av rasterkernel i VBLANK**. Exempel på framtida registerschema:

1. Spelfysik flyttar bulletX/bulletY, kontrollerar aktivitet och bestämmer `region` och `fourthP0Mode`.
2. VBLANK beräknar grov `RESM0`-slinglängd + `HMM0` och väljer rätt förberedda korta registersekvenser (`#10 + #14 + #24`), utan löpande beslut på kritisk rasterrad.
3. Synliga raden måste ge EN gul M0 på exakt x/y, bevara samtliga originalbitmapmasker, undvika NUSIZ-kopior och leva inom c0..c76.
4. Efter bandet registreras `CXM0P` och övriga relevanta latchar; eventuell faktisk logisk NPC-ID/hitbox räknas från NPC X/Y och faktiska bitmaprader, inte enbart TIA-flagga.

Detta är en **forskningsarkitektur**, inte implementerad spelmekanik och inte ett tillstånd att ändra gameplay.

### C. R1-samordning för sex fria NPC är en separat feasibility gate

Ingen av #01–#30 ökar TIA:s inbyggda antal 8-bitars sprites: P0 och P1 är fortfarande två hårdvarugeneratorer, med avstånds- och tidsgaranti. Vi bör fortsätta mäta **två olika originalmasker vid självständigt varierande X på samma Y, med samtidig gul P0 player och gul single M0, utan blinkningar**. Därefter öka antal med helt oförändrat maskkrav; om två fria X är omöjligt under givna registerdeadlines måste MAIN göra ett eget separat design-/scopebeslut, inte försämra maskerna tyst eller kalla 5/6 PASS.

## 4. Externa kod- och hårdvarukällor

- **Berzerk 1982**, Dan Hitchens, rekonstruerad och kommenterad av Dennis Debro: [fast GitHub-commit 480a5287](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm). Specifika 6502-rader 390–510 (render), 900–980 (M0 spawn/förflyttning och NUSIZ0=ONE_COPY), 1490–1570 (robot M1), 2958–2995 (DivideBy15 och coarse+fine positionering), 2113–2120 (per-robot-kollision). Detta är **inte** bevis på att en kopierad Berzerk-kernel kan rita våra sex samma-Y-androids.
- [Stella Programmer's Guide, AtariAge](https://www.atariage.com/2600/programming/2600_101/docs/stella.html): NUSIZ0 styr både P0- och M0-kopior; COLUP0 styr deras gemensamma färg; ett scanline-rasterfönster har 76 CPU-cykler.
- Den ursprungliga 30-trick-bilagan `LET_ME_OUT_30_URSPRUNGLIGA_ATARI_TRICK_MAIN_2026-11-16(3).md`: numrering och tidigare bedömningar bibehållna.

**Integritet:** ingen ändring av `main`, ROM DEVELOPMENT draft PR #7, Verification issue #8, original-8×9-maskbytes eller gameplaycanon av RESEARCH. R1/R2–R4 fortsatt separata blockerade implementation-gates.
