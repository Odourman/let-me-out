# LET ME OUT! – MAIN III R1x: M0 över nästa P1-instans, fem originalandroider och äkta CXM0P

**2026-11-16. Status: isolerat `LOCAL_PASS_R1X_SECOND_FEMALE_COARSE_AND_CXM0P_600`. Full R1 fortfarande blockerad.** Detta är research, inte auktoriserad produktionsimplementation eller fristående VERIFICATION.

## Reproducerbart resultat

- [**GitHub Actions #43847949395**](https://github.com/Odourman/let-me-out/actions/runs/43847949395): **SUCCESS**, 600 konsekutiva faktiska Stella 6.7.1-X11 bildrutor på commit **`f08661cf7a9a660f245c9475b63f30d8985b4b18`**.
- [**Fullständig råevidens artefakt #14216781051**](https://github.com/Odourman/let-me-out/actions/runs/43847949395/artifacts/14216781051): ZIP med **622 poster**, varav **600 råa Stella-PNG**, DASM-källa/listing/symboler, 16 KB F6 ROM, 600-raders CSV och `summary.json`.
- Nedladdad evidens-ZIP SHA256: **`61c760ac55ef225ae4bfdbea5d8cb2fe3650e384cf205f965b87a6a611301ad6`**; testad ZIP CRC: **PASS**.
- ROM: **16 384 byte standard F6/NTSC**, SHA256 **`15b65be5d2baf810576f58dc9fbe6d9a8b62b540d50b04ff2fa7a1dec6fab613`**.
- Referens: exakt R1w-ROM SHA256 `dac6340febe7a0a6e94e3e0231c97e8f79731a60a4eeba8903d95018d804141f`. Generatorn stoppar om referenshashen ändras.

### Vad som förändrats från R1w

**Endast VBLANK-positioneringen av M0.** Ett extra `BIT FRAMELO` (3 CPU-cykler, 9 TIA color clocks) läggs direkt före `STA RESM0`, så M0:s grundposition flyttas **18 GUI-pixlar** till höger. Varken de fem godkända originalmaskernas källbytes, deras härledda 14-radstabeller, eller de fyra specialiserade synliga figurrutinerna för A/B/C/D ändras.

Den tidigare bevisade R1w-omordningen av `STY ENAM0`, `RESP0`, `GRP0` och `COLUP0` återanvänds helt oförändrad. HMM0-tabellens åtta finlägen behålls.

| Skott-X (GUI) | Råa frames | TIA CXM0P D7 |
|---:|---:|---|
| 268 | 75 | Ingen kontakt |
| 270 | 75 | Ingen kontakt |
| 272 | 75 | Ingen kontakt |
| 274 | 75 | Ingen kontakt |
| 276 | 75 | Ingen kontakt |
| 278 | 75 | Ingen kontakt |
| 280 | 75 | **Kontakt med andra stora P1-kvinnans mask** |
| 282 | 75 | **Kontakt med andra stora P1-kvinnans mask** |

**150 frames med verklig M0/P1-kollision, 450 utan kontakt.** Det är inte en simulerad hitbox: den diagnostiska bakgrundsfärgen skapas direkt från `LDA CXM0P; AND #$80; STA COLUBK` efter figurbandet, med `CXCLR` efter avläsningen. Kontaktfärg **RGB [0,0,138]**, icke-kontakt **[0,0,0]**. R1x visar att hårdvarulatchen reagerar på en **annan fysiskt ritad P1-instans** än den första stora kvinnan i R1w.

### Samtliga tester, fail-closed

| Test | Resultat |
|---|---:|
| Faktiska 600 Stella frame-ID utan luckor | **600/600** |
| NTSC 262 scanlines | **600/600** |
| Fem fullständiga ursprungliga NPC-instansmasker i 14 visade rasterrader, utan dolda saknade pixlar förutom exakt avsiktlig M0-overlay | **600/600** |
| En tillfällig gul spelare med en enda gul M0 på armrad GUI-y167, på ett av åtta förväntade X | **600/600** |
| Fjärde P0-liten-kvinna på fyra fasta X: 330,348,360,378 | **600/600** |
| Åtta M0-X × fyra P0-X × två högerdörrstillstånd | **64/64 verkligt observerade kombinationer** |
| 32-raders PF0-högeröppning och BALL-vänstervägg | **600/600** |
| Uteblivna skott eller extra gul/vit missilpixel | **0 / 0** |
| Gammal projektil på GUI-y160 | **0** |
| Hårdvarukollisionsfärg vid förväntad kontakt | **PASS**, 150/150 kontakt, 450/450 ej kontakt |

## Begränsningar (viktiga för MAIN)

**Detta bevisar inte en fri projektil över skärmen.** M0:s åtta steg är fortfarande ett deterministiskt test baserat på `FRAMELO & 7`; det finns ingen eldknapp, självständig kulposition i RAM, faktisk kulhastighet, skottavslutning vid träff eller styrd Android-död. `CXM0P` skiljer **inte** mellan logiskt flera P1-androider: vi vet i detta test vem som stod på den kända X-positionen genom scene-upplägget, men i ett spel med oberoende rörelse måste även den logiska träffidentiteten bestämmas i mjukvara. 

Full R1 kräver fortfarande sjätte original-NPC (andra stora mannen) och fri självständig X-rörelse; fem NPC med fyra fasta fjärde-P0-X är inte tillräckligt. Även karta, full dörr/nyckel och flera andra element återstår. 14-radig visuell upprepning är ett estetiskt researchförslag, inte godkänd ny mask- eller höjdcanon.

### Nästa forskningsgrind

**R1y** undersöker en tredje grov fördröjning, GUI-skott-X **286–300**, alltså genom och förbi andra stora P1:s högra kant x295. Detta ska testas med samma strikta 600-Stella-kontroll; endast ett verkligt PASS får räknas som utökat användbart rasterfönster. Om R1y fallerar visar det en verklig timing-/färggräns och leder till specialiserade regionkernlar (#14) eller en alternativ samordning av M0 och P0.

**Integritet:** `main`, ROM DEVELOPMENT:s draft PR #7 och VERIFICATION issue #8 har inte ändrats av forskningen. Full R1: fortfarande **FAIL/BLOCKED**.
