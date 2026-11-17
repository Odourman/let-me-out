# LET ME OUT! – MAIN VII G5S: användargodkännande C1 + D1 + E1 för framtida femfiendersversion
**Datum:** 2026-11-17. **Status:** `G5S_C1_D1_E1_APPROVED_FUTURE_DESIGN_AND_TEST_TARGETS_ONLY`.
**Beslutsauktoritet:** direkt användarsvar i MAIN VII på exakt namngiven ja/nej-fråga. **Inte:** ROM, G0, G6/F12, faktisk R1/R2-ROM-testacceptans, kartcutover, full G5-PASS, PR-merge eller oberoende Verification.

## 1. Exakt användarreferens och ändrat auktoritetsläge
MAIN VII hade efter G5R:s käll-/poänggranskning frågat:

> "Godkänner du uttryckligen C1, D1 och E1 som framtida spel- och testregler?"

Den användarsvarade nästa repliken löd:

> "Fortsätt Följ dina egna rekommendationer"

Denna direkt påföljande svarstext avser alltså **de tre explicit namngivna rekommendationerna** C1/D1/E1 i [G5R-beslutsunderlaget](G5R_MAIN_VII_FIVE_NPC_REBASELINE_SCORE_SPAWN_DECISION_READINESS_2026-11-17.md). Det är ett **avgränsat jakande beslut via specifik referens**, inte ett godkännande av varje tidigare föreslagen teknik, kartkandidat, senare implementation eller annan projektgrind. Till skillnad från *föregående* lika lydande svar som föregick G5R:s beslutsfråga ändrar denna replik auktoriteten **för just C1+D1+E1**. Äldre rapporttexter om att dessa ännu inte var godkända är bevarade som sina historiska tidssnapshots och supersederas bara inom angivet område.

**Proveniens:** användaren hade redan separat godkänt G5Q A1/B1 ([LM-D12/13](G5Q_MAIN_VII_A1_B1_USER_APPROVAL_DECISION_RECORD_2026-11-17.md)); ursprunglig sexfiendersspec och 57 beslut förblir historiskt autentiska. Originalet och nollgolvet granskades direkt i G5R, med 210 eventbaserade offlinepoängfall ([CSV](G5R_FIVE_NPC_SCORE_FLOOR_210_CASES_SOURCE_ONLY_2026-11-17.csv)). G5P är reproducerad rådgivande forskning, inte hardware PASS.

## 2. LM-D14 – C1: framtida versionssatt R1/R2-femfiendersmål – GODKÄNT
**Framtida R1-mål:** fem vita individuella NPC-instanser **M, M, F, SM, SF** med alla fyra ursprungliga **TOP-DOWN 8×9** figurmasktyper intakta, originalorientering, individuellt fritt logiskt X/Y samt A1/B1:s jakt-/synlighetsmål.

**Framtida R2-mål:** efter att en vald nyckelbärare dödats och dess dödsanimation är avslutad, **fyra kvarvarande NPC + en fysiskt synlig guldnyckel** på bärarens faktiska logiska fallplats. Befintliga K1/O1/E1 och key-/door-regler bevaras.

**Acceptansgräns:** C1 fastslår framtida **design- och testomfattning** men **inte** att en R1/R2-ROM finns, att testkriterier är tekniskt passade eller att v0.18 byter namn/versionshash. Historiska v0.18 R1 **sex** och R2 **fem+key**, inklusive PASS/FAIL, objektblobbar och branchhashar, förblir frysta referenser. Exakt framtida versions-ID, mask-/ROM-/testartefakter och faktisk acceptans kräver separat godkänd implementation och oberoende Verification.

## 3. LM-D15 – D1: kill-straff −30 med fem, originalpoängen i övrigt orörda – GODKÄNT
**Endast för framtida femfiendersspelbas:** poängstraffet vid verkligt dödad NPC ändras från originalets **−25 till −30 per individ**. För historisk sexfiendersbas gäller fortsatt −25; det är inte en retroaktiv rättelse av originalbeslut 043.

