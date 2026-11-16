# MAIN II – R1f: FJÄRDE NPC:s X frikopplad från gul P0, 600/600 riktiga Stella-bildrutor

**Datum:** 2026-11-16. **Resultat:** `LOCAL_PASS_R1F_INDEPENDENT_FOURTH_X_600`. **NYTT:** en och samma körbara standard-F6-ROM växlar fjärde original-NPC:s position **utan att flytta spelaren** och utan att förlora någon av fyra olika original-8×9-masker. **Begränsat tvålägesbevis, inte full fri X / inte sex NPC / inte oberoende VERIFICATION / ingen full R1 PASS.**

## Primär evidens, 100 % reproducerbar i GitHub Actions

- [GitHub Actions `43815510141` – hela bygg- och testkedjan SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43815510141).
- Testad kodcommit `81b9932782b71f82fb8c4c00340e1723e51b705d`; separat branch `research/main-ii-r1f-independent-x-600-20261116`. Senare dokumentationscommits ändrar **inte** den testade ROM-koden.
- Artefakt **`14201559185`**, `main-ii-r1f-independent-fourth-X-600-evidence`. **622 filer**, inklusive 600 faktiska konsekutiva **Stella 6.7.1 X11** screenshot-crops, originalskriven 6502-assembler, DASM-lista/symboler, 16KB standard-F6-ROM, `evidence_600/frames_600.csv`, `evidence_600/summary.json`, originalmaskernas kontroll, reproducerbar byggning och SHA-256.
- Downloaded ZIP checked `testzip()==None`; JSON omläst direkt ur ZIP, ingen ny genererad visuellt rekonstruerad skärm använd. 
- **Binär exakt 16 384 byte** (4×4096-byte F6 image); SHA-256 **`795dd4d0b8e6255facdb528a1fd4008b38047a5e84c4883d34e2f82f73c5bbb3`**, omverifierat från nedladdad faktiska ROM.
- Originaldata från `main/design/NPC_REFERENCE_8x9_masks.json` jämförs byte-för-byte och därefter pixel-för-pixel i *varje* bildruta.

## Verkliga bildrutor: 600/600 helt godkända

| Hård kontroll | Uppmätt |
|---|---:|
| Konsekutiva Stella frame-ID 11–610 | **600/600** |
| Exakt 262 NTSC-rasterlinjer i debugger-HUD | **600/600** |
| Alla fyra olika *originalmasker* 8×9 (stora mannen, stora kvinnan, lilla mannen, lilla kvinnan) | **600/600** |
| Gul P0-spelarkandidats 8×9-mask | **600/600** |
| Ett enda gult M0-skott på y160 ovanför NPC-bandet | **600/600** |
| Oönskade vita GUI-pixlar i NPC-bandet | **0 totalt** |
| Oönskade gula GUI-pixlar i NPC-bandet | **0 totalt** |
| Fjärde NPC på **GUI-X330** | **296 bildrutor** |
| Fjärde NPC på **GUI-X348** | **304 bildrutor** |
| Oklara/misslyckade rasterrader eller bilder | **0** |
| Byte mellan X-lägen i regelbundna 16-frame-block | **JA**, entydigt matchande fasoffset |

### Exakta figurlägen i rå Stella-GUI (2 GUI-pixlar = 1 TIA-färgklocka)

| Figur | Läge A | Läge B | Uppmätt ändring |
|---|---:|---:|---|
| **Gul P0-spelare** | X216 | X216 | 0 |
| Stor vit man P1 | X166 | X166 | 0 |
| Stor vit kvinna P1 | X280 | X280 | 0 |
| Liten vit man P1 | X406 | X406 | 0 |
| **Liten vit kvinna via andra P0/RESP0** | **X330** | **X348** | **+9 TIA-färgklockor** |
| Gult M0-testskott | X240–241 | X240–241 | 0 |

**Därför är det ett verkligt oberoende fjärde-X-delbevis**: medan P0:s första gula kopia och alla tre P1-NPC har **exakt samma position över alla 600 bilder**, byter den fjärde vita originalmasken X mellan två fysiskt skilda, intakta positioner. Inte bara registertabeller, utan faktiska Stella-pixlar.

## Hur detta fungerar, utan att öka 76-cykelbudgeten på synlig rad

