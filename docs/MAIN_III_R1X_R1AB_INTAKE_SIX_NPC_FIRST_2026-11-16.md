# Let Me Out! – MAIN III: granskning och omprioritering efter R1x–R1ab

**Datum:** 2026-11-16. **Typ:** MAIN mottagningsbeslut och teknisk forskningsplan. Inte godkänd ROM-implementation och inte oberoende VERIFICATION.

## Kontrollerade auktoriteter
- GitHub main vid granskning: f6b3fc76c59161e04e583dc8c0787332d2f261c7.
- [Aktuellt projektläge](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_PROJECT_STATE_2026-11-15.md), [uttrycklig v0.18-auktorisation](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_AUTHORIZATION_2026-11-15.md), [scope](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_SCOPE.md), [acceptans](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md) och [stoppregler](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_BLOCKERS.md).
- [MAIN:s 30-trickgranskning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_30_TRICKS_RESEARCH_REVIEW_2026-11-16.md) och [MAIN:s separata NUSIZ1-close-retrigger-studie](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md).
- [PR #7](https://github.com/Odourman/let-me-out/pull/7) DRAFT/OPEN på 82667dae033f70570dce903f8e1d4866528be02a. [VERIFICATION Issue #8](https://github.com/Odourman/let-me-out/issues/8) OPEN men gäller en annan fryst historisk commit, inte de nya research-ROM:arna.

## Status för mottagen research

| Variant | Faktiska 600 Stella-frames | MAIN-bedömning |
|---|---|---|
| [R1x](https://github.com/Odourman/let-me-out/actions/runs/43847949395) | 600 lokalt PASS | Fem oförändrade ursprungs-NPC-maskinstanser som visas i 14-radspresentation, en gul M0 x268–282, fyra diskreta fjärde-P0-X och riktig CXM0P. **Inte full R1**. |
| [R1y](https://github.com/Odourman/let-me-out/actions/runs/43848364350) | 474 PASS, 126 FAIL | Missilen försvinner i D-läget när M0 släcks för tidigt. |
| [R1z](https://github.com/Odourman/let-me-out/actions/runs/43850116022) | 456 PASS, 144 FAIL | Senare avstängning räddar M0 men tidigare COLUP0-färgskrivning gör M0 vit. |
| [R1aa](https://github.com/Odourman/let-me-out/actions/runs/43851081064) | 456 PASS, 144 FAIL | Berzerk-inspirerad ONE_COPY visar 600 gula missiler men förstör efterföljande P0/NPC-kopior. |
| [R1ab](https://github.com/Odourman/let-me-out/actions/runs/43852230740) | 456 PASS, 144 FAIL | NUSIZ0 återställd kring c76. Förlorade gula spelar-maskpixlar återställda, men D-kopior fortfarande fel och 12 420 extra vita pixlar. |

R1ab-ROM: 16 384 byte standard F6/NTSC, SHA-256 4fab355b651599278b7d397b1a85fa3bac2cc0bc9ebaf2e2f9818fa025995350. [R1ab fulla evidensartefakt #14218241250](https://github.com/Odourman/let-me-out/actions/runs/43852230740/artifacts/14218241250), 600 autentiska PNG och register-/källunderlag. Den separat nedladdade ZIP-filen har SHA-256 4f3183c84cc8056dbee6c3d8712c66931a5498a05a0531dc320fc9c3cba67959, kontrollerad CRC. **R1ab är FAIL** trots separata positiva delresultat.

R1x saknar den andra stora mannen, visar bara fyra diskreta positioner för sista P0 och demonstrerar inte sex oberoende X. Att ursprungliga 8x9 maskdata återanvänds som 14 visade rader är inte automatiskt godkännande av ny figurhöjd. Inga av dessa experiment har oberoende VERIFICATION.

## Varför Berzerk är användbart, men inte kopierbart

[Berzerk, kommenterad rekonstruerad 6502-disassembly](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm) illustrerar RAM-baserat X/Y/riktning/livstid för projektil, horisontell coarse+HMOVE-positionering och ENAM0 med radtabell. Men Berzerk utnyttjar huvudsakligen P1 mellan vertikala robotsektioner och ONE_COPY för P0 i spelbilden. Let Me Out! kräver flera olika NPC på samma rasterhöjd, där NUSIZ-kopior redan nyttjas. R1aa och R1ab är därmed negativa integrationstester, inte skäl att byta till Berzerks kernel eller ändra maskerna.

## MAIN:s prioriteringsbeslut

**Sex individuellt placerbara, läsbara androider i R1 prioriteras framför ytterligare skottutbyggnad.** Enligt gällande v0.18-scope räcker ett aktivt **diagnostiskt testsymbolskott**; full eldknapp, kulans gameplay-livstid, skada och komplett hitboxfysik är inte del av uppdraget. Låt R1x vara lagrat tekniskt delbevis, inte marknadsfört som R1-pass.

Viktigaste 30-trickskombination för nästa tekniska feasibility: **#01 sprite multiplexing + #02 mid-scanline GRP rewrite + #09 VDEL vid behov + #10 HMOVE + #15 NUSIZ close retrigger + #24 cykelprecis förberedning**. #14 särskilda regionkernlar som arkitekturstöd, #20 kollisionslatchar senare för gameplay. #27–30 kräver annan kassett, inte godkänd standard F6.

### Nästa avgränsade R1-grind – teknisk plan, INTE ny kodorder

1. **R0:** exakt mätt STA RESP1 PC/bank/scanline/cykel i Stella 6.7.1, korrekt breakpoint med run, före- och efterskrivningskontroll, exakt ROM-hash. Tidigare missade break;frame;step uppfyller inte spårkravet.
2. **R1a:** minimal diagnostisk TWO RESP1 ON SAME SCANLINE med NUSIZ1 nära-kopia. Bekräfta två skilda fysiska P1-utmatningar och faktiskt X, inte två nominella RAM-X. Detta är inte ännu tvåmasker-PASS.
3. **R1b:** två OLIKA, fullständiga original-8x9-NPC på gemensamt höjdband med oberoende X, både nära/långt avstånd, samt fullstor gul P0-spelare och aktiv M0-symbol. Pixel för pixel, 262 NTSC, exakt PC/cykel och verkligt datalager. Om någon ursprungsrad går förlorad: FAIL.
4. **R1c:** först vid R1b PASS och gällande kodmandat kontrollerat: skalning tre till sex NPC och rörelsestress i 600 verkliga frames med kvalitativ flimmerbedömning, oförändrad originalmask och R1-grindens alla krav. Detta är inte automatisk auktorisation av R2–R4 eller fullspel.

MAIN:s forskning och koordination återstartar inte ROM DEVELOPMENT automatiskt efter tidigare rapporterat STOPP. Nytt konkret implementeringsarbete går via separat användarauktorisation om tidigare mandats ram eller stoppförutsättningar kräver det. VERIFICATION måste vara organisatoriskt oberoende, pröva exakt ny ROM/commit/SHA och kan inte låna gamla Issue #8:s resultat.

**Ingen ändring i live main, PR #7, VERIFICATION #8, grafikcanon, R1–R4-scope, NTSC/F6-format eller ett senare implementeringssteg genom detta dokument.**

## Tillägg 16 november: konkret dual-mask-lucka i RESP1-close-raster

[MAIN:s nya cykel- och pixeldeadlineprotokoll](MAIN_III_R1_RESP1_RETRIGGER_DUAL_MASK_FEASIBILITY_GATE_2026-11-16.md) preciserar nästa forskningsfråga: med `NUSIZ1=$01` två `RESP1`-skrivningar kring CPU c30/c38 i samma scanline kan två close-kopior hypotetiskt börja runt TIA-X 39/63. Om andra originalbitmapraden redan finns i X kan `STX GRP1` efter andra reseten, runt CPU c41, ligga efter den första 8-pixelkopian men före den andra. **Detta är en statiskt härledd kandidat, inte en mätt Stella-ROM och inte ett bevis på två fria NPC.** 

R0 instrumentering, R1a kalibrering (identiska enkla masker) och R1b två fullständiga OLIKA 8×9-masker har separata FAIL/PASS-kriterier. R1c sex NPC får inte startas från detta delresultat utan egen auktorisationskontroll. Ingen ändring av projektcanon, `main`, PR #7 eller oberoende VERIFICATION.

## MAIN teknisk kontroll: Stella 6.7.1 och exakt tvåmaskers-timing

[**Korrigerad, direkt källkontrollerad RESP1-rapport**](MAIN_III_R1_RESP1_DUAL_MASK_STELLA_671_SOURCE_AUDIT_AND_8_CYCLE_VARIANTS_2026-11-16.md) har lästs mot `stella-emu/stella` **tagg 6.7.1**, inte senaste master. Åtta 6502-kandidater är kostnadsberäknade i [CSV](MAIN_III_R1_RESP1_DUAL_MASK_STATIC_6502_CYCLE_MATRIX_2026-11-16.csv), men **ingen ny ROM har körts**.

**Korrigering av prioritet:** c30/c38 är gränsnära och inte primär längre, eftersom andra `RESP1`-skrivningen nominellt inträffar vid första 8-pixelkopians sista pixel. **Första kalibrering c30/c40**, därefter fyra varianter **c30/c42, c32/c42, c30/c44 och c32/c44** med oberoende X-växling. Beräknade spritepar (39,75), (45,75), (39,81), (45,81) visar testbar separation, **inte** redan verkligt fri rörelse eller två kompletta masker. Modellens 53–55 cykler inkluderar spelaren och radstyrt skott, men **inte** all integrerad PF-/dörrbudget eller sex NPC. ROM-artifact- och VERIFICATION-status förblir oförändrade.
