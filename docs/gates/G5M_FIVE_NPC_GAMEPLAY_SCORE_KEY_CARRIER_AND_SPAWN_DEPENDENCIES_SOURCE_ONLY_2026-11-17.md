# LET ME OUT! – MAIN VI G5M: FEM-FIENDERS FÖLJDBEROENDEN I POÄNG, NYCKEL OCH SPAWN
**Datum:** 2026-11-17. **Klass:** `NEW_SOURCE_ONLY_DESIGN_DEPENDENCY_REVIEW_NOT_APPROVED`. **G5 formal user decision pending, G6 NOT AUTHORIZED.** Denna fil är ett **nytt kompletterande sakfynd** efter kontroll av fullständiga ursprungsarkivet och 30 trick/research. Ändrar inte canon, kod, source-baslinje, historiska v0.18 acceptance eller officiell E02.

## 1. Ny kontroll av originalet, inte ett minne
I [ursprungliga 21-fils-handoff-ZIP med 57 beslutsrader](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), `03_DECISIONS.csv`, granskades originalbeslut 005–007, 021–025, 042–047, 008, 019–020, 032–034, 051–052, 055 och 057. Den aktuella femfiendersinriktningen M,M,F,SM,SF och svart bakgrund är senare **uttryckt av användaren**, men ingen tyst 57-besluts-/R1-acceptanscutover har gjorts. Orignalhandof­fens ZIP SHA-256: `f291d07af34e12866cd9785387e8ba1d320aa341b70e9646c28e3e0a78896ff4`. ZIP CRC kontrollerades utan fel. Source-snapshottad GitHub HEAD före denna paketskrivning: `2cbb600f6933f181b92e4180cf0c5eef97fd9919`.

## 2. Kritisk poängupptäckt: fem fiender ändrar long-run all-kill-värdet
Kanoniska regler: `-25`/förstörd NPC (043), `+50`/nyckelupptagning (044), `+100`/verklig utgång (045), `+15`/levande NPC vid utgång (046), golv `0` utan skuld (042), all-kill inte en långsiktig positiv highscorestrategi (047).

Vid `N` initiala NPC och `k` förstörda, efter att spelaren faktiskt plockat upp key och lämnat rummet, och **när poängsaldot hela vägen är tillräckligt för att inga avdrag ska klampas till noll**, blir nettopoängen
`Δ = -25k + 50 + 100 + 15(N-k) = 150 + 15N - 40k`.

| Fall | Tidigare N=6 | Föreslaget N=5 | Betydelse |
|---|---:|---:|---|
| Endast nyckelbäraren dödad, k=1 | +200 | +185 | Lagom risk/reward ändras |
| Alla dödade, k=N | **0** | **+25** | **Ny repeterbar tillväxt via all-kill**, mot avsikten i beslut 047 |
| Levande-bonus efter k=1 | 5×15=75 | 4×15=60 | Max survived bonus minskar |

**Golvet gör ordningen viktig vid låga saldon:** Om man startar på 0 och dödar ALLA innan key pickup, klampas straffen till 0 och rumsavslut blir +150 för båda N. Om key plockas upp mellan dödsfallen kan senare -25 dra ner de redan erhållna +50, så första rummets slutpoäng kan bli annorlunda. Siffrorna 0 och +25 är **long-run nettodelta utan klampning**, INTE generellt korrekt för första rummet. En verklig framtida regression måste testa både nyckelupptagning före/efter resterande kills och minst tre på varandra följande rum.

**Ej godkända framtida val:** (A) behåll alla belopp och *godkänn* +25/rum vid all-kill; (B) lägg till en användarbeslutad -25 vid all-kill; (C) ändra t.ex. kill-straff till -30 eller exitbonus till +75, med konsekvenser för all annan poängbalans. Detta är **alternativ att lägga fram**, inte kodbara beslut. Behåll gamla 043–047 tills användaren väljer.

## 3. Nyckelbärarslump och fem spawnpositioner är inte automatiska
- Beslut **021**: ursprungligen **sex** slumpmässigt valda av förhandsvaliderade startpositioner. En femfiendersversion kräver ett nytt *explicit* 5-of-candidates urval, avstånd/pathfinding/rumsnavigering och samma åtkomlighet för alla robot-/nyckelplatser (020), samt spelaren vid vänstra väggen (015). Det räcker inte att sätta `NPC_COUNT=5` utan att kontrollera slump/spawn-policy.
- Beslut **022**: exakt en slumpad bärare med **1/6 per individ** med sex. Ett uniformt femfiendersmål kräver **1/5 per individ**, men det är en **framtida design-/PRNG-revisionspost**. Beslut 023–025 om att key uppstår på fallplatsen och kan passeras av andra androids gäller fortfarande.
- AI-beslut 008, 019, 032–034 kräver likvärdig rörelse, fyra riktningar, jakt vid första skott, undvikanden och att robotarna kan blockera högerdörr men inte lämna rummet. En Berzerk-liknande **Y-lane-spärr** kan ändra vilka vägar AI får gå, effektiv jakt och möjlighet att nå key/door; den är inte godkänd.
- Beslut 055 om "mörk/svart" bakgrund supersederas i denna del av användarens senare direkta **svart** som designriktning. Det är inte en verifierad exakt TIA color registerbyte.

## 4. Varför de 30 tricksen inte kringgår beslutsbehovet
[Källgranskad 30/30-metod och G5L slutrapport](G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md): S0 fem fria same-Y originalmasker saknar G0-pass; S1 Berzerk-inspirerad Y-lane P0/P1+P1-orange-door kräver explicit rörelsewaiver; S2 flimmer saknar acceptans. Inget TIA-/6507-trick korrigerar per automatik all-kill-belöning eller nyckelbärarens fördelning. **R2:s key+door+fiende-samma-Y** med O1 endast preliminär skymningspolicy kan inte tyst göras "gratis". G5L **teknisk research färdig**, G5 **formellt öppet**, G6/ROM **inte auktoriserat**.

## 5. Project Sources-paket och revisionsavgränsning
**Sourcepack:** `LET_ME_OUT_PROJECT_SOURCES_2026-11-17.zip`, full 9-file Markdown/CSV/SHA256-manifest, i [officiell Google Drive-projektmapp](https://drive.google.com/file/d/1Pv0TUKoN3QVu-Yy8UZFOhlv7OgoGOQit/view). Packets egna källor och uppdateringsmetod har prioritet **navigation-only**. Ingen automatisk ersättning av MASTER SPEC, beslutsregister eller projekt-CURRENT.

Ingen ny .asm/.bin/stella, G6-experiment, PR-merge, ändrade 57 beslut, ny gameplay canon eller oberoende VERIFICATION skapad. Nästa legitima steg är dokumenterat explicit G5-design-/poäng-/nyckel-/spawnval och sedan en separat avgränsad G6-order.
