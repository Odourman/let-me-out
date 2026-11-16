# MAIN II R1c – tre olika ursprungliga 8×9-masker, STATISKT 600/600 (lokal kontroll)

**2026-11-16.** Ingen full R1 PASS, ingen fri X eller oberoende VERIFICATION.

## Bevis och utförande
- [GitHub Actions run 43786069997 – SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43786069997), testad commit `95390d5f9f97073695586005608ff44b940b4e53`.
- Forskningsgren `research/main-ii-r1c-three-600-20261116`.
- Evidence artifact ID `14190402154` (`main-ii-r1c-3-distinct-masks-600-frame-evidence`), full rå Stella 6.7.1 X11 600 frame PNG + källkod, ROM, `frames_600.csv`, `summary.json`, SHA manifest.
- ROM NTSC standard F6 exakt 16384 byte. SHA256 `da8a360fc9f3db149d1dc12f9b29ef10c4b2220328395b338083839534425da1`. Fyra identiska 4K banker, DASM 2.20.14.1.
- Ursprungliga tre maskerna från `main/design/NPC_REFERENCE_8x9_masks.json` blob `058800a4c1904d1ff289e7e61b3902aa111ba16d` (large_male, large_female, small_male), verifierade i källan och i råbildspixlarna. Den lilla maskens ursprungliga tomma rader ingår.
- I 600 autentiska Stella debuggerbilder, frame-ID 11–610 utan luckor, är samtliga tre olika originalmaskerna exakt `72/72` bitpositioner på nio rader; kontrollen räknar även varje av 2 horisontella GUI-pixlar per TIA-färgklocka.
- Stella HUD visar 262 rasterlinjer i **600/600**, gul P0 och gult M0 är synliga i **600/600**, **0 extra vita pixlar** utanför maskerna.
- `summary.json` har status **`LOCAL_PASS_STATIC_3_MASKS_600`**, `failed_frames_first_10=[]`.
- Fasta positioner i rå 1366×900 Stella-GUI: stor man X166, stor kvinna X280, liten man X394; samma Y, inga positioneringsförflyttningar i dessa 600 bilder.
- Debugger PC-stopp i separat men identisk ROM, [Actions #43785836805](https://github.com/Odourman/let-me-out/actions/runs/43785836805): P1 `STA RESP1` vid `$F088` c23, `$F096` c42, `$F0A4` c61 på scanline119 bank0. 57 TIA-färgklockors avstånd, sista `STA WSYNC` beräknat c72 av 76.

## Negativ observation bevarad
Den första 54-color-clock-varianten [Actions #43785579266](https://github.com/Odourman/let-me-out/actions/runs/43785579266) gav fel 1 bit i stora kvinnans mask (`$FF` blev `$FE`). Korrigeringen använder 3-cykels `BIT FRAMELO` före de två `GRP1`-omskrivningarna och passar rasterbudgeten.

## Begränsningar
- **Ingen fri X-positionering.** Alla tre figurer är statiska i denna körning. Tredje figuren visas nära skärmens högra sida.
- **Endast tre NPC**, inte projektets sex. Inga playfield-väggar, dörrar, nyckel/O1, full rörelse, färdig spelarkonst eller PAL.
- Ingen separat oberoende VERIFICATION för denna nya ROM. Äldre Issue #8-baslinje och ROM DEVELOPMENT:s draft PR #7 har inte ändrats. Forskning är rådgivande, inga commits till `main`, ingen merge och ingen fullspelsauktorisation.
