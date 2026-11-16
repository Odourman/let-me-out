# LET ME OUT! – MAIN V: R1-F3 självständig mottagning och nästa R1-blockerare

**Datum 2026-11-16.** **Typ:** MAIN:s oberoende källa-/arkiv-/pixelgranskning av **utvecklarens frysta** F3-resultat, **inte** separat VERIFICATION, ROM-exekvering av MAIN, R1-PASS eller fullspelskodauktorisation.

## 1. Exakt fryst R1-F3 och testade utfall

- ROM DEVELOPMENT II-branch: `rom-dev/v018-r1-f3-two-independent-x-20261116`, fryst commit **`65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190`**.
- [F3 originalleverans – teknisk rapport](https://github.com/Odourman/let-me-out/blob/65cdeb3cd9d6ab120043f8bd2f5a3d1106ff8190/rom/v018/experiments/r1_free_xy/TO_MAIN_R1_F3.md).
- Auktoriserad [F3-arbetsorder](MAIN_V_TO_ROM_DEV_II_R1_F3_TWO_INDEPENDENT_X_RUNTIME_FEASIBILITY_AUTHORIZED_2026-11-16.md) och frysta F2-bascommit **`485a6c10047fb9b41e589ac3df724c1bc70f0283`** och F2-ROM-SHA **`941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b`**. F2:s verkliga EN dynamisk X-kontroll (index2 x129↔135) kvar som tidigare DEVELOPER_LOCAL_PASS.
- F3 byggde **en enda** modifierad G0-ROM med index0:s `RESP1` c19→**c20**, `GRP1` c22→**c23**, index1 c28 och index2 c37 orörda. Ingen faktisk F3-G1 tvåindivids-runtime-ROM byggdes när stoppgrinden blev röd. Ingen R2/R4, Y-expansion, R1+R3, PR#7-merge eller VERIFICATION.

### MAIN:s egna raw-arkivkontroller

Alla fyra ZIP:ar har hämtats från faktiska projekt-Drive-filer (parent `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`), inte bara från leveransrapportens påståenden:

| Verkligt arkiv | Byte | MAIN egen helfil-SHA256 | ZIP-CRC |
|---|---:|---|---|
| [F3-G0 16 autentiska Stella-rutor + F6-binär, ASM och symboler](https://drive.google.com/file/d/15mEW912Scoyjt0R8w5d4OT5xDNB-vIGi/view) | 152 488 | `f3cf50fecdcf162131f5c7149206e7799ffcee5d2cbc69299027936a5196238e` | PASS, 29 poster |
| [Stella TIA-registertraps](https://drive.google.com/file/d/1c2rgDld35oPj9_Y2PPEihe7dOHFJZMro/view) | 77 167 | `ee298a6b384066d3fd1760a50d2528eb6e5667b6dfae71e94094b22b9cd9d95a` | PASS, 15 poster |
| [GUI-validerad första RESP1 c20-omtagning](https://drive.google.com/file/d/1GOpFrrndtEro4u94m8DTklOJH4x7wMXD/view) | 25 813 | `81b08bf18e0aa18a5b42af5a9d949dce8419bbf9dfa5c8b7cdf7df1b24eb11c6` | PASS, 6 poster |
| [Read-only mutantcheck (INGA nya riktiga Stella-rutor)](https://drive.google.com/file/d/1vLFnCiu8rK4kdz91gkJ-rm7Gef2Per6Y/view) | 46 446 | `caa2179d93d7a08b8c7121abf63cd311103a0182be907188261b61f352362653` | PASS, 6 poster |

MAIN läste den verkliga F3-G0 16 384 byte F6 ROM inuti ZIP och beräknade `SHA256=1ed9cd9f735dcbf4cd2dc731da607d84a9c4f85f3c894a4dbd48d2d3fc50c286`, exakt rapporten; **4/4 4 KiB-bankkopior är byteidentiska**.

MAIN beräknade också själv varje av de 16 ursprungliga rå-PNG:ernas SHA256 mot `RAW_PNG_SHA256SUMS.txt`: **16/16 PASS**, och använde en **egen direkt Pillow-pixelunion** från de oförändrade maskraderna i `design/NPC_REFERENCE_8x9_masks.json` (GitHub blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`), där en TIA-pixel är **två pixlar i 900×300 Stella-debuggercropen**. Resultat: **16/16 raw frame union exakt**, nio korrekta originalrader, vitpixlar **348** i varje frame, inga saknade/extra vita maskpixlar, positionsursprung **[43,75,129,183,243,303]** för samtliga sex.

**F3:s faktiskt begärda första X = 49, men observerade första X = 43 i 16/16.** Det är en **sex crop-pixel positionsdiskrepans**, inte en fysisk ghostmask. De fem andra står kvar på [75,129,183,243,303]. Visuell position **FAIL** trots att originalmaskerna är fullt korrekta.

MAIN öppnade även verkliga `stella_full.png` i c20-omtagningen: debuggerns `Dest RESP1`, efterinstruktions-PC **`$F1D1`**, `Scn Ln 123/262`, `C. C 20`, `Color Clk 60`, bank 0, A=`$24`, X=`$00`, Y=`$01` är faktiskt synliga i GUI-bilden. Scriptets `trapWriteIf` anger `_scan==123` och `_sCycles>18 && <22`. Detta bekräftar en **visuell loggad 6502/TIA-skrivfas**, inte att kopian flyttades.

CI [43929134626](https://github.com/Odourman/let-me-out/actions/runs/43929134626) är **RÖD** för verkligt G0-positionstest; [43929951068](https://github.com/Odourman/let-me-out/actions/runs/43929951068) grön endast för riktad första c20-trap; [43929551642](https://github.com/Odourman/let-me-out/actions/runs/43929551642) grön endast för read-only negative-mutationstest från äldre F2; **inte** en ny F3-fotoposition-pass.

## 2. MAIN:s beslut och hård statusgrind

**`F3_SECOND_INDEX_GEOMETRY_LOCAL_FAIL`** för *den enda* mål-c20-varianten. **`F3_TWO_INDEPENDENT_RUNTIME_X=INCONCLUSIVE/NOT_RUN`** eftersom den föreskrivna geometri-stoppgrinden utlöstes. **FULL R1 fortsatt `BLOCKED/NOT ACCEPTED`**; inte sex fritt individuellt X/Y, 600-fria-frames, R1+R3, T01–T16 eller oberoende VERIFICATION.

Varning för falskt generellt hinder: Att `RESP1 c19→c20` verkligen sker medan första originalmasken står kvar vid x43 betyder inte att alla tidigare/senare strober eller andra index omöjligt kan ändra X. [Andrew Towers TIA Hardware Notes](https://www.retroisle.com/atari/vcs/Technical/Hardware/TIAnotes.php) beskriver att manuell RESP inte genast startar huvudkopian; NUSIZ-close/medium kopie-start-signaler har faser och ett särskilt gränsfönster. **Detta är extern mekanik, inte uppmätt kausal förklaring i vår specifika ROM.**

## 3. Ett separat snävt ROM-uppdrag, inget annat

MAIN utfärdar endast [R1-F4 – EARLY-COPY PHASE GEOMETRY](MAIN_V_TO_ROM_DEV_II_R1_F4_EARLY_COPY_PHASE_GEOMETRY_AUTHORIZED_2026-11-16.md) **inom redan användargodkända v0.18/NTSC/R1** i [Issue #6](https://github.com/Odourman/let-me-out/issues/6). Detta är **ny uttrycklig MAIN-avgränsning**, inte tillstånd för nya R2/R4, annan ROM-kernelarkitektur, fler R1-F5/F6-delprov, PAL, modifierade originalmasker, kopplade X/Y eller spel. Starta inte oberoende VERIFICATION förrän MAIN fryser ett större acceptansbart evidenspaket.
