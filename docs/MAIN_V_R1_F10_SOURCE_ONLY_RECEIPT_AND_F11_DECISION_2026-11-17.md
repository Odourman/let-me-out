# LET ME OUT! – MAIN V: formell mottagning R1-F10 och en enda nästa teknikgrind

**Datum:** 2026-11-17. **Beslut:** R1-F10 är **MOTTAGEN OCH AVSLUTAD inom det uttryckligen auktoriserade SOURCE-ONLY-scope** med resultatet `F10_NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN`. Ingen ny exekverbar ROM, DASM-/Stella-körning, workflow, Python-test eller graphics har levererats i F10. **Full R1 BLOCKED / NOT ACCEPTED**, inga nya designwaivers och ingen organisatorisk E02 VERIFICATION.

## Verifierad fryst proveniens

- [ROM DEVELOPMENT II F10 fullständig källrapport på fryst commit](https://github.com/Odourman/let-me-out/blob/ef854d7436f1e1650827e2e19cc1b3d33a17f054/docs/ROM_DEV_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_TO_MAIN_2026-11-17.md) **`ef854d7436f1e1650827e2e19cc1b3d33a17f054`**, Git blob `4a8c3cc9cf6893699a1fda48152f155d076bd242`, 38 341 tecken; [formell handoff Issue #6](https://github.com/Odourman/let-me-out/issues/6#issuecomment-6944596854). Compare mot fryst F9 `c36982aef770af6cd3f68c2da37b8ed14aee2393`: exakt **ahead 1 / behind 0**, EN **nytillagd Markdown-rapport om 243 rader**, inga ändrade eller tillagda bygg-/ROM-/ASM-/CI-/Python-/maskfiler.
- [MAIN:s bindande F10-order](MAIN_V_TO_ROM_DEV_II_R1_F10_SIX_FREE_XY_ARCHITECTURE_SOURCE_ONLY_2026-11-17.md) uppfylld: tre **separata** arkitekturfamiljer A/B/C, fem hårda scenarier S1–S5, original 30 numrerade Atari-trick, tidsbudget, RIOT RAM, bank-kalkyl, prioriterad resultatklass och falsifierbara framtida miniprober.
- PR #7 livekontrollerad **OPEN/DRAFT/UNMERGED**, HEAD `82667dae033f70570dce903f8e1d4866528be02a`; `main` historiska projektstatus uppdateras separat. GRAPHICS fortsätter vara pausad/avslutad. Issue #8 oberoende VERIFICATION standby.

## Verkligt resultat och bevisgräns

F9 är tidigare **DEVELOPER_LOCAL + separat MAIN direkt pixelgranskad** på EN standard 16KiB F6/NTSC ROM SHA `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`: **TRE** rättvända olika 8×9-originalmasker med **TRE separata BINÄRA RAM-X** i åtta fasta kombinationer, 144/144 originala råbilder och 12/12 oberoende X-kontraster. De är **inte** numeriskt fritt positionerbara, inget fri-Y och ingen sex-NPC R1. F9:s kodbank har cirka **3019 program +115 data +6 vektorer =3140 av 4096 byte** använd budget; cirka 952 *säkra fritt tillgängliga* bytes under aktuell layout, fyra identiska F6-banker. Dessa historiska värden kontrollerades i tidigare MAIN-mottagning, inga nya F10 mätningar.

F10:s tre arkitekturfamiljer:
- **A: dynamiskt P1 RESP/GRP-tidsschema med individuellt numeriska RAM-X/Y**, högst forskningsvärde men F10 visar inte sex samtidiga individuella START-/GRP-fönster. Tätt/överlappande X ger fysisk single-P1-sample/latch-konflikt och kan kräva explicit framtida occlusion/designpolicy; ingen sådan waiver finns.
- **B: bankfördelade standard-F6-kernels** kan hjälpa kod-/dataordning eller olika Y-topologier men ger inte fler 76 CPU-cykler, fler players eller en fri per-kopia-X-kanal. F10 räknar konkret vanlig hotspot switch+JMP som minst 7 CPU-cykler i den enkla vägen, inte en universell mätning.
- **C: adaptiv NUSIZ-kopiering, Y-multiplex, VDEL/PF** kan optimera gynnsamma geometrier men fasta avstånd, samma-Y och felvänd äldre R1ba-källrad (4 stora inverterade) gör C obestyrkt som generell sex-X/Y-kernel.

**Source-only lower bound för en konkret sex-RESP/GRP-rad**: 18 RESP +18 GRP +12 immediate-mask LDA +5 P0 +5 M0 +3 WSYNC = **61/76 CPU-cykler** med endast 15 kvar före sortering, PF, vänt-/copy-deadlines och faktisk Y. Zero-page-masker ~67/76, ROM index ~73/76, alltid villkorliga modeller, **ingen universell omöjlighetssats**. F10 redovisar S1 sex X=[16,36,56,76,96,116] CC same-Y, S2 [40,44,48,52,56,60] CC överlapp, S3 förskjutna Y som ändå ger sex samtidig täckning, S4 X-ordningsbyte, S5 R2 key/R3 högerdörr. Inget av dessa är nytt Stella-test.

**En användbar men ALDRIG automatisk nästa hypotes** är F10 A:s liten fyra-original-NPC-gate: M/F/SM/SF på en och samma 9-radershöjd, **numeriskt lagrade RAM-X** i stället för `2^4` modekernlar, X i TIA-colorclocks `[16,36,56,76]` och ett oberoende +3CC positionsbyte. Detta räcker inte till sex fria X/Y ens vid PASS.

## MAIN:s separata nästa beslut

[**R1-F11: FOUR ORIGINAL MASKS / NUMERIC RAM-X / ONE-ROM MINIMAL FALSIFICATION**](MAIN_V_TO_ROM_DEV_II_R1_F11_FOUR_NUMERIC_X_P1_DIAGNOSTIC_ONE_ROM_AUTHORIZED_2026-11-17.md) är **EN NY, EXPLICIT MAIN V-auktorisation** för den smalaste reproducerbara A-premissen inom redan användar-godkänd NTSC v0.18 R1 hardware diagnostic. **Obligatorisk SOURCE-ONLY G0 före eventuell build; HÖGST EN ny standard F6/NTSC ROM om G0 PASS, HÖGST en färdig negativ eller positiv studie med STOPP.** Oförändrade originalmasker, P0/M0/PF och 76/262. Inga fjärde *binära* profil-2^4-varianter får rädda ett misslyckat numeriskt läge, ingen R1ba-kernel, mapperbyte, H/W-designwaiver, sex-NPC/R2/R3/R4/PAL/fullspel/GRAPHICS/PR merge/Verification/F12.

**Mottagningsslutklass:** `F10_SOURCE_ONLY_ACCEPTED / NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN / FULL_R1_BLOCKED_NOT_ACCEPTED`.
