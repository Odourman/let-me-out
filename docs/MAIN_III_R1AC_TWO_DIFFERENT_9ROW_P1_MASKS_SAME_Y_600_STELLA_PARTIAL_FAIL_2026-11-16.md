# Let Me Out! – R1ac: TVÅ olika kompletta original-8×9-masker på samma Y via P1-RESP1-retrigger

**2026-11-16. Isolerad RESEARCH, INTE FULL R1. Status: PARTIAL / FAIL, 300/600 strict image PASS.** Kod finns endast på researchgren `research/main-iii-r1ac-dual-p1-mask-close-resp-stella-20261116`. Ingen merge, ingen ändring av ROM DEVELOPMENT PR #7 eller oberoende VERIFICATION.

## 1. Rå verifierbar evidens

- [**GitHub Actions #43856319003**](https://github.com/Odourman/let-me-out/actions/runs/43856319003): **FAIL** (strikt pixeltest), men DASM + faktisk Stella 6.7.1-X11 kördes med 600 konsekutiva skärmbilder, 262 NTSC scanlines.
- **Testad kodcommit:** `eddcc0d52a4a2e9fe3ad89f09543433a90fea22d`.
- [**Evidensartefakt #14220472947**](https://github.com/Odourman/let-me-out/actions/runs/43856319003/artifacts/14220472947): 622 ZIP-poster inklusive 600 råa PNG, assemblerkälla, DASM-listing/symboler, byggmanus, 600-raders CSV och summary.
- ZIP SHA256: `ccf8d78c3db5acda7131ff05d42b080be194c277b86f95275e6c81075accf7c7`; **CRC testat utan fel**.
- Körbar **16 384-byte F6/NTSC-ROM SHA256:** `af47683fccff5fa48546de9c81032502ccf2ea7a980de90ed1880812789a7f30`.
- Generatorn pinnar historisk ROM DEVELOPMENT `vb_9_interleave.asm` Git blob `a25c92adb4ca5087eeace674e371be98b273ae5b`. **De tre oförändrade 8x9-originaltabellerna**: `MaleRows`, `FemaleRows`, `PlayerRows` (exakta nio byte vardera) återanvänds direkt utan ny stil, förstoring eller vertikal interleave.

## 2. Vad experimentet faktiskt gör

En enda NTSC/F6-ROM visar på samma nio rasterrader:
- En stor originalman + en stor originalkvinna, **båda med olika bitmapdata** via P1, `NUSIZ1=$01`, två `STA RESP1` på samma scanline, och cykelprecist `STX GRP1` innan den andra nära-kopian.
- En fullständig originalgul P0-spelare och en ensam gul M0 på mittenraden som diagnostiskt skott.
- Fyra positionskombinationer styrda av `FRAMELO & 3`, med exakta 6507-resettider c30/c42, c32/c42, c30/c44, c32/c44. All övrig svår v0.18-scen inklusive ytterdörr och övriga fyra NPC ingår **inte**.

Faktiska pixlar i **900x300 GUI-screenshotbeskärning**, horisontalposition lokalt x (OBS inte TIA color clocks, inte fritt valfri X över hela skärmen):

| Mode | Stora mannen maskens lokala X | Stora kvinnans maskens lokala X |
|---|---:|---:|
| C | **87** | **159** |
| D | **99** | **159** |
| E | **87** | **171** |
| F | **99** | **171** |

Här finns direkt positivt belägg för **separata X-ändringar**: C→D flyttar endast mannen 12 screenshotpixlar; C→E flyttar endast kvinnan 12 screenshotpixlar; C→F flyttar båda. Varje logiskt mode har stabila, separata positioner i alla 600 bilder. Detta är **begränsad kvantiserad positionsfrihet**, inte sex logiskt fria NPC eller oinskränkt 160CC-kontroll.

## 3. Fail-closed verkligt resultat

| Faktiskt checkat | Resultat |
|---|---:|
| 600 konsekutiva autentiska Stella-frame-ID | **600/600** |
| Stabil **262-scanline NTSC** per frame | **600/600** |
| Fullständiga originalmasker för BÅDA P1: **ingen enda saknad vit pixel** | **600/600**, 0 saknade |
| Gul original-P0-mask: **ingen saknad gul pixel** | **600/600** |
| Exakt **en gul tvåpixel-M0** på mittenraden | **600/600** |
| Fyra distinkta man-X/kvinna-X-par | **4/4** |
| **Oönskade vita ghostpixlar** | **1 200 totalt**, exakt 4 pixlar i 300 frames |
| Oönskade vita pixlar på bandets första rasterrad | **300/600 frames FAIL** |
| **Full stringent PASS** | **300/600**, dvs **R1ac FAIL** |

Den extra grafiken är mycket specifik: på första rasterraden, före stora mannens avsedda bild, syns två vita tvåpixelgrupper från den mask som laddades till `GRP1` **redan c7**, före första `RESP1`. Exempel:
- Man-x=99 ⇒ ghost på lokala GUI x51–52 och x61–62, y96.
- Man-x=87 ⇒ ghost på lokala GUI x57–58 och x67–68, y96.
Ingen maskpixel saknas någonstans; detta är en **extra tidigt utmatad P1-kopia**.

## 4. Nästa korrigeringshypotes R1ad

Den särskilda forskningsgrenen `research/main-iii-r1ad-delay-grp1-after-first-resp-20261116` har en **cykelneutral** förbättring: lägg före första `STA RESP1` först `LDX FemaleRows,Y; LDA PlayerRows,Y; STA GRP0; LDA ShotEnable,Y; STA ENAM0; LDA MaleRows,Y; BIT FRAMELO`, exakt c25 som förr. Behåll NOP-fyllnad och **samma första RESP1 c30/c32**. Ersätt tidigare `BIT FRAMELO` (3 cykler) **omedelbart efter** första reset med `STA GRP1` (3 cykler), så manmaskens register **blir aktivt c33/c35**, före nära-kopians första pixel men EFTER den tidiga spök-kopian. Andra RESP1 förblir c42/c44, kvinnans `STX GRP1` förblir oförändrad. Originalmasker ändras inte.

R1ad är **hypotes tills 600 autentiska Stella-frames pixelkontrollerats**. Risk att den första maskens första pixel påverkas om TIA:s GRP-fördröjning eller P1-counterfas skiljer sig; sådan skada ska ge FAIL. Källor: [Andrew Towers TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) och [Stella 6.7.1 Player.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx).

**Status/ansvar:** Detta är research som MAIN tar emot som delbevis. Full R1 enligt v0.18 C01/C04 kräver sex androider, same-Y, variation och integrerat testsymbolskott. R1ac har bara två NPC + player/skott, ingen PF-dörr, ingen oberoende VERIFICATION. `main`, PR #7 och fristående VERIFICATION issue #8 oförändrade.
