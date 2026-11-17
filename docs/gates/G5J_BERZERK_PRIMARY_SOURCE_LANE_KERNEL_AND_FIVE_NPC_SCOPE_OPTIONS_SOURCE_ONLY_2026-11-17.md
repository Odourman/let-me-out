# LET ME OUT! – MAIN VI G5J: ORIGINAL-BERZERK-GRANSKNING OCH EN NY 5-FIENDERS RASTERARKITEKTUR
**Datum:** 2026-11-17 · **Status:** `G5J_SOURCE_ONLY_HISTORICAL_BERZERK_PRIMARY_REVIEW_COMPLETE_LANE_FEASIBILITY_CONDITIONAL_G5_USER_WAIVER_PENDING_G6_NOT_AUTHORIZED`.
**Mandat:** användarens "Varför avbröt du? Fortsätt" efter G5I. G5 får undersökas färdigt som forsknings-/planeringsarbete; inget tillstånd att retroaktivt ändra 57 ursprungliga beslut, ändra R1/R2-v0.18-canon, godkänna icke-beslutad flicker, utfärda G6 eller skriva/köra ROM.

## 1. Ny starkare faktisk primärkälla, inte en lös liknelse
En **faktisk kommenterad Atari 2600/6502-disassembly av originalspelet Berzerk**, ursprungligen av Dennis Debro (revision angiven 2004), lästes **direkt som 104 967 tecken/3 288 källrader** genom användaransluten GitHub-koppling. Källan är publicerad på:
- [Berzerk, kommenterad Atari 2600-assembler, PINNAD revision `480a5287c6aec61bad333a44de105e45cfed39ff`](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm), blob `e00c50a718d96ffcbfa4e6270c87a037d2758cf3`. **Extern forskningskälla, inte vårt projekts canon och inget resultat av ny DASM/Stella/ROM.**
- [Andra oberoende Stella-disassembly av samma speltitel](https://github.com/marcelovani/Atari/blob/63467398ec631816328468ed85d56734f7e1159e/3.%20Modified/among_berzerk.asm), men den första är den betydligt mer läsbara kommenterade ursprungskällan.
- Den tidigare Berzerk-jämförelsen var korrekt att **många robotar på en originalkonsol** inte innebär bevis för sex eller fem vitt oberoende humanoidmasker på samma rasterhöjd. Nu finns ett **positivt källbevis för varför**.

### 1.1 Specifika rader kontrollerade i den externa källan
| Extern källrad/sektion | Faktisk ursprungsuppgift | Slutsats för oss |
|---|---|---|
| L199 `H_ROBOT=9`, L214 `MAX_ROBOTS=8` | Upptill åtta logiska robotar om nio logiska bitmaprader | Robotkapacitet ≠ åtta sprites samtidigt på EN rasterrad |
| L1826–1839 samt L2093–2109 | Initial Y=`75` och `sbc #H_ROBOT+1` per robot → Y = **75,65,55,45,35,25,15,5** | **Tio logiska rader vertikalt mellan robotarnas start-Y** från början |
| L1323–1367 | Upp-/nedflyttning jämför `robotVertPos[x]` med grannrobotens Y och `H_ROBOT+1/+2`, väljer annat beteende om för nära | Robotarnas Y-rörelse är **inte helt fri**; den tar hänsyn till vertikalt avstånd |
| L401–461 och L464–524 | `P0` spelare, `P1` en aktiv robotgrafik; `kernelSection` och `robotPointers` växlar sektioner; `RESP1` under särskilda faser | **Vertikal zonuppdelning + registeråteranvändning**, inte N fria P1-objekt samtidigt |
| L1279–1285, L2009–2018 och L1310–1366 | Y omräknas med `lsr` för tvålinjers rastermodell, övrig kernel varannan fysisk rad; källan själv anger 2LK | Berzerks 9-raders mask ger i denna rendering ungefär **18 fysiska scanlines**; att kopiera metoden ordagrant skulle **ändra vår 8×9 fysiska rasterstil** |
| L1578–1616 | Grafikpekare och fin/grov robot-X förbereds **innan** visningen; `kernelSection` nollställs | VBLANK-precompute + en aktiv robotkanal per horisontell bildrad gör dynamisk X hanterbar |

**Färsk viktig korrektur mot allmän jämförelse:** Berzerks ursprungliga åtta robotar är tilldelade vertikala positioner som hindrar deras 9-logiska-raders silhuetter från att behöva dela P1 samma-Y från start. Vid rörelse spärrar spelet vissa vertikala möten. Därmed kan det **inte** användas som evidens för att våra fem helt självständiga Y med fem simultana 8×9-figurer, gul spelare, aktiv M0 och P1-orange dörr redan är lösta.

**Viktig gräns för källbeviset:** Koden har granskats i text, inte byteidentiskt omkompilerats eller körts här. Robotarnas **fysiska rasterband** och exakt respons vid alla kollisionstillstånd skulle behöva verifieras separat om man vill portera dess mekanism, men ordnings- och rörelsespärren finns uttryckligen i source.

## 2. Vad förberedelserna från G1–G5 betyder med denna nya kunskap
Förra G5G/G5H räknade **värsta obundna originalfallet fem NPC med Y-overlap sex av nio scanlines** och en orange P1-dörr, där våra A/B-direkta instruktionssekvenser nådde **79/76** (eller 89/76 med vissa extra fall). Det var korrekt för det villkoret men nu finns en **helt annan rationell arkitekturfamilj**:

**G5J-LANE-HYPOTES (FÖRSLAG, EJ SPELREGEL):** Bevara fem logiska fiender, full numerisk **X** för var och en, deras fyra oförändrade 8×9 TOP-DOWN-bitmapidentiteter, gul player, skott, brown PF, black BK och P1-orange+svart keyhole. Använd i stället *Berzerk-liknande Y-arbitrering* (hindrar två robotars 9-fysiska-linjers ritband att sammanfalla) så att **P1 högst visar EN vit robot per rasterrad**. Dörren på högerkanten kan då kräva **ytterligare EN P1-orange event**, inte fem. `CTRLPF REF + Ball x0` från G5G används bara som rumsvägg-hypotes, med tidigare oförändrad R3 P1-door som referens. **DÖRREN ÄR INTE AUTOMATISKT LÖST**, eftersom roboten fortfarande kan röra sig på samma Y som dörren och P1 måste växla vit/orange inom 76c och faktiska GRP/RESP-START.

En sådan regel **begränsar fiendernas Y-rörelse och möjliga omlöp**, särskilt i korridorer. Det är alltså ett framtida **användarägt spelbeslut** och **INGEN automatisk G5-waiver**. Dessutom kan en framtida guldnyckel på en dödad robots Y behöva en ytterligare grafisk policy (O1-skymning och eventuellt door+key på samma Y). Ingen av dessa krav förenklas tyst.

## 3. Offlineaudit 176 rasterrader / fem robot-Y / dörr Y
**Maskinläsbar bevisdata:** [G5J – 176 scanlines, 5 logiska Y-band, P1/dörröverlapp i CSV](G5J_LANE_RENDERING_176_SCANLINE_OCCUPANCY_OFFLINE_2026-11-17.csv).

Kontrollfallet har **ENDAST TESTDATA**, inte en fast spawnform eller användarauktorisation:
- Kartbild 22×8 = **176 fysiska rumsscanlines**, fem 9-scanlineshöga NPC vid **[20,44,68,92,116]** i rumsrelativ Y (alla X godtyckliga, inte ens begränsade i denna offline-testmodells bitband).
- R3/C02:s dörr ligger i 4×8 = **32 rumsscanlines**, rumsrelativt **Y80..111** (det finns även 8 blank övre rasterlinjer i diagnostikens verkliga visible screen; detta är tydligt **rumsrelativa Y**).
- **0 av 176** rader har två överlappande vita fiendband, max **1** vit NPC per rad. Dörren och en fiende sammanfaller i **9 scanlines, Y92..100**. Det är det viktiga återstående P1 vit/orange-testet; det får inte trollas bort av Berzerk-lane-metoden.
- Det här provet antar **en fysisk scanline per original-bitmaprad** för att försöka bevara våra oförändrade 8×9; Berzerks historiska **2LK** är **INTE automatiskt portad**. Detta är offline occupancy-only, ingen TIA timing.

### 3.1 Explicit *ny* direktinstruktionskostnad när det bara finns en samtidig robot
Anta idealiserat `LDA #bitmap (2c); STA GRP (3c); STA RESP (3c)` = 8c per synlig 8bits aktör. P0 gul player, P1 vit robot, P1 orange door, P1 white/orange/next-row return = 2×`LDA#;STA COLUP1`=10c, WSYNC=3c. Preförpositionerat BL, M0, PF/BL-återställning där så anges. **Detta är fortfarande en aritmetisk INSTRUKTIONSMODELL, inte G0 fysisk START:** verkligt RAM-X, mask-/tabladdning, sprite-nollrader, X-korsning, TIA deadlines, M0/shot, Ball placering och collision/AI utelämnas.

| Tillstånd | Modellberäkning | Motsvarande summa | Betydelse |
|---|---|---:|---|
| P0 gul + EN P1 white NPC, ingen dörr | 2×8 + WSYNC3 | **19/76** | Rimligare budgetklass, men fysisk timing ännu okänd |
| P0 gul + EN P1 white NPC + P1 orange door | 3×8 + 2×5 färg + WSYNC3 | **37/76** | Lämnar 39 modellcykler för icke redovisat arbete |
| Som ovan på Ball-dörrgränsraden | +2×5 (`PF0`, `ENABL`) | **47/76** | Lämnar 29 modellcykler; fysiska deadlines obekräftade |
| Som ovan även med ändrade tre PF-register på svår kart-rad | +3×5 PF0/1/2 | **62/76** | Lämnar 14 modellcykler; full dynamik/START kan fortfarande spräcka |

**G5J:s nya bevisvärde:** Ett faktiskt ursprungsspel använder vertikalt åtskilda robotskikt och P1:s sekventiella rendering. I vår **separationshypotes** skiftar den direkta samma-Y-dörrkostnaden från **G5H:s 79c med alla fem** till **37c med högst EN vit fiende**, men **bara** genom att anta en **annan spel-/positionsregel**. Vi får inte marknadsföra detta som optimering av samma obundna femfiendersproblem.

## 4. Två andra verkliga kernels som måste jämföras rätt
**A. Steven Hugg, 2025 – [Three-Stream Versatile Kernel](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html).** Använder två sprite- och en PF-displaylisteström och HMOVE-sekvenser; **tre registerskrivningar per scanline** (en per stream), färg- eller bitmapändring men inte bägge från samma stream på samma rad; cirka **32B RAM per displaylista** i författarens version och multiraders ompositioneringar. BRA rådgivande för **Y-separerade objekt och väggar**, men **kan INTE av enbart tre streams framställa fem fristående same-Y 8bit-identiteter och en orange dörr i samma rad**. Får inte ersätta G5H:s worst-case med displaylista som slogan.
**B. Batari Basic multisprite-kernel, [teknisk originaldokumentation](https://www.randomterrain.com/atari-2600-memories-batari-basic-commands.html).** Ger flera **logiska** sprites, men dokumenterar uttryckligen **flicker/framemässig slotdelning när sprites delar vertikala områden**. Detta är EN möjlig PRODUKTkompromiss om användaren senare ser och godkänner frekvens/visuell effekt och logisk collisionspolicy – **inte** bevis på att alla fem 8×9-masker syns varje frame vid samma Y.
**C. NUSIZ-hårdvarukopior:** Fasta offset + samma bitmap, bara för kompatibel identitet/X; inte allmän fri-X-lösning. Delen var redan negativt verifierad inom våra G5H-kostnadsscheman.

## 5. Rangordnade G5-vägar efter ny primär källgranskning
| Tekniskt spår | Bevarar fem logiska fiender? | Bevarar alla fri Y och alltid simultan 8×9? | Positivt bevis och återstående risk | MAIN-rekommendation |
|---|---|---|---|---|
| **S0 exakt nuvarande simultanitetskrav** | Ja | **Ja som krav** | Inga fungerande fulla 5-NPC ROM; G5H A/B direktkernel FAIL i vissa worst cases; ny arkitektur krävs | Behåll kravet tills explicit användarbeslut; **ingen G6 kodorder med nuvarande plan** |
| **S1 Berzerk-liknande Y-arbitrering** | Ja | **NEJ; Y-rörelse begränsas** | Externt originalspel styrker konceptet, vår G5J offline max 1 white/rad; 37–62c hypotetisk direktbudget, all fysik saknas | **Högst prioriterad villkorad designkandidat** OM användaren senare godkänner ändrad Y-policy |
| **S2 Batari fair slot-/flicker** | Ja | **NEJ; visuell samtidighet offras** | Etablerad logisk multisprite/flicker-arkitektur, men originalmask/nyckel/door/missile inte ours | Reserv med separat uttrycklig synlighetspolicy |
| **S3 Treströms displaylista** | Ja | Nej bevis | Intressant för 2 sprites/PF med billigare per-scanline update, men 3 writes/line, RAM/event build kostar, inte G5 worst-case | Stödteknik till S1, inte en fristående femsameY-lösning |
| **S4 F6+extra hårdvara** | Ja | Möjligen (ej visat) | Kräver annan mapper/timing; strider mot standard-F6-scope | Ej börja utan ändrat användarbeslut |

**Beslutsklass:** Det är nu sakligt ohederligt att säga att "Berzerk har 8 robotar så 5 same-Y borde fungera". Berzerk skapar **en annan simultanitetsregel**. Vi har äntligen ett väldokumenterat, potentiellt spelbart **alternativ på original Atari 2600**, men det kräver användarval om robotskiktens Y-arbitrering. Den varianten har fortfarande ingen ROM/G0-pass.

## 6. G5-exit och nästa *faktiskt* tillåtna arbete
**G5J research PASS (dokumentation):** Berzerk källan läst, åtta robotar och Y-begränsning källspårade med rader, femmaskers separationsprov 176/176 klargjort, P1-robot+door same-Y kvar som stress, tre kernels jämförda. Detta **avslutar den specifika G5J-source-only-delstudien**.

**G5 formell design/canon fortfarande PENDING:** MAIN har en prövad ***valmatris*** men ingen behörighet att ändra fri Y/synlighet, 8×9-fysisk höjd, key-O1, acceptanskriterier eller ge G6/F12-uppdrag. Skiftet 6→5 är uttryckt som användarens arbetsriktning men v0.18 scope är historiskt fortfarande 6 / 5+key. För att gå vidare till en verklig ROM-order måste korrekt **framtida** scope/acceptance beredas och separat uttryckligt godkännas. Frysta källor, PR7/E02, oberoende Verification II och 57 beslut oförändrade.

**Planen G1→G10 respekteras:** Vi *fortsätter G5:s källförberedelser* och ger konkret villkorad S1-policy, men **börjar INTE G6/G7/G8**. Nästa legitimt tekniska forskningsarbete kan avgränsas till en SOURCE-ONLY Berzerk-style en-P1-robot + P1-orange-door + Ball-left x0 + aktiv M0/P0 statisk registerfasmodell, med särskild noga märkt designhypotes och utan ROM. En verklig ROM-order måste ha explicit separat userauktorisation och G0 stoppvillkor.

## 7. Käll- och granskningsspår
1. Extern [Berzerk disassembly, pinned](https://github.com/TheAnsarya/multi-local/blob/480a5287c6aec61bad333a44de105e45cfed39ff/download-atari/asm-files/berzerk.asm), GitHub blob `e00c50a718d96ffcbfa4e6270c87a037d2758cf3` (ursprunglig extern research, read-only).
2. [G5I plan/mandat/rebaseline](G5I_PLAN_RECONCILIATION_FIVE_NPC_DECISION_READY_NOT_G6_2026-11-17.md), [G5H unrestricted budget](G5H_START_GRP_RESP_NUSIZ_SAME_Y_SOURCE_ONLY_DECISION_2026-11-17.md), [G5G left Ball & PF](G5G_BALL_LEFT_WALL_AND_FIVE_NPC_OPCODE_CENSUS_SOURCE_ONLY_2026-11-17.md), [176-line model CSV](G5J_LANE_RENDERING_176_SCANLINE_OCCUPANCY_OFFLINE_2026-11-17.csv).
3. [External three stream 2025](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html), [batari multisprite docs](https://www.randomterrain.com/atari-2600-memories-batari-basic-commands.html).
4. [G5 authorization boundary](G5_AUTHORIZATION_BOUNDARY_AND_USER_CHOICE_2026-11-17.md), [G4 unissued physical-micro draft](G4_FUTURE_SINGLE_MICROPROBE_ORDER_DRAFT_NOT_AUTHORIZED_2026-11-17.md).

**TOTALSTATUS:** G5J source-only fertig; G5 användardriven designcutover INTE klar; G6 och full R1/R2–R4 INTE auktoriserat/inte verifierat. Inga code/graphics/test-mask/ROM ändrade.
