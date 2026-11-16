# LET ME OUT! – MAIN V: R1-F6 mottagen; tvåmaskers X-geometri självständigt granskad

**Datum 2026-11-16.** **Slutklass R1-F6:** `F6_TWO_MASK_HBLANK_PHASE_LOCAL_PASS` – **avslutad DEVELOPER_LOCAL diagnostisk leverans**, separat mottagningsgranskad av MAIN, **INTE fristående VERIFICATION**, inte oberoende RAM-styrda två X och **INTE full R1**.

## 1. Frysta GitHub-underlag och scope

- Fryst [R1-F6 TO_MAIN](https://github.com/Odourman/let-me-out/blob/e45455e09e1d796e576b0012d96e5d817d6210c4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F6.md), rapport Git blob `2ce19e1a45810f5836038526b6b626c567f53ad2`, commit `e45455e09e1d796e576b0012d96e5d817d6210c4`, isolerad branch `rom-dev/v018-r1-f6-two-mask-hblank-20261116`, bas F5 `953c6c5ef20e83d93474de4c094de784761da257`.
- Bindande [F6-order](MAIN_V_TO_ROM_DEV_II_R1_F6_TWO_MASK_HBLANK_COPY_GATE_AUTHORIZED_2026-11-16.md), Git blob `d17996752a2c83e6d387f99a7e3e489d35ad34a6`, höjst **två** F6/NTSC diagnostiska ROM-varianter och två rättvända 8×9-originalmasker. GitHub `compare_commits(F5,F6)`: **ahead=16, behind=0, 10 NYTILLAGDA F6-filer, 0 ändringar av tidigare källfiler**. Inga ändrade F2–F5 eller R1ba/GRAPHICS.
- PR #7 kontrollerad `open/draft/unmerged` HEAD `82667dae033f70570dce903f8e1d4866528be02a`. Issue #8 standby. Ingen PR-merge eller ändrad ROM-canon.

## 2. MAIN:s direkt hämtade riktiga Drive-evidens, INTE enbart rapportpåståenden

[Originalarkivet i den riktiga projektmappen](https://drive.google.com/file/d/1v7Kxo0nikzp0EhHDiuwqMW3ij85s17Gq/view) (Google Drive ID `1v7Kxo0nikzp0EhHDiuwqMW3ij85s17Gq`, parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`), titel `LET_ME_OUT_R1_F6_COMBINED_32_REAL_STELLA_10_TRAPS_SHA256_2026-11-16.zip`:
- Riktiga **1 292 303 bytes**, faktisk **SHA-256 `9e483dfc833843060d93a662d097ba8cc71aa9d9f19f29e915407ca0e9dfda80`**, **144 ZIP-poster**, `ZipFile.testzip()==None` / CRC PASS.
- `EVIDENCE_FILE_INDEX.json`: **142/142** verkliga ZIP-poster kontrollerade oberoende mot faktisk SHA-256 **och** exakt storlek: **0 mismatch**. `SHA256SUMS.txt` innehåller **142/142** verifierade filhashar, också **0 mismatch**; återstående två poster är index och manifest.
- Båda faktiska körbara ROM från ZIP, **16 384 byte** var, vardera fyra **byteidentiska 4 KiB-bankkopior**:
  - c21/c32: `d0572896ed47bf8e75264d1eb33d5e11f640b2390dc42b6565bdac42af86dc32`.
  - c23/c32: `eaed3faa87c496b08c50725f931096d69687385bcd75257d3dd63164dc36baef`.
- **32 originala Stella-crop-PNG 900×300**, **32 originala GUI-PNG**, **10 faktiska trap-GUI-PNG**, två märkta **syntetiska negativa** mutantbilder (inte positiva bevis). Käll-ASM/.lst/.sym, G0, fulla animerade råserier och versions-/CI-handoff i ZIP.

## 3. MAIN:s HELT SEPARATA direkta pixelunion från låsta TOP-DOWN-matriser

MAIN avkodade med en ny, separat Pillow/Python-algoritm var och en av de **32** arkiverade faktiska 900×300-bilderna och hämtade vitt pixelfält utan att använda F6-utvecklarens JSON-asserts. Använda ursprungliga källbitmappar från `design/NPC_REFERENCE_8x9_masks.json`, GitHub blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`:

```text
large_male   TOP-DOWN 3C 3C 18 FF 18 24 24 42 42
large_female TOP-DOWN 3C 3C 18 FF 3C 7E 7E 24 24
```

I varje bild söktes alla möjliga X-starter för **hela originalmönstret på nio rader**, med **två Stella-croppixlar per källbit** och exakt mängdunion. En ensam unik kombination av MAN+KVINNA krävs för att kalla en frame PASS; inga extra vita i pixelbandet. Detta är **egen MAIN-kontroll** med verkliga bildbytes, inte endast avläst källa eller samma utvecklarskript.

| Körning | Förregistrerat screenshot-X | Faktiskt screenshot-X | Verifierat MAIN |
|---|---|---|---|
| c21/c32 bas | `(43,99)` | **`(39,99)`** | **16/16** exakta, nio TOP-DOWN-rader, y=96–104, exakt **132 vita screenshotpixlar**, 0 miss/extra |
| c23/c32 prov | `(45,99)` | **`(45,99)`** | **16/16** exakta, nio TOP-DOWN-rader, y=96–104, exakt **132 vita screenshotpixlar**, 0 miss/extra |

**32/32 source-pixel-PASS.** X0=**39→45 = +6 crop-pixlar**, X1=**99→99** exakt stabil. Direkt jämförelse av en äkta c21- och c23-frame visar alla **76 ändrade skärmpixlar** inom **x39–60,y96–104**, enbart mannens figur; den övriga faktisk bild är identisk inom analyserad x0–335,y50–194. P0-gul, M0 aktiv, brun PF på bägge sidor och 262 NTSC finns i originala bildrutor och utvecklarens riktade audit (MAIN:s vita-pixelunion verifierar inte själv varenda P0/M0/NTSC-registertransition).

**R1ba:s kända inversionsbugg förekommer inte** här: de två F6-originalmaskerna är byte- och rasterorienterade rätt och sex-P1-par-kernel från R1ba har inte kopierats.

## 4. Registercykler, timing och strikt tolkning

Fem per ROM riktade **äkta GUI-register-traps** vid frame12 scanline123/bank0:
- c21-case första `RESP1 c21 (CC63)` med PC efter `$F147`, första `GRP1 c24`, andra `RESP1 c32`, andra `GRP1 c35`, nästa `WSYNC` skärmövergång visar scan124/c0;
- c23-case första `RESP1 c23 (CC69)` PC efter `$F143`, första `GRP1 c26`, andra `RESP1 c32`, andra `GRP1 c35`, nästa `WSYNC` efter övergång scan124/c0.
- `WSYNC c38` och 38-cykels marginal är **SOURCE_ONLY** från faktisk assembler, inte en synligt uppmätt `WSYNC c38`-skärmtext. Verklig UI-trap bekräftar respektive `RESP1`, men *inte* intern TIA START-puls.
- Äldre röda G0/listningstest har bevarats; tre senare gröna actions `43963655377`, `43963975072`, `43964319661` för två verkliga tester och READ-ONLY ZIP-sammanslagning. F6 producerade exakt **två geometriskt unika** ROM:er.

**VIKTIGT:** Den förregistrerade c21-basmodellen `X43` är direkt FALSIFIERAD (verkligt X39). Det är inte tillåtet att skriva efterhandsjusterad prediktion. Den c23-baserade `X45` är träffad; TIA:s EXAKTA interna START-/latchproveniens är **FORTFARANDE INTE ISOLERAD**.

**Begränsningar:** Det är **TVÅ SEPARATA statiskt byggda ROM:er** med **EN rörlig första bitmap och EN fast andra**. Ingen enda ROM har två självständiga variabla RAM-X, ingen 2×2 runtime-kombinationsmatris, sex originalandroider (2M,2F,SM,SF) på samma band eller fri X/Y, och inga verkliga spelkollisioner/O1/HUD/KEY/GAME OVER. Fullt R1 `BLOCKED / NOT ACCEPTED`, inget R1+R3, R2/R4, PAL/fullspel, PR-merge eller E02 oberoende VERIFICATION.

## 5. MAIN:s separat framtida arkitekturstyrning

F6-mottagningen är AVSLUTAD. MAIN auktoriserar **en enda** [R1-F7 – TWO-MASK TWO-RUNTIME-X-BIT MATRIX DIAGNOSTIC](MAIN_V_TO_ROM_DEV_II_R1_F7_TWO_MASK_TWO_RUNTIME_X_BITS_AUTHORIZED_2026-11-16.md) inom redan godkänd NTSC v0.18 R1-förstudie. F7 får bara testa om de två första positionsfamiljerna är **ortogonalt och oberoende valbara ur två RAM-bitar**, i EN ny ROM och fyra förregistrerade val; den är ingen fri-X-acceptans, sexandroidkernel eller ersättning för R1ba. Inga andra åtgärder startas här.

**Mottagningsklass:** `F6_TWO_MASK_HBLANK_PHASE_LOCAL_PASS / F6_TWO_INDEPENDENT_RUNTIME_X_NOT_RUN / SIX_INDEPENDENT_XY_NOT_RUN / FULL_R1_BLOCKED`.
