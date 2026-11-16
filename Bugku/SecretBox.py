from openpyxl import load_workbook

data = load_workbook('SecretBox.xlsx')['Weights']
weights = [[[data.cell(n * 11 + row + 2, col).value for col in range(1, 9)] for row in range(10)] for n in range(18)]
sumpro = lambda x, y: sum(i * j for i, j in zip(x, y))

def check(weight):
    for char in range(32, 127):
        s = ((char + 18) % 128) ^ 33
        s = [(s >> i) & 1 for i in range(7, -1, -1)]
        s = [sumpro(s, weight[i]) + weight[8][i] for i in range(8)]
        s = sumpro(s, weight[9])
        if s == 1:
            return char

res = bytes(check(weight) for weight in weights).decode()
print(f'flag{{{res[-6:] + res[:-6]}}}') # flag{F1n3_y0U_g0t_31946}