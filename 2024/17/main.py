"""
AOC 2024 -- day 17
part 1
"""

import sys
import math


# pylint: disable=global-statement, unused-argument, too-many-locals, broad-exception-caught


class Computer:
    """
    Computer
    """

    def __init__(self):
        self.instruction_pointer = 0
        self.output = []

        self.registers = {"A": 0, "B": 0, "C": 0}
        self.combo_ops = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3,
            4: lambda: self.registers["A"],
            5: lambda: self.registers["B"],
            6: lambda: self.registers["C"],
            7: lambda: None,
        }
        self.op_codes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def adv(self, operand: int):
        """
        The adv instruction (opcode 0) performs division. The numerator is the value
          in the A register. The denominator is found by raising 2 to the power of
          the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2);
          an operand of 5 would divide A by 2^B.) The result of the division operation
          is truncated to an integer and then written to the A register.
        """
        exponent = self.combo_ops[operand]()
        self.registers["A"] = math.floor(self.registers["A"] / (2**exponent))

    def bxl(self, operand: int):
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B
        and the instruction's literal operand, then stores the result in register B.
        """
        self.registers["B"] ^= operand

    def bst(self, operand: int):
        """
        The bst instruction (opcode 2) calculates the value of its combo operand
        modulo 8 (thereby keeping only its lowest 3 bits), then writes that value
        to the B register.
        """
        self.registers["B"] = operand % 8

    def jnz(self, operand):
        """
        The jnz instruction (opcode 3) does nothing if the A register is 0.
        However, if the A register is not zero, it jumps by setting the instruction
        pointer to the value of its literal operand; if this instruction jumps,
        the instruction pointer is not increased by 2 after this instruction.
        """
        if self.registers["A"] == 0:
            return
        self.instruction_pointer = operand - 1

    def bxc(self, operand):
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
        register C, then stores the result in register B. (For legacy reasons, this
        instruction reads an operand but ignores it.)
        """
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

    def out(self, operand):
        """
        The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
        then outputs that value. (If a program outputs multiple values, they are
        separated by commas.)
        """
        self.output.append(operand % 8)

    def bdv(self, operand):
        """
        The bdv instruction (opcode 6) works exactly like the adv instruction except that
        the result is stored in the B register. (The numerator is still read from the A register.)
        """
        exponent = self.combo_ops[operand]()
        self.registers["B"] = math.floor(self.registers["A"] / (2**exponent))

    def cdv(self, operand):
        """
        The cdv instruction (opcode 7) works exactly like the adv instruction except that the
        result is stored in the C register. (The numerator is still read from the A register.)
        """
        exponent = self.combo_ops[operand]()
        self.registers["C"] = math.floor(self.registers["A"] / int(2**exponent))

    def run(self, program, registers):
        """
        run
        param: program: List[Tuple[int,int]]
        param: registers: Dict[str, int]
        """
        print("program: ", program)
        self.registers.update(registers)
        print("registers: ", self.registers)

        while self.instruction_pointer < len(program):
            op = self.op_codes[program[self.instruction_pointer][0]]
            oprnd = (
                self.combo_ops[program[self.instruction_pointer][1]]()
                if program[self.instruction_pointer][1] < 7 and op.__name__ != "bxl"
                else program[self.instruction_pointer][1]
            )
            print(
                f"op/oprnd: {program[self.instruction_pointer]} -- {op.__name__}({oprnd})"
            )
            try:
                op(oprnd)
            except Exception as e:
                print(e)
                print("registers: ", self.registers)
                return ",".join([f"{o}" for o in self.output])

            print("registers: ", self.registers)
            self.instruction_pointer += 1

        return ",".join([f"{o}" for o in self.output])


def load_file(file_name=None):
    """
    load_file

    param: file_name: str OPTIONAL
    """
    if file_name is None:
        file_name = sys.argv[1]
    with open(file_name, "r", encoding="utf8") as fh:

        regs = {
            i.split(":")[0]
            .replace("Register", "")
            .strip(): [int(v) for v in i.split(":")[1].strip().split(",")]
            for i in fh.read().strip().split("\n")
            if i != ""
        }

    program_scripts = regs.pop("Program")
    regs = {k: v[0] for k, v in regs.items()}
    for reg in ["A", "B", "C"]:
        if reg not in regs:
            regs[reg] = 0

    program_scripts = [
        (program_scripts[i], program_scripts[i + 1])
        for i in range(0, len(program_scripts), 2)
    ]

    return program_scripts, regs


def main():
    """
    main
    """
    default_file_name = None
    # default_file_name = "input.txt"

    program_script, regstry = load_file(default_file_name)
    c = Computer()

    outputs = c.run(program_script, regstry)

    print("-------------------------------")
    print(outputs)


if __name__ == "__main__":
    main()
