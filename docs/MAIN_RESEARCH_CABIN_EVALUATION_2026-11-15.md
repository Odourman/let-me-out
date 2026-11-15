# MAIN – bedömning av researchöverföring från The Cabin (2026-11-15)

**Status:** rådgivande forskning och teknisk källgranskning; INGET nytt användarbeslut, ingen design-waiver, ingen ROM-implementation, ingen oberoende VERIFICATION. Gäller enbart *Let Me Out!*.

**Inlämnad rapport:** [RESEARCH_THE_CABIN_TRANSFER_2026-11-15.md](RESEARCH_THE_CABIN_TRANSFER_2026-11-15.md), bevarad från användarens bifogade forskningsunderlag. Primärkällor i uppladdade The Cabin-arkivet har studerats som externa teknikreferenser, inte som canon för Let Me Out!.

## MAIN:s kontroll av primärkod i det bifogade arkivet

1. **Cyloid – bekräftat källmönster, inte sex-NPC-lösning.** `keithadler/cyloid/game.asm` beskriver `P0` som spelare, `P1` som tidsmultiplexade mål, `M0` som skott och `PF` som hinder. I raderna 791–819 väljs ett aktivt mål med `FlickerIdx`; tvålinjerskerneln i raderna 1679–1762 rapporterar högst 61 respektive 71 CPU-cykler på alternerande skärmrader. Det är siffror ur **Cyloids egen källkod**, INTE mätvärden för Let Me Out!. Metoden med en `P1`-android per bildruta upprepar i princip vår misslyckade teknik A och kan inte i sig kallas lösning.
2. **AStar – bekräftad rasterplan, inte humanoidrenderer.** `hippopotamus-prime/astar-free/kernel.asm` har tidsstyrda `PF1/PF2`-skrivningar med angivna cykelpunkter 19, 34, 41 och 48. Detta är användbart för asymmetrisk vägg- och högerdörrplanering, men inte ett bevis för fyra exakta 8×9-androidmasker. Arkivets AStar-kod har **GPL-3.0**-licens; ingen direkt kopiering till Let Me Out! utan separat licensbedömning.
3. **Crystal Castles – vertikal återanvändning.** Tekniken prioriteras för normala fall med separerade Y-band. **Same-Y-stress med sex fria X-positioner återstår**.
4. **The Cabin PoC och Pachinko – testmetodik, inte spelkod.** Riktade motexempel, cykeldeadlines, per-frame-loggar, synlighetsmasker och oberoende ombyggning kan överföras som kontrollmetod. De historiska resultaten ska inte räknas som Let Me Out!-PASS.

## Skillnaden mot senaste ROM DEVELOPMENT

Aktuell [draft PR #7](https://github.com/Odourman/let-me-out/pull/7), senast kontrollerad HEAD `febfda591c1a4b81682bbb33b20f02b6a99aae0c`:

- **Teknik A:** sex logiskt separata X, men endast **100/600 synliga frames per android** och upp till fem osynliga följdframes: **R1 visuellt FAIL**.
- **Teknik B:** betydligt större observerad synlighet men för grov PF-grafik, inte fyra tillförlitliga människoformer: **R1 visuellt FAIL**.
- **600/600 Stella-HUD-bildrutor med 262 scanlines per teknik** rapporteras av utvecklaren; **individuella uppmätta TIA-register-/CPU-cykelspår saknas fortfarande**. R2–R4 inte omtestade med dessa två nya kandidater. Inte oberoende verifierat.
- Researchtextens/äldre MAIN-analysens **cirka 74/76 cykler** får inte förväxlas med de senaste kandidaternas **statiska** uppskattningar A cirka 30 och B cirka 67–70 cykler inklusive WSYNC. Dessa senare tal är inte heller uppmätta registerdeadlines.

## Råd till MAIN och ROM DEVELOPMENT

**Prioritera ett enda avgränsat nytt teknikdelta inom befintlig auktorisation v0.18/R1–R4**, inte att repetera 600 frames med samma två misslyckade rendererformer:

1. Inspektera exakt `RESP1/HMOVE/GRP1/VDEL`-deadline i verklig Stella. Visa två **oberoende X-positionerade originalmasker på samma rastersnitt i samma bildruta**, med `P0` gul spelare och `M0` skott, utan NUSIZ-kopplade X. Dokumentera varför historiskt ompositioneringsprov misslyckades.
2. Om och endast om steget lyckas: pröva tre och därefter upp till sex; mät faktiskt synliga maskbitar, individuellt flimmer och 76-cykelsgräns. Undersök separat normal-Y kontra same-Y-stress.
3. Använd AStars asymmetriska PF-principer för R3/högerdörr och vägghinder, inte som godkänd ersättningsfigur för androidmaskerna.
4. Om ingen realistisk arkitektur klarar godkänt mål: lämna teknisk FAIL/BLOCKED med bevis till MAIN. **Ingen** tyst minskning av sex NPC:er, grafikmaskbyte, ny designwaiver eller ändrad spelmekanik.
5. Oavsett teknikprov: separat VERIFICATION av relevant exakt commit; tidigare [Issue #8](https://github.com/Odourman/let-me-out/issues/8) gäller fryst historisk baseline `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`.

**Spärr:** Bara den redan uttryckligen auktoriserade NTSC-diagnostiken v0.18/R1–R4 får programmeras. Ingen gameplayfas, PAL, kartcutover eller PR-merge är godkänd genom denna forskningsbedömning. *The Cabin* och *I Love a Fish* lämnas orörda.
