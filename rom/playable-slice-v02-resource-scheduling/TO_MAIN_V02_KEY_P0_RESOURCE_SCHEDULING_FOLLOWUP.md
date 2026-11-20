# TO_MAIN_V02_KEY_P0_RESOURCE_SCHEDULING_FOLLOWUP

**DEVELOPER_OBSERVED · Demonstrerade lokala blockerare.** Båda spelbara ROM:arna från `efe23bde3a1b6c6edbfc4fbf9f96c3f95dddd66a` återbyggdes byteidentiskt med DASM och kvarstår som checkpoint. Den nya commiten innehåller provkod, körbara diagnostik-ROM:ar, bilder och mätningar.

## Nyckel och P1:s horisontella fas

VDELP1 valde den äldre GRP1-latchen under den tidigare P1-överlämningen. Två lika långa TIA-skrivningar ändrade latchvalet på setup- och glyfvägen. PX24/PY151 och PX60/PY151 gav båda **14/14 guld, 0 extra och 262 rader**, men SM blev **14/20 respektive 5/20**. Dessutom kvarstod en saknad gul pixel i båda. Det är FAIL. Fryst kontroll PX60/PY159 ger 14/14 och de två frysta PY151-fallen ger 0/14. Fryst nyckel med aktivt skott ger 14/14 utan extra guld.

Gopher på X24-provet loggade CPU-stegen före→efter respektive skrivning. SL197: GRP1 CL−59→−50, VDELP1 −41→−32, HMP1 55→64 och RESP1 64→73. SL198: HMOVE −68→−59, GRP0 −35→−26, VDELP1 −2→7, GRP1 19→28 och COLUP1 40→49. P0:s origin flyttades inte i provet. Latchvalet ändrade maskbyte men behöll inte SM:s tidigare horisontella P1-position efter RESP1. Nästa användbara schema behöver en separat positioneringsfas eller en extra, tidsdelad maskkälla som kan leverera de vita SM-pixlarna innan P1 tar nyckeln. Det provade latcheschemat räcker inte.

## Playfield och HMOVE

Alla 16 saknade bruna pixlar i vart och ett av de frysta låst/öppet/golvnyckelproven ligger i X0–3. Två faktiska varianter av HMOVE-suppression återställde fyra vid X123/Y90 utan saknade eller extra NPC-pixlar i det isolerade provet.

- **Före WSYNC, FAIL.** Villkoret flyttade WSYNC före skrivningen från CL148 till CL154 vid X148. Skrivningen hann inte slutföras inom 76 cykler. Gopher gav 263 rader samt 14 saknade och 14 extra NPC-pixlar. X123 höll 262.
- **Efter WSYNC, FAIL.** X123 och X148 höll 262 och provmaskerna blev exakta. Grenen i vägen med finförflyttning flyttade HMOVE två CPU-cykler. F-masken fick 11 saknade och 11 extra pixlar i en riktad fixtur. Både TOP och BOTTOM höll 600×262 men nådde bara **533/600** exakta femmaskersbilder med extra vitt i **62/600**. Båda klarade kallstartsrundan med 210 poäng och tre liv. En körbar lösning behöver välja nollrörelsevägen före rasterkonflikten och bevara den ordinarie HMOVE-fasen för övriga X.

## M(1) och samtidigt Y

Vid exakt samma bildnummer och koordinater i fem riktade TOP-bilder var RGB **255,255,41** i fryst ROM, **255,255,254** när GRP0-skrivningar ersattes med lika långa skrivningar till en oanvänd TIA-adress, och **6,6,6** när både GRP0- och GRP1-skrivningar isolerades. M0/M1-skrivningarna behölls. 101/101 mätta speltillstånd och radantal matchade mellan sekvenserna. Testet identifierar P0 som källan till den gula pixeln och P1 som källan till den täckta vita pixeln i bilder 96–99 vid (112,97) och bild 101 vid (117,97). Den kompletta vita maskens krav kvarstår.

Färska frysta V02-körningar visar fortfarande **2/5** kompletta masker i det ordinarie Y86-provet, omordningen och tät X-grupp. G5BE ITER6:s tidigare domänavvisningar bevaras som avvisningar. En distinkt integrerad femslottsport **NOT_RUN**.

## Checkpoint och bevis

Färska frysta tester i båda varianterna omfattar riktig kallstartsjoystick utan RAM-POKE (210 poäng, tre liv), riktade nyckel- och same-Y-prov, samt faktisk Stella-input med originalbilder. Fryst 595/600, skott 10/10, 65/65 kallstartsnyckel, öppning 256/256, PF 16/16/16 och uppmätt 128 RIOT-byte inklusive stack är tidigare bevis knutna till de byteidentiska binärerna. Ny 600-bilds körning av den byteidentiska frysta basen **NOT_RUN**. Diagnostik-ROM:arna får inga spelbara godkännanden. Fysisk Atari **NOT_RUN**.

**G5_FORMAL_OPEN. INDEPENDENT_VERIFICATION=NOT_RUN.**
