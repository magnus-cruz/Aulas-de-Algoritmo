# Sistema de Compras - Posto de Gasolina

total_geral = 0
contador_compras = 0

print("=" * 50)
print("BEM-VINDO AO POSTO DE GASOLINA")
print("=" * 50)

while True:
    print("\n--- Nova Compra ---")
    
    # Menu de produtos
    print("\nProdutos disponíveis:")
    print("1 - Gasolina Comum (R$ 5.50/litro)")
    print("2 - Gasolina Aditivada (R$ 6.20/litro)")
    print("3 - Etanol (R$ 4.30/litro)")
    print("4 - Diesel (R$ 5.80/litro)")
    print("5 - Loja de Conveniência")
    print("0 - Finalizar e pagar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == "0":
        break
    
    if opcao in ["1", "2", "3", "4"]:
        # Abastecimento
        litros = float(input("Quantos litros deseja abastecer? "))
        
        if opcao == "1":
            preco = 5.50
            produto = "Gasolina Comum"
        elif opcao == "2":
            preco = 6.20
            produto = "Gasolina Aditivada"
        elif opcao == "3":
            preco = 4.30
            produto = "Etanol"
        else:
            preco = 5.80
            produto = "Diesel"
        
        valor_compra = litros * preco
        print(f"\n{produto}: {litros}L x R$ {preco:.2f} = R$ {valor_compra:.2f}")
        
    elif opcao == "5":
        # Loja de conveniência
        print("\n--- Loja de Conveniência ---")
        produto = input("Nome do produto: ")
        valor_compra = float(input("Valor do produto: R$ "))
        print(f"\n{produto}: R$ {valor_compra:.2f}")
        
    else:
        print("\nOpção inválida! Tente novamente.")
        continue
    
    total_geral += valor_compra
    contador_compras += 1
    print(f"Subtotal até agora: R$ {total_geral:.2f}")

# Resumo final
print("\n" + "=" * 50)
print("RESUMO DA COMPRA")
print("=" * 50)
print(f"Total de itens comprados: {contador_compras}")
print(f"Valor total: R$ {total_geral:.2f}")
print("\nObrigado por escolher nosso posto!")
print("Volte sempre!")
print("=" * 50)
