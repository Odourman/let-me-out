# TO_MAIN_V02_YELLOW_BLINKING_KEY_TEST_ONLY

**VISUAL_PROMISING_TECH_UNRESOLVED.** Tre körbara jämförelser per dörrläge från `efe23bde3a1b6c6edbfc4fbf9f96c3f95dddd66a`. Kontroll-ROM:arna är byteidentiska med den frysta basen. Gul 8 PÅ / 4 AV och gul 6 PÅ / 6 AV är separata försök. Båda använder den oförändrade 14-pixlarsmasken och samma nyckelkoordinater.

## VISUAL RESULT

PÅ och AV upprepades utan förlängning över skiftet 11→0. Kontrollen använder `COLUP1=$1A` och de gula försöken använder `COLUP1=$1E`. Gopher mätte skrivningen från CL40 till CL49 på den riktade nyckelraden. Spelare och skott har fortfarande `COLUP0=$1E`, medan vita fiender har $0E. Matchningen gjordes med separata X/Y-masker för nyckel, spelare och projektil. Rå-PNG, RGB- och registerloggar finns per variant.

| Koordinater | Kontroll, 24 bilder | Gul 8/4, två perioder | Gul 6/6, två perioder |
|---|---:|---:|---:|
| PX24/PY151 | 0/14 i alla | PÅ 0/14 i 16, AV 0/14 i 8 | PÅ 0/14 i 12, AV 0/14 i 12 |
| PX60/PY151 | 0/14 i alla | PÅ 0/14 i 16, AV 0/14 i 8 | PÅ 0/14 i 12, AV 0/14 i 12 |
| PX60/PY159 | 14/14 i alla | PÅ 14/14 i 16, AV 0/14 i 8 | PÅ 14/14 i 12, AV 0/14 i 12 |
| PX60/PY159 med aktivt skott | 14/14 i alla | PÅ 14/14 i 16, AV 0/14 i 8 | PÅ 14/14 i 12, AV 0/14 i 12 |

Noll extra nyckelpixlar i dessa prov. Samma utfall i TOP och BOTTOM. På fungerande position ger båda mönstren fem blinkcykler per sekund vid 60 bilder/s. 8/4 ger 133 ms PÅ och 67 ms AV, 6/6 ger cirka 100 ms i vardera fasen. Klippen spelar upp upprepade, kompletta perioder i 60 bilder/s. Faktisk upplevd läsbarhet på CRT och LCD är **NOT_RUN**.

## TECHNICAL RESOURCE RESULT

I PX60/PY159, även med aktivt skott, gick SM från **16/20 vita pixlar på PÅ** till **20/20 på AV**. Kontrollen gav 16/20. SM förblev åtminstone delvis synlig i alla 24 bilder. Längsta sviten med ofullständig SM är därmed 8 respektive 6 bilder, jämfört med 24 i kontrollen. Skottets enda pixel stämde i alla faser. Vid PY151 var SM:s respektive 20/20 och 10/20 oförändrade. Det kvarstående P0/P1-felet på PÅ-bilderna är **FAIL**. Gemensam färgkod förändrar inte antalet TIA-spelarsprites.

Fasvalet görs i lediga cykler före planerarens WSYNC. TIM64T skrivs på fryst instruktionstid. Renderaren utesluter golvnyckeln ur planeringen i AV-fasen, återställer dess logiska tillstånd direkt efter planeringen och använder ingen ny RIOT-byte. FrameClock reduceras vid 12. Det bevarar pariteten som logikbanken använder. Logikbanken är byteidentisk per dörrläge. Den uppmätta rastervägen når c76 inklusive WSYNC och kollisionsspåret visar SP=$F7 (åtta stackbyte inom 128 RIOT-byte).

Två tidiga versioner kasserades. Fasval och återställning inuti planerarens tidsfönster överskred VBLANK med aktivt skott. En senare timerförskjutning bröt standardsekvensen vid skottövergången. Provkällor, ROM:ar och negativa loggar är arkiverade.

## GAMEPLAY REGRESSIONS

- **PASS** i båda dörrlägena för brun låst dörr med svarta negativa pixlar, **256/256** svarta pixlar i öppningen och **16/16/16** saknade inre PF-pixlar i respektive låst/öppen/golvnyckelfixtur.
- **PASS** för 600 sammanhängande standardbilder utan golvnyckel per blink-ROM. Alla matchar den frysta RGB-sekvensen på fysiska rasterkoordinater, vilket bevarar **595/600** kompletta femmaskersbilder och noll helt osynliga NPC. Samtliga bildrutor hade 262 scanlines. Gopher exporterade ibland ett kortare utsnitt (29–228 i stället för 29–242); analysen använder den loggade aperturen. Originalbilderna bevaras.
- **PASS** för riktade skottprov **10/10**, inklusive X12 på Y105 utan (12,106).
- **PASS** för joystickstyrt fall, upptagning och exit utan RAM-ingrepp. Alla fyra test-ROM:ar klarade två rundor med upptagning i både PÅ och AV och **210 poäng och tre liv**. Upptagningen testades på fas 5 för PÅ och fas 8 respektive 6 för AV. Nyckeln föll ur den verkliga dödssekvensen. I observationerna före upptagningen var samtliga avsedda PÅ-bilder 14/14 och AV-bilder 0/14. Kontrollens kalla nyckel gav 65/65.

Gopher2600 gav pixel-, raster- och spelbevis. Stock Stella 6.7.1 och 7.0 kördes med verklig tangentinput och sparade originalbilder. Fysisk Atari, mänsklig skärmpanel och oberoende verifiering är **NOT_RUN**.

**DEVELOPER_OBSERVED · TEST_ONLY_NO_CANON_CHANGE · G5_FORMAL_OPEN · INDEPENDENT_VERIFICATION=NOT_RUN**
