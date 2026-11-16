# LET ME OUT! – MAIN III R1u: åtta projektil-X tillsammans med fyra NPC-X och fem fullständiga androidinstanser

**2026-11-16. Status `LOCAL_PASS_R1U_EIGHT_M0_X_FOUR_P0_X_600`; endast isolerad research. Full R1 fortfarande FAIL/BLOCKED. Ingen auktoriserad implementation eller oberoende VERIFICATION.**

## Verifierat research-resultat

[**GitHub Actions #43844430592**](https://github.com/Odourman/let-me-out/actions/runs/43844430592): **SUCCESS**, testad exakta commit **`ca647cb5d29aef4ad7c25da6bc6ea7fa362ba111`** på gren `research/main-iii-r1u-eight-m0-x-window-20261116`. Bygget använder samma standard **16 384-byte F6/NTSC-ROM** som tidigare. R1t-basens korrekta byte kontrolleras på hårdlåst SHA `db14c067d386c0f4040a6208f8d97b29f5dbe2568c36d5421da8d0491e25743e`.

- **R1u-körbar ROM SHA256:** `ba06c63fd2247a4dfd47b5baa5619271c3ac851859c3ba3ca516bd4c227fc2e7`.
- [**Evidens från Actions #14215210636**](https://github.com/Odourman/let-me-out/actions/runs/43844430592/artifacts/14215210636); nedladdad ZIP SHA256 `b10022569866468268c1d1fce490ceae4c52d6b96309f380c3c905d9718cddf2`, ZIP CRC godkänd, **600 autentiska Stella 6.7.1-X11-skärmbilder**, ROM, DASM-källa/listing/symboler, CSV och `summary.json`.
- **Kompakt handoff-ZIP**: `Let_Me_Out_R1u_Research_To_MAIN.zip` SHA256 kommer att registreras separat, med ROM, hela källunderlaget, 600-raders audit-CSV, summary och skärmbild.
- Användarens designkrav: ingen skjutanimation; skott ska börja vid spelarens arm och vara en enda projektil.

## Testade åtta X-positioner

R1u är en **större finpositionssvepning** än R1t: `HMM0` väljs med `FRAMELO & $07`, där skottets X ökar ett steg **varje bildruta** i den här test-ROM:ens deterministiska åttafas-sekvens. `HMM0` används vid HMOVE i blankningsraden, inte inne i den kritiska 14-raderskärnan. Samtliga tidigare NPC- och player-bitmapmasker bevaras bit för bit.

| HMM0 | Faktiskt uppmätt Stella M0-X (GUI) | Frame |
|---|---:|---:|
| `$40` | 232 | 75 |
| `$30` | 234 | 75 |
| `$20` | 236 | 75 |
| `$10` | 238 | 75 |
| `$00` | 240 | 75 |
| `$F0` | 242 | 75 |
| `$E0` | 244 | 75 |
| `$D0` | 246 | 75 |

Samtliga M0-figurpunkter är på **GUI-y167**, direkt på samma armhöjd som i R1s. På x246 ligger den ensamma tvåpunktsshoten precis före den första stora kvinnans fullständiga originalmask som börjar vid GUI-x248. Det är en **14 GUI-pixlars X-svepning, inte en full 160-color-clock resa**.

## Faktisk granskning – 600/600

| Exakt krav | R1u |
|---|---:|
| Konsekutiva Stella frame-ID | **600/600** |
| NTSC 262 rasterlinjer | **600/600** |
| Fem kompletta samtidiga originalandroid-instansmasker, härledda 14 raders presentation, ursprungliga 8×9-byte oförändrade | **600/600** |
| Gul temporär spelare med exakt en M0 på y167 på angiven X | **600/600** |
| Inget gammalt skott vid GUI-y160 | **600/600** |
| Ingen oönskad extra M0-kopia eller spökpixel av någon färg | **0 pixlar** |
| Fyra helt korrekta X-lägen för fjärde P0-androiderna | **x330,348,360,378, samtliga** |
| Två högerdörrslägen + 32-raders öppning + vänster BALL-vägg | **600/600** |
| **8 M0-X × 4 P0-X × 2 dörrlägen** | **64/64 kombinationer**, minst 8 frames per tillstånd |

Från separat lokal nedladdningsanalys: ZIP-innehållets **600 verkliga PNG** öppnades ett och ett; samtliga **600 CSV-rader** har `local_pass=True`. SHA256 över spelregionen (debuggertexten exkluderad) gav **64 unika stabila bildhashar**, exakt **en per kombination av M0-X, fjärde-NPC-X och dörrläge**. Detta är extra reproducerbarhetsgranskning av data, **inte oberoende formell VERIFICATION**. Visad jämförelsebild är endast beskärning och pixelzoom av autentiska Stella-rutor, inte syntetiskt ritad scen.

## Koppling till de ursprungliga 30 tricken

- **Trick #10 – HMOVE Fine Positioning:** bevisat för M0 i integrerad fem-NPC-kernel med åtta uppmätta X.
- **Trick #24 – Precomputed Tables and Cycle-Exact Kernels:** förberäknade åtta `HMM0`-värden sparar CPU-operationer i den redan fullbelastade synliga scanline-kerneln.
- **Trick #14 – Multiple Display Kernels:** befintliga fyra NPC-X-rutiner + specialiserad M0-skottrad återanvänds. Krävs sannolikt ytterligare varianter om en kula ska färdas förbi den första kvinnan till höger rumshalva.
- **Trick #15 – NUSIZ Sprite Duplication:** tidigare lösta R1s-avstängningen hindrar den oönskade extraprojektilen, 600/600 även med skott som flyttas.
- **Trick #20 – Hardware Collision Latches:** **inte testad**. Framtida M0-kollision med kvinnan vid x248+ måste kontrolleras i både TIA:s `CXM0P` och logiska NPC-hitboxar. Att skjuta förbi en NPC skulle också kräva fastställda gameplayregler; detta prov har inte lagt till någon skadelogik.

## Hårda kvarstående gränser

**Detta är inte ett färdigt skott som färdas över skärmen:** bara en sekvens om åtta nära X-positioner med 2 GUI-pixlars steg, som upprepas efter åtta bildrutor. Ingen eldknapp, ingen persistent kulposition eller rörelsehastighet efter skott, ingen detektion av träff/vägg, ingen döda-android-logik. På position x248 börjar den första stora kvinnan: dels blir **kollision** möjlig, dels kan nuvarande tidiga M0-avstängningsfönster inte förutsättas klara X längre åt höger. Detta har **inte** testats eller godkänts.

Bara **fem** simultana NPC-maskinstanser, andra stora mannen saknas. Fjärde P0 bara fyra diskreta X, stora P1-kvinnor har låst relation, inte sex individuellt fria X. Inga godkända nya grafikmasker, full karta, orange dörr/nyckelhål, nyckel, PAL eller full R1/R2–R4. Inget mallbyte: fortsatt F6.

**Rekommenderad separat forskning:** förflytta skottet till x248 för att läsa verkliga `CXM0P`-latchar, bedöma white mask-occlusion samt prova nästa M0-enablerasterfönster (#14) utan att kompromissa om en enda androidmask eller skapa M0-kopior. Detta är rådgivande; innebär inte implementationsauktorisation. **Full R1 kvarstår FAIL/BLOCKED.** `main`, ROM DEVELOPMENT:s draft PR #7 och fristående VERIFICATION issue #8 har inte ändrats.
