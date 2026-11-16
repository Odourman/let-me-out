# LET ME OUT! – MAIN V: R1-F5 mottagning och oberoende R1ba-orienteringsaudit

**2026-11-16.** **Beslut:** F5 `SOURCE_ONLY_CAUSAL_HYPOTHESIS_WITH_PREDICTION` är **AVSLUTAD OCH MOTTAGEN SOM TEKNISK KÄLLANALYS**. Inte fullständig orsaksverifiering, ingen fristående VERIFICATION och ingen R1-acceptans. **EXACT_COPY_START_PROVENANCE_NOT_ISOLATED**, **NO_INDEPENDENT_SECOND_X_GEOMETRY**, **R1 BLOCKED/NOT ACCEPTED**. F5 är INTE en ROM-leverans.

## 1. Verklig fryst F5 och filomfattning

- Fryst F5: [`953c6c5ef20e83d93474de4c094de784761da257`](https://github.com/Odourman/let-me-out/commit/953c6c5ef20e83d93474de4c094de784761da257) på isolerad `analysis/v018-r1-f5-p1-copy-provenance-20261116`, fryst förälder F4 `2218e583f4a6f9c60adc3e4bb850b05a7176f1b4`.
- [F5-utvecklarrapport (exakt commit)](https://github.com/Odourman/let-me-out/blob/953c6c5ef20e83d93474de4c094de784761da257/docs/ROM_DEV_R1_F5_P1_COPY_PROVENANCE_SOURCE_ONLY_TO_MAIN_2026-11-16.md), blob `4783c2bc949ed675adc6cced94d53ee52152bbe7`; [Issue #6-leverans](https://github.com/Odourman/let-me-out/issues/6#issuecomment-6930045146).
- MAIN:s direkta GitHub `compare_commits` mot F4: **ahead=1, behind=0**, **exakt EN nytillagd Markdown-fil med 148 rader**, inga ändringar av ASM, Python, DASM/CI, originalmasker, F4, tidigare branch eller production. PR #7 kontrollerad **OPEN/DRAFT/UNMERGED** med head `82667dae033f70570dce903f8e1d4866528be02a`.
- F5:s källhypotes: F4/F3:s första `RESP1 c18/19/20/21` ligger under HBLANK och första X0 observeras x43 för alla, medan F2:s aktiva `c37/c38` faktiskt växlar x129/x135. `TIA::poke`/`resxCounter`, `Player::resp/tick`, `DrawCounterDecodes` visar CPU-write, counter reset, NUSIZ decode och GRP start separat; exakt START-proveniens vid c28 är **inte** spårad. **F5 uppfyller source-only-målet med EN falsifierbar framtida 2-maskershypotes**, inte en bevisad lösning för sex fria X/Y.
- Historisk R1ba `NUSIZ1=$03` visar en annan **begränsad** renderer med fyra manuella `RESP1` och två automatiska stora maskpar, tre förberedda **kopplade** X/Y-profiler. Det visar ingen obegränsad individuell X/Y och kan inte ersätta F4 eller R1-gaten.

## 2. Oberoende MAIN-revision av de faktiska R1ba-råbilderna (VIKTIGT)

MAIN har nu laddat ned och kontrollerat exakt [R1ba-forskningspaket i projekt-Drive](https://drive.google.com/file/d/1c2Sd68dvQsmb_MJcQOLU8dbiMc5YgbsJ/view). Detta var **redan existerande bevis**, inget nytt ROM-bygge, Stella- eller CI-prov. Originalarkiv: **3 930 298 byte**, **622 poster**, ZIP CRC PASS, SHA256 **`f8dd41e62939aa1699d80f70df0c5b5081b87441a1e2c740ff2786139908f325`**, original Stella-råbilder `frame_0001.png`–`frame_0600.png`; arkiverad 16 KiB standard-F6-ROM `proof.bin` SHA **`41fdb87969a20d40fee8cde5673792201663860c2d1e08c8d93f9172ede82361`**.

Källor granskade mot fryst researchcommit `788e2b2764b367f880d78d2caa779da58c281281`:
- `rom/v018/experiments/main_iv_r1ba_combined/r1ba.asm` i original-ZIP: tabellen `MaleRows` innehåller den låsta källordningen `3C 3C 18 FF 18 24 24 42 42`, men den faktiskt exekverade `R1atAScan0` laddar `LDA #$42` till mannen och `R1atAScan8` laddar `LDA #$3C`; samma inversion för stor kvinna `FemaleRows` (kod börjar `LDX #$24` i första rad).
- Forskningens `analyze_600.py`, Git blob `5aee0170ee5cad7f096b9f28b0f22896d18f7a8a`, har `return [...][::-1]` i `mask(name)`, och jämför uttryckligen mot spegelvänd radordning för både stora maskerna. Historiskt "600/600 source masks exact" är alltså **600/600 mot auditorprogrammets ANNAN orientering**, inte bevis mot projektets låsta *top-down* referens.
- MAIN:s **nya, oberoende läsanalys** av alla 600 **äkta, arkiverade 900×300 Stella-PNG**: avkoda original-PNG direkt, hitta alla vita skärmpixlar (RGB >180 och kanalavvikelse <40) i bildens faktiska aktiva band x0–335/y50–194, avläs de sex X från arkiverad CSV och nominella Y-profiloffset från `manifest.json`; bygg förväntad bildpixelunion från nuvarande oförändrade `design/NPC_REFERENCE_8x9_masks.json` i **exakt top-down ordning**, 2 skärmpixlar per källbit, samt källangivna Y-profiler.
- **Top-down originalcheck:** **0/600 PASS**, samma differens **128 SAKNADE + 128 EXTRA vita screenshot-pixlar i varje bildruta** jämfört med korrekt sex-maskers referens. Alla 600 verkliga bilder har **348 vita screenshot-pixlar** i det analyserade området. Andra fel är inte nödvändigtvis uteslutna utanför detta vita pixelband.
- **Felsökande kontroll:** Förväntad bild där de **fyra stora** maskerna `M,M,F,F` vänds i radordning, men `SM,SF` **behåller rätt top-down-rader** med lägesprofiler, ger **600/600 exakt match, 0 saknade och 0 extra vita screenshot-pixlar**. Det betyder att det är en **systematisk, reproducerad orienteringsavvikelse enbart för de stora maskerna**; de två små ritas korrekt i den redan arkiverade R1ba-ROM:en.
- Rå närinspektion: första mannens första faktiska nio bitmaprader i crop-X75 är `42 42 24 24 18 FF 18 3C 3C`, medan låst `large_male` är `3C 3C 18 FF 18 24 24 42 42`; kvinnan visar `24 24 7E 7E 3C FF 18 3C 3C` i stället för låst `3C 3C 18 FF 3C 7E 7E 24 24`. Detta är ej en fråga om maskbytes integritet – **tabellbytes bevaras, EXEKVERAD RASTERORDNING fel**.

### Beslut om äldre R1ba-resultat

- Skriv INTE längre att `R1ba 600/600 six original top-down masks PASS`. Korrekt är **`R1BA_600_LOCAL_NUSIZ_COPY_AND_COUPLED_XY_RESEARCH` med `ORIGINAL_ORIENTATION_FAIL`**. Bevis på **sex vita fulla originalformade maskvärden i omvänd stor-riktning** och tre kopplade X/Y-formationslägen kvarstår.
- Det historiska CI-resultatet raderas/skrivs inte om: det var grönt för **sin egen felvända maskreferens**. MAIN:s oberoende read-only audit har bättre testoracle och är därför ett **faktiskt motbevis mot kanonorienteringsanspråket**, inte en ny utvärdering av TIA-timing.
- R1ba får inte utan nytt uttryckligt tillstånd användas som kanonspelar-NPC-kernel, kopieras till PR #7 eller "fixas snabbt" med nya byte. **Rättvändning av de fyra stora maskerna kräver en verklig ny byggd ROM med exakt pixel-/timing-/grafikresursproof**. Originalmasker/kartor ändras INTE och GRAPHICS förblir avslutat.
- Det här är MAIN:s egen tekniska revision av historisk forskning, **inte** beställd organisatoriskt fristående VERIFICATION (Issue #8 standby), och bevisar inte R1/P1 sex fria X/Y.

## 3. Huvudbeslut och följande enda avgränsade fas

F5 **AVSLUTAD OCH ACCEPTERAD** som SOURCE ONLY. MAIN:s nästa fråga är den specifika, reproducerbara två-originalmaskers **HBLANK/START-latch**-hypotesen i F5 §7, och inget annat. [Ny, separat F6 diagnosarbetsorder](MAIN_V_TO_ROM_DEV_II_R1_F6_TWO_MASK_HBLANK_COPY_GATE_AUTHORIZED_2026-11-16.md) är den **enda** tillåtna fortsättningen inom redan avgränsad användargodkänd NTSC v0.18 R1-hårdvaruförstudie.

**R1-F6 ger inte tillstånd att bygga om R1ba, reparera dess vända 600 bilder, börja sex-X-kernel, R1+R3, R2/R4, ny originalbild, HUD/KEY/GAME OVER, F6SC, PAL, fullspel, ny AI, PR merge eller ny VERIFICATION.** F6 stannar efter som mest två test-ROM:er eller tidigare stopgate. F5 och F4 förblir frysta, alla MASK-/GRAPHICS/ROM original orörda.

**Slutstatus:** `F5_SOURCE_ONLY_CLOSED / CAUSAL_HYPOTHESIS_WITH_PREDICTION / R1BA_ORIGINAL_ORIENTATION_FAIL_INDEPENDENT_MAIN_READ_AUDIT_600_OF_600 / R1_BLOCKED_NOT_ACCEPTED`.