Oförändrat:
- Score startar 0, `score=max(0,score−30)` **på varje kill** i den framtida fem-NPC-regeln; ingen dold minus-skuld.
- **+50** först vid faktisk nyckelupptagning, inte vid key-drop eller kill; K1 om spawn under spelaren.
- **+100** vid faktisk rumsutgång och **+15 per NPC som fortfarande lever då**.
- Missat skott 0, extralivströsklar 500, 1500, 2500 ... en gång per nivå; originalets samtidighets-/prioritetsregler och E1 förblir.
- Målet i ursprungligt beslut 047 att all-kill inte ska vara repeterbart lönsam highscore-farming bevaras.

För fem och `k` kill, om ingen nollklampning inträffar: `Δ=225−45k`; all-kill `k=5` ger **0 netto/rum**. Med nollklampning, alla fem kills före key och verklig exit, `S_next=max(S,150)`: exempel start 0 och fem all-kill rum ger **150→150→150→150→150**. Detta är arithmetic source-only, **ingen ny ROM-verifiering**. Händelseordning och tidiga livsförluster behöver testas i framtida programmering.

## 4. LM-D16 – E1: fem olika giltiga starter och en likformigt slumpad key-bärare – GODKÄNT
**Framtida femfiendersspel:** varje rum startar med **exakt fem olika NPC-startpositioner** valda ur en för det rummet **förhandsvaliderad** pool på den **separat beslutade exakta kartan**. Positionerna måste respektera NPC/NPC-/player-kollision, rimlig rumsnavigation samt logisk nyckel-/dörråtkomst. **Detta godkänner inte nu någon enskild koordinat, pool, slumprutin eller v0.19-rumskarta.** G5N:s Y-separerade startuppsättningar är forskningsdata, inte obligatorisk Y-policy, eftersom LM-D12 kräver fri logisk rörelse.

Vid varje rum får **exakt en** av de fem **NPC-instanserna**, inte en av fyra spriteformer, bära nyckeln, med **uniform sannolikhet 1/5 per individ** (även var och en av de två stora männen 1/5). En naiv 3-bitars `r%5` är ickeuniform och duger inte som bevis på E1. Om implementatören använder rejection sampling eller annan metod måste verklig fördelning och sekvens granskas separat. Inget konkret PRNG-frö, seed-policy eller generatorkod har godkänts.

Nyckeln faller på den dödade bärarens **faktiska fallplats efter dödsanimation**, andra androider får passera över den utan att flytta den, dess logiska plats oförändrad genom O1, och spelaren måste kunna plocka upp den. K1/E1 och dörr-/exitkriterier kvarstår. Validera samtliga fem möjliga bärare i framtida testscope.

## 5. Vad detta INTE godkänner
1. **Ingen kartcutover:** v0.19 exakta `A_OPEN_01/B_OPEN_01/C_OPEN_01/D_OPEN_01` fortsatt kandidater; LM-D04 godkänner enbart *luftig designriktning*. Historiska v0.11 `A01/B01/C02/D01` förblir källvalda referenser tills särskilt exakt kartbeslut.
2. **Ingen ny synlighets-/flimmerwaiver:** LM-D12/13 gäller; kort tillfälligt O1-skymd key vid **faktisk** NPC/key-pixelöverlappning är redan godkänd men inte generellt gömd key vid same-Y. S05:s player+white+key+orange door+M0+PF förblir obevisad i NTSC-standard-F6.
3. **Ingen fysisk G0/G6/F12 eller assembler- /ROM-order:** ny versionssatt R1/R2-bas och −30-regel är **framtida krav**, inte anvisning att ändra .asm, .bin, tidigare ROM-tester, godkända brancher eller historisk Verification.
4. **Ingen merge av PR #7 eller separat researchbranch**, inga oberoende verifieringsanspråk.
5. **G5 formellt fortsatt öppet** för exakt kartbeslut och teknisk raster-/S05-grind; andra senare arbetssteg kräver särskild uttrycklig auktorisation.

## 6. Bindande status
`LM-D12/A1=APPROVED`, `LM-D13/B1=APPROVED`, `LM-D14/C1=APPROVED_FUTURE_SCOPE`, `LM-D15/D1=APPROVED_FUTURE_FIVE_NPC_SCORE`, `LM-D16/E1=APPROVED_FUTURE_SPAWN_AND_KEY_POLICY`; `MAP_V019_EXACT=NOT_APPROVED`; `G5_FORMAL=OPEN`; `G6/F12=NOT_AUTHORIZED`; `ROM=NOT_ORDERED`; `VERIFICATION=NOT_ORDERED`.
