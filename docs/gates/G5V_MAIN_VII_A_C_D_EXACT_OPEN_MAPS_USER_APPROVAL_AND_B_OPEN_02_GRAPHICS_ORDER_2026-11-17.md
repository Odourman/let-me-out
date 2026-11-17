# LET ME OUT! – MAIN VII G5V: användarbeslut om tre exakta OPEN-kartor, B_OPEN_02 beställd
**Datum:** 2026-11-17. **Status:** `G5V_ACD_FUTURE_EXACT_MAP_TARGETS_APPROVED_B02_GRAPHICS_STUDY_AUTHORIZED`. **Scope:** senare explicit användarbeslut, inte en implementerad karta/ROM, G5-PASS eller G6/F12-ordning.

## 1. Exakt samtalsreferens och beslut
MAIN VII granskade fullbordad och offline-reproducerad G5T-kartvisualisering (G5U). Direkt före användarens svar ställde MAIN VII den **sammansatta uttryckliga frågan**:

> "Godkänner du A_OPEN_01, C_OPEN_01 och D_OPEN_01 som framtida exakta kartbaser, och att GRAPHICS II får ett separat, begränsat uppdrag att förbättra B till B_OPEN_02?"

Användaren svarade omedelbart:

> "Ser bra ut"

**Rimlig strikt tolkning i det specifika sammanhanget:** användaren bekräftar **båda** angivna delarna, **endast** som avgränsad framtida kartdesign och en avgränsad grafikarbetsorder. Det är inte ett bredare "fortsätt" som ändrar andra kartor, öppnar G6 eller godkänner någon teknisk lösning. Källorna nedan bestämmer exakt vilken matris som avsågs. Alla äldre formuleringar om att även A/C/D-kartorna ännu väntar på användarval är historiska tidssnapshots och supersederade endast för dessa tre ID:n.

## 2. LM-D17 – exakta A_OPEN_01, C_OPEN_01, D_OPEN_01 godkända för framtida kartbas
- **A_OPEN_01**, **C_OPEN_01**, **D_OPEN_01** enligt oförändrad source-JSON `design/OPEN_ROOMS_V019_40x22_CANDIDATES.json`, ursprunglig källblob **`0e449f97f87bd9b403476fd1435398042eaee285`** på det granskade källcommittet `57a4f4954f5699b3d20893d12893f901fe767f7a`, är **godkända exakta 40×22-layoutmål för framtida separat auktoriserad test-/spelversion**.
- Godkännandet omfattar **matrisernas exakta rumgeometri**, inte att v0.19-filen i sin helhet nu blir en officiell fyrkartsversion. **B_OPEN_01 är inte godkänd** och någon fjärde ersättningsmatris saknas ännu.
- De tidigare exakta historiska v0.11-layouts **A01/B01/C02/D01**, deras frysta testunderlag och Git-blob `820a74e5fb77c818ffb1286c5b23698d4374e771` bevaras intakta. Ändra inte tidigare ROM-resultat, renderings-PASS, referenshashar eller äldre dokument som historik.
- **Ingen redigering av original-JSON-filen krävs eller görs av detta beslut.** Dess gamla statusfält `NOT approved` var korrekt för tidpunkten då kandidatfilen skapades men supersederas **för A/C/D i denna senare beslutsakt**. Framtida versionsmanifest/kartkompilering ska hänvisa till denna separat godkända delmängd, utan att tyst ändra källornas proveniens.
- LM-D12/13 fri logisk fem-NPC X/Y och rättvis fiende-/key-synlighet, LM-D14 5-NPC framtida R1/R2, LM-D15 -30/kill och LM-D16 fem validerade spawn/1/5 key-bärare gäller fortsättningsvis. **Detta bevisar INTE** fem fungerande 8×9 spawns, kollision, AI, TIA/PF eller S05/NPC+key+door.

