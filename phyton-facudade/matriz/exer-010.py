#Fac¸a um programa para ler a nota da prova de 15 alunos e armazene num vetor, calcule
#e imprima a media geral. 

vetor = []


for i in range(5):
    nota = float(input(f"Nota do aluno {i+1}: "))
    vetor.append(nota)


media = sum(vetor) / len(vetor)


print(f"\nA média geral da turma é: {media:.2f}")


