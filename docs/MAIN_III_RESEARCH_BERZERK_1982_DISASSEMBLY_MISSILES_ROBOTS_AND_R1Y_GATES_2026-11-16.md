# LET ME OUT! – Berzerk (Atari 2600, 1982), originalkodsdisassembly och skott-/spritearkitektur

**Datum 2026-11-16. Research only.** Ingen ändring av produktions-`main`, ROM DEVELOPMENT:s draft-PR #7 eller organisatoriskt fristående VERIFICATION. R1/R2–R4 fortsatt blockerade. En angränsande isolerad skottrutekandidat R1z testas separat. 

## Primär kodkälla och status

En fullständig kommenterad 6502-disassembly som själv anger **copyright Atari 1982, programmerare Dan Hitchens**, analyserad och kommenterad av **Dennis Debro (senast 2004-12-29)** har faktiskt öppnats och sökts igenom i GitHub:

**Fast primärkälla:** [Berzerk source at exact GitHub commit 480a5287 – berzerk.asm](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm) (blob SHA `e00c50a718d96ffcbfa4e6270c87a037d2758cf3`, 104 967 texttecken). Originalnoterna hänvisar till [qotile.net minidig](https://www.qotile.net/minidig/disassembly/berzerk.asm); arkivet klassificerar detta som *rekonstruerad* källkod avsedd att bygga exakt original-ROM. **Det är inte Hitchens upphittade originalfiler.** Vi har inte själv verifierat byteidentisk rekonstruktion med en separat dump. Ingen tredjepartskod har kopierats till vårt spel.

Författarens egen prolog beskriver `.skipDraw`-liknande villkorade spritegränser, NTSC/PAL-fördröjningsanpassningar och opålitlig identifiering av vissa RAM-alias/flaggar. Därför ska namngivna symboler användas som rekonstruktörens tolkningar, inte som säker ursprungsdesigncanon.

## Verifierade kodfakta (källradnummer)

### 1. Två riktiga missiler med separata RAM-tillstånd

**Rader 303–315** innehåller tydligt separata variabler: `playerMissilePointer`, `playerMissileFlightTime`, `playerMissileDirection`, `playerMissileHorizPos`, `playerMissileVertPos` respektive `robotMissilePointer`, `robotMissileDirection`, `robotMissileDelay`, `robotMissileFlightTime`, `robotMissileHorizPos`, `robotMissileVertPos`.

**Rader 900–979**: vid `INPT4` på knapptryck och när ingen tidigare spelares missil är aktiv sätts `playerMissileFlightTime` och skottriktning. Första X/Y beräknas från spelarens X/Y samt `InitMissileXOffsetTable`/`InitMissileYOffsetTable` (hand/vapen-offset). Mellan frames uppdateras `playerMissileHorizPos` och `playerMissileVertPos` utifrån riktningen och `HorizontalPixelOffsets`/`VerticalPixelOffsets`. Det här är **logiskt rörligt skott**, till skillnad från våra hittills frame-fasade åtta-X-forsknings-ROM.

**Rader 1490–1562**: roboternas skott får helt separat position, riktning, fartreglage, pointer och ljud. Spelet använder **M0 för spelarprojektil och M1 för robotskott**.

### 2. Separera projektilens X och dess scanline-baserade synlighet

**Rader 2958–2989**: `DetermineDiv15Position` beräknar coarse X-delen i intervall om 15 TIA-color-clocks och fine HMOVE-nibble; `MoveObjectHorizontally` skriver `HMP0,x` och `RESP0,x` i en separat blankningsscanline. Det kan riktas till objekt 0 P0, 2 M0, 3 M1 genom `X` (se användningar **1031–1033** och **1562–1566**).

**Rader 945–980**: missilens Y styr inte var den går horisontellt; det styr en beräknad läspekare till en redan befintlig ROM-datatabell. `playerMissilePointer` byggs av `MazePF0Data+90 - playerMissileVertPos` och eventuellt ett höjdoffset för horisontellt skott.

**Rader 405–406, 467–468, 545–546**: `LDA (playerMissilePointer),Y` och `STA ENAM0` exekveras **per rasterrad** (separate kernel exits). Robotens motsvarighet `LDA (robotMissilePointer),Y; STA ENAM1` finns på rader **438–439, 448–449, 493–494**.

**Rader 2184–2281**: samma `MazePF0Data` innehåller övervägande `$20` (TIA ENAM0 bit1=0), men även byte som `$2F` (bit1=1), så datan kan på ett mycket kompakt sätt **återanvändas som en vertikal on/off-bild för missilens grafikhöjd**. Detta är ett viktigt, faktiskt bevisat originalspelsmönster: *data pointer + scanline index + TIA ENAM enable*, utan extra separat spelarskottsbitmap. En genomgång av just ROM-dataalignment i DASM/NTSC behövs innan man tar över detta slags tabellreuse.

### 3. Berzerk slipper vår specifika M0-dubblering genom annan P0-strategi

**Rader 964–977**: `LDA #ONE_COPY; STA NUSIZ0` vid den ordinarie spelarrutinen; för horisontell missil ändras bara översta storleksbitar till `MSBL_SIZE4` (d.v.s. bredd men fortfarande en P0-kopia). `NUSIZ1` ställs till robotmissilbredd `MSBL_SIZE4` i koden rader 1498–1502. I **score-kerneln**, separat från gameplay, använder Berzerk `THREE_COPIES` (rader 589–651) för att visa siffrorna. Det är alltså **inte** en allmän regel att spelet alltid bara har en kopia, utan den relevanta skillnaden gäller gameplay.

Vår R1n–R1y använder **`NUSIZ0=$02` (två vida P0-kopior)** för att hinna rita flera P0-figurer på **samma** rasterrad. Det duplicerar M0 automatiskt på ett senare X om `ENAM0` inte hinner släckas. Berzerks en-kopia-under-gameplay undviker denna särskilda M0-duplicate-situation. Men att rakt av skriva `NUSIZ0=ONE_COPY` i vår kernel skulle sannolikt förstöra våra redan godkända P0-kopior. Det är **inte** rekommenderat som en oprövad produktionsfix.

### 4. Robotar på olika vertikala rastersektioner

**Rader 429–526**: robotgrafik går via `GRP1`, `RESP1`, `HMP1`, `robotPointers[x]`, `robotVertPos[x]` och `kernelSection`. Koden väljer särskild coarse-X-slinga för höger/vänster rastersektor. Den kan flytta **vilken** robot som visas när rasterlinjen har passerat den föregående figurens vertikala område. `MAX_ROBOTS=8` (rader 198–216) betyder alltså *åtta logiska robotar*, inte åtta samtidiga TIA-players eller åtta på samma Y.

I våra R1-tester står de fem ursprungsandroidinstanserna samtidigt på **samma 14 visade rasterrader**, och de sex som kravbilden vill ha ska vara självständigt rörliga. Berzerks vertikala trick löser inte automatiskt detta. Att byta till Berzerks generella grafikkernel kan inte göras utan separat designauktorisation.

### 5. Hårdvarukollision, avstånd och logisk robotindexering

**Rader 390–399 och 577–586**: rasterkoden läser `CXP1FB`, `CXM0P`, `CXPPMM`, `CXM1P` och sparar en status vid `playerCollisions,x` per `kernelSection`. **Rader 2113–2120** använder `playerCollisions+1,x` tillsammans med `robotAnimationIndex,x` för att initiera robotens dödsanimation. **Rader 775–818** använder `CXM0P`, `CXPPMM`, `CXM0FB` och gränskontroller för att avsluta aktiv spelarprojektil. **`CXCLR` utförs också vid framesynk rader ca 1700**.

Detta visar ett praktiskt sätt att översätta TIA-kollisioner till fiendsektioner och handling i RAM; det är **inte** ett löfte om att `CXM0P` på egen hand identifierar vilken av flera P1-kopior på samma rasterlinje som träffats. TIA-latchar är ackumulerande mellan `CXCLR`-skrivningar, så sektionernas livstid och eventuell bakgrundskollision måste granskas före återbruk.

## R1y:s aktuella problem och vilka idéer som är relevanta

Senast **godkänd** isolerad bas **R1x**: **600/600 riktiga Stella frames** med M0 x268..282, 5 originalmask-NPC, fyra diskreta fjärde-X, 2 dörrtillstånd, korrekt NTSC, verklig hårdvarukontakt med den andra stora P1-kvinnan.

Senast underkänt **R1y**: **474/600**. 126 frames utan projektil i **fjärde NPC-läge D (GUI x378)** när M0 X=288..300. De andra tre NPC-X-lägena klarade alla skott-X. Endast 3 CPU-cykler `BIT FRAMELO` tillkom före `RESM0`; NPC-källmaskerna/rutinerna är identiska.

**Den Berzerk-inspirerade forskningsprioriteringen är att först försöka eliminera M0:s behov av extrem tidig avstängning**: R1z provar cykelneutral omordning av D:s P0-färg, `RESP0` och `ENAM0`. Om den gula M0-pixeln blir vit när `COLUP0` skrivs för tidigt ska **resultatet underkännas**, inte lösas genom att maskera bort pixeln i analysen.

Därefter, separat rådgivande designutforskning:
1. **Berzerk-skottets RAM-tillstånd och `DetermineDiv15Position`-algoritm** som grund för fullständig horisontell M0-positionering utan att addera instruktioner till vår hårt belastade synliga kernel; jobba först i isolerat forsknings-ROM, inte production.
2. **NUSIZ0-kopia kontra M0**: pröva **dynamisk NUSIZ0** endast om det kan bevisas i Stella att alla fem ursprungliga NPC-masker kvarstår på samma Y. Annars använd specialiserade kernel-window-varianter (#14).
3. **Vertical ENAM0 pointer**: förberäkna ON/OFF-radvärdet i VBLANK eller inarbeta en pixel-exakt remappning; Berzerks 8-cykels `LDA (ptr),Y; STA ENAM0` får inte sättas in i vår 76-cykels rad utan egen budgetanalys.
4. **CXM0P target-ID**: logisk collision-ID måste skilja på de två P1-kvinnorna och övriga återanvända P1-NPC; håll separata läges-/mask-/riktningstabeller och använd `CXM0P` som *hårdvarugrind*, inte som ensam fiendeidentifierare. För samma-Y-överlapp krävs mjukvarukontroll per logisk NPC.

**Forskningen är rådgivande.** Ingen auktorisation av nya projektsteg, ingen ny designcanon, `main`/PR7/VERIFICATION issue8 orörda. Full R1 fortsatt FAIL/BLOCKED.
