# Let Me Out! — MAIN: beslut O1, senaste tio steg, nuläge och kommande tio steg

**Datum:** 2026-11-15  
**Projekt:** Atari 2600 — Let Me Out!  
**Status:** Design/analys, **ingen ROM-utveckling auktoriserad**.

## Nytt användarbeslut

Användaren skrev: **"Lite flimmer i spelet är ok. Men följ din rekommendation"**, direkt efter MAIN:s rekommendation om nyckelöverlappning v0.15.

**[BESLUT O1]** En levande android får visuellt skymma nyckeln tillfälligt. Nyckelns logiska position, ägare och upptagningsbarhet ändras inte av överlappningen; den visas på samma plats igen när skymningen upphör. Nyckeln får inte avsiktligt blinkas bara för att ersätta O1. Androiden får fortfarande inte bära med sig nyckeln eller ta upp den. Regeln K1 för nyckeln som uppstår under spelaren förblir oförändrad.

**[ACCEPTERAD KVALITETSPREFERENS]** Ett *mindre, tillfälligt flimmer i spelet* är acceptabelt. Användaren har **inte** angett en kvantitativ flimmergräns eller godkänt att spelaren, farliga androider, skott, nyckel eller dörr blir långvarigt oläsbara. Inga automatiska bildrutebyten, försämrade kollisionsregler eller ändrade hastigheter följer av detta. Bedömningen måste senare göras på verklig Atari-ROM och i oberoende VERIFICATION.

Detta svar ger **inte** tillstånd att börja programmera, skapa ROM-binär eller göra Stella-verifiering.

## Senaste tio avslutade studiestegen

| Version | Arbetat med | Aktuell beslutsstatus |
|---|---|---|
| **v0.6** | Hastighetskurva C-1: varierande 12-rumscykel; svårighet efter lyckad rumsutgång föreslagen | **PRELIMINÄRT**; inga hastigheter kalibrerade |
| **v0.7** | Före-skott-patrull; P2 med sällsynta svängar ger bättre täckning än ren pendling i offline-simulering | **P2-kandidat**, 1/8 ej slutligt värde |
| **v0.8** | Sammanhållen patrull-/jaktmodell P2/J2, händelseprioritet och 160 sexandroidprov | **J2-kandidat**, ingen ROM |
| **v0.9** | Nyckelns uppdykande under spelaren (K1) och dödlig kontakt vid samtidig utgång (E1) | **K1 och E1 GODKÄNDA** |
| **v0.10** | Geometrisk jämförelse C01/C02; kortaste abstrakta 2×2-väg 41 → 35 steg | **C02 rekommenderad** i förstudie |
| **v0.11** | C02 accepterad som planerad karta; A01/B01/D01 oförändrade; 64 045 spawn-kombinationer kontrollerade | **A01/B01/C02/D01 planerade**, S0-bas och S1-testkandidat |
| **v0.12** | Högerdörrens visuella och logiska läge; samtliga fyra kartor; 16 offline-logiktester | **Dörrens funktion beslutad**, orange färg ännu studie |
| **v0.13** | Användarens bildreferenser: guldgul nyckel med runt hål och tandat skaft, orange dörr med svart nyckelhål | **Visuella mål GODKÄNDA**, inga slutmasker |
| **v0.14** | Matematisk RGB-kontraststudie för nyckel/ljusgul spelare/bruna väggar | **Djupguld testkandidat**, inte Atari-färgkod |
| **v0.15** | Nyckel skymd av android och återkomst utan att flytta den; 20 offline-händelsetester | **O1 GODKÄND via senaste användarsvar**; TIA-visning ej verifierad |

## Aktuell status

### [BESLUT]
- Sex vita människoliknande androider, två stora män/två stora kvinnor/en liten man/en liten kvinna, samma logiska rörelse- och träffregler.
- Gul mänsklig spelare, fyra symmetriska bruna labyrinter med enbart högerutgång. Planerade kartor **A01/B01/C02/D01**.
- En slumpad android bär nyckeln. Nyckeln dyker upp efter dödsanimationen, ligger stilla och kan tillfälligt döljas av passerande android (**O1**).
- Första verkligt avfyrade skottet utlöser omedelbar dödlig förföljelse från alla överlevande androider. Ingen tidsgräns. Ingen grace period. Androiden skjuter aldrig.
- En ny avfyrning per knapptryckning, max ett aktivt spelarskott; åtta siktriktningar. Skott prioriteras mot samtidigt träffad android.
- Poäng −25 per förstörd android (golv 0), +50 nyckel, +100 faktisk utgång, +15 per överlevande android vid utgång. Tre liv, extraliv vid 500/1500/2500 osv.
- Låst dörr synlig som smal orange port med svart nyckelhål; nyckeln guldgul. Vid upplåsning försvinner både port och symbol; faktisk utgång är separat. K1/E1 kvarstår.
- **Mindre flimmer får förekomma**, men någon exakt tolerans är inte definierad.

