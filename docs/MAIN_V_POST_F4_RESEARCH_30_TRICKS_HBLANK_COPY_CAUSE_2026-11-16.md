# LET ME OUT! – MAIN V: 30 Atari-trick omprövade EFTER R1-F4
## Ny HBLANK-förklaring för index0, 6B / NUSIZ1=$01

**Datum:** 2026-11-16. **Status:** **KÄLLRESEARCH / MAIN-INFERENS, EJ NY ROM, EJ VERIFICATION, EJ NY F5-KODORDER**. Detta tillägg ska läsas före den redan avgränsade [R1-F5 P1 copy provenance SOURCE ONLY](MAIN_V_TO_ROM_DEV_II_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_2026-11-16.md). Alla originalmasker, frysta ROM-grenar och MAIN-canon oförändrade.

## 1. Faktiska källor och vad de säger

- Ursprungets **exakt 30** [Atari-trick](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), inte 52 ytterligare T-trick, har jämförts med [tidigare MAIN-30-granskning](MAIN_30_TRICKS_RESEARCH_REVIEW_2026-11-16.md), [R1-tillämpningsgranskning](MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md), [TIA close-retriggering forskning](MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md) och [Cabin-transfer](RESEARCH_THE_CABIN_TRANSFER_2026-11-15.md). Dessa äldre rådgivande dokument föregår F2–F4 och kan inte väga över frysta faktiskt mätta positiva/negativa ROM-resultat.
- [Andrew Towers, TIA Hardware Notes, §§ Horizontal Sync Counter / Player Horizontal Position Counters / Re-trigger](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), skriven 2003 utifrån gate-level: **HBLANK upphör efter 68 TIA color clocks** på normalt synligt bildband; P0/P1:s horisontella positionsräknare **räknar enbart under synlig rastertid**, och står stilla under de 68 HBLANK-klockorna. Med `NUSIZ1=$01` kan en s.k. `close` start utlösas cirka **17 färgklockor efter en effektiv P1-positionsreset**, med möjlig fas-/latchpåverkan vid täta om-resetter. En `main`-kopia kräver 160 aktiva klockor för omslag och kan inte starta i ett rasterband med upprepade täta RESP1-strober.
- Fryst [6B/F2/F3/F4 faktisk kod](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/r1_f4_build.py), F4 [utvecklarrapport](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F4.md) och [MAIN:s oberoende 32/32 PNG-omräkning](MAIN_V_R1_F4_RECEIPT_AND_NEXT_DIAGNOSTIC_DECISION_2026-11-16.md): sex originalmasker vid samma rasterhöjd med `NUSIZ1=$01`, sex `RESP1` per källrad. F4 första kopia efter `RESP1` på CPU-c18 eller c21 står x43 i 16/16+16/16, F3 c20 står x43, tidigare 6B c19 står x43; index1 c28→x75, index2 c37→x129 och F2 c38→x135, index3 c46→x183, index4 c56→x243, index5 c66→x303. Riktiga F4 TIA-traps c18, c21, c28, c37 och GRP1 bevarade. `c` är CPU-cykel i den relevanta rasterraden, X är **900×300 Stella crop-pixlar**, inte TIA-färgklockor.

## 2. Nyckelinsikt: tidig RESP1 skrivs före HBLANK:s slut

Med vanlig 3 TIA-färgklockor per 6507-cykel och HBLANK slut vid färgklocka ~68:

| Första RESP1 | Skrivning i färgklockor `3c` | Under HBLANK? | Faktiskt index0-X | Källa |
|---|---:|---|---:|---|
| c18 | 54 | **Ja** | **43** | F4 |
| c19 | 57 | **Ja** | **43** | 6B/F1 |
| c20 | 60 | **Ja** | **43** | F3 |
| c21 | 63 | **Ja** | **43** | F4 |

**HBLANK-insikten:** Att skriva `RESP1` vid c18, 19, 20 eller 21 behöver inte ge några olika interna aktiva räknartillstånd när den synliga delen börjar. Hårdvarudokumentationen säger uttryckligen att spelarräknaren är klockad **enbart under synlig del**. Att upprepa `+/-1 CPU cycle` *inom* HBLANK kan därför aldrig ensam bevisa oberoende X för den första synliga close-kopian.

### En enkel kalibrerad pixelmodell för dessa frysta rasterbilder

Vi använder en empiriskt kalibrerad Stella-crop-origin **+9 skärmpixlar** och två debuggercrop-pixlar per TIA color-clock. En `NUSIZ1=$01 close`-start antas ske ~17 synliga TIA-klockor efter att P1 positionsräknaren börjar efter reset:

