# 05 – Risker, stoppkriterier och kompromissgrindar

## Viktigaste blockerarna
1. **Rasterkomplexitet:** 6 android + spelare + skott eller 5 android + nyckel + spelare + skott (8 logiska enheter på samma höjd). Fler RAM-banker eller större ROM löser inte scanline-/objektbudget.
2. **Asymmetrisk högra dörren:** Inre playfield speglas, men endast högerkant får bli öppen. `PF0`-omskrivning är forskningshypotes, inte verifierad implementation.
3. **Orange port och svart nyckelhål:** Fyra horisontella färgklockors ytterbit ger knapp upplösning; separat TIA-objekt kan konkurrera med skott och androider. Hålet kan bli tekniskt dyrt.
4. **Liten tolerans för flimmer:** användaren accepterar *lite*, inte dolda fiender eller förlorade skott.
5. **Nyckel under android:** O1 är godkänd, men om android står kvar på nyckeln kan synligheten vara blockerad i praktiken utan tidsgräns; dokumentera tidsvaraktighet i framtida speltest, ändra ingen mekanik tyst.

## Tillåtna diagnostiska förenklingar
- Statisk styrd testscen och förprogrammerade objektpositioner i stället för riktig AI.
- Testsymbol för skott i stället för komplett skottfysik (så länge det uttryckligen redovisas).
- Diagnosflagga som öppnar dörr utan full nyckellogik.
- Brun teknisk bas för högeröppningsförsök, **bara** som isolerad testbaseline, inte ett nytt godkänt visuellt mål.
- K09 som reserv att **testa mot** K11, inte att fastställa utan faktisk visuell jämförelse.

## Inte tillåtet utan nytt beslut
- Minska sex androider till fyra, använda samma silhuett för alla trots fyra godkända utseenden, eller göra robotar/ofarliga för att vinna rastertid.
- Göra nyckeln bärbar av android igen, flytta den vid skymning eller dölja den avsiktligt i bildruteväxling.
- Förvandla den godkända högerdörren till vänster-/dubbelutgång eller ta bort den svarta symbolen som slutligt designmål.
- Ändra poäng, extralivströsklar, fienders AI-regel, ljudregler, RESET-exklusivitet eller lägga in en separat startskärm som permanent spelregel.
- Presentera offline-simuleringar som Stella- eller hårdvarutester.
- Göra själva pilotdiagnostiken till ett fullskaligt spel utan nytt uppdrag.

## Stopp och nästa tillstånd
Om R1/R2 misslyckas: skriv kort teknisk blockerarrapport, bevara alla tester och presentera högst två tydligt avgränsade alternativ för MAIN. **Gå inte vidare till fullspel.**

Om bara svart nyckelhål misslyckas: dokumentera det skilt från port/öppningsfunktionen och begär användarbeslut om symbolförenkling. Ingen automatisk waiver.

Om tekniken fungerar: be om oberoende VERIFICATION och invänta godkänt slututlåtande innan eventuellt *separat* senare gameplay-uppdrag formuleras.
