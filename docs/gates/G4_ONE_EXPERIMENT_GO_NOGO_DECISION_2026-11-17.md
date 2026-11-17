# LET ME OUT! – MAIN VI G4 – BESLUT: EN fysisk primitiv, villkorad GO / uttrycklig NO-GO
**Datum:** 2026-11-17. **Mandat:** användarens "Ok, följ dina rekommendationer" efter fullständig G3; tolkas som **G4 SOURCE ONLY**, inte kod- eller genomförandemandat för G5–G6.

## 1. Exakt G4-bedömning
**Huvudstatus:** `G4_CONDITIONAL_GO_FOR_ONE_SEPARATELY_AUTHORIZED_MICROPROBE_WITH_MANDATORY_G0`.

Det finns **en konkret, forskningsförankrad och falsifierbar fysisk hypotes** som förtjänar **ETT** noggrant förberett framtida ROM-mikroprov: **mixed P0/P1** med P0 gul spelare + vit ORIGINAL-M som byter horisontell X-ordning, två rättvända vita P1-original (F och SM), **en aktiv ensam M0 på SAMMA nio rasterrader (icke överlappande med vit-P0 i positiv testscen)** och två verkliga bruna PF-väggkanter. Alla positioner skall komma ur separata **numeriska RAM-X-byte** och en realtidsordnings-/timingmekanism; de får INTE vara R1g:s `FRAMELO & $30` fyra förkompilerade kernlar.

**GO här betyder ett BEGRÄNSAT forskningsbeslut:** *Om användaren senare auktoriserar exakt ETT nytt G6-mikroprov, gör först source-only G0 med full instruktion-/fysikpreflight; kompilera och kör bara om G0 visar en plausibel 76-cykels-, P0/P1/M0/PF-, START/GRP- och NUSIZ0-lösning.* Det är **INTE** ett påstående att källförhandsbeviset redan är färdigt, och **inte** GO för sex fria X/Y. Om G0 inte hittar ett sammanhängande kandidatförlopp blir beslutet `G0_FAIL / NO_ROM` utan flera nya variant-ROMs.

**Separat, faktiskt NO-GO inom en konkret allokering:** Om ett **gult** M0-testsymbolskott och den **vita** P0-androidens 1-bit-vita mask är aktiva på **samma färgklocka och exakt samma slutpixel**, kan `COLUP0` inte visa båda som två distinkta färger. Detta är hårdvaruregisterkoppling och en generell slutpixelbegränsning; det är **inte** bevis för universell R1-omöjlighet. Den frågan om skottträff/occlusion och läsbarhet får inte lösas med en **tyst** spelwaiver. Positiva G6-scenfall måste först välja skottets X **utanför** P0:s motsatt färgade pixelintervall men på SAMMA scanline; X1-negativkontrollen skall mätas/klassas separat om den körs.

