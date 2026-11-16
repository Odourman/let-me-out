# LET ME OUT! – MAIN V till ROM DEVELOPMENT II
## R1-F7 – TWO-MASK / TWO INDEPENDENT RUNTIME X SELECTOR BITS (2×2), EN ENDA NY ROM

**Datum:** 2026-11-16. **Nytt, separat uttryckligt MAIN V-beslut** inom användarens redan godkända **NTSC v0.18 R1-hårdvarudiagnostik**, GitHub [Issue #6](https://github.com/Odourman/let-me-out/issues/6). **EN ENDA ny körbar standard-F6/NTSC ROM högst** och **EXAKT TVÅ OLIKA låsta originalmasker**: en rättvänd stor man och en rättvänd stor kvinna. Inget tredje NPC-testobjekt, ingen ny sexmaskerskernel, ingen R1ba-portning/reparation eller implementation av spelet. Inget steg efter F7 får startas automatiskt.

### 0. Följ authoritative source och tidigare mottagningskontroll

1. Läs [MAIN V:s oberoende R1-F6-mottagning](MAIN_V_R1_F6_RECEIPT_INDEPENDENT_PIXEL_AUDIT_AND_F7_DECISION_2026-11-16.md) och den frysta [R1-F6 utvecklarrapporten](https://github.com/Odourman/let-me-out/blob/e45455e09e1d796e576b0012d96e5d817d6210c4/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F6.md). Bas: exakt fryst F6 commit `e45455e09e1d796e576b0012d96e5d817d6210c4`. Skapa ny **ISOLERAD branch** från denna; tillför endast `r1_f7_*`/ny F7-rapport/workflow, utan att röra ens en byte i F6/F5/F4/F3/F2/R1ba eller i `main`.
2. Låst `design/NPC_REFERENCE_8x9_masks.json` blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`, samma identiska `canon_masks.json` i F6-basen. **ALLT TOP-DOWN; ingen `[::-1]`.** Man `3C 3C 18 FF 18 24 24 42 42`, kvinna `3C 3C 18 FF 3C 7E 7E 24 24`.
3. Bevara F6:s VBLANK/HMOVE och alla nio synliga rader, P0 gul, M0 statiskt aktiv, brun PF två sidor, 262 NTSC samt P1 `NUSIZ1=$01`. Förbud mot P0/M0/PF-förlust, R3 högerdörr, gameplay/Y-frihet eller timingändringar utan ny separat MAIN-order.
4. Kontrollera `PR #7` fortfarande draft, `Issue #8` standby och projektets aktuella STATE högst upp. Full R1 fortfarande `BLOCKED / NOT ACCEPTED`.

### 1. EN ny fråga

Kan **två skilda källbaserade positionsväljare** (`X0_SELECT`, `X1_SELECT`) i **samma** exekverbara F6-ROM och samma 9-radersband välja respektive ursprungsbildmask X i fyra 2×2-kombinationer **oberoende av varandra**? Testa endast **två möjliga lägen för vardera**:
- `X0_SELECT=0` begär första `RESP1 c21`, `X0_SELECT=1` begär `c23`; detta är faktiska, redan framgångsrika F6-positionsfaser.
- `X1_SELECT=0` begär andra `RESP1 c32`; `X1_SELECT=1` begär **c33**, exakt en förregistrerad **oprövad** andra-kopieposition. Inte c34/c35/c36 eller fassvep.
- Endast fyra registerkombinationer **(c21,c32), (c23,c32), (c21,c33), (c23,c33)**, med i förväg deklarerade förväntade X-mål från F6 och en separat *OPRÖVAD HYPOTES* om kvinnans c33-X. Låt inte nya bilder användas för att efterhandsjustera förregistrerat resultat.
- Mät om `X0` ändras när `X0_SELECT` växlas *med X1_SELECT fixerad*, och `X1` ändras när `X1_SELECT` växlas *med X0_SELECT fixerad*; enbart fyra tidsstyrda **kopplade** formationsprofiler eller en FRAMELO-tabell utan två separata lagrade väljare är **inte** ett giltigt ortogonalitetsbevis.

**Preregistrerad, ännu inte mätt X-hypotes i Stella-crop 900×300:** från F6 vet vi två verkliga `X0=39/45` med kvinna `X1=99` vid c32. Vi föreslår att en senare c33-respons ger kvinna `X1≈105`; detta är **inte verifierat** och första mannens X kan störas av den senare andra-fasen, så MAIN tillåter ett i förväg bestämt `F7_DISCRIMINATING_FAIL` utan att "rädda" utfallet med fler varianter.

| RAM-bitar `X0_SELECT,X1_SELECT` | Första/andra RESP1 per rad | Prereg modell: P1-crop (man,kvinna) |
|---|---|---|
| `00` | `c21/c32` | `(39,99)` från F6 |
| `10` | `c23/c32` | `(45,99)` från F6 |
| `01` | `c21/c33` | `(39,105)` **NY HYPOTES** |
| `11` | `c23/c33` | `(45,105)` **NY HYPOTES** |

**Hård framgångsklass:** samma ROM ska visa 4 **källkorrekta** olika bitpar där varje bit orsakar en **egen verklig bildpositionsskillnad** medan den andra figuren förblir pixelekvivalent i de två motsatta testparen; båda 9-radersbitmapparna och övriga objekt måste vara intakta. Även positivt resultat heter bara `F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`. **INTE** två *godtyckligt fria* X, inte sex P1 i samma rasterband, inte VDELY och inte full R1.

### 2. G0 – SOURCE ONLY före ens ett enda nytt ROM-bygge

Använd exakt F6:s redan verifierade assemblerupplägg som **READ-ONLY REFERENS**. Genomför två oberoende källanalysdelar utan att köra Stella:
1. Kartlägg källinstruktioner/opkoder, cycle count inklusive 4-cykels `STA RESP1,X`-variant och `GRP1`-deadline för andra reset `c33`, alltid första som `c21` eller `c23`, per varje nio originalrader samt första/föregående/efterföljande rasterrad. Kontrollera alla fyra unrolled branches max **76 CPU-cykler**, sista `WSYNC` och bank-/ROM-budget inom 16KiB F6. **Inga nya TIA-objekt och ingen självmodifierande ROM.**
2. Deklarera två verkligt **separata RAM-bitar** och deras independent-update och selection-API (t.ex. separata zero-page-adresser eller två namngivna bitmasker). Förbered en automatisk **konsekutiv fyralägessekvens** där de två bitarna oberoende kan vara vardera 0 eller 1, med bevarade lägen om en bit varierar; räkna byte/cykler för selektion **före** nio synliga P1-rader. Exakt 4 förkompilerade nio-radersvarianter får förekomma som intern data/code i den ENDA ROM:en, inte som fyra olika ROM:er. Märk detta `2×2 BINARY RUNTIME SELECTABILITY` och inte fri numerisk X.

Om något hörn kräver >76 cykler per P1-rad, rubbar P0/M0/PF eller kräver OUPPSKATTAD fyrlägenstiming, **STOPP SOURCE_ONLY_INFEASIBLE** och leverera bara källrapport. Ingen alternativ bytevariant, annan kopie-/NUSIZ-familj eller större ROM-gren.

### 3. G1 – EN ny F6/NTSC ROM, fyra tillstånd, minst 64 autentiska Stella-råbilder

**Högst 1 NY 16 384-byte standard F6 ROM** genereras och körs, och **endast** efter grön G0. För att garantera RAM-selektorers oberoende och inte bara påstå fyra profiler:
- Visa `X0_SELECT` och `X1_SELECT` som **separata lagrade RAM-värden**, att båda används oberoende av varandra för att välja fyra 9-radersutmatningssekvenser; selektionskod sker före P1:s synliga raster. Beskriv två olika sekvenser med `X0_SELECT` växlad medan `X1_SELECT` konstant och vice versa.
- Testa **00 → 10 → 00 → 01 → 11 → 01 → 00** som en deterministisk sekvens eller likvärdig förregistrerad sekvens som innehåller båda bitars oberoende ändringar; **minst 16 efter varandra följande genuina Stella 6.7.1-bilder PER tillstånd**, samtliga tillstånd nådda i SAMMA ROM. Totalt **minst 64 olika frameindex**, inte upprepningar av identiska PNG som kallas flera frames. Spara exakt följd och RAM-bitvärden samt faktiskt mode/PC/scanline med debuggertraps eller tydlig F6-basrapport-trace som skiljer dessa fyra.
- Kontrollerna måste läsa **direkt top-down M/F från låst canon**, aldrig `R1ba[::-1]`. Ett fristående algoritmiskt oracle ska avkoda alla verkliga vita pixlar (två croppixlar/bit), finna verkliga M/F-X, 0 extra/missande och korrekt nio-radersorientering i **varje** bild. Y-rader, gult P0, skott M0, brun PF och verklig NTSC 262 måste vara oförändrade i varje test. Även oberoende radbitmap/XOR-check och en märkt syntetisk negativ mutant som båda kontroller avvisar.
- Förregistrera om båda figurerna faktiskt ändrar X **oberoende**. Om `c33` ger identiskt X=99, flyttar X0, klipper masken eller korrumperar nine-row bandet ska ett klart **NEGATIVE GATE** rapporteras och ingen spontan c34-sweep eller femte ROM byggas.
- Få en autentisk PC/bank/scanline/CPU-cycle/TIA color-clock screenshot för de två RESP1 och GRP1 i minst ett tillstånd per c21/c23 och per c32/c33; cykler från enbart kod/listning måste märkas **STATIC_ONLY**. Dokumentera `WSYNC` under verklig frame som nästa scanline/c0, inte falskt verklig c38/c39.
- Fullständig ZIP med verkliga ROM/SHA + EXAKT TVÅ ursprungliga 8×9-masker, återgivna i FYRA positionskombinationer + ASM/list/sym, RAM-värden och generatorkod, råa 64+ frame SHA, autentiska debugger full GUI, trapbilder, negativ mutation, en separat JSON sanningsmatris 4 kombinationer och filer som reproducerar **utan** att röra ursprungliga F6. Upload korrekt projektmapp `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`; ZIP CRC och per-file SHA-manifest samt Actions green/red-run-id.

### 4. HÅRDA GRÄNSER och nästa huvudbeslut

**Stoppa efter G0 source-only infeasible, eller den ENDA ROM:en plus upp till en full verifieringssamling.** F7 får rapportera `F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS`, `F7_ORTHOGONALITY_FAIL`, `F7_SOURCE_ONLY_INFEASIBLE` eller `F7_INCONCLUSIVE`, och ska alltid skriva `ARBITRARY_TWO_X_NOT_PROVEN / SIX_FREE_XY_NOT_PROVEN / FULL_R1_BLOCKED_NOT_ACCEPTED`.

**Inga fler än två sprites, inga variabla Y, inga sex NPC:s same-Y, ingen R1ba-fix, R1+R3/R2/R4, keys/hud/GAME OVER, PAL, F6SC/ARM/mapperbyte, fullspel, grafikändring, PR #7-merge, eller oberoende VERIFICATION.** Ingen F8 eller senare teknisk cutover utan separat uttryckligt MAIN V-beslut. F7:s slutleverans är en fryst `rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F7.md` och komplett ZIP i Google Drive. Låt F5/F6-resultaten stå orörda; utvecklaren avslutar sitt uppdrag efter leverans.

**Syftet är att skilja en faktisk 2×2 oberoende runtime-väljarmöjlighet från rena profiler med ihopkopplade X-värden, inte att härleda sexgodkännande från en tvåmaskersskiss.**
