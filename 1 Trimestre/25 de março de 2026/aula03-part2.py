import math
# Crie um programa que leia um numero
# inteiro
num = int(input('Digite um numero inteiro: '))
raiz = math.sqrt(num)
print('A raiz quadrada de {} é igual a {:.2f}'.format(num, raiz))
print('O numero {} arredondado para cima é {}'.format(num, math.ceil(num)))
print('O numero {} arredondado para baixo é {}'.format(num, math.floor(num)))
potencia = math.pow(num, 4)
print('O numero {} elevado a quarta potência é {}'.format(num, potencia))