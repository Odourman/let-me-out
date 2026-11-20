# LET ME OUT! – MAIN XI:s mottagning av RESEARCH II:s fördjupning och uppdaterad V02-prioritet

Datum: 2026-11-20. Typ: `MAIN_REVIEWED_RESEARCH_ADVISORY_WITH_LIVE_ROM_RECONCILIATION`. Inget implementations-/G5-/Verification-PASS ges av forskning. Detta dokument är en MAIN-sammanställning och ersätter inte faktiska original eller senare liveleveranser.

## 1. Mottagen forskningsleverans och integritetskontroll

Användaren vidarebefordrade RESEARCH II:s `LET_ME_OUT_RESEARCH_II_DEEP_RESEARCH_2026-11-20(1).zip` med fullständig 16-avsnittsrapport, MAIN-action sheet, CSV-matriser och read-only-källanalyser. MAIN öppnade faktisk bifogad ZIP i körmiljön och kontrollerade:
- ZIP **16 filer**; ZIP CRC-test = PASS.
- ZIP SHA-256 från uppladdade bytes: `f5ce5a477b5f02f060a764fdb880515dbbb258b46c80bf08782cd969e9fb1cc9`.
- `SHA256SUMS.txt`: **15/15** interna filer verifierades PASS.
- `python offline_source_checks.py` kördes som SOURCE_ONLY. Nyckelbitmap `00 70 50 7E 24 04 00 00 00` har exakt **14 tända pixlar**; fem oberoende former bland fyra ger **1024 ordnade formkombinationer**. Statisk programkörning är **inte** fysisk DASM/TIA-/ROM-verifiering.
- Kontrollerade full `MAIN_XI_ACTION_SHEET_RESEARCH_ONLY_2026-11-20.md`, relevanta delar av fullrapport, 15 kandidatfamiljer, proveniensregister och negativa testlistan. Det levererade ZIP-paketet är en användarbifogad forskningsartefakt, inte en påstått GitHub-publicerad ZIP; detta är en mottagningssammanfattning.

Forskningsstatus `RESEARCH_COMPLETE / ADVISORY_ONLY`. RESEARCH II har inte auktoriserat eller utfört någon ROM-implementation, ingen Verification. Historiska 30 Atari-trick, 52 teknikmönster och 67 riskpunkter har granskats som **rådgivande material**, inte 82 unika nya metoder och inte ett allmänt hårdvaru-PASS.

## 2. Avgörande källfynd i den verkliga koden

`PrepareKeyAssist` i både `9acaeaf7aa65a3619c062b79f05780e9c5ca1867` och **senare** `4be191123f0e54b583fd72f6aef782be8ee84a2f` har i `prepare_key_assist.inc` **samma villkor**:
- `KeyState == 1`.
- `PY >= 159`; `PX >= 42` och `PX < 124`.
- `KeyY == 153`, `KeyX >= 44`.
- Shot aktivt kräver dessutom `BY >= 159`.

De faktiska underkända `crowd.py --key-cases`-fixturerna har `PY=151`, `KeyX=85`, `KeyY=153`; `floor-key-player-separated-x` med `PX=24` bryter två villkor, `floor-key-player-in-band` med `PX=60` bryter `PY`-villkoret. **Detta bevisar att just specialassistenten avvisas innan sin P1-skrivväg**, inte att en enkel sänkning av villkoret skulle vara korrekt eller att det är enda orsaken till 0/14. Avgörande krav: faktisk TIA/GRP/RESP/VDEL/latch/colorclock-kedja, gul P0, 14/14 guldkontur och ingen ny vit/gul/brun förlust.

