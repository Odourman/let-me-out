# MAIN II – R1b 8-position X-matrix / 600 Stella frames: BLOCKERANDE TIDSGRÄNS

Datum: 2026-11-16. Analys av verkliga råfångster; **inte godkänt R1**, ej oberoende VERIFICATION.

## Reproducerbara råbevis

- [GitHub Actions run 43777543002](https://github.com/Odourman/let-me-out/actions/runs/43777543002), commit `d4dea3a482bf41cc5e63dc3982f345c013126645`.
- Run FAIL på analyssteget eftersom digit-sampling använde fel gultröskel. **Inspelningen av 600 råbilder slutfördes**.
- Artifact ID `14187126506` omfattar 600 verkliga X11-Stella-bilder, kod, sym/lst, F6-ROM.
- ROM SHA256 `4697b6aa1bd905d4cce3ab014ae7f7ba6059275efe2b83da87dc54e1cd1bf5aa`, NTSC standard F6 16384 byte.
- Råbilder återanalyserades externt med korrigerad HUD-gultröskel och två distinkta tillstånd (normalt/rödmarkering) per rastertal. Observerad counter 11–610 exakt och utan luckor.
- R1b-originalmasker (stor man/stor kvinna) jämfördes bit-för-bit mot ursprunglig godkänd designgrafik. P0, M0 och extra vita pixlar kontrollerades också.

## Faktiska resultat

- 600 av 600 bildrutor har sekventiella Stella frame-ID.
- **456/600 bilder:** 262 linjer, två olika kompletta ursprungliga 8×9-bitmaps, individuella grova X-lägen och gult M0-skott.
- **144/600 bilder:** **270 rasterlinjer**, ofullständiga/felplacerade masker och M0-testskott saknas visuellt; P0 fortfarande synlig.
- 0 extra vita pixlar uppmätta i valideringsområdet, men detta kompenserar inte för 144 felaktiga bilder.
- Varje osäker raster-/bildruta klassas ej som PASS.

| A-delay | B-delay | Andel provade frames | Resultat | Förklaring |
|---|---|---:|---|---|
| 1 | 1 | 70 | Maskerna hela; 262 | PASS inom lokal variant |
| 2 | 1 | 80 | Maskerna hela; 262 | PASS inom lokal variant |
| 3 | 1 | 80 | Maskerna hela; 262 | PASS inom lokal variant |
| 1 | 2 | 80 | Maskerna hela; 262 | PASS inom lokal variant |
| 2 | 2 | 80 | Maskerna hela; 262 | PASS inom lokal variant |
| **3** | **2** | **80** | **270 linjer; masker/M0 FAIL** | Rasterbudget överskrids |
| 1 | 3 | 66 | Maskerna hela; 262 | PASS inom lokal variant |
| **2** | **3** | **64** | **270 linjer; masker/M0 FAIL** | Rasterbudget överskrids |

På 9 övergångsbilder markeras 262 i rött av Stella (efter 270) och på 9 övergångsbilder 270 i rött (efter 262). Dessa markeringar räknas efter sitt **faktiska rastertal**, inte via en enda HUD-hash. Summa 456 normala 262, 144 faktiska 270.

**Viktig korrigering av analysverktyg:** frame-ID-texten använder ljusgula UI-pixlar med blå komponent ca 128; första auditor använde tröskel `blue<100` och kunde därför inte kalibrera siffrorna. Det är inte samma gula färgtest som för P0/M0. En separat korrekt HUD-sampling återfår alla 600 frame-ID och den verkliga 270-felklassen.

## Beslut

**8-positionersgruppen är inte hållbar:** de två kombinationerna med A+B=5 ska betraktas som FAIL i just denna enradiga kernel. Det är inte bevis att alla närhets-/X-tekniker är omöjliga. Följande experiment bör begränsas till de sex säkra lägena och kräva 600/600 äkta Stella-bildrutor, fullständiga masker och 262 linjer. Några godtyckligt fria X, 3–6 NPC, PF-väggar eller R2 nyckel/O1 är **inte** verifierade.
