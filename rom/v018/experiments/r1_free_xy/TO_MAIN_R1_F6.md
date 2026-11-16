# LET ME OUT! – ROM DEVELOPMENT II till MAIN V
## R1-F6: TWO-MASK HBLANK → VISIBLE COPY START DIAGNOSTIC – fryst slutrapport

**Datum:** 2026-11-16  
**Status:** **F6_TWO_MASK_HBLANK_PHASE_LOCAL_PASS** – begränsad, reproducerad **DEVELOPER_LOCAL** Stella 6.7.1-geometri; **inte** fullständigt R1, inte oberoende VERIFICATION, ingen slutlig TIA-signalproveniens.  
**Särskilda obligatoriska negativa statusar:** **F6_TWO_INDEPENDENT_RUNTIME_X_NOT_RUN / SIX_INDEPENDENT_XY_NOT_RUN / FULL_R1_BLOCKED**.  
**F6 utvecklingsgren:** \`rom-dev/v018-r1-f6-two-mask-hblank-20261116\`, startad exakt från fryst F5-commit \`953c6c5ef20e83d93474de4c094de784761da257\`. Denna rapport och alla nya F6-relaterade filer ligger endast på den isolerade grenen. Tidigare ROM, maskfiler, R1ba, F2–F5, \`main\` och draft PR #7 är inte ändrade/mergade.

### 1. Auktorisation och tekniskt avgränsat mål

Bindande [R1-F6-order](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F6_TWO_MASK_HBLANK_COPY_GATE_AUTHORIZED_2026-11-16.md), Git blob \`d17996752a2c83e6d387f99a7e3e489d35ad34a6\`; [MAIN V F5/R1ba-mottagning](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F5_RECEIPT_R1BA_VERTICAL_ORIENTATION_INDEPENDENT_AUDIT_2026-11-16.md); [fryst F5 SOURCE_ONLY-rapport](https://github.com/Odourman/let-me-out/blob/953c6c5ef20e83d93474de4c094de784761da257/docs/ROM_DEV_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_TO_MAIN_2026-11-16.md); [F4 föregående tekniska FAIL](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F4.md).

Enda frågan är: kan ett första P1 \`RESP1\` på **c21 eller c23** flytta en **fullständigt rättvänd stor man** medan ett senare \`RESP1\` hålls på **c32** för en **fullständigt rättvänd stor kvinna**, båda på **samma nio rasterrader**, \`NUSIZ1=$01\`? Endast **två** nykompilerade F6/NTSC-geometrier tillåts. Även positivt svar är **inte** två oberoende valbara runtime-X eller sex fria X/Y.

**Låsta top-down-masker** lästa från aktuellt \`design/NPC_REFERENCE_8x9_masks.json\` på \`main\` och den sedan F2/F4 lokala **byteidentiska** \`rom/v018/experiments/r1_free_xy/canon_masks.json\` i den frysta F5-grenen; båda har Git blob **\`058800a4c1904d1ff289e7e61b3902aa111ba16d\`**. Den isolerade F5-basen har inte root-\`design/\` katalogen, därför använder F6-kontrollen **lokal blob-identisk canon**. Detta är inte ett bytebyte eller en ändring av originalmaskerna.

| Objekt | Exakta TOP-DOWN bytes, rad0 till rad8 |
|---|---|
| P1 man, \`large_male\` | \`3C 3C 18 FF 18 24 24 42 42\` |
| P1 kvinna, \`large_female\` | \`3C 3C 18 FF 3C 7E 7E 24 24\` |

Historisk R1ba med \`NUSIZ1=$03\` och **vertikalt omvända fyra stora originalmasker** används **inte** som byggkälla eller maskoracle. MAIN:s egna 600/600-orienteringsmotbevis kvarstår.

### 2. G0 – obligatorisk SOURCE_ONLY-gate före första kompileringen

Nya [\`r1_f6_preflight.py\`](r1_f6_preflight.py) förhandskontrollerar Git blob för ursprunglig **Venetian/F4-stomme** \`a25c92adb4ca5087eeace674e371be98b273ae5b\` och ovan nämnda originalmaskblob; inga andra grafik-/cartridge-familjer. Enbart källhärledning av 6502-opkoder/cykler för **samtliga nio faktiska bildrader**, samt föregående TopBlank/efterföljande BottomBlank, NTSC 262-frame-stomme och HMOVE förberett före bandet. Samma 9-radersband används i båda tillåtna ROM-varianterna. F6:s baseline-/rasterrader är härledda från tidigare lokal F4-positiv bild-/färgstomme, inte från R1ba.

| Sekvens per synlig rad 0–8 | c21/c32-baslinje | c23/c32 |
|---|---:|---:|
| \`STA WSYNC\` vid radstart | c0 | c0 |
| \`STA GRP0\` P0 gul spelare | c5 | c5 |
| \`STA ENAM0\` M0 statiskt testsymbolsskott | c10 | c10 |
| \`LDA #male[y]\` uppifrån/ned, ingen invertering | efter c12 | efter c12 |
| Första \`STA RESP1\` P1 stor man | **c21 / CC63** | **c23 / CC69** |
| Första \`STA GRP1\` man | **c24 / CC72** | **c26 / CC78** |
| Andra \`STA RESP1\` kvinna | **c32 / CC96** | **c32 / CC96** |
| Andra \`STA GRP1\` kvinna | **c35 / CC105** | **c35 / CC105** |
| Nästa \`STA WSYNC\` | **c38 SOURCE_ONLY** | **c38 SOURCE_ONLY** |
| Beräknad återstående marginal av 76 CPU-cykler | **38 cykler** | **38 cykler** |

För **c21**: tre \`NOP\` före första RESP1, därefter \`LDA #female[y]\`, \`BIT FRAMELO\` (3 cykler), \`STA RESP1\` (3). För **c23**: fyra \`NOP\` före första RESP1 och, efter \`LDA #female[y]\`, \`STA RESP1,X\` **nollsidesindexerat**, **X=0**, **4 cykler**, vilket bevarar andra TIA-skrivningen vid c32. \`STA RESP1,X\` adresserar samma faktiska \`RESP1=$11\`, inte ett annat P1-objekt. X laddas 0 utanför 9-radersbandet och ändras inte där. **GRP1-data är hela ursprungliga bytes på varje rad i korrekt ordning;** inga andra NPC, ingen multiprofilselektor.

\`NUSIZ1=$01\`, PF bruna speglade sidoväggar (\`COLUPF=$26\`, \`CTRLPF=$01\`, \`PF0=$F0\`), P0 gula spelaren, M0 ett statiskt skott, initial \`HMOVE\` före synligt band, inga VDEL1-interaktioner och samma frame-skelett bevaras. \`WSYNC c38\` är **statiskt beräknat**; den autentiska WSYNC-trappen efter instruktionsskrivning avbildar **nästföljande scanline/c0**, inte c38. Båda källplanerna avslutar en vanlig nio-radersrad väl under CPU-gränsen; första/efter sista rasterrad har explicit bevarade pre/post-stommar. **F6_G0_SOURCE_ONLY_FEASIBLE_BOTH_PHASES_9_ROWS**, enligt grön G0 före någon lyckad F6-ROM.

**Förregistrerad modell före Stella (INTE justerad):**
- c21/c32 **förväntat crop-X (43,99)**
- c23/c32 **förväntat crop-X (45,99)**
- Hård positiv grind är fysisk första X-förflyttning, konstant andra X och två fullständiga top-down-masker, inte perfekt modellkalibrering.

### 3. G1 – exakt två kompilerade standard-F6/NTSC-binärer, verifierade råbilder

DASM 2.20.14.1 (Ubuntu paket \`2.20.15~20201109+really2.20.14.1-2\`), Stella **6.7.1**, Ubuntu 24.04 GitHub Actions, Pillow/image-råpixelkontroll. Varje ROM exakt **16 384 byte**, fyra **byteidentiska** 4 096-byte F6-banker (bank0–3). Ingen ny bankmekanik/mapper; inga fler än **två unika** geometrivarianter.

| ROM/fas | ROM SHA-256 | Före test: teoretiskt X | Äkta Stella, 16 av 16 | Pixelstatus |
|---|---|---|---|---|
| \`r1_f6_two_correct_masks_C21_C32_F6.bin\` | \`d0572896ed47bf8e75264d1eb33d5e11f640b2390dc42b6565bdac42af86dc32\` | **(43,99)** | **(39,99)** | Båda fulla top-down-masker exakta; 16/16 |
| \`r1_f6_two_correct_masks_C23_C32_F6.bin\` | \`eaed3faa87c496b08c50725f931096d69687385bcd75257d3dd63164dc36baef\` | **(45,99)** | **(45,99)** | Båda fulla top-down-masker exakta; 16/16 |

**FYSISK OBSERVATION:** Man X **39 → 45 = +6 Stella-croppixlar**, kvinna X **99 → 99 = oförändrat**, under byteidentiska ursprungliga maskvärden och med samma andra \`RESP1 c32\`. Alla **32/32** autentiska originalcrop-PNG och deras **32/32** fullständiga debugger-GUI-PNG visar två separata stora rättvända masker, **nio synliga originalrader**, **0 saknade och 0 extra vita** inom verifierat band. Varken sidoförflyttning eller innehåll har härletts från syntetiska bilder.

**P0/M0/PF/NTSC: 32/32**: gult P0 original 9-row, M0 ett statiskt aktivt skott, bruna speglade PF-sidoväggar (inte höger-only R3) samt stabilt **262 NTSC enligt faktisk Stella-HUD**. Ingen ytterligare R2/R3/R4-logik eller gameplay. C21:s avvikelse X39 kontra F5:s X43 **redovisas som verklig avvikelse (-4)** och får inte döljas av att c23 råkar ge exakt X45. En alltför enkel *samma x43-låsning för alla scheman med c21 före HBLANK* är därmed falsifierad av ändrat efterföljande RESP/GRP-schema; en kausal intern TIA-latchmodell är fortfarande **inte slutligt isolerad**.

**Två oberoende källoraklar för varje positiv bild:**
1. direkt XY-mängd/strikt union av de två aktuella **top-down** \`canon_masks.json\`-maskerna i faktiskt observerad geometri, inklusive 0 missing/extra och ghost;
2. fristående bitmap-radvis 336-bitars OR/XOR-popcount-maskkontroll, två unika fulla \`0xFF\`-rader som separata startankare, exakt nio-raders-jämförelse. Ingen \`[::-1]\`, R1ba-oracle eller återskapad bild används som positivt underlag.
   
En **explicit syntetisk negativ mutation per fas**, som tar bort **en** riktig M-pixel i en separat fil märkt \`SYNTHETIC_..._NOT_STELLA\`, avvisades av **båda** källgranskarna; negativa bilder ingår inte i de 32 positiva Stella-bilderna.

### 4. G2 – faktiskt registerbevis, och gränsen mellan CPU-write och intern START

Kritisk autentisk Stella-debugger **frame12 scanline123, bank0**. **Alla nedanstående registercykler och PC efter skrivinstruktionen avlästes från faktiskt körd, oförändrad respektive binär**. Varje ROM har fem **originala 1366×900 GUI-traps** och instruktionsuppgifter i sin egen assembler/DASM-listning.

| Real TIA-write | C21-ROM CPU/CC, PC efter | C23-ROM CPU/CC, PC efter |
|---|---|---|
| första \`RESP1\` | **c21 / CC63**, \`$F147\` | **c23 / CC69**, \`$F143\` |
| första \`GRP1\` | **c24 / CC72**, \`$F149\` | **c26 / CC78**, \`$F145\` |
| andra \`RESP1\` | **c32 / CC96**, \`$F14F\` | **c32 / CC96**, \`$F149\` |
| andra \`GRP1\` | **c35 / CC105**, \`$F151\` | **c35 / CC105**, \`$F14B\` |
| nästa \`WSYNC\` | Stella efter write: **scan124/c0** | Stella efter write: **scan124/c0** |

\`WSYNC\` CPU c38 är enbart **statiskt source-beräknat**, inte ett påstått uppmätt c38 i GUI. Käll-/instruktionsplanen har även P0/M0/PF och 76-cykelkontroll på nio rader; den faktiska trapserien är riktad mot **rad05**, inte en full intern TIA-gate-latchtrace för varje rad.

**Tre tidsdomäner får inte blandas:** CPU \`STA RESP1\` → TIA:s egna counter/reset/decode → intern \`START\`- och \`GRP1\`-latch/pixeloutput. Faktiska CPU/TIA-registertraps och screenshot-X bevisar **positionsrespons**, inte exakt varför en särskild intern START-puls vann racet. Andrew Towers TIA Hardware Notes och Stella 6.7.1 Player/TIA/DrawCounterDecodes är extern källteori, inte interna R1-F6-mätningar.

### 5. Reproducerbarhet: F6-kod, CI-status, råpaket och hashmanifest

**Isolerade nytillagda F6-käll-/hjälpfiler**, samma gren, läsbara vid fryst report commit: 
- [\`r1_f6_preflight.py\`](r1_f6_preflight.py) – G0, exakta mask-Git blobhashar, båda nio-raderscykelplanerna, förregistrerat X, ingen assemblerkörning.
- [\`r1_f6_build.py\`](r1_f6_build.py) – bygger endast valt \`--first 21\` eller \`--first 23\`, exakt originalmaskbyte, DASM \`-f3\` från pinned originalstomme, 4 identiska F6-banker, genererar .asm/.lst/.sym samt ROM SHA.
- [\`r1_f6_audit.py\`](r1_f6_audit.py) – båda fristående top-down pixelkontrollerna samt P0/M0/PF/262 och syntetisk negativ mutant.
- [\`r1_f6_capture.sh\`](r1_f6_capture.sh) – oförändrad Stella real GUI, exakt 16 efter frame10, full 1366×900 och 900×300 raw crop, perbild SHA.
- [\`r1_f6_trace.sh\`](r1_f6_trace.sh) – verkliga separata Stella breakpoint/trap-screens med PC, bank, scanline och CPU/CC.
- [\`r1_f6_c21_baseline_gate.json\`](r1_f6_c21_baseline_gate.json) – sparad G1-grind **före** andra ROM:en, med faktiskt X39/99, första binärens SHA, 16/16+5 traps, kvarhållen ursprunglig c23-prediktion.
- [.github/workflows/v018-r1-f6-c21.yml](../../../../.github/workflows/v018-r1-f6-c21.yml) och [.github/workflows/v018-r1-f6-c23.yml](../../../../.github/workflows/v018-r1-f6-c23.yml) – exakt en binär per fas med fysisk pixel- och trapgate.
- [.github/workflows/v018-r1-f6-evidence-bundle.yml](../../../../.github/workflows/v018-r1-f6-evidence-bundle.yml) – **read-only** hämtning av *redan lyckade* två run-artefakter; inga nya ROM, DASM- eller Stella-exekveringar.

**Reproduktion från fryst källa på Ubuntu 24.04**, för ett **separat** reproduktionsuppdrag, inte tillstånd att köra något ytterligare nu:

    sudo apt-get install dasm stella xvfb xdotool imagemagick python3-pil
    cd rom/v018/experiments/r1_free_xy
    /usr/bin/python3 r1_f6_preflight.py
    /usr/bin/python3 r1_f6_build.py --first 21
    # Baslinjens första ROM måste ge SHA d057... innan test av 23.
    bash r1_f6_capture.sh 21
    bash r1_f6_trace.sh 21
    # Endast efter 16/16 top-down-mask/P0/M0/PF/262 och autentiska traps:
    /usr/bin/python3 r1_f6_build.py --first 23
    bash r1_f6_capture.sh 23
    bash r1_f6_trace.sh 23

Aktuella tre relevanta **gröna** CI-runs:
- [#43963655377](https://github.com/Odourman/let-me-out/actions/runs/43963655377) **SUCCESS**, c21-ROM exakt \`d057...\`, **16 autentiska Stella**, 5 verkliga traps, 16/16 två rättvända källmasker och P0/M0/PF/262, mutant avvisad. **Baseline X39,99**, inte prereg X43,99; CI grön betyder fungerande diagnostik, **inte** perfekt teoretisk prediktion.
- [#43963975072](https://github.com/Odourman/let-me-out/actions/runs/43963975072) **SUCCESS**, **den andra och sista c23-ROM:en** exakt \`eaed...\`, 16 autentiska Stella + 5 traps; faktisk X45,99, byte-/mask- och scenkorrekt, fysisk first-X-rörelse +6 med oförändrad second-X.
- [#43964319661](https://github.com/Odourman/let-me-out/actions/runs/43964319661) **SUCCESS READ-ONLY**, validerar och sammanför **bara två befintliga, frysta** Actions-artefakter, verifierar varenda original-ROM SHA och raw-Stella-hash, inga nya ROM/Stella.

Tidiga **röda** kontroller bevaras exakt:
- [#43963197682](https://github.com/Odourman/let-me-out/actions/runs/43963197682) **RED G0**, första kontrollen pekade på ej existerande root-\`design/\` i fryst F5-bas; **inga** nykompilerade ROM-byte. Rättat till identisk, Git-blobpinnad lokal canon-kopia.
- [#43963459757](https://github.com/Odourman/let-me-out/actions/runs/43963459757) **RED i en DASM-listningstext-guard**, G0 och **första unika c21-ROM-binären lyckades faktiskt byggas** med SHA \`d057...\`, men gamla strängmatchningen missade DASM:s TAB-formaterade \`BIT FRAMELO\` (opkod \`24 80\`). **Ingen** ny c21-geometrivariant; endast regexkontroll rättades och samma ROM-SHA låstes vid nästkommande gröna run. Inga Stella-pixelbevis från den röda körningen.

**Gemensamt slutpaket på verifierad Google Drive-projektplats:**  
[LET_ME_OUT_R1_F6_COMBINED_32_REAL_STELLA_10_TRAPS_SHA256_2026-11-16.zip](https://drive.google.com/file/d/1v7Kxo0nikzp0EhHDiuwqMW3ij85s17Gq/view?usp=drivesdk), file ID \`1v7Kxo0nikzp0EhHDiuwqMW3ij85s17Gq\`, rätt projektfolder \`1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u\`. Verifierad Drive-metadata: **1 292 303 bytes**. Originalarkiv från grön read-only run #43964319661, ZIP SHA256:

    9e483dfc833843060d93a662d097ba8cc71aa9d9f19f29e915407ca0e9dfda80

**ZIP CRC: PASS**, **144 ZIP-poster**, varav **142/142 individuella poster i \`EVIDENCE_FILE_INDEX.json\`** har självständigt kontrollerad storlek och SHA256; de andra två är index-/manifestfilerna. Innehåll: båda riktiga F6-ROM, ASM/.lst/.sym, **32 originala 900×300 raw crop-PNG**, **32 originala fulla 1366×900 GUI-PNG**, **10 separata autentiska TIA/PC/cycle GUI-traps**, två läsbara 16/16 audit JSON, båda syntetiska *endast negativa* mutant-PNG, ursprungliga Actions-logs/script-info, exakta versioner, generatorer och source G0/pixelnegativ. **Positiv Stella-bevismängd = 32 originala frames; inga syntetiska bilder räknade som verkliga.**

### 6. Tolkning, falsifiering och hård STOPP

- **Hård teknikgrind godkänd inom F6:** samma två originalmasker i rätt riktning på samma 9-radersband; riktiga CPU-traps c21/c23 och fix c32; **verkligt X0 39→45**, **X1=99 konstant**, **32/32** pixel- och NTSC-korrekta.
- **F5:s bokstavliga c21-modell \`(43,99)\` är falsifierad för just detta nya c32-schema.** F5:s c23-prediktion \`(45,99)\` är träffad, men exakt resetpipeline/START-/GRP-latchproveniens går inte att härleda unikt enbart ur CPU-traps och skärmbilder. Att c21 x39 skiljer sig från F4 x43 är en del av observationen, inte ett skäl att räkna om tidigare förregistrerade värden.
- **F6 har inte bevisat två godtyckligt eller oberoende RAM-kontrollerade runtime-X**: de två formerna kördes i **två skilda, förkompilerade ROM:er**, inte i samma med två självständiga RAM-reglage. En ändringsbar första X med konstant andra X är endast en **begränsad lokal fysisk genomförbarhet**, inte generaliserad arkitektur för sex NPC.
- **Fullt R1 fortsatt \`BLOCKED / NOT ACCEPTED\`**. Same-band sex individuella X/Y och mixed Y-rader, slutfärdig R1+R3, R2 KEY/O1, R3 dörröppning, R4, grafik/hud, PAL/fullspel, cartridge-familjer, oberoende VERIFICATION har INTE testats eller godkänts i F6. R1ba:s bevisade originalorienteringsfel är oförändrat.
- **HÅRD STOPP uppfylld:** exakt två kompilat med olika geometrisk förstareset (c21/c23), inga andra nya faser, inget F7, ingen kodändring i äldre frysta källor eller originalmasker, ingen PR-merge, ingen F6-kedja på eget initiativ. All eventuell nästa kod-/arkitekturfas kräver ett **nytt uttryckligt MAIN V-beslut**. GRAPHICS och VERIFICATION kvar i sina roller/standby.

**Slutklassning att bokföra i MAIN:**  
\`F6_TWO_MASK_HBLANK_PHASE_LOCAL_PASS / F6_TWO_INDEPENDENT_RUNTIME_X_NOT_RUN / SIX_INDEPENDENT_XY_NOT_RUN / FULL_R1_BLOCKED\`.