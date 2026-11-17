# LET ME OUT! – ROM DEVELOPMENT II → MAIN V
## R1-F9: tre rättvända originalandroider, tre oberoende binära RAM-X, EN standard-F6/NTSC-ROM

**Fryst slutrapport: 17 november 2026.**  
**Resultat: `F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`, enbart begränsad diagnostik med utvecklarens Stella-egenkontroll.**  
**Överordnad status: `FULL R1: BLOCKED / NOT ACCEPTED`.** Inga tre godtyckligt numeriska X, ingen fri Y, ingen full sexandroidskernel och ingen oberoende VERIFICATION.

### 1. Bindande omfattning och kontrollerad proveniens

- [MAIN V:s bindande F9-order](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F9_THREE_MASK_THREE_BINARY_RUNTIME_X_ONE_ROM_AUTHORIZED_2026-11-16.md), Git blob `b174381c423c9a611433d859f675a2c67a2032d7`, tillåter högst **EN ny 16 384-byte standard-F6/NTSC-ROM**, exakt tre originalmasker, exakt åtta RAM-kombinationer och inga ytterligare registerfaser.
- [MAIN:s självständiga F8-mottagning och F9-beslut](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_R1_F8_SOURCE_ONLY_RECEIPT_AND_F9_DECISION_2026-11-16.md), blob `b363b72d58523724f9d7f8b4d1c007d1c2c5e628`. F8 var en källhypotes, inte ett Stella-resultat.
- **Fryst förälder:** F8 commit `5c5e603482be7be482eaf8eae5ba317d91087b3d`; dess bevisade F7-förälder `c8dc8b35f4bb652e3920b70882f8cc1fb84125d3`. F9 skapades på NY isolerad gren `rom-dev/v018-r1-f9-three-binary-x-one-rom-20261117`. Inga tidigare frysta källor eller maskbytes ändrades.
- **Låsta TOP-DOWN-original:** [NPC_REFERENCE_8x9_masks.json](https://github.com/Odourman/let-me-out/blob/main/design/NPC_REFERENCE_8x9_masks.json), blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; bit-/byteidentisk lokal `canon_masks.json` från F7:
  - Stor man `3C 3C 18 FF 18 24 24 42 42`.
  - Stor kvinna `3C 3C 18 FF 3C 7E 7E 24 24`.
  - Liten man `00 00 3C 3C 18 7E 18 24 00`. **Raderna 0, 1 och 8 är uttryckligen noll**, inte utelämnade, förskjutna eller inverterade.
- Referenskriterier [v0.18 acceptance](https://github.com/Odourman/let-me-out/blob/main/docs/ROM_GATE_V018_ACCEPTANCE.md) och [six independent X](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md) är fortsatt öppna. Detta är inte en sex-NPC C01/C04-körning.

### 2. Obligatorisk G0 SOURCE_ONLY före kompilering

[GitHub Actions #44049671587](https://github.com/Odourman/let-me-out/actions/runs/44049671587) **SUCCESS SOURCE_ONLY**; `r1_f9_preflight.py` kördes dessutom en andra gång och passerade som hård förutsättning i G1 **före DASM-installationen**.

G0 kontrollerade från verkliga historiska F7-arkivfiler (inte enbart utvecklarens förra rapport) exakt SHA256:
- `r1_f7_2x2_independent_RAM_X_ONE_ROM.asm`: `2ea6ccbc765bb0472c662bc562c864299e8988dc433c945cf35dae999c79983c`.
- Verklig F7 `.lst`: `5b18b0f5a808b1c38e9b587542dae1b25132a0e92d4f1cd7273156b1b40bf481`.
- Verklig F7 `.sym`: `158e8b7a69a15b2ddf4b60c727d4c8c6d41f51ce8103303cfe6ef71c3c383b83`.
- Ursprunglig F7-ROM: `ede93075c3c2c88b6cca226f52958fbbcb9117a068edca01d4d83ff30e4677df`.

F7 verkliga rasteradresser `$F0FF/$F1F5/$F2E2/$F3D8/$F4CE` ger fyra verkliga ni-raderskernlar med respektive **246+237+246+246=975 bytes**. G0 producerade **72 explicita 6502-källradsscheman** (8 lägen × 9 TOP-DOWN-rader). P0:s `GRP0` källcykel c5, M0 `ENAM0` c10 och de tidigare två P1:s faser finns kvar. Nya tredje masken laddas per **samma källrad** och skrivs till `GRP1` efter kvinnans sista pixel enligt redan observerad F7-geometri.

| RAM `X0X1X2` | M/F/SM `RESP1`, CPU-slutcykel, källa | M/F/SM `GRP1`, CPU-slutcykel, källa | Nästa `WSYNC` rad0–7, STATIC | Sista radens `JMP+WSYNC`, STATIC |
|---|---|---|---:|---:|
| `000` | 21 / 32 / 48 | 24 / 35 / 51 | c54 | c57 |
| `001` | 21 / 32 / 50 | 24 / 35 / 53 | c56 | c59 |
| `010` | 21 / 33 / 48 | 24 / 36 / 51 | c54 | c57 |
| `011` | 21 / 33 / 50 | 24 / 36 / 53 | c56 | c59 |
| `100` | 23 / 32 / 48 | 26 / 35 / 51 | c54 | c57 |
| `101` | 23 / 32 / 50 | 26 / 35 / 53 | c56 | c59 |
| `110` | 23 / 33 / 48 | 26 / 36 / 51 | c54 | c57 |
| `111` | 23 / 33 / 50 | 26 / 36 / 53 | c56 | c59 |

Den värsta källraden slutar c59, alltså **17 av 76 CPU-cykler i marginal**. Dessa källvärden är **inte verkligt mätta Stella-START-pulser**. G0 visade också en **2670-byte rasterkodbudget** för åtta kernlar, F7:s befintliga 310 andra programbytes och en extra 128-byte layoutreserv = preliminärt **3108 programbytes** (reserv, inte löfte om DASM-binärrymd). Tre separat lagrade zero-page-RIOT-byte `X0_SELECT=$A0`, `X1_SELECT=$A1` och `X2_SELECT=$A4` har egna villkorliga `CMP/STA`-uppdateringar. `F7_SEQ_STEP=$A2` / `F7_HOLDCOUNT=$A3` används enbart för det deterministiska testet: två av 30 ursprungliga blank-slot hanterar tre RAM-väljare; 28 ordinarie slots lämnas kvar, högst 41 source-CPU-cykler vid konservativ tre-byte-uppdatering. Varken PAL, en ny bankningsmetod eller extra synlig NTSC-scanline behövdes.

### 3. ENDA verkliga nya 16 384-byte F6-ROM: ROM-hash och faktisk DASM-bank

[GitHub Actions G1 #44050126727](https://github.com/Odourman/let-me-out/actions/runs/44050126727): **SUCCESS**, och **enda** nya F9-DASM-kompileringen. Källgenerator [`r1_f9_build.py`](r1_f9_build.py) använde SHA-pinnad F7 ASM men skapade EN separat F9 ASM och dess verkliga `.lst/.sym`, inklusive åtta i samma exekverbara ROM förberedda nio-radersrutiner. Inga andra geometrier, omkompileringar eller ersättnings-ROM tillkom.

**Binär:** `r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin`. **Exakt 16 384 byte**, fyra **byteidentiska 4 096-byte standard-F6-banker**, `NUSIZ1=$01`, NTSC. **SHA-256 fryst FÖRE Stella:**
`6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`.

**Verkliga F9 DASM-symboler**, inte längre F8:s uppskattning:
- Åtta första rasteradresser: `F9_000_Row00=$F126`, `F9_001_Row00=$F276`, `F9_010_Row00=$F3CF`, `F9_011_Row00=$F516`, `F9_100_Row00=$F666`, `F9_101_Row00=$F7AD`, `F9_110_Row00=$F8FD`, `F9_111_Row00=$FA44`.
- `F9AfterRows=$FB94`, `SetHorizPos=$FBB7`, sista program-RTS `$FBCA` och följande lediga kodadress `$FBCB` → **3019 verkliga programbytes**.
- Datatabeller flyttades från historiska F7:s `ORG $F800` till **`ORG $FE00` inom samma 4KiB-bank**, med de tre oberoende 8-byte desired-tabellerna vid `$FE5B/$FE63/$FE6B`, totalt **115 data-bytes**, samt F6-vektorer 6 byte vid `$FFFA–$FFFF`.
- Faktisk program- och datamängd **3019+115+6=3140 bytes** per exekverande 4KiB-bank, cirka **956 bytes kvar**. DASM:s verkliga symboler/listning bekräftar relocation och branchadresser. Inga bankbyten sker mitt i synligt ni-radersband. Fyra identiska banker ger ingen extra TIA-hårdvara.

### 4. Autentisk Stella 6.7.1: 144/144 råbilder och EXAKT förregistrerade åtta X-tripplar

Samma SHA-låsta ENDA F9-ROM kördes i Stella 6.7.1, debugger frame **#129–#272**, source `FRAMELO=StellaFrame−1`, 9×16 Gray-steg:
`000 → 001 → 011 → 010 → 110 → 111 → 101 → 100 → 000`. Varje byteövergång ändrar exakt EN av de tre RAM-bitarna. **144 originala, oförändrade 900×300 crop-PNG plus 144 originala fulla 1366×900 debugger-GUI-PNG** med perbild SHA256. Varje unikt tillstånd har minst 16 sammanhängande frames, och `000` återkommer sist.

| Faktiskt RAM `X0X1X2` | Förregistrerat X(M,F,SM) | Faktiskt pixelmätt X(M,F,SM) | Autentiska frames | Mask-/färg-/NTSC-status |
|---|---|---|---:|---|
| `000` | (39,99,195) | **(39,99,195)** | **32** | 32/32 PASS |
| `001` | (39,99,207) | **(39,99,207)** | **16** | 16/16 PASS |
| `010` | (39,105,195) | **(39,105,195)** | **16** | 16/16 PASS |
| `011` | (39,105,207) | **(39,105,207)** | **16** | 16/16 PASS |
| `100` | (45,99,195) | **(45,99,195)** | **16** | 16/16 PASS |
| `101` | (45,99,207) | **(45,99,207)** | **16** | 16/16 PASS |
| `110` | (45,105,195) | **(45,105,195)** | **16** | 16/16 PASS |
| `111` | (45,105,207) | **(45,105,207)** | **16** | 16/16 PASS |

**Hård pixelgiltighet 144/144:** båda programmerat **oberoende** TOP-DOWN-oraklen verifierar den fullständiga vita pixelunionen för M, F och SM inom aktiva regionen `x0–335,y50–194`, och oberoende 336-bitars/rad-XOR mot samtliga nio ursprungsrader, **0 pixlar saknade / 0 extra**. Stor-M/F i korrekt riktning, liten-SM:s två översta och sista nollrader **verkligen tomma** och övriga sex korrekt visade, samma ni-radersband `y96–104`. Den fulla vita regionsökningen innefattar nästa rasterrad och fann **inga spökkopior** inom kontrollerad bildyta. P0 gul nio-radersspelare, aktivt statiskt M0-skott, bruna speglade PF-väggar och faktisk **262 NTSC** enligt utvecklarens kontroll **144/144 PASS**. MAIN eller oberoende VERIFICATION har ännu inte gjort en ny fristående färg-/fullframe-egenrevision.

En separat, uttryckligen märkt **`SYNTHETIC_NEGATIVE_NOT_REAL_STELLA`**-bild saknar en riktig M-pixel och förkastas av **båda** oraklen; den är **aldrig** ett av de 144 autentiska positiva bevisen. Körningen stoppades villkorligt vid första felaktiga verkliga bild eller vid varje 16-frames-grind; första riktiga `000`-bilden gav direkt förregistrerat `(39,99,195)` och korrekt NTSC/mask/P0/M0/PF. Alla efterföljande råbilder blev också godkända utan omtag eller annan ROM.

### 5. Tolv logiska ORTOGONALITETSTESTER, faktiskt oberoende 3×binärt X

Varje byte har en separat `CMP/STA`-uppdatering och avläses vid samma-ROMS åtta-kernel-dispatch; det är inte fyra/åtta ROM-varianter eller ett profilindex som ersätter tre RAM-väljare. Följande **12 av 12** fysiskt observerade jämförelser godkändes med de andra två X oförändrade:

| Enda ändrade RAM-bit | Fyra jämförelser med övriga två bitar låsta | Egen fysisk förflyttning | Andra två fysiska X |
|---|---|---|---|
| `X0_SELECT=$A0` | `000→100`, `001→101`, `010→110`, `011→111` | M **39→45 (+6)** | Båda oförändrade |
| `X1_SELECT=$A1` | `000→010`, `001→011`, `100→110`, `101→111` | F **99→105 (+6)** | Båda oförändrade |
| `X2_SELECT=$A4` | `000→001`, `010→011`, `100→101`, `110→111` | SM **195→207 (+12)** | Båda oförändrade |

**12/12 PASS**, inklusive exakt alla åtta förregistrerade numeriska mål **utan någon efterhandskalibrering**. Detta är **tre oberoende BINÄRA X**, inte tre valfria X-koordinater.

### 6. 48 verkliga P1-registertraps, 8 verkliga WSYNC-traps och TIA-bevisgränsen

**48 autentiska originala Stella-debugger-GUI-skärmbilder**, samma oförändrade ROM, från alla 8 RAM-lägen och sex skrivhändelser per läge: **M RESP1, M GRP1, F RESP1, F GRP1, SM RESP1, SM GRP1**. Varje trap har verklig PC, bank, `Scn Ln`, CPU-cycle, TIA colorclock, destination och RAM-minnesvy.

Två direkt i originalbild avlästa exempel:
- RAM `000`, frame136: SM-`RESP1` **c48 / CC144**, PC efter **`$F202`**, scanline123/262, bank0, RAM `A0=00, A1=00, A4=00`.
- RAM `111`, frame216: SM-`RESP1` **c50 / CC150**, PC efter **`$FB20`**, scanline123/262, bank0, RAM `A0=01, A1=01, A4=01`.

**Åtta kompletterande riktiga WSYNC-efter-skrivning-GUI-traps** från exakt samma ROM-hash i [Actions #44050941747](https://github.com/Odourman/let-me-out/actions/runs/44050941747) **SUCCESS**, utan en ny DASM eller binär. Direkt originalavläsning för RAM `111` frame216: efter `WSYNC` är Stella på **scanline124/cpu c0/färgklocka0**, PC efter **`$FB24`**, 262 NTSC. Distinktion: rad0–7 `WSYNC c54/c56` och rad8 c57/c59 är **STATIC SOURCE ONLY** före skrivningen, inte påstådd Stella-mätning av CPU vid post-WSYNC.

**Bevisgräns även efter PASS:** de verkliga CPU-/TIA-skrivtrapsen bevisar **registerskrivningar**, och originalpixlarna bevisar att tre P1-kopior faktiskt syns korrekt. Inga direkta interna `RESET/START/GRP latch`-signaltraces finns; exakt transistornivå-proveniens är inte unikbevisad. Ingen extra vit spritekopia syns inom testad cropregion och alla tre figurerna är separata. Stella debug UI:s auto-sidoreferens till `.cfg/.lst/.sym` med annat filnamn kunde varna, men de verkliga originala `.lst/.sym` finns i ZIP; pixelbevis och registervärden är inte beroende av sidofilsuppslag.

### 7. Fryst, komplett original-evidens-ZIP på rätt Google Drive, SHA-index och reproduktion

**Slutligt paket:** [LET_ME_OUT_R1_F9_FINAL_ONE_F6_ROM_144_STELLA_48_REG_8_WSYNC_SHA256_2026-11-17.zip](https://drive.google.com/file/d/15NquSf1pXcLnSKBzU1fjypDl7RASFR6b/view). **Google Drive-ID `15NquSf1pXcLnSKBzU1fjypDl7RASFR6b`**, verified project-folder parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`, Drive readback size **5 587 328 bytes**.

**Direkt oberoende genomräknat arkiv:** hel ZIP SHA-256 **`fd0127ecba3997a624a74dd1d357f6b2638543f9fc31de120d4968067213c4da`**; **501 ZIP-poster**, **CRC PASS**; **499/499** indexerade faktiska filer exakt rätt storlek och SHA256 i `EVIDENCE_FILE_INDEX.json` + `SHA256SUMS.txt`. De två återstående ZIP-posterna är manifestfilerna själva, inte saknat underlag. Paketet innehåller den enda körbara F9-ROM:en och dess ASM/.lst/.sym; alla genererande/byggande G0-/pixel-/Stella-skript; tidigare arkiverad F7 ASM/.lst/.sym med exakt SHA-pinning; samtliga 144+144 riktiga PNG, 48 riktiga RESP1/GRP1-bilder och 8 riktiga WSYNC-bilder, motsvarande autoexec-script, SHA-filer, 144-raders audit-JSON, 12 kontraster, en märkt syntetisk NEGATIV kontroll samt versions-/stoppinformation. **Inga syntetiska PNG räknas som positiv Stella-bild.**

| GitHub Actions | Faktisk slutsats | Uppdrag och åtgärd |
|---|---|---|
| [#44049671587](https://github.com/Odourman/let-me-out/actions/runs/44049671587) | **SUCCESS** | Fristående **SOURCE_ONLY G0** 72 källrader, 4KiB/RAM-kontroll; inget bygge |
| [#44050126727](https://github.com/Odourman/let-me-out/actions/runs/44050126727) | **SUCCESS** | **ENDA DASM-/ROM-bygget**, SHA före Stella, 144 verkliga bilder och 48 TIA-skrivtraps, 12/12 kontraster |
| [#44050557376](https://github.com/Odourman/let-me-out/actions/runs/44050557376) | **SUCCESS READ ONLY** | Första paketindexet, 471/471 SHA, inga ROM-/Stella-körningar |
| [#44050941747](https://github.com/Odourman/let-me-out/actions/runs/44050941747) | **SUCCESS** | 8 autentiska WSYNC-postwrite-GUI på **samma ROM SHA**, ingen DASM |
| [#44051219389](https://github.com/Odourman/let-me-out/actions/runs/44051219389) | **SUCCESS READ ONLY** | Slutligt sammanfogade originalpaket; **499/499** SHA, ingen DASM/Stella/ny binär |

**Reproducerbarhet för en separat, i framtiden auktoriserad kontroll:** checkout denna **frysta F9-commit**, extrahera de SHA-pinnade historiska F7 ASM/.lst/.sym och F7 original-ROM till repository-root `seed/`; kör `python3 r1_f9_preflight.py` före `python3 r1_f9_build.py`, kontrollera att **EN** 16KiB-F6-binärrygg ger hash `6c258514...` och 4×4KiB identiska banker. Återproducera originaldiagnostiken i standard Stella 6.7.1 med `r1_f9_capture.sh` (144 frame #129–#272) och `r1_f9_trace.sh` (48 traps), samt `r1_f9_wsync_trace.sh` (8 WSYNC traps), följt av `r1_f9_audit.py` mot de låsta maskerna, inte föregående forskningsauditor. Allt finns i arkivet och GitHub-källorna. **Dessa kommandon får INTE utföras som nytt projektsteg här utan separat MAIN-authorization**.

### 8. FORMELL SLUTKLASS, gränser, avslut och hård STOPP

**`F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`** betyder: en enda faktisk F6/NTSC-ROM med tre separat lagrade och lästa binära X-väljare kan producera **åtta oberoende kombinerbara fysiska positions- och masktripplar** med tre rättvända original 8×9-figurer samtidigt på samma höjdband, utan observerade pixelspöken i testområdet, med bevarad gul P0, M0-skott, brun PF, stabilt 262 NTSC och verkliga register-/WSYNC-traps. De **tolv** ortogonalitetsjämförelserna har gått igenom **utan** att de andra två androidernas X ändrats.

**INTE bevisat eller auktoriserat:** tre godtyckligt numeriska X, fri X/Y för sex androider, fjärde android, R1 C01/C04, R1+R3-högerdörr, R2 KEY/O1, R4, PAL, HUD/GAME OVER/AI, fullspelsimplementation, oberoende VERIFICATION eller PR #7-merge. F8:s 4-och-fler-X exponentialkostnad ligger kvar; detta är **inte** en sex-NPC-arkitektur.

**Efter denna enda frysta Markdown-rapport och GitHub Issue #6-handoff STOPPAR ROM DEVELOPMENT II.** Ingen R1-F10 eller ny ROM/CI/Stella/mapper/GRAPHICS/implementation utan ny separat uttrycklig MAIN V-auktorisation.

**`FULL R1: BLOCKED / NOT ACCEPTED`.**
