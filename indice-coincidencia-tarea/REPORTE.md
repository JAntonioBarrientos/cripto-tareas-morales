# Calcula el índice de coincidencia en español

## Instrucciones
Para esta tarea moral, debes conseguir y procesar textos en español suficientemente grandes y calcular tu propio índice de coincidencias.

**Definición 2.1** El índice de coincidencias de una muestra de texto T sobre el alfabeto convencional de 26 letras es:
$$IC(T) = \sum_{i=1}^{26} \frac{n_i(n_i - 1)}{N(N - 1)}$$

donde  $n_i$ es el número de apariciones de la i-ésima letra del alfabeto en  $T$, y  $N$ es la longitud del texto  $T$.

## Ejecución
Coloca tus textos en la carpeta `textos` y ejecuta el script `ic.py`. En ella ya se incluyen ejemplos de textos en español.

## Resultados

Con los textos de prueba se obtuvieron los siguientes resultados:

```bash
Letra  Apariciones  Porcentaje (%) 
-----------------------------------
E      128095       13.51          
A      106051       11.18          
O      81534        8.60           
S      71974        7.59           
N      66762        7.04           
R      62244        6.56           
I      60004        6.33           
L      50212        5.29           
T      48550        5.12           
D      44806        4.72           
C      43141        4.55           
U      39109        4.12           
M      31956        3.37           
P      27503        2.90           
B      14459        1.52           
G      11383        1.20           
Q      9812         1.03           
F      9577         1.01           
V      9526         1.00           
H      8486         0.89           
Y      8059         0.85           
J      4566         0.48           
Z      3526         0.37           
X      3513         0.37           
K      2030         0.21           
W      1594         0.17           
-----------------------------------
Total de letras: 948472
Índice de Coincidencia (IC): 0.07145
```