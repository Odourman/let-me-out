# LET ME OUT! – MAIN VII G5AA: G5Z/ROM DEVELOPMENT III G0-H4-ONE mottagen, slutsats INCONCLUSIVE
**Datum:** 2026-11-17.
**Mottagningsstatus:** `G5AA_G5Z_G0_SOURCE_DELIVERY_RECEIVED_AND_REVIEWED`.
**Slutklass för utförd och uttryckligen auktoriserad G0:** **`G0_INCONCLUSIVE_NO_ROM`**.
**Avgränsning:** MAIN VII:s käll- och leveransgranskning, **inte** eget nytt H4-hårdvaruprov, oberoende Verification II, ny G1/G6/F12-auktorisation eller godkänd slutlig spelarkitektur.

## 1. Exakt bindande mandat och leverans
- Ursprunglig specifik användarauktorisation **LM-D20**: [G5Z-ordern](G5Z_MAIN_VII_ROM_DEVELOPMENT_III_G0_H4_ONE_SOURCE_PREFLIGHT_AUTHORIZED_2026-11-17.md), source-only H4-ONE med STOPP efter rapport.
- [GitHub Issue #12 och specialistens frysta slutleveranskommentar](https://github.com/Odourman/let-me-out/issues/12#issuecomment-6957141007).
- **Fryst ROM DEVELOPMENT III-commit:** `8c7cef622ebaa6543a3f044ddf50d21024b1b978` på isolerad gren `rom-dev-iii/g5z-g0-h4-one-source-only-20261117`. GitHub compare från `main` `2421aa9eb49a10a618f030ef282f1bebc268eac0`: ahead **5**, behind **0**, exakt **4** **tillagda** text/CSV-filer, inga ändrade original, ingen merge.
- [Fullständig TO_MAIN-rapport](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md) blob `70cde51ab76634fdf752f971d94e160882cdb632`.
- [72-raders CC/cykelmatris](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/G5Z_H4_ONE_ROW_CYCLE_CC_MATRIX.csv) blob `fdab6a48c1e9b729f8c6dbc0a97d4e8b3d59289c`.
- [Källproveniens](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/G5Z_SOURCE_PROVENANCE.md) blob `a2cc3c637f080de66ee10474b2aac29ae09d2f38`.
- [Kvarstående fem-NPC/S05-hinder](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/H4_TO_FIVE_NPC_AND_S05_REMAINING_GAPS.md) blob `6eafaf8ba943c5a2f3e294697efa955871e2090b`.
- [Arkivrapport i officiell Google Drive](https://docs.google.com/document/d/1TaX5kgjKvP95pbuXZDS42myxZwi_jvu7zBpezlTj6No/edit), aktuell parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`. Drive-kopian innehåller extra proveniens-/arkivheader; den är **inte byteidentisk** med GitHub Markdown, men rapportens kropp, slutklass och stoppspärrar är återlästa.

## 2. MAIN:s separata mottagningskontroller
1. Hämtade live GitHub-branchens tree och compare; 4 nya analysfiler under `rom/g5z_g0_h4_one/`; **inga** nya `.asm/.bin/.lst/.sym`, ändringar av existerande speloriginal eller ROM-kernel via denna branch. Av detta kan **inte** generellt härledas att ingen annan aktör körde lokala verktyg; specialistens tydliga undertecknade rapport uppger **0 nya DASM/Stella/CI** inom scope.
2. Läste all specialistens fulla TO_MAIN-text, CC/CPU-matrisen, SHA/proveniens och 5-NPC/S05-gap. GitHub Issue-kommentaren motsvarar den frysta leveransen. Återläst officiell Drive-rapport och bekräftad korrekt parent.
3. En **egen maskinell kontroll av matrisen mot originalet** `design/NPC_REFERENCE_8x9_masks.json` (Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`) gav **72/72 rows** med korrekta frysta M, F och SM TOPDOWN-radbytes och för registrerade positiva/negativa stimulus `68 + synlig X = nominellt absolut CC`. Precis åtta ID `G4-A1/A2/B1/B2/X1/X2/M1/P1` × nio rader 0..8, totalt **72 rader**, alla kolumner korrekt antal. Projektspelaren är en diagnostisk 8×9-bitmap, inte officiell slutgrafik.
4. En separat kontroll av rapportens opcodearitmetik gav **58c** per normal aktiv rad (sista rad **57c**) för exakt mallen `4 LDA abs,Y ×4c; 4 STA GRP ×3c; 4 STA RESP ×3c; 2 LDA #color + STA COLUP0 ×5c; DEY/BPL 5c (4c sista); STA WSYNC 3c`. För skott på rad 3 läggs **10c** till `68c`; möjliga två GRP-clears `+6c → 74c` och ett ytterligare NUSIZ write-par `+5c → 79c` i **just denna append-only-mall**. Det är **inte** ett fullständigt körbart eller fysisk START-säkrat schema; utelämnade RAM-fetch/scheduler/branch/pagecross/kritiska delays kan belasta ytterligare.
5. MAIN läste även faktiskt [Stella 6.7.1 Player.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Player.cxx) där `Player::resp` hanterar pågående rendering, [TIA.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/TIA.cxx) där `NUSIZ0` fördelas till både `myPlayer0.nusiz` och `myMissile0.nusiz`, och [Missile.cxx](https://github.com/stella-emu/stella/blob/6.7.1/src/emucore/tia/Missile.cxx) med `enam`/kopieavkodning. Detta stöder **risken** men ger inte ett fullständigt CPU-write→START-latch-bevis.
6. **Redaktionell notis:** TO_MAIN-rapportens enstaka ord `36-raderskalkylen` hänvisar till den levererade **72-radersmatrisen**. Siffran 36 i den frasen är en skrivmiss, inte ett extra halverat testfall; källfilen och övrig redovisning innehåller åtta × nio. Lämna frysta specialistoriginal oförändrade och håll rättelsen här.

## 3. Teknisk mottagningsbedömning
**ACCEPTERAT SOM SCOPE-KORREKT KÄLLBASERAT RESULTAT: `G0_INCONCLUSIVE_NO_ROM`.**

Det finns avgränsade positiva historiska primitivelement (R1f/R1g och F9 i **olika** kernel-familjer) och källa-spårbar möjlig edge-only brun PF i ett **särskilt** statiskt nioradersband. Detta visar inte att en kombinerad H4-ONE är genomförbar.

**Kritisk öppning i beviskedjan:** det finns ingen källgrundad **sammanhängande instruktions-PC/opcode-/STA-write-final-c/RESP→intern START-/GRP-latch/NUSIZ0-M0-gate-scheduler** med separata numeriska RAM-X i **både** P0-identitetsordningarna och två vita P1-original tillsammans med en M0 på exakt samma aktiva rader och PF. G4-X1 visar begränsad konkret negativ `COLUP0`-färgkonflikt vid identisk pixel; G4-X2 riskerar P0-retigger under aktiv rendering. Ingen H4 `SOURCE_PLAUSIBLE` och ingen H4 universell `FAIL` kan styrkas utan att överdriva en begränsad modell.

**Fortsatt giltiga negativa referenser:** F11:s `G0_FAIL` för fyra numeriska P1-X i sin specifika allokering; G5H:s 79/76 respektive 74/76 för direkt fem-NPC-plus-door-allokering. Dessa är inte H4:s fristående dom och inte ett generellt Atari 2600-förbud.

**Inte utfört och inte bevisat:** ingen H4-ROM, ingen körning i Stella, ingen oberoende Verification II, ingen fungerande fem-NPC-R1 eller R2+key, inga 8×9-geomspawn-collisions, ingen S05 orange door+gold key+yellow player+white NPC+M0/PF samma-Y. H4 behöver bara 3 vita fiender; fullspelet kräver 5. LM-D12–D19 mål och källpinnade framtida A_OPEN_01/B_OPEN_02/C_OPEN_01/D_OPEN_01 kvarstår som beslut, inte renderade spelkartor.

## 4. MAIN:s rekommendation – INTE en ny arbetsorder
**Nuvarande G0 stängs som avslutad source-only INCONCLUSIVE.** Den tidigare G5Y-vägen `G0_SOURCE_PLAUSIBLE` → separat H4 fysisk G1-ansökan har **inte** uppnåtts. Därför får en full H4/G6-ROM **inte** följa automatiskt. Varken upprepade likadana källrundor eller komplett spelbygge rekommenderas.

**Mest kunskap per begränsat nästa experiment**, om och endast om användaren ger **NYTT uttryckligt mandat**, vore ett **isolerat, starkt instrumenterat TIA-fas-/kopiekalibreringsmikroprov** som är **ett annat scope än full H4**: en minimal NTSC F6 ROM med mätbar `RESP0` under både giltiga och riskfyllda retriggerförhållanden; `NUSIZ0=$02` effekt på P0 och M0 vid samma Y med `ENAM0`-gate/single-copy och `GRP`-latens; exakta source- och pixel/CC-traces. **Ett sådant försök skulle bara mäta de isolerade osäkerheterna, INTE godkänna H4, S05, fem-NPC eller G5.** Om dess fall inte med säkerhet kan särskilja teorier, bör förslaget avslås innan byggnad. Detta är **en rekommendation att låta användaren ta ställning**, inte utfärdad G1/G6/F12/ROM-order.

Alternativ efter ett sådant mätprov är källstyrd omvärdering av H4, eller vid fortsatt stopp en separat användarstyrd design/arkitekturavvägning. Bevara alla negativa resultat.

**Aktuella spärrar:** `G5_FORMAL_OPEN`; `G0_H4_ONE_COMPLETE_INCONCLUSIVE`; `G1/G6/F12/ROM_DEVELOPMENT_FURTHER/NEW_VERIFICATION/PR_MERGE=NOT_AUTHORIZED`. PR #7 ska förbli draft och oförändrad. Ingen ny renderings-, Y-lane-, flicker-, fiende- eller nyckelwaiver ges av detta dokument.