Källan `G5BE ITER6` [Issue #30](https://github.com/Odourman/let-me-out/issues/30#issuecomment-7001424130) visar fem X med begränsad topologi/Y-domän och negativt tätare X-fall. Kan informera verklig V02-same-Y-scheduler men **visar inte** fem fria NPC X/Y integrerat i V02. Raiders/Berzerk/Space Invaders/Video Chess och stack-/Venetian-varianter är **tekniska analogier**, inte automatiska PASS och inte licensfri kopierbar kod.

## 3. Viktig live-uppdatering EFTER forskningsrapportens 9aca-snapshot

Vid MAIN:s mottagning finns **nyare** [utvecklarleverans TO_MAIN_V02_INNER_RENDER_CONFLICT_REPAIR](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7042654133) i Issue #31 på fryst commit `4be191123f0e54b583fd72f6aef782be8ee84a2f`, katalog `rom/playable-slice-v02-inner-render-conflict-repair/`. GitHub compare `9acaeaf7→4be191`: en ny commit, 150 tillagda filer, äldre frysta filer orörda. MAIN laddade båda nya **16 384-byte** ROM-filerna från GitHub och räknade om SHA-256 från de faktiska binärbytena med standard-SHA256-självtest:
- TOP `let-me-out-v02-brown-door-top.bin`: `65742ea62a9f96fe42ff7263695f271499f9e200d6547a23cf354a4bb89c4f6b`.
- BOTTOM `let-me-out-v02-brown-door-bottom.bin`: `2c4483888cc3a77e2e8fc8dd5f3fa3a61a123c75a24c6a16fca86ca42b120232`.

Utvecklarobserverad begränsad faktisk förbättring: tidigare inre bruna saknade pixlar **20/20/16 → 16/20/16** för locked/open/key-floor i **BÅDA** ROM. En avgränsad tidigare RESP1-fas för P1 X60–62 återställer fyra bruna pixlar X0–3 på Y86 i låst test och enligt rårapport 18/114 positionsfall, 72 bruna pixlar per ROM utan färg-/NPC-förluster; 114/114 riktade NPC X/Y-fixturer och 600/600 standardframe-PNG byteidentiska med 9aca-basens. Utvecklaren uppger 600×262, profilerad c76 max, RIOT stack SP=$F7, riktig joystick/key/exit 210 p/3 liv, key65/65, key+shot14/14, shot10/10, locked brun dörr och top/bottom open256/256. **MAIN har inte själv kört DASM/Gopher/Stella, och ett BOTTOM-rasterbreakpoint prov uppnådde 174 händelser mot tröskel 175; denna del är INTE total breakpoint PASS.**

**FORTSATT FAIL**: key/P0 same-Y på separerade X `0/14`, fem NPC same-Y X20/44/68/92/116 Y86 `2/5`, M(1) fem standardrutor partiella, M(1) skott/key-fixtur `23/28`, PF `16/20/16`. Nya kasserade avgränsade tekniker: BOLL+M0 `0/14` med 20 extra guld, 3 saknade gula och **267 scanlines**; M1 som F-del `32/38`, 10 extra vita, 0 för tre övriga. Dessa är viktiga negativa prov, inte allmänna omöjlighetsbevis. De fem M(1)-avvikelserna sammanfaller enligt utvecklaren med gula spelarpositioner; klassificera **verklig fysisk objektocklusion kontra otillåten förlust** innan detta omdefinieras som design-PASS eller döljs med annan prioritet.

## 4. MAIN:s prioriterade rekommendation inom redan godkänt V02-scope

**NYASTE tekniska start är `4be191123f0e54b583fd72f6aef782be8ee84a2f`, inte gamla forskningsrapportens `9acaeaf7`.** Detta är MAIN:s koordinering av befintligt V02-uppdrag LM-D29/LM-D30 och lämnar alla originella fem-NPC, TOP-DOWN 8x9, AI, fri logisk X/Y, brun PF-dörr, key, shot, färg, poäng/liv och timing oförändrade.

1. **Högsta värde: P0/key same-band.** Mät exakt varför `PrepareKeyAssist` väljs bort för `PY=151`, `PX=24/60`; jämför kontroller `PY=159`, `PX=60` och separat vänster X. Utred tryggt utvidgat fönster eller helt annat P1-/färg-/latch-förhållande; ändra inte enbart jämförelsevärdet och kalla det PASS. Mål exakt `14/14` guld **och 0 extra** i båda key/P0-fallen med P0, fem NPC, wall och skott intakta. Bevara gamla negativa fixturer.
2. **PF och M(1).** Utgå från senaste låsta PF-resultat `16` missing, öppet `20`, key-floor `16`; mät den snäva X60–62-reservfasen och andra faktiskt skilda fas-/wall-kernels. Identifiera de fem M(1)-standardframes per pixel och separera fysisk P0/NPC-ocklusion från felaktig mask. Mål 0/0/0 wall missing och fler än 595/600 fulla masker där fysik och originalkrav medger, utan att ta bort spelarpixlar.
3. **Fem same-Y NPC.** En bredare fullkernelevaluering kan utgå från G5BE ITER6:s **begränsade** positiva X/Y-scheman men aldrig anta frihet. Prova en materiellt annan 6507/TIA-händelseplan med fysiskt register-/deadline- och X-topologiprover, utan BOLL+M0-invalid variant, M1-F partiell variant eller föregående dubbla RESP-reset som pseudo-PASS.
4. **Skyddat regression:** båda TOP/BOTTOM ROM, locked brun PF + black negative contour/hole, 256/256 open svart, shot10/10 utan (12,106), coldkey65/65, keyshot14/14, minst 595/600 standard femmasker, 0 helt osynliga, riktig joystick/key/exit 210p/3 liv, 16KiB F6/NTSC, 600×262, max c76, RIOT128 incl stack. Separata riktade negative/crowd/oracle och reproducerbar DASM/Gopher/Stella och postpush ROM SHA256.

**Research är rådgivande och får inte skriva spelkod.** För ROM DEVELOPMENT IV behövs fortsatt separat **användaröverförd konkret prompt**; en Issue-kommentar eller GitHub-fil startar inte separat Codex. MAIN ska ge den med exakt ny startpunkt. Ingen V03/G6/F12, fyrarumscutover, PAL/mapperbyte, mask-/NPC-/AI-/score-/flicker-waiver, PR merge, release eller självständig Verification ges av dessa anteckningar. `G5_FORMAL_OPEN`, `INDEPENDENT_VERIFICATION=NOT_RUN`.

## 5. Dokumentation och historik

- Tidigare allmänna enrumsspelbasen `8177c` kvarstår fryst och skild från senare **V02 TOP/BOTTOM-testfamiljer** `4c4fc5b7`, `1da716dc`, `9acaeaf7`, `4be191`. Denna mottagning gör inte senare dörrtestfamilj till godkänd fyrarumsproduktion.
- 57 originalbeslut + senare individuellt slumpade fem originalmaskformer och brun PF-dörr i övre/nedre vägg gäller via egen auktoritetsordning. Forskningens 8-bitars-fröanmärkning gäller **enbart deterministisk generator med endast ett initialt 8-bitars tillstånd**, inte system som samlar ytterligare entropi.
- V9 Project Sources och Instructions är daterad navigation. Följ levande `docs/CURRENT_AUTHORITY_STATUS_AND_WORK_QUEUE.md`, Issue #31 och G5 original innan ny faktisk order.
- Källa: [RESEARCH II:s äldre migration](RESEARCH_I_TO_II_HANDOFF_2026-11-17.md), [30-tricksoriginal](../RESEARCH_30_ORIGINAL_ATARI_TRICKS_2026-11-16.md), [G5BE Iter6](https://github.com/Odourman/let-me-out/issues/30#issuecomment-7001424130), [V02 skott 9aca MAIN receipt](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7040774646), [V02 nyare 4be specialistleverans](https://github.com/Odourman/let-me-out/issues/31#issuecomment-7042654133).
