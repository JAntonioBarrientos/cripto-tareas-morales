# Calcula el índice de coincidencia en español

## Instrucciones
Para esta tarea moral, debes conseguir y procesar textos en español suficientemente grandes y calcular tu propio índice de coincidencias.

**Definición 2.1** El índice de coincidencias de una muestra de texto T sobre el alfabeto convencional de 26 letras es:
$$IC(T) = \sum_{i=1}^{26} \frac{n_i(n_i - 1)}{N(N - 1)}$$

donde  $n_i$ es el número de apariciones de la i-ésima letra del alfabeto en  $T$, y  $N$ es la longitud del texto  $T$.

## Ejecución
Coloca tus textos en la carpeta `textos` y ejecuta el script `ic.py`. En ella ya se incluyen ejemplos de textos en español.