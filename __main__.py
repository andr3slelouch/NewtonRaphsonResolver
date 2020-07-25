import numpy as np
import math
from sympy import symbols, sympify, diff
from newtonRaphson import newtonRaphson
from evaluate import evaluate, uso
from error import err
funciones = []
funciones_derivadas = np.array(funciones)

def f(x):
    '''La función original del libro, que evalua las funciones para los valores de x.

        args:

            x(numpy.array): Array con los valores iniciales
        
        returns:

            f(numpy.array): Array con los valores evaluados para el valor actual de x.
    '''
    tamano = len(x)
    f = np.zeros(tamano)

    for i in range(tamano):
        f[i] = evaluate(funciones[i],x)
    return f

def dx(x):
    '''La función original del libro, que evalua las funciones para los valores de x.

        args:

            x(numpy.array): Array con los valores iniciales
        
        returns:

            f(numpy.array): Array con los valores evaluados para el valor actual de x.
    '''
    sistema = len(x)
    dx = np.zeros(sistema)

    temp_list = []
    if sistema == 3:
        for i in range(sistema):
            derivada_x = evaluate(funciones_derivadas[i][0],x)
            derivada_y = evaluate(funciones_derivadas[i][1],x)
            derivada_z = evaluate(funciones_derivadas[i][2],x)
            temp_list.append([derivada_x, derivada_y, derivada_z])
    elif sistema == 2:
        for i in range(sistema):
            derivada_x = evaluate(funciones_derivadas[i][0],x)
            derivada_y = evaluate(funciones_derivadas[i][1],x)
            temp_list.append([derivada_x, derivada_y])
    elif sistema == 1:
        for i in range(sistema):
            derivada_x = evaluate(funciones_derivadas[i][0],x)
            temp_list.append([derivada_x])
    dx = np.array(temp_list)
    return dx

def definir_funciones(x):
    '''En esta función se ingresarán todas las funciones por teclado y se guardarán en una 
    en una variable global para que pueda ser accedida desde la función f(x)

        args:
            x(numpy.array): El array con los valores iniciales de la función. 
    '''
    print("Ingrese la palabra ayuda para ver las funciones matemáticas disponibles.")
    print("No olvide que las operaciones deben ser explícitas, no obvie ningun *,/, etc")
    tamano = len(x)
    for i in range(len(funciones),tamano):
        funciones.append(ingresar_funcion())
    derivar_funciones(x)

def ingresar_funcion():
    '''Dentro de esta función se realiza el ingreso de una función por parte del usuario, 
    además se comprueba que este dentro de x,y y z.

        returns:
            funcion(str): La función ingresada por el usuario.
    '''
    message = "Ingrese la función en términos de x,y,z > "
    funcion = input(message)
    
    while(funcion == 'ayuda'):
        print(uso)
        funcion = input(message)
    return funcion.lower()


def derivar_funciones(x):
    '''En esta función se realizará la derivada para obtener el jacobiano de las funciones ingresadas
    '''
    sistema = len(x)
    variables = [symbols('x'),symbols('y'),symbols('z')]
    global funciones_derivadas
    temp_list = []
    temp_fun = ''
    if sistema == 3:
        for i in range(sistema):
            temp_fun = sympify(funciones[i])
            derivada_x = str(diff(temp_fun,variables[0]))
            derivada_y = str(diff(temp_fun,variables[1]))
            derivada_z = str(diff(temp_fun,variables[2]))
            temp_list.append([derivada_x, derivada_y, derivada_z])
        funciones_derivadas = np.array(temp_list)
    elif sistema == 2:
        for i in range(sistema):
            temp_fun = sympify(funciones[i])
            derivada_x = str(diff(temp_fun,variables[0]))
            derivada_y = str(diff(temp_fun,variables[1]))
            temp_list.append([derivada_x, derivada_y])
        funciones_derivadas = np.array(temp_list)
    elif sistema == 1:
        for i in range(sistema):
            temp_fun = sympify(funciones[i])
            derivada_x = str(diff(temp_fun,variables[0]))
            temp_list.append([derivada_x])
        funciones_derivadas = np.array(temp_list)



def generateInitialArray():
    ''' Dentro de esta función se hace el conteo de las variables ingresadas, si existe solo x tendrá
    un valor de 1, si existe x e y será dos y si existe x,y,z será 3.
    Entonces se retorna un numpy.array del tamaño indicado ademas de preguntar al usuario si desea 
    ingresar los valores iniciales de dicho array.
        
        args:
            funcion(str): La función a ser evaluada
        
        returns:
            x(numpy.array): Array con los valores iniciales

    '''
    msg_dimensiones = "Ingrese el sistema en el que se trabajara(x,xy o xyz) > "
    dimensiones = input(msg_dimensiones)
    vars = 0
    while (vars==0):
        if("x" in dimensiones):
            vars=1
        if("y" in dimensiones):
            vars=2
        if("z" in dimensiones):
            vars=3
        if (vars==0):
            msg_dimensiones = "Error, Ingrese el sistema en el que se trabajara(x,xy o xyz) > "
            dimensiones = input(msg_dimensiones)
    
    definir_valores = input('¿Desea definir los valores iniciales? (s/n)> ')
    #Verificar si el usuario ingreso un valor diferente a S o N.
    
    while(not(definir_valores.lower() == "s" or definir_valores.lower() == "n")):
        definir_valores = input('Error ¿Desea definir los valores iniciales? (s/n)> ')
    
    if(definir_valores.lower() == "s"):
        x = np.zeros(vars)
        for i in range(vars):
            try:
                message = "Ingrese el valor para la posición "+ str(i+1)+ "> "
                x[i] = float(input(message))
            except Exception as e:
                print(e,"ERROR debe ingresar valores numéricos")
        return x
    elif(definir_valores.lower() == "n"):
        raw_list = []
        for i in range(vars):
            raw_list.append(1.0)
        x = np.array(raw_list)
        return x
    else:
        raise("Valor ingresado inválido")

def ingresar_iteraciones():
    '''En esta función se ingresarán las iteraciones que se desea como máximo antes de detectar
    si diverge o no

        returns:
            iteraciones(int): El número de iteraciones.
    '''

    iteraciones = input('Ingrese el numero de iteraciones > ')
    while(not iteraciones.isdigit()):
        iteraciones = input('Error, Ingrese el numero de iteraciones> ')
    
    iteraciones = int(iteraciones)
    return iteraciones

def main():
    iteraciones = ingresar_iteraciones()
    x = generateInitialArray()
    definir_funciones(x)
    (converged, error, solution, iterations) = newtonRaphson(
        f,
        dx,
        x,
        tol=1.0e-4,
        maxiter=iteraciones,
        verbose=False,)
    if converged:
        print("La solucion se encontro en la iteración ", iterations)
        print("La solución encontrada es: ")
        print(solution)
        #print(solution, iteration)
    else:
        print("Se han realizado ",iterations," iteraciones, El sistema no converge")
    input("\nPress return to exit")

if __name__ == "__main__":
    main()