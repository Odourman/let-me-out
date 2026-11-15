# Beslut och spawngranskning v0.11 – Let Me Out!

**Beslut 2026-11-15:** Användaren svarade "Ok, följ din rekommendation. Fortsätt." på MAIN:s uttryckliga förslag att **C02 blir planerad version av rum C**, **C01 sparas för jämförelse**, och **A01/B01/D01 behålls oförändrade**. Det är ett accepterat **designval**, inte ett bevis på spelbarhet eller tillstånd att skriva 6502-kod.

## Planerat fyrarum-set
| Rum | Planerad karta | Kommentar |
|---|---|---|
| A | A01 | Oförändrad ursprunglig layoutkandidat |
| B | B01 | Oförändrad ursprunglig layoutkandidat |
| C | **C02** | Godkänd som planerad kartvariant, C01 arkiverad för jämförelse |
| D | D01 | Oförändrad ursprunglig layoutkandidat |

- [Exakt planerad fyrarumskarta i GitHub](../design/PLANERADE_RUMSKARTOR_V011.json) ([samma JSON i Drive](https://drive.google.com/file/d/1WrDNv2AqMuQ8sbHAFq8HsLTn7_fe7lc-/view?usp=drivesdk)). SHA-256 för den ursprungliga JSON-filen: `760d77bbb71bfdd0b3020d827ca7874abdcde4e399979289f75719572ee22d4a`.

De två öppningarna i C02 är exakt de åtta tidigare granskade väggcellerna x=8–9 och x=30–31, y=10–11 på 40×22-cellsgriden. Kartorna är inte uppmätt i Atari-pixelgeometri och renderingens tekniska lösning har inte godkänts.

## Spawn-granskning (offline)
Exakt **64 045** kombinationer av sex distinkta androidstarter prövades från originalkandidaternas pooler för den valda fyrarumssammansättningen. Det visar att positionerna ligger i en nåbar sammanhängande 2×2-fotankargeometri, inte överlappar varandra vid start och att varje position kan nås från spelarens start i ett 4-vägs rutnät. Det bevisar **inte** rättvis startposition i faktiskt spel.

| Rum | S0-pool | Sexval | Min avstånd i 4-vägs gridsteg till start | Sexval med någon android under 12 steg | S1-pool (förslag) |
|---|---:|---:|---:|---:|---:|
| A01 | 20 | 38 760 | 9 | 68,1% | 17 |
| B01 | 13 | 1 716 | 12 | 0,0% | 13 |
| C02 | 18 | 18 564 | 7 | 73,0% | 15 |
| D01 | 15 | 5 005 | 9 | 65,7% | 13 |

**S0:** Befintliga positionspooler, utan ny säkerhetsmarginal. **S1:** jämförande *icke-godkänt* filter som tar bort startpositioner med kortaste 4-vägs gångavstånd mindre än 12 abstrakta cellsteg från spelaren.

### MAIN:s rekommendation
Behåll S0 som arbetsbas. S1 får endast användas som **jämförande framtida speltestvariant**, om en verklig ROM senare visar att robotar nära spelarens start kan orsaka orimliga tidiga dödsfall. **Ingen** grace period, inga nya fienderegler och inget ändrat antal androider införs av denna studie.

## Källor
- [Drive-paket v0.11: valda 4 kartor, reproduktionsskript, alla spawnkandidater, CSV och manifest](https://drive.google.com/file/d/1WbnLfcSKM-bqmVIz5jCJ0ga0sUzPU0UK/view?usp=drivesdk)
- [Drive-paket v0.10: C01/C02-analys](https://drive.google.com/file/d/13JHPwn11DtoCcPQupKlPMengz0hQQShE/view?usp=drivesdk)
- [Äldre MAIN-beslut K1/E1](APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md).

## Auktoritetsgränser
- **Fastställt designval:** C02 som planerad karta C, oförändrade A01/B01/D01.
- **Inte beslutat:** slutligt pixelutförande av kartorna; AI P2/J2, S1, svårighetskurva C-1.
- **Inte genomfört:** ROM-kodning, emulator-/TIA-/scanlineverifiering, spelbarhetsmätningar.
- **Paus fortsatt aktiv:** starta inte ROM DEVELOPMENT utan ny uttrycklig instruktion.
- **Projektgräns:** endast Odourman/let-me-out. Linear används inte. The Cabin och I Love a Fish påverkas inte.
