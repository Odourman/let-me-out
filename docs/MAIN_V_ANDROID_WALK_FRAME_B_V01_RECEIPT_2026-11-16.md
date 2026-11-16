# LET ME OUT! – MAIN V: ANDROID WALK FRAME B v0.1 mottagning

**Datum:** 2026-11-16
**Beslut:** GRAPHICS v0.1 för gång-Frame B är **avslutad och mottagen som grafiskt arbetsunderlag**, inte som godkänd ny canon, färdig gånganimation, Stella-pass eller ROM-leverans.

## 1. Byte-exakt mottagning av de faktiska Drive-artefakterna

MAIN har med Google Drive-anslutningen läst metadata och laddat ned samtliga sex direktlänkade artefakter. De ligger i dedikerad projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.

- [Komplett ZIP](https://drive.google.com/file/d/10LToEGV-KGQyB4LpixIMV-q02S6qujAx/view), faktiskt **201 031 byte**, **84 ZIP-poster**, CRC PASS och hela ZIP SHA-256 = **`a7c64912f24b0ceada20aac90d99c738882c24ad2730d347bcc71141713e9c3f`** (samma som GRAPHICS rapporterar).
- `SHA256SUMS.txt` har **83/83** matchande filhashar; det enda undantaget är hashmanifestet självt.
- [Handoff](https://drive.google.com/file/d/1ior8uqC4KijDt_JPCtwuS_Gca1Lgnz-k/view), **9 237 bytes**; [JSON-maskdata](https://drive.google.com/file/d/1NPJNmqh6DwPK6Hpmf5JKx_e6FVTWJ6zu/view), **10 409 bytes**; [jämförelsebild](https://drive.google.com/file/d/1z3IMppAsktONPtCCDeAT80GBbQRlPhI2/view), **103 201 bytes**; [sexfigursmontage](https://drive.google.com/file/d/1Q7oZtvgOguGk9zTcUyf8SZUD70_KzGd3/view), **59 063 bytes**; [1×/20× GIF](https://drive.google.com/file/d/1UD-orTTnwQSJNQmqeYzdgu-fK3rIF8fO/view), **31 442 bytes**. Alla är designframställningar, inte Stella-bevis.
- MAIN har själv kontrollerat varje ursprunglig `FRAME_A` byte för byte mot original-`NPC_REFERENCE_8x9_masks.json`, vars innehåll har ursprunglig SHA-256 `1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`. **Fyra originalmasker är orörda.**
- MAIN har separat granskat **alla åtta verkliga 8×9 1×-PNG**, pixel för pixel mot JSON:s A/B-rader, samt original- och B-maskernas niobytes-SHA, antal aktiva pixlar, bitändringsantal. Individuella **fyra** 1× GIF har exakt **3 frames A→B→A**, varje frame är byte-/pixelmässigt rätt och intervallet är **280ms i offline-grafik**. Sexfigurs-GIF har också exakt A→B→A. Allt PASS som **fil- och pixelintegritet**, inte som mänsklig läsbarhet eller emulator-/hårdvarubevis.

## 2. Fyrtypers grafikbeslut

| Androidtyp | A-pixlar | B-pixlar | Bitändringar | MAIN:s grafiska bedömning |
|---|---:|---:|---:|---|
| Stor man `large_male` | 28 | 29 | 7 | **B tillräckligt tydlig för fortsatt kandidatförvaring**; armar/ett knä rör sig, men två nedersta fotrader är exakt oförändrade och kan uppfattas som armgest snarare än gång. |
| Stor kvinna `large_female` | 38 | 39 | 7 | **B tillräckligt tydlig för fortsatt kandidatförvaring**; kjol och typidentitet bevaras; främst armsväng och begränsad knäförflyttning. |
| Liten man `small_male` | 20 | 20 | 4 | Rörelse subtil, armförskjutning syns men **gångillusion ej säkert bevisad i 1×**. |
| Liten kvinna `small_female` | 22 | 23 | 3 | **Svagast**; kan uppfattas som arm-/kjolfladder snarare än steg. **Ingen slutfärdig gångbild.** |

Alla `FRAME_B` är EXAKT 8×9, de stora använder nio synliga rader och de små sex synliga på y=2–7. Alla fyra har exakt bevarad fotrad. Materialet förfogar över **36 extra råa bytes** (4 × 9), men detta ger inte automatiskt tillgång till grafikbyte på en överfull P1-kernel eller individuella sexfasanimationer.

**Mottagningsstatus:** `GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD` för varje B. Frame A oförändrad. GRAPHICS-WALK-B-studien **avslutas efter en leverans**; MAIN beställer inte nya små gångrörelsepixelvariationer eller ROM-införande nu. Glidande rörelse är uttryckligen tillåtet reservläge.

## 3. Nästa avgränsade designuppgift, utan ROM-ändringar

Enligt den ursprungliga 57-beslutshandoff `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip`:
- `02_MASTER_SPEC.md`: **en gemensam dödsanimation för samtliga androider**.
- Dödad nyckelbärare: **nyckeln syns på den bevarade dödspositionen först NÄR animationen är helt färdig**, aldrig parallellt med anim.
- `03_DECISIONS.csv` original-ID **010** (gemensam dödsanimation), **023** (nyckel efter dödsanimation).
- Inga spelregler eller faktisk nyckel-/döds-/maskintegration är implementerade eller auktoriserade av grafisk mottagning.

Nästa designorder är [COMMON ANDROID DEATH ANIMATION v0.1](MAIN_V_TO_GRAPHICS_COMMON_ANDROID_DEATH_ANIMATION_V01_2026-11-16.md): en gemensam lågkostnads-animation, högst två visuella tillvägagångssätt, originalmaskerna oförändrade, tydlig nyckel/icke-nyckel storyboard efter sista animationen. **Bara GRAPHICS-arbete.**

## 4. Teknikgräns

Senast frysta specialist-R1-F3 `65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190` rapporterar en **reell** misslyckad x0 +1 CPU-cykel-geometritest vid P1 c19→20 men inga två individuellt runtimestyrda X. Full R1 **BLOCKED / NOT ACCEPTED**, R3 endast isolerad utvecklar-pass, R2/R4/nyckel ej implementation. PR#7 omergerad, VERIFICATION standby, ingen ny teknisk uppgift genom denna grafikleverans. Ingen ändring i The Cabin, I Love a Fish eller Linear.
