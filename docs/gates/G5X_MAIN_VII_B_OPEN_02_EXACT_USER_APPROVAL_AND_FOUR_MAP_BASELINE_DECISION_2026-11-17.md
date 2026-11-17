# LET ME OUT! – MAIN VII G5X: B_OPEN_02 godkänd och framtida fyrkartuppsättning komplett
**Datum:** 2026-11-17. **Beslutsstatus:** `G5X_LM_D19_B02_APPROVED_EXACT_FUTURE_MAP`; `FOUR_FUTURE_EXACT_MAP_LAYOUTS_SELECTED`. **Detta är ett användarbeslut om framtida exakt kartgeometri, INTE implementerad ROM, G5-PASS, G0/G6/F12-auktorisation eller oberoende Verification.**

## 1. Direkta användarbeslutet och exakt räckvidd
MAIN VII redovisade G5V/GRAPHICS II:s faktiska och av MAIN återkörda B02-leverans, visade trippeljämförelse och ställde uttryckligen frågan:

> "Godkänner du B_OPEN_02 som exakt framtida rum B?"

MAIN hade samtidigt klargjort att detta färdigställer fyrkartornas designval men inte Atari 2600-tekniken, G5 eller G6.

**Användaren svarade omedelbart:**

> "Är bra ut. Följ dina rekommendationer"

**LM-D19: användaren har därmed godkänt `B_OPEN_02` som exakt framtida 40×22-karta för rum B**, i den specifika frysta källversion som MAIN just presenterade. Detta är ett tydligt ja till kartvalet i föregående fråga, **inte** ett generellt godkännande att ändra programmering, börja nästa ROM-steg eller smyga in nya tekniska kompromisser. Tidigare G5W-text om att B väntar på beslut är historisk tidssnapshot, nu supersederad **endast för B-layoutens designstatus**.

## 2. Fullständig framtida exakt fyrkartsbas
Genom sedan tidigare **LM-D17** (A/C/D) och nya **LM-D19** (B) är samtliga fyra framtida exakta kartlayoutmål nu valda:

| Rum | Exakt 40×22-karta | Beslut | Inre väggceller / 760 | FNV-1a 32-bit av 22 gridrader med LF |
|---|---|---|---:|---|
| A | `A_OPEN_01` | LM-D17 | 36 | `f8529fc5` |
| B | `B_OPEN_02` | **LM-D19** | 72 | `c9e29f45` |
| C | `C_OPEN_01` | LM-D17 | 64 | `84612e29` |
| D | `D_OPEN_01` | LM-D17 | 60 | `16317f3d` |

**A/C/D ursprungliga fasta källblobb:** `0e449f97f87bd9b403476fd1435398042eaee285`, källfil `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json`, pin `80bf072ee0e8a9a84905a29d70771a7cc6be7820`.

**B ursprungliga fasta G5V-källblobb:** `c32fc656fb5c60d16a5b73e4cea75f86df3e9621`, källfil `studies/graphics/G5V_B_OPEN_02_2026-11-17/B_OPEN_02.json` i isolerad graphicscommit `2991a94a4d92a0ee75a5de8e8c5302d549734e1e`.

**Maskinläsbart, versionerat urvalsmanifest på main:** [`G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json`](./G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json). Exakt källväg, commit, blob, ID, längd, väggantal och 32-bit hjälpfingerprint per rum. Skapat direkt från båda **live återlästa** originalfilerna och deras frysta referenser. Inga raster-, pixel- eller kollisionstester följer av 40×22-datat.

**Viktigt om källornas historiska statusmarkeringar:** Den gamla v0.19-filen och B02-studiens JSON innehåller metadata såsom `NOT APPROVED` från *när filerna skapades*, före dessa två senare användarbeslut. Dessa fält ska **inte skrivas om retroaktivt**. De senare specifika användarbesluten LM-D17/LM-D19 och detta låsta urvalsmanifest anger den aktuella auktoriteten **för de fyra exakta framtida designlayouterna**, utan att påstå att forskningskällornas ursprungliga status var fel eller att ROM-canon har ändrats.

## 3. G5V/G5W-leveransens tekniska bevisnivå
[MAIN G5W mottagning och självständig G5V-offline-reproduktion](G5W_MAIN_VII_G5V_B_OPEN_02_GRAPHICS_DELIVERY_RECEIPT_AND_MAP_DECISION_2026-11-17.md) bekräftar 18-fils-ZIP med 17/17 manifestkontroller och **12/12 byteidentiskt återgenererade grafikutdata**. MAIN:s separat räknade B02-geometri: **72 innerväggsceller, 90,53 % fri interiör, 565/565 2×2-ankare sammanhängande och 13 historiska B01-kandidatankare 2×2-gångbara**. Dörrkartan `x=39, y=9..12` och den fria mitten bibehållna.

Detta styrker **att kartan kan beskrivas och visas reproducerbart**, INTE att fem verkliga 8×9-fiender kan spawna, jaga och passera, att gold key går att rendera jämsides player+white NPC+P1-door+M0+PF, att TIA/PF-kernel ryms inom 76 cykler eller att spelaren kan klara ett verkligt rum.

## 4. Frysta original och återstående grindar
- Historiska `design/PLANERADE_RUMSKARTOR_V011.json` A01/B01/C02/D01 och v0.18 ROM-/R1/R2-referenser förblir oförändrade, inklusive tidigare FAIL. Den **framtida designuppsättningen** är nu fullständig, men ingen oförklarad implementation/cutover i befintliga programmeringskällor har skett. Ingen branch har mergats.
- LM-D12/A1 fri logisk NPC X/Y, LM-D13/B1 läsbara hot, LM-D14/C1 framtida R1 fem/R2 fyra+key, LM-D15/D1 −30 per kill och LM-D16/E1 fem förhandsvaliderade NPC-spawns med 1/5 key-bärare gäller oförändrat inom sina tidigare specifika framtida scopes.
- För att kallas **tekniskt möjlig** återstår fem NPC 8×9-kollision/start-/AI-förflyttning, realisering av 40×22 vägg-/door-layout i TIA/PF och **S05** key+white NPC+yellow player+P1 orange door+M0+PF på samma raster-Y, plus fysisk färg/scanline/cykelbudget.
- **G5_FORMAL=OPEN** även efter designkartbeslut. **G0/G6/F12/ROM_DEVELOPMENT/ny VERIFICATION/PR-merge=NOT_AUTHORIZED**. Vid senare ny teknisk arbetsorder måste exakt scope bestämmas, inklusive tidigare oförenliga G4 H4-ONE och G5P:s snävare G0-idé, innan någon kod börjar skrivas.

## 5. MAIN:s säkra nästa steg
Nu finns ett **sammanhängande beslut om framtida kartgeometri** för rum A–D. MAIN ska använda detta källpinnade manifest för att förbereda en **explicit G5-teknisk beslutsgrind och falsifierbar testordning**, utan att själva åtgärden beställer kod, ändrar spelregler, utfärdar waiver, öppnar G6 eller ersätter VERIFICATION II. Separat uttrycklig användarauktorisation krävs innan ny ROM/probe/implementation.