## 2. Varför det blev villkorad GO (och inte starkare)
### Verkliga positiva fundament
- [R1f källa](https://github.com/Odourman/let-me-out/blob/552a085d0c1ce0ec47d4f3342173658a25fd0e87/rom/v018/experiments/main_ii_r1f_resp0/build.py) gör två medium-`NUSIZ0=$02` `RESP0` under samma rad, bevisad **spelare vänster, vit originalandroid höger**; [R1g source](https://github.com/Odourman/let-me-out/blob/d1d16758c549ecd657aba3b0aa4d6d7559e19264/rom/v018/experiments/main_ii_r1g_dynamic/build_dynamic.py) visar dess fyra föregivna, i själva verket **förkompilerade** speciallägen.
- [F9 source](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md) ger två eller tre riktiga P1 originalmasker på samma band, men binära X-val i en ANNAN kernel.
- Isolerad [R3/C02](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md) visar **bruna väggar** och källspårbar PF. Om PF bitmönstret verkligen är oförändrat över det valda nio-radersbandet *kan* PF hålla sin data och inte kräva sex nya `STA PF` på varje rad, utan att väggen är borta. Det behöver dock källkontrolleras för varje vald mapp/rad; full R3/D03 orange/P1-dörr ingår inte i G6.

### Verkliga luckor och STOPP-kontroller (inte uppfunna mätningar)
1. **Reversed P0 X-sort:** Ingen fryst ROM visar *vit-först, gul-sedan* med korrekt `RESP0/GRP0/COLUP0` och originalmask samtidigt. I G6 måste båda ordningarna få äkta numerisk RAM-X → fysisk ordning, inte bara ett fast 2-state-switch. `Player::resp` i Stella 6.7.1 har en branch under aktiv render och `NUSIZ0` ändrar interna copy-decoders; enkel `X≈3c` räcker inte.
2. **M0 på SAMMA scanline med `NUSIZ0=$02`:** Detta är den starkast riskfyllda nya detaljen. Atari TIA kopierar även **missiler** enligt NUSIZ0-kopieläget. Historiska R1f/R1g ritade M0 på **raden före** NPC-bandet. Ett nytt prov måste visa **exakt en** M0 och rätt pixel/färg, alternativt stoppa om `NUSIZ0`-stopp-/omkopplingsordning förstör P0 START/cykelbudget.
3. **PF kan inte magiskt bli gratis:** två verkliga bruna kanter behövs på minst samma rasterband, PF-data skall preloada bara när dess faktisk radkod är konstant. R3 gjorde sex PF-registerskrivningar och P1-orangedoor i egen ROM, källestimat upp till 74/76. En full R3/P1-orange dörr samtidigt med vit P1 android är **senare integreringstest**, inte löst genom denna GO.
4. **Total instruktionskostnad är okänd:** Source F10:s P1-only 61/76 är inte en färdig mixed-P0-kernel. G4 har INTE producerat en trovärdig total CPU-cykellista för alla framtida A1/A2/B1/B2. Det är därför GO uttryckligen är villkorad av **en obligatorisk framgångsrik G0**, annars NO-ROM.
5. **Nära-/överlappande P0/NPC-X:** Fyra 8CC-originalpixels kan inte få två separata färger i en färgklocka. P0-omtriggningen kan klippa första aktörens pågående bitmap; den separata X2-scenvarianten skall bedömas som framtida överlapp-/läsbarhetsfall och *inte* tyst vara PASS när bara en vit aktör återstår.
6. **Full numerisk sex-X/Y:** Fyra P0/P1 aktörer i ETT mikroprobe är ett byggstensbevis. De övriga tre vita NPC, R2 key, R3 door, R4 full crossing, 128-byte registerkollision och 4K resident kernel är **fortfarande blockerande** för full R1.

## 3. A/B/C beslut med per-provsstopp
| Plan | Exakt åtgärd | Utfallet bedöms som |
|---|---|---|
| **A – huvudväg** | En framtida, explicit beordrad G6 mikro för H4-ONE. G0 förregistrerar P0 vänster↔höger numerisk X-sort/resp/GRP, två P1 original, PF äkta brunt, **en** M0 samma Y, VBLANK-prep, 9 originalrader. G1/Stella bara vid G0 PASS. | `GO_TO_ONE_SEPARATELY_AUTHORIZED_G6_G0_PREFLIGHT`, inte R1 PASS |
| **B – teknisk reserv** | Om A:s single-M0/dual-`NUSIZ0` interfererar: en **enda** alternativ source-only `NUSIZ/HMOVE/VDEL`- eller kanaltilldelning **inom samma acceptance** utan skott på föregående rad, utan färg-/maskfusk och utan ny mapper. Kräv ny G0-beräkning före ROM. | `G0_REVISED_SOURCE_ONLY`, inget automatiskt ROM-svep |
| **C – stopp/eskalation** | Om A/B saknar giltig START/GRP/färglivstid eller worst-case 76c, eller M0 dupliceras/försvinner, stoppa. Beskriv exakt vilken hårdvarupixel/cykel eller originalmask som fallerar; eventuellt G5 användarval separat. | `NO_GO_FOR_CONCRETE_ALLOCATION`; full R1 förblir BLOCKED. Ingen designwaiver utan uttryckligt godkännande |

**Särregel:** X1 (två olika kravfärger på samma slutpixel) får inte betecknas `PASS` för någon enkel P0/M0-allokering. Det är en *negativ kontroll av färgmodellen*, inte samma sak som ett globalt R1-no-go. Ingen användarbeslutad tolerans för ett sådant misstolkat skott/occlusion finns.

## 4. Exakt leveranspaket och beslut att överlämna till MAIN i senare order
- [G4 förregistrerad source-hypotes](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md) med **A1/A2/B1/B2** numeriska mål, P0-sortering, riktiga 8×9 top-down-masker, NUSIZ-missilrisk, M0/PF och X1/X2 negativa kontroller.
- [G4 register-/colorclock-timeline](G4_REGISTER_TIMELINE_2026-11-17.csv), där alla icke observerade c-tider med flit är `NOT CALCULATED`, inte falska "mätvärden". G0 ansvarar senare för exakt worst-case opcodes, G1 först då för Stella.
- [G3 ursprungligt resurskontrakt](G3_RESOURCE_CONTRACT_COMPLETION_RECEIPT_2026-11-17.md), [G2 historiskt originalbevis](G2_COMPLETION_RECEIPT_AND_FEASIBILITY_BOUNDARY_2026-11-17.md), [G1 besluts- och grafikkälla](G1_COMPLETION_RECEIPT_2026-11-17.md).
- [Färdigt arbetsorderutkast som INTE är utfärdat](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md), för ev. framtida uttrycklig userauktorisation till ROM DEVELOPMENT III; oberoende VERIFICATION II får ej förhandsbjudas att certifiera den.

**G4 bedömning:** `G4_SOURCE_ONLY_COMPLETE_CONDITIONAL_GO_ONE_MICROPROBE_NOT_ORDERED`.
**R1/full v0.18:** `BLOCKED_NOT_ACCEPTED`.
**F11:** `SOURCE_ONLY_G0_FAIL / G1_NOT_RUN`; ingen efterhandsändring.
**G5:** ingen utlösande tvingande användarwaiver eller extra beslut nu; endast om G0/nytt prov visar faktiskt designblock.
**G6:** `NOT_AUTHORIZED`. Inga extra ROM- eller forskningssteg startade här.

## G4-arkiveringskvittens – fullständiga Drive-kopior 2026-11-17

- **Sökbar Google Drive-kopia av fullt GO/NO-GO-beslut och förregistrerad hypotes:** [G4 beslut och teknisk hypotes](https://docs.google.com/document/d/1dCYnzJmI5osXGgcGVygIHX8cfgbYDuVOpvfZbKnBsb4/edit).
- **Sökbar Google Drive-kopia av 21 rad-händelser och framtida uttryckligen EJ UTFÄRDAD G6-order:** [G4 register och endast utkast](https://docs.google.com/document/d/1KGcTovnA9XgSBmqm8aVHSjhoBYguGda5A02arBS-8w0/edit).
- Bägge native Google Docs **skapades i och lästes tillbaka från** officiell projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`. GitHub-filerna är primär auktoritet för råa tidsrader och source text; Drive är extra bevarande.
- **Ingen** bokad eller inledd G6-ROM, Stella, DASM, F12, eller E02. Det finns bara en villkorad rekommendation om en framtida G0-stoppstyrd mikrofysikgrind.

## 5. Slutlig styrning
Den tekniska prioriteringen är **EN** datastyrd mikroskopisk falsifiering framför fler fyra-mode-kodprofiler eller en sex-NPC-kernel på gissning. **Ingen** ny ROM, DASM, Stella, CI, oberoende E02, F12, gameplay, PAL, cartridge/mapperändring, PR-merge eller canon waiver är avsedd eller utförd i G4. Source-only GO är en forskningsrekommendation; teknisk verklighet avgörs först i separat godkänt experiment.
