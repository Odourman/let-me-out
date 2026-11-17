# LET ME OUT! – MAIN VI G2: käll-/bevisluckor och förberedelse för framtida G3
**Datum:** 17 november 2026. G2 dokumentation, ej en ny G3 arbetsorder.

## 1. Vad G2 verkligen låser som RÅKONTROLLERAD evidens
- **Alla fem GitHub Actions originalarkiv** R1e-statik, R1f-statik, R1f-600, R1g-fyrastatik och R1g-600 hämtades genom repoansluten GitHub och kopierades till projektets ursprungliga Google Drive-mapp. **Alla fem laddades tillbaka från Drive och var byteidentiska med Actions-originalen** (exakta helfil-SHA256 i [raw manifest](G2_RAW_REAUDIT_MANIFEST_2026-11-17.json)). Detta säkrar dem oberoende av Actions-retention 14 februari 2027 (rapporterat expiration). F9 och R1ba fanns redan som ZIP i Drive och har verkligen öppnats och rågranskats i G2.
- Ursprungliga CRC-test: **7 historiska ZIP-ar­kiv** PASS: R1e, R1f, R1f600, R1gstatisk, R1g600, F9 och R1ba. F9 index **499/499** SHA-filer PASS. Samtliga ROM kopior är standard-F6-fyra identiska 4K-banker i sina respektive positiva arkiv, inte bevisad dynamisk flerskiktsbankfunktion.
- En **separat offlinepixelalgoritm** läste faktiskt alla 144 F9-rutor, alla 600 R1f-600, alla 600 R1g-600 och alla 600 R1ba. R1e och två R1f-statik huvudbilder direktkontrollerade. Ingen av historiska `analyze_600.py` eller `audit.py` exekverades; originalmasker togs från SHA-kontrollerade användaroriginal-ZIP.
- GitHub Actions jobs kontrollerade LIVE: `43811912249`, `43815070386`, `43815510141`, `43816935556`, `43817440347` och F9 `44050126727` rapporterar `completed / success`. Detta stöder proveniens men innebär **inte** full egen oberoende ny Stella-körning.

## 2. Kvarvarande luckor med beslut om hur de hanteras
| ID | Risk/lucka | Läget efter G2 | Ägare/metod vid behov | Blockerar vad? |
|---|---|---|---|---|
| H01 | F2–F8 originala ZIP/screenshots återverifierades inte byte-för-byte i JUST G2 | Deras MAIN-mottagningsrapporter på live GitHub lästes; fryst F7-källa ligger också i F9:s verifierade ZIP; historisk status bibehållen som `HISTORICAL_MAIN_REVIEWED`, inte `G2_RAW_VERIFIED`. | G3 läsande källanalys eller separat senare re-audit vid konkret behov, hämta exakt fryst Drive-arkiv. | Inte G2 dokumentationsslut, men kan blockera ny byggsten som ENBART dessa bevis stödjer. |
| H02 | Exakta CPU-/START-/GRP-latch-fasförhållanden för nya X utanför provade fyra R1g-lägen | Äldre snapshot+Stella-rastervisning har bevisat specifika pixlar, inte internt signalsekvensprotokoll för alla X. | RESEARCH II/G3 source- och versionspinnad emulatoranalys, event-/deadline-matris. Eventuell ny mikrofysik G6 bara efter ny separat order. | Full fri numerisk X/Y. |
| H03 | Gul P0 och vit P0-NPC behöver `COLUP0` med aktiv gul M0 **på samma synliga scanline** | R1e/f/g har flyttat M0 en rad **före** androidbandet, vilket undviker den centrala samtidiga färgkonflikten. `COLUP0` styr också M0. | G3 per-colorclock P0/M0 registerägarkarta; G4 minimalt falsifierbart eventförlopp. | G6 fysisk crossing GO och full R1. |
| H04 | Tre andra vita NPC:er eller gul P0-spelare kan byta X medan fjärde vita P0 går till vänster | R1g håller alla tre P1-originals och spelaren i fast position. Fyra X-lägen är kodprofiler, inte X från fria byte. | G3/G4 numeriskt RAM-X→schema-design; register-/fasbudget vid varierande sortering. | G7 sex oberoende X/Y. |
| H05 | PF brun, orange/svart right-only, guldnyckel, O1 när samma 9-radersband är redan upptaget | Positiva R1e/f/g saknar PF/vägg och samma-rads-M0; separata R3 prov är inte kombinerade. | G3 sammanhållet R1–R4 resurskontrakt, minsta kritiska samtidighet; G8 framtida endast efter separat order. | R2/R3 integrerad PASS. |
| H06 | Sex maskrader med olika Y och överlappande X | F9/ R1g korrekt topdown på enda konstant rasterband, inte godtycklig Y. R1ba wrong orientation trots 600 positiva interna flaggor. | G3 addera ett Y-index per NPC, varje scanline maskbyte och faktisk tjocklek under sortbyte. | Full R1 C01/C04. |
| H07 | Inte ett enda framtida mått visar **riktig visuell individuell läsbarhet** vid samma-pixel NPC/NPC-occlusion | En vit pixelunion kan vara korrekt men två exakt överlagrade vita aktörer går inte att särskilja visuellt. O1 gäller bara guldnyckel. | G3 markera fysisk omöjlighet/policy som ÖPPEN; användaren ensam fattar eventuellt waiverbeslut om det blir nödvändigt. | S2 tätt-X/8px överlappande acceptans. |
| H08 | Ingen VERIFICATION II oberoende reproduktion av F9/R1g/ny full R1 | G2:s egen läsande PNG-granskning är skild från utvecklarens checker, men MAIN är inte VERIFICATION II. Issue #8 avser äldre baseline `561d3ba`. | Efter separat godkänd ROM-order och fryst rätt commit får VERIFICATION II eget E02-uppdrag och kör egen build/Stella. | E02, PR-merge och full v0.18. |
| H09 | 128 byte RIOT RAM och 4K aktiv F6-bank när alla sex X/Y, sort- och rasterdata är dynamiska | F9 8-kernel-ROM har bara snäv 3-bit RAM-väljare; R1g fyra profiler i en bank; stor siffer-x/y-kod saknas. | G3 RAM/stack-livstid och 76c-/4K-källbudget **inklusive** guldnyckel/dörr. | Val av gångbar G4-hypotes. |
| H10 | Hashade PNG skärmbilder bevisar inte att MAIN/Verification kört egen emulator | Actions-jobben är bekräftat success, men G2 återspelade inte Stella och har ingen ny hardware-test. | Bevara råa PNG, CI-loggar, exakta ROM/bin/källversioner för separat förbestämd nytt G6/E02. | Hårdvara, framtida VERIFICATION sign-off. |

