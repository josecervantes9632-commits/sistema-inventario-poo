# ============================================================
# AVANCE 3 FINAL: COMPOSICIÓN Y MÓDULOS
# Autor: José Gabriel Cervantes Mercado
#
# modelos.py -> definición de todas las clases del
# Sistema de Inventario de Productos:
#   - Proveedor            (clase auxiliar, composición)
#   - Movimiento           (clase auxiliar, composición)
#   - ProductoInventario   (clase base)
#   - ProductoPerecedero   (subclase)
#   - Inventario           (clase contenedora, composición)
# ============================================================

from datetime import date


# ------------------------------------------------------------
# CLASES AUXILIARES PARA COMPOSICIÓN
# ------------------------------------------------------------
class Proveedor:
    """Empresa que surte un producto. Un producto 'tiene-un' proveedor."""

    def __init__(self, nombre, telefono, dias_entrega):
        self.nombre = nombre
        self.telefono = telefono
        self.dias_entrega = dias_entrega

    def contacto(self):
        return f"{self.nombre} (tel. {self.telefono})"

    def fecha_estimada_entrega(self, fecha_pedido):
        return date.fromordinal(fecha_pedido.toordinal() + self.dias_entrega)


class Movimiento:
    """Registro de una entrada o salida de stock."""

    def __init__(self, tipo, cantidad, fecha):
        self.tipo = tipo            # "ENTRADA" o "VENTA"
        self.cantidad = cantidad
        self.fecha = fecha

    def __str__(self):
        signo = "+" if self.tipo == "ENTRADA" else "-"
        return f"{self.fecha.strftime('%d/%m/%Y')}  {self.tipo:<7} {signo}{self.cantidad}"


# ------------------------------------------------------------
# CLASE BASE (Superclase)
# ------------------------------------------------------------
class ProductoInventario:

    def __init__(self, nombre, precio, cantidad, categoria, proveedor):
        self.nombre = nombre
        self.categoria = categoria
        # Encapsulamiento: atributos privados validados por los setters
        self.__precio = 0
        self.__cantidad = 0
        self.precio = precio
        self.cantidad = cantidad
        # COMPOSICIÓN: un producto "tiene-un" Proveedor
        self.proveedor = proveedor
        # COMPOSICIÓN: un producto "tiene" una lista de Movimientos
        self.movimientos = []

    # --- Getter y Setter de precio ---
    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio < 0:
            print(f"Error: el precio de {self.nombre} no puede ser negativo (${nuevo_precio}).")
        else:
            self.__precio = nuevo_precio

    # --- Getter y Setter de cantidad ---
    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        if nueva_cantidad < 0:
            print(f"Error: la cantidad de {self.nombre} no puede ser negativa ({nueva_cantidad}).")
        else:
            self.__cantidad = nueva_cantidad

    # Se sobrescribe en la subclase (polimorfismo)
    def mostrar_informacion(self, fecha_actual=None):
        print(f"Producto: {self.nombre}")
        print(f"Precio: ${self.precio:,.2f}")
        print(f"Cantidad disponible: {self.cantidad}")
        print(f"Categoría: {self.categoria}")
        # Delegación al objeto contenido (Proveedor)
        print(f"Proveedor: {self.proveedor.contacto()}")

    def agregar_stock(self, cantidad, fecha=None):
        if cantidad <= 0:
            print(f"Error: debes agregar al menos 1 unidad de {self.nombre}.")
            return
        self.cantidad += cantidad
        self.movimientos.append(Movimiento("ENTRADA", cantidad, fecha or date.today()))
        print(f"Se agregaron {cantidad} unidades de {self.nombre}. Stock actual: {self.cantidad}")

    def vender_producto(self, cantidad, fecha_actual=None):
        if cantidad <= self.cantidad:
            self.cantidad -= cantidad
            self.movimientos.append(Movimiento("VENTA", cantidad, fecha_actual or date.today()))
            print(f"Se vendieron {cantidad} unidades de {self.nombre}. Stock restante: {self.cantidad}")
        else:
            print(f"No hay suficiente stock de {self.nombre} (pediste {cantidad}, hay {self.cantidad}).")

    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio
        print(f"El precio actual de {self.nombre} es ${self.precio:,.2f}")

    def calcular_valor_total(self):
        return self.precio * self.cantidad

    def solicitar_reabasto(self, fecha_pedido):
        # Delegación: la fecha de entrega la calcula el Proveedor
        llegada = self.proveedor.fecha_estimada_entrega(fecha_pedido)
        return f"Pedido de {self.nombre} a {self.proveedor.nombre}: llega el {llegada.strftime('%d/%m/%Y')}"

    def mostrar_historial(self):
        print(f"Historial de {self.nombre}:")
        if not self.movimientos:
            print("  (sin movimientos)")
        for movimiento in self.movimientos:
            print(f"  {movimiento}")


