# LET ME OUT! – G1: auktoritetsdifferens, supersession och öppna frågor
**MAIN VI · 17 november 2026 · dokumentgrind G1.** Typ: källbaserad kravförsoning, inte ny designauktorisation, inte ROM/Verifikation.

## 1. Exakt källa, integritet och beslutsordning
Ursprunglig Google Drive-fil: [LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view), 738586 byte, SHA-256 `f291d07af34e12866cd9785387e8ba1d320aa341b70e9646c28e3e0a78896ff4`. ZIP:s integritetstest PASS, 20/20 originalmanifestposter matchar SHA-256. `03_DECISIONS.csv`, SHA-256 `e0136b89195c567c33a7435896c77f57e44c0a66555d6fcefed3df81ae8614f1`, har exakt 57 numrerade poster 001–057 utan luckor. Tre användaroriginalskisser verifierade som närvarande i ZIP. Detta är originalspecifikations- och beslutskälla, **inte en färdig spel-ROM**.

Referensmaskerna `assets/NPC_REFERENCE_8x9_masks.json` är byteidentiska med GitHubs `design/NPC_REFERENCE_8x9_masks.json`: original SHA-256 `1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`; Git blob SHA-1 `058800a4c1904d1ff289e7e61b3902aa111ba16d`. Fyra typer, vardera 8×9 rader i TOP-DOWN-referens; M/F har 9 synliga bitmaprader, SM/SF 6 synliga (nollor rad 0,1,8). Referensmaskerna är **låst jämförelseunderlag i v0.18-diagnostik**, men originalfilen säger uttryckligen att de tidigare uppskattade pixelmockuperna **inte är ROM-verifierade** och inte automatiskt är slutgiltiga animeringsmasker för fullspelet. En framtida byte kräver spårbart designbeslut, inte tyst ersättning.

**Auktoritetsregel:** direkta användarbeslut, originalskisser och 57 originalposter; senare uttryckligt användarbeslut kan supersedera en specifik äldre regel; kompletterande beslutsregister och aktuell MAIN-status tolkar besluten; ROM Gate v0.18 Issue #6/acceptanskriterier styr exekveringsscope; forskning/offlinebilder får aldrig ge ny spelcanon. `docs/MAIN_STATUS_NEXT_10_2026-11-15.md`, `docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md` och `docs/APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md` innehåller äldre statusfraser om att ROM-prototypen är PAUSAD. Dessa statusfraser gäller sin historiska tidpunkt och **upphäver inte** senare Issue #6. Tekniska regler i dessa dokument kan fortfarande vara beslutade.

## 2. Faktiska supersessioner och skenbara motsägelser

