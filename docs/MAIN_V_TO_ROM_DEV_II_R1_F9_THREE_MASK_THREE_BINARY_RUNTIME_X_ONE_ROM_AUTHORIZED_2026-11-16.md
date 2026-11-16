# LET ME OUT! – MAIN V till ROM DEVELOPMENT II
## R1-F9 – EN standard F6/NTSC ROM: 3 korrekta NPC-masker, 3 separata BINÄRA RAM-X, 8 tillstånd

**Datum 2026-11-16. NY, SEPARAT, EXPLICIT MAIN V-AUKTORISATION** inom användarens befintligt godkända tekniska v0.18 R1/NTSC/F6-diagnostik [Issue #6](https://github.com/Odourman/let-me-out/issues/6). Detta är **en mycket avgränsad hårdvarusondering**, INTE fullspel, ny R1/6-NPC-kernel, designwaiver, godtyckliga numeriska X, fri Y eller oberoende Verification. **HÖGST EN (1) NY KÖRBAR 16 384-byte F6-ROM**, aldrig flera geometrier eller fassvep. Hårt stopp efter rapport. **Ingen automatisk F10.**

### 0. Verifiera styrande projektkällor själv innan ändring

1. Läs [MAIN V:s F8-mottagning/oberoende källberäkning](MAIN_V_R1_F8_SOURCE_ONLY_RECEIPT_AND_F9_DECISION_2026-11-16.md), den [FRYSTA F8-rapporten](https://github.com/Odourman/let-me-out/blob/5c5e603482be7be482eaf8eae5ba317d91087b3d/docs/ROM_DEV_R1_F8_THIRD_BINARY_X_SCALING_SOURCE_ONLY_TO_MAIN_2026-11-16.md) och exakt F7-bas `c8dc8b35f4bb652e3920b70882f8cc1fb84125d3`, F7 [TO_MAIN](https://github.com/Odourman/let-me-out/blob/c8dc8b35f4bb652e3920b70882f8cc1fb84125d3/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F7.md). Skapa **NY isolerad F9-branch** från just frysta F8 `5c5e603482be7be482eaf8eae5ba317d91087b3d`; endast NYA `r1_f9_*`-filer/workflows och `TO_MAIN_R1_F9.md`, inga tidigare F2–F8 filer, `main`, PR#7 eller research-GRAPHICS ändras.
2. Läs och pinna `design/NPC_REFERENCE_8x9_masks.json` Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; top-down masker EXAKT:
   - `large_male: 3C 3C 18 FF 18 24 24 42 42`
   - `large_female: 3C 3C 18 FF 3C 7E 7E 24 24`
   - `small_male: 00 00 3C 3C 18 7E 18 24 00`.
   Den tredje maskens top-down rader 0/1/8 är faktiskt **NOLL** och får INTE klippas, komprimeras, flyttas eller ignoreras. Ingen `[::-1]` eller R1ba-spegling, inga extra figurer.
3. Läs aktuell `docs/CURRENT_PROJECT_STATE_2026-11-15.md`, bindande [`ROM_GATE_V018_ACCEPTANCE.md`](ROM_GATE_V018_ACCEPTANCE.md), sex-NPC [kravet](MAIN_SIX_INDEPENDENT_X_V018_2026-11-15.md). PR #7 ska förbli **OPEN/DRAFT/UNMERGED**, Issue #8 VERIFICATION standby. P0 gul, M0 statiskt skott, bruna PF på båda sidor, NUSIZ1=`$01`, standard 262 NTSC/HMOVE/VBLANK. Ingen R3-högeröppning, HUD, KEY, GAME OVER, PAL eller fullspel.

### 1. EN enda F9-testfråga och exakt registrerad 2×2×2-sanningstabell

Kan **samma ENDA F6/NTSC-ROM**, med **separat verkligt lagrade, oberoende RAM-bytes** `X0_SELECT=$A0`, `X1_SELECT=$A1`, `X2_SELECT=$A4`, producera alla **8** kombinationer av tre rättvända original-NPC-X med **enbart** de förregistrerade `RESP1`/GRP1-faserna? Alla tre använder en enda fysisk P1 på samma **nio** rasterrader och måste förbli synliga och källkorrekta. **X2 är ENDAST en oprövad fassvars-hypotes**.

| RAM-bitar X0X1X2 | M/F/SM RESP1, CPU c | M/F/SM GRP1, CPU c | Hypotetiskt förregistrerat (M,F,SM) i 900×300 Stella-crop |
|---|---|---|---|
| 000 | c21 / c32 / c48 | c24 / c35 / c51 | **(39,99,195)** |
| 001 | c21 / c32 / c50 | c24 / c35 / c53 | **(39,99,207)** |
| 010 | c21 / c33 / c48 | c24 / c36 / c51 | **(39,105,195)** |
| 011 | c21 / c33 / c50 | c24 / c36 / c53 | **(39,105,207)** |
| 100 | c23 / c32 / c48 | c26 / c35 / c51 | **(45,99,195)** |
| 101 | c23 / c32 / c50 | c26 / c35 / c53 | **(45,99,207)** |
| 110 | c23 / c33 / c48 | c26 / c36 / c51 | **(45,105,195)** |
| 111 | c23 / c33 / c50 | c26 / c36 / c53 | **(45,105,207)** |

**Ingen efterhandsförändring av X-prediktioner, c48/c50 eller andra tidigare två X-faser.** En alternativ fysisk position kan beskrivas som faktisk geometri och avvikelse, men får inte benämnas förregistrerat FULL-LOCAL-PASS om de numeriska målen missades. Särskilj position-PASS från START-proveniens-hypotes och från uppgifter om godtyckliga fria X.

### 2. G0 – OBLIGATORISK källgrind INNAN ny ROM eller DASM

Skapa endast F9-namngivna analys-/källskript på nya branchen; **kör först source-only G0, INGEN ny ROM innan det**. Utgå från verkliga frysta F7 `.asm/.lst/.sym` och låsta F8 pappersmatriser, inte enbart F8-slutklass:
- Redovisa **72 explicita per-row/per-state 6502-uppställningar**, även alla SM nollrader. Exakta första två P1-faser c21/c23 och c32/c33 oförändrade; tredje SM-fas endast c48/c50. Bekräfta `STA GRP1` för SM först efter F:s sista synliga pixel (inte enbart efter `STA RESP1`), före SM:s egna 8 pixelstartar; på grund av intern TIA-latch är detta en förregistrerad hypotetisk fysisk grind.
- Verifiera att alla åtta 9-radskernels exekverar max **76 6502-cykler/rad**, även rad8 med `JMP` och `WSYNC`, noggrant föregående och efterföljande scanline och övergångsloop. Förregistrerat källmål: `WSYNC` rad0–7 **c54/c56**, sista rad8 **c57/c59**, marginal min **17**, annars `F9_G0_FAIL_NO_ROM`.
- Kontrollera bankutrymme mot **verklig** F7 .lst/.sym och framtida kod: exakt **en 4KiB kritisk F6-bank** och 16KiB standard-ROM. En särskild **128-byte övre reserv** för ny selector-/init-/dispatchkod var bara F8:s uppskattade plan; `3 108` bytes programutrymme är **inte ett garanterat faktiskt compilat**. Om branch/JMP-räckvidd, relocation från gamla `ORG $F800` till t.ex. `$FE00`, RIOT RAM eller data-/vektorkollision gör att verklig byggning inte får plats, STOPP utan att ge dig själv rätt att byta mapper, banka mitt i synlig kernel eller skapa alternativ X-mönster.
- Använd **TRE faktiskt separata RAM bytes** `$A0/$A1/$A4`, var och en separat ändringskontrollerad `CMP/STA`, ingen enda `modeID`-proxy. Kontrollera 8 Gray-lägen `000→001→011→010→110→111→101→100→000`, en bit ändras per steg, 16 frames per på varandra följande steg. Förbered uppdatering och dispatch under redan tillgänglig VBLANK/TopBlank utan extra rasterrader; skilj G0:s source-cykler från framtida GUI-trap.
- Kontrollera P0/M0/PF/HMOVE, 262 NTSC, eventuella extra P1-kopior vid följande scanlines (TIA main wrap), särskilt om tredje `RESP1` på CC144/150 stör nästa rads första `RESP1` CC63/69. Det är en **faktisk framtida STOPP-risk**, inte en källbevisad "kommer aldrig hända".

**HÅRD G0 STOPP:** Om någon 8×9-kodsekvens, RAM-väljare, GI/ASM-layout, registerdeadline, kopie-fysiska förutsättningar eller källbudget misslyckas, rapportera `F9_SOURCE_ONLY_INFEASIBLE`, bygg **INGEN** ROM. Ingen andra kandidat, ingen NUSIZ-$03 eller R1ba-kodportning.

### 3. G1 – ENDASTA EN ny 16KiB F6/NTSC-ROM, autentiska Stella-traps och 8-läges-pixeltest

Efter fullständig G0 PASS: bygg **max EN** faktiskt exekverbar **16 384-byte** standard F6/NTSC-ROM, 4×4096 identiska banker enligt F7-mönstret. Frys SHA-256 för ROM **före** Stella. Ingen andra binär ens om den första har fel. Inga omkompileringar eller breda fassvep; verifiera att alla originalmasker och första två RAM-X F7-schedules är byte- och top-down-korrekta.
- Kör i äkta **Stella 6.7.1**, en enda ROM. Spara **minst 16 efter varandra följande autentiska frames per var och en av Gray-sekvensens NIO 16-frame-steg**, således **minst 144 olika verkliga frameindex** totalt, med 8 unika RAM-lägen och return `000`. Vid tidiga allvarliga sprite-/scanline-/timingfel: **STOPP**, bevara redan insamlad evidens, ingen recovery-ROM.
- Kräv för varje positiv frame en **separat source-canon-top-down 3-mask-pixelunion** i hela relevant x0–335,y50–194 samt **rad-för-rad 8-bitars maskoracle**, som aldrig baseras på en R1ba-`[::-1]` eller utvecklarens egen posthoc förväntansbild. Båda originalstor M/F och liten SM i **exakt nio** positioner y96..104, den lilla med synliga rader2–7 och frånvarande pixlar rader0,1,8. **0 extra/0 missing** vita pixels per frame, alla 3 faktiska X motsvarar förregistrerad 8-radig tabell.
- Automatisk **minst tolv (3×4) logiska oberoende X-kontraster**, var och en jämför en valbit medan de övriga två är låsta. Testa varje bit i vardera kombination av andra bitarna. Dessa måste ge exakt (6,6,12) Stella-crop-pixlars byte-gating för respektive man/kvinna/liten man; andra två X måste vara pixelidentiska i jämförelseparen. Även verifiera faktiska sekventiella en-bitförändringar och RAM A0/A1/A4.
- Spara **reella PC/bank/scanline/CPU-cycle/TIA CC debug-GUI registerbilder** för var och en av **tre RESP1 och tre GRP1** i **alla åtta RAM-lägen** (mål 48 riktiga trapbilder), plus GUI-minnesvy av `$A0,$A1,$A4` med värden, full GUI-screenshot av varje autentiskt frame och 262 NTSC/WSYNC efter-kontroll. Alla cykelvärden som bara kommer från assemblern ska uttryckligen märkas **STATIC_ONLY**. Register-traps är CPU-skrivningar, inte interna TIA START-latchsignalbevis.
- Bevara gul P0, statisk M0, brun PF, pixelrader och NTSC-scanlines. Spara ett separat **SYNTHETIC_NEGATIVE_NOT_REAL_STELLA**-exempel (vändighet eller en pixel) som BÅDA validerarna avvisar. Om småmasken syns men gammal M/F rör sig eller spöken visas på nästkommande rad är detta **FAIL**.
- Fryst reproducerbart bevispaket i riktig Drive projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`, innehåll: enda `F9.bin`/SHA/fyra banker, ASM/.lst/.sym, G0 source-tidstabeller och faktiska bygginstruktioner, 144+ verkliga crop och full GUI PNG + per-frame index/objektfärg/NTSC, 48 märkta autentiska registertrapbilder om målet kan nås, syntetiskt negativt separat, bit-/pixelpositioner JSON med alla 12 oberoende kontraster, SHA256SUMS och per-file index, ZIP CRC PASS, GitHub Actions-IDs även RED.
- En följande read-only återanalys av de ursprungliga redan insamlade ROM-screenshots är tillåten utan ny rom/grafindata för att rätta externa läsfel **endast om originalbevis och prediktionsmål står frysta**. Skilj rådatafel från verifieringskodsfel öppet som F7. MAIN/VERIFICATION ska kunna läsa allt utan att utvecklarens audit måste tros på förhand.

### 4. Gränser, klassificering och HÅRT STOPP

Rapportera `F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS` ENDAST vid faktisk åttahörns-/tolvkontrast-ORTHOGONALITET, tre exakt top-down källmasker, en ROM, alla registrerade X och intakt P0/M0/PF/262. Annars en tydlig `F9_SOURCE_ONLY_INFEASIBLE`, `F9_THIRD_COPY_OR_ORTHOGONALITY_LOCAL_FAIL`, `F9_PREDICTION_MISMATCH` eller `F9_INCONCLUSIVE`. Ingen gynnsam etikett för source-only, delvis synlig SM eller lägesstyrda PAR-profilformationer. **Ett positivt F9 är fortfarande bara tre oberoende BINÄRA X-väljare, inte tre valfria numeriska X eller sex fria X/Y, och INTE full R1.**

**STOPP efter EN rapport:** `rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F9.md` på isolerad ny F9-branch, handoff i Issue #6; ingen F10, fjärde sprite, sex-NPC, NY kernelarkitektur, P1-NUSIZ-mappexperiment, gameplay-key/GAME OVER/HUD, R1+R3, R2/R4, PAL/F6SC/ARM, PR #7 merge, canon-ändring, nya GRAPHICS-versioner eller oberoende Verification Issue #8. Allt kräver separat, senare MAIN V-beslut och i den mån det överskrider användarens tidigare godkända F6/NTSC R1-diagnostik även uttryckligt nytt användarscope.

**Full R1: BLOCKED / NOT ACCEPTED** oavsett F9-resultat.
