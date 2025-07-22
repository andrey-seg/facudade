# Função para ler nomes e notas dos alunos
def lerdados():
    alunos = []
    notas = []

    q = int(input("Quantos alunos você deseja cadastrar? "))

    for i in range(q):
        estudante = input(f"Nome do aluno {i+1}: ")
        alunos.append(estudante)

        notasalunos = []
        for j in range(3):
            nota = float(input(f"Digite a nota {j+1} do {estudante}: "))
            notasalunos.append(nota)

        notas.append(notasalunos)

    return alunos, notas

# Função para calcular as médias dos alunos
def calcularmedia(notas):
    medias = []
    for notasalunos in notas:
        media = sum(notasalunos) / 3
        medias.append(media)
    return medias

# Função para determinar a situação com base na média
def determinar_situacao(media):
    if media >= 7:
        return "Aprovado"
    elif media == 5:
        return "Exame"
    else:
        return "Reprovado"

# Função para mostrar todos os resultados
def mostrar_resultados(nomes, notas, medias):
    print("\nResultado final")
    print("=" * 50)
    for i in range(len(nomes)):
        situacao = determinar_situacao(medias[i])
        notas_formatadas = ", ".join([f"{n:.1f}" for n in notas[i]])
        print(f"Aluno: {nomes[i]}")
        print(f"Notas: {notas_formatadas}")
        print(f"Média: {medias[i]:.2f}")
        print(f"Situação: {situacao}")
        print("-" * 50)

# Programa principal
nomes, notas = lerdados()
medias = calcularmedia(notas)
mostrar_resultados(nomes, notas, medias)

