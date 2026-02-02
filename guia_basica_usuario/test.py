import unittest

def cuadrado(numero: int) -> int:
    return numero ** 2

class Pruebas(unittest.TestCase):
    def test_cuadrado(self):
        lista = [1, 2, 3, 4, 5]
        cuadrados_lista = [n ** 2 for n in lista]
        self.assertEqual(cuadrados_lista, [1, 4, 9, 16, 25])
    
if __name__ == '__main__':
    unittest.main()