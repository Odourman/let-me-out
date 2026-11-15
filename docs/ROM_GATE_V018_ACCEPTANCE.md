# 02 – Acceptanskriterier för framtida diagnostik-ROM

**Detta är TESTKRAV, inte godkända testresultat.** Ingen mätning finns ännu. Ansvar: ROM DEVELOPMENT producerar; oberoende VERIFICATION provar; MAIN samordnar; användaren godkänner eventuella visuella kompromisser.

## A. Artefakter, giltighet och reproducerbarhet – obligatoriskt
**A01** En körbar `.bin` av vald/auktoriserad konfiguration samt fullständig egen 6502/assemblerkälla, grafikdata och buildskript/kommandon. Ange assembler- och Stella-version, målstandard och bankformat.

**A02** En oberoende ren ombyggnad från levererade källor ska ge exakt **samma SHA-256** för ROM-filen som originalleveransen. Om tidsstämplar/verktyg ger variation måste orsaken och normalisering anges; annars FAIL.

**A03** Testscenerna R1–R4 måste gå att reproducera med dokumenterade inputs, initiala koordinater, bildrutor och emulatorinställningar. Scenidentitet syns i logg eller kan erhållas reproducerbart. Här krävs **inte** en ny startskärm i spelet.

**A04** Minst en ställningstagandelogg per test med `PASS`, `FAIL` eller `INCONCLUSIVE`; inga tomma slutsatser eller automatiskt PASS för ej körda test.

## B. Verklig raster- och tidskontroll – blockerande
**B01** Visa via Stella Debugger att NTSC-diagnostiken **faktiskt** producerar stabila bildrutor och rätt VSYNC/VBLANK/overscan. **Föreslagen testprofil:** 600 efter uppstart följande bildrutor per R1/R2/R4, med **262 scanlines** per bildruta för NTSC. Variationer ska loggas och förklaras, inte döljas. 262 är ett NTSC-mål i denna profil, inte ett påstående om uppnådd stabilitet.

**B02** På kritiska höjdlinjer redovisas `scanline`, CPU-cykelposition, relevanta TIA-registerskrivningar och körd scen; skärmuppdateringar ska ligga inom hårdvarans **76 CPU-cykler per scanline**. En rutin som råkar gå över bildgränser eller flyttar flera linjers bild felaktigt är FAIL, inte en optimeringsdetalj.

**B03** Dokumentera RAM-användning, bank-/ROM-storlek och objektallokering (P0/P1/M0/M1/BL/PF eller annan teknik). Bankbyte förbättrar inte TIA-objektantal, 76 cykler eller standard-128 B RIOT-RAM.

## C. Obligatorisk bildbelastning – blockerande
**C01** R1 innehåller **exakt sex** androider, en spelare och ett aktivt testsymbolskott med överlappande **rasterhöjd**. De får inte ersättas av färre figurer eller turas om i en specifik scen utan att detta öppet redovisas som kompromiss. Fyra androidsilhuetter måste kunna identifieras i använd testgrafik.

**C02** R2 innehåller **exakt fem** kvarvarande androider, en synlig nyckel, spelaren och ett skott, även på samma rasterhöjd. När android skymmer nyckel enligt O1 får nyckeln vara tillfälligt osynlig men den **logiska positionen** måste vara oförändrad; efter skymning måste den återkomma på samma koordinater.

**C03** En mindre mängd kortvarigt flimmer är accepterat kvalitativt, men testet är inte godkänt om kritiska objekt regelmässigt blir omöjliga att särskilja, spelaren och skottet försvinner så att kontroll förloras, eller vita farliga androider blir obegripliga. **Ingen numerisk maximal flimmerandel är användarbeslutad**: därför krävs separat manuell visuell bedömning med videobevis och explicita noterade kompromisser.

**C04** Testa minst två separata situationer: (i) sex figurer på exakt gemensamt höjdband, (ii) samma antal men skiftade inom intilliggande scanlines och olika 8x9-masker. Att endast prova en luftig normalfördelning är otillräckligt.

## D. Endast högerdörr och nyckelhål – blockerande + separat designrisk
**D01** Alla fyra kända kartor har logiskt dörrläget `x=39, y=9–12` i 40×22-prototypmodellen och stängd vänsterkant. Minst en av kartorna måste i ROM visa verkligt **låst högerkant / upplåst högeröppning** medan vänster förblir visuellt stängd. Rapportera hur de övriga kartornas data skulle kunna användas; **full fyra-rums-RAM/ROM-cykel ingår inte**.

**D02** Efter upplåsning ska den låsta portens synliga markering försvinna helt och ett tydligt hål finnas till höger; ingen vänsteröppning får uppstå genom speglad PF. En diagnosflagga får simulera upplåsning utan att full nyckelupptagningslogik implementeras.

**D03** Prova orange dörrstreck och svart nyckelhål **som separata verifieringsmål**. Om ett svart hål inte kan visas inom samma TIA-budget som C01/C02, märk D03 **FAIL / BLOCKED** och redovisa tekniska orsaker och möjliga alternativ. **Byt inte tyst designmål**. En brun reserv får användas i ett baslinjetest men ger inte i sig full designacceptans.

## E. Leverans, bedömning och stopp
**E01** Leverera emulatorvideo/screenshot från R1–R4 med information om scen, bildrutnummer, emulatorversion och oförändrad video/skärmbild; minst en synlig exempelbild från R1, R2 och låst/öppen R3. Inkludera CPU-/scanlineloggar och SHA-256-manifest.

**E02** En **annan** VERIFICATION-mottagare gör oberoende rebuild, kör R1–R4 och signerar separat bedömningsfil. ROM DEVELOPMENT:s egna markeringar är endast förtest, inte slutacceptans.

**E03** Slutresultatet blir `PASS`, `PASS_WITH_EXPLICIT_DESIGN_WAIVER`, `FAIL` eller `INCONCLUSIVE`. En designwaiver kan bara ges av användaren efter redovisat problem; MAIN får inte anta den från enbart flimmertoleransen. Om blockerande C01/C02 eller D01/D02 fallerar är diagnosen **inte godkänd**.

**E04** Tekniskt PASS betyder enbart att raster-/dörrdiagnosen fungerar i kontrollerad miljö. Det betyder **inte** att hela spelet, dess AI, poäng, ljud, GAME OVER eller spelbalans är klart eller godkänt.