| ID/källor | Äldre ordning/fakta | Senare bindande status | Praktisk hantering |
|---|---|---|---|
| ORIGINAL 005, tidigare 8 androids | Äldre spelutkast hade åtta | Original 005 beslöt exakt sex och markerar uttryckligen att åtta ersätts; LM-D01 bekräftar M,M,F,F,SM,SF | **Endast sex** vid rumsstart. Ingen fyra-/åtta-variant som slutspel utan användarbeslut |
| ORIGINAL 053 / `00_START_HERE.md` | ROM-kod/bygg/Stella pausad | **2026-11-15 Issue #6 auktoriserade uttryckligen R1–R4 NTSC v0.18-diagnostik**, ej fullspel | Märk äldre paus SUPERSEDED **för detta begränsade diagnostikscope**, inte generellt |
| ORIGINAL 054 / Issue #6 | 16KiB F6 endast rekommendation | Användaren tillät **16KiB F6 om tekniskt motiverat** för v0.18; standard-F6 användes i frysta experiment | Valet är **diagnostikformat**, inte ändrad slutspelsmapper/hårdvarupolicy; inget automatiskt F6SC/DPC+/ARM |
| ORIGINAL 011–012 / v0.11 / v0.19 | Fyra fasta labyrinter, speglade innerväggar | **Godkänd nyare designriktning: luftiga rum**. Exakta `A_OPEN_01..` är **kandidater**, inte godkänd ersättning av förut källvalda A01/B01/C02/D01. C02 valdes specifikt i v0.11 | Följ v0.11-källset vid spårbara R3-prov; ingen oannonserad kartcutover. Användarval av exakta v0.19-matriser återstår |
| ORIGINAL 016–018 / LM-D05 / v0.13 | En låst högerdörr, vänster stängd | **Orange markör och svart nyckelhål** godkända visuella mål; bägge försvinner vid unlock. Inget exakt bitmapp-/TIA-objekt-PASS | R3 D01/D02/D03 separat, brun V1 bara testbas, ej slutgiltig dörr |
| ORIGINAL 003 / LM-D02–03 | Gul människa med hatt/vapen | Gul spelare **lika stor synligt** som stora vita androider och inte större än dörröppningen. **Ingen fast slutbitmap** eller exakt kollisionsrektangel | Stresstesta jämförbar storlek, inte AI-förstoringsbild som Stella-proof |
| ORIGINAL 006–009 / LM-D01 | Fyra humanoidtyper, två gångframes om möjligt | Fyra originalmasker är exakta **diagnostiska top-down-referenser**. 2 gångframes fortfarande villkorat, glide uttrycklig reserv | Inte tyst förenkling av mask i R1. Färdiga grafikförslag senare är kandidater, inte ROM-canon |
| ORIGINAL 023–025 / O1 / K1 | Nyckel efter animation, stannar kvar, tas av spelare | **O1** android får visuellt skymma den men logiskt key-X/Y bevaras; **K1** om spawn under spelare får upptagning ske tidigast nästa uppdatering och +50 en gång | R2/R4 O1 och framtida gameplay-K1 skilda testgrindar |
| ORIGINAL 028–030,041 / E1 | Fredlig kontakt före första skott, därefter dödlig jakt; skott först vid samtidighet | **E1** dödlig kontakt från överlevande android avbryter riktig utpassage/bonus, men skottträff på samma android behandlas först | Framtida gameplay-tick-prioritet, inte ny R1–R4 gameplayorder |
| ORIGINAL 049 + senare GAME OVER | Tre liv, ny spelstart efter död | Ingen separat startskärm; GAME OVER i samma rum, **endast konsol RESET** kan starta om; FIRE får inte omstart | Senare fullspelsregel, ej v0.18-diagnostik |
| ORIGINAL 051–052 | Egen varierad kurva C; tolv-rumsvärden illustration | Exakt C-1 och dödens nivåeffekt fortfarande öppna | Behåll preliminärt, ingen hastighetspolicy väljs i G1 |
| ORIGINAL 055 / v0.19 skiss | Exakt mörk/svart bakgrund ej beslutad | Offlinev0.19 använder svart illustrativt | Fortfarande **ej låst faktisk bakgrund/TIA-färgkod** |
| ORIGINAL 056 / nuvarande MAIN | Nyckelljud beslutat, annan audio ej fastställt | Full ljudprofil alltjämt ej auktoriserad eller beslutad | Framtida gameplay, inte G1 eller v0.18 |
| ORIGINAL 057 / F9–F11/R1e–R1g | Nyckel/BALL-dörr/robotmultiplexning samtidigt obevisade | F9 tre binärt växlade RAM-X, R1e/f/g begränsade P0/P1-prover; F11 G0 FAIL | Fortsatt **full R1 BLOCKED**, R2/R3 tekniskt inte integrerade. Begränsad research får ej skriva över UNKNOWN |
| v0.11 kart- och collision offline | 2×2 fotankare, föreslagen 6×6 hitbox | Inget användarbeslut om exakt 6×6-rect eller färdig TIA-kollision | Logiskt samma hitbox mellan stor/liten android är bindande, dimension fortfarande öppen |
| O1 och C03 flimmer | Användaren accepterar lite, kort flimmer | **Ingen numerisk procent** och ingen generell NPC/NPC-occlusionwaiver | Mät faktisk läsbarhet; ingen 1/6-frame-cykel, försvunnet skott eller permanent dold NPC automatiskt accepterad |
| Issue #8 / F9/F11 | Äldre E02-verifikation planerad för commit 561d3ba | Issue #8 gäller just gammal fryst baseline, inte ny G1 eller F9-11 | Bevara oberoende roller och commitbindning; ingen felaktig ärvd PASS |
| `docs/MAIN_STATUS_NEXT_10_2026-11-15.md` / ny MAIN VI G1–G10 | Gammal lista om v0.6–v0.15 och paus | MAIN VI deep reassessment + A/B/C playbook är nuvarande **villkorade arbetsgrindar** | Historisk processbevarande, ingen automatisk G2 eller F12 |

