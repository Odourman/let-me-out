# LET ME OUT! – MAIN VI G5I: PLANAVSTÄMNING, FEMFIENDERS DELTABASLINJE OCH BESLUTSSPÄRR FÖRE G6
**Datum:** 2026-11-17. **Status:** `G5I_SOURCE_ONLY_PLAN_RECONCILIATION_COMPLETE_G5_FORMAL_CUTOVER_PENDING_G6_NOT_AUTHORIZED`.
**Användarorder:** "Ok, om vi klara med nuvarande steg fortsätt då till nästa. Om inte, så gör klart nuvarande steg. Tänker du på vår plan och våra förberedelser?" Denna order innebär att MAIN först måste bedöma om den **faktiska, formella G5-grinden** är avklarad. En avslutad teknisk **G5H-delforskning** får inte tolkas som G5-CANON PASS eller ge en automatisk G6-ROM-order.

## 1. Källauktoritet som verkligen lästs i detta steg
Vid granskningens början GitHub `main` = `a48970eea9af460f36dcbd4e5282ddefdb867672`. Jämförde:
- [Bindande närmast aktuella G1–G10-definition](../MAIN_VI_DEEP_REASSESSMENT_30_TRICKS_FEASIBILITY_AND_TEN_GATES_2026-11-17.md), kompletterande [G1–G10 A/B/C playbook](../MAIN_VI_G1_G10_CONTINGENCY_PLAYBOOK_A_B_C_2026-11-17.md), [historiska 10+10 – märkt ersatt för framåtplanering](../MAIN_VI_LAST_10_CURRENT_NEXT_10_ROADMAP_2026-11-17.md).
- [G4 villkorad GO för EN separat G6-mikro](G4_ONE_EXPERIMENT_GO_NOGO_DECISION_2026-11-17.md), [G4 framtida arbetsorder uttryckligen DRAFT_NOT_AUTHORIZED](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md).
- [G5 feasible-review](G5_CANDID_FEASIBILITY_ASSESSMENT_AND_DECISION_BRIEF_2026-11-17.md) och [G5 bindande beslutsspärr](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), båda GitHub som versionsstyrd originalkälla och båda fullständiga officiella Drive-kopior via Google Drive-anslutning lästa tillbaka.
- Nytt read-only tekniskt G5F [speglad PF](G5F_FIVE_ANDROID_REFLECTED_PF_DOOR_SOURCE_ONLY_ARCHITECTURE_2026-11-17.md), G5G [Ball x0 och opcodebudget](G5G_BALL_LEFT_WALL_AND_FIVE_NPC_OPCODE_CENSUS_SOURCE_ONLY_2026-11-17.md), G5H [24+36 X-ordningar och naiva kernelbegränsningar](G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md); G5H Drive läst tillbaka.
- Originala fyra 8×9 rättvända masktyper [design/NPC_REFERENCE_8x9_masks.json](../../design/NPC_REFERENCE_8x9_masks.json), frysta R3/C02-källa [P1 orange door med inbyggt transparent svart nyckelhål](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md); historiska [v0.18 C01/C02/D03 acceptance](../ROM_GATE_V018_ACCEPTANCE.md).

**Auktoritetsordning:** uttryckliga senare användarbeslut om design väger högre än äldre förslag, men ett forskningsdokument eller assistantbedömning kan inte ändra formell baseline eller starta en ROM-order. Existerande historiska experiment, hashes, negativa resultat och E02-separation ska förbli oförändrade.

## 2. Riktig status för vår plan – vad som är avslutat respektive INTE
| Planerad grind | Faktiskt läge | Vad får ske utan extra user-order? |
|---|---|---|
| **G1** krav-/baseline och authority | READ-ONLY UNDERLAG KLART | Läsa/rapportera |
| **G2** kontroll av originalkällor, 600-PNG historiska tester och negativa R1ba/F11 | READ-ONLY UNDERLAG KLART | Läsa/rapportera |
| **G3** gemensamt TIA 76c/128B/4KB/PF/färgkontrakt | SOURCE-ONLY UNDERLAG KLART | Källanalys |
| **G4** en falsifierbar minimal P0/P1/M0-hypotes | SOURCE-ONLY KLAR, EN MICRO **VILLKORLIGT** rekommenderad | Inget G6-bygge |
| **G5** feasibility bedömning | **TEKNISK RAPPORT KLAR**; G5F/G/H källförstudier avslutade med negativa naiva worst-case och positiv OFFLINE vägggeometri | Beslutsunderlag/deltaförberedelse |
| **G5** formellt beslut/canon/reviderade testkrav | **INTE KLART: FORMAL REBASE PENDING** | Dokumentera användarens uttryckta femfiendersmålsättning utan att skriva om historisk C01/C02 |
| **G6** ett begränsat, källpreflight-styrt fysik-ROM-mikro | **NOT AUTHORIZED / NOT ORDERED** | Inte skapa ROM, branchar, G0-implementation, programmeringsorder |
| **G7–G10** full R1, R2/R3, R4/E02, gameplay | **BLOCKED, egna framtida expressmandat** | Endast beredskap |

