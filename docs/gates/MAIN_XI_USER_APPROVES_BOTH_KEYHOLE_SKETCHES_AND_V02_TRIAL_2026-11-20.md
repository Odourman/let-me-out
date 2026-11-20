# LET ME OUT! – MAIN XI: användaren accepterar båda nyckelhålsskisserna och väljer rekommenderad testordning

Datum: 2026-11-20
Typ: Senare uttryckligt användarbeslut om visuellt godtagbara PROVKANDIDATER och fortsatt tekniskt V02-test, inte godkänd produktions-ROM eller kartcutover.

## Exakt besked

Användaren skrev efter att ha sett två illustrerade nyckelhål, först en fyrdubbelt förstorad P1-bitmap och därefter en grövre symmetrisk playfield-bitmap:

> "Båda bilderna är ok ut. Man kommer fatta vad det är. Vi fortsätter efter dina rekommendationer"

Det innebär att **båda exemplifierade nyckelhålsformerna får provas och är visuellt acceptabla som designriktning**. Utseendet behöver vara igenkännbart som nyckelhål men inte pixelidentiskt med R3. Detta är en precisering av [föregående explicita beslut om ungefärligt nyckelhål](MAIN_XI_USER_DECISION_RECOGNIZABLE_NEGATIVE_KEYHOLE_NOT_EXACT_R3_2026-11-20.md), inte retroaktiv grafik-PASS för befintliga ROM:ar.

## Ordning godkänd för teknisk prövning

A, förstahandsprov: **Orange 32px förstorad P1-sprite i exakt det 8-raders yttre dörrbandet**, med svarta hål som transparenta bitmap-nollor mot svart bakgrund/PF=0. Principskiss 8x8 före horisontell 4x-förstoring:

    ########
    ###..###
    ###..###
    ###.####
    ###.####
    ###.####
    ########
    ########

Här är # orange grafik och . genomskinligt (svart bakgrund). Syfte: 8px huvud + 4px stam. NUSIZ1-förstoring och exakt form måste kontrolleras på verklig TIA-pixelbild. Prova topp och botten separat, först TOP när det ger snabbast evidens. **P1 får inte långvarigt tas från de fem NPC**, inklusive då fiender kommer nära top/bottom-bandet. Kontrollera registerfärg/position/reset, raster och P0/shot/key.

B, godtagbar fallback: **enbart speglad PF** med grövre nyckelhålsliknande svart utskärning, t.ex. 16px huvud/8px stam med skilda PF2-bitmasker per rad. Kräver samtidigt lösning av orange färgspill till den bruna ytterväggen genom verifierad cykel-/färgtiming (forskningsalternativ C). Använd inte B:s form som tekniskt undantag från riktig TIA-rendering.

Båda är av användaren accepterade visuella RIKTNINGAR, men inga exakt slutligt fastslagna spritebyte, framtida karta-topp/botten-tilldelningar, dörr-X/bredd, permanenta kartversionshashar eller releasegrafik. En annan form än dessa skisser, eller en ful/diffus slutbild, kan behöva användargranskning.

## Oförändrade bindande spelkrav

Svart hål är **avsaknad av orange dörrgrafik mot svart bakgrund**, inte extra svart objekt. En enda orange låst dörr i övre/nedre vägg beroende på framtida karta; låst stoppar spelaren, upplåst öppning måste passeras fysiskt. Resterande vägg brun, ingen orange färgspill, ingen oavsiktlig passage, inga gula rester, extra skottpixlar eller borttagna fiender.

Exakt fem individuella fiender med fria logiska X/Y, fyra orörda TOP-DOWN 8×9-masker (i framtiden oberoende slumpade per individ), full key/player/same-Y- och shot-funktion. Aldrig sänkta fiende-/synlighets-/flimmerkrav. Fryst F6/NTSC 16 384 B, 262 scanlines, högst 76 CPU-cykler/rad och 128 RIOT-byte inklusive stack.

V02-prov är teknisk test-only enligt LM-D29/LM-D30 och den senaste frysta [två-ROM-testleveransen](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7037851276), MAIN:s [mottagning](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7037903760). Ingen automatisk produktionskartcutover, V03, G6/F12, mapper/PAL, canon-waiver, PR-merge, release eller självsignerad Verification. `G5_FORMAL_OPEN`, `INDEPENDENT_VERIFICATION=NOT_RUN`.

Tekniskt underlag: [MAIN XI:s jämförelse av fem metoder och 30 trick](../research/MAIN_XI_KEYHOLE_OPTIONS_30_TRICKS_ONLINE_2026-11-20.md).
