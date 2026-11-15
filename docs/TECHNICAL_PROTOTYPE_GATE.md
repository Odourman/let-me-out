# Framtida ROM-test: teknisk grind (ej auktoriserad)

**Status:** planerat test; ingen kodstart godkänd, ingen ROM byggd.

## Syfte

Bevisa eller falsifiera om Atari 2600 kan visa det planerade spelets viktigaste element samtidigt med godtagbar spelbarhet och timing. Detta dokument är inte ett implementeringsuppdrag.

## Obligatoriska stresstillstånd

1. Sex levande androider i olika höjder, spelare och speglade väggar.
2. Sex androider på samma rasterhöjd som varandra, spelaren och ett aktivt skott.
3. Nyckel efter förstörd bärare (max fem levande androider) plus spelare/skott.
4. Högerdörr med endast högeröppning medan innerväggarna är speglade.
5. Trånga passager, överlappande visuell höjd, flera figurer med olika silhuetter.
6. Stabil NTSC-timing i Stella Debugger, och uttryckligt klargörande om PAL senare ska testas.

## Acceptanskriterier som behöver förfinas före start

- Faktiskt körbar binär och full reproducerbar 6502-assemblerkälla.
- Loggade scanlines och cykler per skärmlinje, med angiven ROM/build-hash.
- Video eller Stella-frame dumps på svåraste bildfallen; synligt flimmer bedöms och redovisas, inte döljas.
- Dörrtest visar högeröppning utan felaktig vänsteröppning.
- Kontrollera att grafiktekniken inte stjäl nödvändiga TIA-objekt från spelarens skott.
- Separat **VERIFICATION** bedömer ROM oberoende av den som skrev den.

## Risken med tidigare underlag

Tidiga placeringstester fann fyra androider i samma rasterlinje i vissa startlägen. Det är **inte** värstafallet. Under rörelse kan samtliga sex sammanfalla i höjd; även spelare och skott måste budgeteras.

Ingen offline-simulering bevisar att Atari 2600-kerneln fungerar. Inga siffror från modelltester ska marknadsföras som Stella-timing.

## Tillståndsgrind

Inled inte ROM DEVELOPMENT, kodändringar, binärgenerering eller verifiering innan MAIN får **separat uttrycklig användarauktorisation**. Föreslagna P2/J2/C02/C-1 får inte tyst förvandlas till slutliga beslut.

## Upphovsrätt och repositories

Publicera inte användarens Berzerk-referens-ROM, reproducerad kommersiell kod eller andra tredjepartsbinärer i detta offentliga GitHub-förråd.