**Beslut för användarens "fortsätt om klara":** G5:s fristående källstudier G5F/G5G/G5H är färdiga i sitt avgränsade scope, **men G5-grinden är fortfarande INTE genomgången**. Därför startar MAIN VI INTE G6/ROM DEVELOPMENT III, utan färdigställer nedan exakt G5:s förberedda delta-/beslutspaket. Det undviker ett felsteg där gammal G6/G7 testar sex NPC efter att användaren tydligt har orienterat arbetet mot fem.

## 3. Det användaren REDAN har uttryckt – fråga inte om samma sak igen
- **Föreslagen målmaskin:** fortsatt **original Atari 2600**, standard-F6/NTSC som teknisk projektbas. Användaren har inte valt Atari 7800 eller extra ARM/cartridgeformat.
- **Antalsriktning:** användaren har diskuterat **5 fiender: 2 stora manliga, 1 stor kvinnlig, 1 liten manlig, 1 liten kvinnlig**, uttryckligen följt upp med "med dessa förändringar, 5 fiender och den fixade dörren" och fortsatt forskningsorder. Det är **en verklig användaruttryckt målriktning**, inte MAIN:s påhittade 6→5-waiver.
- **Färger:** bakgrund ska vara **svart**; brown väggar, yellow player, white androids, gold key, orange right door med **svart utskuret transparent keyhole i DÖRR-masken**, aldrig en fristående keyhole sprite.
- **Dörrmetod:** isolerat R3 har developer-local-PASS med **P1 orange + samma bitmap-negativa nyckelhål**. En **Ball+REF vänstervägg** är först en OFFLINE 3520/3520 kartcellskorrekt forskningskandidat, **inte** en godkänd ny integrerad ROM-renderer. Bevara R3 som fryst fallback.
- **Inte auktoriserat eller beslutat:** minskad 8x9-silhuett; 10 Hz flimmer; tyst saknade hotande NPC; tappad nyckels logiska X/Y ändras; fiender låses till specialformationer; ändrad P0/M0-skottfärg; separat utgång vänster; mapper/PAL/PR7/E02/fullspel eller ny ROM.

**Viktig gräns:** Dessa uttryckta önskemål skall styra framtida beslut, men G5F/G5G/G5H har samtliga uttryckligen bevarat historisk testcanon och användaren har ännu **inte** godkänt ett precist reviderat G6/G7 acceptance-/sam­tidighetskontrakt. MAIN får inte kalla den gamla 6-NPC v0.18-romens kriterier för automatiskt PASS efter att ha räknat fem.

## 4. Förberedd men INTE UTFÄRDAD fem-NPC cutover-delta
Följande tabell är **förhandsspecificerade ändringar som skulle behövas OM G5 formellt godkänns**. Gäller inte på retroaktivt R1–R4 eller frysta F9–F11.

| Historisk test/scope | Föreslagen framtida 5-NPC version | Bevarad blockerande princip |
|---|---|---|
| R1 C01 6 vita (M,M,F,F,SM,SF) + gul P0 + skott | **5 vita (M,M,F,SM,SF)** + full gul player + exakt ett synligt skott | Alla fem samma Y även svåra X-ordningar, varje numerisk X/Y |
| R2 C02 5 kvar efter dödsfallet + gold key | **4 kvar** + guldnyckel + player + skott | Original X/Y/key efter event, nyckelns O1-skymning bara vid faktisk överlapp |
| C04 fyra 8x9 originalformstyper | **Samma fyra masktyper byte för byte**, M duplicerad | TOP-DOWN, inga felvända original, bevarade tomma maskrader |
| D01–D03 endast högerport orange + svart keyhole | **Oförändrad visuell design**, svart COLUBK och brun PF, nytt Ball+REF endast om verifierat | Ett keyhole är NEGATIVT UTRYMME inuti orange DÖRRBITMAP, ingen extra sprite |
| R4 stress, numerisk mobilitet | **5 självständiga X/Y plus player** med player-mellan-två-män, trånga/delvis gemensamma Y | Ingen 4-mode/profile-fusk, ingen osynlig NPC utan uttryckligt userdesignbeslut |
| G6 preliminär H4-ONE mikro | Samma lilla **tekniska primitiv** kan eventuellt användas med 5-mål; inget fullspelsbevis | G0 statisk källa/START färgfönster före en enda ROM, och särskilt expressorder |

**INGEN av ovanstående acceptansändringar träder i kraft genom denna rapport**, och ingen äldre G7/G8-plan får tyst ersättas utan godkänd scope-revision.

