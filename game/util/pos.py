class Pos:
    def __init__(self, x: int, y: int) -> None:
        self.x : int = x
        self.y : int = y
        self.xy: tuple[int,int] = (x,y)
    
    def unapply(self) -> tuple[int,int]:
        return self.xy
