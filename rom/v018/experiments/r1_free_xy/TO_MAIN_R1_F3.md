# LET ME OUT! – ROM DEVELOPMENT II till MAIN V
## R1-F3 – Two Independent Runtime X Controls: avslutande reproducerbar rapport

**Datum:** 2026-11-16  
**F3_SECOND_INDEX_GEOMETRY:** **FAIL** för den enda byggda och faktiskt körda index0 +1-CPU-cykel-varianten, 16/16 autentiska Stella-rutor. Inget påstående om att alla andra offsets eller index är omöjliga.  
**F3_TWO_INDEPENDENT_RUNTIME_X:** **INCONCLUSIVE / NOT_RUN** – den bindande stoppgrinden utlöste innan ett tvåindividers runtimeförsök var tillåtet. Ingen F3-runtime-ROM har byggts.  
**FULLT R1:** **BLOCKED / NOT ACCEPTED**; sex individuellt fria X/Y inte visade.  
**Evidensnivå:** endast ROM DEVELOPMENT / GitHub Actions **DEVELOPER_LOCAL**, ingen separat oberoende VERIFICATION.

### 1. Exakt källa, auktorisation och oförändrade gränser

MAIN V:s bindande [R1-F3-arbetsorder](https://github.com/Odourman/let-me-out/blob/main/docs/MAIN_V_TO_ROM_DEV_II_R1_F3_TWO_INDEPENDENT_X_RUNTIME_FEASIBILITY_AUTHORIZED_2026-11-16.md) gäller bara diagnostik på NTSC v0.18 i Issue #6. F3-branchen skapades **från exakt fryst F2-commit 485a6c10047fb9b41e589ac3df724c1bc70f0283**:

- F3-gren: **rom-dev/v018-r1-f3-two-independent-x-20261116**. GitHub compare mot F2 visar enbart nytillagda F3-skript, CI-yaml och denna rapport. Original R1, F1, F2, R3, main och draft PR #7 är orörda.
- F2:s redan accepterade enindividers runtime-ROM är oförändrad: **16 384 byte**, SHA-256 **941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b**. F2-index2 kan växla x129↔135 med en och samma kernel; detta har **inte** gått förlorat och **inte** kompletterats med index0-styrning.
- Bas-6B-ROM: SHA-256 **36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4**. Ursprungsmasker i design/NPC_REFERENCE_8x9_masks.json, Git blob **058800a4c1904d1ff289e7e61b3902aa111ba16d**.
- Masktyper per explicit källindex: **0=large_male, 1=large_male, 2=large_female, 3=large_female, 4=small_male, 5=small_female**; inga ändrade bitmapbytes.
- Ubuntu 24.04 GitHub Actions, DASM motor **2.20.14.1** (paket 2.20.15~20201109+really2.20.14.1-2), **Stella 6.7.1** (paket 6.7.1+dfsg-1build2), Pillow 10.2.0. Normal F6 16 384 bytes: fyra byteidentiska 4 KiB-bankkopior, bank 0 under rasterkerneln.
- Förbjudna saker såsom R2/R4/Y-expansion, R1+R3-dörr, PAL, ny mapper, fullspel, 600-frame-prov och oberoende VERIFICATION har **inte** påbörjats.

### 2. F3-G0 – source-only envelope före den enda ändringssonden

Befintlig F2-kernel har 9 utrullade bitmaprader och alla sex P1-maskerna på samma rasterhöjd; P0=gul originalspelare, M0=aktivt skott, PF=bruna väggar och NUSIZ1=$01 (källbaserad Reset-init). Registren Y och X är inte annars nödvändiga inne i nio-raderskärnan utom den redan existerande F2:s CPX-test på index2. Detta motiverade den av MAIN föreslagna CPY-hypotesen för index0.

**Den enda byggda geometriproben** ersatte i samtliga nio maskrader den ursprungliga index0-sekvensens två NOP och BIT FRAMELO med:

    CPY #0
    BNE *+2
    STA RESP1      ; index0
    STA GRP1
    BEQ *+2
    STA RESP1      ; index1, kompenserad tid

I just G0 sätts Y=1 och X=0 före källrad00: första RESP1 ska bli **c20 i stället för 6B:s c19** och index1 ska förbli **c28**. Den separat accepterade F2-kontrollen index2 hålls i sitt basläge **c37/X=129**. Konditionella 6502-grenar här har taken/not-taken 3/2 cykler, med en **kompenserande** 2/3-kombination så klockan inte driver vidare för index1–5.

**Teoretiskt**, inte verifierat som fysisk X: +1 CPU-cykel motsvarar +3 TIA color clocks = +6 pixlar i 900×300-debuggercrop. Därför valdes:

- Begärt för index0: **x49**; basvärde **x43**.
- Begärt för övriga fem index1–5: **x75,129,183,243,303**, exakt original 6B.
- För de nio raderna är inlastade P1-originalmaskbytes, P0, M0, PF och övriga fem RESP-skrivningar oförändrade; inga extra P1-masker.

**Denna källcykelberäkning är inte ett PASS** och orsaken till den uteblivna pixelrörelsen får inte härledas enbart från antalet lediga CPU-cykler.

### 3. Autentiska Stella-pixlar – reproducerbar första-grinds-FAIL

En enda kompilerad G0-ROM: **r1_f3_6B_I0_P1_I2_FIXED_F6.bin**, exakt **16 384 bytes**, SHA-256:

**1ed9cd9f735dcbf4cd2dc731da607d84a9c4f85f3c894a4dbd48d2d3fc50c286**

Samma F2-källor byggdes rent och kontrollerades med pinned F2 SHA innan F3-proben byggdes. DASM returnerade success, och emulatorn fångade **exakt 16 följande autentiska råbildrutor** (frame-label 11–26) på denna ENDA F3-geometry-ROM.

| Källindex | Originalmask | Begärt F3-G0 X | Faktiskt renderat X, alla 16 PNG |
|---|---|---:|---:|
| **0** | large_male | **49** | **43 – FAIL: ingen förflyttning** |
| 1 | large_male | 75 | 75 |
| 2 | large_female | 129 | 129 |
| 3 | large_female | 183 | 183 |
| 4 | small_male | 243 | 243 |
| 5 | small_female | 303 | 303 |

Koordinater är **Stella-debuggercropens dubbelupplösta pixlar**; 2 crop-pixlar per TIA-color-clock. Källa och pixelmatcher identifierar varje masktyp och samtliga **nio källrader**, med **0 källmaskpixelavvikelser per figur och rad i 16/16 PNG** när de jämförs mot de faktiskt observerade start-X. Ingen fysisk extra ghostmask uppträdde; det strikt begärda X-testet FAIL eftersom index0 inte flyttades.

**Bevarade kontroller i alla 16:** gul original-P0, aktivt M0, bruna PF-väggar och Stella-debugger-HUD **262 NTSC-scanlines**. Inga byten av sex originalmasker, inga maskrader har avlägsnats. Klassningen 16/16 "maskerna korrekta" är **inte** 16/16 positions-PASS.

Det strikta analysprogrammet beräknade för begärt x49, jämfört med synligt x43, **38 saknade och 38 extra vita positioner i DIFFERENSMODELLEN**; det är en **6-pixlarspositionsdiskrepans**, inte fysiskt extra vita ghost-pixlar. Alla sex grupper är källkorrekta när de matchas vid faktiskt x43. Detta är den avsedda positionsgrinden som nu ger rött.

**Original-G0 CI-run är RÖD:** [GitHub Actions 43929134626](https://github.com/Odourman/let-me-out/actions/runs/43929134626). Detta är ett verkligt FAIL för testat geometryoffset. Testet avbröts efter 16 faktiska skärmbilder; G1-runtime startades **inte**.

### 4. Verklig TIA-CPU/PC-registermätning och kvarvarande orsak

G0 sänder **i verkligheten** de avsedda P1-registerskrivningarna på vald källmaskrad **05 = Stella scanline 123**, frame12, bank0. Den tidigt automatiskt infångade screenshoten för första RESP1 blev svart vid Xvfb-start och **underkändes som bevis**; den enda riktade och GUI-validerade omtagningen gav den verkliga c20-träffen:

| Registerhändelse | Faktiskt uppmätt CPU-cykel | Verkligt PC efter STA | Bevis |
|---|---:|---|---|
| **RESP1, index0** | **20** | **$F1D1** | Stella trap efter GUI-omtagning; frame12, scan123, bank0, A=$24, Y=$01, X=$00, color clock60 |
| **GRP1, index0** | **23** | **$F1D3** | Stella trap, A=$24 |
| **RESP1, index1** | **28** | **$F1D7** | Stella trap, A=$24 |
| **RESP1, index2** | **37** | **$F1DF** | Stella trap, A=$7E |

Baseline 6B:s första RESP1 var **c19** på samma källrad enligt F1:s tidigare autentiska trap, alltså är ändringen **c19→c20 bevisligen exekverad**. Index1/2 är kvar c28/c37. Source/DASM visar att resterande index3/4/5 hålls c46/c56/c66; **dessa tre återtrappades inte** i den stoppade F3-sonden, men är byteidentiska i den kritiska sekvensen och positionerna är fysiskt oförändrade. GRP1:s sista c69 och WSYNC cirka c72/76 är **statiska** tal från samma nio-radersinstruktioner, inte nya F3 worst-case-traps. 76-cykelgränsen har **inte** uppmätts i ett fullt tvåindividers runtimeprogram, eftersom något sådant inte har skapats.

NUSIZ1=$01 och tidigt HMOVE under blankning följer oförändrad fryst bas/assembler och tidigare F1-kontroller; **ingen falsk ny init-trap påstås**. Även med riktig c20/c23 kan den ursprungliga masken visuellt stå kvar på x43. Detta avgränsar felet till sambandet mellan P1-reset/kopieplacering och verklig renderad position i detta schema; den inre hårdvaru-/emulator-kopieeffektens exakta orsak har **inte ytterligare isolerats**. Det är **inte** bevis att det är generellt omöjligt att flytta index0 via varje annat offset eller P1-schema.

Den andra, tidiga indexkandidaten **index1** granskades endast källmässigt: dess nominella RESP1 ligger vid c28, med index2 tätt vid c37/c38 och balansbehov före tredje stroben. Något pixelprov eller annan kodfamilj för index1 har **inte** byggts, eftersom den hårda initiala G0-geometristoppgrinden redan utlösts.

### 5. Två kodmässigt oberoende pixelgranskare och fyra negativa mutationer

R1 har historiskt haft ett sträng/heltal-auditfel; F2 hade ett felaktigt frame/RAM-fasantagande. F3 har därför två parallella valideringsprinciper i [r1_f3_audit.py](r1_f3_audit.py):

1. Befintliga källmask-/index-/nio-radersgruppen i r1_f2_checker.py, inklusive verklig P0/M0/PF och exakt Stella-HUD 262.
2. Separat direkt jämförelse av alla vita P1-pixlars **fulla union** med den förväntade 8×9-origincanon-rastern; en avvikelse som flyttar, suddar, lägger till eller återanvänder fel x-position avvisas.

Där G0-proben inte klarade positionsgrinden kördes de fyra **mutantnegativerna enbart mot befintliga SHA-kontrollerade, källkorrekta autentiska F2 6B-baslinjebilder**, alltså **utan en enda ny emulatorframe**. Read-only CI [43929551642](https://github.com/Odourman/let-me-out/actions/runs/43929551642) är **GRÖN**: två checker-vägar godkände samtliga 16 ursprungliga riktiga bildrutor och de konstruerade kopiorna avvisades på alla fyra sätt:

- Erase: borttagen vit källmaskpixel.
- Ghost: två extra vita pixlar vid vänsterkanten.
- Stå-still: flyttning av en mask som skulle förbli på samma X, index1.
- Frame-/RAM-fas: avsiktligt förväntat fel index0-läge för en annars korrekt autentisk pixelbild.

Alla manipulerade bilder är fysiskt märkta **SYNTHETIC_TESTDATA_NOT_STELLA** och levererade i separat katalog. Ingen mutantbild presenteras som äkta Stella-råbild. Detta gröna verktygsprov **gör inte** den verkliga röda F3-G0 till PASS.

### 6. Fyra-kombinationsmatris – endast planerad, INGEN G1-exekvering

Arbetsordern kräver fyra oberoende runtimekombinationer **endast om den tidigare geometrigrinden PASS**. Eftersom +1 index0 faktiskt inte flyttade masken stoppades F3 innan runtime-ROM. Följande är därför **begärda, hypotetiska X-värden, EJ demonstrerade i F3**:

| Planerat (index0_mode,index2_mode) | Begärt index0 X | Begärt index2 X | Autentiska F3 G1-bilder |
|---|---:|---:|---|
| 00 | 43 | 129 | **NOT_RUN** |
| 01 | 43 | 135 | **NOT_RUN** |
| 11 | 49 | 135 | **NOT_RUN** |
| 10 | 49 | 129 | **NOT_RUN** |

RAM-lägena för en hypotetisk F3-G1 beskrivs på källnivå i [r1_f3_build.py](r1_f3_build.py): **$83=F3_X0_MODE**, **$84=F3_X2_MODE**, tänkt självständig lagring från olika FRAMELO-bit3 respektive bit2, med en Gray-sekvens 00,01,11,10. Denna runtimekod har **INTE** byggts eller körts och får inte räknas som evidens för två faktiskt individuellt skrivbara styrningar. Den enda nya körbara F3-ROM som skapades är G0-diagnostiken enligt punkt 3. F2:s redan frysta enindividers runtime-ROM är fortsatt den enda visat fungerande RAM-styrda implementationen.

**Inga 4 per-state F3-runtime-bilder finns**, och inga har påståtts finnas. Att fylla matrisen med F2-bilder eller självsyntetiserade bilder skulle bryta mot arbetsordern.

### 7. Evidenspaket, hash och reproduktion

Alla fyra nedanstående filer ligger på projektets befintliga dedikerade Drive-mapp; deras metadata (byteantal och folder-ID) är lästa tillbaka efter uppladdning. ZIP CRC och SHA-256 har kontrollerats. All autentisk F3-screen evidence ligger i 16-rutorspaketet respektive små tillhörande registertraces:

| Paket | Byte | ZIP SHA-256 | Status |
|---|---:|---|---|
| [16 riktiga G0-Stella-bilder, G0 executable, assembler/list/sym och per-PNG SHA](https://drive.google.com/file/d/15mEW912Scoyjt0R8w5d4OT5xDNB-vIGi/view) | 152 488 | **f3cf50fecdcf162131f5c7149206e7799ffcee5d2cbc69299027936a5196238e** | G0 16/16 **position FAIL** |
| [Stella source-row05-traps; första startupbild svart, tre övriga riktiga](https://drive.google.com/file/d/1c2rgDld35oPj9_Y2PPEihe7dOHFJZMro/view) | 77 167 | **ee298a6b384066d3fd1760a50d2528eb6e5667b6dfae71e94094b22b9cd9d95a** | Cycles 23/28/37 mätta |
| [En enda autentisk omtagning av RESP1 c20, skärmbild + loggar](https://drive.google.com/file/d/1GOpFrrndtEro4u94m8DTklOJH4x7wMXD/view) | 25 813 | **81b08bf18e0aa18a5b42af5a9d949dce8419bbf9dfa5c8b7cdf7df1b24eb11c6** | Cyclic c20 + PC mätt, startup-artefakt hanterad |
| [Fyra MUTANT-negativer och 16 genuina F2-baslinjer re-audit, NO emulator](https://drive.google.com/file/d/1vLFnCiu8rK4kdz91gkJ-rm7Gef2Per6Y/view) | 46 446 | **caa2179d93d7a08b8c7121abf63cd311103a0182be907188261b61f352362653** | Validator **PASS**, ej F3 geometripass |

Samtliga **16 rå-PNG:er** i första arkivet är bytevis SHA-verifierade mot inkluderade RAW_PNG_SHA256SUMS.txt; ZIP CRC är godkänd. Källfiler för minimal F3-G0 är [r1_f3_build.py](r1_f3_build.py) och [r1_f3_capture_g0.sh](r1_f3_capture_g0.sh). Mätning: [r1_f3_trace_g0.sh](r1_f3_trace_g0.sh) och [r1_f3_g0_first_resp_retry.sh](r1_f3_g0_first_resp_retry.sh). Negativkontroll: [r1_f3_validator_readonly.py](r1_f3_validator_readonly.py).

**Reproducerbar kommandoföljd** på fryst F3-gren (eller exakt detta report-commit) med DASM 2.20.14.1 / Stella 6.7.1, från rom/v018/experiments/r1_free_xy:

    /usr/bin/python3 build_six_sweep.py
    /usr/bin/python3 r1_f2_build_runtime.py
    printf '%s  %s\n' 941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b dist/r1_f2_6B_I2_RUNTIME_F6.bin | sha256sum -c
    /usr/bin/python3 r1_f3_build.py
    printf '%s  %s\n' 1ed9cd9f735dcbf4cd2dc731da607d84a9c4f85f3c894a4dbd48d2d3fc50c286 dist/r1_f3_6B_I0_P1_I2_FIXED_F6.bin | sha256sum -c
    bash r1_f3_capture_g0.sh
    # KOMMANDOT OVAN SKA SLUTA FAIL: x49 begärt, x43 observerat.
    # Valfri endast läsande komplettering (utan annan ROM variant):
    bash r1_f3_trace_g0.sh
    bash r1_f3_g0_first_resp_retry.sh

Detta ger **avsiktligt röd** G0-check och riktiga screenshots från denna exekvering; reproduktionsskriptet skapar inte någon G1-ROM. De historiska F2 originalen används endast i separat read-only auditor-run.

**GitHub Actions**:
- **43929134626: FAILURE** – genuin utebliven X-rörelse, testgrind röd, men alla 16 reala PNG insamlade.
- **43929434607: SUCCESS** – läsande 4-registertraps (inklusive första startup-black som räknades bort).
- **43929551642: SUCCESS** – SHA-kontrollerade F2-bildbytes, båda auditvägarna + 4 avsiktliga fel, **ingen Stella**.
- **43929951068: SUCCESS** – en läsande GUI-validerad omtagning av första RESP1 c20.
Röda testet har **inte** suddats bort genom en efterhandsjustering av förväntat X.

### 8. Stoppbeslut och rekommenderat nästa beslut (ej auktorisation)

**F3_SECOND_INDEX_GEOMETRY_FAIL:** G0:s enda index0 +1-cykelkontroll träffar verkligen rätt CPU-register/cykel men ger ingen ändrad faktisk maskposition. Samtliga sex masker är intakta på sina gamla X. Sondens strikt begärda position FAIL i 16/16. Ingen andra kompilerad offset och ingen ny annan index-arkitektur startades, helt i linje med stoppregeln.

**F3_TWO_INDEPENDENT_RUNTIME_X_LOCAL_INCONCLUSIVE (NOT_RUN):** Inget data från två samtidigt och logiskt oberoende RAM-kontroller, ingen körbar två-X-runtime-ROM eller fyra tillstånd finns. Det är inte en dold G1-FAIL-kampanj, utan ett korrekt stopp före det prov som annars skulle följt efter G0-PASS.

**FULL R1 BLOCKED / NOT ACCEPTED.** Fortfarande ej sex individuellt fri X/Y, varierande Y, nära/överlappande maskpositioner, 600 fria frames, R1+R3, full T01–T16 eller oberoende VERIFICATION.

**Ett möjligt separat nästa MAIN-uppdrag (INTE utfört/auktoriserat nu):** Undersök den tidiga index0-kopians faktiska TIA close-copy-fasrespons (c19/c20 och förhållande till andra RESP1 c28) med en mycket liten tvåpunktsmätning eller ett tidigarelagt (-1)-offset; alternativt en strikt källbaserad index1-fasförstudie. Innan en andra runtime-X byggs krävs först **fysisk maskposition ändrad med alla fem andra orörda**, inte enbart en ändrad skrivcykel. Sluta på första falsifierande pixelprov.

**ROM DEVELOPMENT II avslutar R1-F3 inom den hårda grinden och avvaktar separat MAIN V-beslut.**
