# LET ME OUT! – MAIN XI: användarbeslut om igenkännbart men ej pixel-exakt svart nyckelhål

Datum: 2026-11-20. Status: `EXPLICIT_USER_VISUAL_TOLERANCE_DECISION`.

Användaren beslutade:

> "Det behöver inte se exakt ut som ett nyckelhål, men bör likna ett."

Detta ändrar **endast** det tidigare framtida kravet på R3:s exakta 1–2 colorclock nyckelhålsmask. En framtida dörr får ha en grövre, tekniskt möjlig **nyckelhålsliknande** svart utskärning. Originalets exakta R3-nyckelhål förblir historiskt bevarat original och lämplig kvalitetsreferens, **inte** längre automatisk pixel-för-pixel acceptansspärr för själva hålets kontur. Någon slutlig ny hålform, minsta öppning, bitmap, svart pixelandel eller X/Y-dimension har ännu inte beslutats.

**Fortsatt bindande:**
- Svart nyckelhål betyder avsaknad av orange dörrpixlar över svart bakgrund. **Inte** bara en separat svart överläggssprite eller färgat svart objekt (om detta ska ändras krävs eget uttryckligt användarbeslut).
- En enda orange låst dörr i framtida **övre eller nedre yttervägg beroende på karta**, brun PF-vägg omkring, svart bakgrund; dörrens upplåsning och spelaren måste fysiskt passera.
- Inga orange spillpixlar på brun yttervägg, inga bruna väggskador, inga oavsiktliga öppningar eller nya gula/skott-/NPC-grafikfel accepteras som följd av toleransen.
- Fem individuella fiender, fyra exakta originalmasker med framtida oberoende slumpat val, riktig key+player och same-Y synlighet samt övriga ursprungsregler står kvar.
- Denna visuell formtolerans är **inte** i sig en ROM-/G5-/Verification-PASS, gameplaysteg, waiver för NPC-osynlighet, release eller automatiskt kartcutover.

**Researchimplikation:** det är nu rimligt att prova en mittställd PF-baserad "huvud 16px / skaft 8px"-silhuett eller en förstorad P1-baserad **orange dörrsprite med transparent 8px huvud och 4px skaft**, så länge hela dörren/nyckelhålet uppfyller ovan och P1 inte offrar NPC-rendering i något nödvändigt dörrband. Dessa är rådgivande provhypoteser, INTE godkända slutgrafiker. Teknikjämförelsen finns i [forskningsnot](../research/MAIN_XI_KEYHOLE_OPTIONS_30_TRICKS_ONLINE_2026-11-20.md).

Frysta test-ROM `4c4fc5b7c5545217b2321a38d9db6db5dac7db2f` har idag **8px bred rak utskärning**, orange spill på yttervägg, bottom två gula öppningspixlar, skottregression 9/10, key/player 0/14, same-Y NPC 2/5. Denna nya formtolerans gör **inte** dessa filer automatiskt godkända. Håll `G5_FORMAL_OPEN`, `INDEPENDENT_VERIFICATION=NOT_RUN`.
