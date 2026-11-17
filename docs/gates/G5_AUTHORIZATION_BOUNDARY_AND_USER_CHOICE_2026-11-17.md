# LET ME OUT! – G5: bindande beslutsspärr och framtida scope (ingen canon-ändring)
**2026-11-17 · MAIN VI. Status: `G5_USER_DECISION_PENDING_NO_CANON_CHANGE`.**

Detta är en styrning av vad *inte* får påbörjas till följd av teknisk feasibility-granskning. [Fullständiga käll-/risk- och vägvalsbedömningen](G5_CANDID_FEASIBILITY_ASSESSMENT_AND_DECISION_BRIEF_2026-11-17.md) är separat och normativ som **MAIN:s rekommendation**, men **inte ett nytt användarbeslut**.

## 0B. G5F source-only fem-NPC/REF PF baserad på faktisk källanalys, INTE en kodorder

Efter användarens "Ok, fortsätt" färdigställde MAIN VI [G5F source-only arkitekturrevision](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5F_FIVE_ANDROID_REFLECTED_PF_DOOR_SOURCE_ONLY_ARCHITECTURE_2026-11-17.md) och [Drive fullständigt underlag](https://docs.google.com/document/d/1PAELvVABaDAVuhZILC1Czo5kEIiRGQV2IaZ1bdtKRNw/edit). Alla fyra kartor speglar vänsterhalvan på 18/22 rader, endast dörr x39/y9–12 avviker. Förslaget är `CTRLPF.REF`, latched återbruk av väggdata, eventuellt PF0-only högersidig override på dörrlinjerna samt befintligt P1-dörrmotiv med svart utskuret nyckelhål. 5-NPC-maskradlast 3/3/5/5/5/5/5/5/3; F11 och P0/M0-färgkonflikter kvarstår. **Ingen G6/ROM-implementationsorder, ändrad v0.18-acceptans eller ny teknisk PASS följer av denna dokumentation.** Formellt G5-beslut, fem-NPC cutover av historisk R1/R2 och eventuella visuella waivers är fortfarande användarägt.

## 0A. Ny användarinitierad fem-NPC- och Video Chess-forskningskandidat (2026-11-17)

[GitHub dokument med användarens femandroidsförslag, Berzerk-jämförelse, och Video Chess/Venetian Blinds för guldnyckel + högerdörr](../MAIN_VI_FIVE_ANDROID_BERZERK_VIDEO_CHESS_RESEARCH_DIRECTION_2026-11-17.md) · [arkiverad Google Drive-kopia](https://docs.google.com/document/d/1Iv9XrYt3CvkPNhiCGxSgEQSe0M91SHa4CHIjqP6YAA8/edit). Exakt kandidat: **2 large M + 1 large F + 1 small M + 1 small F = 5** (mot frysta 2M+2F+SM+SF=6). R2 blir hypotetiskt 4 kvarvarande NPC + nyckel om antalet ändras. Kandidat för nyckel/dörr: pröva omväxlande scanlines NÄR de ligger på samma höjd; jämför först med enkel Y-separerad spriteåteranvändning och PF-buren dörr. Tidigare android-Venetian-negativfall är inte automatiskt key/door-negativfall.

**Auktoritet:** användaren bad att minnas och arkivera förslagen, **INTE** uttryckligen att fastställa ny canon eller utfärda kodorder. Originalantal 6, R1/R2 acceptans, fyra 8×9 TOP-DOWN-masker och G5 PENDING USER kvarstår. Varken G6 eller någon annan implementation är beslutad.

## 1. De två möjliga framtida produktbesluten
**A – Atari 2600, ny visuell renderingspolicy.** Behåll sex logiska individuell X/Y NPC, fyra typers originalidentiteter, gul spelare, en projektil, fyra rum, högernyckeldörr, O1/K1/E1, poäng, liv, RESET-only och spelkänsla **som mål**. Användaren måste *se och uttryckligen godkänna* den föreslagna policyn för hur många NPC som får saknas/flickra/occluderas på överbelastad same-Y-rad och exakt vad original8×9-krav ska betyda för en överlagrad grafisk framställning. Varken ändrade exakta rumsrutor, begränsad NPC Y-mobilitet, annan dörrfärg eller reducerat antal NPC följer automatiskt.

**B – originalambition bibehålls, plattformsbyte till Atari 7800/MARIA.** Användaren behöver uttryckligen bestämma att Atari 2600-målmaskinen överges som leveransplattform. Exakta originalmasker, sex fria X/Y, fullfärgsguldkey och orange/black dörr blir då vidareförda designmål; 7800-renderingen och ROM/gameplay måste nyutvecklas separat och är inte verifierad ännu. Standard-F6-DASM/2600 TIA-resultat är forskningshistoria, **inte** en färdig 7800 implementation.

Den tidigare G4-"villkorad GO" för EN mikrofysik-uppgift är en **alternativ forskningsmetod om användaren önskar testa originalspecen lite till**, inte ett tredje automatiskt produktbeslut. Ett lyckat mikroprov har INTE visat sex NPC eller guldkey/door samtidigt; inte heller ska ett misslyckande automatiskt ändra canon.

## 2. Frågor som kräver uttrycklig framtida användarformulering
- Vilket är absolut viktigast: **Atari 2600 som hårdvara** eller **alla nuvarande samtidiga originalgrafikregler**?
- Om A väljs: exakt **flicker-/occlusion-policy** och vilken minsta läsbarhet som krävs, särskilt sex same-Y och gameplay-/collision-invariant, baserat på synliga testklipp innan godkännande.
- Om B väljs: uttryckligt målmaskins- och scopebyte; nytt ROM- och oberoende verification-upplägg.
- Om användaren vill fortsätta exakt 2600-forskning: explicit separat mikro-G6-order enligt [G4 DRAFT_NOT_AUTHORIZED](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md), med **G0 före bygg**, bounded exit och ett förhandsgodkänt kostnadsstopp.

**Nej till tysta antaganden** om "lite flimmer" = 10 Hz för en NPC, F6SC/ARM löser sprites, ändring 6→4 NPC, att nyckeln får vara brun eller att den vänstra väggen får öppnas.

## 3. Aktuell auktorisation och tekniskt tillstånd efter G5-analysen
| Del | Nuvarande faktiska status |
|---|---|
| **G1–G4** | Dokumentation/evidens/source-only analyser färdiga, ej ROM-PASS |
| **G5 feasibility-analys** | COMPLETE – ärlig 2600 produktplan bedöms **NO_GO med samtliga exakta krav samtidigt** (ingen universell omöjlighetssats) |
| **G5 val av canon/teknisk väg** | **PENDING USER DECISION** – inte godkänt/inte färdigt |
| **G6 nytt ROM-mikroprov/F12** | **NOT AUTHORIZED / NOT ORDERED** |
| **Full R1 och R2–R4** | BLOCKED / NOT ACCEPTED |
| **PR #7** | DRAFT, UNMERGED |
| **Issue #8** | Oberoende äldre fryst E02-baslinje, ej ny G5/future-ROM |
| **Andra projekt eller annan cartridge-mapper/PAL/fullspel** | INTE auktoriserade inom detta steg |

## 4. MAIN:s styrrekommendation
**Gör inget flerförgrenat F9–F12-probe-svep.** Pausa ytterligare grafikkernel-forskning tills användaren har valt vilken kompromiss de föredrar, eller har uttryckligen avgränsat att de vill lägga **EN sista** forskningsmikro på bevisning trots att det inte garanterar ett spel. Inga fullspelsfunktioner skall byggas i förtid mot en oföränderlig icke bevisad spritekernel.

**Bevara hela originalet.** Originalets 57 beslut och skisser, senare LM-D/Issue6, alla frysta ROMs, G1–G4 underlag och G5-bedömningen kvarstår oförändrade. Ingen gamla positiva/negativa bevis raderas. Huvudchattens nästa verkliga uppgift efter ett användarbeslut är ny, uttryckligen begränsad roadmap och separat rollordrade prov.

*Dokumentattest: MAIN VI, rådgivande produkt-/feasibility- och authority-gräns, inte användarsignerad canon.*
