# MAIN II R1c – tredje NPC kan flyttas självständigt 3 TIA-färgklockor, 600/600 LOCAL PASS

**2026-11-16.** Isolerad rådgivande v0.18 NTSC standard-F6-forskning, inte full R1, inte fri X och inte oberoende VERIFICATION.

## Reproducerbart bevis
- [GitHub Actions #43786384041 – SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43786384041), testad commit `73b0589e5eb0f486e3c1779345f94dcf6ecc83d3`, branch `research/main-ii-r1c-third-x-toggle-20261116`.
- Artifact ID `14191045065`: `main-ii-r1c-third-x-toggle-600-frame-evidence`, inkluderar ROM/källkod, full X11-Stella råbilder frame 11–610, `frames_600.csv`, `summary.json`, hashmanifest.
- DASM standard F6 exakt **16384 byte** i fyra identiska 4096-byte bankar, SHA256 `266046eeddb61fe475597b43c8445ea214ecc8afc7c823952d4e3656fc8a0e22`.
- DASM 2.20.14.1, verklig Stella 6.7.1, 262 NTSC-rasterlinjer. De tre maskerna kontrolleras direkt mot `main/design/NPC_REFERENCE_8x9_masks.json`, blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`.

## Faktiskt Stella-utfall

| Test | Resultat |
|---|---:|
| 600 verkliga konsekutiva frame-ID 11–610 | **600/600** |
| 262 scanlines enligt Stella HUD | **600/600** |
| Stor man (72/72 originalbitar) | **600/600** |
| Stor kvinna (72/72 originalbitar) | **600/600** |
| Liten man (72/72 originalbitar inklusive tomma rader) | **600/600** |
| Gul P0 + gult M0 synliga | **600/600** |
| Oönskade vita pixlar utanför förväntade maskerna | **0** |
| Liten man vid rå Stella GUI-X 394 | **296 bilder** |
| Liten man vid rå Stella GUI-X 400 | **304 bilder** |
| Källmasker identiska med MAIN-referens | Ja |

Stora mannen ligger **hela tiden** vid GUI-X 166 och stora kvinnan vid GUI-X 280. Lilla mannen växlar mellan X394 och X400, en förflyttning med **6 råa GUI-pixlar = 3 TIA-färgklockor**, via två distinkta statiskt assemblerade rasterkärnor valda av bit 4 i `FRAMELO`. Det är ett genuint men **extremt begränsat individuellt X-bevis**, inte full rörelse.

Programmet ändrar **enbart** inladdningen av tredje P1-kopians delay: i det ena mode `LDX #1` (2 CPU-cykler), i det andra `LDX THIRD_DELAY` (3 CPU-cykler, där `THIRD_DELAY=$81` initierats till 1). De två första maskerna/RESP1-tidpunkterna hålls identiska. Typiskt tredje `RESP1` inträffar före instruktion c61 respektive c62. Rasterbudgetgränsen ligger mycket nära: efter tredje strobe och loopens slut ligger `STA WSYNC` beräknat vid c72 respektive c73 av 76.

## Relation till tidigare experiment och fortsatta blockerare
- Baslinjen `research/main-ii-r1c-three-600-20261116` har tre helt statiska korrekta maskpar 600/600; detta nya prov visar därutöver just en självständig mindre förflyttning.
- Den äldre 54-CC-varianten har ett verkligt 1-bitfel i stora kvinnans mask. 57 CC-kerneln behåller korrekt 72/72 i båda lägena.
- Inga fler än **tre** NPC samtidigt. Inga helt fria och godtyckliga X för dessa tre, ingen generell positionering över 160 color clocks, ingen rörelse i Y, inga PF-väggar/dörrar eller R2 nyckel/O1. Metoden ensam kan inte antas skala till projektets sex NPC.
- Ingen skärmsynk- eller maskdispens: alla sex fritt placerbara original-NPC krävs fortfarande för full v0.18 R1.
- Inga ändringar i `main`, ROM DEVELOPMENT PR #7 eller oberoende VERIFICATION Issue #8. Ingen merge/auktorisation för fullspel.

**MAIN II tekniskt:** 76-cykelbudget lämnar mycket litet spelrum. I just denna serieexpanderade P1-kernel kräver en fjärde fullständigt separat kopia ett nytt kodschema; bankbyte eller extra F6-ROM-plats skapar inte fler TIA-cykler eller färgregister. Prioritera alternativ arkitektur med oförändrade originalmasker och tillräckligt fri X innan vidare uppskalning.
