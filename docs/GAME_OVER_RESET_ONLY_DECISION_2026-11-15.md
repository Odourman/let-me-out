# Let Me Out! – beslut om GAME OVER och RESET

**Datum:** 2026-11-15
**Projekt:** Endast Atari 2600-spelet Let Me Out!
**Status:** BESLUT om grundflödet; exakta effekter behöver tekniskt och visuellt test innan slutlig pixelimplementering.

## Användarbeslut

Användaren säger: "Vi gör som Berzerk,men reset startar om spelet. Inte ett knapp tryck". Detta följer på den tidigare instruktionen "Ingen start skärm" och samtalet om Game Over med färgväxling och blinkande poäng.

1. **Ingen separat startskärm.**
2. **GAME OVER** efter sista förlorade livet. En Berzerk-inspirerad, enkel slutpresentation i det befintliga labyrintfältet är det visuella målet: avvikande/växlande kontrastfärger och blinkande slutpoäng. Exakt färgval, frekvens och utseende är öppna för senare tekniskt/visuellt test.
3. **Endast konsolens GAME RESET/RESET startar om efter GAME OVER.** En omstart ger nytt spel med tre startliv och noll poäng. Highscore behandlas enligt tidigare särskilt beslut, inte som nollställt av detta beslut.
4. **Joystickens FIRE får inte starta om spelet vid GAME OVER** och får inte skapa ett skott när spelet har upphört. Fire är endast relevant för skjutning under pågående spel.
5. **RESET under pågående spel startar om spelet**, enligt normal Atari 2600-konsolprincip. Omstart är inte en död eller rumsutgång och utlöser ingen rumsbonus.
6. **Ingen separat GAME OVER-skärm krävs.** Befintlig spelplan kan ligga bakom effekten; grafikdetaljer och ljud är inte slutligen fastställda.

## Faktakontroll – Berzerk-originalet

Berzerks Atari 2600-manual anger uttryckligen att GAME RESET startar spelet om, och att joystickens Fire också kan starta ett nytt spel när det är slut. Det nya Let Me Out!-beslutet avviker därför medvetet från Berzerk genom att **förbjuda omstart via Fire**. Den ursprungliga manualen bekräftar **inte** att Berzerk Game Over specifikt inverterar skärmens färger eller blinkar totalpoängen. Vår visuella effekt ska därför benämnas **Berzerk-inspirerad**, inte beskrivas som tekniskt verifierad kopia.

Källa: https://www.atariage.com/2600/manuals_old/berzerk.html

## Teknik och verifiering – ej utförd

- Speltillstånd: `PLAYING`, `GAME_OVER` och omstart med `RESET` är *logisk design*, inte körbar 6502-kod.
- Vid GAME OVER ska vare sig Fire-tryck, styrspaksrörelse eller ett kvarstående projektiltillstånd ge gameplay-effekt.
- RESET-prioritet och switch-debounce ska testas i verklig ROM efter separat auktorisation.
- Färgväxling och blinkande poäng ska vara långsamma/läsbara; användarens flimmertolerans omfattar **lite flimmer**, inte obegränsat.
- Påslag av konsolen utan separat startskärm: exakt första spelstartflöde ska fastställas i tekniskt test och inte antas av denna text.
- Inget ändrat poängsystem, ingen ny AI-regel, inga ändrade kartor och ingen ROM-implementation godkänns här.

## Projektisolation

Uppdateringen hör bara till Odourman/let-me-out och den separata projektmappen i Google Drive. The Cabin och I Love a Fish ska inte ändras. Linear används inte för Let Me Out!.
