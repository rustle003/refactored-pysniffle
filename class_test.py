from typing import Callable

class A:
    def __init__(self: 'A', inst_attr: int) -> None:
        self.inst_attr: int = inst_attr
        self.board: list[list[int]]
        self.other_attr: str = "Hello"
        # print(self.B().inst_attr2)
   
    class B:
        def __init__(self: 'A.B', inst_attr2: int = 32) -> None:
            self.inst_attr2: int = inst_attr2
            A.call_from_class_b(self, 33)
        
        def check_new_attr(self: 'A.B') -> int:
            return self.new_attr
        
        def call_from_class_a(self: 'A', new_attr: int) -> None:
            self.new_attr = new_attr

    def call_from_class_b(self: 'A.B', new_attr: int) -> None:
        self.new_attr: int = new_attr

class C(A):
    def __init__(self: 'C') -> None:
        self.inst_attrc = 20
    
    def apply(self: 'C', inst_attrc: int) -> Callable[[int],None]:
        self.inst_attrc = inst_attrc
        return super().__init__
    
    def print_attributeC(self: 'C') -> None:
        print(f"{self.inst_attrc} belongs to C; {self.inst_attr} belongs to A")

my_c = C()
# my_c.apply(53)(44)
my_c.call_from_class_b(4)
print(my_c.new_attr)