# LET ME OUT! – MAIN VII G5U: G5T GRAPHICS II mottagen och självkontrollerad, kartval fortfarande öppet
**Datum:** 2026-11-17. **Status:** `G5T_GRAPHICS_DELIVERY_RECEIVED_AND_OFFLINE_REPRODUCED_NO_MAP_APPROVAL`.
**Ägare:** MAIN VII, endast projektmottagning/source-only jämförelse. **Inte** ROM/Stella, oberoende VERIFICATION II, kartcanon, G0/G6/F12 eller PR-merge.

## 1. Faktisk leverans och källa
- [GRAPHICS II leverans, Issue #10](https://github.com/Odourman/let-me-out/issues/10#issuecomment-6956007300).
- [G5T isolerad graphicsbranch, fast commit `d20c7ad2ab3c1579586418068884dd8c743a669b`](https://github.com/Odourman/let-me-out/tree/d20c7ad2ab3c1579586418068884dd8c743a669b/studies/graphics/G5T_2026-11-17): **22 nya textbaserade studiefiler** (SVG-kartor/par/spawn overlays, rapport, validation.json, renderer), 1 commit före main, 0 bakom vid mottagning; **ingen merge**. Original-MAIN-källcommit `57a4f4954f5699b3d20893d12893f901fe767f7a`.
- [Drive leverans-ZIP](https://drive.google.com/file/d/1x4EuWvkwVrJhobUFPRO-IhkA-vF3ZBqG/view): **426 865 bytes**, SHA256 `d8e3a6d3e3c1e6ee6879881ace5207cbfa1c246dc74cb9759acbcbf739780306`, **23 filer** (18 PNG, rapport, JSON, lokalt Python-script, RLE och spawns), ZIP CRC=PASS. [Drive kontaktsida](https://drive.google.com/file/d/17FSrkKVYprkYW8YucqEzCT17MdzgsK2s/view), [Drive rapport](https://drive.google.com/file/d/1HnE89U3kVDvM1GmhfirCsjmu5rG5BiyG/view) alla har verifierad officiell Drive-mapp-parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`.
- GitHub-källblobbar v0.11 `820a74e5fb77c818ffb1286c5b23698d4374e771`, v0.19 `0e449f97f87bd9b403476fd1435398042eaee285`. Båda lästes vid pinnat källcommit från GitHub.

## 2. MAIN VII:s oberoende mottagningskontroll av grafikleveransen
1. ZIP öppnades lokalt, CRC-test gav ingen felaktig medlem. SHA-256 beräknad över exakt Drive-ZIP.
2. `render_local.py` kördes separat i en tom isolerad mapp med levererade `source_rle.txt` och `spawns.json`. **18/18 återgenererade PNG-filer byteidentiska** med ZIP-arkivets 18 PNG. Den återgenererade `VALIDATION.json` var innehållsmässigt identisk med leveransen.
3. En **separat** pixelkontroll med PIL av färgen i mitten på samtliga 40×22=880 celler för samtliga åtta rena PNG-kartor jämfördes mot de avkodade RLE-ritmatriserna: **7 040/7 040 korrekta**, noll fel. Detta är offline-källa-vs-PNG, inte rekonstruktion av TIA-scanlines.
4. Samtliga åtta kartors FNV-1a 32-bit textvärden beräknades **separat ur de ursprungliga JSON-filerna på GitHub** och jämfördes mot leveransens renderer/validation: `A01=88c24581`, `B01=d94133dd`, `C02=11a3207d`, `D01=5046ecfd`, `A_OPEN_01=f8529fc5`, `B_OPEN_01=7746b1c9`, `C_OPEN_01=84612e29`, `D_OPEN_01=16317f3d`. Alla 8 matchade. 32-bitars digest är ett hjälpkontrollvärde, inte kryptografiskt bevis om innehållet.
5. Mottagaren öppnade faktiskt den kompletta fyra-pars-kontaktsidan och granskade presentationen visuellt.

**Slutsats om leveransen:** källtroheten, leveranskomplettheten och den deterministiska offline-reproduktionen är godkända **som MAIN:s mottagningskontroll av en rådgivande grafikstudie**. Inte en VERIFICATION II-signal om ROM/test/grafikkernel.

## 3. Konkreta jämförelsetal, 38×20 interiörceller per karta
| Rum | historisk v0.11 | öppen % | OPEN-kandidat v0.19 | öppen % | v0.19 geometriskt återanvändbara tidigare NPC-spawnankare |
|---|---|---:|---|---:|---:|
| A | A01 | 91,6 | A_OPEN_01 | 95,3 | 18 |
| B | B01 | 79,5 | B_OPEN_01 | 93,7 | 9 |
| C | C02 | 83,7 | C_OPEN_01 | 91,6 | 16 |
| D | D01 | 77,9 | D_OPEN_01 | 92,1 | 15 |

**Bedömning från actual bild:** A_OPEN_01 behåller tydliga L-hörn och rymd; C_OPEN_01 har rumsidentitet och väggvinklar trots fri mitt; D_OPEN_01 behåller egna sidovägar/avdelningar. B_OPEN_01 visar mest bara fyra fristående raka väggstumpar, med risk för ensartad och alltför naken rumsupplevelse. Historiska B01 är å andra sidan mycket blockrikt (156 interiöra väggceller). **Detta är en visuell kvalitetsbedömning, inte godkänt G5-speltest**. Varken nio B-kandidater eller de övriga gamla ankarmängderna bevisar fem verkligt förhandsvaliderade 8×9-/NPC-/key-/exit-spawns.

## 4. Rekommenderat kartbeslut för användaren – ENDAST FÖRSLAG
**MAIN rekommenderar att användaren får välja följande uttryckliga väg:**
- **A_OPEN_01, C_OPEN_01 och D_OPEN_01** kan erbjudas som **exakta 40×22-kartbaser för den framtida fem-NPC-testversionen**, om användaren godkänner just dessa tre.
- **B_OPEN_01 bör ännu inte låsas**. Behåll `B01` som historiskt definierad interimskälla och låt GRAPHICS II, **endast efter ett separat uttryckligt grafikuppdrag**, rita en eller flera nya 40×22-kandidater, t.ex. `B_OPEN_02`, med mer taktiskt intressanta men fortsatt luftiga väggformationer. **Nya B-kartor måste levereras som icke-godkända kandidater**, med spel-/door-/spawn-/förflyttningsunderlag.
- Alternativ för användaren: acceptera alla fyra befintliga `*_OPEN_01` om det enkla B är estetiskt önskvärt, eller behåll historiska kartorna tills vidare.

**Inga av dessa exakta kartor har blivit godkända genom G5T.** Grafikriktning LM-D04 är redan godkänd, men den ersätter inte ett exakt kartbeslut. Det skulle också vara fel att kalla blandad framtida kartbas `v0.19` innan en explicit versionsdefinition gjorts.

## 5. Stoppspärr och nästa steg
- **G5T graphics source-only assignment = DELIVERED / RECEIVED / OFFLINE REPRODUCED.** GitHub Issue #10 kan avslutas som **färdigt uppdrag**, men frågan om kartval kvarstår i G5.
- **LM-D12/13/14/15/16** är godkända framtida gameplay-/kvalitets-/poäng-/spawnmål, medan **exakt kartbas och en framtida 8×9-real-hitbox/spawnpool** återstår.
- **S05 (player, white NPC, gold key, orange P1-door, M0+PF)** saknar fortfarande fullständig TIA-implementering, och förbättrad visuell offline-karta ger ingen ny rastergaranti.
- **G5_FORMAL OPEN**, **G6/F12/ROM not authorized**, ingen PR-merge, ingen ersättning av originalkart-JSON och ingen ny oberoende VERIFICATION utförd.
