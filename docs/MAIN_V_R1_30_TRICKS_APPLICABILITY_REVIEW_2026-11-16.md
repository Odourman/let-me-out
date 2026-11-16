# LET ME OUT! – MAIN V: kritisk tillämpningsgranskning av 30 Atari-trick på aktivt R1

**Datum:** 2026-11-16. **Typ:** rådgivande MAIN-research efter mottagen isolerad R3/C02-utvecklarleverans. **Inte** en ny kodauktorisation, R1-PASS, forskningsbranch, ändring av R1-arbetsorder eller oberoende VERIFICATION. Aktivt utvecklingsscope förblir [MAIN V R1-arbetsorder](MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md) inom användarens Issue #6-auktorisation.

## Källor och historisk skillnad

- Original 30: [RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md). Tidigare [MAIN:s 30-tricksbedömning](MAIN_30_TRICKS_RESEARCH_REVIEW_2026-11-16.md); 52 T-teknikmönster överlappar de 30, alltså inte 82 oberoende lösningar.
- [Särskild close-retriggering-research](MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md) och [RESP1-rotorsaksanalys](MAIN_RESP1_ROOT_CAUSE_ANALYSIS_2026-11-15.md).
- [Andrew Towers, TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php): close-copy kan starta ~17 TIA-color-clocks efter RESP-reset i rätt NUSIZ-läge, med fas-/närhetsberoende. Samma-linje flera RESP-triggers är en separat mekanism från tidigare misslyckad en-RESP-per-linje Venetian.
- [Space Invaders faktisk spriteprincipsammanställning](https://retrocomputing.stackexchange.com/questions/7502/how-does-space-invaders-on-the-atari-2600-display-all-the-aliens): två spelarsprites P0/P1, vardera tre NUSIZ-kopior med fast arrangemang, GRP registerskrivningar mellan kopior; **vår P0 är upptagen av gul spelare** och sex fria X är därför ett helt annat problem. Ingen evidens för att Space Invaders använde godtyckliga RESP-strober för sina sex fiender.
- [Stella Debugger manual](https://stella-emu.github.io/docs/debugger.html): `break`/Run och `trapWrite`, bank, `_scan`, `_sCycles`; trap stannar EFTER skrivande CPU-instruktion.
- Fryst R3-lokal PASS: `000b6f2a579e4aa96995229b2174884fb7c565e2`, bruna PF-väggar och orange port/transparent svart nyckelhålsutskärning från P1; 7 verkliga rastertraps i en definierad linje; statisk maxbudget 74/76. Isolerad teknik, **ingen** R1+R3 same-frame-pass.

## Objektivt problem att lösa

Aktiv R1 kräver sex källkorrekta 8×9-originalmasker, fyra visuellt identifierbara silhuettkategorier, sex **individuellt X/Y-positionerbara** androider på samma/överlappande rasterband, gul P0-spelare, M0-skott och bruna PF-väggkanter. Endast en P1-kvalitetskanal återstår typiskt för fulla NPC-masker. Sex identiska kopior, fasta avstånd, tidsmultiplex med 1/6 bildsynlighet, grova PF-gubbar, halverade 9-raders masker eller tre sammanlänkade X/Y-profiler uppfyller **inte** acceptanskravet.

## Passar nu, men bara som mätbara hypoteser

| Ursprungligt trick | MAIN-bedömning 2026-11-16 | Vad måste visas |
|---|---|---|
| **02 – mid-scanline GRP rewriting** | Högsta relevans, **ej bevisad för fria X** | Två olika fulla originalmasker i samma 9-raders höjd med P1, P0+M0, skilda fritt valda X och korrekt byte per rasterrad |
| **15 – NUSIZ copies + same-scanline close RESP retriggering (trick 01/02/10/15)** | Bästa nya tekniska hypotesen, **ej tidigare positivt Stella-provad i Let Me Out!** | Först två close-kopior med korrekta verkliga X, sedan två olika maskmönster, sedan flera oberoende X-par och skillnader i position över frames |
| **10 – HMOVE fine positioning** | Nödvändig kalibreringshjälp, **ger inga sprites** | Begärt X mot faktiskt uppmätt X, först/andra copy och påverkan på P0/M0 |
| **24 – precomputed tables + cycle-exact kernel** | Starkaste arkitekturstöd om kopior alls fungerar | Register-/pixeldeadlinebudget per rad, data staged i VBLANK, 128B RAM och page-crossing inklusive GRP, RESP, PF, P0, M0 |
| **09 – VDEL** | Villkorat timingstöd, äldre VDEL-version **FAIL** | Bevisa exakt latchbyte och bevarad nio-raders originalform; ingen tredje sprite |
| **01 – vertical sprite multiplex** | Hög relevans vid separata Y, **inte lösning för same-Y utan extra mekanism** | Samma-Y-stress kvar som hård grind |
| **08 – two-line kernel** | Reserv efter framgång i primitiv timing, risk för fel vertical pixel/höjd | Maskexakthet i nio rader och stabil scanlineprofil |

## Nyttiga men INTE högprioriterade i nuvarande R1

- **07 asymmetrisk PF:** redan demonstrerat lokalt för isolerad R3; gör inte ännu ett R3-projekt. Dess 6 registerskrivningar plus P1 och statiska 74/76 cykler är senare **integrationskonflikt**, inte en ny R1-lösning.
- **14 flera kernels / vanlig F6 bankväxling:** arkitektur och extra ROM-tabeller efter R1:s grundläggande rasterbevis, **inga nya playerkanaler/cykler/RAM**. Fyra identiska 4KB-bankkopior i senaste R3-provet ger ingen faktisk kodspecialisering.
- **05 dynamiska PF-sprites:** äldre PF-humanoider otillräckliga som originalmasker; PF lämpar sig för väggar och enkla data.
- **17 M0/M1/ball; 19 PF priority:** resurs-/skymningsexperiment för senare R2 eller integrationsarbete, inte extra 8-bitars humanoider. M0 är redan det aktiva skottet.
- **12 rasterfärg; 13 48px; 21 RIOT timer:** visuellt/timing/arkitektoniskt stöd men fixar inte 6 fria X.
- **03 Venetian och 04 sexfasmultiplexflimmer:** redan konkret negativt provade i våra former. Repetera inte oförändrade experiment: 9-raders interleave visar bara 5/4 originalrader; SEX_X_FREE A 100/600 per NPC.
- **06, 11, 16, 18, 20, 22, 23, 25, 26:** lågt värde för **det nuvarande** tvåmaskers same-Y-problemet; riskerar tid, förvrängning, färgkonflikter, stackfel eller kompatibilitet utan att lösa objektkanalen.
- **27–30 SCABS/Superchip/Supercharger/DPC/DPC+/CDF/ARM:** kräver annan cartridgearkitektur, **inte standard F6 och inte auktoriserat**. Inte heller sådana lösningar skapar TIA-pixelskrivtid/sprites.

## Rekommenderat minsta testpaket INOM REDAN AKTIVT R1

**G0 – verifiera mätningen, inte gissa registertiming.** På fryst miniprob: kontrollera PC/bank/scanline/cycle VID verklig `STA RESP1`, `STA GRP1`, `STA NUSIZ1`, `STA HMOVE` med Stella 6.7.1; undvik det tidigare felaktiga `break; frame; step`-mönstret. `trapWrite` är ett efterinstruktionsstopp. Visa raw screenshot/trace och beräkna pixeldeadlines.

**G1 – kan same-scanline close-retrigger alls ge två P1-kopior?** Isolerad ROM med P0 gul + M0 aktivt och enkel P1-probmönster, NUSIZ1 close, **två RESP1-strober i en och samma scanline**. Registrera båda verkliga bild-X och varje faktisk write/cycle samt edge cases. Även om tekniken fungerar: inte full NPC-mask-PASS.

**G2 – kan kopiorna ha TVÅ OLIKA fulla godkända 8×9-masker?** På samma nio scanlines: GRP1-byte till skilda källkorrekta man/kvinna-masker mellan rätt pixeldeadlines, originalpixelmatch för båda och spelare/skott kontinuerligt synliga. Prova två olika ordningar och minst tre separationsfall (nära, medel, långt). Om bara en mask överlever eller masklinjer faller bort: FAIL för grinden.

**G3 – är X verkligen fria, inte bara NUSIZ-låsta?** Håll maskerna oförändrade, håll den ena begärda X konstant medan den andra ändras; upprepa omvänt. Testa minst fyra individuellt valda X-par över flera frames, inklusive svåra nära/överlappande eller kantfall. Logga begärd X och faktiskt renderad X för *vardera* masken; markera fasta relativa avstånd, minimum spacing, horisontella deadlines, tappade/överlappande masker. Om bara fasta grupper går att visa: PARTIAL/FAIL för godtycklig X, inte fri-X PASS.

**G4 – endast efter G2+G3 verkligt positivt:** skala i samma R1-arbetsorder till 3→6, individuella X/Y, same-Y och delvis överlappande Y, PF-väggar, gul P0, M0. Mät per-NPC mask/synlighet, 600 sammanhängande frames och TIA-write timing som krävs. Stanna om hårda gränser kräver färre NPC, förvrängda originalmasker, otillåten cartridgehårdvara eller oacceptabel blinkning.

Detta är **rådgivande ordning till ROM DEVELOPMENT** att väga mot existerande MAIN-order, inte order att köra ytterligare testfamiljer utanför det enda aktiva R1-scope. Om G2/G3 misslyckas och inga rimliga tekniska alternativ återstår: lämna FAIL/BLOCKED med avgränsade två tekniska eller designrelaterade alternativ till MAIN. Ingen tyst waiver. Separat VERIFICATION förblir STANDBY till en verkligt stor fryst batch.

## MAIN:s skarpa slutsats

**Ja, 02/10/15/24 (med VDEL som eventuellt stöd) bör undersökas NU inom R1, och inte som 30 parallella experiment.** Särskilt *close-retriggering* är faktiskt en ny testbar TIA-mekanism jämfört med våra misslyckade Venetian-försök. **Nej, inget av tricksen har ännu bevisat eller garanterar sex fria originalmasker på samma höjd med P0/M0 och PF.** Upplös först den binära tvåmaskers- och fri-X-frågan; skala inte något som redan saknar realistisk grafik-/cykelbudget.

Inga nya användarbeslut, ändringar i R1-kod, PR-merge eller oberoende VERIFICATION genomförs genom detta dokument.
