# LET ME OUT! – MAIN XI: senare uttryckligt beslut, BRUN PF-dörr med SVART kontur

Datum: 2026-11-20
Status: `EXPLICIT_USER_DESIGN_DECISION_FUTURE_BROWN_DOOR`
Prioritet: senare uttryckligt användarbeslut som ersätter tidigare tvingande framtida ORANGE dörrfärg och därmed den tidigare P1-orange-först-ordningen, endast inom exakt angiven dörrfärg/utseende och teknisk prioritering.

## Ursprungligt användarbesked

Efter MAIN XI:s jämförelse av tre färgalternativ, där "1. Brun PF-dörr med svart kontur och nyckelhål" rekommenderades som tekniskt enklast, sade användaren:

> "Jag tycker att vi kör med 1an då. Med svart kontur.
> Jag har inte gett senaste prompten till Rom development än. Ska du ändra något med den innan jag ger den?"

**Tolkning:** användaren väljer **brun dörr i samma färg som den bruna playfield-ytterväggen, med tydlig SVART kontur och SVART igenkännbart nyckelhål** som framtida designmål. Föregående krav om en **orange** dörr i framtida spel ersätts på denna punkt av en lika brun dörr. De tidigare illustrerade orange skisserna och den tidigare P1-orange-testrekommendationen är historiska alternativ, inte bindande första prioritet. Svart kontur och nyckelhål är frånvaro av PF-/dörrgrafik, så svart bakgrund syns; inga extra svartmålade P0/P1-objekt krävs. Ett stort svart hål med en brun rektangel utan läsbar nyckelhåls-/dörrkontur räknas inte automatiskt som visuellt godkänt.

**Varför och vilka risker återstår:** `COLUPF` kan vara oförändrad brun `#$26` under ytterbandet, vilket potentiellt eliminerar tidigare orange→brun-färgfönster/spill och sparar CPU, men den verkliga 6507/TIA-planen måste byggas och mätas. Speglad `CTRLPF=$01` ger horisontell upplösning i 4 färgklockor per PF-bit; symmetrisk kontur kan kräva flera PF-maskrader. Konturen får inte se ut som flera giltiga utgångar eller lämna oavsiktliga visuella/mer än avsedda kollisionshål. Exakt ny PF-bytegeometri, bredd och bästa detaljform avgörs efter visuellt riktigt emulatorprov; ingen tyst sänkning av synlighet eller enda dörr. Den tidigare accepterade grövre nyckelhålsliknande silhuetten (ungefär 16px huvud/8px skaft) är godkänd kandidat, inte en exakt bitmappstvingande canon. Ingen pixelidentisk R3-form krävs längre.

## Vad som INTE ändrats

- Exakt **en** låst dörr och verklig öppning i övre eller nedre yttervägg beroende på framtida karta; vilken karta som får vilket läge är ännu inte bestämt.
- Dörren ska synas och se ut som en **låsbar dörr**, stoppa spelaren tills riktig nyckel har tagits, öppnas till svart bakgrund och kräva verklig fysisk passage. Ingen andra utgång, ingen väggskada.
- Svart bakgrund, **bruna** innerväggar, gul spelare, fem individuella **vita** fiender, guldnyckel. Nyckeln och de fyra ursprungliga TOP-DOWN 8x9-maskerna ändras inte. Framtida utseenden väljs oberoende slumpmässigt per individ, utan att låsa en viss blandning.
- Fem fienders fria logiska X/Y, AI, kollision, skott, nyckelfall, poäng/liv och synlighetskrav kvarstår. Ingen flimmerwaiver eller osynlig NPC som dörrpris.
- Tidigare frysta ROM:ar och originella designreferenser ska bevaras. Detta är inte ett beslut att retroaktivt skriva över historiska R3-/orange-PF-original.
- `G5_FORMAL_OPEN`, `INDEPENDENT_VERIFICATION=NOT_RUN`. Beslutet ger inte automatisk V03/G6/F12, fyra-rums-kartcutover, PAL-/mapperbyte, PR-merge, release eller oberoende godkännande.

## Avgränsad provordning och ännu inte skickad prompt

Användaren har uttryckligen sagt att tidigare kopierbara prompten om **orange P1-dörr** ännu **inte skickats** till separat ROM DEVELOPMENT IV. **Skicka den inte oförändrad.** MAIN XI ska i samma Issue #31 **ersätta dess prioritering** med `BROWN_PF_DOOR_BLACK_OUTLINE` som första verkliga V02-testspår: två verkliga test-only F6/NTSC-varianten TOP och BOTTOM från fryst `4c4fc5b7c5545217b2321a38d9db6db5dac7db2f`, där PF håller brun dörrfärg och svart negativ kontur/nyckelhål, tillförlitligt lock/unlock/exit, fem NPC/key/player, raster-, RAM- och pixel-/kollisionsbevis. Det tidigare orange P1-spåret får behållas som historiskt alternativ eller jämförelse, **inte** drivas som aktuell förstahandslösning. Om den bruna lösningen inte kan ge igenkännbar synlig dörr inom budget: dokumentera negativt och återkom för nytt kreativt färgval, i stället för att själv återgå till orange som slutcanon.

Detta dokument är nytt designbeslut, inte påstående att en brun ROM byggts eller att en separat Codex-chatt har startats.
