InstallKeyAssist:
 tax
 dex
 lda #156
 sta SplitY
 lda #0
 sta AssistID
 jsr InstallAssist
 jmp CompensateAssistX
