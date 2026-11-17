# LET ME OUT! - GRAPHICS till ny ren chatt: formell handoff

**Datum:** 2026-11-17. **Roll:** GRAPHICS (avslutad studiefas). **Mottagare:** ny dedikerad GRAPHICS-chatt, förslagsvis `GRAPHICS II`.
**Klassning:** administrativ överlämning på användarens uppdrag. **Ingen ny grafikorder, ROM-auktorisation, implementation eller canonändring.**

## 1. Mandat och aktuellt beslut

MAIN V har mottagit och självständigt granskat de sex avgränsade grafikstudierna. **Ingen GRAPHICS-version eller ytterligare grafikstudie är auktoriserad nu.** GRAPHICS ska vänta på ett konkret nytt designbehov eller tekniska resultat från faktisk Atari-kernel och en separat uttrycklig MAIN V-order.

**Bindande stoppstatus:** `GRAPHICS STUDY COMPLETE / CANDIDATES NOT APPROVED / NOT STELLA TESTED`.

Accepterad studie/korrekta filhashar betyder inte användargodkänd grafik, att ett Atari TIA-objekt kan visa den, eller att någon får implementera den.

## 2. Källordning och verkliga ingångar

**Repository:** https://github.com/Odourman/let-me-out
**Dedikerad Google Drive-mapp:** https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u
**Ursprunglig 57-beslutshandoff med användarens skisser:** https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view

Läs följande i live-repot:
- `docs/CURRENT_PROJECT_STATE_2026-11-15.md` - **senaste översta sakligt tillämpliga sektionen** är aktuell, inte datumen i filnamnet eller äldre historiska avsnitt.
- `docs/MAIN_DECISION_LEDGER_SUPPLEMENT_2026-11-15.md` och originalets `02_MASTER_SPEC.md`, `03_DECISIONS.csv`, `07_DECISION_HISTORY.md`.
- `docs/MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md` - den äldre rollbeskrivningen gäller som arbetsmetod, **inte** som ny aktiv uppdragslista.
- `design/NPC_REFERENCE_8x9_masks.json` - fyra låsta originalmasker. Git-blob vid migrering `058800a4c1904d1ff289e7e61b3902aa111ba16d`, filbytes-SHA256 `1ace693e093be62d256b2d1f573e5ef8bc540e8ec8daae1b245ebdfb435c8e38`.
- `design/PLANERADE_RUMSKARTOR_V011.json` - ursprunglig planerad C02 (40x22, stängd vänsterkant, högerdörr x=39 och y=9..12), ingen `C_OPEN`-cutover.
- `docs/GAME_OVER_RESET_ONLY_DECISION_2026-11-15.md` och `docs/KEY_AND_DOOR_VISUAL_TARGET_V013.md`.

**Prioriteringsprincip:** direkta användarbeslut/originalmaterial och senare uttryckligen auktoritativa MAIN-beslut före rådgivande förslag, äldre mottagningar och forskning. En senare teknisk utvecklarrapport ger inte en grafikfullmakt. Vid motstridiga källor: ange exakt konflikt, låt MAIN avgöra. **Memory, tidigare chatt och ett påstått uppladdat filnamn är inte bevis på aktuell projektstatus eller filinnehåll.**

## 3. Mottagna grafikstudier (alla avslutade, ingen slutgodkänd)

