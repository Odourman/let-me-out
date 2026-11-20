# LET ME OUT! – RESEARCH OCH 30 TRICK / V8

**Project Sources V8, MAIN XI, 2026-11-20.** Daterad navigationskopia, **inte** självständig projektcanon, en ny implementationsorder, emulator-PASS eller oberoende Verification. Följ alltid aktuell [GitHub-status](https://github.com/Odourman/let-me-out/blob/main/docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md), [AGENTS.md](https://github.com/Odourman/let-me-out/blob/main/AGENTS.md), [G5-spärren](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), faktisk Issue, fryst commit och originalbeslut i [Google Drive](https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u). Om ny leverans publicerats senare än denna daterade källa ska den granskas innan nuläget anges.

[Originalets 30 programmeringstrick](https://github.com/Odourman/let-me-out/blob/main/docs/RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md) och [G5L-rasterexit](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5L_FINAL_TECHNICAL_EXIT_30_TRICKS_R1_R2_DOOR_KEY_AND_USER_DECISION_2026-11-17.md) är rådgivande teknikbibliotek. Sprite multiplexing, GRP/RESP mitt i scanline, NUSIZ-kopior, HMOVE, förladdning av maskbyte, VDEL och Venetian Blinds är tekniska kandidater, **inte** flimmerwaiver eller godkänd ändring av originalmasker/fiendeantal. Z3-SAT/UNSAT bevisar endast prövad modell, inte fysisk TIA-rendering.

## Faktiska tekniska slutsatser

[Spelbar V02-8177c](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036737753) har lokal **80/96** utökad PF/NPC-domän: X63–78 i Y77,90,100 och Y40,130 korrekt; Y160 fortfarande 2 saknade brunpixlar per fall. Låst dörrs bruna pixelmissing **36**; öppnad **58**; cold-key **16**. Standard femmaskers pixel-PASS i **595/600**, men densitetsexperiment same-Y86 **2/5** och nyckeln med spelare samma Y-band vid annat X **0/14**. Dödlig resurskonflikt kan inte döljas av 262 stabila scanlines eller att spelets logiska aktörer lever.

Utvecklarens två **negativa R3-PF-hålprover** gav **294 resp 282 scanlines**, tappade orange pixlar: bitmaskad speglad PF har fyra färgklockor per bit och ger inte automatiskt ursprunglig R3:s en- eller tvåfärgklockor smala utskärning. P1 sent bytt efter SM: **9/14** nyckelpixlar med skadad SM; reserverad P1-slot: **14/14 key men SM helt borta**. Dessa försök är lokalt negativa, inte generell Atari-UNSAT.

## Nya forskningsriktningar, utan kodauktoritet

[Nytt framtida designbeslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/MAIN_XI_USER_DECISION_FUTURE_RANDOM_NPC_FORMS_TOP_BOTTOM_EXIT_2026-11-20.md) medger en dörr centrerad i övre eller nedre ytterväggen för att utnyttja `CTRLPF`-spegling. **Vänster–höger-spegling av PF** underlättar en centrerad horisontell öppning; den bevisar **inte** en exakt orange dörr med svart utstansad liten nyckelhålsmask eller full fri fem-NPC same-Y. [V02-provorder](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7036700643) beställer tekniska **byggda och uppmätta** topp- och bottenvarianter utan release-/kartcutover. Behåll testet isolerat från skarp framtida kartcanon.

**Slumpade utseenden:** framtida fem individer väljer bland fyra oförändrade TOP-DOWN 8×9-masker vid rumsstart. Maskvalets timing och RAM-/sorteringsschema måste utvärderas mot samtliga combinationsklasser (inkl. fem samma form, små/stora same-Y) och oberoende 1/5 nyckelbärare. Inget rätt att begränsa vilka masker som får väljas för att klara scanlines.

RESEARCH II undersöker och ger råd, **ROM DEVELOPMENT IV** programmerar inom särskilt delegerat scope; MAIN leder och VERIFICATION II kontrollerar oberoende. Följ snabb utveckling: reella spel-ROM-iterationer först, rena studier bara där de löser fysisk blockerare.
