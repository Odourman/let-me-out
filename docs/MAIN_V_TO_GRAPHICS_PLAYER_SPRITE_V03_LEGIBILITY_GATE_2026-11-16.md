# LET ME OUT! – MAIN V till GRAPHICS
## PLAYER SPRITE v0.3 – Weapon-versus-third-leg legibility gate

**Datum:** 2026-11-16. **Kategori:** nytt snävt **GRAPHICS DESIGN**-uppdrag. Ej ny canon, ROM-, Stella- eller implementationsorder.

### 1. MAIN:s mottagning av v0.2

GRAPHICS levererade i chatten två faktiska åttabits- och nioradersmasker jämte v0.1 A. MAIN har återberäknat deras pixelantal, A-vs-variant-bitdifferenser och hexrader från **de faktiskt inklistrade bitmapparna**:

| Mask | Fulla rader top→bottom | Gula pixlar | Ändrade bitar mot v0.1 A |
|---|---|---:|---:|
| A v0.1 | `3C 7E 3C 18 7C DC 98 24 42` | 33 | 0 |
| A1 v0.2 | `3C 7E 3C 18 3C 7C D8 14 22` | 33 | 8 |
| **A2 v0.2** | `3C 7E 3C 18 7E 5E D8 94 22` | 36 | 9 |

Båda v0.2-varianterna behåller A:s exakta rader 0–3, har 8×9 bitmapdatastorlek och synliga gula pixlar i alla nio rader. Välkontrollerat DATAUNDERLAG, **inte** ROM-test eller användargodkännande. Grafiskt pekar **A2** närmare den handritade pistolens diagonal nedåt-vänster, men dess utstickande gula pixlar vid vänster lår/knä riskerar att tolkas som ett tredje ben. A1 är renare men liknar ännu mindre ett avskilt vapen. MAIN väljer **A2 som ARBETSBAS, EJ SLUTGODKÄND**.

**Arkivmottagningsreservation:** GRAPHICS text beskriver ett ZIP-arkiv på 271 563 byte / 38 poster / SHA256 `02a71e790b2c3b2a57f67047aebe45def440a75935b2bf45b5f5e0d25a9601b1`, men texten ger **inga fungerande fil-URL:er eller bifogad ZIP**. Vid MAIN:s Drive-inventering 2026-11-16 hittades **inget `PLAYER SPRITE v0.2`-ZIP i dedikerade projektmappen**. Därför har MAIN varken kunnat läsa de 38 filerna eller oberoende verifiera ZIP/hash; siffrorna är tills vidare **utvecklarpåståenden, ej MAIN-verifierade**. Skapa/leverera faktisk länk eller lämna arkivet som `MISSING`, gissa inte filvägar.

### 2. Den tydliga konstnärliga frågan

**Kan spelaren visas 8×9 med igenkännbar hatt, mänskliga två ben och ett SNEDSTÄLLT VAPEN I HANDEN snarare än ett tredje ben – när man betraktar sprite i dess riktiga lilla storlek utan förklarande etiketter?**

Sannolikt är detta en **siluett- och negativ-rumsfråga**, inte endast "gör pipan en pixel längre". Handritad originalspelare: `LET_ME_OUT_MAIN_HANDOFF_2026-11-15.zip/assets/02_USER_PLAYER_SKETCH.jpg` (blå penna), vapnet hålls i vänster hand och pekar snett nedåt-vänster; hatt med brätte, mänsklig bål, två fötter. Samma visade höjd/skala som nio synliga rader för de två stora vita androidtyperna, gul P0 i 1 färg. Inga nya TIA-objekt, ingen extra färg eller ändrad koppling till M0-skottet.

### 3. DITT ENDA UPPDRAG: HÖGST TVÅ NYA 8×9-KANDIDATER

**V03-A2R – strikt A2-orienterad förbättring:** Behåll hattens igenkännbara krona och brätte men flytta de minsta antal nödvändiga pixlar för att vapnets nedåt-vänstra diagonal går att skilja från VÄNSTER BEN. Skapa tydligare tomrum/visuell avgränsning mellan vapenpipa och två ben. Vapnet ska kunna läsas som ett objekt som hålls, inte som lösgjord prick. Alla 9 rader ska synas; de 8 kolumnerna kan inte breddas; våga ändra hals/arm/ben om det behövs.

**V03-B – alternativ SILUETTSTRATEGI:** Inom **samma 8×9** får du även omfördela hatt/huvudets fyra övre rader, **förutsatt att hatt med tydligt brätte fortfarande går att känna igen och figurens skala är oförändrad**. Det ger mer frihet för ett mer karakteristiskt grepp och vapen med tydlig kort pipa nedåt-vänster. Målet är en verkligt annorlunda lösning på vapen-versus-ben, inte en tredje kosmetisk A2-version. Förklara om den alternativa hatten försämras. Byt inte spelarkaraktär eller riktning till höger bara för att det är enklare.

