# LET ME OUT! – MAIN VI: användarens uttryckliga svarta bakgrund (2026-11-17)
**Typ:** nytt användaruttryckt visuellt riktmärke under MAIN:s granskning av TIA/PF/färgtrick.
**Användarens exakta ord:** "Bakgrunden bör vara svart."

## 1. Ny designriktning, inte ny ROM-implementationsorder
- **Spelets bakgrund bakom väggar, figurer, dörr och nyckel bör vara svart.** Behandla detta som användarens aktuella visuella riktmärke vid kommande research, grafikstudier och ROM-design. Äldre v0.14-dokument beskrev bakgrunden som preliminärt "mörk" och illustrerade nära svart `#080A0D`. Användarens nyare formulering väger tyngre för framtida bedömning: eftersträva **svart**, inte blåsvart/mörkgrå dekorativ ton.
- Detta byter inte automatiskt exakta NTSC/PAL TIA-färgkoder, tidigare PNG-bildfiler, verifikations-PASS, master-specens andra färger eller mapper. Riktig svart på standard-Atari 2600 kräver korrekt `COLUBK` i den senare auktoriserade implementationen samt bevis mot faktisk Stella/NTSC-/PAL-emission. Ingen binär skapas här.
- Befintliga visuella mål bevaras: **bruna** väggar (PF), **vita** androider, **gul** spelare, **guldgul** nyckel, **orange** smal högerdörr med **svart** nyckelhål. Bakgrundsfärgen får inte ändra deras silhuetter, form eller logiska läge.
- Användaren har **inte** ändrat antal androider; fem (2 stora M, 1 stor F, 1 SM, 1 SF) är fortfarande separat utvärderingskandidat. G5:s teknikval och all G6/ROM-implementation är fortsatt ej auktoriserade.

## 2. Faktisk TIA-/grafikkonsekvens
**Separera tre register-/objektlager:**
1. `COLUBK` bestämmer bakgrundsfärgen bakom icke ritade objekt. När playfield (= vägg) är avstängt, och ingen sprite, missile eller ball täcker pixeln, bör svart bakgrund visas.
2. `COLUPF` styr PF och BL i normal färglägesfördelning; en väggpixel som fortfarande är aktiv kommer att visas **brun**, även om `COLUBK` är svart.
3. `COLUP0` styr P0/M0 och `COLUP1` styr P1/M1. Ett transparent utskuret nyckelhål i en orange P1-port blir **inte automatiskt svart** om en brun PF-väggpixel ligger bakom. För ett svart hål måste varken orange P1-pixel eller brun PF-pixel täcka just hålets utdata-CC, eller måste en separat faktiskt möjlig och dokumenterad lager-/färgstrategi användas.

**R3-historisk teknikreferens:** `rom/v018/experiments/r3_c02/TO_MAIN_R3.md`, fryst commit `000b6f2a579e4aa96995229b2174884fb7c565e2`, gav en orange P1-port med transparent svart nyckelhål och korrekt högersidig öppning i den **isolerade** developer-local-ROM, inte en integrerad R1–R4-verifiering. Originalets svart bakgrund som visuell idé ska inte felaktigt tolkas som att en brun PF-cell under nyckelhålet kan lämnas orörd.

## 3. Forskning efter senaste 30-tricksomvärderingen
- Prioritera **`COLUBK` svart + brun PF + P1 orange** som visuell basprofil, inte som en ny oanvänd TIA-kanal.
- Utvärdera PF-buren dörr enligt #05/#07/#12/#14/#24 **med den svarta bakgrunden orörd** och verifierat svart negativt nyckelhål, samt kontrollera korrekt brun yttervägg, endast högeröppning x39 y9..12 och ingen falsk vänsteröppning.
- `Venetian Blinds` #03 är **inte relevant som nyckel–dörr-överlappsdelning om de ligger på olika Y**; vanlig rasterhöjdsseparerad reuse #01 är då enklare. Andra tricks #12 färgväxling och #14 skilda kernels kan användas för HUD och rum, men inte som ursäkt att ändra bakgrund till mörkgrå/gradient utan userbeslut.
- Testa kontrast/läsbarhet av guldnyckel, vit android, gul spelare, bruna väggar och orange dörr mot **svart** bakgrund när grafik-/ROM-prover senare får separat tillstånd.

## 3A. Drive-arkivering 2026-11-17
- [Google Drive – svart bakgrund som visuellt riktmärke](https://docs.google.com/document/d/1Ak5ocPfPARJ8xCxg3kbMYbxXs9Pjhb1ix-BzaDC3PuQ/edit), skapad som native Google Doc, flyttad till officiell projektmapp och läst tillbaka; behåller användarens exakta formulering och TIA/PF-konsekvenser.
- Denna GitHub-fil är den versionsstyrda kopian och aktuell status pekar hit. Ingen ny binär/ROM.
  
## 4. Projektstatus och avgränsningar
**Dokumentation och framtida designriktning mottagen.** Varken ny ROM, DASM, Stella, GRAPHICS-värdeskifte, originalmasker, R1/R2-antal, mapper, PAL eller oberoende E02 verifiering har gjorts. G1–G4 tidigare dokumentationsstatus består, full R1/R2–R4 `BLOCKED/NOT ACCEPTED`, G5 användarval om antal/scope `PENDING`, G6 `NOT AUTHORIZED`.

**Källor:** [Visuellt v0.13-mål](KEY_AND_DOOR_VISUAL_TARGET_V013.md), [v0.14 svart-/guld-kontraststudie](KEY_CONTRAST_RGB_REVIEW_V014.md), [R3 dörr](https://github.com/Odourman/let-me-out/blob/000b6f2a579e4aa96995229b2174884fb7c565e2/rom/v018/experiments/r3_c02/TO_MAIN_R3.md), [30-tricks 2026-11-17](MAIN_VI_30_TRICKS_CROSS_OBJECT_REASSESSMENT_2026-11-17.md), [Current Project State](CURRENT_PROJECT_STATE_2026-11-15.md).
