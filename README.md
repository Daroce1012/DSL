# DSL
   Integrantes:
   .Belsai Arango C311
   .Carlos Carret C312
   .Daniela Roguez C311
   
# Dominio de aplicación del Dsl:
   Lenguaje de dominio específico creado con el objetivo de ayudar a detectar enfermedades. 

# Sintaxis del lenguaje:
   El lenguaje fue inspirado en python y c# por lo que presenta una sintaxis similar al de ellos. Los tipos definidos fueron str, int , bool y patient. Este permite la definición de funciones con el objetivo de extender la cantidad de enfermedades a detectar. Permite la ejecución de operaciones aritméticas y operaciones lógicas.  

# Características de la gramática:
 Palabras Claves:
            Patient,name, sex, age, add, remove, len, Find, BreastCancer, OvarianCancer, PancreaticCancer, if, else, for, int, str, bool, func, print, return.

# Arquitectura general del compilador
 El proyecto está dividido en 3 fases. Cada una de estas fases fueron implementadas desde cero con ayuda de las clase prácticas de la asignatura.
   1. Tokenización: Este se encarga de todo el proceso de tokenización de la entrada y detecta algunos errores como la de comandos no definidos.
   2. Parser: Este se encarga de todo el proceso de confección del parse shiftreduce y el autómata LR1.
   3. Ast: Por ultimo en esta fase se lleva a cabo la confección del Ast con ayuda de Nodes.py, asi como su recorrido y evaluación y el chequeo semántico. 
    
# Ejecución
  Para la ejecución es necesario:
   1. Escribir el código a compilar en code.txt.
   2. Compilar el archivo test.py este se encarga de todo el proceso, iniciando en la lectura del txt
