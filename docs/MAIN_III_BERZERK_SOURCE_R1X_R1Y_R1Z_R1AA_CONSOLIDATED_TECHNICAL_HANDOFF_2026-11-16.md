# LET ME OUT! — Konsoliderad Berzerk-källanalys och skottgrind R1x→R1aa

**MAIN III / Research, 2026-11-16. STATUS: ADVISORY ONLY. Ingen produktionsimplementering, ingen slutlig VERIFICATION.** Alla källuppgifter från Berzerk nedan kommer från den faktiskt öppnade och kontrollerade rekonstruerade assemblerkällan: [Dan Hitchens' Berzerk 1982, kommenterad disassembly av Dennis Debro, fast SHA](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm) (Git-blob `e00c50a718d96ffcbfa4e6270c87a037d2758cf3`). **Det är inte originalutvecklarens bevarade källfiler och rekonstruktionens byteidentitet har inte kontrollerats här.**

## Vad Berzerk faktiskt gör

1. **Logiskt skott:** RAM-adresser för spelarens M0-X/Y, riktning, flight time, pointer (rader **303–310**); separat robotskott M1-X/Y/riktning/flight time/pointer (rader **311–315**).
2. **Eldknapp och spawn:** `INPT4` (rader **904–935**) sätter skottets X/Y från spelarens RAM-koordinater plus riktningstabeller, när ingen tidigare kulas flight time är aktiv. Berzerk har därmed en riktig projectile state machine.
3. **X-position:** `DetermineDiv15Position` (rader **2958–2978**) räknar coarse sektor i steg om 15 TIA-color clocks och HMOVE-finnibble. `MoveObjectHorizontally` (rader **2980–2991**) skriver `HMP0,x`, `RESP0,x` under egen blankningsrad. Anropas för M0 med X=2 och M1 med X=3.
4. **Y-aktivering utan kostsam byteklassning i varje synligt fönster:** `LDA (playerMissilePointer),Y; STA ENAM0` i den synliga kerneln (rader **405–406, 467–468, 545–546**). M1 motsvarande `robotMissilePointer` och `ENAM1`. `playerMissilePointer` är vertikalt positionerad i `MazePF0Data`-ROM (rader **945–980**), där bit1 i exempelvis `$2F` aktiverar missilen och `$20` inte gör det.
5. **Sprite-kopior:** I gameplay används `NUSIZ0=ONE_COPY` (rader **964–977**) vilket hindrar den NUSIZ0-bundna automatiska *andra M0-kopian*. Berzerk använder `THREE_COPIES` i separat **score kernel** (rader **589–651**) och missile-width-bitar separat för bredare skott. Detta är inte samma strategi som vår `NUSIZ0=$02`.
6. **Flera robotar via vertikal multiplex:** P1 `robotGraphics`, `RESP1`, `HMP1`, `kernelSection`, `robotPointers`, `robotVertPos` (rader **390–525**). Upp till åtta *logiska* robotar (`MAX_ROBOTS=8`), inte åtta P1-hårdvarusprites på en rasterlinje.
7. **Kollisionsgrind:** `CXM0P`, `CXM1P`, `CXP1FB`, `CXPPMM` läses i robotsektionerna och status sparas i `playerCollisions,x` (rader **390–399, 577–586**), vilket senare används vid robotdödsanimation (rader **2113–2120**). TIA collision latches är ackumulerande tills `CXCLR`; samma-Y flera kopior kräver fortfarande extra identifiering.

## Två samtidiga faktiska hinder i vårt spel

| Variant / Action | Villkor | Resultat | Teknisk slutsats |
|---|---|---|---|
| **R1x** [#43847949395](https://github.com/Odourman/let-me-out/actions/runs/43847949395) | M0 x268–282; 5 hela mask-NPC, fyra fjärde-X, två dörrar; verklig CXM0P över andra stora kvinnan | **600/600 PASS**, 64/64 tillstånd | Senaste strikt godkända referensen |
| **R1y** [#43848364350](https://github.com/Odourman/let-me-out/actions/runs/43848364350) | M0 x286–300, ursprunglig D-specialrad | **474/600 FAIL** | 126/144 D-frames saknar skott då M0 stängs vid c53 |
| **R1z** [#43850116022](https://github.com/Odourman/let-me-out/actions/runs/43850116022) | D-M0 off senare c59; D `COLUP0` vit tidigare c53; `RESP0` c56 oförändrad | **456/600 FAIL** | M0 fysiskt närvarande men **vit**, eftersom P0 och M0 delar COLUP0. 108 vita extrabildpunkter i 54 av D-frames. |
| **R1aa** [#43851081064](https://github.com/Odourman/let-me-out/actions/runs/43851081064) | Berzerk-en-kopieläge på D-skottraden `STY NUSIZ0` c53; avsluta M0 vid c71 med cykelneutral fall-through | **456/600 FAIL** | Alla **600 gula skott visas korrekt**; men 144 D-frames har skadad NPC-grafik då P0-kopieringsläget förblir ONE_COPY i senare rader. |

### Maskinellt uppmätt R1aa-effekt

600 äkta Stella-frames och 262 NTSC per frame bevaras, **600 av 600 exakta gula projektiler**, men D:s fjärde kvinnas x378-mask är inte längre igenkännbar under **144/144 D-frames**. R1aa förlorar totalt **7488 gula spelar-maskpixlar**, får **612 felmatchade P1-andropixlar** och **2628 oönskade vita pixlar**. R1aa:s `CXM0P`-readout är alltså inte skälet till FAIL: själva 5-NPC-figurintegriteten bryts.

**R1z bevisar färgkonflikten; R1aa bevisar dubbelkopieringsberoendet.** Dessa är två skilda hårdvaruhinder som båda måste lösas om vi vill ha ett enskilt gult M0 genom hela rummet *och* sex originella självständiga NPC på samma Y.

## Prioriterade fortsatta research-spår (inte auktoriserad implementation)

**A. Cykelbudget och NUSIZ-restore:** bevisa med faktiskt 76-cykel-/scanline-tidsdiagram om `NUSIZ0=$02` kan återställas **innan** de nedre NPC-maskraderna börjar, samtidigt som `ENAM0` släcks i tid. Skapa endast ett explicit ändrings- och testprotokoll, utan att offra någon av fem ursprungsinstanser. Tidigare data visar att naiv direkt `ONE_COPY` saknar denna återställning och därför underkänns.

**B. Skilda högerkärnor / resurser:** undersök en annan registerlayout för längre M0-X eller om M1 som alternativ resurs kan fungera. M1:s egen NUSIZ1/P1-koppling är också ett möjligt hinder; förutsätt inte en lösning före rå Stella-pixeltest.

**C. Berzerk-inspirerad logik när teknisk sprite-kernel väl klarar det:** håll aktiv kula som `x,y,direction,lifetime` i RAM, flytta under VBLANK med coarse/finpositionering, använd radbaserad `ENAM0`-aktivering, och kombinera `CXM0P`/Tia-latch med ett logiskt fiende-ID. Gör ingen produktionskoppling innan oberoende VERIFICATION.

**Projektgrind:** `main`, ROM DEVELOPMENT:s draft PR #7 och separat VERIFICATION issue #8 inte ändrade av forskningen. Full R1 fortsatt **BLOCKED/FAIL**; fjärde P0 endast fyra diskreta X, två stora kvinnor inte fri-X, sjätte stor man saknas. Forskningsfiler får inte slås ihop med produktion utan separat MAIN-beslut.
