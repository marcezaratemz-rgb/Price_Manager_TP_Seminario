# -*- coding: utf-8 -*-
"""Módulo de interfaz de usuario para el sistema Price Manager.

Provee una interfaz de consola (CLI) interactiva para operar el sistema.
"""

import datetime
from price_manager.entities.entities import Categoria, Proveedor, Producto, Precio, CotizacionDolar

class ConsoleUI:
  """Consola interactiva del sistema Price Manager."""

  def __init__(self, servicios: dict):
    self.servicios = servicios

  def mostrar_menu_principal(self):
    print("\n" + "="*45)
    print("💻 PRICE MANAGER v1.1 - STAR COMPUTACIÓN 💻")
    print("="*45)
    print("1. 📦 Gestión de Productos")
    print("2. 🏷️  Gestión de Categorías")
    print("3. 🏢 Gestión de Proveedores")
    print("4. 📉 Gestión de Cotizaciones (Dólar)")
    print("5. ➕ Gestión de Stock (Entradas/Salidas)")
    print("6. ❌ Salir")
    print("="*45)

  def run(self):
    print("🚀 Iniciando Módulo de Consola UI...")
    try:
      while True:
        self.mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
          self._menu_productos()
        elif opcion == "2":
          self._menu_categorias()
        elif opcion == "3":
          self._menu_proveedores()
        elif opcion == "4":
          self._registrar_dolar()
        elif opcion == "5":
          self._registrar_stock()
        elif opcion == "6":
          print("\n👋 Saliendo del sistema... ¡Hasta pronto!\n")
          break
        else:
          print("\n⚠️ Opción no válida. Intente nuevamente.")
    except KeyboardInterrupt:
      print("\n👋 Interrupción detectada. Saliendo del sistema... ¡Hasta pronto!\n")

  # ==========================================================
  # GESTIÓN DE PRODUCTOS
  # ==========================================================
  def _menu_productos(self):
    while True:
      print("\n--- GESTIÓN DE PRODUCTOS ---")
      print("1. Listar Productos")
      print("2. Alta de Producto")
      print("3. Baja de Producto")
      print("4. Modificar Producto (Precio/Nombre)")
      print("5. Volver al menú principal")

      op = input("Seleccione: ")
      if op == "1": self._listar_productos()
      elif op == "2": self._alta_producto()
      elif op == "3": self._baja_producto()
      elif op == "4": self._modificar_producto()
      elif op == "5": break

  def _listar_productos(self):
    productos = self.servicios["producto"].listar_todos()
    if not productos:
      print("\n🚨 No hay productos cargados.")
      return
    print("\n" + "-"*60)
    print(f"{'ID':<5} | {'Nombre':<25} | {'Categoría':<15} | {'Precio':<10}")
    print("-"*60)
    for p in productos:
      print(f"{p.id:<5} | {p.nombre[:25]:<25} | {p.categoria.nombre[:15]:<15} | ${p.precio.valor:>8.2f}")
    print("-"*60)

  def _alta_producto(self):
    try:
      id_p = int(input("ID del nuevo producto: "))
      nombre = input("Nombre: ")
      desc = input("Descripción: ")
      valor = float(input("Precio inicial: "))

      self._listar_monedas()
      mon_id = int(input("ID de la Moneda: "))
      moneda = self.servicios["moneda"].obtener(mon_id)

      self._listar_categorias()
      cat_id = int(input("ID de la Categoría: "))
      categoria = self.servicios["categoria"].obtener(cat_id)

      self._listar_proveedores()
      prov_id = int(input("ID del Proveedor: "))
      proveedor = self.servicios["proveedor"].obtener(prov_id)

      precio = Precio(valor=valor, moneda=moneda, fecha=datetime.date.today())
      nuevo = Producto(id=id_p, nombre=nombre, descripcion=desc, precio=precio, categoria=categoria, proveedor=proveedor)

      self.servicios["producto"].crear(nuevo)
      print("✅ Producto creado exitosamente.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  def _baja_producto(self):
    try:
      id_p = int(input("ID del producto a eliminar: "))
      self.servicios["producto"].eliminar(id_p)
      print("✅ Producto eliminado.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  def _modificar_producto(self):
    try:
      id_p = int(input("ID del producto a modificar: "))
      p = self.servicios["producto"].obtener(id_p)
      print(f"Modificando: {p.nombre}")

      p.nombre = input(f"Nuevo nombre [{p.nombre}]: ") or p.nombre
      nuevo_valor = input(f"Nuevo precio [{p.precio.valor}]: ")
      if nuevo_valor:
        p.precio = Precio(valor=float(nuevo_valor), moneda=p.precio.moneda, fecha=datetime.date.today())

      self.servicios["producto"].actualizar(p)
      print("✅ Producto actualizado.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  # ==========================================================
  # GESTIÓN DE CATEGORÍAS
  # ==========================================================
  def _menu_categorias(self):
    while True:
      print("\n--- GESTIÓN DE CATEGORÍAS ---")
      print("1. Listar Categorías")
      print("2. Alta de Categoría")
      print("3. Baja de Categoría")
      print("4. Modificar Categoría")
      print("5. Volver")

      op = input("Seleccione: ")
      if op == "1": self._listar_categorias()
      elif op == "2": self._alta_categoria()
      elif op == "3": self._baja_categoria()
      elif op == "4": self._modificar_categoria()
      elif op == "5": break

  def _listar_categorias(self):
    cats = self.servicios["categoria"].listar_todos()
    print("\n--- CATEGORÍAS ---")
    for c in cats:
      print(f"[{c.id}] {c.nombre}")

  def _alta_categoria(self):
    try:
      id_c = int(input("ID: "))
      nom = input("Nombre: ")
      self.servicios["categoria"].crear(Categoria(id=id_c, nombre=nom))
      print("✅ Categoría creada.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  def _baja_categoria(self):
    try:
      id_c = int(input("ID a eliminar: "))
      self.servicios["categoria"].eliminar(id_c)
      print("✅ Categoría eliminada.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  def _modificar_categoria(self):
    try:
      id_c = int(input("ID a modificar: "))
      c = self.servicios["categoria"].obtener(id_c)
      c.nombre = input(f"Nuevo nombre [{c.nombre}]: ") or c.nombre
      self.servicios["categoria"].actualizar(c)
      print("✅ Categoría actualizada.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  # ==========================================================
  # GESTIÓN DE PROVEEDORES
  # ==========================================================
  def _menu_proveedores(self):
    while True:
      print("\n--- GESTIÓN DE PROVEEDORES ---")
      print("1. Listar Proveedores")
      print("2. Alta de Proveedor")
      print("3. Baja de Proveedor")
      print("4. Modificar Proveedor")
      print("5. Volver")

      op = input("Seleccione: ")
      if op == "1": self._listar_proveedores()
      elif op == "2": self._alta_proveedor()
      elif op == "3": self._baja_proveedor()
      elif op == "4": self._modificar_proveedor()
      elif op == "5": break

  def _listar_proveedores(self):
    provs = self.servicios["proveedor"].listar_todos()
    print("\n--- PROVEEDORES ---")
    for p in provs:
      print(f"[{p.id}] {p.nombre} - Contacto: {p.contacto}")

  def _alta_proveedor(self):
    try:
      id_p = int(input("ID: "))
      nom = input("Nombre: ")
      cont = input("Contacto: ")
      self.servicios["proveedor"].crear(Proveedor(id=id_p, nombre=nom, contacto=cont))
      print("✅ Proveedor creado.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  def _baja_proveedor(self):
    try:
      id_p = int(input("ID a eliminar: "))
      self.servicios["proveedor"].eliminar(id_p)
      print("✅ Proveedor eliminado.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  def _modificar_proveedor(self):
    try:
      id_p = int(input("ID a modificar: "))
      p = self.servicios["proveedor"].obtener(id_p)
      p.nombre = input(f"Nuevo nombre [{p.nombre}]: ") or p.nombre
      p.contacto = input(f"Nuevo contacto [{p.contacto}]: ") or p.contacto
      self.servicios["proveedor"].actualizar(p)
      print("✅ Proveedor actualizado.")
    except Exception as e:
      print(f"⚠️ Error: {e}")

  # ==========================================================
  # AUXILIARES Y OTROS
  # ==========================================================
  def _listar_monedas(self):
    mons = self.servicios["moneda"].listar_todos()
    for m in mons: print(f"[{m.id}] {m.nombre}")

  def _listar_categorias(self):
    cats = self.servicios["categoria"].listar_todos()
    for c in cats: print(f"[{c.id}] {c.nombre}")

  def _listar_proveedores(self):
    provs = self.servicios["proveedor"].listar_todos()
    for p in provs: print(f"[{p.id}] {p.nombre}")

  def _registrar_dolar(self):
    print("\n--- REGISTRO DE COTIZACIÓN ---")
    for tc in self.servicios["tipo_cotizacion"].listar_todos():
       print(f"[{tc.id}] {tc.nombre}")
    try:
      tipo_id = int(input("\nID del Tipo: "))
      tipo = self.servicios["tipo_cotizacion"].obtener(tipo_id)
      valor = float(input(f"Valor para '{tipo.nombre}': "))
      self.servicios["cotizacion_dolar"].registrar_cotizacion(CotizacionDolar(valor=valor, fecha=datetime.date.today(), tipo=tipo))
      print("✅ Cotización registrada.")
    except Exception as e: print(f"⚠️ Error: {e}")

  def _registrar_stock(self):
    try:
      p_id = int(input("\nID del producto: "))
      producto = self.servicios["producto"].obtener(p_id)
      stock_actual = self.servicios['stock'].obtener_stock(p_id)
      print(f"Operando: {producto.nombre} (Stock: {stock_actual})")
      mov = int(input("Movimiento (+ entradas, - salidas): "))
      nuevo = self.servicios["stock"].registrar_movimiento(p_id, mov)
      print(f"✅ Stock actualizado: {nuevo}")
    except Exception as e: print(f"⚠️ Error: {e}")