### [FORTFARANDE PRELIMINÄRT]
- AI P2 och J2 inklusive 1/8 svängchans, omvägslängd och turordning.
- Svårighetskurva C-1, hastighetsprocent och vad död gör med hastighetsnivån.
- S0 kontra S1 för startavstånd; detaljkalibrering av 2×2-rutmått mot riktig pixelgeometri.
- Exakta bitmapmasker K11/K09, djupguld/NTSC/PAL-värden, nyckelhålets teckning och eventuell TIA-kernelmetod.
- Exakt nivå av acceptabelt flimmer och upplevd rättvisa på faktisk spelkonsol.

### [INTE IMPLEMENTERAT / EJ VERIFIERAT]
- Ingen godkänd 6502-kodning, ingen byggd ROM, ingen Stella-/TIA-cykel- eller scanlineverifiering för detta projekt.
- Huvudrisk: sex androider + spelare + skott, alternativt fem androider + spelare + nyckel + skott, kan hamna på samma rasterhöjd.
- GitHub och Drive är underlag och arbetsarkiv, **inte** automatiskt synkade appar. Linear används inte i Let Me Out!.

## Föreslagen prioriterad plan – kommande tio arbetsmoment

Det här är **planering, inte genomförda uppgifter eller genomförandeauktorisation**.

1. **Långvarig skymning:** Specificera hur en android som står kvar på nyckeln ska hanteras visuellt utan att ändra O1; definiera fall att granska i senare speltest.
2. **Rastervärstafall:** Sammanställ bilder och explicita acceptanskriterier för 6 androider + spelare + skott samt 5 androider + spelare + nyckel + skott på samma höjd; skilj flimmer från försvunna spelobjekt.
3. **Högerdörren:** Välj rådgivande teknikordning för synlig orange kant, svart nyckelhål och rättvis öppning endast åt höger – med tydligt V1-reservfall.
4. **Nyckelgrafik:** Avgränsa K11 vs K09 och jämför kontrast på simulerade mörka/bruna/gula skärmar; fastställ inte NTSC/PAL-färgkoder utan riktigt test.
5. **AI-kontrakt:** Förfina P2/J2 med få och tydliga alternativ för sväng, omväg och turordning; prioritera att sex androider inte blir permanent blockerade.
6. **Startlägen och balans:** Definiera senare jämförelse S0/S1 och kritiska situationer vid första skottet när spelaren måste stå stilla och sikta.
7. **Svårighetskurvan:** Förbered val av C-1 eller enklare alternativ och frågan om död ska behålla samma svårighetssteg.
8. **Poäng/HUD:** Specificera poäng, liv, extraliv och highscore-visning i gränssnittet utan att ändra godkänt poängsystem.
9. **Presentation/ljud:** Avgränsa start, game over, skott, androiddöd, nyckelupptagning och öppnad dörr. Behåll tekniska krav små.
10. **Samlad implementationstestgrind:** Frys bara godkända designbeslut i en masterlista; förbered ett tydligt framtida ROM-testuppdrag med oberoende Stella-verifiering. **Vänta sedan på separat uttryckligt kodgodkännande.**

## Källor och förvaltning
- Ursprungliga `02_MASTER_SPEC.md`, `03_DECISIONS.csv`, `06_OPEN_QUESTIONS.md` i [Master handoff](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view?usp=drivesdk).
- Läs mer i GitHub: `docs/CURRENT_PROJECT_STATE_2026-11-15.md`, `docs/KEY_OCCLUSION_LOGIC_V015.md`, `docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md`, `design/PLANERADE_RUMSKARTOR_V011.json`.
- Arkiv v0.6–v0.15 ligger i [Let Me Out!-mappen i Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u).

**Projektgräns:** denna rapport och alla nya uppdateringar gäller endast Let Me Out!. **The Cabin, I Love a Fish och deras resurser får inte ändras.**
