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
                self.ram[self.pc] = int(x[0:8], 2)
                self.pc += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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
        IR = self.ram[self.pc]
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        HRT = 1
        LDI = 82
        PRN = 47

        while True:
            if IR == HRT:
                break
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
                IR = self.ram[self.pc]
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
                IR = self.ram[self.pc]
            self.pc += 1
            IR = self.ram[self.pc]
