import pandas as pd
import matplotlib.pyplot as plt


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        self.root = self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if node is None:
            return Node(data)

        # Insert node recursively
        if self._calculate_metric(data) < self._calculate_metric(node.data):
            node.left = self._insert_recursive(node.left, data)
        elif self._calculate_metric(data) > self._calculate_metric(node.data):
            node.right = self._insert_recursive(node.right, data)
        else:
            if self._calculate_second_metric(data) < self._calculate_second_metric(node.data):
                node.left = self._insert_recursive(node.left, data)
            else:
                node.right = self._insert_recursive(node.right, data)

        # Update balance factor and balance the tree
        node = self._balance_tree(node)

        return node

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


    def _plot_node(self, node, x, y, level):
        # Si el nodo es None, no hay nada que graficar
        if node is None:
            return

        # Calcular la posición x e y del nodo en el gráfico
        x_shift = 100  # Espacio horizontal entre nodos
        y_shift = 80   # Espacio vertical entre niveles del árbol
        node_radius = 30  # Radio del nodo en el gráfico

        # Graficar el nodo actual
        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, color='blue', edgecolors='black', s=node_radius*100)
        plt.text(x, y, str(node.data), ha='center', va='center', color='white', fontsize=12)

        # Graficar las conexiones con los hijos izquierdo y derecho
        if node.left is not None:
            plt.plot([x, x - x_shift], [y, y - y_shift], color='black')
            self._plot_node(node.left, x - x_shift, y - y_shift, level + 1)

        if node.right is not None:
            plt.plot([x, x + x_shift], [y, y - y_shift], color='black')
            self._plot_node(node.right, x + x_shift, y - y_shift, level + 1)

        plt.title('Árbol AVL')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axis('off')
        plt.show()


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
    avl_tree.insert(data)