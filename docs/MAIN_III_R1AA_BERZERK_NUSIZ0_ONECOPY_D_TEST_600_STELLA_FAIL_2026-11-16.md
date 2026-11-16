# LET ME OUT! – MAIN III R1aa: test av Berzerks NUSIZ0=ONE_COPY i vår kritiska D-skjutrad

**Datum 2026-11-16. Forskningsstatus: FAIL (456/600).** Direkt testad Atari 2600-originalhårdvarulogik i autentisk Stella 6.7.1, inte en generell bedömning av Berzerk. Full R1 fortsatt blockerad. `main`/ROM DEVELOPMENT/VERIFICATION har inte ändrats.

## Varför denna kandidat testades

Kommenterad Berzerk (1982)-disassembly [fast GitHub-källa](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm), bl.a. rader 964–977, använder `NUSIZ0=ONE_COPY` under den ordinarie spelbilden (övre två bits vid horisontell projektil sätter bara missilbredd). Vi ville se om samma trick kunde hindra vårt R1y's `NUSIZ0=$02`-automatiska extramissiler och hålla en **gul** M0 på GUI-x286..300 efter den annars omöjliga tidiga avstängningen vid CPU c53. R1y:s sista lilla P0-kvinna står GUI-x378.

## Exakt byggt isolerat prov

Från hårdlåst R1y-ROM SHA256 `aaf9ecf5b6698e1df75e9c0f70c114a913711d1edf99b4ef48ef8f7ad40e02b0` ändrades bara specialskottraden i D:
1. Ersätt `STY ENAM0` med **`STY NUSIZ0`**, 3 cykler vid c53. Här är `Y=8`, alltså `NUSIZ0=$08` och de tre lägsta bitarna = `000` (**ONE_COPY** för P0/M0).
2. Lämna `STA RESP0` c56, `STA COLUP0` c59 och alla ursprungliga NPC-bitmapbytes oförändrade.
3. Ersätt `JMP R1oLowerD` (3 cykler) efter `DEY` med **`STY ENAM0`** (3 cykler) och fall-through till nästa rasterrad, så att M0 släcks innan nästa rad. Detta är totalt cykelneutralt på specialraden.
4. **Medveten risk för testet:** `NUSIZ0=$08` ligger kvar i den nedre halvan av figurbandet, så automatkopierade P0-figurer kan försvinna. Vi accepterar INTE detta som ett löst resultat; det strikta pixeltestet måste upptäcka det.

## Verkligt resultat: missile-biten fungerar, fem-NPC-biten gör det INTE

[**GitHub Actions #43851081064**](https://github.com/Odourman/let-me-out/actions/runs/43851081064) **FAIL** med 600 konsekutiva faktiska Stella 6.7.1/X11-råbilder på testad källcommit `0ba288aaf6b08a21a4723414bd5fef5e2ca96682`. [**Evidensartefakt #14217043217**](https://github.com/Odourman/let-me-out/actions/runs/43851081064/artifacts/14217043217), 622 arkivposter inkl. 600 PNG, full assembler/ROM/DASM-listning, 600-raders CSV och summary. Nedladdad ZIP **SHA256 `b676b9865698ba132678bbc96268d1995e3a5773c38d1a2c049f8e7224ecd758`**, CRC PASS. Standard 16 384-byte NTSC/F6-ROM **SHA256 `9a1a464252c3f0da3d6aecc85fc21514e1cb43c3c35f258548e4919837c84778`**.

| Exakt mätt kontroll | Resultat |
|---|---:|
| Konsekutiva faktiska Stella-frame-ID | **600/600** |
| NTSC 262 rasterlinjer | **600/600** |
| **En korrekt GUL M0-projektil vid armhöjd y167 på förväntad X** | **600/600** |
| Fjärde lilla P0 x330 (A) | 150/150 helt korrekt |
| Fjärde lilla P0 x348 (B) | 160/160 helt korrekt |
| Fjärde lilla P0 x360 (C) | 146/146 helt korrekt |
| Fjärde lilla P0 x378 (D) | **0/144** – masken sönderfallande/ej igenkännbar |
| Sammanlagd originalmask-PASS inkl. färg, inga ghosts, dörrar/NTSC | **456/600 FAIL** |
| Förlorade gula spelarbildpixlar (summa över testade frames) | **7488** |
| Felmatchade pixlar i den andra stora kvinnans mask | **612** |
| Överskjutande vita pixlar | **2628** |
| Extra gula spökpixlar | **0** |
| Liten mans P1-maskfel | **0** |

**Reproducerbart orsakssamband:** D:s specialrad fungerar för själva M0-missilen, men när `NUSIZ0` lämnas i ONE_COPY på de efterföljande rasterraderna kan spelet inte längre visa de automatkopierade P0-figurer som gör vår fem-NPC-kernel möjlig. De ursprungliga maskdatabyten är oförändrade, men maskerna kan inte återges korrekt. Detta är precis den skillnad som Berzerks vertikala robot-P1-multiplex och vår simultana fem-NPC-samma-Y-kernel ger.

## Slutsats till MAIN

**Berzerks användning av `ONE_COPY` är tekniskt relevant, men inte direkt flyttbar till vår nuvarande kernellösning.** Om detta ska undersökas ytterligare måste `NUSIZ0=$02` återställas före första nedre-NPC-raden **och** M0 släckas före nästa rad med en cykelneutral pålitlig schemaläggning, eller hela den kritiska D-regionen kodas på ett annat sätt. Det finns ingen evidens för att en sådan 76-cykelslösning existerar med nuvarande grafik. Den får inte antas vara löst bara för att M0 ser rätt ut på en rad.

Berzerks övriga **riktiga** tekniker är fortfarande direkt forskningsvärda utan att påverka grafiken: skottets RAM-X/Y/riktning/livstid, individuell `HMM0`-positionering under blankning via 15-TIA-CC-sektorer, per-rad-`ENAM0`-data och separata P1-robotsektioner när fiender inte delar rasterrader. Projektgrindar förblir oöppnade.

**Ingen ändring av `main`, ROM DEVELOPMENT:s draft PR #7 eller VERIFICATION issue #8**. Senast strikt godkända skottintervall fortsätter att vara R1x x268..282, 600/600 PASS.