# ------------------------------------------------------------
# SUBCLASE (Herencia)
# ------------------------------------------------------------
class ProductoPerecedero(ProductoInventario):

    def __init__(self, nombre, precio, cantidad, categoria, proveedor,
                 fecha_caducidad, temperatura_almacenamiento):
        super().__init__(nombre, precio, cantidad, categoria, proveedor)
        self.fecha_caducidad = fecha_caducidad
        self._temperatura_almacenamiento = temperatura_almacenamiento

    def esta_caducado(self, fecha_actual=None):
        return (fecha_actual or date.today()) > self.fecha_caducidad

    def dias_para_caducar(self, fecha_actual=None):
        return (self.fecha_caducidad - (fecha_actual or date.today())).days

    def aplicar_descuento(self, porcentaje):
        if porcentaje <= 0 or porcentaje >= 100:
            print(f"Error: el descuento debe estar entre 1 y 99 % (recibido: {porcentaje} %).")
            return
        precio_anterior = self.precio
        self.precio = round(self.precio * (1 - porcentaje / 100), 2)
        print(f"Descuento de {porcentaje} % en {self.nombre}: ${precio_anterior:,.2f} -> ${self.precio:,.2f}")

    # Polimorfismo: agrega los datos de caducidad
    def mostrar_informacion(self, fecha_actual=None):
        super().mostrar_informacion()
        dias = self.dias_para_caducar(fecha_actual)
        print(f"Caduca el: {self.fecha_caducidad.strftime('%d/%m/%Y')}")
        print(f"Almacenar a: {self._temperatura_almacenamiento} °C")
        if self.esta_caducado(fecha_actual):
            print(f"Estado: CADUCADO (hace {abs(dias)} días)")
        else:
            print(f"Estado: vigente (faltan {dias} días)")

    # Polimorfismo: no se vende un producto caducado
    def vender_producto(self, cantidad, fecha_actual=None):
        if self.esta_caducado(fecha_actual):
            print(f"No se puede vender {self.nombre}: el producto está caducado.")
        else:
            super().vender_producto(cantidad, fecha_actual)


# ------------------------------------------------------------
# CLASE CONTENEDORA (Composición)
# ------------------------------------------------------------
class Inventario:
    """Una tienda 'tiene' un inventario, que 'tiene' muchos productos."""

    def __init__(self, nombre_tienda):
        self.nombre_tienda = nombre_tienda
        self.__productos = []       # composición + encapsulamiento

    def agregar_producto(self, producto):
        self.__productos.append(producto)

    def buscar(self, nombre):
        for producto in self.__productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None

    def vender(self, nombre, cantidad, fecha_actual=None):
        # Delegación: el inventario le pide al producto que se venda
        producto = self.buscar(nombre)
        if producto is None:
            print(f"El producto '{nombre}' no está en el inventario.")
        else:
            producto.vender_producto(cantidad, fecha_actual)

    def valor_total(self):
        return sum(p.calcular_valor_total() for p in self.__productos)

    def productos_por_caducar(self, fecha_actual, dias=7):
        return [p for p in self.__productos
                if isinstance(p, ProductoPerecedero) and 0 <= p.dias_para_caducar(fecha_actual) <= dias]

    def reporte(self, fecha_actual=None):
        print(f"===== Inventario de {self.nombre_tienda} =====")
        for producto in self.__productos:
            print(f"\n[{type(producto).__name__}]")
            producto.mostrar_informacion(fecha_actual)   # polimorfismo
        print(f"\nValor total del inventario: ${self.valor_total():,.2f}")

    def __len__(self):
        return len(self.__productos)
