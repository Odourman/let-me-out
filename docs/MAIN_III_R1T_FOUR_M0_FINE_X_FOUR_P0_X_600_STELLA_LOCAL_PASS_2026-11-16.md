# LET ME OUT! – MAIN III R1t: trick #10 + #24, fyra M0-skott-X och fyra P0-X i samma verkliga ROM

**Datum:** 2026-11-16. **Status:** `LOCAL_PASS_R1T_FOUR_M0_X_FOUR_P0_X_600`, strikt **isolerad forskningsdemonstration**. **Full R1 fortfarande FAIL/BLOCKED.** Inget designbeslut, implementationsgodkännande eller oberoende VERIFICATION.

## 1. Direkt bevis och reproducerbarhet

[GitHub Actions **#43843808615**](https://github.com/Odourman/let-me-out/actions/runs/43843808615): **SUCCESS**, testad källcommit `3de41d8a4a39b81eb98c7dff09c7bf76c8749c11`. Proveniens: research branch `research/main-iii-r1t-four-missile-x-hmove-20261116`, byggd från exakt pinad och lokalt validerad R1s-ROM-hash `33ab04b95ca6f649593e50082bf17275b605caea282e6e044aeb49abf93d1d85`.

- **ROM:** 16 384 byte vanlig **F6/NTSC**, fyra identiska 4 KB-banker.
- **R1t ROM SHA-256:** `db14c067d386c0f4040a6208f8d97b29f5dbe2568c36d5421da8d0491e25743e`.
- **GitHub Actions evidensartefakt:** [#14213708043](https://github.com/Odourman/let-me-out/actions/runs/43843808615/artifacts/14213708043), 622 poster, inklusive **600 på varandra följande faktiska Stella 6.7.1/X11-PNG**, källa/ROM/DASM-listing/symboler, CSV, `summary.json`.
- **Nedladdad råevidens-ZIP SHA-256:** `d980aed758c9d88985e39f209482400326aebde9bc04a80807d772a37514b972`, **ZIP CRC PASS**.
- **Kompakt research/handoff ZIP SHA-256:** `d57616734f352733b7c7e93b8ee3a45d4aab1a232bf3588650a171a6d8877fdb`, innehåller exakt ROM, källa, screen-crops, CSV och summering.

Första [GitHub Actions #43843646816](https://github.com/Odourman/let-me-out/actions/runs/43843646816) stannade **före emulering** i bygggeneratorns etikettassertion: `MaleRows:` hittades av en substringkontroll också i `SmallMaleRows:`. Kontrollkoden ändrades till exakta helradsetiketter. Ingen maskingrafik ändrades eller audit mjukades upp. Vid omkörning av samma ändring genomfördes full 600-frame audit med SUCCESS.

## 2. Oberoende förflyttning i liten skala

`HMM0` sätts före varje rasterbilds `HMOVE` från en **fyrpoststabell i ROM**. Tabellen styrs av `FRAMELO & $0C` (upprepas i 4-frame-slag) och är helt oberoende av `FRAMELO & $30` (lilla kvinnans fyra P0-X) och `FRAMELO & $40` (högerdörr).

| HMM0 tabellbyte | Verklig mätt M0 GUI-X | Frames |
|---|---:|---:|
| `$40` | **232** | 150 |
| `$30` | **234** | 148 |
| `$20` | **236** | 150 |
| `$10` | **238** | 152 |

Skottet kvar på **GUI y167**, direkt vid/till höger om gula testspelarens hand. Skottets M0-enable/disable-kernel från R1s ändras **inte**, och hela M0-rörelsen sker i positioneringsfas utanför NPC:s synliga scanlines. Fyra separata M0-X är faktiska Stella-pixlar, inte en simulator eller offline-genererade positionskurvor.

## 3. Fullständiga hårda pixelfakta från 600 frame

| Test | Verkligt utfall |
|---|---:|
| 600 konsekutiva Stella-frame-ID, utan luckor | **600/600** |
| NTSC **262 rasterlinjer** | **600/600** |
| Fem samtidiga kompletta originalmaskinstanser (1 stor man, 2 stora kvinnor, 1 liten man, 1 liten kvinna) vertikalt visade i 14 rader | **600/600** |
| Gul temporär spelare och exakt **EN** M0 på y167 i ett av fyra X | **600/600** |
| Fjärde lilla NPC x330/x348/x360/x378 korrekt | **600/600** |
| Höger 32-raders PF0-dörr och vänster BALL-vägg | **600/600** |
| **Alla 4 M0-X × 4 P0-X × 2 dörrläge** | **32 av 32**, minst 16 frame per kombination |
| Gammalt skott på huvudlinjen y160 | **0** |
| Oönskade extra gula eller vita bildpunkter | **0 + 0** |
| Oförändrade ursprungliga 8×9-bitmapbytes och deras tidigare härledda 14 visade rader | **PASS** |

Detta omfattar både Stella screenshotbaserad fail-closed audit och **separat lokal nedladdningsgranskning**. Vid separat kontroll beräknades SHA256 över **spelområdet** för alla 600 verkliga PNG och jämfördes med auditens 600 CSV. Resultat: **32 olika scenhashar**, exakt en för varje X-M0 × X-NPC × dörr-kombination, aldrig två olika skärmbilder för samma logiska läge och ingen delad scenbild mellan olika logiska lägen. Avsiktligt exkluderades Stella HUD/counter från bildhashen.

## 4. Vilka av de 30 programmeringstricken används?

- **#10 HMOVE Fine Positioning:** används direkt: tabellen ändrar `HMM0`, och `HMOVE` i horizontal blank flyttar missilen. Behåller `HMBL` och all annan finpositionering oförändrade.
- **#24 Precomputed Tables and Cycle-Exact Kernels:** fyra `HMM0`-värden ligger färdiga i ROM, val görs före det synliga figurbandet. Inga instruktioner läggs till inne i de 14 kritiska NPC-raderna.
- **#14 Multiple Display Kernels:** befintliga R1s använder fyra olika P0-rader och en egen skottrad; själva R1t-provet ändrar **inte** dessa rasterrutiner. Tekniken blir viktig om skottet ska långt över hela skärmen.
- **#15 NUSIZ Sprite Duplication:** används och dess negativa missilkopiebeteende undviks med den tidigare bevisade R1s-avstängningen.
- **#20 Hardware Collision Latches:** **inte prövat**. `CXM0P`, `CXM0FB` och `CXCLR` kan signalera överlappning men inte direkt vilket logiskt P0/P1-multiplexat NPC-ID som träffats; det kräver separat logisk hitboxmappning/test.

Teknisk primärreferens: *Stella Programmer's Guide*, sektionerna 6.1 och 7 om M0, NUSIZ och HMOVE; den separata ursprungliga 30-trick-listan `LET_ME_OUT_30_URSPRUNGLIGA_ATARI_TRICK_MAIN_2026-11-16(3).md` har använts för riktig #numrering.

## 5. Hårda begränsningar – ingen fullspelsclaim

**Det som faktiskt bevisats:** En och samma F6-ROM kan förflytta ett ensamt skott mellan **fyra närliggande, diskreta** GUI-X 232/234/236/238, **oberoende** av de fyra sen tidigare bevisade NPC-X och dörrens två lägen, med fem hela originalandroider i 14-radspresentation och ingen extra projektil eller en enda spökpixel.

**Inte bevisat:**
1. **Hela skärmbredden:** detta är bara 6 GUI-bildpunkters förflyttningsintervall (3 TIA color clocks); det är **inte** ett fritt rörligt skott från hand till högerkant. M0:s enable-fönster i R1s är fortfarande specialiserat för tidiga X och kan behöva bytas/riktas om för senare skottpositioner.
2. **Riktig spelmekanik:** ingen eldknapp, skotthastighet, automatisk vidareförflyttning, försvinnande vid träff/kant, kollisionsregisterläsning eller identifierad NPC-träff. Rörelsen är deterministiskt driven av `FRAMELO` som ett mätprov, inte logiskt bullet-RAM-tillstånd.
3. **Full R1-sex-NPC:** sjätte originalstor man saknas. De två stora kvinnornas P1-X är inte fria oberoende positioner; fjärde P0 har endast fyra diskreta X. Ingen 160-color-clock-frihet för alla sex, ingen fullständig originaldesign/karta/nyckel/orange dörr/nyckelhål.
4. Ingen oberoende formell VERIFICATION, inget produktionsgodkännande, ingen PAL, inget byte av F6-mapper.

**Nästa rådgivande, isolerade test:** kartlägg maximalt M0-X med samma R1s-synliga kernel genom en finpositions-svepning. Om den senare kolumnen går utanför R1s:s aktiveringsfönster, prova separata **skottrutiner per horisontell region** (#14) med olika M0-on/off-deadlines, men lämna fem originalmasker och alla fyra P0-X orörda. Testa `CXM0P`/logiska hitboxar (#20) separat och fail-closed innan något kallas träffregistrering.

**Integritet:** `main`, ROM DEVELOPMENT:s draft PR #7 och VERIFICATION-issue #8 är inte modifierade av denna forskningsgren. Full R1 är fortsatt **FAIL/BLOCKED**.
