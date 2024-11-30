# gf.py

class GF:
    def __init__(self, degree, irreducible_poly):
        """
        Inicializa el campo finito GF(2^degree).

        :param degree: Grado del campo finito (n en GF(2^n)).
        :param irreducible_poly: Polinomio irreducible representado como un entero.
                                 Por ejemplo, x^3 + x + 1 se representa como 0b1011 (11).
        """
        if degree <= 0:
            raise ValueError("El grado del campo debe ser un entero positivo.")
        
        # Verificar que el polinomio irreducible tiene el grado correcto
        if irreducible_poly >> degree == 0:
            raise ValueError(f"El polinomio irreducible debe tener grado {degree}.")

        self.degree = degree
        self.irreducible_poly = irreducible_poly
        self.order = 1 << degree  # 2^degree

    def element(self, value):
        """
        Crea un nuevo elemento del campo.

        :param value: Valor del elemento como entero.
        :return: Instancia de GFElement.
        """
        return GFElement(self, value)

    def __eq__(self, other):
        """Igualdad entre dos campos finitos."""
        if not isinstance(other, GF):
            return False
        return (self.degree == other.degree and
                self.irreducible_poly == other.irreducible_poly and
                self.order == other.order)


class GFElement:
    def __init__(self, field, value):
        """
        Inicializa un elemento del campo finito.

        :param field: Instancia de GF que representa el campo.
        :param value: Valor del elemento como entero.
        """
        if not isinstance(field, GF):
            raise TypeError("field debe ser una instancia de GF.")
        self.field = field
        self.value = value & (field.order - 1)  # Asegura que el valor esté dentro del campo

    def __add__(self, other):
        """Suma de dos elementos del campo utilizando XOR."""
        if not isinstance(other, GFElement):
            return NotImplemented
        if self.field != other.field:
            raise ValueError("Los elementos deben pertenecer al mismo campo para sumar.")
        result = self.value ^ other.value
        return GFElement(self.field, result)

    def __sub__(self, other):
        """Resta de dos elementos del campo utilizando XOR (igual que la suma)."""
        return self.__add__(other)  # En GF(2^n), la resta es igual a la suma

    def __mul__(self, other):
        """Multiplicación de dos elementos del campo con reducción modular."""
        if not isinstance(other, GFElement):
            return NotImplemented
        if self.field != other.field:
            raise ValueError("Los elementos deben pertenecer al mismo campo para multiplicar.")
        
        a = self.value
        b = other.value
        result = 0

        while b:
            if b & 1:
                result ^= a  # Suma polinómica (XOR)
            a <<= 1
            b >>= 1

        # Reducción modular
        result = self._reduce(result)
        return GFElement(self.field, result)

    def _reduce(self, poly):
        """Reduce el polinomio 'poly' usando el polinomio irreducible del campo."""
        irreducible = self.field.irreducible_poly
        degree = self.field.degree
        while poly.bit_length() > degree:
            shift = poly.bit_length() - degree - 1
            poly ^= irreducible << shift
        return poly

    def __truediv__(self, other):
        """División de dos elementos del campo: self / other."""
        if not isinstance(other, GFElement):
            return NotImplemented
        if self.field != other.field:
            raise ValueError("Los elementos deben pertenecer al mismo campo para dividir.")
        if other.value == 0:
            raise ZeroDivisionError("No se puede dividir por cero en un campo finito.")
        inverse = self._multiplicative_inverse(other)
        return self * inverse

    def _multiplicative_inverse(self, other):
        """Calcula el inverso multiplicativo de 'other' usando el algoritmo extendido de Euclides."""
        a = other.value
        b = self.field.irreducible_poly
        u, v = a, b
        g1, g2 = 1, 0

        while u != 1:
            j = u.bit_length() - v.bit_length()
            if j < 0:
                u, v = v, u
                g1, g2 = g2, g1
                j = -j
            u = u ^ (v << j)
            g1 = g1 ^ (g2 << j)
        
        # g1 es el inverso multiplicativo
        return GFElement(self.field, g1)

    def __pow__(self, exponent):
        """Exponenciación de un elemento del campo."""
        if not isinstance(exponent, int):
            raise TypeError("El exponente debe ser un entero.")
        
        if exponent == 0:
            return self.field.element(1)  # Elemento neutro multiplicativo
        
        elif exponent < 0:
            inverse = self._multiplicative_inverse(self)
            base = inverse
            exponent = -exponent
        else:
            base = self

        result = self.field.element(1)  # Elemento neutro multiplicativo
        while exponent > 0:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        return result

    def __eq__(self, other):
        """Igualdad entre dos elementos del campo."""
        if not isinstance(other, GFElement):
            return False
        return (self.value == other.value and
                self.field == other.field)

    def __repr__(self):
        """Representación del elemento en formato binario."""
        return f"GFElement({bin(self.value)})"

    def __str__(self):
        """Representación del elemento en formato binario."""
        return self.__repr__()

    def __hash__(self):
        """Permite usar GFElement como claves en diccionarios."""
        return hash((self.field, self.value))

    def __neg__(self):
        """Negación de un elemento (igual a sí mismo en GF(2^n))."""
        return self  # En GF(2^n), -a = a


# Agregar método __eq__ a la clase GF para comparar campos
def gf_eq(self, other):
    if not isinstance(other, GF):
        return False
    return (self.degree == other.degree and
            self.irreducible_poly == other.irreducible_poly and
            self.order == other.order)

GF.__eq__ = gf_eq
