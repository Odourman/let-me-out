# LET ME OUT! – MAIN VII G5AC: beslutsberedskap för ETT minimalt TIA-fas-/kopieprov

> **SENARE BESLUT LM-D21 (2026-11-17):** G5AC var ett legitimt **beslutsutkast** när det skrevs, men användaren har därefter uttryckligen godkänt **en enda specifik** TIA-fas-/kopie-mät-ROM genom "Gör så". För exakt nytt aktivt uppdrag och spärrar läs [G5AD auktoriserad teknisk order](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5AD_MAIN_VII_ONE_TIA_PHASE_CALIBRATION_ROM_EXPLICIT_USER_AUTHORIZATION_2026-11-17.md) och [Issue #13](https://github.com/Odourman/let-me-out/issues/13). **Detta G5AC-utkast är historik, inte en andra parallell ROM-order**. Full H4/G6/F12/fem-NPC/S05 och oberoende Verification förblir EJ auktoriserade.

**Datum:** 2026-11-17. **Status:** `SOURCE_ONLY_DECISION_READY_NOT_ORDERED`. **Ej** G0-pånyttstart, G1/G6/F12, ROM/ASM/DASM/Stella-körning, Verification II, PR-merge eller speldesignändring.

## 1. Varför detta är rätt fråga efter G5AA – och vad det INTE är
[ROM DEVELOPMENT III G5Z](https://github.com/Odourman/let-me-out/blob/8c7cef622ebaa6543a3f044ddf50d21024b1b978/rom/g5z_g0_h4_one/TO_MAIN_G5Z_G0_H4_ONE.md) slutade **`G0_INCONCLUSIVE_NO_ROM`**, [MAIN G5AA](G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md) mottog det som korrekt stopp. Vi vet inte faktiska `RESP0/1`→intern sprite-START/GRP-latch under aktiv rendering, samspel mellan `NUSIZ0=$02` och M0-kopior, eller `ENAM0`-gate i ett verkligt nio-radersband. Att repetera full H4-källanalys utan ny faktisk TIA-signal skulle sannolikt återge samma osäkerhet.

**Förslag enbart:** om användaren **senare uttryckligen godkänner ett nytt, begränsat ROM-/Stella-uppdrag**, pröva **ett enda isolerat standard-F6 NTSC-kalibreringspaket** som mäter dessa mekanismer separat. Det är **inte** nästa H4-ONE full kernel eller fem-NPC-rom. Ett godkänt eller misslyckat enskilt kalibreringsfall kan aldrig få `G5_PASS`.

## 2. Förregistrerade kalibreringsfrågor före eventuell ny kod
| ID | Kontrollerad hypotes/förändring | Observerbar skillnad som krävs | Varning |
|---|---|---|---|
| TIA-C0 | En enda P0 bitmap med numeriskt RAM-X (kontroll) | Faktiskt pixel-X, maskens nio rader och stabilt START-fönster | Ingen full datastyrd multiplexer |
| TIA-C1 | `RESP0` efter påbörjad P0-bitmap, i både vänster→höger och höger→vänster identitetsordning | När en originalmask klipps, felvänds, ghostar eller repositioneras enligt faktisk CPU-write-cykel kontra pixelCC | Bryter aldrig originalmask-/identitetskrav och betecknar inte fail som pass |
| TIA-C2 | `NUSIZ0=$02` P0-kopieffekt medan en **enskild** M0 är aktiverad i samma band | En eller flera synliga M0-pixlar/extra kopior; mät fysisk CC och rörelse för varje kopia | Ingen M0 på tidigare y som falsk same-Y-pass |
| TIA-C3 | Jämför C2 med tidsstyrd `ENAM0`-avslutning eller andra tydligt avgränsade registerfaser | Om ett **enda** M0 får ligga kvar i avsett CC-fönster utan ny ghost och utan P0-klippning | Fungerande M0-isolering är inte H4 |
| TIA-C4 | `GRP0/GRP1` last/latch före och nära synlig START i enstaka kontrollmasker | Verklig fördröjning/ghost/copy-skifte och sista giltiga byte-skrivtid i CPU c och pixel-CC | Kan inte lova all samtidig två-P1-H4 geometri |
| TIA-N1 | Negativ `COLUP0` simultan vit P0 + separat gul M0 vid **samma pixel** | Begränsad färgdelningskonflikt ska synas eller förstås korrekt | Ett misslyckande här är förväntat, inte universellt Atari-NO-GO |

**Viktigt:** Tabellen definierar vad som måste gå att falsifiera. Den anger **inte** redan uppmätta CPU- eller CC-värden och **inte** en ny förenklad rendering godkänd av användaren. Minsta uppsättning scenfall och om den faktiskt går att få in i **en** ROM ska kontrolleras på källnivå innan man ens föreslår ett konkret programmeringsmandat.

## 3. Hårda gränser för en eventuell, separat auktoriserad specialistorder
- En enda explicit avgränsad standard-F6/NTSC diagnostisk ROM **endast om ny användarauktorisation faktiskt ges**; inga ändringar av originalkartor, originalmasker, spelregler eller historiska frysta test-ROM; arbetet på separat branch utan merge.
- Ingen modifikation av framtida fem-NPC-målet, fri X/Y, accepterad O1/LM-D13, orange P1-dörr eller framtida godkända rumskartor.
- Isolera en registerfamilj i taget. Om aktivering av PF/M0/andra objekt behövs för ett visst test, etiketteras detta explicit per kontrollfall. Ett kontrollexperiment med PF=0 får inte senare sägas ha visat H4 med faktiska bruna väggar.
- Förregistrera synliga CC-mål, numeriska RAM-X, förväntade bitmaprader och maskfärg; välj nödvändiga kontrollfall så att resultaten **kan** skilja mellan hypotetiskt säker och osäker START/GRP/ENAM-timing. Undvik en "många ROM-varianter tills vi får en snygg screenshot"-slinga.
- Planerad evidens från en **framtida faktiskt körd** kontroll: full källcommit + `.bin` SHA256, exakt Stella-version, NTSC frame/scanline, CPU PC/cykel och riktiga register- och TIA colorclock spår; rå pixel mask/position och korrekt 8×9-orientering; fryst filindex och reproduktionsrecept. Egenkontroll av ROM DEVELOPMENT III är INTE oberoende Verification II.
- Klassificera varje faktisk kontroll som `OBSERVED_EXPECTED`, `OBSERVED_UNEXPECTED`, `NOT_DETERMINABLE` med verifierbar mätning och slutsats begränsad till kontrollens eget register/timing-scope; ingen "H4_PASS" utan full separat H4-order.

## 4. Vad MAIN rekommenderar före beslutet
1. Kräv en kort utförarbekräftelse på **vad en minimal fysisk mätning kan skilja åt** i G5Z:s befintliga okända `RESP/GRP/NUSIZ0/ENAM0`-faser. Råa Stella-traces måste vara instrumenterbara, annars är ROM-beställningen dålig.
2. Om ovanstående uppfylls är en **enda mät-ROM** betydligt mer informativ än ännu en bred source-only H4-omgång, men den kan sluta negativt eller inkonklusivt. Samtidig P1/key/door, femfienders-WC och 8×9-spawn-validation är fortfarande andra grindar.
3. **Stopp här:** detta dokument är **beslutsberedskap inom MAIN**, inte uppdrag åt ROM DEVELOPMENT III eller någon annan specialist. **G5_FORMAL_OPEN, G1/G6/F12/NEW_ROM/VERIFICATION/PR_MERGE_NOT_AUTHORIZED** tills en ny konkret användarauktorisation finns.

Källankare: [G5AA](G5AA_MAIN_VII_G5Z_G0_INCONCLUSIVE_SOURCE_ONLY_RECEIPT_AND_NEXT_DECISION_2026-11-17.md), [G5Y testplan](G5Y_MAIN_VII_FALSIFIABLE_HARDWARE_TEST_PLAN_H4_ONE_S05_FIVE_NPC_NOT_AUTHORIZED_2026-11-17.md), [G4 prereg](G4_PREREGISTERED_PHYSICAL_HYPOTHESIS_2026-11-17.md), [G2 negativa tester](G2_NEGATIVE_TESTS_AND_NONREPEAT_RULES_2026-11-17.md).
