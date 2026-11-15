# 01 – Avgränsat framtida uppdrag till ROM DEVELOPMENT

## Uppdragstyp
**En körbar teknisk diagnostik-ROM för Atari 2600, med källkod och spårbara rasterbevis.** Den ska avgöra om de mest belastande delarna i Let Me Out!:s bild kan hanteras med acceptabel synlighet och korrekt enkel högerdörr. Den är **inte** ett spel och får inte marknadsföras som fungerande fullversion.

**Börjar först efter separat uttryckligt godkännande av användaren.** Föreliggande dokument är framtaget i MAIN utan kodauktorisation.

## Framtida leveransens minimala omfång
1. **NTSC som diagnostisk förstaregion – FÖRSLAG.** Fastställ faktiskt videoläge och motivera valet när koduppdraget auktoriseras. PAL hör till senare separat prov och får inte antas löst.
2. **En diagnostik-binär** för den valda videostandarden, med full reproducerbar källa och buildinstruktioner. 16 KB F6 är ett tidigare *föreslaget*, inte fastställt ROM-format; implementatören får redovisa valt format, men ska inte byta format utan spårbar motivering och godkänd uppdragsram.
3. **Scen R1 – sex androider + spelare + aktivt skott** på samma vertikala rastersnitt, med alla fyra vita människoliknande silhuetter (två stora män, två stora kvinnor, en liten man, en liten kvinna) där det är möjligt utan att ändra testets objektantal.
4. **Scen R2 – fem androider + nyckel + spelare + skott** på samma höjd. Nyckelns guldform ska kunna skymmas av en android enligt godkänd O1, för att sedan återkomma **på samma koordinat**.
5. **Scen R3 – enbart högerdörren** med logiskt låst/öppet tillstånd i en vald, källspårbar karta från A01/B01/C02/D01. Vänsterkanten måste förbli ogenomtränglig visuellt och i den minsta positionskontroll som behövs för testet. Den orange porten ska provas som visuellt mål och den svarta nyckelhålsformen undersökas som explicit separat teknikdel.
6. **Scen R4 – rörelse-/överlagringsstress**, förbestämda reproducerbara positioner för figurer vid flera angränsande scanlines och scenövergångar; ingen AI krävs. Visa nyckelns återkomst när tillfällig skymning upphör.
7. **Tydlig scenidentifiering**, t.ex. i emulatorns debugger/logg eller styrt med en diagnosväxel. En tillfällig intern diagnosselektor är inte en startskärm i det planerade spelet. Dess interface måste dokumenteras, och får inte återanvändas som ny spelregel.

## Avsiktligt utanför uppdraget
- Ingen fullständig rumsprogression, slumpmässig nyckelbärare, faktisk spelbar nyckeljakt, poäng/bonus/extraliv/highscore, GAME OVER, ljudpalett eller permanent lagring.
- Ingen fullständig P2/J2-patrull-/jakt-AI, spawn-säkerhet S0/S1, svårighetskurva C-1, joystick-stillastående sikte eller fullständig projektil-/hitbox-fysik. Ett synligt testsymbolskott är tillräckligt, **men får inte felaktigt benämnas verifierad projektilmekanik**.
- Inga ändringar av antalet androider eller användarens godkända visuella riktning för att få testsiffrorna att se bättre ut.
- Ingen kopiering av Berzerks kommersiella ROM, disassembly eller andra tredjepartsbinärer till publik repository. Använd endast egna testkällor/godkända projektgrafikreferenser.
- Ingen ny repository, PR eller commit som ändrar The Cabin eller I Love a Fish; inget Linear.

## Föreslagen sekvens för den framtida implementatören
A. Skapa oberoende diagnostic scaffold och lås buildrecept.  
B. Visa R1 och R2, få reproducerbara timing- och flimmerrapporter.  
C. Visa R3 (högerdörr), först funktionell asymmetri, därefter orange och nyckelhål.  
D. Visa R4 (förutbestämd rörelse), samt återkörning av värstafall.  
E. Leverera alla spårbara bevis till MAIN **utan att själv utfärda slutgodkännande**.

## Spärr
Om ingen rimlig grafikteknik visar farliga enheter läsbart ska arbetet **redovisa blockeraren** och stanna inom diagnostikuppdraget. Förenkling som att minska antalet androider, ta bort den godkända dörrsymbolen permanent, ändra kollisionsregler eller acceptera ohanterligt flimmer kräver **nytt explicit användarbeslut**.
