from __future__ import annotations
from operator import add, mul, lt, eq
from collections import defaultdict, deque
from typing import List, Dict

WAITING_FOR_INPUT = object()
BEGIN_LOOP = object()

class Intcode:

    def __init__(self, state: List[int]):
        self.memory: Dict[int, int] = defaultdict(int)
        self.memory.update(enumerate(state))
        self.pointer_position = 0
        self.relative_base = 0
        self._program = self._run_program()
        assert next(self._program) == BEGIN_LOOP

    def clone(self) -> Intcode:
        clone = type(self)([self.memory[idx] for idx in range(max(self.memory)+1)])
        return clone

    def get_value(self, pntr:int , mode: int) -> int:
        if mode == 0:
            ret = self.memory[pntr]
        if mode == 1:
            ret = pntr
        if mode == 2:
            ret = self.memory[pntr+self.relative_base]
        return ret

    def _run_program(self):
        two_param_operations = {
            1: add,
            2: mul,
            7: lt,
            8: eq,
        }
        op_params = (0, 3, 3, 1, 1, 2, 2, 3, 3, 1)
        yield BEGIN_LOOP
        while self.memory[self.pointer_position] != 99:
            opcode = f'{self.memory[self.pointer_position]:05d}'
            op = int(opcode[-2:])
            modes = [int(c) for c in opcode[:-2]][::-1]
            param_count = op_params[op]
            storage_position = self.memory[self.pointer_position+param_count] if modes[param_count-1] == 0 else self.memory[self.pointer_position+param_count] + self.relative_base
            # Advance the pointer by 1 so we can start processing parameters.
            self.pointer_position += 1
            parameters = [self.get_value(self.memory[idx], mode) for idx, mode in zip(range(self.pointer_position, self.pointer_position+param_count), modes)]
            if op in (1, 2, 7, 8): # 2 parameters
                self.memory[storage_position] = int(two_param_operations[op](parameters[0], parameters[1]))
            elif op == 3: # input
                self.memory[storage_position] = yield WAITING_FOR_INPUT
            elif op == 4: # output
                yield parameters[0]
            elif op == 9: # update offset
                self.relative_base += parameters[0]
            elif (op == 5 and parameters[0]) or (op == 6 and not parameters[0]): # Jumps
                self.pointer_position = parameters[1]
                continue # We want to avoid incrementing the pointer position because we did a jump
            self.pointer_position += param_count # Advance pointer to next opcode
        return self.memory[0]

    def __next__(self):
        return next(self._program)

    def __iter__(self):
        return self._program

    def send(self, val):
        return self._program.send(val)

    def send_multiple(self, *vals):
        for v in vals:
            if (x := self.send(v)) != WAITING_FOR_INPUT:
                return x

    def throw(self, exc, value=None, traceback=None):
        return self._program.throw(exc, value, traceback)

    def run_until_input(self, val=None) -> List[int]:
        ret = []
        try:
            while (v := self.send(val)) != WAITING_FOR_INPUT:
                ret.append(v)
        except StopIteration as e:
            if not ret:
                return [e.value]
        return ret

    def send_ascii(self, cmd_string):
        v = self.send_multiple(*[ord(c) for c in cmd_string])
        return self.run_until_input(ord('\n'))
