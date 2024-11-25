import os
import string
from collections import Counter
import re

# Variable global que define la carpeta que contiene los textos
TEXTS_FOLDER = "textos"

class TextReader:
    """
    Clase para leer archivos de texto desde una carpeta especificada.
    """
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.texts = {}
    
    def read_texts(self):
        """
        Lee todos los archivos .txt en la carpeta y los almacena en el diccionario self.texts
        con el nombre del archivo como clave y el contenido como valor.
        """
        if not os.path.isdir(self.folder_path):
            raise NotADirectoryError(f"La carpeta '{self.folder_path}' no existe.")
        
        archivos = os.listdir(self.folder_path)
        archivos_txt = [archivo for archivo in archivos if archivo.lower().endswith('.txt')]
        
        if not archivos_txt:
            raise FileNotFoundError("No se encontraron archivos .txt en la carpeta especificada.")
        
        for archivo in archivos_txt:
            ruta_completa = os.path.join(self.folder_path, archivo)
            with open(ruta_completa, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.texts[archivo] = contenido
    
    def get_texts(self):
        """
        Retorna el diccionario de textos leídos.
        """
        return self.texts

class IndexOfCoincidenceCalculator:
    """
    Clase para calcular las frecuencias de letras, los porcentajes de aparición y el índice de coincidencia.
    """
    def __init__(self, text):
        self.text = text
        self.letter_counts = {}
        self.total_letters = 0
        self.ic = 0.0
        self.letter_percentages = {}
    
    def preprocess_text(self):
        """
        Limpia el texto eliminando caracteres que no son letras y convierte todo a mayúsculas.
        """
        # Utiliza expresiones regulares para mantener solo letras
        self.text = re.sub('[^A-Za-z]', '', self.text).upper()
    
    def count_letters(self):
        """
        Cuenta las apariciones de cada letra en el texto.
        """
        counter = Counter(self.text)
        # Asegura que todas las 26 letras estén en el diccionario, incluso si su conteo es 0
        for letra in string.ascii_uppercase:
            self.letter_counts[letra] = counter.get(letra, 0)
        self.total_letters = sum(self.letter_counts.values())
    
    def calculate_percentages(self):
        """
        Calcula el porcentaje de aparición de cada letra.
        """
        if self.total_letters == 0:
            for letra in string.ascii_uppercase:
                self.letter_percentages[letra] = 0.0
            return
        
        for letra, count in self.letter_counts.items():
            self.letter_percentages[letra] = (count / self.total_letters) * 100
    
    def calculate_ic(self):
        """
        Calcula el índice de coincidencia según la definición dada.
        """
        if self.total_letters <= 1:
            self.ic = 0.0
            return
        
        numerator = sum(n_i * (n_i - 1) for n_i in self.letter_counts.values())
        denominator = self.total_letters * (self.total_letters - 1)
        self.ic = numerator / denominator
    
    def display_table(self):
        """
        Muestra una tabla con las apariciones de cada letra, su porcentaje de aparición,
        ordenadas de las más frecuentes a las menos frecuentes.
        """
        # Crear una lista de tuplas (letra, conteo, porcentaje)
        tabla = []
        for letra in string.ascii_uppercase:
            tabla.append((letra, self.letter_counts[letra], self.letter_percentages[letra]))
        
        # Ordenar la tabla por conteo descendente
        tabla_ordenada = sorted(tabla, key=lambda x: x[1], reverse=True)
        
        # Imprimir la tabla
        print(f"{'Letra':<6} {'Apariciones':<12} {'Porcentaje (%)':<15}")
        print("-" * 35)
        for letra, conteo, porcentaje in tabla_ordenada:
            print(f"{letra:<6} {conteo:<12} {porcentaje:<15.2f}")
        print("-" * 35)
        print(f"Total de letras: {self.total_letters}")
    
    def get_ic(self):
        """
        Retorna el índice de coincidencia calculado.
        """
        return self.ic
    
    def process(self):
        """
        Ejecuta todos los pasos necesarios para calcular el índice de coincidencia.
        """
        self.preprocess_text()
        self.count_letters()
        self.calculate_percentages()
        self.calculate_ic()

def main():
    print("Cálculo del Índice de Coincidencia para Todos los Textos en la Carpeta")
    print(f"Carpeta de textos: {TEXTS_FOLDER}\n")
    
    # Leer los textos
    lector = TextReader(TEXTS_FOLDER)
    try:
        lector.read_texts()
    except Exception as e:
        print(f"Error: {e}")
        return
    
    textos = lector.get_texts()
    
    # Combinar todos los textos en uno solo
    texto_combinado = ""
    for nombre_archivo, contenido in textos.items():
        print(f"Lectura de archivo: {nombre_archivo}")
        texto_combinado += contenido + " "  # Añadir un espacio para separar textos
    
    print("\nCalculando Índice de Coincidencia para el texto combinado...\n")
    
    # Calcular IC para el texto combinado
    calculador = IndexOfCoincidenceCalculator(texto_combinado)
    calculador.process()
    calculador.display_table()
    ic = calculador.get_ic()
    print(f"Índice de Coincidencia (IC): {ic:.5f}")

if __name__ == "__main__":
    main()
