# LET ME OUT! – MAIN V: KEY SPRITE – NATIVE 1× READABILITY v0.1, mottagning

**Datum:** 2026-11-16. **Beslut:** grafikdataleverans mottagen och avslutad; **K09-R är preliminär huvudsaklig GRAFIKKANDIDAT**, K11-R dokumenterad reserv. Inget användar-slutgodkännande av nyckelbitmap, ingen NTSC/TIA-palett, Stella, ROM, R2-nyckelrendering, faktisk O1-överlapp eller oberoende VERIFICATION.

## 1. Verifierade källor och direkt nedladdade byte

MAIN hämtade via ansluten Google Drive följande **riktiga projektfiler**, samtliga i föräldermapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`:
- [Original ZIP](https://drive.google.com/file/d/1y7SaRC4nJ9NCZ5k918Tp8yhz2nO5MkFJ/view), `LET_ME_OUT_KEY_SPRITE_READABILITY_V01_GRAPHICS_CANDIDATES_2026-11-16.zip`: faktiskt **297 376 byte**, **118 ZIP-poster**, `ZipFile.testzip()==None` (CRC PASS), full SHA256 **`ef0ed4c378e41363f29804b8ed1ff45c260bafb4b173716d06a38e1e74e9e975`**, matchar leverans.
- `SHA256SUMS.txt` uppgick till **116/116 hashade filer som alla matchade faktisk ZIP-entry-data**, övriga 2 poster `SHA256SUMS.txt` + `MANIFEST.json`.
- [GRAPHICS-handoff](https://drive.google.com/file/d/18chdSi_10S7szwRHyrnE-9k2TtiVivil/view) faktisk 7 512 byte, [nyckelmask-JSON](https://drive.google.com/file/d/1QQlLuuUdHLF53mv5lrYEHZpHPpRPCdJB/view) 17 291 byte, [exakt comparisons-PNG](https://drive.google.com/file/d/1_e2XzpwqgueN7zcc_ZE2vaQRVjwlxV9F/view) 83 450 byte, [D1/O1 storyboards](https://drive.google.com/file/d/1cL6nMb_f1p1MmaqQjUgI6fQwrKdB5DEu/view) 65 035 byte, [K09-R efter död GIF](https://drive.google.com/file/d/19M0PT8dQGp22itL25r1gx3RHIqVeKMay/view) 30 263 byte, [K09-R skymning GIF](https://drive.google.com/file/d/1WlrRupIhKYZgm5PezRZnDq8nMPEY2Qv7/view) 24 623 byte. Alla länkade artefakter bekräftades i rätt mapp och laddades ned i sin faktiska filform.
- MAIN:s eget separata audit-skript beräknade från faktiska bitmaprader **råbytes-SHA256, CRC32, hex, tända pixlar, bit-differenser**, testade topologiskt helt inneslutet hål som 4-neighbor-connected komponent av tomma pixlar utan kontakt med bildkanten, och jämförde alla fyra ursprungliga och reviderade nyckelmaskerna bit för bit mot både `deep_gold` och `near_yellow` **8×9/8×11 verkliga 1× PNG**. Allt PASS.
- `sources/NPC_REFERENCE_8x9_ORIGINAL_UNCHANGED.json` har SHA256 **`1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`**, matchar låst ursprung och nuvarande GitHub original blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. `C02_original_cell_grid` är 22×40, byteordnade rader utan slutnewline SHA `9247cc46c7003b1011b43af333f2876279f196167277813e78a718faf54a0460`, matchar godkända **C02** i `design/PLANERADE_RUMSKARTOR_V011.json`, dörr x39 y9–12 och alltid sluten vänsterkant.
- MAIN verifierade **alla 8 faktiska animations-GIF:er** (K09-R/K11-R × death/O1 × 1×/4×), jämförde varenda av deras GIF-rutor med motsvarande verklig PNG, kontrollerade antal rutor (D1 5, O1 4) och exakta **endast illustrativa** GIF-tider. PASS. D1 (för båda kandidaterna): guldnyckel vid `(132,80)` är **0 färgpixlar** i de första **fyra** scenrutorna ORIGINAL/HIT/DISSOLVE/EMPTY och framträder först i **femte** `KEY_VISIBLE` (K09-R exakt 30 guldfärgade pixlar, K11-R exakt 36). O1: nyckelregionens exakta pixelbytes vid första synlig och fjärde återkomst är lika för båda. Detta kontrollerar OFFLINE-visuell ordning, **inte** TIA-spriteöverlapp, RAM-tillstånd eller collision.

## 2. Fyr-mask-baserat MAIN-beslut

| Mask | Storlek | Pixlar | Topologiskt slutet mörkt hål | Ändrade bitar från motsvarande tidigare jämförelse |
|---|---|---:|---:|---:|
| K09 (historiskt, **ej slutgodkänt**) | 8×9 | 34 | 2 | – |
| **K09-R (ny, föredras)** | **8×9** | **30** | **6, 2×3** | **12** |
| K11 (historiskt, ej slutgodkänt) | 8×11 | 41 | 4 | – |
| K11-R (ny, reserv) | 8×11 | 36 | 12 | 15 |

**K09-R exakt niobytesmask: `3C 66 66 66 3C 18 1C 18 1C`**, rå-SHA256 `12dfe9ca1d9b5234fdc9ea4e507cd7e1a3fd3006ab02baedd9b22eafef8afa8d`.

**K11-R elvabytesmask: `3C 66 C3 C3 66 3C 18 1C 18 1C 18`**, rå-SHA256 `14e08f1eed72239ecc6e4f0129d762ba2ef480cea39a179bff64bc597fad7a94`.

**Grafiskt omdöme:** K09-R skiljer ut ett sammanhängande ringhuvud, 2×3 hål, kort skaft och två enkla högertänder utan att vara högre än stor androids nio synliga maskrader. K11-R visar större ringhål när det förstoras men i faktisk 1× mindre säker förbättring och två ytterligare bildrader/råbytes (+22,2 % data, inte ett verifierat 22 % total CPU-tillägg). 8×11 ökar okänd raster-/objektkonfliktrisk. **K09-R föredras**, K11-R förvaras men inget design-waiver eller faktisk bitmapgodkännande utfärdas. Färg `#F2AD00` / `#FFDE00` endast schematisk RGB, inte en validerad Atari 2600-färgkod. Normal TV-/CRT-distans och oberoende blindläsbarhet **EJ TESTAD**. Hålet är matematiskt slutet, men tändernas faktiska läsbarhet är subjektiv.

