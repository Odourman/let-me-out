# LET ME OUT! – MAIN III R1q: fyra P0-X bevarade, M0-dubbelkopian kvar

**2026-11-16. Status: RESEARCH FAIL.** Ingen produktionsimplementation eller independent VERIFICATION. Full R1 fortfarande FAIL/BLOCKED.

## Körning och exakt evidens

[GitHub Actions **#43838985789**](https://github.com/Odourman/let-me-out/actions/runs/43838985789), testad commit **`98189ebfe5205761f4182755f800147fc85d8453`**, genomförde riktiga 600 konsekutiva Stella 6.7.1 NTSC frames. ROM: 16384 byte F6 standard, SHA256 **`6dea652ffdee7c1ab17fea9a17ff7cfd467885e5ca244e674d8ad849260ebd53`**.

[Evidensartefakt #14212446712](https://github.com/Odourman/let-me-out/actions/runs/43838985789/artifacts/14212446712); nedladdad ZIP SHA256 **`f410a5161cff9f967949c467ad447c56d02f805eb0c26549324dcd336cb5465b`**; 622 poster, 600 rå PNG plus inledande/slutlig Stella-skärmbild, validerad CRC och komplett mask-CSV.

Metod: från exakt låst R1o-ROM SHA `41a1b55a4d413cca88eccd690d29b6af1a041e4a354e0f4838a832f10fd6c44d`. Originalmaskerna och 14-raders presentation är oförändrade. Enbart C/D:s avstängning `STY ENAM0` flyttades **efter** respektive `STA RESP0`, vilket återställde de nödvändiga sena strobefönstren.

## Faktisk bilddata

| P0 fjärde X-läge | Frames | NPC-mask korrekt på alla 14 rader | EN M0 exakt vid handen (inga kopior) |
|---|---:|---|---|
| x330 (A) | 150 | PASS | PASS |
| x348 (B) | 160 | PASS | PASS |
| x360 (C) | 146 | PASS | **FAIL: 2 extra gula pixlar på varje frame** |
| x378 (D) | 144 | PASS | **FAIL: 2 extra vita pixlar på varje frame** |

- **600/600** komplett fem-NPC originalbitmapinstans i 14 visade rader, gul testspelare, NTSC 262 scanlines, vänster BALL vägg och 32-raders höger PF-dörr, fyra rätta P0-X, alla åtta P0-X/dörrkombinationer.
- **600/600** det avsedda gula M0-skottet GUI-x232–233 på armhöjd GUI-y167, gammalt huvudskott saknas.
- **310/600** fullständigt rent: inga spöken.
- **290/600** misslyckas trots korrekta NPC-masker: C `STA RESP0` end CPU **c53**, M0 stängs inte förrän **c56**; D `RESP0` c56, M0 avstängning **c59**. Kopian på cirka GUI-x296–297 hinner redan genereras av `NUSIZ0=$02` och blir gul i C / vit i D när `COLUP0` ändras.
- Summa oönskade pixlar **292 gula + 288 vita**, exakt två per C- eller D-frame. Detta är ett faktiskt TIA-kollisions- och grafikproblem och får inte döljas som vit sprite eller tvättas bort i bildbehandling.

## Cykelhypotes för nästa avgränsade prov R1s

**Flytta i stället `STX GRP0` till efter sena `STA RESP0`**, med samma totala CPU-budget. Då kan M0 stängas **redan vid c48**, original-P0-strobe för C göras vid **c53** och D vid **c56**, medan den fjärde P0-bitmapen skrivs vid **c56 respektive c59**, fortfarande innan den börjar visas på skärmen runt x360/378. Grundprincipen är att TIA:s `GRP0` läses kontinuerligt när bitmapen faktiskt ritas: den behöver inte vara laddad vid horizontal reset, bara i tid inför synliga pixlar. Detta är **hypotes**, kräver verklig 600-frame pixelgranskning av fem hela NPC, exakt en M0 och väggar.

R1q FAIL, `main` oförändrad, ROM DEVELOPMENT draft PR #7 oförändrad, VERIFICATION issue #8 opåverkad.
