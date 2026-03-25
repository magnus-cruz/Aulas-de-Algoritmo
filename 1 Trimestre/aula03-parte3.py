# Use o pacote random para sortear um número inteiro entre 1 e 10.
# Imprima o número sorteado.
import random

num = random.randint(1, 10)
print(f"O número sorteado foi: {num}")

# Crie um programa que sorteie 4 nomes de alunos e imprima os nomes sorteados.
nomes = input("Digite quatro nomes de alunos separados por vírgula: ")
lista_nomes = [nome.strip() for nome in nomes.split(",") if nome.strip()]

sorteados = random.sample(lista_nomes, 4)
print("Os nomes sorteados foram:")
for nome in sorteados:
    print(nome)

# Dados os quatro nomes, mostre a lista de nomes em ordem sorteada.
random.shuffle(lista_nomes)
print("Os nomes em ordem sorteada foram:")
for nome in lista_nomes:
    print(nome)