## 3. LM-D18 – separat G5V GRAPHICS II studie B_OPEN_02 är uttryckligen beställd
Användaren har separat godkänt att MAIN VII utfärdar en **begränsad GRAPHICS II-designstudie** för att förbättra den alltför tomma B_OPEN_01, inte att en ny B-karta redan finns eller är godkänd.

[GitHub Issue #11 – G5V GRAPHICS II B_OPEN_02, source-only](https://github.com/Odourman/let-me-out/issues/11).

**Instruktionens föremål:** en tydligt definierad reproducerbar **ny 40×22 B_OPEN_02-kandidat** med luftig men mindre monoton väggstruktur och bibehållen stängd vänsterkant, högerdörr `x=39, y=9..12`, svart bakgrund och bruna väggar. Jämför B01/B_OPEN_01/B_OPEN_02 samt validera endast offline-rastercell-/geometri-/grova 2×2-nåbarhetsantaganden. **Ingen automatisk B-kartcanon** eller tekniskt femspawn-PASS. Original A/C/D och båda kartkällorna lämnas orörda; leverera endast inom grafikstudiescope och överlämna till MAIN för separat framtida B-beslut.

Skapandet av detta GitHub issue **startar inte automatiskt den andra GRAPHICS II-chattens körning**. MAIN kan lämna issue till specialistchatten; får inte påstå att GRAPHICS II gjort studien innan en verklig leverans finns.

## 4. Exakt gällande beslutsläge
| Objekt | Giltig status efter detta svar |
|---|---|
| G5Q A1/B1, LM-D12/D13 | GODKÄNDA FRAMTIDA DESIGNMÅL |
| G5S C1/D1/E1, LM-D14/D15/D16 | GODKÄNDA FRAMTIDA TEST-/POÄNG-/SPAWNPOLICYER |
| A_OPEN_01, C_OPEN_01, D_OPEN_01, LM-D17 | **GODKÄNDA EXAKTA FRAMTIDA KARTLAYOUTMÅL** |
| B_OPEN_01 | **INTE GODKÄND** |
| B_OPEN_02, LM-D18 | **UPPDRAG ATT SKAPA KANDIDAT GODKÄNT; SJÄLVA KARTAN INTE SKAPAD/GODKÄND** |
| Gemensam ny exakt fyrkartsversion | **INTE KOMPLETT/INTE GENOMFÖRD** |
| 8×9 kollisionsgiltiga spawnkoordinater och NTSC/TIA-rendering | **INTE VERIFIERADE** |
| S05 integrerad player+NPC+key+orange door+M0+PF kernel | **OLÖST** |
| G5 formell gate | **ÖPPEN** |
| G0, G6/F12/G7+, ROM DEVELOPMENT III/VERIFICATION II/PR-merge | **INTE AUKTORISERAT AV DETTA BESLUT** |

## 5. Original- och specialistkällor
- [G5T GRAPHICS II:s ursprungliga 8 kartvisualiseringar i egen graphicsbranch](https://github.com/Odourman/let-me-out/tree/d20c7ad2ab3c1579586418068884dd8c743a669b/studies/graphics/G5T_2026-11-17).
- [MAIN VII G5U mottagningsrapport, återkörd 18/18 PNG](G5U_MAIN_VII_G5T_GRAPHICS_DELIVERY_INTAKE_AND_MAP_CHOICE_RECOMMENDATION_2026-11-17.md).
- [G5S användarbeslut C1/D1/E1](G5S_MAIN_VII_C1_D1_E1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md).
- [Historisk v0.11 källa](../../design/PLANERADE_RUMSKARTOR_V011.json), [v0.19 exakt kandidatkällfil](../../design/OPEN_ROOMS_V019_40x22_CANDIDATES.json), [MAIN ledger](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md), [G5 spärr](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md).

**Nästa steg:** GRAPHICS II levererar B_OPEN_02 som rådgivande visuell icke-canon studie till MAIN VII, sedan nytt användarval om exakta B-layouten. Ingen ny ROM innan en senare avgränsad separat auktorisation.
