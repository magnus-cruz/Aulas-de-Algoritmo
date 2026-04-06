#Programa: Analisador de entrada do teclado
#Descrição:
"""
- Lê um valor digitado pelo usuário
- Mostra o tipo do dado recebido
- Exibe várias informações possíveis sobre o conteúdo informado
- Apresenta transformações úteis do valor
"""
#autor:Luís fernando
VALOR = input("Digite algo: ")

print("\n--- Análise da entrada ---")
print(f"Valor digitado: {VALOR}")
print(f"Tipo do dado: {type(VALOR)}")

print("\n--- Informações possíveis ---")
print(f"Só tem espaços? {VALOR.isspace()}")
print(f"É numérico? {VALOR.isnumeric()}")
print(f"É decimal? {VALOR.isdecimal()}")
print(f"É dígito? {VALOR.isdigit()}")
print(f"É alfabético? {VALOR.isalpha()}")
print(f"É alfanumérico? {VALOR.isalnum()}")
print(f"Está em maiúsculas? {VALOR.isupper()}")
print(f"Está em minúsculas? {VALOR.islower()}")
print(f"Está capitalizado? {VALOR.istitle()}")
print(f"Quantidade de caracteres: {len(VALOR)}")

print("\n--- Transformações úteis ---")
print(f"Maiúsculas: {VALOR.upper()}")
print(f"Minúsculas: {VALOR.lower()}")
print(f"Sem espaços nas pontas: {VALOR.strip()}")
