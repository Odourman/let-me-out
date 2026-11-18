; Generated from evidence/brief/solver.jsonl by emit_packet.py.
Packet48:
 sta WSYNC
 iny
Packet48_m0:
 ldx #0
 lda PlayerRows,y
 sta.w GRP0
Packet48_m2:
 lda #0
 stx.b GRP1
 ldx #0
 sty.b RESP1
 stx.b ENAM0
Packet48_m1:
 ldx #0
 sty.w RESP1
 sta.b GRP0
 stx.b GRP1
 lda #30
 ldx #14
 stx.b COLUP0
 sty.w RESP1
Packet48_m3:
 ldx #0
 stx.b GRP1
Packet48_m4:
 ldx #0
 sty.b RESP1
 stx.w GRP1
 nop
 sta.b COLUP0
 sta.w ENAM0
 rts
Packet48End:
 IF Packet48End-Packet48 > 64
 ERR
 ENDIF
Packet48Offsets:
 byte Packet48_m0-Packet48+1,Packet48_m1-Packet48+1,Packet48_m2-Packet48+1,Packet48_m3-Packet48+1,Packet48_m4-Packet48+1
Packet49:
 sta WSYNC
 iny
 lda PlayerRows,y
 sta.w GRP0
Packet49_m0:
 lda #0
 sta.b GRP1
 ldx #0
Packet49_m1:
 lda #0
 sty.b RESP1
 stx.w ENAM0
Packet49_m2:
 ldx #0
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
Packet49_m3:
 ldx #0
 stx.b GRP1
 sty.w RESP1
Packet49_m4:
 ldx #0
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 rts
Packet49End:
 IF Packet49End-Packet49 > 64
 ERR
 ENDIF
Packet49Offsets:
 byte Packet49_m0-Packet49+1,Packet49_m1-Packet49+1,Packet49_m2-Packet49+1,Packet49_m3-Packet49+1,Packet49_m4-Packet49+1
Packet50:
 sta WSYNC
 iny
 lda PlayerRows,y
 sta.w GRP0
Packet50_m0:
 lda #0
 sta.b GRP1
 lda #0
 nop
 sty.b RESP1
 sta.w ENAM0
Packet50_m1:
 lda #0
 sty.b RESP1
 ldx #14
 sta.b GRP1
Packet50_m2:
 lda #0
 sta.b GRP0
 stx.w COLUP0
Packet50_m3:
 ldx #0
 sty.b RESP1
 stx.b GRP1
Packet50_m4:
 lda #0
 sty.b RESP1
 sta.b GRP1
 ldx #30
 stx.b COLUP0
 stx.b ENAM0
 nop
 rts
Packet50End:
 IF Packet50End-Packet50 > 64
 ERR
 ENDIF
Packet50Offsets:
 byte Packet50_m0-Packet50+1,Packet50_m1-Packet50+1,Packet50_m2-Packet50+1,Packet50_m3-Packet50+1,Packet50_m4-Packet50+1
PacketLo:
 byte <Packet48,<Packet49,<Packet50
PacketHi:
 byte >Packet48,>Packet49,>Packet50
PacketSize:
 byte Packet48End-Packet48,Packet49End-Packet49,Packet50End-Packet50
PacketPatchLo:
 byte <Packet48Offsets,<Packet49Offsets,<Packet50Offsets
PacketPatchHi:
 byte >Packet48Offsets,>Packet49Offsets,>Packet50Offsets
