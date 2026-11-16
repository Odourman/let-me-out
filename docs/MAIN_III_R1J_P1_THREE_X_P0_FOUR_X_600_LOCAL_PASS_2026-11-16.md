# LET ME OUT! – MAIN III R1j: tredje P1-X-fönstret c42, 600 verkliga Stella-frames

**Datum:** 2026-11-16. **Status:** `LOCAL_PASS_R1J_P1_THREE_X_P0_FOUR_X_600`, endast isolerat forskningsbevis. **Full R1 = FAIL/BLOCKED.**

## Exakt artefakt

- Forskning, ej spelkod: branch `research/main-iii-r1j-p1-third-x-20261116`, byggd och testad commit **`55c2bdad33e38e1cdcc4fd66adce7627ea380182`**.
- [GitHub Actions #43829950274](https://github.com/Odourman/let-me-out/actions/runs/43829950274) **SUCCESS** (DASM, Stella 6.7.1/X11, 600 påföljande råbilder, pixelaudit, SHA-256-kontroll).
- [Evidens-artefakt #14208865190](https://github.com/Odourman/let-me-out/actions/runs/43829950274/artifacts/14208865190), nedladdad lokalt.
- Testad **16 384-byte standard-F6 ROM** SHA256: `71337e7787ab14d5fc1730700c0cda1ac4ad15fef5566f29c642faa966819837`. Fyra identiska 4 KB banker.
- Nedladdad evidens-ZIP SHA256: `d80f17f49b7e7d9117c161c0358c2e00c98b4315d91ecff9ba6bba3b24ea6184`, **622** arkivposter, **600 PNG**; ZIP CRC kontroll: `testzip() == None`.
- Ursprung: R1i-A (kört, SHA `34a7f515773c6991d0a7abff4d48f6f9d82dadcfb364fb8996d5ccb31539c55c`). Generatorn bygger ursprunglig R1i och kontrollerar SHA innan den lägger till tredje P1-positionen.

## Kärnförändring: fyra plus tre tidsscheman

Stora kvinnans `GRP1` skrivs oförändrat vid c36. Två befintliga 3-cykels `BIT FRAMELO` och en befintlig 3-cykels `STA RESP1` permuteras:

| P1 läge | Andra `STA RESP1` slutar | Verklig stor kvinna i Stella X11 GUI |
|---|---:|---:|
| Tidig | **c39** | **x244** |
| Mellan | **c42** | **x262** |
| Sen | **c45** | **x280** |

Ingen extra registerinstruktion tillförs i nio-radersbandet. Fyra fjärde-NPC-`P0`-scheman `x330/348/360/378` bibehålls. Tredje P1-läget skapar totalt **12** specialiserade originella 8x9-kärnor, valda före figurbandet med `FRAMELO & $0C` (P1 tre lägen), `& $30` (fjärde P0 fyra lägen). Högerdörrens separat `& $40` bevaras. **Detta är förkompilerade tidsfönster, inte generella 160 färgklockors fri X.**

Fyra olika godkända vita originalmasker är identiska med `main/design/NPC_REFERENCE_8x9_masks.json`. Stor man x166 och liten man x406 stillastående. Gul temporär spelare x216; M0-skott är en pixelrad **före** NPC-bandet, ej i deras nio rasterrader.

## Mätningar och dubbla granskningar

- **600/600** löpande frame-ID och **600/600** NTSC med 262 scanlines; **600/600** kompletta fyra originalmasker, testspelare, ett testsymbolskott, BALL vänstervägg, PF0 höger brun 32-raders dörröppning; **0** vita/gula spökpixlar; **0** misslyckade frames.
- Stora kvinnans P1 tidig/mellan/sen: **150 / 148 / 302** frames. Lilla kvinnans fyra lägen och dörrens öppet/stängt bevarade.
- **24/24** kombinationer av 3 P1 ×4 P0 ×2 dörr, minst **16 frames per kombination**.
- Oberoende lokal extra dubbelkontroll av **600 rå-PNG** mot CSV: exakt **24 olika SHA-256-bildhashar** för spelområdet (croppad region), exakt **en** stabil unik bild per kombination och ingen hash delas mellan kombinationer. Utgör **inte** organisatoriskt oberoende VERIFICATION.
- Det finns två möjliga 128-frames fasoffsetar i `summary.json`: `[127,255]`, eftersom P1 nu endast kodar låga två bitar, P0 bit4–5 och dörr bit6; bit7 påverkar ingen av scenfaserna. Detta är **inte en datamotsägelse**.

## Begränsningar / statusgates

**R1j PASS** är enbart tredje valbara X-positionen för **en av fyra** vita androidmasker samtidigt med fjärde androidens fyra valbara lägen och övrig rasterbelastning. Ingen femte/sjätte android, inga sex generellt fritt placerbara objekt, ingen joystickstyrd rörelse/AI, inga näraöverlappsförhållanden, inget samtidigt M0 inne i NPC-bandet, ingen 40×22-karta, ingen guldnyckel, ingen orange port med svart nyckelhål och ingen full R1–R4-kompatibilitet.

**Nästa separat hypotes R1k:** ersätta en 3-cykels väntinstruktion med `STA RESP1`, så att samma stora kvinnomask potentiellt syns **två gånger inom samma rasterrad** (strobningar c39 och c45, 18 färgklockor isär). Detta får inte kallas femte NPC förrän två hela ursprungliga kvinnosilhuetter syns samtidigt i en verklig Stellabild. TIA:s 18CC-fas kan medföra återtriggningseffekter; ett test får klassas FAIL även om scanlineantalet är korrekt.

**Scope:** allt isolerat under `research/`. `main`, ROM DEVELOPMENT/PR #7 och oberoende VERIFICATION/issue #8 ändras inte. Full R1 fortsatt FAIL/BLOCKED.
