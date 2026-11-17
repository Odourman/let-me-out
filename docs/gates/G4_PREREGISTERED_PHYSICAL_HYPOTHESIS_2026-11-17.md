# LET ME OUT! – MAIN VI G4: förregistrerad MINIMAL P0/P1/M0/PF-fysikhypotes (SOURCE ONLY)
**Datum:** 2026-11-17. **Status:** `G4_PREREGISTERED_SOURCE_HYPOTHESIS_ONLY`. Detta dokument innehåller **ingen ROM, ASM-kod, Stella-körning eller färdig cykelexakt implementation**. Framtida ROM-test kräver separat uttrycklig auktorisation och full G0-källpreflight.

## 1. En enda fysisk hypotes, inte sex-NPC-förhandsbevis
**H4-ONE:** På NTSC standard-F6, med originala TOP-DOWN-8×9-masker, kan **en och samma** datastyrda, som worst-case analyserad 9-raderskernel efter VBLANK-förberedelse rita (a) en fullskalig gul P0-spelare och (b) **en vit P0-originalandroid** som passerar spelaren både från vänster och höger, samtidigt med (c) **två vita P1-originalandroider**, (d) **ett synligt enda M0-skott i SAMMA 9-radersband men initialt på icke överlappande X**, och (e) två äkta bruna PF-väggkanter, **utan** att någon av de fyra bitmapobjekten blir vertikalt felvänd, utan oönskade M0-kopior, inom 76 CPU-cykler per rad och i en 128B RIOT/standard-F6-ROM.

**Mikroförsökets enda avgörande outforskade primitiv:** *Kan P0:s två individuella bitmap-/färg-/RESP0-fönster vara numeriskt RAM-X-styrda och vändas i horisontell ordning (vit→gul och gul→vit) medan en enda M0 faktiskt är aktiv på exakt samma scanlines som P1 och brun PF?* Detta är ett och samma sammanhållna rastermekanismprov med tydliga kontrollscener. Det behövs INTE redan ett källbevis för sex godtyckligt rörliga vita NPC.

## 2. Varför hypotesen alls är PLAUSIBEL men INTE bevisad
- **R1f (fryst källbranch `552a085d0c1ce0ec47d4f3342173658a25fd0e87`):** `NUSIZ0=$02` och **två `STA RESP0` per originalrad**, plus `STX GRP0` och `STA COLUP0` före den vita figuren, ger lokalt historiskt rättvänd **gul spelare till vänster → vit android till höger**; två separata statiska ROM. Ingen omvänd sortordning, fri numerisk 8bitars X, same-Y M0 eller PF i originalprovet.
- **R1g (fryst `d1d16758c549ecd657aba3b0aa4d6d7559e19264`):** EN standard-F6-ROM kunde växla fjärde P0-NPC mellan **fyra förkompilerade positionskernlar** (600/600 korrekt originalbild), P1 tre andra originalmasker och gul spelare stilla. `FRAMELO & $30` valde kernel **FÖRE** rasterbandet. M0 ritades **en rasterrad ovanför** 9-radersbandet: alltså INGET positivt same-Y M0-bevis.
- **F9 (fryst `c36982aef770af6cd3f68c2da37b8ed14aee2393`):** tre original-P1-masker med tre binära enbits-RAM-väljare; 144/144 riktiga rasterbilder, `RESP1/GRP1` vid dokumenterade historiska c21..53. Detta är EN ANNAN kernel än R1g, inte en godkänd addition eller tre fritt numeriska P1-X.
- **R3/C02 (fryst `000b6f2a579e4aa96995229b2174884fb7c565e2`):** PF vänster `c7/15/22`, höger `c37/45/52`, P1 orange dörr `c62`; ca **74/76** källberäknad separat worst row. Detta bevisar att asymmetrisk PF är möjlig under villkor i egen ROM, inte att rätt dörr och fyra bitmapobjekt kan samsas.
- **Stella 6.7.1 source `Player.cxx`:** `Player::resp` sätter intern räknare och har en särskild branch om `myIsRendering && ...<4`; `Player::nusiz` kan ändra pågående render-/divider-beteende; `GRP` byter faktisk bitmap. `DrawCounterDecodes.cxx` innehåller source-setup för NUSIZ `$02` kopiedekod (counter 28 + offset, spacing ≈32 CC). Därför kan varken ett skrivet `RESP0` eller en nollrad i maskerna översättas till önskad fysisk START med en enkel `x=3c`-formel.
- [Atari Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) visar två playerströmmar, 160 synliga CC, 76 CPU-cykler och att `NUSIZ0` också påverkar missilkopior. [Andrew Towers TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) beskriver de särskilda kopierings-/resetfaserna.

