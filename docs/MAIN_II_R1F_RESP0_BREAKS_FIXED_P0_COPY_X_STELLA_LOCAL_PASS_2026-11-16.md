# MAIN II R1f – fjärde ORIGINAL-NPC kan flyttas OBEROENDE av gul spelare på samma Y

**Datum:** 2026-11-16. **Resultat:** `LOCAL_PASS_FOURTH_X_INDEPENDENT_TWO_CLEAN_CONFIGS` för två exakta statiska Stella-prover. **Detta upphäver den tidigare konstaterade fasta P0↔vit-kopia-kopplingen i just denna nya rasterarkitektur. Det är inte fritt 160-CC-X eller sex-NPC R1 PASS.**

## Varför en ny TIA-mekanism behövdes

Föregående R1e använder `NUSIZ0=$04`, en gul P0-huvudkopia och en vit P0-fjärrkopia +64 CC. `HMOVE` flyttar dessa två tillsammans (trick #10 och [Actions 43813500872](https://github.com/Odourman/let-me-out/actions/runs/43813500872)), vilket inte ger individuell NPC-rörelse.

**Ny lösning att prova:** med `NUSIZ0=$02` (medium-dubblett) skriver R1f `RESP0` TVÅ GÅNGER på VARJE originalrad. Den första återutlösningen startar den gula spelarens mediumkopia. Den andra, senare, återutlösningen startar den vita lilla kvinnans mediumkopia efter att `GRP0` har laddats med hennes oförändrade bitmask och `COLUP0` har ställts vit. En tidig och en sen variant byter bara ordning på `STX GRP0` och `STA RESP0` för den senare kopian. Det är två olika 3-cykels 6502-instruktioner: den sena positioneringen kommer **9 TIA-färgklockor** längre till höger utan att den första P0-stroben eller P1 behöver byta tidsposition.

**Hårdvarukälla:** Andrew Towers, `TIA Hardware Notes`, särskilt "The Re-trigger Trick" – https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php. Den exakta implementationen och dess pixelutfall är vår egen DASM/Stella-mätning, inte något som källartikeln garanterar.

## Reproducerbara bevis

- [GitHub Actions `43815070386` – alla steg SUCCESS](https://github.com/Odourman/let-me-out/actions/runs/43815070386); testad commit **`552a085d0c1ce0ec47d4f3342173658a25fd0e87`**, separat gren `research/main-ii-r1f-resp0-independent-fourth-20261116`.
- Evidence Artifact **`14201569326`**, `main-ii-r1f-dual-resp0-fourth-x-evidence`; ZIP lokalt kontrollerad, **88 filer**, `testzip()==None`. Båda ROM, källkodslistningar, PC-/bank-/cykelbilder och pixelgranskning i `rom/v018/experiments/main_ii_r1f_resp0/audit.json`.
- **Tidigt vitt P0-läge**, standard NTSC/F6 16 384 byte, ROM-SHA256 `cb57ba5adeb2da5f4a51f64262ac443196a1d31ca1d894989622dd08c4f9f72b`.
- **Sent vitt P0-läge**, standard NTSC/F6 16 384 byte, ROM-SHA256 `f25dda5c57454d86cb58d17e93a6a1e25768e4115a170a98d4ccd0e3b0b965fa`.
- Originala 8×9-maskdata från `main/design/NPC_REFERENCE_8x9_masks.json`, kontrollerat byte-för-byte vid bygg/test samt i verkliga Stella 6.7.1 X11 screenshot, inte rekonstruerade pixlar.
- Dubbel`RESP0`-källans debugger PC-symboler: gul P0-retrigger vid **`$F0A1`** i båda varianter, andra vita P0-retrigger vid **`$F0AE`** (tidig) eller **`$F0B0`** (sen); verkliga `runToPc`-skärmbilder ingår. PC-stoppen sker **före** `STA RESP0`, inte efter registerskrivningen. Påstå inte post-write-cykler utan separat mätning.

## Faktiska råa Stella-GUI-pixlar (inte TIA-logisk 160-X)

| Objekt | Tidig fjärde P0 | Sen fjärde P0 | Originalets form |
|---|---:|---:|---|
| Gul spelare, P0 via första `RESP0` | **216** | **216** | exakt 8×9 |
| Stor man, P1 #1 | 166 | 166 | exakt original 8×9 |
| Stor kvinna, P1 #2 | 280 | 280 | exakt original 8×9 |
| Liten man, P1 #3 | 406 | 406 | exakt original 8×9 |
| **Liten kvinna, P0 via andra `RESP0`** | **330** | **348** | exakt original 8×9 |
| M0 gult diagnostikskott | 240–241 | 240–241 | en kopia på rasterrad ovanför NPC |

**Varje pixelgrind PASS i båda varianterna:** 262 NTSC-rasterlinjer enligt Stella HUD; alla fyra godkända olika originalmasker och temporär gul spelares mask 100 % intakta; exakt en mask av varje typ (inga dubblett-gubbar); inga extra vita eller gula pixlar i de nio originalraderna; en M0-kopia; maskerna i original 9-radershöjdband. Skillnaden 348−330=18 rå GUI-pixlar = **9 TIA-färgklockor**. Spelarens X=216 är oförändrat, även alla P1-positioner oförändrade.

## Vad det betyder och vad det inte betyder

**Positivt nybevis:** P0-objektets andra ritade bitmap måste INTE alltid vara fast vid första spelarens +64 CC. TVÅ separata `RESP0`-utlösningar på samma rasterrad kan ge **minst två distinkta individuella fjärde NPC-X** utan extra bildrad, spökbilder eller maskförlust i de testade specialiserade 6502-kärnorna.

**Fortfarande blockerad:** godtycklig fri NPC-X över hela 160 CC, nära överlapp, aktiv spelarrörelse och fyra oberoende NPC samtidigt med ALLA positioner, femte/sjätte NPC, fulla bruna PF-väggar, dörr/nyckel, integrerat M0-skott i samma nio rader, rörelse-AI, riktig hårdvara, PAL, oberoende Verification. Två separata statiska ROM är heller inte samma sak som att en ROM kan växla X under exekvering. **Därför behöver nästa prov en enda ROM som växlar mellan de två bevisade rasterkärnorna, under 600 sammanhängande Stella-bilder.**

Research-grenen och den levererade ROM:en är **inte** implementerad i main, draft PR #7 eller VERIFICATION Issue #8, och ändrar ingen designcanon eller spelarregel. Ingen ny implementationstillåtelse eller full-R1 PASS härleds.
