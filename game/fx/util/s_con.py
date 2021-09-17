class _SCon:
    esc     : str = '\u001B'
    bra     : str = '['
    eb      : str = esc + bra
    bRed    : str = eb + '41m'
    white   : str = eb + '37m'
    bold    : str = eb + '1m'
    right   : str = 'C'
    left    : str = 'D'
    down    : str = 'B'
    up      : str = 'A'
    reset   : str = eb + '0m'
    cyan    : str = eb + '36m'
    del_char: str = eb + 'X'
    save    : str = eb + 's'
    restore : str = eb + 'u'
    
    def caret_to(self, x: int, y: int) -> None: print(self.eb + f"{y};{x}H", end = "")
    def caret_save(self)               -> None: print(self.save, end = "")
    def caret_restore(self)            -> None: print(self.restore, end = "")
    def del_line(self)                 -> None: print(self.eb + "2K", end ="")
    def reset_screen_and_caret(self)   -> None: print(self.eb + "2J" + self.eb + "0;0H", end = "")
    def caret_x_pos(self, x: int)      -> None: print(self.eb + f"{x}G", end = "")
    def caret_y_pos(self, y: int)      -> None: print(self.eb + f"{y}d", end = "")

SCON: _SCon = _SCon()