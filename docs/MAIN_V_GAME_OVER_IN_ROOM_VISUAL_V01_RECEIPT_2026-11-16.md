# LET ME OUT! – MAIN V: GAME OVER – IN-ROOM VISUAL v0.1 – mottagning

**Datum:** 2026-11-16. **Beslut:** Grafikstudien G1/G2 mottas som **avslutad och fil-/maskgranskad GRAPHICS CANDIDATE**. **INGEN** slutgiltig GAME OVER-canon, score-font, färgkod, ROM-implementering, Stella-test eller oberoende VERIFICATION godkänns.

## 1. MAIN:s egen kontroll av faktisk uppladdning

Grafikpaket från [dedikerad Google Drive](https://drive.google.com/file/d/1sky2m5Y8QG4oM0eRiL5HRE2FTOG4S32Y/view), Google Drive parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u` och exakt namn `LET_ME_OUT_GAME_OVER_IN_ROOM_VISUAL_V01_GRAPHICS_CANDIDATES_2026-11-16.zip`. **Riktiga nedladdade bytes** ger:
- **164 694 byte**, **41 ZIP-poster**, ZIP CRC **PASS**, hela filens SHA-256 exakt `23afbe7804d76c1de91e9c31ccc02386a68dd8833b3305ea8374d94b529570f6`.
- `SHA256SUMS.txt` kontrollerad med separat MAIN-script: **39/39 individuella fil-SHA-256 matchar**. Endast `MANIFEST.json` och `SHA256SUMS.txt` själva listas inte.
- Sex faktiska `raw/G1_{A,B,C}_160x176.png` och `raw/G2_{A,B,C}_160x176.png`: samtliga **verkligt 160×176 RGB**, var och en har samma dekodade-pixelbytes-SHA256 som den levererade käll-JSON:en. Offline-källa, **inte verklig Stella/CRT-bild**.
- Fyra faktiska `animations/G1_1X_GAME_OVER.gif`, `G1_4X_GAME_OVER.gif`, `G2_1X_GAME_OVER.gif`, `G2_4X_GAME_OVER.gif`: **3/3 exakta pixelrutor per GIF** jämförda mot källa-PNG i oförändrad 1× samt 4× nearest-neighbor, **alla 12/12 faser MATCHAR**; illustrativa GIF-durations `[900,900,650]` ms, **ej** spelbeslut.
- Den verkliga käll-JSON:ens `room.original_grid_rows` och `SOURCE_C02_GRID.txt` motsvarar exakt C02:s **22 rader à 40 tecken** i aktuella `design/PLANERADE_RUMSKARTOR_V011.json`, GitHub blob `820a74e5fb77c818ffb1286c5b23698d4374e771`: stängd vänsterkant samtliga rader, `D` endast `x=39, y=9,10,11,12`. **Ingen C_OPEN-cutover**.
- I `GAME_OVER_IN_ROOM_V01_SOURCE.json` finns **sex** ursprungsandroider i rätt fördelning 2 stora män / 2 stora kvinnor / liten man / liten kvinna, och alla sex källmaskerna exakt samma som original-`design/NPC_REFERENCE_8x9_masks.json` blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Gul P0 endast `V03_B` **ej godkänd jämförelsesprite**. Den påhittade frozen-snapshoten är **inte** ny logik om att NPC ska överleva GAME OVER.
- Samma `700` scorevärde i käll-JSON över alla faser, `G1_B→G1_C` och `G2_B→G2_C` byter bildpunkter **endast i poängrektangeln x63–96, y88–101** (196 avvikande synliga pixlar), medan sex NPC, P0, väggar och dörr är oförändrade. `G2_A→G2_B`: accent-/score-ändring, rummets grundpalett och karta kvarstår. `G1_A→G1_B`: nästan hela rumspaletten ändras, vilket är uttryckligen koncept G1.
- Separata Drive-filer: [handoff](https://drive.google.com/file/d/1pgYlDLw3qZpCSG63e5DaLQmN23lPIHSq/view) 9093 bytes, [käll-JSON](https://drive.google.com/file/d/1vML4DV6mQEsp2y_OBgR63SZlJq5M7cCX/view) 10082 bytes, [jämförelsebild](https://drive.google.com/file/d/117jtImqqo3Ljw8y4sylYIRFsjejrOOTi/view) 51454 bytes, [G1 GIF](https://drive.google.com/file/d/1_7LstJEdKoivvIDJmdrtC6hT24jnOqZw/view) 20218 bytes, [G2 GIF](https://drive.google.com/file/d/13M4SqyKbLquQM0qpcC54bZSLd97m5ppl/view) 24034 bytes. Samtliga ligger i rätt projektmapp och motsvarande bytes är också bundlade i ZIP.

## 2. Grafisk bedömning

**G1:** färgskifte mellan normal mörk/brun och kall blågrå rumspalett, utan ny titel. Kräver fortfarande faktisk färg-/poängrendering och riskerar att uppfattas som en nivåvariation, paus eller specialläge. Positivt att det inte förutsätter en GAME OVER-textfont. **GRAPHICS CANDIDATE, ej slutgodkänd.**

**G2:** normalt brun/mörkt rum bevaras, lokala vägg-/poängkontrastaccenter, slutpoäng `700` blinkar och **`GAME OVER` visas i den offline-ritade mockupen**. Uppfattas tydligare som slutläge och är **MAIN:s preliminära visuella förstahandsalternativ**, men **starkt VILLKORAT** av att just ny extra text, score-siffror och små väggfärgsskiften över huvud taget får plats i en framtida NTSC 6502/TIA-kernel. Ny `3×5`-bokstavsfont är **endast designhypotes, ej kanonisk grafik eller kodresurs**.

**Kritisk gräns:** inget av koncepten har ROM/Stella-färgtest, skarp CRT-/TV-proportioner, 76-cykel-laserbudget, text- eller sifferkernel, utredd RAM-layout, mänskligt blindtest eller kodad GAME OVER/RESET-logik. Datorn har producerat **offline-pixelart**, inte verkliga TIA-objekt.

**MAIN:s statusbeslut:** v0.1 **avslutad som korrekt grafikdataleverans**, G2 bevaras som **visuell kandidat med blockerad textimplementeringsfråga**, G1 som enklare visuellt reservkoncept. Inget G2-canon-beslut; ingen v0.2 med kosmetiska färgombyten nu. Senare **separat** teknik-/användarbeslut behövs för score/font/RESET. Enligt [användarens beslut](GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md) får **ENDAST konsolens RESET starta om**, FIRE inte; detta har bara **dokumenterats** i dessa grafiker, inte implementerats.

## 3. Nästa fristående grafikuppdrag

[KEY SPRITE – 1× READABILITY v0.1](MAIN_V_TO_GRAPHICS_KEY_SPRITE_READABILITY_V01_2026-11-16.md) är ett **nytt, snävt GRAPHICS-uppdrag** med högst två fasta nyckelmasker – en 8×9, en 8×11 – för att överväga visuell läsbarhet, litet gyllene ringhuvud, verkligt hål, kort skaft och små tänder. Utgår från användargodkänt visuellt mål [v0.13](KEY_AND_DOOR_VISUAL_TARGET_V013.md) och obundna K09/K11-maskskisser, [v0.14 kontrast](KEY_CONTRAST_RGB_REVIEW_V014.md), godkänd O1-skymning [senare supplement](MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md), [v0.15 separat logisk studie](KEY_OCCLUSION_LOGIC_V015.md) och D1 death key-after-death storyboard. Får **inte** auktorisera keyspawn, RAM, TIA-resurs, R2-kod eller PAL. Tidigare grafisk GAME OVER-order stängd.

## 4. Tekniskt projektläge, oberoende av denna grafikmottagning

Full R1 sex individuellt fritt X/Y `BLOCKED/NOT ACCEPTED`; ROM DEV R1-F3:s enda index0 +1-cykelprov gav geometry FAIL, två oberoende runtime-X NOT_RUN. PR#7 draft, Issue#8 verification standby. Denna rapport startar ingen ny kodfas, gör inget P0/score/PF-mutation i repository och ändrar inte någon ursprunglig referens, ROM, spelregel eller cutover.
