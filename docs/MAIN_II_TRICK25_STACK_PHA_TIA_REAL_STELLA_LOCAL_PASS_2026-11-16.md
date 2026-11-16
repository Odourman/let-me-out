# MAIN II – trick #25 stackbaserade TIA-registerskrivningar: PHA till speglad COLUPF i verklig Stella

**2026-11-16.** **`LOCAL_PASS_PHA_WRITES_MIRRORED_TIA_COLUPF`** i isolerat standard NTSC/F6-test. **Tekniken fungerar som TIA-skrivmekanism, men ingen CPU-cykelbesparing i R1f har visats.** Inte oberoende Verification.

## Reproduktion

- [GitHub Actions **43816526765 – SUCCESS**](https://github.com/Odourman/let-me-out/actions/runs/43816526765); testad commit `194a4b3559c0a4717f1827b2ffb6780f268028f2`, researchbranch `research/main-ii-trick25-stack-tia-20261116`.
- Evidens-artefakt **`14202324136`**, `main-ii-trick25-stack-pha-TIA-mirror-evidence`, 45 filer, full reproducerbar 6502-källa, DASM-list/symbol, två 16KB-F6 ROM:er, fyra verkliga Stella 6.7.1 debuggerbilder (locked/open för vardera ROM) och komplett `audit.json`. Nedladdad ZIP `testzip()==None`.
- Kontroll-ROM 16 384 byte SHA256 `39ce0027c28baf6c74c7c0c2aaabee7dd2c045399f93dd19e1277d9ebc71ef5b`; `STA COLUPF` med brun färg `$36`.
- Stack-ROM 16 384 byte SHA256 `9a0125fa0a95bc9c793be210f214e55f8a053763a33bc15980d583851d317b1e`; i Reset `LDA #$36; LDX #$08; TXS; PHA; LDX #$FF; TXS`. `PHA` skriver på stackadress **`$0108`**, speglad till TIA **`COLUPF=$08`**. Stackpekaren återställs till `$FF` **före** några subrutiner/returer. Inga `BRK`-trick.
- Båda använder exakt samma isolerade dörrbas från trick #07, med vänster stängd och möjlig högeröppning. Det enda funktionella avsedda testdeltat är *hur* `COLUPF` får färg.

## Verkligt Stella-utfall

| Läge | Skillnad i aktiva TIA-synlighetsrutan mellan `STA` och `PHA` | Vänster vägg | Höger vägg | NTSC |
|---|---:|---|---|---|
| Låst | **0 RGB-pixlar** | 48/48 | 48/48 | 262 linjer |
| Öppet | **0 RGB-pixlar** | 48/48 | 16/48 | 262 linjer |

**Slutsats:** stackad `PHA` kan verkligen leverera samma TIA-registereffekt som `STA` i denna speglingsadress. Den precisa RGB-pixelidentiteten i båda separata ROM-körningarna är ett lokalt, praktiskt bevis för att speglingen fungerar i Stella 6.7.1.

**Viktig cykelbudget:** en enkel `PHA` tar **3 CPU-cykler**, liksom vanlig `STA COLUPF` på 0page **3 CPU-cykler**. För att flytta stackpekaren till rätt adress och återställa den krävs extra instruktioner; detta exempel är **långsammare** än en direkt färgskrivning. Möjlig framtida vinst i specialfall kan vara ROM-byte, att skriva flera TIA-register i fallande stackordning eller mycket specifik registerplan. **Ingen faktisk raster-/CPU-förbättring i sex-NPC-R1 har demonstrerats.**

**Gränser:** endast färgregister i Reset, inte skrivning på cykelkritisk NPC-rad, inte Combat/BRK-variant, ingen hårdvarukonsol, inga sex NPC, inget fullspel. `main`, draft PR #7 och Verification Issue #8 oförändrade.
