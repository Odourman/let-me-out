# TO_MAIN_PLAYABLE_SLICE_V01 · ROM DEVELOPMENT IV → MAIN X

**PLAYABLE_SLICE_V01_GAMEPLAY_LOOP_OBSERVED_RENDERING_PARTIAL.** En verklig NTSC/F6-ROM gick att spela från kallstart till rumsutgång med joystick i Gopher2600, helt utan POKE. Rundans slut var **210 poäng och tre liv**. Rendering är fortfarande en blockerare för användbarheten. Vid kallstartsprovets nyckelfall syntes ingen nyckel. Högerdörren visar ännu inte sitt visuella låst-/öppet-tillstånd.

`let-me-out-v01.bin` är **16 384 byte** med SHA-256 `7115e3c8c46f8296106a6320622b501eb57a28ac431631b83a6f61e227f0d1e6`. Öppna den i stock Stella som F6/NTSC och använd piltangenter och mellanslag. [Spelarinstruktioner](README.md) · [Originalinspelning från Stella 6.7.1](evidence/stella-play.mp4)

## Underlag

Jag läste AGENTS.md, levande arbetskö, G5-spärr, originalets Master Spec och CSV med 57 beslut samt senare LM-D12–D17/D19. Drive-originalen har SHA-256 `9ddc9a27e68a6e874489a33e0fb189d3689fb298b3cbe6b3991113eaa8fc5b30` respektive `e0136b89195c567c33a7435896c77f57e44c0a66555d6fcefed3df81ae8614f1`. Kartan A_OPEN_01 genereras från godkänd 40×22-källa med Git-blob `0e449f97f87bd9b403476fd1435398042eaee285`, som underlag för både kollision och bild. Historisk v0.18-diagnostik vid `82667dae033f70570dce903f8e1d4866528be02a` gav referens för playfield och bildrutor. Spelarmasken hämtas från projektets frysta G5BE-kärna. NPC-maskerna genereras ur projektets godkända 8×9-JSON. Frysta positiva och negativa ITER5/ITER6-resultat ligger kvar på sina ursprungliga refar. [Originalarkiv](https://drive.google.com/file/d/1mqU07Q7xTgU5t5lYQhCOyI7wRQl6vD7o/view) · [Kartbeslut](https://github.com/Odourman/let-me-out/blob/main/docs/gates/G5X_MAIN_VII_APPROVED_FUTURE_FOUR_MAPS_SOURCE_MANIFEST_2026-11-17.json) · [ITER5](https://github.com/Odourman/let-me-out/issues/30#issuecomment-7001014340) · [ITER6](https://github.com/Odourman/let-me-out/issues/30#issuecomment-7001424130)

## Implementerat och provat

| Funktion | Status | Mätutfall |
|---|---|---|
| Joystick och väggkollision | IMPLEMENTED / RUN / PASS | Åtta riktningar med riktig controllerinput. Spelaren stannade vid X4 vid ytterväggen och vid X24 framför innerväggen. Båda stock Stella-versionerna visade förflyttning under faktisk tangentinput. |
| Skott | IMPLEMENTED / RUN / PASS | Nedtryckt knapp höll spelaren på samma X/Y. En hållen knapp gav inget andra skott efter väggträff. Ny knappkant medan ett skott levde behöll det tidigare skottet. Släpp och nytt tryck kunde skjuta igen. Väggkollision slog av skottet. |
| Fem NPC | IMPLEMENTED / RUN / PASS för provad logik | M/M/F/SM/SF har fem separata X/Y och samma 8×9-box. Fredlig patrull före skottet, jakt från första avfyrningen. Seedade prov visade alternativt steg runt vägg och annan fiende. NPC skjuter aldrig. |
| Träff, kontakt och liv | IMPLEMENTED / RUN / PASS | En träff räckte. Vid samtidstestet vann skottet, score 10 sjönk till 0 och tre liv kvarstod. Separat jaktkontakt kostade ett liv. |
| Nyckel och poäng | IMPLEMENTED / RUN / PASS för tillstånd | Nyckeln blev golvobjekt först efter dödsanimation. Seedat bildprov visar 14 nyckelpixlar. Seedad runda gav 40→10 vid träff, 10→60 vid upptagning och 220 vid faktisk passage med fyra överlevande. Upplåsning gav ingen poäng. |
| Bärarval | IMPLEMENTED / INCONCLUSIVE | LFSR har 255 tillstånd och 51 per index efter mod 5. Sju startankare valideras mot kollision och nåbarhet i bygget. Verklig startentropi och likformighet över hårdvarustarter återstår. |
| Fyra grafiska masktyper, synlighet och dörrgrafik | RUN / FAIL | En fiende eller nyckeln kan utelämnas när dess Y-band konkurrerar om P1. Den orange dörren med svart nyckelhål och synlig öppning återstår. Spelare/PF kan få artefakter vid P1-byte. |
| HUD, extralivströsklar, fysisk Atari | NOT_RUN | Poäng och liv finns internt. HUD och extralivströsklar är ej implementerade i V01. |

Kallstartrundan använde `STICK LEFT …` i Gophers debugger, läste RAM och skrev inga spelvärden. Spelaren gick från vänsterstart ned till (12,154), sköt åt höger, gick ned till Y159 och korsade södra korridoren. Upptagning gav 50 poäng. Därefter gick spelaren upp längs högra väggen till (148,80). Upplåsning höll score på 50. Vid (160,80) sattes avslutsflaggan och score blev 210. En tidigare rutt träffade en annan android och en andra rutt gav faktiskt kroppskontaktdöd. Båda försöken finns i råloggarna. Kallstartsnyckeln var logiskt nåbar men osynlig i sin tagna golvbild. Det seedade provet visar att P1 kan rendera den när en slot är ledig.

## Raster, bildkvalitet och hårdvara

Den spårade slutversionen gav **600/600 sammanhängande Gopher-bildrutor med 262 scanlines** under växlande joystickinput. I samma serie rapporterade P1-planeraren minst ett utelämnat objekt i **347/600** bildrutor och högst två vid ett och samma tillfälle. NPC:ernas spelrörelse fortsätter när renderingen saknar slot. Ingen rörelsebana låstes för grafiken.

Den tidigare A/B-ROM:en varierade mellan 261 och 262 rader. Ett tidigt långprov nådde 263 rader. Fasloggen ledde till flytt av overscan-timerstarten bort från en WSYNC-gräns och till kortare inträde i första rumsraden. Huvudbilden startar vid SL44, sista rumsraden är SL219 och overscan börjar vid SL228 enligt Gophers koordinater. Längsta P1-placeringsrad når högst **75 CPU-cykler** vid kantens X148, inklusive WSYNC. Det fysiska kantprovet nådde synkskrivningen vid CL148 (c72). Källräknad normal grenväg är högst 70 cykler. Första rummets normala rad har sju extra förberedelsecykler och når högst 74. Första glyph-radens budget är högst 65 inklusive möjlig gränspassage för grenen. Stella-bildrutelängd och hårdvarustabilitet är NOT_RUN.

RIOT täcker som högvattenmärke 108 byte i $80–$EB och den djupaste väg som observerades för väggprov gav SP=$F7 från $FF, åtta stackbyte. **116/128 RIOT-byte inklusive stack.** F6-bilden har fyra banker om 4096 byte. Bank 0 har video, bank 1 spellogik, och bank 2/3 kopierar video. Växling vid $FFF6/$FFF7 sker utanför aktiv raster.

Isolerad pixelkalibrering gav exakt gul P0-mask på tolv X-värden. P1-förhämtningen förbättrade den första maskraden. Den senare kalibreringen hade exakta originalpixlar för åtta uppmätta X-värden mellan 32 och 148. Längre till vänster hade X4/12/17/24 fysiska pixelfel. Heltäckande fler-NPC-rendering återstår. Ett kontrollerat stilla rumstest mot originalgriden gav **180 saknade och 84 extra bruna pixlar** av 4992 förväntade. Den logiska kartan använder originalets väggceller.

## Bygg och återkör

DASM **2.20.14.1** byggde de två kodbankerna. Gopher2600 **v0.57.2** mätte controllerinput, TIA/CPU, scanlines och RIOT. Stock Stella **6.7.1/7.0** körde slut-ROM:en med verkliga X11-tangenttryck. Originalbilderna ligger i `evidence/images/`. Inspelningen är 7,87 sekunder enligt ffprobe. Verktygshashar ligger i `evidence/brief/tools.txt`. [G5AR](https://github.com/Odourman/let-me-out/issues/19#issuecomment-6976852310) · [Stock Stella 7.0](https://github.com/Odourman/let-me-out/issues/27#issuecomment-6983956225)

Från `rom/playable-slice-v01` med G5AR-prefixet och Python/Pillow. Korta resultat finns i `evidence/brief/`. Råarkivet innehåller ursprungliga emulatorbilder, PTY-svar och tidigare negativa prov.

```bash
export PYTHONDONTWRITEBYTECODE=1
python build.py
sha256sum -c SHA256SUMS
out=$(mktemp -d)
python replay.py let-me-out-v01.bin "$out/basic" > "$out/basic.jsonl"
for case in patrol wall touch priority key-door soak unseeded controls npc-obstacles; do
    python scenarios.py let-me-out-v01.bin "$out/$case" "$case" > "$out/$case.jsonl"
done
python phase.py let-me-out-v01.bin > "$out/phase.jsonl"
python phase.py let-me-out-v01.bin --max-x > "$out/max-x.jsonl"
python calibrate.py let-me-out-v01.bin "$out/cal" > "$out/cal.jsonl"
bash stella_play.sh let-me-out-v01.bin "$out/stella671" 583 record
STELLA_BIN=/workspace/work/g5bb/stella7/usr/bin/stella \
    bash stella_play.sh let-me-out-v01.bin "$out/stella70" 584
```

**Mottagningspunkt för MAIN X.** En styrbar enrumsloop är levererad i en isolerad branch. Synligheten för fiender, golvnyckel och dörr är konkreta återstående fel. Oberoende **VERIFICATION II är NOT_RUN**. `G5_FORMAL_OPEN` kvarstår.
