# ============================================================
# AVANCE 2: HERENCIA, ENCAPSULAMIENTO Y DIAGRAMA UML
# Autor: José Gabriel Cervantes Mercado
#
# Sistema de Inventario de Productos.
# Registra los productos de una tienda, controla su stock
# (entradas y ventas) y su precio. En este avance:
#   - Se protegen el precio y la cantidad con atributos privados
#     y @property para no aceptar valores negativos.
#   - Se crea la subclase ProductoPerecedero, que hereda de
#     ProductoInventario y agrega fecha de caducidad y temperatura
#     de almacenamiento.
# ============================================================

from datetime import date


# ------------------------------------------------------------
# Creación de la clase base (Superclase)
# ------------------------------------------------------------
class ProductoInventario:

    def __init__(self, nombre, precio, cantidad, categoria):
        self.nombre = nombre
        self.categoria = categoria
        # Aplicación de Encapsulamiento: atributos privados (doble guion bajo).
        # Se asignan a través de los setters para que pasen por la validación.
        self.__precio = 0
        self.__cantidad = 0
        self.precio = precio
        self.cantidad = cantidad

    # --- Getter y Setter de precio (@property) ---
    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, nuevo_precio):
        # Validación: el precio no puede ser negativo
        if nuevo_precio < 0:
            print(f"Error: el precio de {self.nombre} no puede ser negativo (${nuevo_precio}).")
        else:
            self.__precio = nuevo_precio

    # --- Getter y Setter de cantidad (@property) ---
    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        # Validación: el stock no puede quedar en negativo
        if nueva_cantidad < 0:
            print(f"Error: la cantidad de {self.nombre} no puede ser negativa ({nueva_cantidad}).")
        else:
            self.__cantidad = nueva_cantidad

    # Método 1: consultar los datos del producto
    # (será sobrescrito en la subclase -> Polimorfismo)
    def mostrar_informacion(self):
        print(f"Producto: {self.nombre}")
        print(f"Precio: ${self.precio:,.2f}")
        print(f"Cantidad disponible: {self.cantidad}")
        print(f"Categoría: {self.categoria}")

    # Método 2: sumar unidades al inventario
    def agregar_stock(self, cantidad):
        if cantidad <= 0:
            print(f"Error: debes agregar al menos 1 unidad de {self.nombre}.")
            return
        self.cantidad += cantidad
        print(f"Se agregaron {cantidad} unidades de {self.nombre}.")
        print(f"Stock actual: {self.cantidad}")

    # Método 3: vender solo si hay stock suficiente
    def vender_producto(self, cantidad):
        if cantidad <= self.cantidad:
            self.cantidad -= cantidad
            print(f"Se vendieron {cantidad} unidades de {self.nombre}.")
            print(f"Stock restante: {self.cantidad}")
        else:
            print(f"No hay suficiente stock de {self.nombre} (pediste {cantidad}, hay {self.cantidad}).")

    # Método 4: cambiar el precio (usa el setter, así que también se valida)
    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio
        print(f"El precio actual de {self.nombre} es ${self.precio:,.2f}")

    # Método 5: valor total del producto en inventario
    def calcular_valor_total(self):
        return self.precio * self.cantidad