**Därför går det att formulera ett seriöst, falsifierbart enkelt fysikprov. Men hypotesen har ännu ingen integrerad, cykelexakt källa.** Det är G4:s tillåtna begränsning.

## 3. DATADRIVNA, förregistrerade scenlägen (en test-ROM senare – aldrig fyra profil-ROM)
Betrakta följande värden som **mål för synliga TIA-colorclock-START**, inte faktiska redan uppmätta `RESP`-cykler. Firmware måste vid framtida prov läsa **separata numeriska RAM-byte** `PLAYER_X`, `NPC0_X`, `P1_A_X`, `P1_B_X`, `SHOT_X` och bestämma den faktiska ordningen och `RESP`-faserna. En ROM som väljer ett helt hårdkodat program per rad från `FRAMELO` eller fyra positionsprofiler får aldrig `NUMERIC_X_PASS`.

| Prov | P0 spelare | P0 vit M | P1 vit F | P1 vit SM | M0 skott | Tolkning |
|---|---:|---:|---:|---:|---:|---|
| **A1** | 40 | 104 | 68 | 132 | 24 | Gul→vit, två P1, skott samma Y på icke-kolliderande X |
| **A2** | 48 | 96 | 72 | 128 | 24 | Variabelt numeriskt P0-avstånd; inte samma inkapslade specialläge |
| **B1** | 104 | 40 | 68 | 132 | 24 | **Vit→gul**, exakt omvänd horisontell P0-ordning |
| **B2** | 96 | 48 | 72 | 128 | **Vit→gul** med annat numeriskt avstånd |
| **X1** | 104 | 40 | 68 | 132 | **43** | Negativ färgvittnesscen: M originalrad3 = `FF` på CC40..47 och M0 projektil på CC43, med omedelbart önskad skott-testfärg gul |
| **X2** | 44 | 40 | 68 | 132 | 24 | Täta/överlappande P0-originalpixlar och sortbytesrisk; behöver separat policy om individuell synlighet |
| **M1** | 40 | 104 | 68 | 132 | 24 | Missilkopiekontroll: exakt **ett** aktivt M0-skott trots `NUSIZ0=$02` |
| **P1** | 40 | 104 | 68 | 132 | 24 | Två P1-originals TOP-DOWN 9 rader, PF vänster/höger båda äkta bruna; inte P1-only GUI-overlay |

**NPC-type:** P0 en *large_male* M och P1 en *large_female* F och *small_male* SM från låst `design/NPC_REFERENCE_8x9_masks.json` (Git blob SHA1 `058800a4c1904d1ff289e7e61b3902aa111ba16d`). P0 gul spelare används som *diagnostiskt* fullt 8×9 visuellt riktmärke tills Graphics exakta slutbitmap beslutats. Ingen fullspelsbitmap skapas i G4. Alla tre vita maskerna måste vara källbyte-exakta TOP-DOWN över 9 rader; SM:s nollrader får inte kortas bort eller vändas.

**Y:** alla fyra 8bitars aktörer får ett överlappande band `Y0..Y0+8`, t.ex. Y=96..104, och M0 är aktiv på en synligt icke-tom rad inuti **samma** band, t.ex. y99 när M rad3 är `11111111`. PF är en riktig brun source-spårbar väggkant i samma band; den får vara *konstant genom just den valda nioraderszonen*, så att PF-register kan laddas innan bandet endast om faktisk kart-/maskdata tillåter det. Detta testar verkliga PF-pixlar, inte ett borttaget PF. P1:s två aktörer måste visas i **samma** 9-raderszon och växla korrekt masks.

**Tydligt testbart icke-krav för mikron:** Den här tekniska grundfysiken påstår inte sex oberoende numeriska X/Y ännu, inte guldnyckel eller orange dörr i samma rad, inte full shot-hit-gameplay eller full fyra-rum, och inte E02. Den negativa X1-färgscenen kan inte godkännas som "två separat gula/vita pixelutgångar" på exakt samma pixel; det är en *bevisad enkel färg-/slutpixelgräns*, inte en automatisk waiver för framtida kollision/shot synlighet.

