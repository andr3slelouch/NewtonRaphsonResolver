import math
funciones_permitidas = {

    k: v for k, v in math.__dict__.items() if not k.startswith("__")

}

bienvenida = f"""

Ingrese un valor para una función matemática válida después de ">"

Escriba "ayuda" para más información


"""


uso = f"""

Escriba cualquiera de las siguientes funciones y constantes en x,y y z.

{', '.join(funciones_permitidas.keys())}

"""

def evaluate(expression, x):
    #Obtenido de :https://realpython.com/python-eval-function/
    """Esta función permite evaluary retornar un valor de la funcion ingresada por el usuario
        args:

            expression(str): La función ingresada por el usuario
            x(numpy.array): El array con los valores iniciales
        returns:

            (float): El resultado de la funcion para los valores de x"""

    # Compile the expression

    code = compile(expression, "<string>", "eval")

    funciones_permitidas['x'] = x[0]
    funciones_permitidas['X'] = x[0]
    if (len(x)>1):
        funciones_permitidas['y'] = x[1]
        funciones_permitidas['Y'] = x[1]
        if(len(x)>2):
            funciones_permitidas['z'] = x[2]
            funciones_permitidas['Z'] = x[2]
    # Validate allowed names

    for name in code.co_names:

        if name not in funciones_permitidas:

            raise NameError(f"The use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {}}, funciones_permitidas)
