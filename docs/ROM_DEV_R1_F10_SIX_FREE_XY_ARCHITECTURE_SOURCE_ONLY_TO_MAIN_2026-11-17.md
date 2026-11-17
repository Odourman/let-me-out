# LET ME OUT! – ROM DEVELOPMENT II till MAIN V
## R1-F10: Six Free X/Y Kernel Architecture, SOURCE ONLY

**Datum:** 2026-11-17  
**En enda tillåten leverans:** denna källbaserade Markdown-rapport, isolerad från exakt fryst F9. **Inga nya ASM, DASM, ROM, Stella-körningar, CI, Python-test, PNG, ZIP, grafikfiler eller ändrade äldre projektkällor.**  
**Slutklass: `F10_NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN`.**  
**Överordnad projektstatus: `FULL_R1_BLOCKED_NOT_ACCEPTED`.**

**Precisering av slutsatsen:** Det är **inte** bevisat att sex fria X/Y är omöjliga på all 6507/TIA-hårdvara med standard-F6. Det är bevisat av den inspekterade utvecklingshistoriken att **ingen hittills testad renderer uppfyller det låsta kravet**, och denna source-only-studie kan inte framlägga en komplett tids-, pixel-, RAM- och bankstyrkt väg för alla tillåtna sex-X/Y-belastningsfall. Familj A är det bästa **forskningsspåret**, inte en godkänd arkitektur. Banker i B kan stödja A, men löser inte de fysiska kopiefönstren. C behöver ytterligare fysiska avstånds-/occlusionvillkor som inte är auktoriserade.

---

### 1. Auktoritet, ursprung och fakta som inte får extrapoleras

**Bindande F10-order:** [MAIN V:s R1-F10 SOURCE-ONLY-order](MAIN_V_TO_ROM_DEV_II_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_2026-11-17.md), Git blob `e1f09187bf46d6e434dd0616a287f42bce0ba51e`; [MAIN V:s direkta F9-mottagningsrapport](MAIN_V_R1_F9_RECEIPT_INDEPENDENT_EVIDENCE_AUDIT_AND_ARCHITECTURE_DECISION_2026-11-17.md), blob `b898bc8c4186af2ef4111b036cb257082c55b0c4`; [aktuell MAIN status](CURRENT_PROJECT_STATE_2026-11-15.md), blob `36b6e699f03fbcbc146f81215de1fb08883ebeb9`.

