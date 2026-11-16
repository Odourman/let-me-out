# MAIN II – trick #05 Dynamic Playfield Sprites: 4/4 separata PF-rasterprov i verklig Stella

**Datum:** 2026-11-16. **Klassificering:** `LOCAL_PASS_PF1_COARSE_SPRITE_SEPARATE_BAND` (egenkontroll), **inte** en extra same-Y originalandroid, **inte** en R1 PASS och **inte** oberoende VERIFICATION.

## Exakt källmatchning och reproduktion

- Ursprunglig teknik: punkt **05, Dynamic Playfield Sprites** i `main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md`; PF0/PF1/PF2 är 4 TIA-färgklockor breda per PF-pixel och playfielden ritar ett upprepnings-/speglingmönster i bildens andra halva.
- [GitHub Actions run 43814436467 – SUCCESS alla steg](https://github.com/Odourman/let-me-out/actions/runs/43814436467), testad commit `675249d2b5d273f2ee4685b4a057122adc2661e7`, gren `research/main-ii-trick05-dynamic-pf-20261116`.
- Artefakt **14201971767**, `main-ii-trick05-dynamic-pf-stella-evidence`: 55 filer med fyra reproducerbara 16KB standard-F6/NTSC-ROM, källor, DASM-list/sym, verkliga Stella 6.7.1 skärmbilder, manifest och `audit.json`. ZIP-integritet `testzip()==None` kontrollerad efter nedladdning.
- Samtliga fyra ursprungliga NPC 8×9-masker kommer oförändrade från R1e-styrkällan `main/design/NPC_REFERENCE_8x9_masks.json`; inga grafikavsteg eller designwaiver.
- PF-provet skriver `PF1` 9 gånger i ett eget PF-band **ovan** 9-raders NPC-bandet. `COLUPF=$36` ger brun färg. Varje ROM förskjuter original-PF-mönstret 1 eller 2 PF-bitpositioner. `TopLines` minskas från 79 till 70 för att rymma nio egna PF-rader: **totalt 262 NTSC-rasterlinjer**.

## Verkliga råa Stella-pixelmätningar

Mellanraden för PF-figuren (Stella GUI y156), uppmätta sammanhängande färggrupper. **En PF-bit = 4 färgklockor = 8 GUI-pixlar.** Grupperna upprepas med 160 GUI-pixlar = **80 TIA-färgklockors fast avstånd**.

| Variationsnamn | Vänster PF-färgsegment GUI-X | Höger kopia GUI-X | Byte mot föregående |
|---|---|---|---|
| `left2` | 168–199 | 328–359 | baslinje |
| `left1` | 160–191 | 320–351 | −4 TIA CC |
| `right1` | 144–175 | 304–335 | −8 TIA CC |
| `right2` | 136–167 | 296–327 | −4 TIA CC |

Åtta PF-bitsteg täcker maximalt 32 CC; kopian i andra halvan är INTE ett tredje oberoende P0/P1-objekt. Varje variant innehåller **320 identiskt färgade GUI-pixlar** i hela bruna PF-bandet. Förflyttningen har verifierats som en exakt translation av samtliga färgpixlar, inte enbart bounding box.

- **4/4** PC/ROM-variantbilder: 262 scanlines.
- **4/4**: 0 fel i var och en av fyra olika godkända NPC-originalmasker.
- **4/4**: 0 fel i gul temporär P0-spelares mask.
- **4/4**: ett enda gult M0-skott på raw GUI x240–241 y160.
- **0 extra vita och 0 extra gula pixlar** i NPC:s 9-radersband i alla fyra.
- `audit.json` status `LOCAL_PASS_PF1_COARSE_SPRITE_SEPARATE_BAND`, samtliga fyra varianter `local_test_pass=true`.

## Begränsning för R1 och nästa forskningsgrind

Detta bevisar att **PF kan rita och flytta grov extra grafik i ett SEPARAT rasterband** utan att störa fyra statiska originalandroidmasker. Det är inte fyra ytterligare högupplösta sprite-kanaler; PF:s 4-färgklockorspixel breder ut formerna, playfielden upprepas i två delar, och den delar resurs med de bruna väggarna och högerdörren. Ingen skärmkontroll har gjorts för **PF-figur och fyra originalandroider på samma nio fysiska rasterrader**. Ingen samtidig full rumskarta/vägg-/dörr-PF, 600 sammanhängande bilder, objekt-AI, fri X eller oberoende VERIFICATION.

**Teknik 05 har därmed en egen praktisk Stella-provning och ett positivt begränsat PF-bandresultat; ingen uppgradering till R1.** Vid separat forskning bör PF-/väggkonflikten testas med ett verkligt asymmetriskt R3-playfield, utan att offra originalmaskerna. Ingen ändring av `main`, ROM DEVELOPMENT PR #7, oberoende Verification Issue #8, F6-format eller godkända spelregler.
