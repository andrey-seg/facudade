#Fac¸a um programa que leia um vetor de 5 posic¸oes para n ˜ umeros reais e, depois, um ´
#codigo inteiro. Se o c ´ odigo for zero, finalize o programa; se for 1, mostre o vetor na ordem ´
#direta; se for 2, mostre o vetor na ordem inversa. Caso, o codigo for diferente de 1 e 2 ´
#escreva uma mensagem informando que o codigo ´ e inv ´ alido. 

# Programa que lê um vetor de 5 posições e processa conforme código

def main():
    # Lendo o vetor de 5 posições
    vetor = []
    print("Digite 5 números reais:")
    
    for i in range(5):
        numero = float(input(f"Posição {i+1}: "))
        vetor.append(numero)
    
    # Loop principal do programa
    while True:
        print("\n" + "="*40)
        print("MENU DE OPÇÕES:")
        print("0 - Finalizar programa")
        print("1 - Mostrar vetor na ordem direta")
        print("2 - Mostrar vetor na ordem inversa")
        print("="*40)
        
        # Lendo o código
        try:
            codigo = int(input("Digite o código: "))
        except ValueError:
            print("ERRO: Digite apenas números inteiros!")
            continue
        
        # Processando o código
        if codigo == 0:
            print("Programa finalizado!")
            break
        elif codigo == 1:
            print("\nVetor na ordem direta:")
            for i, valor in enumerate(vetor):
                print(f"Posição {i+1}: {valor}")
        elif codigo == 2:
            print("\nVetor na ordem inversa:")
            for i, valor in enumerate(reversed(vetor)):
                print(f"Posição {5-i}: {valor}")
        else:
            print("CÓDIGO INVÁLIDO! Digite apenas 0, 1 ou 2.")

# Executando o programa
if __name__ == "__main__":
    main()