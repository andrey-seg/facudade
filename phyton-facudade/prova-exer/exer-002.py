#maior

def maior (a,b):

    if a > b:
        return (f"{a} e maior que {b}")
    
    else:
        return (f"{b} e maior que {a}")
    
a=int(input("Digite um numero: "))
b=int(input("Digite outro numero: "))

resultado=maior(a,b)

print(resultado)