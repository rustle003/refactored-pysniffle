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

    
    def caret_to(self, x: int, y: int) -> None: print(self.eb + y + ";" + x + "H", end = "")
    def caret_save(self)               -> None: print(self.eb + "s", end = "")
    def caret_restore(self)            -> None: print(self.eb + "u", end = "")
    def del_line(self)                 -> None: print(self.eb + 2 + "K", end ="")

SCON: _SCon = _SCon()