# MAIN – fyra luftiga rum 40×22, studie v0.19

**Datum:** 2026-11-15. **Status: nya exakta kartkandidater; inte ersatta kanoniska kartor och inte byggd Stella-ROM.**

## Beslut och gränser

Användaren har godkänt principen om luftiga rum som **antyder mindre rum** med några korta väggformationer, breda öppningar och ingen egentlig labyrint. Användaren har sedan uttryckligen begärt att MAIN ska ta fram **fyra exakta 40×22-kartor** och offlinegranska spelare + sex androidstarter. Denna studie utför det uppdraget men fastställer inte de nya geometriska varianterna som slutgiltiga kartor utan ytterligare granskning.

- Nuvarande beslutade/källvalda baseline är **A01/B01/C02/D01 v0.11**, och **C02 var ett uttryckligt tidigare kartval**. Den gamla JSON-filen har **inte ersatts**.
- Nya förslag heter **A_OPEN_01, B_OPEN_01, C_OPEN_01, D_OPEN_01**. Dessa är fyra kandidater i parallellt designspår, inte ROM-kod.
- Alla fyra behåller 40×22-grid, stängd vänsterkant, högerdörr x39/y9–12, player start x2/y10, speglad innerväggsgeometri, brun vägg. Färg och nyckelhål i bilden är målillustration, inte TIA-prov.
- En gridcell i förstudien motsvarar **4 färgklockor vågrätt och 8 skärmlinjer lodrätt**. Totalt spelplanegridskarta 40×22; detta ger ingen garanti att sprites med 8×9-pixlar och riktig kollisionsrektangel kan navigera.
- Originalets sex androider och gemensamma logiska NPC-kollisionsyta ändras inte. Inga nya spawnregler beslutas.

## Resultat, offline

| Rum | Gammal väggandel | Ny väggandel | Fri 2×2-framkomlighet | Ursprungliga S0-kandidater fortfarande fria |
|---|---:|---:|---|---:|
| A_OPEN_01 | 8.42 % | 4.74 % | 623/623 nåbara | 18/20 |
| B_OPEN_01 | 20.53 % | 6.32 % | 619/619 nåbara | 9/13 |
| C_OPEN_01 | 16.32 % | 8.42 % | 579/579 nåbara | 16/18 |
| D_OPEN_01 | 22.11 % | 7.89 % | 591/591 nåbara | 15/15 |

**Alla fyra** klarar strikta rasterbaserade **kartstrukturkontroller**: 40 kolumner ×22 rader, innerväggarnas spegling, enbart högerdörr, stängd vänsterkant, sammanhängande graf för alla lagliga **2×2-fotankare** samt en möjlig väg till högerutgången från spelstart. För varje rum finns minst sex distinkta återanvändbara gamla S0-startpunkter med möjlighet att välja sex utan 2×2-överlappning.

**Detta bevisar inte** att sex jagande androider inte fastnar när de rör sig samtidigt, eller att den slutliga fysiska 8×9-formen/hitboxen glider bekvämt längs väggarna. Det kräver separat dynamisk offline-simulering med rörelser och senare faktiskt ROM-speltest.

### Varför dessa rum passar designbeslutet

- A: diskreta L-former i hörnen lämnar mittarenan helt fri.
- B: fyra dubbla väggstumpar ger lätta visuella skärmar, men inga smala korridorer.
- C: väggarna antyder nästan separata rum, men lämnar stora passager runt alla partier.
- D: korta väggarmar på båda sidor av centralarenan ger växling mellan skydd och fri sikt.

## Visuellt vs logiskt

- `FYRA_NYA_RUM.png` och `*_MAP.png` är **precisa offline-previews**, INTE Stella-bilder och INTE godkända nya pixelmasker.
- `*_ILLUSTRATIVE_STARTS.png` använder **schematiska cirklar** för spelare/androider enbart för att illustrera sex 2×2-fotankare. Figurens form och färgposition är inte den faktiska Atari-grafiken.
- De historiska S0-kandidaterna återanvänds som testpunkter där de är fria; deras sannolikhetsfördelning och urvalsregler är inte ändrade eller godkända för de nya kartorna.
- För riktigt spel krävs: beräknad sprite/hitbox-korridorbredd, dynamiskt test av sex blockerande NPC:er, diagonalslidning vid vägg, samt oberoende VERIFICATION av faktisk ROM.

## Nästa arbetsgrind

1. Visuell granskning av de fyra alternativa kartorna jämfört med den av användaren accepterade öppna room-känslan.
2. Kör dynamisk offline-simulering av sex 2×2-androidfotankare och rörlig spelare, samt kollision mot väggar/NPC:er. Högre spelbarhetskrav kan resultera i nya kandidatlayouter utan att ändra canon automatiskt.
3. MAIN får därefter lägga fram uttryckligt beslut om huruvida A01/B01/C02/D01 ska ersättas. **Det aktuella ROM DEVELOPMENT-uppdraget v0.18 R1–R4 utvidgas inte; PR #7 förblir draft.**

## Källor

- `design/PLANERADE_RUMSKARTOR_V011.json` (GitHub main, bevarad), och `docs/APPROVED_MAP_C02_AND_SPAWN_AUDIT_V011.md`.
- `design/NPC_REFERENCE_8x9_masks.json` (tidigare 8×9 visuella referenser), `docs/MAIN_PLAYER_SCALE_V018_2026-11-15.md`.
- `OPEN_ROOMS_V019_40x22.json`, `MAP_METRICS.csv`, `ROOMS_ASCII.txt` och `BYGG_OCH_TESTA.py` i detta paket.
- Projektisolering: endast `Odourman/let-me-out`; The Cabin/I Love a Fish orörda; Linear används inte.

## Andra kontrollen: förenklad dynamisk framkomlighet

100 deterministiska försök per karta × 180 logiska ticks med sex 2×2-androidobjekt och en spelare som försöker nå högerdörren. Alla objekt behandlas som fysiska hinder för just denna trafikstudie; spelets verkliga före-skott-överlappning, jakt/attack, hastighet och kollisionsregler simuleras INTE.

| Rum | Spelaren nådde dörr inom 180 ticks | Högsta NPC-stillestånd, ticks | Androidernas andel lyckade förflyttningsförsök |
|---|---:|---:|---:|
| A_OPEN_01 | 100/100 | 0 | 100.0 % |
| B_OPEN_01 | 100/100 | 2 | 100.0 % |
| C_OPEN_01 | 100/100 | 0 | 100.0 % |
| D_OPEN_01 | 100/100 | 2 | 100.0 % |

Resultaten visar endast denna specificerade rutnätsmodell. De visar varken garanterad fri framkomlighet i verkligt spel eller att sex samverkande robotar inte fastnar i andra situationer. Underlag i `SIX_MOVING_NPCS_OFFLINE.csv` och `DYNAMIC_SIMULATION_SUMMARY.json`.