```text
TIA_colorclock_at_RESP = 3*c
visible_begin = 68
P1_close_start_visible_X_ideal = 17 + max(0, 3*c - 68)
Stella_crop_X_prediction = 9 + 2 * P1_close_start_visible_X_ideal
```

| P1-kopia | CPU-cykel | Idealt kalibrerat crop-X | Observerat crop-X | Diff |
|---|---:|---:|---:|---:|
| index0, F4 tidig | 18 | 43 | 43 | 0 |
| index0, 6B | 19 | 43 | 43 | 0 |
| index0, F3 | 20 | 43 | 43 | 0 |
| index0, F4 sen | 21 | 43 | 43 | 0 |
| index1 | 28 | 75 | 75 | 0 |
| index2, F2 mode0 | 37 | 129 | 129 | 0 |
| index2, F2 mode4 | 38 | 135 | 135 | 0 |
| index3 | 46 | 183 | 183 | 0 |
| index4 | 56 | 243 | 243 | 0 |
| index5 | 66 | 303 | 303 | 0 |

Modellen passar **alla dessa faktiskt rapporterade/MAIN-omräknade positioner exakt**. `+9` är en KALIBRERAD SCREENSHOT-förskjutning, **inte** något Atari-hårdvaruregister. Därför bevisar den här perfekta matchningen **starkt stöd för HBLANK + close-delay** men **inte** i sig vilken faktisk START-latch, vilket internt tvåfassteg eller vilken individualiserad kopieidentitet som orsakade varje vitt pixelstartläge.

**Viktig närhetsgräns:** c28 är färgklocka `84`, bara **16 aktiva TIA-klockor** efter synlig start `68`. En ren close-START från den tidigt HBLANK-nollställda räknaren skulle idealiskt inträffa efter ca **17** aktiva klockor (kring klocka 85), dvs på gränsen **omedelbart EFTER nästa `RESP1 c28`**. Towers beskriver uttryckligen att en nollställning under start-dekoder/latchöverföring kan försena eller förlora START upp till 3 klockor. Då faktiskt X=43 visas, måste F5 hålla isär den idealiserade positionsformeln och den verkliga interna aktiveringsordningen. Det duger inte att förenklat påstå "varje första close-kopia startar fritt från c18" eller "c28 hade ingen effekt". En ROOT-CAUSE-trace på signalnivå är ännu **inte** genomförd.

### Falsifierbar gräns för nytt schema – INTE en testorder

För att flytta första close-kopian från HBLANK-låsta `X=43` måste dess **effektiva** första positionsreset hamna **efter** visible-begin (runt `c23` eller senare). Men om nästa `RESP1` lämnas fixerad på **c28**:
- `c23 ` motsvarar cc69; dess teoretiska close-start tid `69+17=86`;
- index1:s fasta `c28` nollställer räknaren redan cc84, **före** denna potentiella close-START;
- Towers dokumenterar att åter-reset *före* en kopias Start vanligtvis innebär att den inte ritas, med särskilda fas-/latchundantag.

**Konsekvens:** Våra tidigare F4-variantprober (bara c18/c21 och fixerat c28) kunde inte pröva en fullt normal *efter-HBLANK* egen X-geometri. För att seriöst testa egen första-X måste man sannolikt också ändra det andra `RESP1`-fönstret eller kopierutinen för den andra NPC:n, med förstastartens och andra originalmaskens pixeldeadlines samplanerade. En enkel `c23` med c28 fast har för liten ideal startmarginal (15 färgklockor). Att skjuta c28 till c29 ger 18 färgklockor men flyttar då **även index1** enligt den uppmätta kopiemodellen och är inte fri individuell X. Det är **arkitektur-/kopieplanering**, inte en godkänd plus-en-cykel-lösning.

**Ingen full R1-lösning härmed påvisad**; bara en mycket skarpare orsaksmodell som matematiskt förklarar varför de fyra tidigare första-fasproven var blinda inom HBLANK och vilken *kombinerad* kopieplanfråga en framtida arkitektur måste lösa.

## 3. Samtliga 30 trick har klassats mot F4 med tydlig förklaring

**A. Direkt relevanta för teknisk lösningsfamilj:**
- **#02 Mid-scanline GRP1 rewriting:** krävs för de fyra exakt olika NPC-silhuetterna när en P1 används flera gånger i samma rad. Synlig maskbyte måste inträffa före varje pixelstart.
- **#15 NUSIZ close-copy/retriggering** tillsammans med **#01 multiplex:** dagens sex-synliga-6B och F2 positiva kopie-exempel använder redan detta. Men HBLANK-c18..21 visar **inte** fri index0-X.
- **#24 förberäknade/cykelexakta kernels:** starkast om full kopie-/GRP-plan måste ändras; flytta CPU-logik före aktiva rader, men inga gratis TIA-cykler. En ny arkitektur är inte F5-scope.
- **#09 VDEL:** möjligt för att förbereda/synka GRP-data, men gammal Venetian/VDEL-Fail skapar ingen tredje P1.
- **#10 HMOVE fine positioning:** kan placera P1-gruppen, men verkar på själva P1 och därmed risk för samrörelse och även P0/M0. Ingen förklaring för individuell index0-X utan efterföljande bevis.
- **#08 two-line:** kan spara relativa beräkningsfönster men måste behålla **alla** nio bitmaprader och same-Y-stress.

