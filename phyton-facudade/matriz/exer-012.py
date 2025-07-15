#Fazer um programa para ler 5 valores e, em seguida, mostrar todos os valores lidos
#juntamente com o maior, o menor e a media dos valores.

valor=[1, 8, 9, 10, 1000]
maior=valor[0]
menor=valor[0]

for num in (valor):
    if num > maior:
        maior=num

    if num < menor:
        menor=num

    media=sum(valor) / len (valor)

print(f"Menor valor e {menor}")
print(f"O maior valor e {maior}")
print(f"A media e de {media}")

