# Calculadora de Campos Finitos

## Pruebas unitarias
Para ejecutar las pruebas unitarias, se debe correr el siguiente comando:
```sh
  python3 test_gf.py
```

## Instrucciones de Uso

Para cada campo se usan los siguientes polinomios irreducibles:

- **GF(2^1)**: x + 1
- **GF(2^2)**: x^2 + x + 1
- **GF(2^3)**: x^3 + x + 1
- **GF(2^4)**: x^4 + x + 1
- **GF(2^5)**: x^5 + x^2 + 1
- **GF(2^6)**: x^6 + x + 1

Para utilizar la calculadora de campos finitos, sigue estos pasos:

1. Ejecuta el script `calculator.py`:
    ```sh
    python3 calculator.py
    ```

2. Selecciona el campo finito con el que deseas trabajar:
    ```plaintext
    Selecciona el campo finito con el que deseas trabajar:
    1. GF(2)
    2. GF(4)
    3. GF(8)
    4. GF(16)
    5. GF(32)
    6. GF(64)
    Ingresa el número correspondiente: 
    ```

3. Una vez seleccionado el campo finito, el menú principal te permitirá realizar las siguientes operaciones:
    ```plaintext
    --- Menú de Operaciones ---
    1. Suma (+)
    2. Resta (-)
    3. Multiplicación (*)
    4. División (/)
    5. Exponenciación (^)
    6. Tabla de Exponenciación
    7. Salir
    ```

4. Para cada operación, se te pedirá que ingreses los coeficientes de los polinomios que representan los elementos del campo finito. Por ejemplo, para ingresar el polinomio \(x^3 + x + 1\), debes ingresar `1 0 1 1`.

5. Sigue las instrucciones en pantalla para realizar la operación seleccionada y ver el resultado.

6. Para salir de la calculadora, selecciona la opción `7. Salir`.

### Ejemplo de Uso

A continuación se muestra un ejemplo de uso de la calculadora:

```plaintext
=== Calculadora de Campos Finitos ===

Selecciona el campo finito con el que deseas trabajar:
1. GF(2)
2. GF(4)
3. GF(8)
4. GF(16)
5. GF(32)
6. GF(64)
Ingresa el número correspondiente: 3

Campo finito seleccionado: GF(8)
Polinomio irreducible: x^3 + x + 1

--- Menú de Operaciones ---
1. Suma (+)
2. Resta (-)
3. Multiplicación (*)
4. División (/)
5. Exponenciación (^)
6. Tabla de Exponenciación
7. Salir
Selecciona una opción: 1

--- Suma en GF(8) ---
Define el primer operando:
Ingresa los coeficientes del polinomio de grado 2 a 0.
Por ejemplo, para x^3 + x + 1, ingresa: 1 0 1 1
Polinomio irreducible: x^3 + x + 1
Coeficientes (separados por espacios): 1 0 1
Elemento definido: x^2 + 1

Define el segundo operando:
Ingresa los coeficientes del polinomio de grado 2 a 0.
Por ejemplo, para x^3 + x + 1, ingresa: 1 0 1 1
Polinomio irreducible: x^3 + x + 1
Coeficientes (separados por espacios): 0 1 1
Elemento definido: x + 1

Resultado: x^2 + 1 + x + 1 = x^2 + x
```

### Explicación de la Implementación de GF

#### Suma (`__add__`)
**Proceso:**
- **Verificación de Campo:** Asegura que ambos elementos pertenezcan al mismo campo finito.
- **Operación XOR:** Aplica una operación XOR bit a bit entre los valores binarios de los elementos.
- **Creación del Resultado:** Retorna un nuevo `GFElement` con el valor resultante de la operación XOR.

#### Resta (`__sub__`)
**Proceso:** En GF(2^n), la resta es equivalente a la suma, por lo que este método delega la operación a `__add__`.

#### Multiplicación (`__mul__`)
**Proceso:**
- **Verificación de Campo:** Confirma que ambos elementos pertenezcan al mismo campo finito.
- **Multiplicación Polinómica:**
  - Inicializa un resultado en cero.
  - Itera sobre cada bit del multiplicador (`other.value`):
    - Si el bit actual es 1, aplica XOR al resultado con el multiplicando (`self.value`).
    - Desplaza el multiplicando una posición a la izquierda y el multiplicador una posición a la derecha.
- **Reducción Modular:**
  - Aplica la función `_reduce` al resultado de la multiplicación para asegurar que el polinomio resultante tenga un grado menor que el campo finito.
- **Creación del Resultado:** Retorna un nuevo `GFElement` con el valor reducido.

#### Reducción Modular (`_reduce`)
Reduce un polinomio de grado mayor o igual al del campo finito utilizando el polinomio irreducible.

**Proceso:**
- **Obtención del Polinomio Irreducible y Grado:** Recupera el polinomio irreducible del campo y su grado.
- **Iteración de Reducción:**
  - Mientras el grado del polinomio a reducir (`poly.bit_length() - 1`) exceda el grado del campo:
    - Calcula el desplazamiento necesario para alinear el polinomio irreducible con el término de mayor grado del polinomio actual.
    - Aplica una operación XOR entre el polinomio actual y el polinomio irreducible desplazado.
- **Resultado Final:** Devuelve el polinomio reducido que ahora tiene un grado menor que el campo finito.

#### División (`__truediv__`)
**Proceso:**
- **Verificación de Campo y Divisor No Nulo:** Asegura que ambos elementos pertenezcan al mismo campo finito y que el divisor no sea cero.
- **Cálculo del Inverso Multiplicativo:**
  - Utiliza el algoritmo extendido de Euclides para encontrar el inverso multiplicativo del divisor.
- **Multiplicación por el Inverso:** Multiplica el dividendo por el inverso multiplicativo del divisor utilizando `__mul__`.
- **Creación del Resultado:** Retorna un nuevo `GFElement` que representa el cociente de la división.

#### Inverso Multiplicativo (`_multiplicative_inverse`)
**Proceso:**
- **Inicialización:** Asigna los valores de `a` (elemento a invertir) y `b` (polinomio irreducible).
- **Algoritmo Extendido de Euclides:**
  - Itera hasta que `u = 1`, aplicando operaciones XOR y desplazamientos para reducir el grado del polinomio.
  - Durante cada iteración, ajusta los coeficientes `g1` y `g2` que eventualmente representarán el inverso.
- **Resultado Final:** Devuelve un nuevo `GFElement` que es el inverso multiplicativo del elemento original.

#### Exponenciación (`__pow__`)
**Proceso:**
- **Manejo de Exponentes Negativos:** Si el exponente es negativo, calcula el inverso multiplicativo del elemento y utiliza el exponente positivo correspondiente.
- **Inicialización:**
  - Establece el resultado inicial como el elemento neutro multiplicativo (1).
  - Establece la base para la exponenciación como el elemento actual.
- **Exponenciación Rápida (Exponentiación Binaria):**
  - Mientras el exponente sea mayor que cero:
    - Si el bit menos significativo del exponente es 1, multiplica el resultado actual por la base.
    - Multiplica la base por sí misma.
    - Desplaza el exponente una posición a la derecha.
- **Creación del Resultado:** Retorna un nuevo `GFElement` que representa el elemento elevado a la potencia especificada.