**Mottagningsklass:** `KEY SPRITE v0.1 COMPLETE AS GRAPHICS STUDY / K09-R FIRST-CANDIDATE / NOT USER APPROVED / NOT STELLA TESTED / NO ROM AUTHORIZATION`. Original-NPC, PLAYER V03-B (inte slutgodkänd), D1, G2, regler, dörr/nyckelhål och kartor förblir oförändrade.

## 3. Nästa separata GRAPHICS-uppdrag och teknikgräns

Nästa *nya avgränsade grafiska förstudie* är [SCORE & LIVES HUD – VISUAL v0.1](MAIN_V_TO_GRAPHICS_SCORE_LIVES_HUD_VISUAL_V01_2026-11-16.md). Originalbeslut `03_DECISIONS.csv` #042–050 binder poängstart 0, nollgolv, -25 android, +50 nyckel, +100 faktisk utgång, +15 per kvarlevande android, highscore efter **endast poäng**, tre startliv och extraliv 500,1500,2500,... en gång. Därmed finns legitimt grafiskt behov av siffror och liv, men **poängdisplayens maximala antal siffror, HUD-layout, font, palett och högsta liv** är ännu öppna; GAME OVER G2 text är endast preliminär grafikhypotes. Ingen utformning av ett HUD i denna framtida studie får bli ny canon/scorelogic. Hela R1 är fortfarande `BLOCKED/NOT ACCEPTED` enligt senaste R1-F3-diagnostik. **Ingen ROM**, score, HUD-kod, KEY-spawn, R2 eller TIA-/BANK-implementation får starta på grund av detta beslut.
