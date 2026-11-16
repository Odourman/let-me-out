# LET ME OUT! – MAIN III R1w: skott förbi första P1-androiderna + verklig TIA-träff

**Datum 2026-11-16. Status: `LOCAL_PASS_R1W_COARSE_M0_FOUR_KERN_AND_P1_COLLISION_600`, isolerat forskningsprov. Full R1 fortfarande FAIL/BLOCKED.** Inte implementerat i huvudspels-PR. Inte formellt oberoende VERIFICATION.

## 1. Referenser och exakt reproducerbart ROM

- [**GitHub Actions #43846485646 – SUCCESS**](https://github.com/Odourman/let-me-out/actions/runs/43846485646), commit **`c6f0f65cb3a9e4e28ba001755ce3fd75e8d8750d`**.
- Researchgren `research/main-iii-r1w-resm0-coarse-window-timing-20261116`.
- [**Actions råevidens #14214713551**](https://github.com/Odourman/let-me-out/actions/runs/43846485646/artifacts/14214713551) – 622 arkivposter inklusive **600 autentiska Stella 6.7.1/X11-PNG**, fullständig DASM-källkod/listing/symboler och binärfil, 600-raders CSV, `summary.json`.
- Nedladdad ZIP SHA256 **`ebc950ae8ce138ddd2b74ba86b35fbacce162d2bc754abf7defe01e98b98edf1`**; ZIP CRC PASS, lokalt granskad.
- **ROM:** exakt **16 384 byte standard F6 NTSC**, fyra identiska 4KiB-banker; **SHA256 `dac6340febe7a0a6e94e3e0231c97e8f79731a60a4eeba8903d95018d804141f`**.
- Baspinning: R1v ROM SHA256 `0110ae7cdf33aee5af75b008c2cdd091bffc3abce85dc3b43a0bcc3f07c3ffe3` och hela tidigare R1u/R1s-kedjan låses i respektive generator.

## 2. Teknisk orsak till förbättringen

I R1v [Actions #43845730545](https://github.com/Odourman/let-me-out/actions/runs/43845730545) flyttade `BIT FRAMELO` före `STA RESM0` M0:s VBLANK-grundposition **9 TIA-CC = 18 GUI-pixlar** höger från R1u till åtta nya X-positioner **250,252,254,256,258,260,262,264** på GUI-y167. All NPC-grafik överlevde och `CXM0P` signalerade genuin M0/P1-kontakt, men skottet saknades i 144 av 600 frames när M0 stängdes för tidigt i sena fjärde-P0-lägen. R1v var korrekt FAIL (456/600).

**R1w ändrar enbart INSTRUKTIONSORDNINGEN för M0-avstängning på specialrasterraden**, inte maskbytes, total kernellängd, 262-NTSC-antalet eller de kritiska `RESP0`-positioneringscyklerna:

| Fjärde-P0-läge | M0 stängs vid 6507-CPU-cykel | Kritisk fjärde-P0-resettid | Anmärkning |
|---|---:|---:|---|
| A (GUI-x330) | **56** (tidigare 54) | originalfas | `LDA #$0E` sker före `STY ENAM0`, `COLUP0` är kvar vid c59 |
| B (GUI-x348) | **56** (tidigare 54) | originalfas | Samma omordning |
| C (GUI-x360) | **56** (tidigare 48) | **c53** | `STX GRP0; LDA #$0E; STA RESP0; STY ENAM0; STA COLUP0` |
| D (GUI-x378) | **53** (tidigare 48) | **c56** | `LDA #$0E; STX GRP0; STY ENAM0; STA RESP0; STA COLUP0` |

**Resultat:** M0 är aktiverad när skottet passerar första stora kvinnans originalmask på x248–263 och avaktiveras innan `NUSIZ0=$02` hinner framställa en oönskad kopia +64 GUI-pixlar. `RESP0` och `GRP0` går fortfarande att skriva i tid för fjärde P0-androiderna; inga verifierade originalmaskpixlar går förlorade utom att två avsiktligt överlagrade gula missilpixlar kan täcka vit P1 på skottets EXAKTA position. Underliggande pixel i samma ögonblick kan inte observeras, men alla källmaskbytes och samtliga övriga pixlar verifierades.

## 3. Exakt resultat från 600 verkliga Stella-bildrutor

| Kontroll | Resultat |
|---|---:|
| 600 löpande Stella 6.7.1 frame-ID, inga luckor | **600/600** |
| 262 NTSC scanlines | **600/600** |
| En ensam gul M0 GUI-y167 vid rätt en av åtta X | **600/600** |
| 8 M0-X x250..264, 75 frames vardera | **8/8** |
| 4 NPC-fjärde-P0-X x330,348,360,378 med hela respektive originalmask | **600/600** |
| Fem samtidiga hela original-NPC-instansmasker (en stor man, två stora kvinnor, en liten man, en liten kvinna), med 14-radspresentation av bevarade 8×9-bitmapmönster | **600/600** (synlig mask efter exakt tillåten M0-overlay) |
| 8 M0-X × 4 fjärde-P0-X × 2 högerdörrslägen | **64/64**, minst 8 reala frames i varje |
| vänster BALL-vägg och höger PF0-vägg med 32-raders dörröppning | **600/600** |
| M0:s gamla huvudhöjd GUI-y160, oönskad andra missil, extra gula/vita pixlar | **0** |
| **Verklig hårdvarukollision:** `CXM0P` read D7 = 1 med avsiktlig M0/P1-overlap på första kvinnan GUI-x250..262 | **525 frames** |
| **Ingen hårdvarukollision:** `CXM0P` D7 = 0 när M0 GUI-x264 precis passerat kvinnans högra pixel | **75 frames** |
| Avsiktligt gula M0-pixlar över vit P1 på skottraden | **1050 pixlar = 525 × 2** |
| Extra vita eller gula spökpixlar utanför förväntad NPC+P0+M0 | **0 / 0** |
| Underkända frames | **0** |

Kollisionen visualiserades i forsknings-ROM:en genom att `LDA CXM0P; AND #$80; STA COLUBK` kördes **EFTER det 14-raders figurbandet**. Bakgrundsregion under figuren är blå, RGB `[0,0,138]`, vid M0/P1-kontakt, annars svart `[0,0,0]`. `CXCLR` nollställer latchen inför nästa frame och `COLUBK` återställs i blankning. **Detta bevisar fysisk M0/P1-överlappning, inte spelregeln om vilken logisk android som träffades**, eftersom P1 återanvänds inom samma rasterband. Ingen hitbox- eller damage-logik har godkänts eller kodats.

## 4. Separat lokal datagranskning

MAIN III laddade ned exakt Actions-artefakten och verifierade **direkt i filerna**:
- ZIP CRC: **PASS**; 622 arkivposter; exakt 600 autentiska PNG med frame-ID som föregående CI-kontroll använder.
- ROM extraherad ur ZIP: **16 384 byte** och exakt ovan angiven SHA256.
- **600/600** fälten `local_pass=True` i rå CSV.
- Verkligt avläst diagnostik: `[0,0,138]` på **525** CSV/PNG-par vid x250–262; `[0,0,0]` på **75** par vid x264.
- SHA256 över **hela spelregionens råa RGB-pixlar** (debugger-HUD utesluten) gav **64 distinkta, stabila bilder**, exakt en för varje M0-X/NPC-X/dörrläge; inga två olika tillstånd delar samma bildhash och inga tillstånd fluktuerade.

Detta är en **egen återanalys av CI-underlag**, men inte organisatoriskt oberoende VERIFICATION.

## 5. Samband med de ursprungliga 30 tricken

- **#10 HMOVE Fine Positioning:** R1u:s `HMM0` åtta-stegsförflyttning används oförändrad.
- **#24 Precomputed Tables/Cycle-Exact Kernels:** `HMM0` hämtas ur åttapost-ROM-tabell under VBLANK; R1w:s fyra rasterlägen är cykelneutralt omordnade.
- **#14 Multiple Display Kernels:** fyra P0-lägen har varsin exakt specialiserad skottrad. Denna arkitektur visar varför separata fönster kan behövas för nästa horisontella område.
- **#15 NUSIZ Sprite Duplication:** dess kopior tas uttryckligen hänsyn till; en felaktig extra M0-kopia har 0 tillåtna pixlar.
- **#20 Hardware Collision Latches:** `CXM0P` **D7** är för första gången direkt instrumenterad och validerad i 600 riktiga frames. Primär TIA-spec: *Stella Programmer’s Guide*, kollisionsregistertabellen.

## 6. Projektgränser och nästa rådgivande forskningsgrind

**Löst ENBART i denna isolerade ROM:** fem hela tidigare originalmaskinstanser, fyra diskreta X-positioner för fjärde P0, åtta nya M0-X från 250 till 264 (över samt precis förbi första stora P1-kvinnan), exakt en missil, rätt Y/handsprunget, verklig hårdvarulatch för M0/P1, korrekt NTSC/yttervägg/dörr, 600/600 utan extra pixlar.

**Inte löst:** M0 över **hela rummets bredd**; skottets faktiska eldknapp och livstid, fri X-spawn, spelarmovement, skotthastighet och försvinnande vid träff, logisk träff-ID/vilken NPC som ska ta skada, fullständig sex-NPC-rad (andra stora mannen saknas), endast fyra fjärde-P0-X, P1-kvinnornas X inte fria oberoende, fullständig originalgrafik/karta/orange dörr/nyckelhål, PAL, R2–R4, formell oberoende VERIFICATION.

**Nästa separata research-fråga:** mät hur långt ytterligare fördröjning av `RESM0` kan nå med den nu bevisade R1w-schemaläggningen innan projektilen faller utanför M0:s aktiva cykelfönster; pröva därefter nya registerfönster/andra kernels (#14) under samma hårda mask- och kollisionstest. Ingen ny spelimplementationsfas får startas bara för att detta research-prov passerar.

**Integritet:** ingen ändring i `main`, ROM DEVELOPMENT:s draft PR #7, VERIFICATION issue #8 eller godkända designmasker. Full R1 är fortfarande **FAIL/BLOCKED**.
