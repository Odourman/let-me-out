# MAIN II – sex cykelsäkra X-lägen: 600/600 Stella PASS (lokal forskningskontroll)

**2026-11-16.** Körbar NTSC 16KB standard-F6 i GitHub Actions; separat forskningsgren, inte oberoende VERIFICATION och inte sex-NPC R1.

## Källa och reproduktion

- GitHub Actions **SUCCESS**: https://github.com/Odourman/let-me-out/actions/runs/43777884182
- Testad commit: `172666bc20439bc07cf4b76bd6d447f8f6fed457`
- Artifact ID `14185994808` (`main-ii-r1b-six-safe-x-600-frames`), 626 filer, 600 verkliga råa obeskurna inom debugger-ROI 900×300 X11-PNG.
- F6 ROM SHA256 `9ea80a1e2dd8a794a24cafb43f89a6c7647c381d840db3a9982348fc2e073fb9` (16 384 byte).
- DASM 2.20.14.1 / Stella 6.7.1, Ubuntu 24.04.
- Verifierade efter nedladdning `evidence_600/summary.json`, `frames_600.csv`, `SHA256SUMS.txt`; `LOCAL_PASS_600` och tom `frame_errors`.

## Uppmätt under 600 SAMMANHÄNGANDE bilder

| Mått | Faktiskt utfall |
|---|---:|
| Bildruteföljd 11–610 utan luckor | 600/600 |
| Faktisk Stella HUD: exakt 262 scanlines | 600/600 |
| Båda olika original-8×9-maskerna exakt (9 rader, 72 bitpositioner vardera) | 600/600 |
| Båda väntade X-koordinaterna i rå Stellabild | 600/600 |
| Gul temporär P0-spelare | 600/600 |
| Gult M0-projektiltest | 600/600 |
| Extra vita pixlar utanför två maskområden | 0 |
| Olika prövade grova delay-par | 6 |
| Pass-klass | `LOCAL_PASS_600` (egenkontroll) |

Sex säkra fördröjningspar: `(1,1)`, `(2,1)`, `(3,1)`, `(1,2)`, `(2,2)`, `(1,3)`. De ger GUI-X-par `(196,334)`, `(226,364)`, `(256,394)`, `(196,364)`, `(226,394)`, `(196,394)`. Varje av dessa finns i minst 96 faktiska bildrutor i bevisningen. Sekventiell bildruta analyserades via Stella HUD-frame-ID, inte antagen körning. Stella HUD:s vanliga/rödmarkerade 262 och 270 klassificerades skilt.

## Viktig NEGATIV gräns från tidigare 8-lägesprov

[8-lägesprovet](https://github.com/Odourman/let-me-out/actions/runs/43777543002) ger **456/600** 262-raders/maskkorrekta och **144/600** med **270 rasterlinjer**, felaktiga masker/avvikande kvinnoposition och saknat M0. De två utpekade kombinationerna är `(3,2)` och `(2,3)`: enradskerneln överskrider 76-cykelsbudgeten där. Fyndet får inte trollas bort av att sex övriga lägen är stabila.

## Vad detta inte visar

R1b är bevisat endast för **två olika originalmasker** med **begränsade, grova X-justeringar** och stor separation. Det finns **inget** bevis för nära placeringar/överlappar, fullständigt fritt X, tre till sex samtidiga androider, R2 nyckel/O1, playfield-väggar/dörr, 600 bildrutor på riktig konsol, slutligt vald spelargrafik eller oberoende VERIFICATION.

**R1 sex fria NPC kvarstår FAIL/BLOCKED.** Inga ändringar till `main`, draft PR #7 eller Issue #8, ingen merge och ingen fullspelsimplementation.