- Först tidigare R1e: `NUSIZ0=$04` och en automatisk fjärrkopia med obrytbar +64 CC-relation till gul P0.
- Nu R1f: `NUSIZ0=$02` mediumkopieläge, **två** riktiga `STA RESP0` per fysisk NPC-rad.
- Gul P0:s kopia utlöses av den tidiga `STA RESP0`; efter dess fullständiga bild har TIA/6507 tid att ladda lilla kvinnans oförändrade byte i `GRP0` och `COLUP0` vitt.
- Andra `STA RESP0` utlöser fjärde vita NPC:s mediumkopia vid ett separat horisontellt tidsfönster. I den tidiga kärnan ligger `STA RESP0` **före** `STX GRP0`, i den sena **efter**. Båda instruktionerna tar 3 CPU-cykler; ändrad ordning flyttar den senare utlösningen 3 CPU-cykler = **9 TIA CC** utan att den gula P0-kopian flyttas.
- **Verkliga Stella-debuggerstopp i de föregående identiska två del-ROM-kärnorna:** `STA RESP0` gul vid scanline119 CPU-cykel **26**, `STA RESP0` vit före/efter `STX GRP0` vid cykel **45/48**, sista `STA RESP1` vid cykel **63**. Alla är PC-stopp **före** instruktionsexekvering; post-write-tid får inte förväxlas.
- För **en enda ROM som faktiskt rör den fjärde NPC:n** ligger två i förväg assemblerade dedikerade rasterloopar på samma F6-bank. `FRAMELO & $10` väljer en av de två före hela 9-radersbandet, medan renderingsloopen använder exakt samma skrivtider utan en dynamisk branch mitt i kritisk pixelklocka. Väljer var 16:e bildruta.
- `WSYNC` efter sista av 9 rader är i respektive dedikerade loop före gemensam bottom-kod; inga extra fysiska rasterrader. Real-Stella-HUD 262 i 600/600 verifierar frame-budget.
- **Ingen särskild cartridgeprocessor**, inget SCABS/F6SC/DPC/ARM, och inga källmaskändringar.

## Fortfarande verkligt blockerade krav

- **ENDAST TVÅ** möjliga belagda fjärde-NPC-X. Detta är ett oberoende steg på +9 CC, inte global fri 160-CC-X, kanter, näröverlapp eller sexfaldig individuell rörelse.
- De tre P1-figurerna är **statiska i samma 600-frame-ROM**. Den gula spelaren är också statisk. Äldre separat R1c bevisade bara ett litet tredje-P1-X-steg. Dessa delbevis får inte automatiskt kombineras till ett allmänt dynamiskt fyra-fritt-X-PASS.
- Testskottet M0 är på raden omedelbart *ovanför* de nio fullständiga NPC-raderna, inte en spelintegrerad rörlig projektil med alla R1/R2-villkor. Ingen samtidig full brun PF-vägg/högerdörr/nyckel, ingen full R1–R4, ingen PAL eller fysisk Atari-hårdvara.
- P0 spelarmask är en temporär testform, inte en designwaiver.
- **Ingen full R1 PASS, ingen separat VERIFICATION**. Allt ovan är MAIN II research med egenkontroll. `main`, draft PR #7 och äldre verification Issue #8 har inte ändrats.

## Föreslagen nästa forskningssekvens

1. Isolera och mäta fler möjliga **vitt-P0-RESP0-utlösningsfönster** samt effekter av NUSIZ nära/far, innan något påstående om fri X. Välj minst fyra distinkta positioner medan gul P0, alla tre P1 och M0 förblir oförändrade, 9×8 originalform.
2. Prova **separat fri förflyttning av de tre P1-NPC** samtidigt som P0 har två lägen och validera 76 CPU-cykler/9-raderskant. Kräv minst nära/överlappande, mitten- och kantfall.
3. Separat #07 Asymmetric Playfield (bruna väggar/högerdörr) och #25 Stack-Based TIA Register Tricks under 26-tricksregistret, men behandla deras CPU-resurskonflikt med den här tidskritiska kerneln som en oberoende blockerare.
4. Vid varje lovande kombination 600 riktiga Stella-bilder + full käll-/maskspårning; först därefter ge en uppdaterad MAIN-handoff. **Implementering** kräver separat uttryckligt scope och fristående Verification.

**Källkritik:** Andrew Towers [TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) för same-line RESP/NUSIZ-underlag; våra datum, bitfel, X, ROM-hash och phase counts härrör från ovanstående *faktiska* Actions-artefakt, inte från webbartikeln.
