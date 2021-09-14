class _Outcome:
    def __init__(self, state: bool) -> None:
        self.state = state
    
    def getState(self) -> bool:
        return self.state

class Outcome(_Outcome):
    def __init__(self, state: bool) -> None:
        _Outcome.__init__(self,state)
    
    FAILURE: _Outcome = _Outcome(False)
    SUCCESS: _Outcome = _Outcome(True)