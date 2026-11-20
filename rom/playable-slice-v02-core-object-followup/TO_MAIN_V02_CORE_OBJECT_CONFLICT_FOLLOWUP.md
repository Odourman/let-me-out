# TO_MAIN_V02_CORE_OBJECT_CONFLICT_FOLLOWUP

**Spelbara TOP/BOTTOM-ROM:ar med reparerad enpixelprojektil. BOUNDED_SHOT_PROGRESS / OBJECT_CONFLICT_FAIL.** Fryst bas `1da716dc62edee73c1e40049c0b9223986d1b496`. [Gällande arbetsorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7039566370)

| ROM, 16 384 byte F6/NTSC | SHA-256 |
|---|---|
| `let-me-out-v02-brown-door-top.bin` | `72293ecdb770286f1f3109b88e96f342a0a5caeab43fade8adff0ce0c905bce6` |
| `let-me-out-v02-brown-door-bottom.bin` | `adab6abd29496d7e7b87e2bfe4dc3dc5922c396a705a65ff3a8a8d3b81b27fa1` |

## Integrerad reparation

Ordinarie spriterader kommer in med A=0 från tomma RoomFlags. Den nya vägen använder det värdet för att nollställa ENAM0 före vänsterkanten, och aktiverar missilen enbart på vald rad. Den tar bort den tidigare sena nollskrivningen. Två cyklers väntan bevarar den gamla GRP1-tiden på rader utan skott. Det tidigare kasserade försöket lade en tidig skrivning ovanpå den gamla vägen och försköt GRP1. Den här versionen håller M (1) kvar på 23/28 i skott- och nyckelfixturen.

- **10/10** riktade M0-lägen i båda ROM:arna, upp från 9/10. Vid X12 mättes endast (12,105). Den extra pixeln (12,106) är borta. Gopher stod före nollskrivningen på SL135 CL−47, alltså c7, med A=0 i båda ROM:arna.
- **595/600** standardbilder med fem kompletta masker och noll extra vita pixlar i båda. Noll fullständigt utelämnade NPC. M (1) har kvar fem partiella bilder. De åtta crowd-fixturerna per variant gav samma NPC- och färgpixelmått som respektive fryst brun start. Parets RGB-jämförelse mot respektive fryst brun variant gav inga ändrade vita, gula eller gemensamma bruna koordinater i standardprofilens jämförda inre bildområde.
- **Dörr PASS.** Kantens bruna/svarta låsorakel har noll avvikelser. Öppen TOP/BOTTOM ger 256/256 svarta aperturpixlar, noll orange pixlar och rätt omgivande vägg. Lås, två konturlägen, gammal högerkant, fel X, motsatt kant och fysisk utgång testades. Båda kalla joystickrundorna utan RAM-POKE gav 210 poäng och tre liv.
- **Nyckelregression PASS.** Båda har 65/65 exakta bilder under golvtiden från kallstart och 14/14 med aktivt skott. Samma rasterband med spelaren är fortsatt 0/14 på skilda och överlappande X. Övriga inre väggfel ligger kvar vid 20/20/16 i låst/öppet/kallnyckel-oraklen.

## Kasserade fysiska metoder

- **BOLL för nyckeln.** Förpositionerad BOLL testades som oberoende källa med växlad COLUPF och vit P1 kvar åt SM. På separerad X gav den 8/14 korrekta guldpixlar och 12 extra vid 262 scanlines. Spelaren var pixelrätt i detta prov och SM klarade 20/20. En ensam sammanhängande missilkropp/BOLL återger inte originalets delade rader. Försöket är negativt för denna bredd- och färgplan. Guldbrunt färgbyte loggades före skrivning vid CL79 respektive CL106 på SL198. Det flyttade varken spelarens eller nyckelns logiska position.
- **Två P1-omstarter per scanline.** Förladdade F- och SM-byte provades med GRP1-omskrivning och två RESP1-händelser på det riktiga fem-samma-Y-fallet. I den uppmätta omstartsraden loggades reset före skrivning vid CL52 respektive CL76, åtta CPU-cykler isär. Provet höll 262 scanlines men gav F 4/38 och SM 0/20. SF behöll 22/22. Provet visar hur det direkta resetfönstret tar bort tidigare pixlar, med en annan metod än tidigare VDEL/NUSIZ-prov. Ingen generell hårdvaruomöjlighet har fastställts. Spel-ROM:arna behåller fryst utfall 2/5 i detta hårdprov.

## Hårdvarumätning

Båda binärerna har 16 384 byte och byteidentiska logikbanker mot respektive fryst brun start. Gopher2600 v0.57.2 gav exakt 262 scanlines i vardera 600 sammanhängande bilder. Kantens mätta väg håller c64/c65 inklusive WSYNC. Sen väggväg når c76 inklusive WSYNC. Kollisionens stackmätning gav SP=$F7, åtta stackbyte inom 128 RIOT-byte. Stock Stella 6.7.1 (topp) och 7.0 (botten) kördes med verklig tangentinput. Fysisk Atari är NOT_RUN.

[Byggkommandon](README.md) · [Läsbara mätprotokoll](evidence/brief) · [Originalbilder och råprotokoll](evidence) · [Negativa ROM-prov](evidence/negative)

**DEVELOPER_OBSERVED · G5_FORMAL_OPEN · INDEPENDENT_VERIFICATION=NOT_RUN**
