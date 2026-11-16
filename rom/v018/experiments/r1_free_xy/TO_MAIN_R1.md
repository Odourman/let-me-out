# LET ME OUT! – ROM DEVELOPMENT → MAIN V

**R1: sex individuellt X/Y-positionerbara originalandroider, NTSC v0.18**  
**Utvecklaregenkontroll, 2026-11-16. Slutstatus: BLOCKED / NOT ACCEPTED.**  
Endast det av MAIN V separat auktoriserade R1-uppdraget. Ingen R2, R4, R1+R3-integration, designwaiver, PR-merge, PAL, fullspel eller oberoende VERIFICATION.

## 1. Slutsats för MAIN

Fysiska Stella 6.7.1/DASM-prov visar **två kompletta, rättvända originalmasker med två oberoende X- och två oberoende Y-tillstånd** i 16 distinkta kombinationer i *en* ROM och **48/48** exakta Stella-bildrutor. R1:s två-X-version överlevde dessutom **600/600 på varandra följande autentiska Stella-bildrutor**, med originalmänniskor, gul P0, M0 och bruna PF-väggar intakta och 262 scanlines i samtliga. Dessa är **DEVELOPER_LOCAL_PASS på avgränsade prov**, inte obegränsad fri X/Y-rörelse.

Separata riktiga assembler-/Stella-prototyper med tre, fyra och fem kompletta originalmasker på samma nio rader gav **16/16** exakt matchade bildrutor vardera i **fasta** test-X. Men sex individstyrda P1-resetstarter på samma nio rader misslyckades i **fem skilda tidsscheman med 16/16 fail vardera = 0/80 exakta sexandroid-bildrutor**. Felen gäller klippning och felaktiga/extra vita pixelgrupper i de första eller sista originalsilhuetterna. Gul P0, M0, PF-väggarna och 262 scanlines var intakta i alla 80 sexfigurproven. Att registerskrivningar ryms *statiskt* inom 76 cykler innebär inte att TIA:s P1-copy-deadlines medger sex korrekta, självständigt placerade maskbilder.

Den separata, äldre forsknings-ROM:en R1ba kunde återge sex fullständiga masker i 600/600 bilder, men bara med **NUSIZ-kopplade M/M- och F/F-par i tre kopplade X/Y-profiler**. Det är ett nyttigt kontrollfall men bryter fortfarande mot R1:s individuella positionsfrihet. Varken denna forskning eller nya 3–5-fasta-X-prover får upphöjas till R1-PASS.

**MAIN-beslut behövs för nästa tekniska uppdrag; vi lämnar R1 som tekniskt blockerat inom prövade kernels.** Vi har inte bevisat att sex oberoende X/Y är fysikaliskt omöjliga på Atari 2600. Vi har bevisat att de faktiskt prövade, körbara P1-close-copy-varianterna inte klarar det utan pixelkorruption.

## 2. Auktoritet, originalgrafik och isolering

- Bindande arbetsorder: `main/docs/MAIN_V_R3_RECEIPT_AND_R1_WORK_ORDER_2026-11-16.md`, och Issue #6 (endast v0.18 NTSC R1–R4-diagnostik). Aktivt arbete är enbart R1.
- Repo `Odourman/let-me-out`, isolerad gren `rom-dev/v018-r1-independent-xy-20261116`, skapad från historiska draft PR #7 HEAD `82667dae033f70570dce903f8e1d4866528be02a`. Draft PR #7 ändras inte; `main` ändras inte.
- Canon 8×9 JSON byte-exakt från `main/design/NPC_REFERENCE_8x9_masks.json`, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Eftersom PR7-grenen saknade denna nya fil lades en identisk, hashkontrollerad `canon_masks.json` i enbart R1-provets underkatalog. Alla fyra masktyper bevarade oförändrade: stor man, stor kvinna, liten man, liten kvinna. Spelaren är en separat tidigare 8×9 gul diagnoskandidat, inte ändrad originalandroid.
- Standard 16 384-byte F6, fyra byte-identiska 4 KiB-bankkopior. Detta utökar inte TIA:s faktiska sprite-resurser.
- Verktyg: Ubuntu 24.04 Actions, `dasm` 2.20.14.1-motor, `stella` 6.7.1, Xvfb, xdotool, ImageMagick och `python3-pil`. Upprepade lokala körningar reproducerade samma binär-SHA.

## 3. Observerade positiva ROM-resultat

| Fysiskt prov | Riktig Stella | Masker/X/Y-resultat | Utvecklarstatus |
|---|---:|---|---|
| TVÅ, faktoriell 2×2 X | 600/600, 262 scanlines | M+F, fulla rättvända 8×9; X-par i GUI-crop `(75,219),(75,231),(87,219),(87,231)`; bruna PF, P0, M0 exakt | **DEVELOPER_LOCAL_PASS** inom litet X-område |
| TVÅ, faktoriell 2×2 X × 2×2 Y | 48/48, 262 scanlines | 16 kombinationer; varje syntes faktiskt sedd 3 gånger; M/F Y-start `96/97` pixlar på crop; full mask, ingen ghost, P0/M0/PF | **DEVELOPER_LOCAL_PASS** inom steg om en rasterlinje |
| TRE, fasta X | 16/16 | stor man, stor kvinna, liten man, alla 8×9 | **DEVELOPER_LOCAL_PASS**, **inte** fria X |
| FYRA, fasta X | 16/16 | stor man, stor kvinna, liten man, liten kvinna | **DEVELOPER_LOCAL_PASS**, **inte** fria X |
| FEM, fasta X | 16/16 | två stora män, stor kvinna, liten man, liten kvinna | **DEVELOPER_LOCAL_PASS**, **inte** fria X |

