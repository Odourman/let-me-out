# LET ME OUT! – MAIN III R1y: gräns för nästa M0-fönster; 126 uteblivna skott i ett NPC-läge

**2026-11-16. FORSKNINGSSTATUS: FAIL** för 8 M0-X × 4 NPC-X × 2 dörrlägen. `474/600` strikta godkända verkliga Stella frames. Full R1 fortsatt FAIL/BLOCKED.

## Reproduktion och exakta bevis

- [GitHub Actions #43848364350](https://github.com/Odourman/let-me-out/actions/runs/43848364350) = **FAIL** (testad commit `f6265a841998430e3a0a9cb66e5575309b42ee52`); DASM byggde, riktiga Stella 6.7.1-X11 spelade in **600 konsekutiva frames**, pixelgranskning underkände 126 frames.
- [Full evidensartefakt #14216866490](https://github.com/Odourman/let-me-out/actions/runs/43848364350/artifacts/14216866490), 622 poster inkl. 600 råa PNG, källor/listing/symboler, CSV och ROM.
- Nedladdad evidens-ZIP SHA256 **`ddbe7f882afae2b5dc8b0b452ba47346681fad20e416a000de7e241559ba3881`**, CRC PASS.
- ROM: 16 384 byte, vanlig F6/NTSC, SHA256 **`aaf9ecf5b6698e1df75e9c0f70c114a913711d1edf99b4ef48ef8f7ad40e02b0`**.
- Basen är exakt tidigare R1x SHA256 `15b65be5d2baf810576f58dc9fbe6d9a8b62b540d50b04ff2fa7a1dec6fab613` (600/600 PASS, andra stora kvinnans P1-kontakt verifierad). R1y lägger **bara ytterligare 3 CPU-cykler `BIT FRAMELO` före blanknings-`STA RESM0`** = +9 TIA color clocks = +18 Stella-GUI-pixlar. Inga ändringar i fem NPC:s originalmasker, deras 14-radskernlar eller R1x:s fyra skottrutiner.

## Precist uppmätt rasterfel

| Fjärde NPC:s X (GUI) | Skott X=286 | Skott X=288,290,292,294,296,298,300 | Resultat |
|---|---|---|---|
| 330 (A) | PASS | PASS, alla 7 | **150/150** |
| 348 (B) | PASS | PASS, alla 7 | **160/160** |
| 360 (C) | PASS | PASS, alla 7 | **146/146** |
| 378 (D) | **PASS** | **FAIL, alla 7** | **18/144** |

- **474/600** fulla original-mask+projektil+NTSC+vägg-kontroller PASS.
- **126/600 FAIL** är samtliga D-läget med M0-X 288..300 (18 frames vardera). För dessa är `M0_gui_pixels=0` och `raw_projectile_x_coords=[]`, vilket utesluter enbart fel koordinatuträkning. Faktiska gula M0-pixlar saknas.
- **600/600** autentiska konsekutiva frame-ID, NTSC 262 linjer, fem ursprungliga NPC-instansmasker visuellt korrekta, original 8×9 bytes identiska, vänster BALL och höger PF0/32-raders dörr.
- **0** gula eller vita extrakopior/spökpixlar. Felet är alltså **utebliven M0**, inte dubblering.
- Verklig `CXM0P`-diagnostik skiljer fortfarande kontakt från utebliven/ej överlappande projektil: `303` frames med visuellt förväntad P1-kontakt och motsvarande färg `[0,0,138]` kontra svart `[0,0,0]` för återstående `297`.
- I R1w/R1x fungerade D-läget eftersom M0 avaktiverades vid 6502-cykel **c53** efter projektilet. Vid R1y:s ytterligare förskjutning når kula x288..300 för sent för detta aktiveringsfönster. De tre andra lägenas M0-avstängning vid **c56** räcker längre.

## Konsekvens för nästa forskning

**R1y är inte godkänt och får inte ersätta R1x.** Det visar ett mycket specifikt hinder: D-lägets `STY ENAM0` vid c53 måste läggas senare för en korrekt projektil x288..300, men `STA RESP0` måste samtidigt ligga vid c56 för att den lilla kvinnans X=378 ska förbli korrekt. Att flytta endera naivt skadar masken eller får en oönskad missilkopia (jfr tidigare R1o/R1q-försök).

Nästa hypotes under trick #14 (Multiple Display Kernels): använd en separat skottrutin för senare M0-X som omfördelar `ENAM0`, `RESP0`, `GRP0` och `COLUP0` inom samma 76-cykelsscanline, med full pixelaudit och **inga** kompromisser i de fem maskerna. Alternativt gör en separat klinisk research-test av vilket NPC-ID `CXM0P` D7 avser efter P1-multiplex, genom att kombinera den bevisat korrekta R1w-första P1-kollisionen med R1x-andra P1-kollisionen.

**Integritet:** Ingen ändring av `main`, ROM DEVELOPMENT draft PR #7 eller VERIFICATION issue #8, ingen utökning av implementeringsauktorisation. Full R1 fortsatt FAIL/BLOCKED.
