# LET ME OUT! – MAIN VII G5P: mottagning och självständig reproduktion av RESEARCH II-leverans
**Datum:** 2026-11-17. **Status:** `G5P_ADVISORY_DELIVERY_RECEIVED_REPRODUCED_OFFLINE`. **Mottagare:** MAIN VII. **INTE:** spelcanon, G5 formellt PASS, G0/ROM/Stella, G6/F12, oberoende VERIFICATION II, PR-merge eller produktionskernel.

## 1. Auktoritet, leverans och proveniens
- [RESEARCH II:s Issue #9 och överlämningskommentar](https://github.com/Odourman/let-me-out/issues/9#issuecomment-6954821978).
- [Researchrapport på isolerad gren](https://github.com/Odourman/let-me-out/blob/research/g5p-adaptive-y-offline-20261117/docs/research/G5P_RESEARCH_II_FULL_REPORT_2026-11-17.md). Rapportslut commit `d19ae44b11082927a1c24b04e35c1508c1087526` kontrollerades direkt via GitHub.
- [Forskningsmapp med scripts och råfiler](https://github.com/Odourman/let-me-out/tree/research/g5p-adaptive-y-offline-20261117/docs/research/g5p_2026-11-17). Jämförelse mot `main`: **10 tillagda filer, totalt 14 commits före main, 0 bakom** vid mottagningen. **Ingen branch har mergats.**
- [Drive originalrapport](https://drive.google.com/file/d/1oeCZO2gfU0oqhwmhU5bhco18rc46HzeG/view) och [Drive reproduktions-ZIP](https://drive.google.com/file/d/18WGE3b31Ro7kiEuyfjW1z6J7iKOF1D7S/view), båda kontrollerat föräldraskap `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.
- **Drive ZIP**: 42 568 byte; SHA-256 `696701bc728a15871c31cdf59b0237bad2a7f7cf68796978e4fbbc6258cced14`; 10 filer, ZIP CRC PASS. **RUN_METADATA.json**: nio interna filer kontrollerade mot angivna SHA-256 och samtliga stämde. Rapportens ZIP-innehåll matchar den av användaren inkomna .md-filen byte för byte, SHA-256 `83adbfcc1d8cd913c1626d88b06ae35d6a5f5b4392b2c589c7c9b19eb25ffa31`.

## 2. Självständig, avgränsad MAIN-kontroll
Den nedladdade Drive-ZIP:ens scripts granskades för standardbiblioteksberoenden och kördes på nytt i isolerad kontrollkatalog:
```
python g5p_offline.py
python g5p_global_control.py
```
**Exakt bytejämförelse PASS** efter ny körning mot ursprungspaketets **sex** genererade CSV: `g5o_replay.csv`, `g5p_scenarios.csv`, `g5p_traces.csv`, `g5p_summary.csv`, `s05_logical_stress.csv`, `g5p_global_control.csv`. Alltså numeriskt och bytevis reproducerbart **inom den publicerade Pythonmodellen**, inte oberoende ROM-verifierat.

Kartkontroll: samtliga åtta inbyggda 40×22-hexkartor avkodades och jämfördes mot live GitHub-originalens `grid`: **8/8 exakt samma 40×22-symboler**. De fyra v0.11-kartornas kandidater: **4/4 exakta**; de fyra v0.19-förslagens kandidater: **4/4 exakta** mot fältet `reusable_old_S0_candidates_for_geometry_only`, alltså **inte** hela historiska `historic_S0_candidate_positions` (detta är en medveten nedfiltrering till geometri). Inget kartbyte, ingen skala/hitbox-acceptans.

Kontroll av råtabell: `g5p_scenarios.csv` innehåller **672** nya huvudscenarier (8 kartor × 3 spawns × 7 spelarbanor × 4 policyer); `g5p_global_control.csv` innehåller **168** tilläggsfall; `g5o_replay.csv` innehåller **12** gamla reproducerade G5O-fall.
- v0.11/84 fall per policy, `unique_threats` medel: strikt girig **2,869**, strikt adaptiv **3,155**, mjuk **4,048**, fri logisk X/Y **4,048**.
- v0.11 30-ticks stall: strikt girig **84/84**, strikt adaptiv **84/84**, mjuk och fri **67/84**.
- v0.11 konservativ mjuk-Y-kö: genomsnitt **498,6 bortprioriterade NPC×ticks av 900**, motsvarande 55,4 % av just *modellens* femfiendersvisningsplatser; **inte uppmätt flickerfrekvens, inte verkligt osynliga procent i TIA**.
- Global-BFS-känslighet: v0.11 **3,321** unika hotande; **18,8 %** move rate; **84/84** stall-fall. V0.19 kandidat **3,226**; **19,5 %**; **84/84** stall.

## 3. Vad som kan godtas och vad som INTE är visat
**Kan tas emot som pålitlig rådgivande offlineberäkning:** åtta källriktiga rutnät, deterministiska scripts, reproduktionsbara resultat, uttryckligen kollisionsbegränsade fem NPC, negativ indikation för enkla hårda Y-lanes och stor renderingsbörda vid mjuk Y. Den verkliga 8×9-mask-/TIA-rastermodellen är INTE kodexekverad eller bekräftad.

**Tre tolkningsgränser:**
1. `soft` och `free` delar **samma logiska jakt och samma NPC/NPC-kollision**; skillnaden är en **syntetisk** enfärgs/ensprite-synlighetskö som endast appliceras i `soft`. Identiskt jaktresultat är således metodmässigt väntat, inte två oberoende AI-framgångar.
2. 30-ticks-stall inträffar även vid **67/84** mjuka/fria fall, så stall-flaggan ensam visar inte en universell brist i en viss policy. Fiendehot över tid, verklig player-controller, taktiska exploits och balanserad spelbarhet behöver framtida prov. G5O:s `near≤1` var dessutom geometriskt begränsat; dess historiska raw-data ska bevaras.
3. De två S05-exemplen (13 vs 0 pixlars NPC/key-bitöverlapp) är *mask- och resurshypoteser*, ingen cycle-säker 76-cykel-kernel. O1 täcker bara **faktiska pixelöverlapp**, aldrig same-Y utan överlapp. En aktuell komplett standard-F6/NTSC G0/ROM/Stella-lösning för player+white+goldkey+orange P1-door+M0+PF saknas.

## 4. MAIN VII:s slutsats och fortfarande nödvändiga beslut
**Researchuppdraget G5P mottaget som levererat inom rådgivande scope.** **Ingen av G5-S0/S1a/S1b/S2 får status godkänd produktarkitektur.** G5P är ett NO-GO mot att *nu* välja en säker produktionskernel, **inte** NO-GO för spelet.

**MAIN-rekommendation:** behåll **fri logisk X/Y som önskad spelvision** och undersök situationsberoende renderingsplanering/hybrid endast som **framtida teknisk kandidat**. Förkasta inte allt arbete med lanes; använd strikta lanes som tydligt begränsat jämförelsespår, inte tyst AI-ändring. Acceptera inte nya generella osynlighets-/flickerregler från rådgivande modell.

**Formella användarägda G5-punkter, fortsatt obeslutade:** (A) fri Y kontra uttrycklig Y-/visningskompromiss och mätbar kvalitet; (B) framtida versionerad fem-NPC R1/R2-rebaseline; (C) eventuell scorebalans -25/kill kontra föreslaget -30/kill; (D) fem förhandsvaliderade spawns och ny 1/5 key-bärare; (E) exakt v0.11 vs v0.19-kartval. Allt separerat från redan godkända O1/LM-D06, K1/E1 och originalbeslut.

**Nästa säkra MAIN-åtgärd:** lägg fram ett konkret *användarbeslutspaket* om spelrörelse, framtida renderingskvalitet och femfienderspoäng utan att välja ny generell ROM-kernel i förväg. Hårdvarans minsta falsifierbara mikroprobe/G0 kan bara ske inom en senare **separat uttryckligen godkänd teknisk arbetsorder**, inte automatiskt ur G5P eller stängning av researchärendet. **G5 FORMAL fortsätter OPEN; G6/F12/G7–G10 och ROM/VERIFICATION/PR-merge inte auktoriserade.**

## 5. Avgränsning för specialistroller
RESEARCH II har levererat rådgivande forskning, ingen "independent VERIFICATION" eller ROM-generation. MAIN:s reproduktion av research-CSV är egen mottagningskontroll, inte VERIFICATION II:s oberoende kontroll av DASM/Stella/ROM. Alla tidigare misslyckanden inklusive F11 G0 FAIL och G5O negativa råfall kvarstår. Ingen design- eller spelcanondetalj får tyst härledas från denna researchleverans.
