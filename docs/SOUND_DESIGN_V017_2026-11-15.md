# Let Me Out! – MAIN, ljuddesign steg 9 (v0.17)

**Datum:** 2026-11-15  
**Projekt:** Endast Atari 2600 – Let Me Out!  
**Status:** Designrekommendation, inte färdig ljudimplementation. Användarens förslag om siren, skott och androiddöd är godkänd inriktning för vidare detaljdesign; exakta parametrar, mixning och ljudprioriteringar är ännu inte användargodkända. Ingen ROM-utveckling auktoriserad.

## Utgångspunkt och beslutskällor

Master Spec §12 och ursprungligt beslutsregister ID 025/056 fastslår **ljud vid nyckelupptagning**. Andra ljudeffekter och musik var inte fullt beslutade. Första verkliga skottet aktiverar omedelbart jakt i det aktuella rummet (ID 029), och nyckeln uppstår efter dödsanimationen. Ett skott per nytt Fire-tryck, högst en aktiv projektil. GAME OVER: endast konsolens RESET startar nytt spel; Fire gör ingenting då. Ingen separat startskärm.

Användarens önskemål 2026-11-15: ”Jag tänker att det ska låta en ton som pitchas högre till ett tjut när androiderna blir aggressiva. Sedan ett ljud när androiderna förstörs. Kanske ljud när man skjuter också. Det kanske räcker?”

## Rekommenderad minimal ljudpalett: fyra ljud

| Händelse | Rekommenderad karaktär | Tidsförslag att provlyssna på (inte beslut) | Utlösande spelhändelse |
|---|---|---|---|
| A1 – Larm | Låg elektronisk ton som i tydliga frekvenssteg stiger till ett kort genomträngande tjut, därefter tystnad | cirka 0,4–0,7 s | **En gång per rum**, vid den första **faktiskt avfyrade** projektilen, oavsett om skottet träffar |
| A2 – Skott | Mycket kort, torrt elektroniskt laserknäpp, ingen lång efterklang | cirka 0,04–0,10 s | Vid varje **faktiskt genererat** skott, inte vid knapptryck om det redan finns en aktiv projektil; även första skottet |
| A3 – Android förstörd | Kort brusigt, elektriskt sammanbrott, gärna fallande tonhöjd; skilj tydligt från larm | cirka 0,12–0,25 s | Varje gång en android förstörs efter träff, utan att vänta på nyckeluppdykandet |
| A4 – Nyckel upphämtad | Mycket kort, ljus tvåtonssignal, renare än skott/robotkrasch | cirka 0,12–0,25 s | Vid faktisk nyckelupptagning och +50 **exakt en gång**. **Redan beslutat att ljud ska spelas.** |

**Ingen bakgrundsmusik**, inget upprepat larm under jakt, inga kontinuerliga androidljud. Ingen femte unik effekt för dörren eller Game Over behövs i första tekniska provet. Det är rekommendationer som kan revideras efter provlyssning.

## Ljudkonkurrens och prioritering – TESTFÖRSLAG

Atari 2600 TIA har **två självständiga ljudkanaler**, styrda via AUDC/AUDF/AUDV. Riktig spelkod får inte anta fler kanaler. På **första skottet** bör A1 (larm) kunna spelas på en kanal och A2 (skott) på den andra. En senare androiddöd A3 eller nyckelhämtning A4 ska inte bli ohörbar för att ett kort skott fortfarande klingar; kortare ljud får avslutas eller avbrytas efter tydlig, testad prioritetsregel.

**Arbetsprioritet att testa:** (i) ljud vid faktisk nyckelupptagning, (ii) tydlig första jaktsignal, (iii) androidens dödsljud, (iv) skottljud. Vid samtidig första avfyrning och androidträff måste första skottet fortfarande aktivera jakten *utan fördröjning* – ljudet får aldrig fördröja AI eller kollisioner. Prioritet mellan simultana ljud är inte en ny spelregel.

## Vad ett framtida auktoriserat ROM-test behöver bevisa

1. A1 triggas exakt en gång per rum av första giltiga skottet; inga extra larm för missar eller fler skott i samma rum.
2. A2 spelas inte när Fire trycks trots att projektilen fortfarande är aktiv. Larm och skott samexisterar utan att lämna ljudkanalen permanent på.
3. A3 triggas vid androidförstörelse; upprepade träffar och nära simultana händelser ger inte fastnat ljud.
4. A4 sker exakt en gång vid +50; inte vid nyckelns uppdykande eller skymning (O1).
5. Vid GAME OVER tystnar kvarvarande spelljud; Fire är inaktivt, RESET återställer ljudtillstånd så att nästa rum får sitt larm vid första skottet.
6. NTSC/PAL-upplevd tonhöjd, volymbalans och ljudets påverkan på raster-/cykelbudget mäts och lyssnas på.
7. VERIFICATION oberoende av ROM DEVELOPMENT; testerna här har **inte** körts i ROM eller Stella.

## Status och avgränsning

- **Beslutat sedan tidigare:** Nyckelljud; första skottets spelmekanik; en projektil åt gången; GAME OVER/RESET; ingen startskärm.
- **Användarinriktning:** Stigande varningstjut, androidförstörelseljud, möjligt skottljud.
- **MAIN rekommenderar:** fyra ljud totalt inklusive redan beslutade nyckelljudet. Exakta rytmer, registreringsvärden och ljudmix är fortfarande **förslag**.
- **Ingen 6502-kod, ROM eller Stella-verifiering görs i detta steg.** Ändra inte The Cabin eller I Love a Fish; Linear används inte för detta projekt.

## Tekniska referenser

- Stella Programmer's Guide, avsnitt 11 (två ljudkanaler och AUDC/AUDF/AUDV): https://www.atariage.com/2600/programming/2600_101/docs/stella.html
- Projektets originalbeslut: `02_MASTER_SPEC.md`, §12 och `03_DECISIONS.csv` ID 025/029/036/037/056 i den privata huvudöverlämningen: https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u
