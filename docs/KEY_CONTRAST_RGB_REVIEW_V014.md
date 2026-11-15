# MAIN v0.14 – synlighetsjämförelse av den guldgula nyckeln

**Datum:** 2026-11-15. **Status:** rådgivande offline-studie, **inga** nya fastställda pixelmasker/färgkoder eller ROM-uppdrag.

## Auktoritativa designbegränsningar
- **Master Spec §3:** spelare gul med hatt/vapen, vita androider, bruna väggar. Mörk bakgrund är preliminär.
- **Godkänt visuellt mål v0.13:** guldgul nyckel med runt huvud, synligt hål och kort tandat skaft. Orange högra dörr med svart nyckelhål försvinner helt vid upplåsning.
- Exakt PAL-/NTSC-färgkod, spritebitmask, blinkning, grafisk renderingsmetod och flimmer har **inte** godkänts eller verifierats.

## Tre hypotetiska RGB-färgtest
För att endast jämföra **färgriktning**, och inte ge sken av en färdig Atari-skärm, används följande påhittade RGB-värden i samma schematiska A01-bild:
- **Illustrerad spelare:** `#FFE500`
- **Illustrerad svart bakgrund:** `#080A0D`
- **Illustrerad brun vägg:** `#744926`
- **Nästan spelargul nyckel:** `#FFDE00`
- **Djupguld (MAIN:s preliminära kandidat):** `#F2AD00`
- **Mörk bärnsten:** `#D98E00`

| Nyckelton | Luminanskontrast mot svart* | Mot spelargul* | Mot brun vägg* |
|---|---:|---:|---:|
| Nästan spelargul | 14,82:1 | 1,05:1 | 5,76:1 |
| **Djupguld** | **10,15:1** | **1,53:1** | **3,95:1** |
| Mörk bärnsten | 7,38:1 | 2,10:1 | 2,87:1 |

*Kvoter baserade på matematisk sRGB-relativ luminans. De mäter inte pixlig igenkännbarhet, TV-visning, färgblindhet eller CRT- och TIA-emission. Dessa hexvärden är **inte Atari 2600-färgkoder.***

## MAIN:s råd
Använd en något mörkare **djupguldton** än spelarens gula färg som nästa visuella *testkandidat*. Nyckeln ska kännas som de uppladdade referensbilderna men kunna identifieras på sin **form**, inte enbart på nyansen. **K11 (8×11)** har ett två rader högt öppet hål och används som läsbarhetsreferens. **K09 (8×9)** kvarstår som teknisk reserv om scanlinebudgeten kräver det. Varken nyansen eller masken är slutligt beslutad.

**Ingen blinkning föreslås** eftersom grundregeln är att nyckeln ligger statiskt tills spelaren hämtar den. En android får gå över nyckeln utan att flytta den, och grafisk överlappning får inte förlora nyckelns logiska position.

## Vad är verifierat?
- **9/9 matematiska RGB-jämförelser** har beräknats för tre nyckeltoner × tre mörka bakgrundsförslag. Resultaten finns i CSV och kan återkontrolleras med medföljande skript.
- **2/2 tidigare pixelmasker** har klarat enkla offline integritetskontroller.
- **0 ROM-byggen, 0 Stella-mätningar, 0 faktiska NTSC-/PAL-color tests**, ingen användarpanel eller riktig TIA-objektsbudget.

## Kommande verifieringsgrind (kräver separat ROM-auktorisation)
Visa vald nyckel tillsammans med gul spelare, minst fem levande vita androider, aktivt skott och brun vägg. Testa när android passerar över synlig tappad nyckel, dödsanimationens slut och nyckelhämtning. Mät faktisk flimmer-/scanlinebudget och kontrast i NTSC/PAL. Oberoende VERIFICATION efter särskilt godkänd ROM DEVELOPMENT.

## Länkar till leverans
- [Drive ZIP v0.14, 13 filer](https://drive.google.com/file/d/17I6nUhYTCSRIQ35fMvILE1pmVIIDh8SA/view?usp=drivesdk) – fullständiga rapporter, RGB-data, mask, skript, illustrativa PNG och manifest.
- [Drive PDF v0.14](https://drive.google.com/file/d/1E_ShhSLz3MLBVkHOcvVvUPfX-npKbEBq/view?usp=drivesdk) – 3 sidor mobilöversikt.
- [RGB-jämförelsen som PNG](https://drive.google.com/file/d/1tlL60lQXVtYF-sqkIaAnxhkbwcxrM3iG/view?usp=drivesdk).
- [Tidigare visuellt beslut v0.13](KEY_AND_DOOR_VISUAL_TARGET_V013.md) och [officiell kartdata A01/B01/C02/D01](../design/PLANERADE_RUMSKARTOR_V011.json).

**Isolering:** endast Let Me Out!; inga ändringar av The Cabin, I Love a Fish eller Linear. Ingen ROM-kodning får starta utan separat uttryckligt användarbeslut.
