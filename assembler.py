"""
	This is an assembler for the Cardiac Computer 

	Syntax:
		<Label> <DATA> instruction/literal
		instruction : opcode+addr
	Eg:
		A DATA 444
		B DATA 555
			LDA A
			ADD B
			OUT
		L1	LDA 
			SUB 34
			JMP L1 
			HLT

	Breakdown of the two passes
		 1. run through the code and count the number of instuction
			this count becomes the offset for all the symbol addresses.
			which means that all the literals that the symbols point to
			are kept at addresses after this count.
		
		 2.	In this pass we  populate the symbol table and addr-
			-ess table
				Eg:
				addr = count + instr_count + 1
				data_table["A"] = addr
				address_table[addr] = symbol_val
				sym_count++
		    And also decode instruction
		  		first the opcode 
					op = opcode_table[field[0]]
				then the symbol/literal
				if digit(field[1])
					addr = field[1]
				else
					addr = data_table[field[1]]	  						
				then join both
				instr = op*100 + addr

		 3.	after all instructions are done, dump the address_table contents at the end

		Instruction Set:
0       INP         Read a card into memory
1       CLA         Clear accumulator and add from memory (load)
2       ADD         Add from memory to accumulator
3       TAC         Test accumulator and jump if negative
4       SFT         Shift accumulator
5       OUT         Write memory location to output card
6       STO         Store accumulator to memory
7       SUB         Subtract memory from accumulator
8       JMP         Jump and save PC
9       HRS         Halt and reset
"""
import sys

opcode_table = {"INP":'0',
				"CLA":'1',
				"ADD":'2',
				"TAC":'3',
				"SFT":'4',
				"OUT":'5',
				"STO":'6',
				"SUB":'7', 
				"JMP":'8', 
				"HRS":'9'}
 
data_table = {} # data symbol:address
symbol_table = {} # symbol:address
address_table ={} # address:value
instruction_count = 0
data_count = 0
symbol_count = 0

with open("code.sap","r") as f:
	lines= f.readlines()

#collect all symbols
for i,line in enumerate(lines):
	if "DATA" in line:
		fields = line.split()
		if len(fields) == 3:
			symbol = fields[0]
			val    = fields[2]
			data_table[symbol] = data_count
			address_table[i] = val
			data_count += 1
		else:
			print "Error, Unrecognised Data definition, Line:",i
	else:
		if line.strip():
			fields = line.split()
			if len(fields) == 3:
				label = fields[0]
				#have to check for symbol before inserting
				symbol_table[label]= str(instruction_count)

			instruction_count += 1

for i in data_table:
	data_table[i]=  str(data_table[i]+instruction_count)


#assemble
for i ,line in enumerate(lines[data_count:]):
	if not line.strip():
		continue #empty line
	fields 	= line.split()
	opcode 	= None
	addr 	= None
  	if len(fields) == 3:
		opcode 	= fields[1]
		addr 	= fields[2]
	elif len(fields) == 2:
		opcode 	= fields[0]
		addr 	= fields[1]
	else:
		print "Error, Unrecognised Instruction, Line:",i	      


	if not addr.isdigit():
		if addr in data_table.keys():
			addr = data_table[addr]
		elif addr in symbol_table.keys():	
			addr = symbol_table[addr]		
		else:
			print "Error, Undefined symbol: ",addr
			sys.exit(-1)
	
	if int(addr) < 10:
		addr = '0' + str(int(addr)%10)
		
	opcode = opcode_table[opcode]
	print opcode+addr
				

#output the data definitions
for addr in address_table:
	print address_table[addr]


