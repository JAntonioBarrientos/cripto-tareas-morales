import unittest
from gf import GF, GFElement

class TestGFOperations(unittest.TestCase):
    def setUp(self):
        # Definir los polinomios irreducibles para cada campo como enteros
        # Ejemplos:
        # GF(4): x^2 + x + 1 -> 0b111 (7)
        # GF(8): x^3 + x + 1 -> 0b1011 (11)
        # GF(64): x^6 + x + 1 -> 0b1000011 (67)
        self.gf4 = GF(2, 0b111)        # GF(4)
        self.gf8 = GF(3, 0b1011)       # GF(8)
        self.gf64 = GF(6, 0b1000011)   # GF(64)

    # Pruebas de Suma y Resta en GF(4)
    def test_addition_gf4(self):
        a = self.gf4.element(0b01)  # 1
        b = self.gf4.element(0b10)  # 2
        result = a + b              # 1 ^ 2 = 3 (0b11)
        expected = 0b11
        self.assertEqual(result.value, expected, "Suma en GF(4) incorrecta.")

    def test_subtraction_gf4(self):
        a = self.gf4.element(0b11)  # 3
        b = self.gf4.element(0b10)  # 2
        result = a - b              # 3 ^ 2 = 1 (0b01)
        expected = 0b01
        self.assertEqual(result.value, expected, "Resta en GF(4) incorrecta.")

    # Pruebas de Suma y Resta en GF(8)
    def test_addition_gf8(self):
        a = self.gf8.element(0b010)  # 2
        b = self.gf8.element(0b101)  # 5
        result = a + b              # 2 ^ 5 = 7 (0b111)
        expected = 0b111
        self.assertEqual(result.value, expected, "Suma en GF(8) incorrecta.")

    def test_subtraction_gf8(self):
        a = self.gf8.element(0b110)  # 6
        b = self.gf8.element(0b011)  # 3
        result = a - b              # 6 ^ 3 = 5 (0b101)
        expected = 0b101
        self.assertEqual(result.value, expected, "Resta en GF(8) incorrecta.")

    # Pruebas de Suma y Resta entre Campos Diferentes
    def test_addition_different_fields(self):
        a = self.gf4.element(0b01)  # GF(4)
        b = self.gf8.element(0b01)  # GF(8)
        with self.assertRaises(ValueError):
            _ = a + b

    def test_subtraction_different_fields(self):
        a = self.gf4.element(0b01)  # GF(4)
        b = self.gf8.element(0b01)  # GF(8)
        with self.assertRaises(ValueError):
            _ = a - b

    # Pruebas con Elemento Neutro (0) en GF(64)
    def test_addition_identity_gf64(self):
        a = self.gf64.element(0b1010)  # 10
        zero = self.gf64.element(0b000000)  # 0
        result = a + zero
        self.assertEqual(result, a, "Suma con el elemento neutro en GF(64) falló.")

    def test_subtraction_identity_gf64(self):
        a = self.gf64.element(0b1010)  # 10
        zero = self.gf64.element(0b000000)  # 0
        result = a - zero
        self.assertEqual(result, a, "Resta con el elemento neutro en GF(64) falló.")

    # Pruebas de Multiplicación en GF(4)
    def test_multiplication_gf4(self):
        a = self.gf4.element(0b10)  # 2
        b = self.gf4.element(0b10)  # 2
        result = a * b              # 2 * 2 = 4 -> reducción: 4 ^ 7 = 3 (0b11)
        expected = 0b11
        self.assertEqual(result.value, expected, "Multiplicación en GF(4) incorrecta.")

    # Pruebas de Multiplicación en GF(8)
    def test_multiplication_gf8(self):
        a = self.gf8.element(0b010)  # 2 (x)
        b = self.gf8.element(0b011)  # 3 (x + 1)
        result = a * b              # x * (x + 1) = x^2 + x = 0b110
        expected = 0b110
        self.assertEqual(result.value, expected, "Multiplicación en GF(8) incorrecta.")

    def test_multiplication_with_reduction_gf8(self):
        a = self.gf8.element(0b100)  # 4 (x^2)
        b = self.gf8.element(0b010)  # 2 (x)
        result = a * b              # x^2 * x = x^3 -> reducción: x^3 + x + 1 = 0b1011 ^ 0b1000 = 0b0011 (3)
        expected = 0b011  # 3
        self.assertEqual(result.value, expected, "Multiplicación con reducción en GF(8) falló.")

    def test_multiplication_identity_gf64(self):
        a = self.gf64.element(0b1010)  # 10
        one = self.gf64.element(0b000001)  # 1
        result = a * one
        self.assertEqual(result, a, "Multiplicación con el elemento neutro (1) en GF(64) falló.")

    def test_multiplication_zero_gf64(self):
        a = self.gf64.element(0b1010)  # 10
        zero = self.gf64.element(0b000000)  # 0
        result = a * zero
        expected = 0b000000
        self.assertEqual(result.value, expected, "Multiplicación con cero en GF(64) falló.")

    # Pruebas de División en GF(8)
    def test_division_gf8(self):
        a = self.gf8.element(0b011)  # 3
        b = self.gf8.element(0b010)  # 2
        result = a / b              # 3 / 2 = 3 * inverse(2) = 3 * 5 = x +1 * x^2 +1 = x^3 +x +x^2 +1 = x^2 =4
        expected = 0b100  # 4
        self.assertEqual(result.value, expected, "División en GF(8) incorrecta.")

    def test_division_by_one_gf64(self):
        a = self.gf64.element(0b1010)  # 10
        one = self.gf64.element(0b000001)  # 1
        result = a / one
        self.assertEqual(result, a, "División por 1 en GF(64) falló.")

    def test_division_by_self_gf8(self):
        a = self.gf8.element(0b101)  # 5
        result = a / a
        expected = self.gf8.element(0b001)  # 1
        self.assertEqual(result, expected, "División de un elemento por sí mismo en GF(8) falló.")

    def test_division_by_zero_gf8(self):
        a = self.gf8.element(0b101)  # 5
        zero = self.gf8.element(0b000)  # 0
        with self.assertRaises(ZeroDivisionError):
            _ = a / zero

    # Pruebas de Exponenciación en GF(8) y GF(4)
    def test_exponentiation_positive_gf8(self):
        a = self.gf8.element(0b010)  # 2 (x)
        exponent = 3
        result = a ** exponent      # x^3 = x + 1 = 0b011
        expected = 0b011
        self.assertEqual(result.value, expected, "Exponenciación positiva en GF(8) falló.")

    def test_exponentiation_zero_gf8(self):
        a = self.gf8.element(0b101)  # 5
        exponent = 0
        result = a ** exponent
        expected = 0b001  # 1
        self.assertEqual(result.value, expected, "Exponenciación a la potencia 0 en GF(8) falló.")

    def test_exponentiation_negative_gf8(self):
        a = self.gf8.element(0b010)  # 2 (x)
        exponent = -1
        result = a ** exponent      # Inverso de 2 es 5 (0b101)
        expected = 0b101
        self.assertEqual(result.value, expected, "Exponenciación negativa en GF(8) falló.")

    def test_exponentiation_negative_gf4(self):
        a = self.gf4.element(0b10)  # 2
        exponent = -1
        result = a ** exponent      # Inverso de 2 en GF(4) es 3 (0b11)
        expected = 0b11
        self.assertEqual(result.value, expected, "Exponenciación negativa en GF(4) falló.")

    def test_exponentiation_large_gf64(self):
        a = self.gf64.element(0b000010)  # 2
        exponent = 10
        result = a ** exponent
        # Calculo manual:
        # 2^1 = 2
        # 2^2 = 4
        # 2^3 = 8
        # 2^4 = 16
        # 2^5 = 32
        # 2^6 = 64 → reduce: 64 ^ 67 (0b1000011) = 3
        # 2^7 = 3 * 2 = 6
        # 2^8 = 6 * 2 = 12
        # 2^9 = 12 * 2 = 24
        # 2^10 = 24 * 2 = 48
        expected = 0b110000  # 48
        self.assertEqual(result.value, expected, "Exponenciación grande en GF(64) falló.")

if __name__ == '__main__':
    unittest.main()
