# TO_MAIN_V02_R2_REACHABILITY_AND_YELLOW_KEY_RESCUE_TEST_ONLY

**DEVELOPER_OBSERVED · R2-felet är nåbart i verkligt spel.** Båda kritiska PX/PY-lägena reproducerades med joystick från kallstart, verkligt skott, dödsanimation, tappad nyckel och fyra levande NPC. Gul $1E med kontinuerlig blinkning när nyckeln ligger på golvet gäller som användarens visuella krav. Takt 8/4 eller 6/6 är fortsatt ospecificerad för framtida spel.

## R2 REALITY

| Klass | Position och prov | PÅ | AV | Fortsättning |
|---|---|---:|---:|---|
| REAL_COLD | TOP 8/4, PX24/PY151 efter förflyttning av levande SM till Y149 | 0/14 i 16/16 bilder | 0/14 i 8/8 | Nyckeln plockades upp. Senare utgångsrutt gav rasterfel, från 262 till 289 och andra felvärden, och slutade med två liv. |
| REAL_COLD | BOTTOM 6/6, PX60/PY151, SM Y151 | 0/14 i 12/12 bilder | 0/14 i 12/12 | Upptagning och fysisk utgång, 210 poäng och tre liv. |
| REAL_COLD | TOP 8/4, PX24/PY151 med SM kvar på Y146 | 14/14 i 16/16 bilder | 0/14 i 8/8 | Senare utgångsrutt stoppades när spelaren träffades. |
| REAL_COLD | BOTTOM 6/6, avskuren väg rakt upp vid PX60 | NOT_RUN på målpositionen | NOT_RUN | En fiende träffade spelaren innan provpositionen. Arkiverat. |

Hårdproven ovan hade 262 rader under själva 24-bildsbesöket. I båda 0/14-besöken hade bäraren SF `Life=0`, fyra fiender `Life=$FF`, och nyckeln låg kvar vid X85/Y153. Inga RAM-ingrepp. Separata ordinarie kallstartskörningar klarade TOP 8/4 och BOTTOM 6/6 med upptagning på AV samt utgång med 210 poäng och tre liv. Det senare TOP-rasterfelet i lurrutten är ett nytt negativt spelbevis, ännu utan isolerad orsak eller motsvarande kontrollrutt.

## KEY RENDER

**CONSISTENT_SEEDED:** 17 fixturer × 12 konsekutiva bilder per ROM, 1 224 bilder över sex ROM:ar, samtliga vid 262 rader. En död bärare sattes till `Life=0` på nyckelns fallplats. Övriga fyra var levande. Proven validerar väggarnas kollisionspunkter och att levande NPC inte sitter i varandra eller spelaren. Alla identiteter 0–4 prövades, inklusive att SM själv var bärare. Detta bevisar planerarens beteende för de tillstånden. Det nuvarande kallstartsprogrammet valde SF i de körda spelrundorna.

- Nio av 17 fixturer gav 0/14 trots avsedd synlighet i varje variant. Vid de båda PY151-positionerna försvann nyckeln för fyra av de fem identiteterna. När SM var död gav båda positionerna 14/14. Vid PX104/PY151 med nyckeln till vänster gav referensen också 0/14.
- Återstående åtta fixturer gav 14/14 varje PÅ-bild. Varje AV-bild gav 0/14 utan extra gula keypixlar. Kontrollen använder $1A. Båda provrytmerna använder $1E. I fixturen med aktivt skott stämde skottpixeln i båda faserna.
- **OUT_OF_DOMAIN_STRESS:** gamla prov med fem levande fiender plus golvnyckel bevaras i blinkreferensen. De behövs inte för slutsatsen att felet finns i R2.

## RESOURCE GAIN

I det konsistenta PX60/PY159-fallet med levande SM, även med aktivt skott, går SM från 16/20 PÅ till 20/20 AV. Vid de två svåra PY151-positionerna räcker inte tidsdelningen för att få nyckeln synlig. M(1)-ocklusionsbevisen och den gula spelarprioriteten kvarstår.

