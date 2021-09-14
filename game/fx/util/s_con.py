class _SCon:
    esc     : str = '\u001B'
    bra     : str = '['
    eb      : str = esc + bra
    bRed    : str = eb + '41m'
    white   : str = eb + '47m'
    bold    : str = eb + '1m'
    right   : str = 'C'
    left    : str = 'D'
    down    : str = 'B'
    up      : str = 'A'

    
    def caretTo(self, x: int, y: int) -> None: print(self.eb + y + ";" + x + "H", end = "")
    def caretSave(self)               -> None: print(self.eb + "s", end = "")
    def caretRestore(self)            -> None: print(self.eb + "u", end = "")
    def delLine(self)                 -> None: print(self.eb + 2 + "K", end ="")

SCon: _SCon = _SCon()