## 4. Source-only föreslagen instruktionsordning / DATAflöde – inte en hävdad cykelplan
1. **VBLANK/prefetch:** Läs oberoende numeriska X från RIOT, sortera P0 player och original M i *X-ordning* med identiteter och färg per actor; välj P1 F och SM separat; förbered nästa nio TOP-DOWN-rader, shot X, `NUSIZ0`/M0 one-shot-regel och PF-data. Inga `2^N` helprofil-ROM.
2. **Före första aktiva pixeln på raden:** Håll brunt PF-kantmönster korrekt, genom förreglerad PF-skrivning eller hållna identiska PF-register från föregående linje. `COLUPF` brun och `COLUBK` bakgrund. Säkerställ att `NUSIZ0` är kompatibelt med **endast en M0** på raden; historiens R1e flyttade M0 till raden ovanför för att undvika problemet. Därför är det **öppet hur** `NUSIZ0=$02` skall samverka med exakt en M0.
3. **Tidig P0-grafik:** Ladda den *vänstra* P0-aktörens rättvända radbyte i `GRP0`, dess gul/vit i `COLUP0`, trigga första `RESP0` vid numeriskt utledd fysisk fas. Sätt korrekta P1 `RESP1` och `GRP1` för F/SM, i egen ordning. **Inga P0/P1-traps får tidstämpelgaranteras utifrån F9/R1g i separat ROM.**
4. **Sen P0-grafik:** När den första P0-bitmapen faktiskt har lämnat sin 8CC-renderlucka, ladda den *högra* P0-aktörens radbyte/färg och trigga andra `RESP0` vid numeriskt utledd fas. Om P0 återställs under `myIsRendering` nära intern START får G0/G1 markera kontradiktion i stället för att acceptera halva/ghost-masker.
5. **M0 samma rad:** Projektilens bildpixel skall ligga på rätt `SHOT_X` inom y-banden och endast ha en kopia trots NUSIZ0 (pröva kontroll M1). Om M0 ligger **utanför** båda P0-grafikfönstren måste `COLUP0` vid M0:s faktiska pixel visa dess utvalda testfärg. Om den ligger inne i vitt P0-originalpixel-fönster är samtidiga olika färger **omöjliga med denna allokering** och utfallet blir en negativ kontroll, inte en fejkad PASS.
6. **Slut av raden:** Avsluta `GRP0/1` utan ghost och `WSYNC` senast radslut utan >76c; upprepa exakt nio gånger med samma aktörs-ID och TOP-DOWN bytes.

## 5. Falsifieringskriterier – minst ett måste på riktigt skilja PASS från FAIL
**G0 source preflight (obligatorisk efter separat order, före ROM-kompilering):** exakt DASM-/6507-opcode-lista med värsta `LDA/STA/branch/WSYNC` och konstruerade kandidat-fasintervall för A1/A2/B1/B2, M1 och P1. Visa var varje `RESP0/GRP0/COLUP0/ENAM0/NUSIZ0/PF` hamnar **före** verklig pixel-START/deadline; worst-case <=76 CPU per rad, faktisk 128B RIOT/stack, 4KB F6-bank, korrekt source mask. Om ingen plausibel ordnings- och single-M0-lösning existerar: **G0 FAIL → BYGG INGEN ROM.**
**G1 physical (endast om G0 PASS och separat användarauktorisation att testa):** exakt EN standard-F6/NTSC ROM, reella Stellatraces `c, PC, bank, scanline`, 262 linjer, fulla 9 rättvända bitmappsrader och 600 kontigua frames om relevant; åtminstone A1/A2/B1/B2 visar faktiskt korrekta positioner från numeriska RAM-värden, två P1-original och äkta bruna PF samt ETT M0 på **samma** rasterrad och rätt färg utanför överlapp.
**Kontroll som skall FAILa för direkt P0/M0-tvåfärg:** X1 är *omöjlig att återge som två samtidigt distinkta färger i en pixel under detta P0/M0-schema*; dokumentera det, men det måste inte blockera icke-overlap-mikro om projectile-hit-occlusion ännu är öppet som framtida designfråga.
**Tydligt FAIL:** vita originalmaskpixlar försvinner/vertikalvänds, M0 dupliceras/placeras föregående rad, P0-ordningsbyte misslyckas, eller firmware bara väljer mellan fyra specialkodprofiler med `FRAMELO`. Inga "PASS" genom att visa bara P0 och M0 i olika höjdband, ta bort PF eller reducera antalet original-P1.

## 6. Slutsats SOURCE ONLY (ej ny auktorisation)
H4-ONE är ett **rimligt avgränsat, falsifierbart experimentförslag** grundat i två frysta men separata positiva primitivfakta (R1f/R1g för P0-retrigger; F9 för P1-original). Dess styrka är att ***det kan misslyckas konkret***; det påstår inte att ny mekanism redan är genomförbar eller att alla X över 160CC kan stödjas.

**Rekommendation för G4:** `CONDITIONAL_GO_TO_ONE_SEPARATELY_AUTHORIZED_MICRO_PHYSICS_PROBE` **med hård source-G0 preflight**. Om det före en tänkt ROM inte går att ge en verkligt källbunden dual-P0 + single-M0 + PF deadlineordning, växla till `NO_GO_THIS_ALLOCATION` utan ROM-svep. **Ingen faktisk G6 får beställas eller byggas genom denna fil.**
