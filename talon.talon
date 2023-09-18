mode: all
os: mac
-
# Mac only; sleep talon and computer
^talon goodnight [<phrase>]$:
    speech.disable()
    key(cmd-ctrl-q)