## 5. Aktuellt tekniskt utfall: varför G5 inte kan signeras som full GO
- G5F: alla fyra rum 18/22 speglade kart­rader; 4/22 samma högra D-undantag; alla fem aktiva på sex av nio 8x9-maskrader.
- G5G: Ball x0 + speglad PF har **3520/3520 offline-väggcells-matchning**, men fysisk BL-position/ENABL/missile/P1-/dörrfärg ej verifierad; naiv A/B-orangedoor på stadig same-Y-rad **79/76 CPU** (den tidigare PF0-togglingen **89/76**) INKL. immediate-maskladdning men UTAN RAM-X/Y/TIA-start etc. Direct plan FAIL i detta fall.
- G5H: 24 P1-ordningar A kräver rad6 **79/76**; B har 36 ordningar, **74/76** när båda stora M hålls ihop men **79/76** när gul player går mellan dem; vid en hypotetisk G4-gul M0-färgkonflikt kan direkta summan nå **89/76**. `NUSIZ` fasta kopior hjälper inte godtyckliga 20-colorclock X. **G0 full fysisk plan NOT PASSED** och ingen ny Stella genomförd.
- Negativa budgettal är *för naiva direkta opcode-sekvenser*, inte matematisk omöjlighet för fem NPC på Atari 2600. **Men de ger inget skäl att förklara G5/G6 klar** eller automatiskt utfärda F12.

## 6. Gräns för nästa möjliga arbetsmoment
**G5:s käll-/förberedelsedel kan avslutas nu med ett transparent valunderlag.** Nästa *obligatoriska* steg är **formellt avgränsa G5-design, testkrav och visuell samtidighets-/occlusion-policy** mot femfiendersmålet. Om användaren inte uttryckligen godkänner avvikelser bör gamla stränga synlighetskrav antas fortsätta, inte försvinna. Samma-Y-färger, P0/M0 och P1-orange mot vit behöver fortfarande en fysiklösning.

**G6 får först övervägas efter särskild explicit ROM-auktorisation**, med en scope som förklarar om det är original-G4 H4-ONE-minimala fysiktestet eller en ny femfiendersvari­ant. Den gamla sex-NPC-G7/5+key-G8-planen kan inte fungera som nytt femfienders-R1/R2 efter tyst sök-och-ersätt. Ett senare G6 GO verifierar bara den lilla, i förväg namngivna hårdvarumekanismen, inte spelets användarsynliga fem-NPC-krav. Separat oberoende VERIFICATION II först efter fryst ROM och separat order.

**Main rekommenderar inte** att fortsätta med G5J/G5K och fler kosmetiska cycle-censuses utan en ny konkret kernelarkitektur eller ett användarägt visuellt kompromissbeslut. Bevara forskning, stoppa falska PASS, håll normal Atari 2600 som mål så länge användaren så önskar. Inget datum eller tidsuppskattning för att "vara klar" kan legitimt utlovas.

## 6A. Bekräftad Drive-kopia i officiella projektmappen
- [Google Drive: G5I plan- och beslutsavstämning, fullständigt läst tillbaka](https://docs.google.com/document/d/1Zc-n5K-RHRZ5YriInxyQBqmb99siXl44547cVteT1YI/edit). Native-dokumentet skapades, flyttades till `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`, lästes tillbaka och kontrollerades för G5I-status, G1–G10, R1-acceptansdelta och spärren mot G6/ROM. GitHub är versionsstyrt källoriginal. Ingen ROM, ingen canonändring.

## 6B. Nya konkreta G5J/G5K-underlag efter användarens "fortsätt"

[G5J extern primärkälla Berzerk och 176-raders occupancy](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5J_BERZERK_PRIMARY_SOURCE_LANE_KERNEL_AND_FIVE_NPC_SCOPE_OPTIONS_SOURCE_ONLY_2026-11-17.md) · [Drive med full G5J](https://docs.google.com/document/d/1yV_4qJdesdrN1d8IbOVA9kbjY-KjCR9zba8wuBzjpDM/edit); [G5K ny 176-raders dynamisk P0/P1-ägarallokering, vit robot flyttas till P0 under orange dörr](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5K_BERZERK_LANE_DYNAMIC_P0_P1_DOOR_R1_R2_SOURCE_ONLY_2026-11-17.md) · [Drive G5K fulltext och CSV](https://docs.google.com/document/d/1OuqluwyUycObf-tB27SoN-kKaqvwVUWbdmUal7oqB60/edit). G5I slut­satsen att **formell G5-cutover återstår** gäller, men forskningsstatus har förbättrats: en faktisk historisk 8-robotars vertikal-lane-spelmekanik och en **conditionally cheaper** P0/P1-door-kandidat finns. G5K:s 37/47/62c är inte källmask-/registerfysiska pass utan naiva direktopcodes. Ingen användarwaiver för begränsad Y, O1/shot/color eller en G6-ROM-order har skapats.

## 7. Fil- och auktoritetsmanifest
- G5I är **en source-only MAIN VI-grindavstämning**. Det är **inte** en ROM DEVELOPMENT III-prompt, inte en ändring av `ROM_GATE_V018_ACCEPTANCE.md`, `design/NPC_REFERENCE_8x9_masks.json`, original 57 beslut, Issue #6 scope eller E02-fryst baseline.
- Vid senare faktisk userbeslut skall en ny explicit versions- och kravdelta skrivas, följd av separat G6-uppdragsorder med pass/fail. Inga andra projekt eller repo påverkas.
