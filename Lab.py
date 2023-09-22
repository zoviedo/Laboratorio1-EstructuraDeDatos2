import matplotlib.pyplot as plt
import pandas as pd
import folium
from collections import deque

class Node:
    def __init__(self, data, metric):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1
        self.metric = metric

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        self.root = self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if node is None:
            metric = self._calculate_metric(data)
            return Node(data, metric)

        # Insert node recursively
        if self._calculate_metric(data) < self._calculate_metric(node.data):
            node.left = self._insert_recursive(node.left, data)

        elif self._calculate_metric(data) > self._calculate_metric(node.data):
            node.right = self._insert_recursive(node.right, data)
        else:
            if self._calculate_second_metric(data) < self._calculate_metric(node.data):
                node.left = self._insert_recursive(node.left, data)
            else:
                node.right = self._insert_recursive(node.right, data)

        # Update balance factor and balance the tree
        node = self._balance_tree(node)

        return node

    def _encontrar_predecesor(self, nodo_actual):
        while nodo_actual.right is not None:
            nodo_actual = nodo_actual.right
        return nodo_actual

    def eliminar_nodo_por_metrica(self, metrica):
        self.root = self._eliminar_nodo_por_metrica_recursive(self.root, metrica)

    def _eliminar_nodo_por_metrica_recursive(self, nodo_actual, metrica1, metrica2):
        # Caso base: si el nodo actual es None, retorna None
        if nodo_actual is None:
            return None

        # Comparar las métricas del nodo actual con las métricas dadas y determinar si se debe eliminar el nodo
        if (self._calculate_metric(nodo_actual.data) == metrica1 and
                self._calculate_second_metric(nodo_actual.data) == metrica2):
            # Caso 1: El nodo a eliminar es una hoja (no tiene hijos)
            if nodo_actual.left is None and nodo_actual.right is None:
                return None

            # Caso 2: El nodo a eliminar tiene un solo hijo
            if nodo_actual.left is None:
                return nodo_actual.right
            if nodo_actual.right is None:
                return nodo_actual.left

            # Caso 3: El nodo a eliminar tiene dos hijos
            # Encuentra el nodo predecesor (el nodo más grande en el subárbol izquierdo)
            predecesor = self._encontrar_predecesor(nodo_actual.left)

            # Reemplaza el valor del nodo a eliminar con el valor del predecesor
            nodo_actual.data = predecesor.data

            # Elimina el predecesor del subárbol izquierdo
            nodo_actual.left = self._eliminar_nodo_por_metrica_recursive(nodo_actual.left, self._calculate_metric(predecesor.data), self._calculate_second_metric(predecesor.data))
        elif (self._calculate_metric(nodo_actual.data) > metrica1 or
              (self._calculate_metric(nodo_actual.data) == metrica1 and
               self._calculate_second_metric(nodo_actual.data) > metrica2)):
            nodo_actual.left = self._eliminar_nodo_por_metrica_recursive(nodo_actual.left, metrica1, metrica2)
        else:
            nodo_actual.right = self._eliminar_nodo_por_metrica_recursive(nodo_actual.right, metrica1, metrica2)

        # Equilibrar el árbol AVL después de realizar las eliminaciones
        nodo_actual = self._balance_tree(nodo_actual)

        return nodo_actual

    def insertar_nodo_manual(self):
        # Pedir los datos al usuario
        data = {}
        data['title'] = input("Ingrese el título: ")
        data['department'] = input("Ingrese el departamento: ")
        data['city'] = input("Ingrese la ciudad: ")
        data['property_type'] = input("Ingrese el tipo de propiedad: ")

        # Validar los parámetros
        if not isinstance(data['title'], str) or len(data['title']) == 0:
            print("El título no es válido.")
            return

        if not isinstance(data['department'], str) or len(data['department']) == 0:
            print("El departamento no es válido.")
            return

        if not isinstance(data['city'], str) or len(data['city']) == 0:
            print("La ciudad no es válida.")
            return

        if not isinstance(data['property_type'], str) or len(data['property_type']) == 0:
            print("El tipo de propiedad no es válido.")
            return

        data['latitude'] = float(input("Ingrese la latitud: "))
        data['longitude'] = float(input("Ingrese la longitud: "))

        if not isinstance(data['latitude'], float) or data['latitude'] < -90 or data['latitude'] > 90:
            print("La latitud no es válida.")
            return

        if not isinstance(data['longitude'], float) or data['longitude'] < -180 or data['longitude'] > 180:
            print("La longitud no es válida.")
            return

        data['surface_total'] = float(input("Ingrese la superficie total: "))
        data['surface_covered'] = float(input("Ingrese la superficie cubierta: "))

        if not isinstance(data['surface_total'], float) or data['surface_total'] <= 0:
            print("La superficie total no es válida.")
            return

        if not isinstance(data['surface_covered'], float) or data['surface_covered'] <= 0 or data['surface_covered'] > \
                data['surface_total']:
            print("La superficie cubierta no es válida.")
            return

        data['bedrooms'] = int(input("Ingrese el número de dormitorios: "))
        data['bathrooms'] = int(input("Ingrese el número de baños: "))

        if not isinstance(data['bedrooms'], int) or data['bedrooms'] < 0:
            print("El número de dormitorios no es válido.")
            return

        if not isinstance(data['bathrooms'], int) or data['bathrooms'] < 0:
            print("El número de baños no es válido.")
            return

        data['operation_type'] = input("Ingrese el tipo de operación: ")

        if not isinstance(data['operation_type'], str) or len(data['operation_type']) == 0:
            print("El tipo de operación no es válido.")
            return

        data['price'] = float(input("Ingrese el precio: "))

        if not isinstance(data['price'], float) or data['price'] <= 0:
            print("El precio no es válido.")
            return

        # Insertar el nodo en el árbol AVL
        AVLTree.insert(data)

    def _calculate_metric(self, data):
        price = data['price']
        surface_total = data['surface_total']
        metric = price / surface_total
        return metric

    def _calculate_second_metric(self, data):
        bedrooms = data['bedrooms']
        bathrooms = data['bathrooms']
        second_metric = bedrooms * 0.5 + bathrooms * 0.5
        return second_metric

    def _balance_tree(self, node):
        # Actualizar la altura del nodo
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Calcular el factor de equilibrio del nodo
        balance_factor = self._get_balance_factor(node)

        # Caso de desequilibrio a la izquierda-izquierda
        if balance_factor > 1 and self._get_balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        # Caso de desequilibrio a la derecha-derecha
        if balance_factor < -1 and self._get_balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        # Caso de desequilibrio a la izquierda-derecha
        if balance_factor > 1 and self._get_balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso de desequilibrio a la derecha-izquierda
        if balance_factor < -1 and self._get_balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _get_balance_factor(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        # Realizar rotación
        y.right = z
        z.left = T3

        # Actualizar alturas
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        # Realizar rotación
        y.left = z
        z.right = T2

        # Actualizar alturas
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def recorrer_por_nivel(self):
        if self.root is None:
            return

        queue = deque()
        queue.append(self.root)

        while queue:
            node = queue.popleft()
            print(node.data, end=" ")

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

    def plot_tree(self):
        if self.root is not None:
            plt.figure(figsize=(10, 6))
            self._plot_node(self.root, 0, 0, 1)
            plt.title('Árbol AVL')
            plt.axis('off')
            plt.show()

    def _plot_node(self, node, x, y, level):
        if node is not None:
            # Espaciado entre nodos y niveles
            x_spacing = 100000  # Aumenta este valor para un espaciado horizontal más amplio
            y_spacing = 100000  # Aumenta este valor para un espaciado vertical más amplio

            # Dibujar el nodo actual
            plt.scatter(x, y, color='pink', edgecolors='black', s=1000)
            plt.text(x, y, str(node.metric), ha='center', va='center', color='black', fontsize=10)

            # Calcular las coordenadas de los hijos
            x_left = x - x_spacing * 2 ** (5 - level)
            x_right = x + x_spacing * 2 ** (5 - level)
            y_next = y - y_spacing

            # Dibujar las conexiones con los hijos
            if node.left is not None:
                plt.plot([x, x_left], [y, y_next], color='black')
                self._plot_node(node.left, x_left, y_next, level + 1)

            if node.right is not None:
                plt.plot([x, x_right], [y, y_next], color='black')
                self._plot_node(node.right, x_right, y_next, level + 1)



AVLTree = AVLTree()
df = pd.read_csv('co_properties_final.csv')
# Insertar cada registro del DataFrame en el árbol
for _, row in df.iterrows():
    data = {
        'title': row['title'],
        'department': row['department'],
        'city': row['city'],
        'property_type': row['property_type'],
        'latitude': row['latitude'],
        'longitude': row['longitude'],
        'surface_total': row['surface_total'],
        'surface_covered': row['surface_covered'],
        'bedrooms': row['bedrooms'],
        'bathrooms': row['bathrooms'],
        'operation_type': row['operation_type'],
        'price': row['price']
    }
    AVLTree.insert(data)

AVLTree.plot_tree()