## 3. Pre-registrerat underlag för nästa SOURCE-ONLY-grind (G3), inte dess genomförande
1. Rekommenderad huvudväg är **mixad P0/P1** med P0 gul+vit omtriggning baserad på R1f/R1g, inte F11:s låsta P1-only-fas; detta är en **hypotes att budgetera**, ingen bevisad R1-lösning.
2. G3 måste på varje relevant colorclock och scanline lägga in P0/P1/M0/M1/BL/PF, **COLUP0/1/PF-registerkoppling**, `RESP0/1, GRP0/1, NUSIZ0/1, ENAM0, PF0/1/2, HMOVE, WSYNC`, faktisk 76c-total plus deadlines, ROM bank och RIOT/stack.
3. Stressa att gul spelare kan flytta förbi vit P0-mask utan att M0 byter färg när M0:s pixlar ritas. F9:s 3 binära väljare och R1g:s en diskret fjärde kan inte adderas utan **gemensam programkärna**.
4. G4 GO kan bara betyda GO för **EN** separat förankrad G6 mikrofysikhypotes om sourceplanen plausibel, inte att full R1 genomförbarhet bevisats. Plan B/C från [A/B/C playbook](../MAIN_VI_G1_G10_CONTINGENCY_PLAYBOOK_A_B_C_2026-11-17.md) hålls tillgänglig.
5. Inga ROM/ny mapper/PAL/fullspel/F12/PR-merge/E02 eller designwaivers är auktoriserade av G2.

## 4. Bevarade primärkällor
- [G2 raw recheck manifest med alla binär- och arkiv-SHA](G2_RAW_REAUDIT_MANIFEST_2026-11-17.json).
- [G2 evidence ledger alla F2–F11 + R1e/f/g + R1ba](G2_EVIDENCE_LEDGER_2026-11-17.csv).
- R1e static original ZIP [Drive](https://drive.google.com/file/d/1nq5QcaeKxHR94mvtTKTK8s9TTQ2cdOUo/view).
- R1f static ZIP [Drive](https://drive.google.com/file/d/1srogtJQa6Zs7PCUx2IdG5f10XbFA35X1/view).
- R1f 600 ZIP [Drive](https://drive.google.com/file/d/1td8ZK5fMyqo1OUqGK00xMXcobJug0a1o/view).
- R1g four-static ZIP [Drive](https://drive.google.com/file/d/1ksWm-a-9RBpUe86m-FslZQlEOhnUWemj/view).
- R1g 600 ZIP [Drive](https://drive.google.com/file/d/1BUA6KE7AJRmHNb1XugxbpSx6P3VgJTVM/view).
- F9 final ZIP [Drive](https://drive.google.com/file/d/15NquSf1pXcLnSKBzU1fjypDl7RASFR6b/view), R1ba original ZIP [Drive](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view).
- Alla historiska rapporters source/ref finns i [G2 evidence ledger](G2_EVIDENCE_LEDGER_2026-11-17.csv).
