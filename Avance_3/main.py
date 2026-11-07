# ============================================================
# AVANCE 3 FINAL: COMPOSICIÓN Y MÓDULOS
# Autor: José Gabriel Cervantes Mercado
#
# main.py -> solo importaciones, creación de objetos y pruebas.
# ============================================================

from datetime import date

from modelos import Inventario, Proveedor, ProductoInventario, ProductoPerecedero

# Fecha fija para que la salida siempre sea la misma
hoy = date(2026, 11, 6)

# --- Objetos auxiliares (componentes) ---
lala = Proveedor("Lala", "33-1234-5678", 2)
techmx = Proveedor("TechMX", "33-8765-4321", 5)

# --- Productos (herencia) ---
laptop = ProductoInventario("Laptop", 15000, 5, "Tecnología", techmx)
leche = ProductoPerecedero("Leche entera 1 L", 28.50, 40, "Lácteos", lala, date(2026, 11, 10), 4)
yogurt = ProductoPerecedero("Yogurt natural", 19.90, 15, "Lácteos", lala, date(2026, 11, 1), 4)

# --- Contenedor (composición) ---
tienda = Inventario("Abarrotes Cervantes")
for producto in (laptop, leche, yogurt):
    tienda.agregar_producto(producto)

print("========== 1. REPORTE INICIAL (polimorfismo) ==========")
tienda.reporte(hoy)

print("\n========== 2. ENCAPSULAMIENTO ==========")
laptop.precio = -500
laptop.cantidad = -3
print(f"Precio y cantidad siguen válidos: ${laptop.precio:,.2f} | {laptop.cantidad}")
try:
    print(laptop.__precio)
except AttributeError:
    print("No se puede leer laptop.__precio desde fuera (atributo privado).")

print("\n========== 3. HERENCIA Y POLIMORFISMO ==========")
leche.aplicar_descuento(15)                 # método propio de la subclase
tienda.vender("Leche entera 1 L", 10, hoy)   # vigente: sí se vende
tienda.vender("Yogurt natural", 5, hoy)      # caducado: no se vende
tienda.vender("Laptop", 10, hoy)             # sin stock suficiente
tienda.vender("Refresco", 1, hoy)            # no existe en el inventario

print("\n========== 4. COMPOSICIÓN (delegación) ==========")
# Método del objeto contenido (Proveedor) llamado a través del producto
print(laptop.solicitar_reabasto(hoy))
print(leche.solicitar_reabasto(hoy))
print(f"Contacto del proveedor de la leche: {leche.proveedor.contacto()}")
# Movimientos guardados dentro del producto
laptop.agregar_stock(3, hoy)
tienda.vender("Laptop", 2, hoy)
laptop.mostrar_historial()
leche.mostrar_historial()
# El inventario contiene los productos
por_caducar = tienda.productos_por_caducar(hoy)
print(f"Productos por caducar en 7 días: {[p.nombre for p in por_caducar]}")
print(f"Productos en el inventario: {len(tienda)}")

print("\n========== 5. INVENTARIO FINAL ==========")
for producto in (laptop, leche, yogurt):
    print(f"{producto.nombre:<18} | Precio: ${producto.precio:>10,.2f} | "
          f"Stock: {producto.cantidad:>3} | Valor: ${producto.calcular_valor_total():>10,.2f}")
print(f"Valor total de {tienda.nombre_tienda}: ${tienda.valor_total():,.2f}")
