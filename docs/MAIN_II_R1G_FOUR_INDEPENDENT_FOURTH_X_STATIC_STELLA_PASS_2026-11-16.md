# MAIN II – R1g: fyra oberoende X-lägen för fjärde original-NPC i fyra separata Stella-ROM

**Datum:** 2026-11-16. **Bevisklass:** `LOCAL_PASS_FOURTH_X_INDEPENDENT_MULTIPLE_CLEAN_CONFIGS`, **endast fyra separata statiska ROM-varianter**. Använd INTE detta som bevis för fri X i allmänhet, fyra helt dynamiska NPC, integrerad full R1 eller oberoende VERIFICATION.

## Vad som faktiskt har visats

- [GitHub Actions #43816935556 – SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43816935556), testad commit `09289305c99b4f8cb77c2b117104c4695ca0de64`, researchgren `research/main-ii-r1g-fourth-x-four-permutations-20261116`.
- Artifact ID `14202424404`, `main-ii-r1g-four-independent-fourth-NPC-X-evidence`: **84 filer** inklusive originalskriven DASM-källa, fyra 16KB standard-F6-NTSC-ROM, verkliga Stella 6.7.1 X11-ramar, PC-stopp före andra `STA RESP0`, manifest och `audit.json`.
- ZIP-filen nedladdad och kontrollerad `testzip()==None`. Samtliga fyra ROM:s SHA256 kontrollerades direkt mot deras egna binärbytes och `manifest.json`.
- Maskerna för stor man, stor kvinna, liten man och liten kvinna matchar `main/design/NPC_REFERENCE_8x9_masks.json` exakt i både källtabeller och 8×9 TIA-pixlar. Gul temporär P0-spelare, ett M0-skott på rasterraden före NPC-bandet och 262 NTSC-linjer bevaras. Inga extra vita eller gula pixlar.
- De tre ursprungliga P1-NPC behåller sin plats, medan den fjärde vita lilla kvinnan kan få fyra olika X utan att gula spelaren flyttas.

| Variant | Gul spelare rå GUI-X | Fjärde original-NPC rå GUI-X | SHA256 för 16KB ROM |
|---|---:|---:|---|
| `pre_mask` | 216 | 330 | `cb57ba5adeb2da5f4a51f64262ac443196a1d31ca1d894989622dd08c4f9f72b` |
| `post_mask` | 216 | 348 | `f25dda5c57454d86cb58d17e93a6a1e25768e4115a170a98d4ccd0e3b0b965fa` |
| `post_lda` | 216 | 360 | `88d1026e6d6455854877fe88fa0054ef3ebe76eb6ff72b2b6f401cc3f9402f91` |
| `post_color` | 216 | 378 | `91da920891ab9f7273f4caed63ad56fbeb9436cf0929794da3a6917557556e96` |

Alla X-tal ovan är i rå 1366×900 Stella-GUI och **inte** Atari-native 160-CC-koordinater. Här ger 48 GUI-pixels spann **24 TIA-färgklockor** från X330 till X378.

## Varför det är en ny teknikvinst

Föregående R1e hade fjärde NPC låst till den gula spelarens X +64 CC genom automatisk `NUSIZ0=$04`-wide-kopia. R1f introducerade **två separata `RESP0`-utlösningar per rasterrad** i mediumkopieläge `NUSIZ0=$02`, där fjärde vita figuren får separat återutlösning. Dessa R1g-varianter omordnar `STX GRP0` (3c), `LDA #$0E` (2c), `STA COLUP0` (3c) och `STA RESP0` (3c), totalt 11 cykler i samtliga varianter. De vita bitmappens olika utlösningsfönster flyttar fjärde figuren utan fler CPU-cykler på de kritiska raderna. **De bevisar inte att godtyckliga instruktionstidpunkter eller närliggande figurer fungerar.**

## Skilj noga mellan R1f och R1g

- **R1f dynamiskt bevis:** [GitHub Actions #43815510141](https://github.com/Odourman/let-me-out/actions/runs/43815510141), **EN enda ROM** som växlar fjärde NPC:s X330/X348 var 16:e bildruta, **600/600** exakta autentiska Stella-ramar. Den ROM:ens SHA är `795dd4d0b8e6255facdb528a1fd4008b38047a5e84c4883d34e2f82f73c5bbb3` och egen rapport finns i [R1f 600-rapporten](https://github.com/Odourman/let-me-out/blob/research/main-ii-r1f-independent-x-600-20261116/docs/MAIN_II_R1F_FOURTH_NPC_X_INDEPENDENT_600_LOCAL_PASS_2026-11-16.md).
- **R1g fyralägesbevis:** fyra **separat byggda** ROM-filer, stillbilder från samma typ av Stella-emulator och samma cykelbudget; ännu **ingen enskild fyraläges-ROM** med 600-rams växling. Fyra rena X betyder inte fyra simultana olika positioner i samma spel.

## Verkliga blockerare och nästa grind

Ännu återstår globalt fritt X över 160 färgklockor, exakt originalgeometri vid näröverlapp, fyra rörliga NPC på en och samma gång, och därefter totalt **sex** unika originalandroider med gul spelare, M0-skott och brun PF-/dörrbelastning. Separata trick #07 Asymmetric PF och #25 Stack TIA PHA har visats i isolerade ROM, men **inte** på samma rasterrader som R1f/R1g. Nyckeln/O1 och hela R1–R4 är inte verifierade.

Den här rapporten är RESEARCH; koden ligger endast i isolerad forskningsgren. Ingen merge, ingen ändring i `main`, draft PR #7 eller oberoende VERIFICATION Issue #8. Ingen designwaiver och ingen fullspel-/PAL-auktorisation.
