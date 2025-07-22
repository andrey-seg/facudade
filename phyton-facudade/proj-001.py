def adicionar(lista):
    print("Apenas letras")
    nome = input("Nome: ")
    print("Apenas números")
    numero = input("Número: ")
    lista.append([nome, numero])
    print("Contato adicionado com sucesso!")

def listar(lista):
    if not lista:
        print("Contato nao encontrado")
    else:
        print("--->Contatos encontrados<---")
        for i, contato in enumerate(lista):
            print(f"{i+1}. nome= {contato[0]}, numero= {contato[1]}")
        print()

def buscar (lista):
    nomebusca= input("Nome para a busca: ")
    econtrado=False
    for contato in lista:
        if contato[0].lower() == nomebusca.lower():
            print("--->Contato encontrado<---")
            print(f"Nome: {contato[0]}, Numero: {contato[1]}")
            econtrado=True
    if not econtrado:
        print("--->Contato nao econtrado<---")
        


def menu():
    print("=" * 25)
    print("Menu")
    print("""
1 - Adicionar contato
2 - Listar contatos
3 - Buscar por nome
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