En ny isolerad P0-rad byggdes med DASM. Den bevarar en vit SM-glyf på P1. Enbart andra RESP0 plus GRP0 gav ingen andra synlig huvudkopia i de uppmätta varianterna, oavsett skrivordning. Med ett tajmat `NUSIZ0`-extra START och andra GRP0/RESP0 återgavs vid PX24 exakt spelarens sex pixlar X25–30, nyckelhuvudets tre pixlar X86–88 och de två vita SM-pixlarna X62–63 på samma rad. Andra GRP0: CL46→55, RESP0: CL55→64. Vid PX60 gav samma schema fortfarande key X86–88 men tog bort spelarens X64–66. Ett sent försök med nyckeln till vänster gav endast nyckelhuvudet. Samtliga isolerade prober har 262 rader. Gopher rapporterade F6 för det slutliga far-provet. Ingen visade alla fem nyckelrader i samma bild. Skott och återställning av P0 inför nästa aktiva rad i den nya metoden är **NOT_RUN**.

V02-spåret visar ordinarie GRP0 CL−20→−11, GRP1 CL31→40 och WSYNC vid CL79 före skrivningen på den provade raden. Vid PX60 måste den först ritade spelarens lit-pixlar kunna gå till X66. Den provade extra-kopian kräver omskrivning före den gränsen för att landa på X86 med originalmasken. Koden behöver ett annat schema för den nära positionen snarare än bara samma registersekvens. Fasta NUSIZ-avstånd 16/32/64 matchar inte X-avstånden 61, 25 eller 19. Detta är en lokal blockerare för de provade schemana, inte en generell utsaga om TIA.

## R1 FEASIBILITY

Y86 X20/44/68/92/116 är fortfarande 2/5 i den spelbara femfiendersreferensen. 24 färgklockor mellan spriteorigin ger ungefär åtta CPU-cykler per återkommande position. Två nollsidesskrivningar kostar sex redan före grafikdata och looparbete. ITER6 visar att förladdade radpaket och fasval kan täcka vissa separerade koordinater; dess 126/128-byte diagnostiska layout och koordinatdomän kan inte läggas ovanpå hela V02-kärnan. Tidigare avvisade V02-koordinater räknas inte som renderingsresultat.

Vid täta same-Y-positioner kan kollisionslogiken tillåta åtta pixlars originavstånd. Det är mindre än nio färgklockor för en trecyklersskrivning. Transparens och en tidig förladdning kan ge ett fönster för enskilda maskrader, men det finns inget demonstrerat allmänt schema där. Gul P0 och M0 gör ett P1-schema nödvändigt på rader där P0 inte kan lånas utan pixel- eller färgkonflikt. Identiska maskrader kan dra nytta av NUSIZ vid fasta avstånd, medan oberoende former och X/Y kräver värsta fall med olika radbyte. En full fri femslottskärna är **NOT_RUN**. Varken glest, tätt, P0-samtidigt eller slumpade former har fått ett allmänt PASS.

## NEXT DECISION

Ge ett avgränsat uppdrag för **en flerradig R2-kärna** där den mätta P0-extra-kopian är en byggsten som måste få en alternativ radplan för nära och vänsterplacerad nyckel. Acceptera först efter 14/14 gult på PÅ, exakta spelare/fyra NPC/M0/PF, 262/76/128, samt samma riktiga TOP/BOTTOM-lurrutter hela vägen till utgång. Om nära/vänster aldrig når kraven behövs ett användarbeslut om synlighetskravet. R1 förblir separat. Denna rapport startar inget nytt implementationssteg.

De sex jämförelse-ROM:arna återbyggdes byteidentiskt. 595/600, 10/10 skott, 16/16/16 PF och 256/256 dörröppning hör till deras frysta standardbevis. Nya R2-fixturer och joystickutfall redovisas ovan. Stock Stella gav originalbilder från verklig input. Fysisk Atari och oberoende verifiering **NOT_RUN**. Ingen ny spelbar checkpoint utses.

**TEST_ONLY · G5_FORMAL_OPEN · INDEPENDENT_VERIFICATION=NOT_RUN**
