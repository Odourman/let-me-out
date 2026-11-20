# Framtida individuella NPC-former

Det godkända framtida målet har fem individers visuella utfall och fyra oförändrade masker. Följaktligen finns 4⁵ = 1 024 ordnade formkombinationer. Var och en av de fyra homogena kombinationerna måste vara nåbar och har sannolikhet 1/1 024 vid fem oberoende likformiga val.

Nuvarande RNG är en 8-bitars Galois-LFSR med 255 icke-nolltillstånd. Fem deterministiska anrop med bara detta initiala tillstånd kan ge högst 255 olika kombinationer, oavsett vilka två bitar som läses. En framtida implementation behöver minst tio bitars utfallsrymd vid rumsstart. En möjlig metod är ett likformigt 16-bitarsvärde och fem disjunkta tvåbitsfält. Om en maximal 16-bitars LFSR används behöver dess likformighet vid faktisk sådd först visas. En avgränsad avvisningsmappning kan då acceptera tillstånd 1–64 512, subtrahera ett och använda de låga tio bitarna. Varje formkombination har då 63 representanter i den accepterade tillståndsrymden.

De fem värdena ska förbli stabila under rummet. Separata fält kräver tio bitar och därmed två packade byte. RIOT är fullt i checkpointen. Undersök därför en bitvis packning i den befintliga riktnings- eller blockeringslagringen och maskera samtliga berörda läsningar och skrivningar. Key-carrier ska dras separat per individ och får varken härledas ur formkod eller begränsas av formfördelningen.

I renderaren behöver `Shapes`, `LeadingBlank` och samtliga fasta antaganden om SM/SF-index ersättas med den faktiska formen för individen. Behåll logisk 8×9-kollisionsruta, identitet och AI. För varje ny uppställning ska samma-Y och de specialiserade maskvägarna provas, även när flera instanser har samma mask. Detta är rådgivande analys. RNG och formtilldelning är NOT_RUN i dessa två ROM:ar.