För Y-provet uppdaterar den stabila, reproducerade versionen två separata 10-bytes-radbuffertar i 128 bytes RIOT-RAM under 18 befintliga toppblankningslinjer, förskjutna med exakt 0 eller +1 rad. Inga ändrade originalmasker, inga försvunna figurer och inga sekventiellt turade sprites. X-värden i tabellen är från Stellas 900×300 debugger-crop (dubbla TIA-färgklockor), inte godkända universella positionsgränser. Vi har **inte** provat fri X-övergång, korsning, sammanfallande X eller individuellt fritt Y över hela spelplanen.

**ROM-hashar SHA-256:**
- 2X, 600 rutor: `affec8170c9e0dece70975b16702c227ec1546b2fb317564c996943169313538`.
- 2X×2Y, 48 rutor: `c668111c19f18de859631f18b95999571c867057455bb8060f34255a7ed9a6c6`.
- 3-masker: `fd6526454577adff9a29e36b32bbdc25659fd0497620ee9664495fd02651795e`.
- 4-masker: `fcb087374541fbc9d4549a8e2c6d4bc9b51cf2cf4af7a04ded48a8fb78ac0b5e`.
- 5-masker: `5368d88474187604284c8348054dc6f68cdaeec8492a2ad0d5cd659e4e48a506`.

## 4. Observerade negativa sexmask-prover

Samtliga maskoriginal är käll-exakta och 9 rasterlinjer höga. Inga förändringar av antal/androidtyper användes för att få bättre statistik.

| Sexmask-schema | P1 RESP1-slutcykler (statisk kompilering) | Pixelperfekt sex/16 | Observation |
|---|---|---:|---|
| 6A | ursprunglig unrolled six-test, genererad av `build_scaling.py` | 0/16 | första stor man + små maskfragment trasiga |
| 6B | 19,28,37,46,56,66 | 0/16 | tidig/gles grupp och sena maskförluster |
| 6C | 20,29,38,47,57,67 | 0/16 | extra white ghost vid vänster x0 och mindre maskskada |
| 6D | 21,30,39,48,58,68 | 0/16 | extra white ghost vid vänster x0, ofullständiga masker |
| 6E | 18,27,36,45,56,66 | 0/16 | bara fem särskiljbara vitgrupper trots sex opcodes |

Alla fem byggdes till verkliga `.bin` av DASM och testades i äkta Stella; fulla råa skärmbilder och negativa pixel-CSV medföljer. `continue-on-error: true` på vissa analysskript medför att en Actions-jobbruta kan visa `SUCCESS` trots **R1-grafik-FAIL**. För 6B–6E kraschade den *avslutande utskriftssatsen* i analysprogrammet på strängformatet `%d` för `6B`, etc.; de maskinläsbara JSON-/CSV-resultaten var redan fullständigt skrivna och visar entydigt 0 exakta sexfigur-rutor. Programmeringsfelet är redovisat separat från TIA-felet. Den oavsiktliga feltexten är sparad i Actions-loggen.

Varje sexfigur-ROM har **262 scanlines 16/16**, P0/M0 16/16, vänster/höger PF 16/16. Det är alltså inte en falsk systemfelkälla från palett eller VSYNC. Trots beräknad maximalt ca 73–74/76 cykler ger `RESP1`-/`GRP1`-timingen inte 6 × 8×9 fullständiga masker med originalantal. `NUSIZ1=$01` CLOSE skapar omstarter som kan klippa pågående kopior. **Source-exact** kodbyte är inte samma sak som **source-exact** visuella pixlar.

Den ytterligare alternativa Y-renderingen med indirekta ROM-tabellpekare gav 24/48 godkända bilder och endast två av fyra förväntade X-par. Den behölls i repositoryt som `build_two_xy_rom_pointers_negative.py`, inte som den aktivt godkända Y-källan. Den tidigare RIOT-cachekoden återställdes och testades om 48/48 i Stella. Första felsökningskörningar med saknad mask-JSON och starttiming för Stella-fönstret finns i Actions-historiken; dessa är infrastruktur-/utvecklarfel och inte mask-PASS.

## 5. Faktisk CPU/TIA, inte bara statiska estimat

Real-Stella Debugger `trapWriteIf` för den kompletta TVÅ-X-prototypen:

