"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, file):
        """Load a program into memory."""
        with open(file) as f:
            for x in f:
                if x[0] != '#':
                    self.ram[self.pc] = int(x[0:8], 2)
                    self.pc += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.pc = 0
        self.reg[7] = 0xf4
        IR = self.ram[self.pc]
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        while True:
            if IR == HLT:
                break
            elif IR == LDI:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.reg[operand_a] = operand_b
                self.pc += 3
                IR = self.ram[self.pc]
            elif IR == PRN:
                operand_a = self.ram[self.pc + 1]
                print(self.ram, self.reg)
                print(self.reg[operand_a])
                self.pc += 2
                IR = self.ram[self.pc]
            elif IR == MUL:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
                IR = self.ram[self.pc]
            elif IR == ADD:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3
                IR = self.ram[self.pc]
            elif IR == PUSH:
                operand_a = self.reg[self.ram[self.pc + 1]]
                self.reg[7] -= 1
                self.ram[self.reg[7]] = operand_a
                self.pc += 2
                IR = self.ram[self.pc]
            elif IR == POP:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.reg[7]]
                self.reg[7] += 1
                self.pc += 2
                IR = self.ram[self.pc]
            elif IR == CALL:
                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.pc + 2
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[reg]
                IR = self.ram[self.pc]
            elif IR == RET:
                self.pc = self.ram[self.reg[7]]
                self.reg[7] += 1
                IR = self.ram[self.pc]
            else:
                print("Unknown instruction")
                sys.exit(1)
