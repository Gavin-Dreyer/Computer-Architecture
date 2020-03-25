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
                #print(int(x[0:8], 2))
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
        IR = self.ram[self.pc]
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

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
                print(self.reg[operand_a])
                self.pc += 2
                IR = self.ram[self.pc]
            elif IR == MUL:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
                IR = self.ram[self.pc]
            else:
                print("Unknown instruction")
                sys.exit(1)