**Exakt fryst teknisk utgångspunkt:** F9 commit `c36982aef770af6cd3f68c2da37b8ed14aee2393` och [F9-slutrapport](https://github.com/Odourman/let-me-out/blob/c36982aef770af6cd3f68c2da37b8ed14aee2393/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md), blob `fd54ed338a0b067ee9551b57bc4cadb28c62c842`. **F9 accepterad av MAIN enbart som diagnostisk utvecklarleverans**, inget E02/fristående Verification.

**F9 verkliga primärfiler lästa SOURCE ONLY:** I exakt tidigare fryst [F9-evidensarkiv på Drive](https://drive.google.com/file/d/15NquSf1pXcLnSKBzU1fjypDl7RASFR6b/view) lästes `F9/r1_f9_three_masks_three_binary_ram_x_ONE_ROM.asm` och `F9/dist/r1_f9_three_masks_three_binary_ram_x_ONE_ROM.sym` med vanlig arkivtextläsning; **ingen** DASM/ROM/Stella/testkod har körts i F10. MAIN:s mottagning fastställde original ZIP SHA-256 `fd0127ecba3997a624a74dd1d357f6b2638543f9fc31de120d4968067213c4da`, 499/499 filhashar, en 16 384-byte ROM SHA `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, 144/144 autentiska pixelbilder och 12/12 binära X-kontraster. För F10 är detta **ärvd, fryst evidens**, inte en ny utförd verifiering.

**Ursprungsdefinition:** [Låsta fyra 8×9-top-down-maskar](../design/NPC_REFERENCE_8x9_masks.json), Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; [v0.18 acceptans B02/C01/C02/C03/C04/E02](ROM_GATE_V018_ACCEPTANCE.md); [sex individuell X/Y-kravställning och stressmål](MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md).

| Verkligt objekt | Antal i R1 | Låsta nio bitmaprader, uppifrån och ned |
|---|---:|---|
| Large male (M) | 2 | `3C 3C 18 FF 18 24 24 42 42` |
| Large female (F) | 2 | `3C 3C 18 FF 3C 7E 7E 24 24` |
| Small male (SM) | 1 | `00 00 3C 3C 18 7E 18 24 00` |
| Small female (SF) | 1 | `00 00 3C 3C 18 7E 3C 24 00` |

Alla sex ska ha **egna uppdaterbara NUMERISKA X och Y** och renderas med rätt TOP-DOWN-originalrader, även med samma Y och överlappande rasterhöjder. **P0** är fullstor gul spelare, **M0** aktiv projektil, **PF** bruna väggar. R2 kräver senare fem NPC + guldnyckel och oförändrad logisk nyckelposition vid skymning (O1); R3 kräver asymmetrisk öppning **endast till höger** och svart nyckelhål. En separat ROM med bra R3 och en separat ROM med bra R1 **är inte** ett fungerande fullspel.

**Separat, källkonkurrerande hårdvaruunderlag:**
- [Andrew Towers, *TIA Hardware Notes* (2003)](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php), avsnitten *Player Position Counters*, *The Re-trigger Trick*, *CPU Clock to Player Pixel Table*: CPU-`RESP1`, 4-CC counter-reset, NUSIZ decode och intern START-latch är skilda händelser; close/medium/far-decodes ~12/28/60 räknarklockor (visuell kopia nominellt efter omkring 17/33/65 CC); på varandra följande reset kan tappa eller fördröja START.
- **Faktiska versionspinnade Stella 6.7.1-källor, LÄSTA utan körning:** [`Player.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx), [`Player.hxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.hxx), [`DrawCounterDecodes.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/DrawCounterDecodes.cxx), [`TIA.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx), [`CartF6.cxx`](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/CartF6.cxx). Den **verkliga** `DrawCounterDecodes` har tabellindex 12,28,60 och huvuddecode 156; `Player::tick()` använder EN `myIsRendering`, EN `myRenderCounter` och EN `mySampleCounter` och **återinitierar samma räknare** när en ny copy-decode inträffar. `Player::resp()` korrigerar early-render-counter efter reset. `TIA::poke(GRP1)` går genom delay-queue; `TIA::poke(RESP1)` via `resxCounter`. Detta är viktiga fysiska modellbegränsningar, **inte** en intern START-signalmätning av sex NPC.
- [Stella Programmer's Guide](https://www.digitpress.com/library/techdocs/2600_Stella_Guide_12-3-79_reformatted.pdf), primär hårdvarudokumentation: 228 TIA-färgklockor/scanline = 68 blank +160 synliga; 3 CC/CPU, **76 CPU-cykler/scanline**, fem rörliga TIA-kanaler och endast två fulla 8-bitars players. [Stella Debugger](https://stella-emu.github.io/docs/debugger.html) för verkliga register- och cykelbevis i eventuellt senare separata uppdrag.
- F6 är **4×4096 ROM-byte, en aktiv 4KiB-bank**, hotspots `$FFF6..$FFF9` (6507 mirror `$1FF6..$1FF9`), inte fyra samtidiga spritekopior. Stella 6.7.1 `CartridgeF6::checkSwitchBank` visar uttryckligen bankval vid access till de fyra hotspots.

**Researchordning/30 trick:** [De ursprungliga exakt 30](RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md) (alla 01–30 lästa igen), [MAIN:s tillämpningsgranskning](MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md), [MAIN:s separata 30-granskning](MAIN_30_TRICKS_RESEARCH_REVIEW_2026-11-16.md), [post-F4 HBLANK/30-trick-korrigering](MAIN_V_POST_F4_RESEARCH_30_TRICKS_HBLANK_COPY_CAUSE_2026-11-16.md), [F5:s korrigerade START/latch-orsak](MAIN_V_F5_SOURCE_ONLY_CROSSCHECK_HBLANK_R1BA_AND_30_TRICKS_2026-11-16.md), [retrigger-research](MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md), [F6-bankrevision](MAIN_F6_BANK_MEMORY_AUDIT_2026-11-15.md), [R3-integrationsmottagning](MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md), [The Cabin-forskningens begränsade tekniköverföring](RESEARCH_THE_CABIN_TRANSFER_2026-11-15.md). Deras äldre forskningskonklusioner är rådgivande; **MAIN:s nyare F9 direktbevis väger högre än äldre negativa tvåkopiehypoteser**, men *bevisar fortfarande inte sex*.

---

### 2. Faktiskt F9-kernelresultat och varför tre binära X inte kan generaliseras fritt

I F9 styr tre **separata lagrade** RAM-byte `$A0,$A1,$A4` tre P1-kopior, med 8 förkompilerade kombinationskernlar. 144 autentiska frames och 12 ortogonalitetskontraster bevisar tre rättvända originalmasker (M/F/SM) på samma 9-radersband. Övriga krav uppfylls endast i detta **lokala fasta** diagnostikfall.

| Register | F9 verklig källa för lågt/högt RAM-val | F9 verkligt uppmätta screenshot-crop-X |
|---|---|---|
| M `RESP1` | c21/c23; `GRP1` c24/c26 | 39/45 |
| F `RESP1` | c32/c33; `GRP1` c35/c36 | 99/105 |
| SM `RESP1` | c48/c50; `GRP1` c51/c53 | 195/207 |
| Följande `WSYNC` | source c54/c56; sista radens `JMP+WSYNC` c57/c59 | efter-`WSYNC` verklig Stella-trap på nästa scanline c0 |

F9 har `NUSIZ1=$01` och **en enda P1-kanal**, inte tre fristående samtidiga player-enheter. Varje av de nio källraderna har statiskt upprullade `LDA #maskByte` och vänt-`NOP` innan de låsta CPU-faserna. **F9:s 17 lediga CPU-cykler gäller bara värsta förkompilerade sista radens c59, inte en framtida sexmaskskernel med runtime-sortering, uppdaterbara 1-CC-X, väggen, nyckeln eller dörren.**

F9:s verkliga DASM-`.sym` ger 8 kernlar på adresser `$F126,$F276,$F3CF,$F516,$F666,$F7AD,$F8FD,$FA44`; slut `F9AfterRows=$FB94` och sista kod-RTS `$FBCA`. **3019 exekverbara programbyte +115 tabelldata +6 vektorer =3140/4096 byte**, aritmetiskt **956 byte återstående**. Men `$FFF6..$FFF9` är **fyra bankhotspots**, inte 4 säkra generella data-/kodbytes: de faktiska säkert oallokerade luckorna är `$FBCB..$FDFF = 565 byte` och `$FE73..$FFF5 = 387 byte`, totalt **952 säkra oallokerade byte** under aktuell F9-layout. Det betyder inte att 952 byte räcker till full AI, sortering, riktiga sex-X/Y, spelare, nyckel, högerdörr och HUD.

**Varför detta inte är en datatabellfråga:** redan **sex binära** selectors skulle kräva `2^6=64` kombinationer. En ren dubblering av enbart F9:s **trefigur-kärnor** blir `8×2670 = 21 360 byte` över alla 64, FÖRE instruktioner för figur 4–6 och all spelkod: mer än hela standard-F6:s 16KiB. Om 64 profiler delas jämnt på 4 banker behövs 16 profiler/bank × F9:s 333,75 genomsnittliga rasterbytes = **5340 rasterbytes per bank**, över **4096** redan utan övrig kod. För sex *godtyckliga* X med 160 möjliga CC-positioner har man i stället upp till `160^6=16 777 216 000 000` X-kombinationer, före Y: ingen F6-tabell av alla statiska profiler är tänkbar. Ingen sådan profilupprullning ger dessutom fria Y eller en fungerande rums-/dörrrenderer.

---

### 3. Fysisk TIA-tidslinje, åtskild från CPU-klockbudget

**En NTSC scanline = 228 CC = 76 CPU-cykler, med 68 CC HBLANK och 160 CC synlig bild.** En 8-bitars P1-kopia i normal bredd använder åtta synliga färgklockor. En tidig `RESP1` är **en registerskrivning**, inte samma sak som omedelbar intern reset, START-decode eller synlig första pixel. `GRP1` är **ett enda** aktuellt mönsterregister, inte en kö med sex oberoende maskbytes. NUSIZ har inbyggda kopiestarter med bundna avstånd; HMP1/HMOVE är gemensamma för P1 och inte individuell finjustering av var och en av sex P1-kopior.

**Fem nödvändiga, särskilda worst-case-scenarier. Ingen ny tidsmätning görs i F10:**

| Fall | Källfastställt begärt scenutfall (TIA-CC eller raster-Y, INTE F10 Stella-resultat) | Minsta nödvändiga CPU/TIA-kedja | Öppet svårt/falsifierande förhållande |
|---|---|---|---|
| **S1. Sex same-Y, åtskilda men INTE låst NUSIZ-geometri** | `X=[16,36,56,76,96,116]` CC, **alla Y=96**, de fyra låsta typerna M,M,F,F,SM,SF över 9 rader, P0/M0/PF samtidigt | På varje av y96–104 behövs sex separata korrekta maskstarter i stigande X och maskbyte i rätt fönster. Ett enkelt F9-close-latens-resonemang pekar ungefär på `RESP1≈c22,29,36,42,49,56`; **ENDAST VILLKORLIGT RÄKNEEXEMPEL**, inte förregistrerad faktisk hårdvaruprediktion | Endast ~20 CC = 6–7 CPU-cykler mellan startmål, men direkt serie `LDA #mask; STA RESP1; STA GRP1` kostar redan **8 CPU-cykler =24 CC per mask**, även innan PF/dynamisk återordning; ingen sexfönster-plan visad |
| **S2. Sex täta/överlappande** | `X=[40,44,48,52,56,60]` CC och Y=96, med par endast **4 CC** isär och 8-CC bitmapbredd | Samma P1 scan-counter skulle behöva bibehålla flera olika 8-pixel-avläsningar under **samma** CC-intervall | Stella 6.7.1 `Player::tick` har ett renderings-/sampletillstånd. Nya START återinitierar räknarna, inte sex simultana kopiekanaler. Bevarade sex individuella överlappande originalformer kan **inte antas**. MAIN/användare måste besluta explicit **occlusion/priority**, annars strider samma-pixel-fallet mot krav på sex separata läsbara fulla masker |
| **S3. Delvis Y-förskjutning, men sex aktiva på vissa rader** | `Y=[96,97,98,99,100,101]`, varje mask 9 rader. På `y101–104` är **alla sex** samtidigt aktiva trots olika Y; X kan röra sig separat | Per skärmrad `r_i=y−Y_i` ger 0–8 för aktiva NPC; radbyte M/F/SM/SF måste förberedas, Y-nollrader måste vara äkta 0, aktiv lista och sorteringsordning varierar | Vertikal multiplex löser inte den **verkliga sexaktiva-raden**. Direkt per-scanline test/sort/reindex tillkommer efter redan mycket snäv GRP/RESP-budget |
| **S4. Ordning byts genom rörelse** | Två olika NPC rör sig från t.ex. `(X_M,X_F)=(60,64)` till `(66,58)`, andra fyra har kvar egna X/Y; mötes-/överlappningspunkt passeras | Sorterad *renderingsordning* måste bytas utan att NPC-ID, typ, 9-raders bitmapposition, kollisionsidentitet eller logiskt X/Y byter ägare | Statiska `modeID`/NUSIZ-par och tidigare bankrutiner kan inte bara byta namn på kopior; sortering/timing behöver per-frame förberedelse och en explicit pixelöverlappningspolicy |
| **S5. R2 fem NPC plus nyckel / R3 samtidiga högerdörr** | Fem originella NPC, **en guldnyckel** vid låst logiskt X/Y som får skymmas enligt O1, gul P0, M0, bruna PF och senare endast-höger-öppen dörr med svart nyckelhål | Samma synliga rad kan kräva fem P1-retriggers **och** guldnyckelbyte i annat grafiskt/färgläge; R3 kräver asymmetrisk PF-vänster/höger-skrivning samt P1-dörr/nyckelhåls-overlay | Nyckel `P1` konkurrerar om samma 8-bitarsregister, `COLUP1` vit→guld→vit kostar skrivtid, `M1/BL` ger ej originalnyckelns 8-bitarsform, `PF` delar vägg-/dörrkanal. Ingen R1+R2+R3-integration är uppmätt |

**Viktig fysisk gräns för S2:** Kravet på **sex separat lagrade koordinatpar** är inte detsamma som sex samtidigt synliga 8-bitars rasterkanaler. För två 8-breda figurer med X-skillnad 4 finns ingen enkel singel-P1-signal som samtidigt avläser två olika figurpixelindex för samma CC. En **bitvis sammanslagen maskunion** eller *priority occlusion* kunde vara en annan designregel, men kan förstöra läsbarhet/individuell maskexakthet och är **inte** en befintlig godkänd waiver. Man får inte tyst byta C01/C04 mot ett antagande om att NPC aldrig kolliderar.

**S1:s nominella c22,29,36,42,49,56 är inte ett egentligt TIA-bevis.** F9:s verkliga fas och HBLANK-klamp samt Towers reset/latch visar varför enkel `x≈3c−68+17` inte kan extrapoleras mellan alla positioner. Vid runt 18/33 CC täta resetter finns enligt Towers latchfaseffekter. För att över huvud taget godkänna A behövs en **faktisk källrad med register- och synliga pixeldeadlines** för alla sex vid valda X, inklusive rest-/wrap-kopian på nästa rad.

---

### 4. Sexparens CPU-cykelUNDRE gräns, och varför det inte räcker med 76-kryss

Det följande är **uttryckligen villkorlig lower-bound för familj A med EN separat `RESP1` och EN separat `GRP1` per NPC, och statisk P0/M0**. Det är **INTE** ett hårdvaruteorem som utesluter alla NUSIZ-auto-kopior, GRP-värdesåteranvändning eller någon helt annan renderer.

| Händelse / komponent per belastad rad | Minsta CPU-cykler med enkla zero-page TIA-write-opcodes | Vad som INTE inkluderas |
|---|---:|---|
| Sex separata `STA RESP1`, minst 3 cykler/st | **18** | Kopiestart-/latchlatens, fin X-quantization, HMOVE |
| Sex separata `STA GRP1`, minst 3 cykler/st | **18** | Maskhämtning, GRP-delay, copy föregående/senare timing |
| Sex `LDA #maskByte`, minst 2 cykler/st från omedelbara statiska värden | **12** | Faktiskt **dynamiskt** Y/typ/index/RAM-uppslag |
| Gul spelare P0 `LDA/STA GRP0` | **5** | Flyttande P0/ändrat P0-color register |
| Statiskt M0 `LDA/STA ENAM0` | **5** | Rörligt skott, re-positionering, kollisionsarbete |
| Nästa rad `STA WSYNC` | **3** | Kontroller/branch, PF/väggar, bankval |
| **SUMMA, direkt och optimistisk statisk A-layout** | **61 / 76** | **Bara 15 cykler kvar**, för precis hela `sort/dispatch/index/PF/Y/RESP-gap` |

Om de sex maskbytes faktiskt måste hämtas från **zero-page RAM** (`LDA zp` =3 cykler vardera) i stället för inbrända immediates, blir det **67/76**, endast **9 kvar**. Om de kräver `LDA table,X` i ROM (~4 cykler, mer vid page-cross) blir det **73/76**, bara **3 kvar**, före dynamiska X-gap och vägg. Det finns optimeringar (förladdning i A/X/Y, dela identiska maskbytes i vissa rader, auto NUSIZ-starter, VDEL, hård registerplan), men **INGEN komplett sådan källa existerar för sex godtyckliga X/Y under ovanstående adversarialt belastade scenarier**.

**R3-konflikt konkret:** den [frysta isolerade R3/C02-kerneln](MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md) har riktiga PF-skrivtraps på c7/15/22 (vänster) och c37/45/52 (höger), plus P1 `GRP1` runt c62; den statiska sista-radens uppskattning var **74/76**, för en **annan** kernel. Om en sådan kritisk rad behöver sex individuella `LDA/STA PF0/1/2` = **6×5=30 cykler** på köpet, blir den enkla direktarkitekturens **61+30=91 >76** redan utan tid för sortering, extra NUSIZ eller orange svart hål. Detta bevisar INTE att alla alternativa kombinerade R1/R3-kernels omöjliggörs – en perfekt staged PF-rad kan ha färre skrivningar – men **det avfärdar att F9:s befintliga 17-cyklersmarginal skulle finansiera R3-integration gratis**.

**Y-kravets skarpa implikation:** för varje synlig scanline `s` måste logisk rad `r_i=s−Y_i` bestämma vilken exakt källbyte som ska ritas i ordningen för de aktiva 6, inklusive de särskilt nollställda småmaskraderna. Att göra sex Y-intervallsjämförelser, sortera X och hämta sex radbytes **inne på samma kritiska linje** ryms inte i den visade optimistiska 61-cykelkalkylen utan ny förberedelsestruktur. Men att förberäkna en hel 160×6 maskplan i RIOT är minst **960 bytes**, över 128 bytes *före* koordinater. En rullande per-rad-eventkö i VBLANK + en konstantcykel kernel är ett **möjligt designmönster**, men ingen härledd fungerande plan med konkreta CPU-deadlines och rätt image-buffertar har ännu belagts.

---

### 5. Familj A – dynamisk P1-retriggering och datastyrda deadlines

**Mest relevant hypotes:** ersätt F9:s `2^n` upprullade modekernlar med ett sorterat fysiskt eventflöde för sex logiskt separata NPC. I VBLANK sorteras SEX individuella numeriska `X_i` med beständigt NPC-ID, deras `Y_i` hålls separat, och en plan beskriver för varje aktiv rasterrad `(NPC-id, row_i, maskByte_i, requested_X_i, RESP-write-cycle_i, GRP-write-cycle_i, riskflag)`. Följande åtta-fas-funktioner behöver konkreta bevis innan de ens får kallas fungerande:
1. Positionstransform `X_i→RESP1 CPU-cycle/phase` där exakta enskilda färgklockor antingen kan åstadkommas eller redovisas som icke uppfyllda; en `RESP1`-instruktion har 3-CC CPU-kvantisering. `HMP1/HMOVE` finjusterar P1 som helhet, inte sex individuella kopior efter var och en.
2. **Sex olika P1 START-fönster inom samma 160 synliga CC**; nästa `RESP1` får inte gå in i föregående START/latch/8-pixel-scan-counter på ett otillåtet sätt.
3. `GRP1` måste matas med rätt TOP-DOWN bytes före respektive start, utan att skriva över en tidigare ritande kopia; real TIA 6.7.1 har EN `Player::myPatternNew` och EN aktiv graphics-scan-counter.
4. Runtime-väntning för varje `X_i` får inte vara en cykelvariabel `BNE`-loop som ibland kommer för sent: worst-case `LDA/STA/branch/page-cross` måste vara explicit. ROM är **read-only**; en dynamisk kö i RIOT kan innehålla **data**/index, men inte självgenererad exekverbar 6502-kod utan en ny, hårdgranskad teknik/mapper. En ROM-tabell med tidsplaner per gap begränsar gap-envelopen och ger inte `160^6` fria formationer.
5. Om de sex önskade X blir tätare än de nödvändiga kopie-/skrivfönstren krävs en explicit **spel-/designpolicy** för återanvändning, överlappning, occlusion eller särskilda test-FAIL. Inget automatiskt mål-X får korrigeras i spelkameran utan MAIN:s beslut.
6. Y-bandseparering kan göra färre objekt aktiva på NORMAL-rad, men det angivna `C04`-fallet med sex överlappande nio-radersfönster tvingar tillbaka sex-objektslasten; åtta olika X-baserade ROMkernlar får inte bli ordnings-ID i stället för numeriska X.

**Redan bevisat:** F9 bevarar P0/M0/PF och **TRE** rättvända individuellt BINÄRA kopior på en rad, inklusive tre verkliga P1-registertraps/copy. **Inte bevisat:** ens **fyra** fritt numeriska, överlappande X eller bytehämtning från 6 separata Y-banor under 76 cykler.

**Fysisk HARD STOP för A:** varje scen som kräver sex separata 8-CC pixelkopior som överlappar på P1 i samma ögonblick utan godkänd compositor/occlusion; varje `RESP/GRP` deadline-paket över 76 cykler; utebliven/lost/restarted START; fel vänd mask eller ghost; direkt positionskvantisering som inte kan justeras individuellt till begärda X.

**EN minimal, framtida, separat auktorisationskrävande falsifieringsgrind A:** en **enda** standard-F6/NTSC-ROM med **fyra** olika rättvända originaltyper M/F/SM/SF och fyra **verkliga numeriska RAM-X**, `Y` samma 9-radersband, **ingen** 2^4-modeprofil, positionstrippel till fyra runtime-coordinates, scen `X_CC=[16,36,56,76]` i 9 rader samt en RAM-X-förändring +3 CC för exakt EN utan att röra övriga tre. P0 gul, M0 skott och PF väggar. Kräv 9/9 originalrader, äkta fyra-START- och GRP-traps, exakt faktisk X och 262 NTSC på två följande frames. **FAIL** om exempelvis endast tre skilda fullständiga masker kvarstår, första/andra X ändras vid fjärde, eller +3 CC inte kan realiseras. **PASS vore bara ett nödvändigt delbevis**, INTE tillstånd till sex eller R1. Ingen ny testgrind är auktoriserad genom denna rapport.

---

### 6. Familj B – bankfördelade specialiserade standard-F6-displaykernlar

**Korrekt funktion:** fyra olika bankar skulle kunna bära **data, Y-topologier och specialiserade whole-band display-kernlar** med en säker gemensam hotspot-/vektor-/returtrampolin. Sortera sex numeriska X/Y under blanking, välj specialiserad bank beroende på **typer av belastning**, inte precomputed varje X-kombination. En bank kan innehålla tung same-Y-kernel, en annan lätt blandad-Y, en separat statiskt hanterad väg-/dörrkernel etc. **Viktig begränsning:** om sex same-Y och högerdörr ligger i samma rad måste den aktiva bankens enda kernel ändå göra båda; olika R1/R3-demobanker gör inte samma-frame-integration.

**Källfakta:**
- Standard F6: hotspots `$1FF6..$1FF9`; access till en adress väljer bank 0–3 (Stella `CartridgeF6::checkSwitchBank`). **4×4096 ROM**, endast den valda bankens `$F000..$FFFF` exekveras vid varje tidpunkt.
- En vanlig absoluta `STA/BIT $FFFx` använder **4 CPU-cykler** för själva accessen. Om man sedan måste hoppa till säkert inträde med absolut `JMP` kostar det minst **3 till**, alltså **7 CPU-cykler** för denna *konkreta switch+JMP-kodväg*, exklusive bank-/re-entry-state, flaggor, eventuella `PHA/PLA`/`JSR/RTS` och avvikande branch. Det är INTE en generell uppmätt tidskostnad i spelet eller en ny faktisk bankswitch.
- Instruktionen **efter hotspot-accessen** avkodas redan i **målanvänd bank på samma 6507-adress**. Därför måste safe continuation/trampoline vara identiskt placerad eller medvetet återkopplad, helst under VBLANK/mellan hela rasterband – aldrig fritt antagen **mitt i en kritisk P1-START/GRP-rad**. Vektorer `$FFFA–$FFFF` ska finnas och fungera i alla startup-banker; stack/flaggar/`SCENE` måste överleva och inte förväxla RAM med ROM.
- Historiska [MAIN:s F6-bank-/minnesrevision](MAIN_F6_BANK_MEMORY_AUDIT_2026-11-15.md) anger **481-byte** tidigare identisk huvudkernel och 2048-byte tabeller per huvuddiagnostikbank, **1557 särskilt oallokerade bytes/bank** vid 2026-11-15 baseline. **Detta är en ANNAN branch/diagnostik**; blandas **inte** med F9:s 3019+115+6=3140 byte och 952 säkert fritt i sin experimentbank.
- De fyra **identiska** ROM-banker som användes i F9 är inte proof på att olika bankspecialiseringar och fortsättnings-PC fungerar vid runtime. Ett annat projekt kan komprimera statiska kart-/dataflöden i ROM men skapar **inte** nytt RAM eller en tredje 8-bitars-P1.

**Ej skalbart enligt verkliga banktal:** en naiv 16-lägesbank kräver minst **5340 byte** rasterkod, mer än 4096 per bank; sex binärlägeprofiler kräver minst **21360 byte** rasterkod för endast de tre ursprungliga maskers motsvarande F9-stil, mer än alla fyra bankers 16384, utan sexfigurskod. Sex numeriska X/Y kan inte fördelas över en ändlig profilbankkatalog.

**HARD STOP för B:** fel gemensam bank-byte-/PC-trampolin, >4KiB per resident kernel, byte- och hotspot-/reset-konflikt, bankval i samma 76-cykels kritiska rad utan uppmätt säker cykel; **och framför allt** att den residenta kärnan fortfarande inte har sex P1-START-/GRP-/Y-fönster. Bankerna levererar ROM-utrymme, inte sex fysiska X.

**EN minimal framtida separat falsifieringsgrind B:** vid uttrycklig ny auktorisation, ett enda enkelt standard-F6/NTSC-test med **två olika** bankars *identiskt adresserade* safe-trampoline och olik 9-radersgrafik-/data-kernel, och ett bankbyte **före** rasterbandet. Logga faktisk hotspot-PC/cykel, efterföljande mål-PC och bank, 262 scanlines och oförändrad P0/M0/PF i två följande frames. Misslyckad PC-övergång eller bankdata från fel bank **falsifierar bankfördelningspremissen**. Även PASS ger **ingen** ny P1-kopia, ingen fri-X/Y och ingen R1-acceptans. Bankfördelning är stöd till en godkänd A-kernel, inte kandidat som isolerat räddar sex same-Y.

---

### 7. Familj C – adaptiv NUSIZ-gruppering, Y-multiplex och eventuella VDEL/HTR/PF-hybrider

**Möjlig referens:** adaptivt `NUSIZ1=$01/$02/$03/$04/$06` för nära/mellan/långa grupper, med `GRP1`-skrivningar mellan automatkopior, plus uppdaterbar Y-plan för objekt på åtskilda rasterhöjder. Historisk R1ba `NUSIZ1=$03` visar att två par stora originalmaskbytes på liknande Y kan utnyttja kopiegrupper.

**Men huvudkravet i C04 är just SEX som kan ligga på SAMMA Y och behöva oberoende X.** Automatkopiors NUSIZ-avstånd är **hårdvarubundna**, inte sex individuellt räknade X. MAIN:s [sex-X-geometrirevision](MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md) enumererade **64 045** originalspawn-6kombinationer och fann **44 191** (69,0 % av dessa poolkombinationer, EJ spelens sannolikhet) där **inte ens ett par** låg på de tidigare provade 32/64-CC separationerna. Distinkta, rörliga X med önskat avstånd **20 CC** är en sådan konkret profil, och en auto NUSIZ-grupp kan inte fritt flytta sina två figurer med skilda hastigheter.

**HISTORISKT MOTBEVIS mot R1ba som kanon:** [MAIN:s F5/R1ba-orienteringsaudit](MAIN_V_R1_F5_RECEIPT_R1BA_VERTICAL_ORIENTATION_INDEPENDENT_AUDIT_2026-11-16.md) gick direkt mot 600 verkliga arkiv-PNG: **0/600 rättvända enligt låst top-down original**; fyra stora M/M/F/F exekverades uppochned, trots att forskarens `[::-1]`-oracle gav 600/600 mot en annan referens. Småmaskerna var rättvända, men X/Y förberedda i **tre kopplade formationer**, inte sex enskilda numeriska X/Y. R1ba är **inte** en godkänd integrationsbas och får inte repareras i F10.

**Y-multiplex:** Om två NPC aldrig har överlappande 9-radersband kan P1 återanvändas på olika scanlines, men R1 C04 innehåller medvetet både exakt samma och delvis skiftade Y, inklusive y101–104 i S3 där samtliga sex fortfarande är aktiva. Historiska Venetian 9-/18-line interleave ger **5/4 av 9 källrader** för två samtidigt; VDEL har inte återskapat full nio-radersmask i denna familj. Sexfas-flimmer gav en NPC **100/600 synliga frames**, fem följande osynliga = ungefär 10Hz på 60Hz-utgång, tidigare lokalt visuellt FAIL. En VDEL-latch duplicerar **inte** P1-scan-counter; pixelkorrigering måste visas utan att ta bort någon av nio bitmaprader. PF har 4 färgklockor per grafiskt bitsteg (20 bitar per halvskärm), kan inte automatiskt ersätta de pixel-exakta 8-bitarskropparna, och används samtidigt av bruna väggar/asymmetrisk högerdörr. P0 omfördelning strider mot låst gul player, M0 är redan projektil, M1/BL är inte 8-bitars människosprites.

**HARD STOP för C:** varje scen med ingen lämplig kopiegrupp, en NPC:s X förändrar automatiskt en annans X, fel top-down rad (R1ba), kontinuerlig 5/4-interleave eller oacceptabel mask-/färgbortfall, eller R2-nyckeln och R3-dörrens kanalbehov tränger undan NPC. C kan vara en **snabbväg i en delmängd av geometrierna**, men kan inte under nuvarande krav vara enda sex-fria-X/Y-renderern.

**EN minimal framtida separat falsifieringsgrind C:** om MAIN uttryckligen begär det, en original-SF+SM+M+F-same-Y-rad och nominella X-CC `[16,36,56,76]`, därefter ändra endast SM med +4 CC medan övriga tre kvarstår, och låt en av dem överlappa Y med en rad. Måste bevara fyra pixel-exakta top-down-masker utan någon fast X-parrelation, i samtliga nio källrader. Fungerar inte utan alternativ dynamisk retrigger/occlusion → **adaptiv NUSIZ som fristående fri-X-lösning falsifierad**. PASS är villkorat och ger inte sex, nyckel eller dörr. Inget arbete får utföras utan senare separat mandat.

---

### 8. A/B/C-beslutsmatris och rangordning

| Familj | Ursprungstrick (av 30) | Positivt redan faktiskt visat | Avgörande hård blockerare mot sex fria numeriska X/Y | En tydlig framtida falsifierande prob | Källklass |
|---|---|---|---|---|---|
| **A. Dynamisk P1-retrigger + prefetch/sort/timing** | **01,02,09,10,15,24**; 08 stöd | **F9 TRE binära** RAM-X + tre rättvända originals, 144/144 pixel | Sex fritt tidslagda kopior på same-Y inte visade; tät X/START/GRP-latch, dynamiska Y, 76 cykler och individuell 1-CC-X | **Fyra unrolled-fria** numeriska X, 4 ursprungstyper, X=[16,36,56,76], en X+3 CC och två äkta frames | **Högst forskningsvärde; NOT_PROVEN** |
| **B. Standard-F6 bankspecialiserade displaykernlar** | **14,24,21**; 27–30 ej tillåtna | Baslinje-F6 bankmatning i äldre diagnos, F9 1 faktisk 4KiB-kernel ×4 identiska banker | 4KiB resident, hotspots/PC, >5KiB vid 16 statiska profiler; ingen ny P1-/CPU-/Y-kapacitet | Två olika bankkernlar, safe trampoline före 9-radersband, exakt PC/bank/frame | **Stöd till A; NOT en fristående R1-lösning** |
| **C. Adaptiv NUSIZ + vertikal multiplex/VDEL/PF** | **01,03,04,05,08,09,15,17,19** | F9 nära kopior, äldre R1ba visade begränsad gruppmekanik (med stor-maskorienteringsfel), isolerad R3 PF | Kopplade avstånd, 69,0 % av referenspoolens sexval saknar tidigare provat kopiepar; same-Y och originalpixlar, key/door-krock | Fyra originalmasker same-Y X=[16,36,56,76] och en individuellt +4 CC | **Reserv för glesa delscener; NOT_PROVEN som full R1** |

**Rangordning:** **A först för grundforskningsvärde**, **B som sekundär kod-/datainfrastruktur när någon A-liknande verklig sechs-START-kernel är möjlig**, **C som begränsad opportunistisk optimering för vissa fördelaktiga geometrier**. Ingen av dessa får utses som **vinnande, tekniskt styrkt F6-fullarkitektur**. Kombination A+B kan fortfarande inte överbrygga en **fysisk** single-P1/GRP-överlappning. En hypotetisk C-omväg som slutar i partiell occlusion eller annat färg-/maskutseende kräver explicit designbeslut, inte teknisk genväg.

---

### 9. Explicit RIOT-RAM-kontrakt: minst 12 koordinatbyte, och ett ärligt spel-estimat

Standard RIOT har **128 byte RAM**, med stack-/zero-page-mirroring; F6 tillför ingen kassett-RAM. Endast sex individuella **X + Y** kräver minst **12 byte** med 8-bitars positioner. Det säger ingenting om att den **synliga** kerneln kan rita dem. Ett realistiskt men ännu **icke allokerat** RAM-schema, uttryckligen grov kapacitetsanalys och inte en faktisk assembler-symbolkarta:

| Ändamål | Hypotetiska byte | Löpande totalt |
|---|---:|---:|
| Sex individuella X samt sex individuella Y | 12 | 12 |
| Sex objekt-ID/typ, sex status/HP, sex animation/facing | 18 | 30 |
| Sorterad aktiv renderkö (6 index) och sex 2-byte mask-/radpekarpar | 18 | 48 |
| Sex förberedda aktuella maskbytes samt sex individuella RESP-/delayvärden | 12 | 60 |
| P0-spelare pos/tillstånd; M0-projektil pos/enable | 7 | 67 |
| Guldnyckel pos/status, dörr/rum/lås | 6 | 73 |
| PF-vänster/höger scratch | 6 | 79 |
| Frame/timer/scanline/mode counters | 6 | 85 |
| Objektkollision/ID-/händelseflaggor | 8 | 93 |
| Konservativt stackutrymme, reserverat | 24 | **117** |
| **Nominellt kvar (ej fria bytes förrän kartan har verifierats)** | **11** | **128** |

**Obs:** En mer kompakt packed type/status eller återanvänd scratch skulle kunna minska RAM; en verklig spelmotor behöver dessutom AI, rörelseriktningar, ljud, score/lives, kart-/nyckel-/dörrstate och stabil stack/JSR-disciplin och kan **öka** budgeten. Denna tabell är **inte** en färdig RAM-tilldelning, inte ett bevis att 128 byte räcker, och inte ett bevis på omöjlighet. RAM kan inte lagra 160×6 färdiga scenrader (960 B) eller skriva en ny 6507-instruktionsström in i F6-ROM. En framtida eventkö måste därför kunna streama/rulla inom 128 byte och hålla källkorrekta rader utan branch-jitter.

---

### 10. Samtliga 30 ursprungliga Atari-trick har kontrollerats, med verklig F9-status

**Det finns exakt 30 numrerade originaltrick, inte 30+52=82.** Den större teknikatlasens T-poster är korsreferenser. F9 förändrar bevisläget för #01/#02/#15/#24 från tidigare tvåmaskprov till **tre binära originalkopior**, men skapar inga nya gratis TIA-kanaler.

| Nr | Teknik | Praktisk relevans för F10, efter F9 |
|---:|---|---|
| 01 | Sprite Multiplexing | Nödvändig för skilda Y; same-Y sex kvar olöst |
| 02 | Mid-scanline GRP rewriting | Nödvändig P1-datakopia, verkligt 3× binär F9 PASS |
| 03 | Venetian Blinds | Tidigare 9/18/VDEL förlorade originalrader, inte tillräcklig |
| 04 | Sprite Flickering | Tidigare 1/6 bildsynlighet 100/600 och visuellt FAIL |
| 05 | Dynamic Playfield Sprites | Vägg-/enkelikonstöd, ej exakt NPC-kropp |
| 06 | Mid-frame Sprite Resizing | Förvränger källmask; inte fri X |
| 07 | Asymmetric Playfield | Kritisk R3-högeröppning med konkurrerande write-deadlines |
| 08 | Two-Line Kernel | Kan skjuta arbete mellan rader, får inte tappa 8×9-pixelrader |
| 09 | VDEL / Delayed Graphics | Timing/bufferverktyg, inte fler P1-kanaler; äldre negativt försök |
| 10 | HMOVE Fine Positioning | Global fin-X för P1, inte individuella kopior efter START |
| 11 | Late HMOVE | Fas-/rev-hårdvarurisk, inte sex-X-lösning |
| 12 | Raster Color Changes | Krävs potentiellt för vit P1/guldkey/orange dörr; cykelkostnad |
| 13 | 48-Pixel Score Kernel | Fixerad geometrikärna; relevanta registerfönster, inte fri-X |
| 14 | Multiple Display Kernels | B:s bank-/zon-specialisering, ingen extra rastertid |
| 15 | NUSIZ Sprite Duplication | F9 close PASS men fasta inbördes gruppavstånd i C |
| 16 | Sprite Reflection | ROM-besparing i vissa former, ändrar inte sex individuella positioner |
| 17 | Missile and Ball Reuse | M0 upptagen av skott; M1/BL har inte 8-bitars originalmasker |
| 18 | Playfield Score Mode | Färgkoppling till P0/P1 riskerar brun/gul/vit separation |
| 19 | PF Priority Switching | Möjlig O1-skymning, inte fri mask eller nyckelns logiska state |
| 20 | Hardware Collision Latches | Hårdvaru-P1 återbruk tappar enskild NPC-identitet |
| 21 | RIOT Timer Scheduling | Blankperioder/framebudget, inte fler 76 synlighetscykler |
| 22 | Stack/RAM Mirroring | Riskabel resursdisciplin; +0 RAM |
| 23 | Undocumented 6502 Opcodes | Ingen verifierad ny P1-START och kompatibilitetsrisk |
| 24 | Precomputed Tables and Cycle-Exact Kernels | Starkaste source-designstödet, men inga 160^6 ROM-profiler |
| 25 | Stack-Based TIA register tricks | Specialisering/stackrisk; ingen gratis skriv-/objektkanal |
| 26 | Timing-Based Horizontal Scrolling | Förbättrar inte sex samtidiga originalhumanoider |
| 27 | SCABS automatic bankswitch | Annan kassett, UTANFÖR standard-F6 och scope |
| 28 | Extra Cartridge RAM / Superchip / Supercharger | Annan kassett, UTANFÖR scope; räddar inte P1 |
| 29 | DPC | Specialchip, UTANFÖR scope; ingen fri 8-bitars-TIA-player |
| 30 | DPC+/CDF/ARM | Coprocessor/ny mapper, UTANFÖR scope; renderingens TIA-CC kvar |

**Särskild välkontrollerad slutsats:** #02/#15 fungerar som tre kopior i F9, medan #24 ger nödvändig statisk cykelprecision. F10:s egentliga olösta problem är **den dynamiska per-rad-kopiebokningen när alla sex X/Y får ändras oberoende**. Historiska effekter från andra spel är inspirations-/reproduktionskällor, inte redan godkända svar. Ingen ny waiver för 9-raders, flimmer, färg eller antal NPC finns.

---

### 11. MAIN V:s återstående beslutsgrind, separat framtida mandat och formellt STOPP

**F10:s source-only-arkitekturbeslut: `NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN`.** Ingen av A/B/C är tekniskt styrkt över ALLA S1–S5 med strikt originaldesign. A är det mest lovande **undersökningsspåret**, med en liten *villkorlig* fyra-NPC-ramprob som kan falsifiera dess grundläggande 4:e numeriska X-START-/GRP-deadline, men det är **inte** en vinnande sex-X/Y-arkitekturplan.

**Två möjliga MAIN-beslut efter mottagningen, inget utfört av F10:**
1. **Behåll samtliga låsta spel-/grafikkrav och standard-F6:** bevilja eventuellt en NY, separat och minimal teknisk auktorisation för *A:s enda falsifierande fyrmaskprobe* (först efter MAIN:s egen analys av denna rapport). Om den faller krävs ytterligare source-/hårdvarubeslut; ingen automatisk variant- eller fasräddning. Om den lyckas krävs nytt MAIN-uppdrag för sex, fri Y, 600-frames C01/C04/B02, nyckel/O1 och dörrintegration; **ingen automatisk F11**.
2. **Om ett framtida verkligt worst-case-fel visar sig oåterkalleligt:** återrapportera teknisk blockerare och be **användaren** om ett explicit, prioriterat design-/hårdvarubeslut, t.ex. policy för 8-pixels NPC-överlappning/occlusion, minsta visuella separation, accepterad flimmerandel, sprite-allokering för dörr/nyckel eller byte av cartridgeformat. Detta är **inte** F10:s rätt att införa sådana ändringar: en ändrad mapper, reducerat antal/förenklad figur, frisläppt P0 eller svart keyhole-skippning är nya scopes/waivers som måste godkännas uttryckligen.

**Vad MAIN inte får tillskriva denna rapport:** en verifierad sex-START-kernel, en dokumenterat tillräcklig 76-cykelplan för sex godtyckliga samtidiga X, faktiskt RAM-/bankintegrerat spel, fungerande same-Y dense/cross/shifted-Y, självständig Verification eller källa/build/ROM efter F9. Krav E02/V0.18 är **fortfarande öppna**.

**HÅRT STOPP:** Endast den här nya Markdown-filen på en ny isolerad F10-source-only-gren från `c36982aef770af6cd3f68c2da37b8ed14aee2393`; formell handoff i [Issue #6](https://github.com/Odourman/let-me-out/issues/6), därefter STOPP. **Ingen** F11, ny assembler, DASM, ROM, Stella, CI, Python-test, ZIP, PNG, bank-switch-kod, R1ba-reparation, fjärde kopieprob, grafik, PAL, F6SC/ARM, R2/R3/R4, fullspel, PR #7-merge eller oberoende VERIFICATION Issue #8 utan ny separat uttrycklig MAIN V-auktorisation.

**Full R1: `BLOCKED / NOT ACCEPTED`.**
