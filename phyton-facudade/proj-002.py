#lista de mercado

def adicionar(lista):
    produto = input("Nome do produto: ")
    valor = input("Número valor (apenas numeros): ")
    quantidade= input("Quantidade em estoque: ")
    lista.append([produto, valor, quantidade])
    print("Produto adicionado com  sucesso!")

def listar(lista):
    if not lista:
        print("--->Produto nao encontrado<---")
    else:
        print("--->produtos encontrados<---")
        for i, itens in enumerate(lista):
            print(f"{i+1}. produto= {itens[0]},  R$:{itens[1]}, Quantidade:{itens[2]}")
        print()

def buscar (lista):
    nomebusca= input("Nome para a busca: ")
    econtrado=False
    for itens in lista:
        if itens[0].lower() == nomebusca.lower():
            print("--->Contato encontrado<---")
            print(f"produto= {itens[0]}, R$:{itens[1]}, quantidade={itens[2]}")
            econtrado=True
    if not econtrado:
        print("--->Contato nao econtrado<---")
        


def menu():
    print("=" * 25)
    print("Menu")
    print("""
1 - Adicionar produtos
2 - Listar produtos
3 - Buscar por produto
4 - Sair
""")
    print("=" * 25)

# Programa principal
lista = []
fim = True

while fim:
    menu()
    try:
        operador = int(input("Operador: "))
    except ValueError:
        print("Por favor, digite um número válido.\n")
        continue

    if operador == 1:
        adicionar(lista)
    elif operador == 2:
        listar(lista)
    elif operador == 3:
        buscar(lista)
    elif operador == 4:
        print("----> Programa encerrado <----")
        fim = False
    else:
        print("Opção inválida. Tente novamente.\n")
