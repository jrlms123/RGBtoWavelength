import numpy as np
from scipy.spatial import KDTree

def rgb_to_wavelength(r, g, b):
    """
    Converte valores RGB em um comprimento de onda aproximado no espectro visível (380-700 nm).

    Parâmetros:
        r (int): Valor de vermelho (0-255).
        g (int): Valor de verde (0-255).
        b (int): Valor de azul (0-255).

    Retorna:
        float ou str: Comprimento de onda em nanômetros, ou -1 para cores fora do espectro visível.
    """
    # Passo 1: Normalizar os valores RGB
    R = r / 255.0
    G = g / 255.0
    B = b / 255.0
    
    RGB = np.array([R, G, B])

    # Passo 2: Converter para o espaço XYZ
    matrix = np.array([
    [0.49000, 0.31000, 0.20000],
    [0.17697, 0.81240, 0.01063],
    [0.00000, 0.01000, 0.99000]])
    
    X, Y, Z = np.dot(matrix, RGB)

    # Passo 3: Calcular as coordenadas cromáticas (x, y)
    if X + Y + Z == 0:
        return -1

    # Cada coordenada
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    z = Z / (X + Y + Z)

    # Passo 4: Mapear (x, y) para comprimento de onda
    data = np.loadtxt("CIE.csv", delimiter=",")  # Carrega como um numpy array
    w_values = data[:, 0]       # Primeira coluna é w
    coordinates = data[:, 1:]   # Colunas x, y, z

    tree = KDTree(coordinates)

    def encontrar_w_mais_proximo(x, y, z):
        ponto = np.array([x, y, z])
        indice_mais_proximo = tree.query(ponto)[1]  # Índice do ponto mais próximo
        return w_values[indice_mais_proximo]       # Retorna o w correspondente
    
    w = encontrar_w_mais_proximo(x, y, z)
    
    return w

# Exemplo de uso
r, g, b = 0, 0, 0  # cor em RGB
w = rgb_to_wavelength(r, g, b)
print(f"O comprimento de onda aproximado para RGB({r}, {g}, {b}) é: {w} nm")
