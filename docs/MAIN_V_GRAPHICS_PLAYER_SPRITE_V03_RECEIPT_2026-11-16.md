# LET ME OUT! – MAIN V: PLAYER SPRITE v0.3 grafisk mottagning

**Datum:** 2026-11-16. **Beslut:** v0.3 mottas som **avslutad GRAPHICS CANDIDATE-studie**, **inte** som slutgodkänd spelarmask, Stella-prov, ROM-acceptans eller nytt gameplaybeslut.

## Kontroll av faktiskt uppladdade artefakter

MAIN hämtade själv ned följande två filer **från den dedikerade Drive-mappen** (parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`) och utförde lokala kontrollberäkningar av hela ZIP-byteströmmen:

| Arkiv | Verklig filstorlek | Poster | Full ZIP-SHA256 | ZIP-CRC |
|---|---:|---:|---|---|
| [PLAYER SPRITE v0.2](https://drive.google.com/file/d/1q0_GOmupv1WnOJhKVKIRIvRPW85OsYvm/view) | 271 563 bytes | 38 | `02a71e790b2c3b2a57f67047aebe45def440a75935b2bf45b5f5e0d25a9601b1` | PASS |
| [PLAYER SPRITE v0.3](https://drive.google.com/file/d/1AVQhwVEpb5Bo8XssSro6JARHe-G3LE5C/view) | 297 750 bytes | 69 | `d3db276b032b9a9d0b256a8766fbc65313dd7040162b2e8849240c79cbc28500` | PASS |

v0.3-ZIP har **67 maskinverifierade SHA256-poster i `SHA256SUMS.txt`**, samtliga matchar motsvarande ZIP-innehåll; de återstående två posterna är själva manifestfilerna. De separata Drive-filerna finns och har kontrollerad storlek och parent:
- [Handoff Markdown](https://drive.google.com/file/d/1Lvs6SVWCkpAUuiLlXhXVD5BpgJC0wDrc/view), 8408 bytes.
- [Jämförelsebild PNG](https://drive.google.com/file/d/1MgpxAg2rXrRO7G7mn8yGi4zqq-DRkHjI/view), 230161 bytes.
- [Maskdata JSON](https://drive.google.com/file/d/1P74sUKLMY8y5JOBerwPOQ7bx5v_obOAm/view), 14458 bytes.

MAIN jämförde de faktiska PNG:s 8×9 gul/pixel-binära data mot motsvarande `PLAYER_SPRITE_V03_MASKS.json` direkt (utan att köra GRAPHICS eget verifieringsskript). **Alla fem spelarmaskers 1×-bilder motsvarar källmaskbytes exakt**; två stora original NPC 8×9 1×-PNG finns i paketet. Alla faktiska bitmaphexvärden och SHA256 hos de nya två 9-byte-tabellerna matchar handoff.

| Namn | Hexrader uppifrån/ned | Tända pixlar | Bitändringar mot A2 | Källstatus |
|---|---|---:|---:|---|
| **V03_A2R** | `3C 7E 3C 18 7E 5E DC 24 42` | 36 | 6 | GRAPHICS CANDIDATE |
| **V03_B** | `1E 3F 1C 18 3E 6E CE 0A 11` | 34 | 20 | GRAPHICS CANDIDATE |

Användarens originalskiss, v0.1 A och v0.2 A1/A2 finns i jämförelsen. De fyra ursprungliga androidmaskerna i `design/NPC_REFERENCE_8x9_masks.json` (blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`) ska alltid vara designens orörda jämförelsebas.

## Kritisk grafisk bedömning

**V03_B är preliminärt den bättre av de två nya formerna för separation av vänster arm/vapenzon och två ben.** B flyttar hatten/överdel åt höger, vilket avviker lite mer från användarens handskiss. Vid faktisk 8×9/1×-silhuett är det fortfarande tvetydigt om den diagonala vänsterdelen är en pistol eller en böjd arm. V03_A2R liknar den ursprungliga hattformen mer men vapnet ser ännu mer integrerat ut i armens vänstersida.

**MAIN instämmer i GRAPHICS hårda slutsats: `8x9 WEAPON READABILITY STILL FAILED`.** Det har inte genomförts någon oberoende blind mänsklig läsbarhetsundersökning eller någon faktisk Atari/Stella 8×9 P0-rendering med kandidaterna. Kvadratisk 1× pixelpreview är ett maskdataprov, inte en verifierad TV-bild i faktiska visningsproportioner.

**Inget implicit slutligt godkännande av V03_B.** V03_B behålls bara som den bäst lämpade **nuvarande jämförelsekandidaten**; användaren får bedöma den mot originalskissen. Inga ytterligare små justeringar/v0.4 av samma 8×9-pose utan nytt MAIN-/användarbeslut om annan övergripande siluettstrategi. Ursprungsmålet spelare gul, hatt, vapen, mänsklig kropp, samma storlek som de två stora androiderna består.

## Nästa separata grafikbeslut

Flytta parallellt **GRAPHICS-designarbetet** till fyra ursprungsandroiders föreslagna **gånganimation Frame B**, medan `Frame A` = orörda, tidigare användargodkända 8×9 originalmasker. [Bindande designorder](MAIN_V_TO_GRAPHICS_ANDROID_WALK_FRAME_B_V01_2026-11-16.md). Det är **inte** en ROM-order; genomförbarhet i sexfigurskerneln med `GRP1` och en extra grafikfas är okänd och får inte antas.

**ROM-status hålls separat:** R1-F3 fryst utvecklarrapport på `65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190` beskriver `F3_SECOND_INDEX_GEOMETRY_FAIL` för en enda +1-cykelprovning av index0, och `F3_TWO_INDEPENDENT_RUNTIME_X_LOCAL_INCONCLUSIVE/NOT_RUN`. Full R1 fortsatt BLOCKED/NOT ACCEPTED, ingen VERIFICATION, ingen ny ROM-kod beställs här. Kartor, androidmasker, P0-ROM, PR#7 och canon oförändrade.