## 3. G1 tydliga öppna frågor (inte tekniska bevis eller beslutsbegäran nu)
- **OPEN-DESIGN-01: exakt framtida rumsgeometri.** Användaren har godkänt luftiga rum som stil, men inte de exakta fyra v0.19-bitmaprutorna. Bas A01/B01/C02/D01 i v0.11 bevaras under rådande arbets- och diagnoskriterier. Kan avgöras först när ett reellt val behövs.
- **OPEN-DESIGN-02: NPC/NPC/p0-person pixelöverlappning.** För samma färg och exakt samma pixel på samma X/Y kan två skilda vita figurer inte visuellt särskiljas i en enda statisk slutbild. Detta är INTE samma sak som O1 nyckelskymning, och inget explicit userbeslut definierar full visuell NPC/NPC-occlusionprioritet. G3/G4 får analysera både pixelunion och individuell logik, men inte tyst acceptera en dold NPC som legitim.
- **OPEN-DESIGN-03: exakt spelarbitmap och hatch-/vapenläsbarhet.** Gul storlek och attribut bestämda; kandidat V03_B eller annan offlinekandidat är inte slutlig.
- **OPEN-DESIGN-04: K11 vs K09 (och senare K09-R), svart nyckelhålsmask, exakta NTSC/PAL-color codes.** Visuell form-/färgriktning beslut, men ingen pixel-/TIA-acceptans.
- **OPEN-DESIGN-05: kvalitativ kortvarig flickertolerans.** Ingen numerisk maxandel godkänd, och permanent oläsbar fiende eller M0-skott inte ett godkänt fall.
- **OPEN-DESIGN-06: AI C-1/P2/J2, exakta värden, S0/S1-spawns och dimensionsmått.** Endast framtida gameplay-canon/studier; dessa får inte påverka diagnostic stress eller förfalska fri X/Y.
- **OPEN-DESIGN-07: bakgrundsfärg, heltäckande audio, GAME OVER-färg-/blinkintervall och permanent highscore-persistens.** RESET-only-spelflödet är beslutat, effekterna ännu kandidater.
- **OPEN-TECH-08: full R1/R2/R3/R4 teknisk genomförbarhet.** Hittills R1 BLOCKED, F11 G0 FAIL/G1 NOT RUN, ingen fristående E02-godkänd full diagnostik. G2–G4 får inte upphöja detta till "no-go bevis" för all Atari 2600-hårdvara.

**Inga öppna poster kräver nya användarbeslut för att G1-dokumentationen ska slutföras**. Exakt acceptans för pixelöverlappning eller slutval av nya rum efterfrågas först om det blir en verklig blockerare i G3–G5 eller framtida grafik-/gameplaygate.

