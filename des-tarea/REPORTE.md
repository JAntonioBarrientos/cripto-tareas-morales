# Tarea Implementación DES

## Instrucciones

Implementa DES. Puedes usar ChatGPT, Gemini. o tu imaginación, pero asegúrate que esté bien hecho. (1 punto)

## Investigación llaves de DES


### Llaves Débiles

Las llaves débiles en DES presentan una particularidad que las hace vulnerables: cada mitad de la llave está compuesta únicamente por ceros o unos. Esto provoca que la misma subllave se utilice en cada una de las rondas del algoritmo de cifrado, eliminando la variabilidad necesaria para garantizar la seguridad. LLaves débiles:

- 0101010101010101
- `fefefefefefefefe`
- `1f1f1f1f1f1f1f1f`
- `e0e0e0e0e0e0e0e0`

### Llaves Semi-Débiles

Las llaves semi-débiles forman parejas donde cada llave puede utilizarse para descifrar mensajes cifrados con la otra llave del par. Estas llaves generan únicamente dos subllaves en lugar de dieciséis, y cada subllave se utiliza ocho veces en el algoritmo. LLaves semi-débiles:

- 01fe01fe01fe01fe  fe01fe01fe01fe01
- 1fe01fe01fe01fe0  e01fe01fe01fe01f
- `01e001e001e001e0`  `e001e001e001e001`
- 1ffe1ffe1ffe1ffe  fe1ffe1ffe1ffe1f
- 011f011f011f011f  1f011f011f011f01
- e0fee0fee0fee0fe  fee0fee0fee0fee0

El uso repetido de las mismas subllaves con estas llaves incrementa la probabilidad de que se identifiquen patrones, debilitando la resistencia del cifrado frente a ataques.

### Llaves Posiblemente Débiles

Además de las llaves débiles y semi-débiles, existen llaves clasificadas como posiblemente débiles. Estas llaves generan sólo cuatro subllaves, cada una utilizada cuatro veces por el algoritmo. Aunque no son tan vulnerables como las débiles o semi-débiles, su uso también reduce la seguridad del cifrado. Se identifican 48 llaves posiblemente débiles, entre las cuales se incluyen:

- 1f1f01010e0e0101  e00101e0f10101f1
- 011f1f01010e0e01  fe1f01e0fe0e01f1
- `1f01011f0e01010e`  `fe011fe0fe010ef1`
- `01011f1f01010e0e`  `e01f1fe0f10e0ef1`
- ...

El uso de llaves débiles, semi-débiles y posiblemente débiles en DES afecta la seguridad del cifrado pues disminuye la entropía del cifrado, facilitando la identificación de patrones y la ruptura del cifrado. Así que en conclusión es mala idea utilizar estas llaves ya que facilitan la tarea de los atacantes para descifrar mensajes cifrados.


## Preguntas
### ¿Qué pasa al usar estas llaves?

Al usar llaves débiles, semi-débiles o posiblemente débiles en el algoritmo DES, se reduce la entropía del cifrado. Esto provoca patrones repetitivos en el proceso de cifrado, lo que facilita la identificación y ataque por parte de terceros.

### ¿Por qué es mala idea usarlas?

El uso de estas llaves disminuye la seguridad del cifrado, ya que los patrones repetitivos pueden ser explotados para descifrar mensajes sin conocer la llave completa. Esto aumenta la vulnerabilidad del sistema frente a ataques criptográficos, comprometiendo la integridad y confidencialidad de la información.

### ¿Por qué el diseño de DES hace que éstas llaves no sean las adecuadas?

El diseño de DES hace que estas llaves no sean adecuadas porque cada mitad de la llave compuesta únicamente por ceros o unos resulta en la reutilización de las mismas subllaves en cada ronda del algoritmo de cifrado. Esta falta de variabilidad necesaria reduce la entropía del cifrado y facilita la identificación de patrones, debilitando la seguridad del sistema.