| TIA-register | Uppmätt | Evidens |
|---|---|---|
| `RESP1` första | scanline124 / CPU-cykel30 | `evidence/two_x_24/traps/first_resp/stella_full.png` |
| `GRP1` första | scanline124 / CPU-cykel35 | `evidence/two_x_24/traps/first_grp/stella_full.png` |
| `RESP1` andra | scanline124 / CPU-cykel54 | `evidence/two_x_24/traps/second_resp/stella_full.png` |
| `GRP1` andra | scanline124 / CPU-cykel57 | `evidence/two_x_24/traps/second_grp/stella_full.png` |
| `NUSIZ1` | VBLANK/rasterlinje0, cykel15, värde `$01` | `evidence/two_x_24/traps/nusiz/stella_full.png` |
| `HMOVE` | blankningsrasterlinje7, cykel3 | `evidence/two_x_24/traps/hmove/stella_full.png` |

De uppmätta cyklerna avser en uppmätt tvåmaskrad och registerskrivning. Det finns **inte** en komplett sexmask-TIA-skrivtrace över 600 frames. Y-förskjutningskärnan håller samma `RESP1`/`GRP1`-kolumnstruktur och klarade faktisk pixelkontroll, men det är inte en generellt mätt banköverskridande cykelprofil. B02/T07 är därför **INCONCLUSIVE** för hela R1-villkoret. R1ba:s NUSIZ-grafik skapar heller inga extra hårdvarusprites från F6-banker.

## 6. 600 frames och reproducerbar byggning

- [Actions 43911479618](https://github.com/Odourman/let-me-out/actions/runs/43911479618): 600 **riktiga** efterföljande Stella Debugger GUI-framecrops i `evidence/two_x_600/raw/`, pixelperfekta två källmasker och giltigt 262-HUD på samtliga. Testad ROM SHA angiven ovan.
- [Actions 43911675301](https://github.com/Odourman/let-me-out/actions/runs/43911675301) och [slutlig omkörning 43912321860](https://github.com/Odourman/let-me-out/actions/runs/43912321860): 48 real-Stella RAM-cachad XY, 16/16 unika separata X/Y-uppställningar, 48/48 exakta fullmasker; stabil byggare `build_two_xy.py` i fryst R1-gren.
- [Actions 43909428292](https://github.com/Odourman/let-me-out/actions/runs/43909428292): 3..6 fullmasker, 3/4/5 lokal PASS men sex fail.
- [Actions 43910212163](https://github.com/Odourman/let-me-out/actions/runs/43910212163): 6B–6E alla fail (och separat beskrivet analysformat-fel).
- [Actions 43910212031](https://github.com/Odourman/let-me-out/actions/runs/43910212031): 24 source-orienterade originalmasker + sex real-Stella-traps.

Builder och källor finns under `rom/v018/experiments/r1_free_xy/`: `build_two.py`, `build_two_xy.py`, `build_scaling.py`, `build_six_sweep.py`, motsvarande `capture_*`, `analyze_*`, canonical JSON och samtliga DASM `.asm` från evidensarkivet. Genomför på Ubuntu 24.04 med paket `dasm stella xvfb xdotool imagemagick python3-pil` och kör de Pythonbaserade builderna. Originala ROM-listningar, symboler och påstådda SHA följer artefakterna; efter byggning använd `sha256sum` och jämför mot ovanstående.

*Observera:* 600 originalrutor ger bevis för två X inom fyra profiler, **inte** de sex oberoende figurpositioner som R1 kräver. Allt är utvecklarens egenkontroll, ingen independent clean rebuild och ingen VERIFICATION-grind.

## 7. T01–T16 och fortsatt beslut

Se `TEST_MATRIX_R1_DELTA.csv`. Sammanfattat T01/T02/T04/T07 för full R1 kan inte få PASS från begränsade prover. Sexfigur-scenen är observerat FAIL, 600 sammanhängande *sex* NPC-originalmasker inte utfört, full X/Y-kompatibilitet inte demonstrerad, och T07 global registerprofil INCONCLUSIVE. T14 egenbyggt och hashverifierat, men **ingen oberoende** byte-identisk rebuild. Övriga krav för R2/R3/R4 tillhör inte denna arbetsorder (R3:s separat mottagna DEVELOPER_LOCAL_PASS är oförändrad). T15 VERIFICATION STANDBY.

**Max två möjliga nästa teknikbeslut för MAIN:**
1. Tillåt fortsatt **separat R1-kernelresearch** mot sex fria positioner, exempelvis villkorad omordning av P1-kopior, scanline-fas-/datauppdateringar och verifierade gränsfall för P1-reset utan ändrad originalmask. Detta är tekniskt öppet men inget PASS garanterat.
2. Om det krävs en grafisk kompromiss (t.ex. para ihop vissa positioner, flera frameband eller fler ramar), **måste användaren uttryckligen auktorisera den** efter konkreta jämförande Stella-bilder. Ingen kompromiss får automatiskt tillämpas av ROM DEVELOPMENT eller MAIN.

**ROM DEVELOPMENT påbörjar inte R2, R4 eller R1+R3-integration utan separat arbetsorder.** R1 avslutas här som tekniskt blockerad inom de dokumenterat provade arkitekturerna.
