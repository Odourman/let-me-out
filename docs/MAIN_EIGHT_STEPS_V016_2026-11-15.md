# MAIN v0.16 – Åtta fullföljda design- och analyssteg

**Datum:** 2026-11-15. **Projekt:** Atari 2600 – Let Me Out!, endast detta projekt. **Ingen 6502-kodning, ROM, Stella eller independent VERIFICATION genomförd.**

**Användarens uppdrag:** Fria händer att genomföra de första åtta momenten i [den godkända 10-stegsplanen](MAIN_STATUS_NEXT_10_2026-11-15.md) och följa MAIN:s rekommendationer. Den tidigare spärren mot ROM-implementation gäller fortsatt.

## Genomförda analyser

| Steg | Modell/underlag | MAIN:s rekommendation och status |
|---|---|---|
| 1. Lång nyckelskymning | 160 abstrakta femandroidförlopp, 40 frön × 4 kartor, 140 logiska steg | Behåll **godkända O1**. En stillastående android kan i princip dölja nyckeln på obestämd tid; kräver framtida mänskligt speltest, inte en tyst blinkregel. |
| 2. Rastervärstafall | Fyra geometriska scenarier med sex androidankare på samma höjdband. 6+spelare+skott=8 eller 5+spelare+nyckel+skott=8 logiska objekt | **Högsta tekniska risk.** 76 CPU-cykler/scanline och få TIA-objekt; modell bevisar inte grafiktiming. Testa båda. |
| 3. Enbart högerdörr | 4/4 kartor har dörr vid x39, y9–12 och stängd vänsterkant | Framtida teknisk testordning: korrekt högeröppning → orange kant → svart nyckelhål. **V2B är godkänt visuellt mål**, PF0-metod inte verifierad. |
| 4. Nyckelmask | K11 (8×11, 41 pixlar) jämfört med K09 (8×9, 34 pixlar) | **K11 som läsbarhetsreferens**, **K09 teknisk reserv**; djupguld endast RGB-färgtest, inte Atari-färgkod. |
| 5. AI P2/J2 | **480 prov:** 24 frön × 4 kartor × 5 parametriseringar, stillastående mål | **P2/J2 1/8 och roterande tur** fortsatt huvudtestkandidat. I modellen 5,81/6 nådde nära målet; andra varianter 5,74–5,90. Inget spelsäkerhetsbevis. |
| 6. Startpositioner | Exakt **64 045** sexkombinationer ur fyra tidigare pooler, S0 vs hypotetiskt S1-radiusfilter | **Behåll S0**. S1 ska testas först mot verklig tidig dödlighet när kod är separat godkänd. |
| 7. Svårighetskurva | 48 abstrakta nivåer för C-1 och en mildare C-soft | **C-1** kvar som huvudkandidat. Rekommendation: bara lyckad utgång räknar upp svårighetssteget; **inte godkänd regel**. |
| 8. Poäng/HUD | Sex poängkedjor plus extra-livstest: 480→455→505→680 ger **ett** extraliv | **HUD-A** som testförslag: score och liv under spel, highscore på start/game-over. Poängen och extralivströsklarna ändras inte. |

## Fördjupad statistik, tolkning och begränsningar

**Nyckel, abstrakta modellsteg:** längst observerad sammanhängande 2×2-överlappning A01=9, B01=11, C02=17, D01=19. De är varken sekunder, bildrutor eller exakt visuell osynlighet. En inaktiv android kan i princip blockera utan tidsgräns.

**AI:** basparametrar P2/J2 med 1/8 och roterande tur gav per karta A01=5,96, B01=5,46, C02=5,92, D01=5,92 androiders närmande av sex, vid **stillastående mål nära utgången** och inom två gridsteg. 24 frön per karta. Beteendet hos rörlig mänsklig spelare är otestat.

**S0-startval med nära robot (<12 fyrvägssteg):** A01 68,07 %, B01 0 %, C02 73,04 %, D01 65,71 %. Detta är antal **kombinationer** som innehåller en nära startpunkt, **inte** sannolikhet att spelaren dör. S1 kvarstår som en icke godkänd kandidat.

**Poäng vid noll startpoäng och en till sex dödade androids:** 225 / 210 / 195 / 180 / 165 / 150 efter nyckel och faktisk rumsutgång. Vid redan intjänade 250 poäng är rumsnettot +200 / +160 / +120 / +80 / +40 / +0 eftersom minuspoäng då faktiskt dras av. Extraliv vid 500, 1500, 2500 ... var och en högst en gång.

## Vad är godkänt, vad är INTE godkänt?

- **BESLUT:** sex androider; K1/E1; kartuppsättning A01/B01/C02/D01 som planerad bas; V2B/GULD visuella mål; O1 med tillfällig nyckelskymning; lite flimmer är acceptabelt utan satt numerisk tolerans; ursprunglig score/highscore- och skottrutin.
- **ENDAST TESTKANDIDAT:** 1/8 P2, J2:s omväg, turordning, S0/S1-jämförelsen, C-1/C-soft, K11/K09, NTSC/PAL-färger, PF0-dörrlösning, HUD-A.
- **INTE VERIFIERAT:** sex sprites på samma rasterhöjd, skott och nyckel/port samtidigt, flimmermängd, riktig timing, hårdvarukollisioner och spelbalans.

## Reproducerbara leveranser
- [Fullständigt v0.16-paket på Google Drive](https://drive.google.com/file/d/1YrXJtgqvY9bjaSKKxoyb7hvs7ye5msx-/view?usp=drivesdk) med **38 filer**, inklusive åtta separata stegrapporter, originala schematiska PNG, kartdata och källskript, 12 CSV-filer, JSON-resultat och SHA-256-manifest.
- [Mobilanpassad v0.16-PDF (6 sidor)](https://drive.google.com/file/d/1RbjgcJs_oTlYIqeHF3tZk6PZawRIbiZu/view?usp=drivesdk).
- `REPRODUCERA_OFFLINE_ANALYS.py` har körts på nytt med deterministiskt oförändrade centrala CSV/JSON-resultat; ZIP-innehållets checksummeringar kontrollerade.
- `TESTKONTRAKT_22_SCENARIER.csv` innehåller **22 framtida hårdvarutestfall**, samtliga märkta **NOT_RUN_IN_ROM**.
- [Godkänt O1 och tidigare 10-stegsplan](MAIN_STATUS_NEXT_10_2026-11-15.md).

## Kvarvarande planpunkter (9–10)

9. Presentation och ljud: kort start/game-over och kärnljud utan att lägga extra rasterbörda.  
10. Samlad teknisk grind: konsolidera endast godkända beslut och definiera ett litet framtida ROM-uppdrag med **oberoende** VERIFICATION. **Grinden ger inte kodstart i sig.**

## Projektisolation

Detta gäller **enbart Let Me Out!** och dess egna Google Drive-mapp och GitHub-repository. **The Cabin och I Love a Fish lämnas helt orörda; Linear används inte för detta projekt.**
