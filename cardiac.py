"""
	Cardiac computer
	https://www.cs.drexel.edu/~bls96/museum/cardiac.html


Cardiac Computer Instruction Set:
Opcode	Mnemonic	Operation
0		INP			Read a card into memory
1		CLA			Clear accumulator and add from memory (load)
2		ADD			Add from memory to accumulator
3		TAC			Test accumulator and jump if negative
4		SFT			Shift accumulator
5		OUT			Write memory location to output card
6		STO			Store accumulator to memory
7		SUB			Subtract memory from accumulator
8		JMP			Jump and save PC
9		HRS			Halt and reset



"""
import sys 

ram_size = 32
ram = []
A = 0
PC = 0 

def init_ram():
	for i in range(ram_size):
		ram.append(0)

def load_program(progfile):
	with open(progfile, "r") as f:
		code = f.readlines()
	if len(code) >= ram_size:
		print "Program too large"
		exit()
	for i in range(0,len(code)):
		ram[i] = int(code[i])
	print ram

def run():
	while PC < (len(ram)):
		instr = ram[PC]
		opcode = (instr/100)%10
		operand = instr%100
		if operand > ram_size:
			print "invalid address...Exiting"
			sys.exit(-1)
		execute(opcode,operand)
		

def execute(opcode, operand):
	global A
	global PC
	if opcode == 0x0:
		#print "INP" 
		while 1:
			_input = sys.stdin.readline().strip() 
			try:
				ram[operand] = int(_input)
			except:
				print "invalid input..Try again\n"
				continue
			else:
				break
	elif opcode == 0x1:
		#print "CLA",operand
		A = ram[operand]
	elif opcode == 0x2:
		#print "ADD",operand
		A = A + ram[operand]
	elif opcode == 0x3:
		#print "TAC"
		if A<0:
			PC = operand
			return  
	elif opcode == 0x4:
 		#print"SFT"
		A = A >> 1
	elif opcode == 0x5:
		#print "OUT",
		print ram[operand] 
	elif opcode == 0x6:
		#print "STO"
		ram[operand]=A
   	elif opcode == 0x7:
		#print "SUB",operand
		A = A - ram[operand]
   	elif opcode == 0x8:
		#print "JMP" 
		PC = operand
		return
	elif opcode == 0x9:
		#print "HLT"
		sys.exit(0)
	else:
		print "Invalid Opcode...Exiting"
		sys.exit(-1)
	PC = PC + 1

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "No file given to execute"
		sys.exit(-1)
	init_ram()
	load_program(sys.argv[1])
	run()
