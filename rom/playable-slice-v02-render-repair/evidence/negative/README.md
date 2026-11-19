# Kasserade integrerade tester

- `key-overlap-344-lines.*` och `key-overlap-147-lines.*` visar två tidigare planeringsvarianter som missade RIOT-timerns väntfönster i provet med fem levande NPC och golvnyckel. Byggt med samma renderings- och positionsdata för fixturen. Slutprovet av samma koordinater finns i `../brief/key-crowd.jsonl`.
- `late-hmove/` innehåller en X64-kalibrering från spel-ROM:en. Flyttad HMOVE tar bort den mörka ytan men ger orange vänsterkant och 1/28 korrekta NPC-pixlar. ROM-kandidaten använder avsiktligt en fast fördröjning för det jämförda X-värdet.
- `door-stencil/` innehåller ett separat byggrundlag, ROM, rålogg och originalbilder. M1 ger två mörka högerpixlar, 267 scanlines och konflikt med den vita P1-masken. Den delade COLUP1-färgen och rasteröverskridandet gör tekniken olämplig för den här integrerade kärnan.
- Föregående matchs negativa ROM:ar och underlag finns kvar i den frysta fortsättningskatalogen.