**Bevarad jämförelsebas:** A v0.1, A1 v0.2 och A2 v0.2 ska alltid finnas med oförändrade. Originalets fyra NPC-masker i `design/NPC_REFERENCE_8x9_masks.json` är skyddade och får inte ändras. R1-F3:s individuella X-FAIL ändrar **inte** dessa visuell-canon.

### 4. VISUELL KVALITETSGRIND SOM MÅSTE VARA REELL

- Leverera riktiga 8×9 bitmatriser, 9 rader uppifrån, hex per rad, pixelantal, bitdiffar mot A2, original och nya SHA256/checksummor. Kontrollera genom kod, inte uppskattningar.
- Skapa exakta PNG med naturlig Atari-illustrationsskala, **verklig 1× bitmap**, samt närmaste-granne 2×/4× och separat 20× med pixelrutnät; uppskalningen får aldrig vara enda beviset för läsbarhet. Möjlig resultatbild med gul P0, vit stor man/kvinna på mörk bakgrund i samma maskpixelskala.
- Gör **anonymiserad avbildning utan etiketter** för varje kandidat, i mörk spelbakgrund, samt rent svartvitt omvända/kontroll, där det syns om pipan går att skilja från tredje benet. Om möjligt gör en enkel mänsklig läsbarhetsbedömning; ange tydligt om bara GRAPHICS själv har bedömt den.
- Visa raderna som visuella ASCII-gridar med bevarat mellanrum/negativ yta; markera vapen-hand-ben-samband i ett separat annoterat diagnoslager, aldrig i det grafiska källassetet.
- Jämför vad som **faktiskt** blivit bättre mot A2, och vilken detalj som försämrats. Välj EN favorit men märk `GRAPHICS CANDIDATE / EJ GODKÄND / EJ STELLA-TESTAD`. Om ingen inom 8×9 skiljer vapen från tredje ben på naturlig skala: säg `8x9 WEAPON READABILITY STILL FAILED`, föreslå en teknisk valfråga till MAIN – men BYT INTE själv till 8×10, extra sprites eller andra nya arkitekturer.
- **Avsluta efter dessa max två varianter.** Ingen v0.4 eller oändlig kosmetikserie utan nytt beslut.

### 5. FULLSTÄNDIG OCH FAKTISKT ÅTKOMLIG LEVERANS

**Först:** rätta leveransbristen från v0.2 genom att **ladda upp** det redan skapade 271 563 byte/38-filers grafikpaketet till den dedikerade Drive-mappen (om det verkligen finns) eller tillhandahåll **faktisk nedladdningslänk** till verifierbar användarfil. Rapportera en ny SHA om bytes ändrats och lämna original-SHA som historisk claim, inte obemärkt ersättare.

**Sedan:** paketera v0.3:s två nya varianter, jämförelsebilder, källmasker, egen testskript och sammanhållen `PLAYER_SPRITE_V03_TO_MAIN.md` i eget ZIP eller verifierbara filer. Följ projektmappen https://drive.google.com/drive/folders/1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u och ange verkliga Drive-/sandboxfil-URL:er, manifest (filnamn, storlek, SHA256), källstatus, vad som INTE är testat. En bild med visuellt perfekt vapen bevisar **inte** ROM-/Stella-pass.

**Projektskydd:** GRAPHICS skapar endast designkandidater och handoff. Ingen ROM-kodändring, P0-byte, R1/R2/R3/R4-integration, MAIN-canonändring, PR #7-merge, Issue #8-VERIFICATION, nya Atari-hårdvarukrav eller ändring i The Cabin/I Love a Fish. För grafiska förslag krävs inte ett konstgjort CI-resultat; MAIN och användaren fattar senare beslut om kandidat och eventuell separat ROM-testorder.

### 6. Auktoritativa länkar

- [MAIN:s GRAPHICS-rollinstruktion](MAIN_V_GRAPHICS_CHAT_STARTPROMPT_2026-11-16.md).
- [MAIN:s v0.2-order](MAIN_V_TO_GRAPHICS_PLAYER_SPRITE_V02_REFINEMENT_2026-11-16.md).
- [Oförändrad ursprungsdesign, original NPC-masker](../design/NPC_REFERENCE_8x9_masks.json).
- [Spelarens skal-/silhuettbeslut](MAIN_PLAYER_SCALE_V018_2026-11-15.md).
- [Användarens handritade ursprungskälla och 57 beslut](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view).

**Det viktigaste är att kunna se ETT HÅLLT VAPEN och TVÅ BEN – inte att vinna ännu en omgång av pixelantal eller rendering i 20×.**
