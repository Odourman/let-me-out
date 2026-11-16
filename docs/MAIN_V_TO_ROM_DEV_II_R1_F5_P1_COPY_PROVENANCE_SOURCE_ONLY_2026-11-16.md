# LET ME OUT! – MAIN V till ROM DEVELOPMENT II
## R1-F5 – P1 COPY PROVENANCE: endast källa/hårdvaruresearch, INGEN NY ROM

**Datum:** 2026-11-16. **Auktorisationsnivå:** en **ny uttrycklig, helt källbaserad teknisk analysorder** inom det befintligt godkända v0.18 NTSC R1-undersökningsområdet [Issue #6](https://github.com/Odourman/let-me-out/issues/6). **Inte** implementation, F5-kod, ny Stella-exekvering, full-R1-acceptans, byteändring, R2/R4, PR-merge eller oberoende VERIFICATION. GRAPHICS är fortsatt avslutat.

### 1. EN avgränsad fråga

**Vilken av TIA:s P1-huvudkopior / NUSIZ1-close-kopior / historiska kopiestarter kan ge den första synliga originalandroiden vid debuggercrop-X=43, samtidigt som den första verkliga `RESP1` på samma rasterrad flyttas mellan CPU-c18/19/20/21 och nästa faktiska `RESP1` hålls vid c28?**

Jämför varför index2 i fryst F2 **verkligen ändrar x129↔135** vid `RESP1 c37↔38`, medan den tidiga index0-kopian **INTE flyttar sig** när första `RESP1 c18..21`. En **kausal teori ska ge unika, falsifierbara prediktioner** som särskiljer den från tidigare misslyckade `+/- CPU-cycle`-försök.

### 2. Bindande källor, precedens och exakt format

Läs live:
1. [MAIN:s egna R1-F4 mottagning](MAIN_V_R1_F4_RECEIPT_AND_NEXT_DIAGNOSTIC_DECISION_2026-11-16.md) – **F4: bägge c18/c21 verkligt FAIL, 32/32 riktiga bilder, ingen runtime**.
2. [Fryst F4-utvecklarrapport](https://github.com/Odourman/let-me-out/blob/2218e583f4a6f9c60adc3e4bb850b05a7176f1b4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F4.md) på commit `2218e583f4a6f9c60adc3e4bb850b05a7176f1b4`, där `r1_f4_6B_I0_C18_I2_FIXED_F6.bin` SHA256 `d06fa761ddcc4756fbb2b9b2d72bbe49cc4ec5146a04c8e5e4ff8483dfd9f15d`, c21-ROM `fc3e3622e155c3faded0d91e12f2889c24d0c9eb16822bbef58a4d7cdd6d704f`, båda X0=43. [F4 kombinerade riktiga Drive-evidens](https://drive.google.com/file/d/1ELlpy5rlXrgtW-flmKT7sUpZXKGj3LMJ/view), full ZIP SHA256 `c8585485eeb78cf3fb7c17dd1dbddbc77d17118485232161d9b1c16736dd8c50`.
3. [F3](https://github.com/Odourman/let-me-out/blob/65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F3.md) c20→x43 med verklig PC/cycle-trap; [F2](https://github.com/Odourman/let-me-out/blob/485a6c10047fb9b41e589ac3df724c1bc70f0283/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F2.md) index2 c37↔38 → x129↔135 i **samma** körbara ROM; [F1 correction](MAIN_V_R1_F1_RECEIPT_AND_HISTORICAL_AUDIT_CORRECTION_2026-11-16.md) c19→x43 och 6B fasta sexmask-PASS. Ursprunglig 6B standard-F6 `36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4`.
4. Original `design/NPC_REFERENCE_8x9_masks.json` Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; sex figurer i indexordning `large_male,large_male,large_female,large_female,small_male,small_female`. Ingen ny bitmap får införas.
5. [Tidigare MAIN TIA-forskningsrapport](MAIN_TIA_RETRIGGER_NUSIZ_CLOSE_RESEARCH_2026-11-16.md), [MAIN RESP1-analys](MAIN_RESP1_ROOT_CAUSE_ANALYSIS_2026-11-15.md), [30-trickstillämpning](MAIN_V_R1_30_TRICKS_APPLICABILITY_REVIEW_2026-11-16.md); de är **rådgivande**, inte implementation eller bevis. Läs och ange exakta externa primärkällor, särskilt [Andrew Towers – TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) och vid behov Stella/TIA 6.7.1 emulatorimplementationskod, och håll isär emulator-/dokumentbevis från våra faktiska raw images.
6. Reellt F4-ASM/`r1_f4_build.py`, `r1_f2_build_runtime.py` och faktiskt per-row DASM-listning, inklusive **föregående och efterföljande scanlines**, `NUSIZ1=$01`, `HMOVE`, `VDEL1` (om aktiv), alla 6 `RESP1`, `GRP1`, `WSYNC`. Alla indexnamn refererar till källordningen, inte en antagen TIA-copy-ID.

### 3. Arbetsmetod: SOURCE-ONLY, inget nytt program

Från de **frysta** redan levererade listningarna, ROM-binarna, screenshots/traps och externa TIA-källor:
- Skapa en tabell för **alla nio bitmaprader** med sex `RESP1`-cykler, fyra `GRP1`-cykler, P0/M0/PF och `WSYNC`; inkludera **föregående rasterrad och nästkommande rad** för att kunna skilja huvudkopia från föregående linje mot extra copy på aktuell linje.
- Räkna ut reset-offset, copy-trigger-fönster och när `GRP1` ändrar vilken kopias aktiva data. Knyt varje förklaring till *konkreta externa TIA-dokument/kodrad* eller tydligt märkt **HYPOTES**; två olika kopior får inte likställas bara för att de båda är vita i samma debugbild.
- Fyll i en **source/trap/pixel-uthållighetsmatris** för `c18, c19, c20, c21` med `index1=c28`, samt fungerande index2 `c37,c38`. Beräkna på förhand *vilken* fysisk start X respektive möjlig trigger-teori förutsäger. Om en teori är förenlig med alla utfall men inte prediktiv: märk **NOT_DISCRIMINATING**.
- Identifiera eventuella förväxlingar mellan masktyp/index och TIA-copy, maskbits som redan är låsta av en tidigare P1-copy, display latch, `GRP1`-deadlines, eller nästa `RESP1`. Distingvera faktiska mätta registertraps från source-only timestamps och inferenser.
- Om det går, presentera **EN** tydligt falsifierbar nästa testidé (specifik enda register-/copyförutsättning och två på förhand registrerade möjliga pixelresultat), men **bygg den inte**. Om inte: `F5_CAUSE_NOT_ISOLATED`; bedöm rakt att blinda en-cykelssvep inte är motiverade och att MAIN måste ta design-/arkitekturfrågan som ett separat beslut.
- Max två framtida **alternativa vägval** till MAIN: en ny snäv, separat explicit diagnostic *endast om en ny mekanism och tydlig positivitetsgrind kan formuleras*, eller avbryt 6-fri-X på aktuellt schema och lyft arkitektur-/user-waiverfrågan. **Inget automatiskt val av kompromiss.**

### 4. Leverans, kontroll och hård stoppgrind

Leverera **en** välstrukturerad `docs/ROM_DEV_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_TO_MAIN_2026-11-16.md` på **en ny isolerad analysbranch** från frysta F4 `2218e583f4a6f9c60adc3e4bb850b05a7176f1b4`. Endast ny Markdown/text/CSV och read-only extrakt; inga binärändringar, ingen assemblerändring, ingen ny DASM, ROM, Stella, Github Actions, python-auditkod eller release. Inkludera exakta GitHub-källrefar och ställningstaganden `SOURCE_ONLY_CAUSAL_HYPOTHESIS_WITH_PREDICTION` eller `F5_CAUSE_NOT_ISOLATED`, med öppna motbevis.

**STOPP** efter denna enda rapport. F5 levererar **ingen** andra runtime-X, **ingen** fri sex-X/Y, **ingen** R1+R3, **ingen** R2/R4, **ingen** F6SC/ARM/PAL, **ingen** integration, **ingen** PR-merge och **ingen** oberoende VERIFICATION. Fullt R1 fortsätter **`BLOCKED / NOT ACCEPTED`** oavsett hur bra en källteori verkar. GRAPHICS förblir avslutat och inga originalmasker, kartor eller gameplayregler ändras. För alla nya ROM-experiment krävs ett nytt **uttryckligt MAIN V-beslut efter F5**.