**B. Bra för annat än den nuvarande första P1-X-blockeraren:**
- **#07 Asymmetric PF** = redan isolerad R3-högerport; PF/P1/P0/M0-integration fortfarande separat problem.
- **#14 Multiple display kernels/F6** = HUD, separata R2/R3-zoner/ROM-data, men **inga** extra P1-kanaler eller 76-cykelsmarginal.
- **#05 Dynamic PF** = för grova humanoider med 4CC/pixel, PF är samtidigt brun vägg.
- **#12 Rasterfärg, #13 48px font, #16 REFP, #17 M0/M1/BL, #18 PF SCORE, #19 PF PRIORITY, #20 hardware collisions, #21 RIOT timer, #22 stack/RAM mirroring, #26 horiz scrolling** = värdefulla vid andra steg, men **inte** en direkt fri-original-NPC-X-lösning.
- **#06 Mid-frame resize, #11 late HMOVE, #23 undocumented opcodes, #25 stackbaserad TIA-skrivning** = ingen bevisad spritekanal, hårdvara-/kompatibilitets- eller skalerisk.
- **#03 Venetian** 9/18/VDEL och **#04 sextur-flimmer** = lokalt negativa i våra konkreta tester och kräver ny tydlig orsak för att återupptas.
- **#27–30 SCABS, Superchip/Supercharger, DPC, DPC+/CDF/ARM** = andra kassettformat än standard F6 och inga fler inbyggda TIA-sprites. Inte tillåtna av nuvarande användarauktorisation.

## 4. MAIN:s forskningbeslut och hur F5 borde användas

Detta är **inte** en automatisk ny F5-kommitt, ny ROM, egen Stella-körning, ny full-R1-arkitektur eller designwaiver. Ingen av 30 tekniker ger en självklar friktionsfri sex-fri-X/Y-lösning under oförändrad F6/NTSC och same-Y.

**Konkreta prioritering inom REDAN AUKTORISERAD SOURCE-ONLY R1-F5:**
1. Validera eller falsifiera **HBLANK/close-copy-positional clamping** med den frysta 6B/F2/F3/F4-koden, TIA source/schematics och de originala trapsen. Notera att c28=84 inträffar 16 färgklockor efter HBLANK och nära close-start cc85; undersök om start-latch/äldre puls faktiskt används. Dokumentera exakt antal CPU/TIA-cykler och vilka GRP-maskrader som redan finns.
2. Jämför F2:s verkliga index2 `c37↔c38`, där båda strober ligger under aktiv video och nästa `RESP c46` har en betydligt större färgklockmarginal.
3. Utred **på papper, utan ny ROM** om någon rejält källgrundad och falsifierbar **start-efter-HBLANK och nästa-kopiekompensation** kan ge index0 eget X och samtidigt hålla index1 på sin X, utan att ta 5 extra cykler när sista `GRP1/WSYNC` redan slutar statiskt c69/c72. Om nej: `F5_CAUSE_EXPLAINED_BUT_TWO_INDEPENDENT_X_NOT_FEASIBLE_WITH_THIS_ROW_SCHEDULE` eller `F5_CAUSE_NOT_ISOLATED`, och MAIN måste ta separat R1-arkitekturbeslut. Ingen annan teknikfamilj öppnas automatiskt.
4. Enda nästa framtida DASM/Stella-experiment, **endast om MAIN separat beställer efter F5**, bör vara en minimal kontrollerad *kopia-/HBLANK-grind* med förutbestämda X-prediktioner, inte ett nytt blint `RESP1 +1`-svep. En sådan geometri kan fortfarande vara blockerad av c28 och av index1:s maskdeadline.

**Slut:** R1 `BLOCKED/NOT ACCEPTED`. Vi har en **starkt dataöverensstämmande och hårdvarustödd orsakshypotes** till det gamla index0-Fail; vi har **inte** en färdig modell för sex fria NPC-positioner eller en bevisat fungerande ombyggnad. F5 förblir read-only inom redan utfärdad scope och GRAPHICS/VERIFICATION ligger kvar i tidigare roller.
