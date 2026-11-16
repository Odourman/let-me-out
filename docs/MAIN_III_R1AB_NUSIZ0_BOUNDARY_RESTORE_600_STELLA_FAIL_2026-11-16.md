# LET ME OUT! – R1ab: Berzerk-ONE_COPY + 76-cykelsgräns + separat första nedre D-rad

**2026-11-16, RESEARCH. Status: FAIL, 456/600 strikta Stella frames.** Delvis godkänt specifikt effektprov (återställda gula spelarpixlar och synligt gult skott), men **inte** användbar fem-NPC-kernel och inte full R1. Ingen oberoende VERIFICATION eller produktionsimplementation.

## Exakt testad kandidat

- Källgren `research/main-iii-r1ab-berzerk-nusiz-restore-boundary-20261116`.
- [**GitHub Actions #43852230740 – FAIL**](https://github.com/Odourman/let-me-out/actions/runs/43852230740), exakt testad commit `ab636f6d5d536968088d42c9366fd39c9cc0f05f`, 600 autentiska sammanhängande Stella 6.7.1-X11 PNG och fail-closed auditering.
- [**Full råevidens-artefakt #14218241250**](https://github.com/Odourman/let-me-out/actions/runs/43852230740/artifacts/14218241250), 622 ZIP-poster, 600 PNG, käll-ASM och DASM-listning/symboler, 600-raders CSV, `summary.json` och binärfil.
- Lokalt nedladdad ZIP: **SHA256 `4f3183c84cc8056dbee6c3d8712c66931a5498a05a0531dc320fc9c3cba67959`**, **ZIP CRC PASS**, 3 829 085 bytes.
- Körbar ROM: **16 384 byte standard F6/NTSC**, SHA256 **`4fab355b651599278b7d397b1a85fa3bac2cc0bc9ebaf2e2f9818fa025995350`**. Generatorn pinnar R1aa-bas `9a1a464252c3f0da3d6aecc85fc21514e1cb43c3c35f258548e4919837c84778`.

## Arkitekturhypotes, inte kopierad Berzerk-kod

R1aa hade provat `NUSIZ0=ONE_COPY` på D:s skottrad, varvid **alla 600 gula skott blev synliga**, men efterföljande P0-kopior förstördes. R1ab försökte lägga till cykelneutral återställning precis på rastergränsen:

1. På D-skottrad `STY NUSIZ0` vid c53; `STA RESP0` vid c56 (lilla kvinnans fjärde X), `STA COLUP0` vid c59 (vit P0-kopia).
2. Efter `DEY`, `STY ENAM0` vid cirka c71 stänger projektilen.
3. `LDA #$02` följt av `STA NUSIZ0` slutar vid **beräknad c76**, alltså två P0-kopior till efterföljande rad.
4. D:s **första** nedre NPC-rad har en ny specialrutin `R1abFirstLowerD`, som **utelämnar `STA WSYNC`** eftersom exekveringen ska kunna fortsätta vid horisontell ny linje utan extra blank rad. Efter första radens `DEY; JMP R1oLowerD` används ursprunglig `STA WSYNC`-styrd loop för övriga lägre rader.
5. Samtliga ursprungliga 8×9 maskbytes, alla härledda 14-raders databitar, dörr, fyra NPC-positioner och övriga tre skottrutiner A/B/C är oförändrade på källnivå.

Detta kombinerar trick **#14 Multiple Display Kernels**, **#15 NUSIZ Sprite Duplication**, **#24 Precomputed/Cycle-Exact** och Berzerks **ONE_COPY**-princip. Det finns inga kopierade instruktioner från extern Berzerk-kod.

## Verkligt utfall, med inbördes jämförelse

| Testad egenskap | R1aa, utan NUSIZ-restore | R1ab, med c76-restore |
|---|---:|---:|
| 600 konsekutiva faktiska Stella frame-ID | **600** | **600** |
| 262 NTSC-scanlines och intakta väggar/dörr | **600/600** | **600/600** |
| Korrekt ensam **GUL M0 GUI-y167** | **600/600** | **600/600** |
| Gul spelares saknade maskpixlar | **7 488 totalt** | **0 totalt** |
| A/B/C fjärde-NPC-X-lägen helt korrekta | **456/456** | **456/456** |
| D fjärde-NPC-X=x378 **hela** masken korrekt | **0/144** | **0/144** |
| Oönskade vita pixlar totalt | **2 628** | **12 420** |
| Oönskade gula pixlar | **0** | **0** |
| Verklig `CXM0P`-kontaktfärg via diagnostisk COLUBK | **Konsekvent** | **Konsekvent** |
| Strikta helhets-PASS | **456/600** | **456/600** |

**Det avgörande:** R1ab bekräftar att linjegränsåterställning kan reparera de saknade gula spelar-maskpixlarna **utan att döda själva skottet**, men ger fler oönskade vita pixelkopior och inte exakt originalmask på fjärde P0-x378. Exempel i den faktiska `CSV`-raden med första D-mode-fail (Stella frame-ID 49): fjärde-mask matchar närmast läge `post_color` med **8 felpixlar** mot 60 i R1aa, medan **82 extra vita pixlar** uppstår på denna frame. Det indikerar en förbättring av delar av D-masken men ett fortsatt felaktigt P0-kopiedekoderläge/timing; det är inte bevis för en generell fix eller ens att alla resterande D-rader har korrekt geometri. `CXM0P`-diagnostiken har skilda stabila blå (kontakt) och svarta (ingen kontakt) färger, men detta ensamt identifierar ingen logisk NPC.

**Slutsats: R1ab FAIL.** Missilfärg, `NUSIZ0`-decoder-fas, `RESP0`-reset och P0-synlighet kan inte behandlas som oberoende när registers byts mitt i samma scanline. Den exakta c76-återställningen och specialraden, i denna variant, uppfyller inte alla 14 ursprungs-maskrader.

## Nästa användbara testdesign, utan att implementera

Skriv ett **TIA-registerdeadlines-diagram** för D-regionen (skottrad + *första* nästa rad) som markerar:
- Exakta writes, PC/bank, CPU-cykler och **faktiska pixeländringar** för `NUSIZ0`, `COLUP0`, `RESP0`, `GRP0`, `ENAM0`, `RESP1`.
- Vilka P0-/M0-copy-decode-events redan har startat **före** `NUSIZ0` skrivs, och om byte av kopieläge redan har initierat en dubblett/spökbild. Mät med Stella debugger och riktig konsol innan produktionsclaim.
- Om en dedikerad D-kernel kan rita en enda gul M0 utan att P0-copy-mönstret påverkas på någon av 14 rader; om inte, studera separat M1/BL eller beräknade skottregioner. M1 och BL har sina **egna gemensamma färg- och kopieresurser** och är inte automatiskt lösningar.
- Berzerks RAM-skott, coarse/finpositionsalgoritm och per-rad-ENAM0-pointer är lovande för logisk skottmekanik **senare**, men skapar inte fler TIA-sprites.

**Avgränsning:** Fem, inte sex, NPC samtidigt; x378 är ett av endast fyra diskreta P0-X, inte sex oberoende fri-X. Full R1, logisk bullet-RAM/eldknapp/hit-ID, karta, R2–R4, PAL och independent VERIFICATION kvarstår ej godkända. `main`, ROM DEVELOPMENT draft PR #7 och VERIFICATION issue #8 är oförändrade.