# ------------------------------------------------------------
# Uso de super() y Herencia (Subclase)
# ------------------------------------------------------------
class ProductoPerecedero(ProductoInventario):

    def __init__(self, nombre, precio, cantidad, categoria, fecha_caducidad, temperatura_almacenamiento):
        # super() reutiliza el constructor de la clase padre
        # (nombre, precio, cantidad y categoría, con sus validaciones)
        super().__init__(nombre, precio, cantidad, categoria)
        # Atributos nuevos propios de la subclase
        self.fecha_caducidad = fecha_caducidad                      # público
        self._temperatura_almacenamiento = temperatura_almacenamiento  # protegido

    # Método propio: saber si el producto ya caducó
    def esta_caducado(self, fecha_actual=None):
        if fecha_actual is None:
            fecha_actual = date.today()
        return fecha_actual > self.fecha_caducidad

    # Método propio: días que faltan para que caduque
    def dias_para_caducar(self, fecha_actual=None):
        if fecha_actual is None:
            fecha_actual = date.today()
        return (self.fecha_caducidad - fecha_actual).days

    # Método propio: rebajar el precio cuando está por caducar
    def aplicar_descuento(self, porcentaje):
        if porcentaje <= 0 or porcentaje >= 100:
            print(f"Error: el descuento debe estar entre 1 y 99 % (recibido: {porcentaje} %).")
            return
        precio_anterior = self.precio
        self.precio = round(self.precio * (1 - porcentaje / 100), 2)
        print(f"Descuento de {porcentaje} % en {self.nombre}: ${precio_anterior:,.2f} -> ${self.precio:,.2f}")

    # Sobrescritura de métodos (Polimorfismo):
    # extiende mostrar_informacion() del padre con los datos de caducidad
    def mostrar_informacion(self, fecha_actual=None):
        super().mostrar_informacion()
        dias = self.dias_para_caducar(fecha_actual)
        print(f"Caduca el: {self.fecha_caducidad.strftime('%d/%m/%Y')}")
        print(f"Almacenar a: {self._temperatura_almacenamiento} °C")
        if self.esta_caducado(fecha_actual):
            print(f"Estado: CADUCADO (hace {abs(dias)} días)")
        else:
            print(f"Estado: vigente (faltan {dias} días)")

    # Sobrescritura de métodos (Polimorfismo):
    # no se permite vender un producto caducado
    def vender_producto(self, cantidad, fecha_actual=None):
        if self.esta_caducado(fecha_actual):
            print(f"No se puede vender {self.nombre}: el producto está caducado.")
        else:
            super().vender_producto(cantidad)


# ============================================================
# Instanciación y pruebas
# ============================================================
# Se usa una fecha fija para que el resultado sea siempre el mismo
hoy = date(2026, 10, 17)

# 1 objeto de la clase base y 2 de la subclase
laptop = ProductoInventario("Laptop", 15000, 5, "Tecnología")
leche = ProductoPerecedero("Leche entera 1 L", 28.50, 40, "Lácteos", date(2026, 10, 25), 4)
yogurt = ProductoPerecedero("Yogurt natural", 19.90, 15, "Lácteos", date(2026, 10, 10), 4)

print("========== INVENTARIO INICIAL ==========")
print("\n----- PRODUCTO 1 (clase base) -----")
laptop.mostrar_informacion()
print("\n----- PRODUCTO 2 (subclase) -----")
leche.mostrar_informacion(hoy)
print("\n----- PRODUCTO 3 (subclase) -----")
yogurt.mostrar_informacion(hoy)

# --- Prueba de Encapsulamiento ---
print("\n========== PRUEBA DE ENCAPSULAMIENTO ==========")
print(f"Precio de la laptop consultado con el getter: ${laptop.precio:,.2f}")
laptop.precio = -500          # el setter rechaza el valor negativo
laptop.cantidad = -3          # el setter rechaza la cantidad negativa
print(f"Después del intento, precio: ${laptop.precio:,.2f} | cantidad: {laptop.cantidad}")
laptop.actualizar_precio(14500)   # valor válido: sí se actualiza
# El atributo privado no se puede leer directamente desde fuera
try:
    print(laptop.__precio)
except AttributeError:
    print("No se puede acceder a laptop.__precio desde fuera de la clase (atributo privado).")

# --- Prueba de Herencia y método sobrescrito ---
print("\n========== PRUEBA DE HERENCIA Y POLIMORFISMO ==========")
leche.agregar_stock(20)           # método heredado sin cambios
leche.aplicar_descuento(15)       # método propio de la subclase
leche.vender_producto(10, hoy)    # método sobrescrito: está vigente, sí vende
yogurt.vender_producto(5, hoy)    # método sobrescrito: está caducado, no vende
laptop.vender_producto(10)        # método de la clase base: no hay stock suficiente

# El mismo llamado mostrar_informacion() se comporta distinto según el tipo de objeto
print("\n----- Mismo método, distinto comportamiento -----")
for producto in [laptop, leche]:
    print(f"\n[{type(producto).__name__}]")
    producto.mostrar_informacion()

# --- Independencia de los datos entre instancias (self) ---
print("\n========== INVENTARIO FINAL ==========")
for producto in [laptop, leche, yogurt]:
    print(f"{producto.nombre:<18} | Precio: ${producto.precio:>10,.2f} | "
          f"Stock: {producto.cantidad:>3} | Valor total: ${producto.calcular_valor_total():>10,.2f}")
