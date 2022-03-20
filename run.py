import os
import re
from subprocess import PIPE, Popen
def ddt(S, n, m):
	D = [[0] * (2 ** m) for _ in range(2 ** n)]
	for alpha in range(2 ** n):
		for x in range(2 ** n):
			beta = S[x] ^ S[x ^ alpha]
			D[alpha][beta] += 1
	return D

def print_ddt_to_file(fname, S, n, m):
      D = ddt(S, n, m)
      ddt_text_file = open(fname, "w")
      first_row = '|'.rjust(4)
      for i in range(2 ** m):
            first_row += str(hex(i))[2:].rjust(4)
      print(first_row, file = ddt_text_file)
      horiziontal_divider = '-' * len(first_row)
      print(horiziontal_divider, file = ddt_text_file)
      for alpha in range(2 ** n):
            row_string = ''
            row_string += str(hex(alpha))[2:].rjust(3) + '| '
            for beta in range (2 ** m):
                  d = D[alpha][beta]
                  row_string += str(d).rjust(3) + ' '
            print(row_string, file = ddt_text_file)
      ddt_text_file.close()
first_num_inputs = 2
R1 = []
R2 = []
fotmat_input = '{i:0%dx}' % (first_num_inputs)

bits = [fotmat_input.format(i=i) for i in range(1 << (4 * first_num_inputs))]
print(bits)
for b in bits:
    print(b)
    for i in range(2):
        planText = b + ('0' * (16 - first_num_inputs))
        if i == 0:
            proc = Popen(f"java blowfish_addP {planText} 0000000000000000".split(' '), stdout=PIPE, shell=False)
        else:
            proc = Popen(f"java blowfish_twokey {planText} 0000000000000000".split(' '), stdout=PIPE, shell=False)
        (out, err) = proc.communicate()
        cipher = re.findall(r'Cipher Text: (.*)', str(out))[0][:16]
        print(cipher)
        if i == 0:
            R1.append(int(cipher[:first_num_inputs], base=16))
        else:
            R2.append(int(cipher[:first_num_inputs], base=16))
n = (4 << (first_num_inputs - 1))
print_ddt_to_file(f'ddt_addP_{first_num_inputs}_.txt', R1, n, n)
print_ddt_to_file(f'ddt_towkey_{first_num_inputs}_.txt', R2, n, n)
print_ddt_to_file('ddt_addP.txt', R1, 8, 8)
print_ddt_to_file('ddt_towkey.txt', R2, 8, 8)

# print(r)