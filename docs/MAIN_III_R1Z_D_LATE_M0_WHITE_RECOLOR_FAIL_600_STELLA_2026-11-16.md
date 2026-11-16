# LET ME OUT! – R1z: en-kopieringslärdom från Berzerk, D-lägets sena M0 och den VERKLIGA färgkonflikten

**Datum 2026-11-16. Status: FAIL, 456/600 strikta Stella frames.** Testprototypen får inte ersätta tidigare godkända R1x. Full R1 fortsatt FAIL/BLOCKED; ingen auktoriserad produktionsimplementation eller oberoende VERIFICATION.

## Reproducerbarhet

- [GitHub Actions **#43850116022**](https://github.com/Odourman/let-me-out/actions/runs/43850116022), testad commit `0227f80b0a62da2dc171948cf484082b0a7afb93`: **FAIL** efter genomförd 600 konsekutiva autentiska Stella 6.7.1/X11-frame och strikt raster-/originalmask-/dörr-/NTSC-/missil-/collisiongranskning.
- [Komplett råevidensartefakt **#14215934991**](https://github.com/Odourman/let-me-out/actions/runs/43850116022/artifacts/14215934991): 622 poster inklusive 600 råa Stella-skärmbilder, käll-ASM, DASM-listning och 16 KiB F6-ROM, CSV och sammanfattning. Nedladdad ZIP SHA256 **`636df4e8b7e6690679b23c7f64aa6b6fd26d8ef87e10c706bfe1bae3df0d5a43`**; CRC PASS.
- ROM SHA256 **`8cbc1ed28bfee2cd922f73664b38e8dfd5f256572a19eb575b01f609ba9cc2b3`**; 16 384 byte NTSC/F6 med identiska 4 KiB-banker.
- Exakt låst R1y-bas `aaf9ecf5b6698e1df75e9c0f70c114a913711d1edf99b4ef48ef8f7ad40e02b0`. Ursprungliga fem NPC-bitmapmasker och hela 14-radersvisningen lämnas orörda; endast D-lägets **specialiserade skottrad** ändras.

## Testet och dess exakta 6502-cykelhypotes

R1y tappade den gula projektilen i D-läget (fjärde P0/GUI-x378) efter M0-X=286. Hypotesen var att inte bara off-tiden `STY ENAM0` utan också P0-färgfasen kan schemaläggas om med **samma totala antal CPU-cykler**.

D:s tidigare steg efter `LDA #$0E; STX GRP0`:
- `STY ENAM0` vid c53 = stäng M0
- `STA RESP0` vid c56 = behåll x378
- `STA COLUP0` vid c59 = byt P0/M0 färg till vit

R1z **byter plats på de två sista operationernas logiska uppgifter**:
- `STA COLUP0` c53 = byt P0/M0 färg till vit **tidigare**
- `STA RESP0` c56 = behåll exakt x378
- `STY ENAM0` c59 = stäng M0 **sex cykler senare**

Ingen ompositionering av androiderna, ingen maskeradsjustering, inga extra CPU-cykler.

## Faktiskt resultat från all 600 PNG + CSV

| Fjärde P0-lilla kvinnans GUI-X | Riktiga frames | Strikt PASS | Utfall |
|---:|---:|---:|---|
| x330 (A) | 150 | **150** | Oförändrad R1y, korrekt gul M0 |
| x348 (B) | 160 | **160** | Oförändrad R1y, korrekt gul M0 |
| x360 (C) | 146 | **146** | Oförändrad R1y, korrekt gul M0 |
| x378 (D) | 144 | **0** | **FAIL**: M0 skjuts ut, men som **VIT** i stället för gul |

**Viktig ny upptäckt:** Vid D-lägets GUI-x286..294 ligger skottet inuti den **andra vita P1-kvinnans** täckta pixelområde, och den vita M0-projektilen blir osynlig visuellt mot vita pixelmasker. Trots att det inte går att se den gula kulan visar TIA-latchbakgrunden **blått när det är verklig M0/P1-kollision**. Vid GUI-x296,298,300 ligger skottet utanför den vita P1-figuren; då uppstår en **vit tvåpixelprojektil** som analysen korrekt markerar som oönskade extra vita pixlar.

Dessa synliga extra-vita M0-pixlar ger **108 vita extrabildpunkter** över hela körningen, `36? [korrigerat nedan: 54 frames x 2 pixlar = 108]`, medan de fyra NPC-positionerna och deras masker fortsatt är korrekta (600/600), NTSC 262 linjer 600/600, vänster BALL-vägg/höger PF0-dörr 600/600, 0 extra gula pixlar. D:s 144 frames underkänns, inte bara de 126 som föll bort i R1y.

**Detta avvisar ett alltför förenklat råd om att bara slå av M0 tre eller sex cykler senare**. `COLUP0` styr nämligen **både P0 och M0**. R1y:s problempunkt kräver att samma vita P0-NPC och den gula M0 samtidigt förblir korrekta på en scanline, medan `RESP0` bibehålls vid c56.

## Verklig jämförelse med original-BERZERK

Den kommentargranskade, rekonstruerade 1982-disassemblyn av Berzerk finns som **fixerad extern källa**: [`TheAnsarya/multi-local/.../berzerk.asm` commit `480a5287...`](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm).

- Berzerk sätter `NUSIZ0=ONE_COPY` i den ordinarie spelkoden (rader 964–977), med separat missilbredd via bits 4–5. Våra 5 originalandroidinstanser på **samma Y** kräver `NUSIZ0=$02` för P0-multiplex, vilket ger en automatisk **andra M0** när `ENAM0` förblir på. Berzerk har en **annorlunda synlig sprite-arkitektur**, inte ett enkelt registertrick vi kan kopiera.
- Berzerk använder självständig RAM-bullet-X/Y, `DetermineDiv15Position` (rader ca 2958–2979), `MoveObjectHorizontally` (ca 2980–2995), och per-rad läspointer `LDA (playerMissilePointer),Y; STA ENAM0` (rader 405–406, 467–468, 545–546). Robotarnas motsvarighet har M1/ENAM1.
- Sådant kan ge oss *fullständig logisk skottposition över skärmen*, men det ändrar **inte automatiskt M0:s färgkoppling och NUSIZ0-dubblering**. Dessutom är Berzerks robot-P1 vertikalt multiplexad mellan olika rastersektioner, medan våra figurer måste hållas på samma Y i aktuellt uppdrag.

## Rekommenderad separat forskningsfortsättning

1. **Undersök tidsstyrt `NUSIZ0=ONE_COPY` just under skottrad**, inspirerat av Berzerk. En sådan testkandidat måste verifiera att fjärde P0 vid x378 fortfarande ritas exakt, att M0 behåller **gul** färg och inte klonas, och att två-kopieringsläget är återställt nästa rasterrad utan att ändra 262 NTSC eller en enda ursprungsbitmapspixel. Att ställa `ONE_COPY` permanent vore ett ogodkänt ingrepp i fem-NPC-kerneln.
2. Alternativ separat missile-/playfield-kernel för en viss horisontell region (#14), med reproducerbart tidsbevis.
3. När ett korrekt hela-rums-M0-pixelprov finns, separera skottets verkliga RAM-tillstånd, eldknapp, logisk fiende-ID och kollisionsläsning från bildhårdvarans färgregister, såsom Berzerks uppdelning gör. Logisk fiendeidentitet kräver mjukvarubedömning eftersom TIA:s `CXM0P` bit7 inte kodar ID på den multiplexerade P1-instansen.

**Ingen ändring av `main`, draft PR #7 eller VERIFICATION issue #8.** Full R1 och senare implementation fortsatt blockerade; detta är rådgivande och reproducerbar research.