| Studie | MAIN:s preliminära utgångspunkt | Kritisk begränsning | Kontrollerad arkivkälla |
|---|---|---|---|
| PLAYER SPRITE v0.3 | `V03_B` jämförelsesprite | `8x9 WEAPON READABILITY STILL FAILED`; varken slutlig P0 eller Stella-pass | [Drive ZIP](https://drive.google.com/file/d/1AVQhwVEpb5Bo8XssSro6JARHe-G3LE5C/view), 297750 byte, 69 poster, SHA256 `d3db276b032b9a9d0b256a8766fbc65313dd7040162b2e8849240c79cbc28500` |
| ANDROID WALK FRAME B v0.1 | Stora B rimliga designkandidater | De små har svag gång, särskilt liten kvinna; A exakt oförändrade. Glidande förflyttning tillåten reserv | [Drive ZIP](https://drive.google.com/file/d/10LToEGV-KGQyB4LpixIMV-q02S6qujAx/view), 201031 byte, 84 poster, SHA256 `a7c64912f24b0ceada20aac90d99c738882c24ad2730d347bcc71141713e9c3f` |
| COMMON DEATH v0.1 | `D1` pixeldissolve | `D2` reserv; nyckel syns **först efter hela animationen** och EMPTY, inte under faserna | [Drive ZIP](https://drive.google.com/file/d/1zujHqITl_UJYWSb2aRPxJZoL7EpqA0bP/view), 385148 byte, 273 poster, SHA256 `aa1478e3476d5b6afaf1a2d4e8843247d65685ac030921188697bdfa8f0ca338` |
| GAME OVER IN ROOM v0.1 | `G2` | `G1` reserv; G2:s extra textgrafik saknar tekniskt TIA-/rasterbevis | [Drive ZIP](https://drive.google.com/file/d/1sky2m5Y8QG4oM0eRiL5HRE2FTOG4S32Y/view), 164694 byte, 41 poster, SHA256 `23afbe7804d76c1de91e9c31ccc02386a68dd8833b3305ea8374d94b529570f6` |
| KEY SPRITE v0.1 | `K09-R` 8x9 | `K11-R` 8x11 reserv; högre mask och TIA-färg är inte godkända. O1-skymning flyttar aldrig nyckeln | [Drive ZIP](https://drive.google.com/file/d/1y7SaRC4nJ9NCZ5k918Tp8yhz2nO5MkFJ/view), 297376 byte, 118 poster, SHA256 `ef0ed4c378e41363f29804b8ed1ff45c260bafb4b173716d06a38e1e74e9e975` |
| SCORE & LIVES HUD v0.1 | `H1` toppband | `H2` reserv med olöst android-överlapp; H1:s 13 extra synliga rader är **obevisade**, ingen final HUD-font | [Drive ZIP](https://drive.google.com/file/d/1onEQZXXAK2GM7atBr3qOd1BdJCNBzPU-/view), 317321 byte, 134 poster, SHA256 `de9780f60c1caf1d0a5319d20d4302717562f60624d79b44b291c1d048945b38` |

**MAIN-mottagning på GitHub:**
- `docs/MAIN_V_GRAPHICS_PLAYER_SPRITE_V03_RECEIPT_2026-11-16.md`
- `docs/MAIN_V_ANDROID_WALK_FRAME_B_V01_RECEIPT_2026-11-16.md`
- `docs/MAIN_V_COMMON_ANDROID_DEATH_ANIMATION_V01_RECEIPT_2026-11-16.md`
- `docs/MAIN_V_GAME_OVER_IN_ROOM_VISUAL_V01_RECEIPT_2026-11-16.md`
- `docs/MAIN_V_KEY_SPRITE_READABILITY_V01_RECEIPT_2026-11-16.md`
- HUD: [MAIN V:s explicita Drive-mottagning och pausbeslut](https://docs.google.com/document/d/1jFhNAs5kPwlGZFIz0q7mmtXja5kII5QDEHPOpMGMe3I/edit), 132/132 hashkontroller och 40/40 poäng-/livbilder.

Alla sex är `GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD`. Inget ingår automatiskt i spelets godkända slutgrafik. Tidigare leveranser och deras maskrader bevaras oförändrade.

## 4. Originalidentitet och beslutad funktion som ska skyddas

- Sex **vita människoliknande** androider: 2 stora män, 2 stora kvinnor, 1 liten man och 1 liten kvinna. Fyra låsta original-Frame-A-masker 8x9; små har bara 6 synliga rader (y=2..7), stora 9. Inga uppenbara robotdetaljer eller minskat antal.
- **Gul** spelare med hatt och vapen, visuellt samma höjd som stora androider, slutlig bitmap ej bestämd.
- **Bruna väggar**, mörk bakgrund, planerad C02 bevaras, **högerutgång endast till höger**, orange port med svart nyckelhål som separat användargodkänt visuellt mål.
- **Guldgul nyckel** med runt hål, kort skaft och små tänder; syns efter komplett nyckelbärares dödsanimation på dennes lagrade fallposition. Android får skymma den (O1) utan att flytta den.
- **Ingen separat startskärm.** GAME OVER i befintligt rum med växlande kontrast och blinkande slutpoäng; endast konsolens **RESET** startar om, **FIRE gör inte det**.
- Tre startliv; startpoäng 0, score aldrig under 0; -25 android, missat skott 0, +50 verklig nyckelhämtning, +100 verklig rumsutgång, +15 per överlevande android vid rumsutgång. Extraliv vid 500,1500,2500,... högst en gång per tröskel/omgång. Maxpoäng/maxliv/font/highscore-persistens fortfarande öppet.

## 5. Status i ROM-arbetet vid migrering (bara för orientering)

Den 17 november 2026 hade MAIN V mottagit R1-F10 SOURCE-ONLY: `F10_NO_CURRENT_F6_SIX_FREE_XY_ARCHITECTURE_PROVEN`. Full R1 fortfarande `BLOCKED / NOT ACCEPTED`. R1-F11 var separat, aktiv, begränsad ROM DEVELOPMENT II-ordrerad diagnostik (fyra originalmasker och numeriska RAM-X-positioner, en ROM högst efter G0); **det är INTE en GRAPHICS-order**. Kontrollera levande MAIN-status innan du nämner F11 i framtiden. PR #7 fortsatt draft/omerget; oberoende VERIFICATION Issue #8 standby vid tidpunkten.

Atari 2600: P0 spelare, P1/GRP1 multiplexade androider, M0 skott, PF väggar i aktuella diagnostiska studier; 76 CPU-cykler per scanline, 128-byte RIOT RAM, 262 NTSC-scanlines. PNG/GIF och SHA-verifiering är inte Stella-/TIA-/CPU-bevis och skapar inte lediga skärmrader.

## 6. Den nya chattens första meddelande och framtida arbetsflöde

Nya chatten ska genom **egna tool-anrop** kontrollera GitHub, Drive, den senaste statusfilen och denna handoff innan den redovisar: tillgång, gällande stoppstatus och kända osäkerheter. Ingen ny grafik skall genereras eller arkiveras på egen hand.

Vid eventuell framtida, konkret MAIN V-order: hämta HELA aktuell arbetsorder; identifiera exakt scope; kontrollera originalmasker, källhierarki och kernelbegränsningar; producera bara uttryckligen beställda grafikkandidater; skilj `VISUAL CANDIDATE` från `TECHNICALLY PROVEN`; verifiera och länka verkliga Drive-artefakter. Inga spontana v0.2, ROM-builds, PR-merge, egna grinds eller implementationer.

**Rollisolering:** GRAPHICS designar. MAIN V auktoriserar/koordinerar. ROM DEVELOPMENT II kodar endast eget scope. VERIFICATION granskar oberoende efter egen order. Ändra aldrig The Cabin, The Skraun, I Love a Fish eller Linear som bieffekt.

**Detta dokument flyttar inte ChatGPTs interna konversationshistorik.** Användaren skapar en ny chatt, klistrar in startprompten och den nya chatten läser de faktiskt publicerade projektfilerna.
