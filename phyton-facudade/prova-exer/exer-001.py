#numero

def numero (n):

    if n > 0:
        return("numero positivo")
    
    elif n < 0:
        return("numero negativo")
    
    else:
        return("numero igual a zero")
    
n=int(input("Digite um numero: "))

resutado=numero(n)

print(resutado)