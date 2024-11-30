from gf import GF, GFElement

class Calculator:
    def __init__(self):
        # Polinomios irreducibles para cada campo como enteros
        self.irreducible_polys = {
            2: 0b11,        # GF(2): x + 1
            4: 0b111,       # GF(4): x^2 + x + 1
            8: 0b1011,      # GF(8): x^3 + x + 1
            16: 0b10011,    # GF(16): x^4 + x + 1 
            32: 0b100101,   # GF(32): x^5 + x^2 + 1
            64: 0b1000011,  # GF(64): x^6 + x + 1
        }
        self.fields = {size: GF(degree=size.bit_length()-1, irreducible_poly=poly) 
                       for size, poly in self.irreducible_polys.items()}
        self.current_field = None

    def run(self):
        print("=== Calculadora de Campos Finitos ===\n")
        self.select_field()
        self.main_menu()

    def select_field(self):
        print("Selecciona el campo finito con el que deseas trabajar:")
        print("1. GF(2)")
        print("2. GF(4)")
        print("3. GF(8)")
        print("4. GF(16)")
        print("5. GF(32)")
        print("6. GF(64)")
        choice = input("Ingresa el número correspondiente: ").strip()

        field_map = {'1': 2, '2': 4, '3': 8, '4': 16, '5': 32, '6': 64}
        if choice in field_map:
            field_size = field_map[choice]
            self.current_field = self.fields[field_size]
            poly = self.irreducible_polys[field_size]
            print(f"\nCampo finito seleccionado: GF({field_size})")
            print(f"Polinomio irreducible: {self.poly_to_string(poly)}\n")
        else:
            print("Selección inválida. Por favor, intenta de nuevo.\n")
            self.select_field()

    def main_menu(self):
        while True:
            print("--- Menú de Operaciones ---")
            print("1. Suma (+)")
            print("2. Resta (-)")
            print("3. Multiplicación (*)")
            print("4. División (/)")
            print("5. Exponenciación (^)")
            print("6. Tabla de Exponenciación")
            print("7. Salir")
            choice = input("Selecciona una opción: ").strip()

            if choice == '1':
                self.perform_binary_operation('suma', '+')
            elif choice == '2':
                self.perform_binary_operation('resta', '-')
            elif choice == '3':
                self.perform_binary_operation('multiplicación', '*')
            elif choice == '4':
                self.perform_binary_operation('división', '/')
            elif choice == '5':
                self.perform_exponentiation()
            elif choice == '6':
                self.perform_exponentiation_table()
            elif choice == '7':
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, intenta de nuevo.\n")

    def perform_binary_operation(self, operation_name, operator):
        print(f"\n--- {operation_name.capitalize()} en GF({self.current_field.order}) ---")
        print("Define el primer operando:")
        elem1 = self.get_element()
        print("Define el segundo operando:")
        elem2 = self.get_element()

        try:
            if operator == '+':
                result = elem1 + elem2
            elif operator == '-':
                result = elem1 - elem2
            elif operator == '*':
                result = elem1 * elem2
            elif operator == '/':
                result = elem1 / elem2
            else:
                print("Operador inválido.")
                return
            print(f"\nResultado: {elem1} {operator} {elem2} = {result}\n")
        except ZeroDivisionError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Error inesperado: {e}\n")

    def perform_exponentiation(self):
        print(f"\n--- Exponenciación en GF({self.current_field.order}) ---")
        print("Define el operando base:")
        base = self.get_element()
        exponent_input = input("Ingresa el exponente (entero): ").strip()
        try:
            exponent = int(exponent_input)
            result = base ** exponent
            print(f"\nResultado: {base} ^ {exponent} = {result}\n")
        except ValueError:
            print("Exponente inválido. Debe ser un número entero.\n")
        except Exception as e:
            print(f"Error inesperado: {e}\n")

    def perform_exponentiation_table(self):
        print(f"\n--- Tabla de Exponenciación en GF({self.current_field.order}) ---")
        print("Define el elemento para generar su tabla de exponenciación:")
        element = self.get_element()

        exponent = 1
        current = element
        table = []

        while True:
            table.append((exponent, current))
            # Multiplicar por el elemento para obtener la siguiente potencia
            try:
                current = current * element
            except Exception as e:
                print(f"Error al multiplicar: {e}")
                break

            exponent += 1

            # Detenerse si hemos llegado al elemento neutro
            if current.value == 1:
                table.append((exponent, current))
                break

            # Prevenir bucles infinitos: en GF(2^n), el máximo exponente es 2^n -1
            if exponent >= self.current_field.order:
                print("Se alcanzó el máximo exponente sin encontrar el elemento neutro.")
                break

        # Mostrar la tabla
        print(f"\nTabla de Exponenciación para {element}:\n")
        print(f"{'Exponente':>10} | {'Elemento (Binario)':>20} | {'Elemento (Polinómico)':>30}")
        print("-" * 65)
        for exp, elem in table:
            print(f"{exp:>10} | {bin(elem.value):>20} | {str(elem):>30}")
        print()  # Línea en blanco

    def get_element(self):
        degree = self.current_field.degree
        # El polinomio irreducible tiene grado 'degree', pero los elementos tienen grado 'degree -1'
        element_degree = degree -1
        print(f"Ingresa los coeficientes del polinomio de grado {element_degree} a 0.")
        print("Por ejemplo, para x^3 + x + 1, ingresa: 1 0 1 1")
        polinomio = self.poly_to_string(self.irreducible_polys[self.current_field.order])
        print(f"Polinomio irreducible: {polinomio}")
        coeffs_input = input("Coeficientes (separados por espacios): ").strip()
        coeffs = coeffs_input.split()
        expected_coeffs = element_degree +1
        if len(coeffs) != expected_coeffs:
            print(f"Debe ingresar exactamente {expected_coeffs} coeficientes.\n")
            return self.get_element()
        try:
            coeffs = [int(c) for c in coeffs]
            if any(c not in [0,1] for c in coeffs):
                print("Los coeficientes deben ser 0 o 1.\n")
                return self.get_element()
            # Convertir los coeficientes a un entero binario
            poly = 0
            for c in coeffs:
                poly = (poly << 1) | c
            element = self.current_field.element(poly)
            print(f"Elemento definido: {element}\n")
            return element
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar solo números enteros (0 o 1).\n")
            return self.get_element()

    def poly_to_string(self, poly):
        """Convierte un polinomio binario a su representación polinómica."""
        if poly == 0:
            return "0"
        degree = poly.bit_length() -1
        terms = []
        for i in range(degree, -1, -1):
            if (poly >> i) &1:
                if i ==0:
                    terms.append("1")
                elif i ==1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        return " + ".join(terms)

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