## 4. V0.18-scope, test-ID och G1/ROM-separation
[Issue #6](https://github.com/Odourman/let-me-out/issues/6) är den bindande användarauktorisationen för **enbart** NTSC R1–R4 diagnostik; [Scope](../ROM_GATE_V018_SCOPE.md), [Acceptance](../ROM_GATE_V018_ACCEPTANCE.md) och [T01–T16](../../planning/ROM_GATE_V018_TEST_MATRIX.csv) anger mål. R1: 6 android + gul spelare + aktiv skott, samma Y/spridd Y, korrekt fyra maskreferenser. R2: 5 + key + spelare + shot, O1. R3: endast högerdörr locked/open och orange/svart separat. R4: crossings och key-occlusion. E02: oberoende rebuild på exakt fryst commit/hash. Fullspel, PAL, ny mapper, nya fullspels-AI/score/lives/audio/HUD och kartbyte **ej auktoriserade**.

G1-registerfilen innehåller samtliga 57 originalbesluts-ID, de 11 senare LM-D-id, de 18 A/B/C/D/E-acceptans-id och 16 T01–T16 test-ID = **102 kravposter**. Det är en *normaliserad katalog* med originalkällpekare – det förstör inte originalets beslutsordalydelse. Varje original-ID visar `source_status`, `effective_status`, `scope` och `delta`. Se [G1_REQUIREMENTS_TRACE](G1_REQUIREMENTS_TRACE_2026-11-17.csv) och [G1_BASELINE_MANIFEST](G1_BASELINE_MANIFEST_2026-11-17.json).

## 5. Faktiskt projektläge vid G1, och beslut om nästa steg
- GitHub HEAD före G1: `a2dcc8b5faaae681cfd91e73b51f5eb155ff457e`. Issue #6 OPEN, PR #7 OPEN/DRAFT/UNMERGED, Issue #8 OPEN (gammal 561d3ba E02).
- Freeze F9 `c36982aef770af6cd3f68c2da37b8ed14aee2393`; F10 `ef854d7436f1e1650827e2e19cc1b3d33a17f054`; F11 `dfe21c80b7cbdcdd20138ebf5eadf4b89dbf0cc4`. Dessa ändras inte.
- **G1_STATUS:** `G1_DOCUMENTATION_COMPLETE_WITH_OPEN_ITEMS`, vilket är en **administrativ käll-/kravgrind, inte en ROM- eller gameplay-PASS**. Konflikter som kunde klaras med befintligt later authority är lösta, öppna userdesignval tydligt markerade; G1 kräver ingen ytterligare användarfråga just nu.
- **NÄSTA:** G2 är **endast nästa potentiella uppgift**, aldrig automatiskt startad här. G2 ska granska rådatan bakom R1e/R1f/R1g, F9/F11 och markera varje bevisklass. Ingen G6-ROM får initieras på den här leveransen.

## 6. Källor i prioriterad ordning
1. [Original ZIP med 57 originalposter, master spec och tre handskisser](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view).
2. [Kompletterande 11 besluts-ID](../MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md), [K1/E1](../APPROVED_EDGE_CASE_DECISIONS_K1_E1_2026-11-15.md), [O1 och historisk v0.15](../MAIN_STATUS_NEXT_10_2026-11-15.md), [GAME OVER/RESET](../GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md), [v0.13 key & door](../KEY_AND_DOOR_VISUAL_TARGET_V013.md).
3. [v0.11 kartset](../../design/PLANERADE_RUMSKARTOR_V011.json) och [v0.19 ännu ej slutgodkända kartor](../../design/OPEN_ROOMS_V019_40x22_CANDIDATES.json).
4. [Original 8×9-maskreferenser](../../design/NPC_REFERENCE_8x9_masks.json), [spelarskala](../MAIN_PLAYER_SCALE_V018_2026-11-15.md).
5. [Issue #6](https://github.com/Odourman/let-me-out/issues/6), [v0.18 acceptans](../ROM_GATE_V018_ACCEPTANCE.md), [v0.18 scope](../ROM_GATE_V018_SCOPE.md), [v0.18 testmatris](../../planning/ROM_GATE_V018_TEST_MATRIX.csv).
6. [MAIN VI aktuellt läge](../CURRENT_PROJECT_STATE_2026-11-15.md), [G1–G10 playbook](../MAIN_VI_G1_G10_CONTINGENCY_PLAYBOOK_A_B_C_2026-11-17.md).
