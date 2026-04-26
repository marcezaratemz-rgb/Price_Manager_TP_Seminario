# -*- coding: utf-8 -*-
"""Módulo para precargar datos iniciales en el sistema Price Manager.

Contiene funciones para leer datos desde archivos CSV y poblar
los repositorios del sistema con las entidades correspondientes.
"""

import csv
import datetime
from typing import Dict

from price_manager.entities.entities import (
  Categoria, Proveedor, Moneda, TipoCotizacion,
  Precio, Producto, CotizacionDolar, Stock
)
from price_manager.services.services import (
  ServicioCategoria, ServicioProveedor, ServicioMoneda,
  ServicioTipoCotizacion, ServicioProducto, ServicioStock,
  ServicioCotizacionDolar
)

def importar_datos_por_defecto(servicios: Dict):
  """Importa datos iniciales desde archivos CSV a los servicios correspondientes.

  Args:
      servicios (Dict): Diccionario de servicios del sistema.
  """
  print("⚙️  Iniciando precarga de datos por defecto...")

  srv_cat: ServicioCategoria = servicios["categoria"]
  srv_prov: ServicioProveedor = servicios["proveedor"]
  srv_mon: ServicioMoneda = servicios["moneda"]
  srv_tipo_cot: ServicioTipoCotizacion = servicios["tipo_cotizacion"]
  srv_prod: ServicioProducto = servicios["producto"]
  srv_stock: ServicioStock = servicios["stock"]
  srv_cot: ServicioCotizacionDolar = servicios["cotizacion_dolar"]

  # Limpiar repositorios antes de cargar para evitar duplicados en tests
  # (Esto es útil para un ciclo de desarrollo, en producción se manejaría distinto)
  # NOTE: Para el TP, no se nos pidió un método de 'limpiar todo', así que omitimos esto.

  # 1. Cargar Categorias
  with open('/content/price_manager/src/price_manager/migrations/csv/categorias.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      try:
        srv_cat.crear(
          Categoria(id=int(row['id']), nombre=row['nombre'])
        )
      except ValueError:
        pass # Ya existe, ignorar
  print("  ✅ Categorías cargadas.")

  # 2. Cargar Proveedores
  with open('/content/price_manager/src/price_manager/migrations/csv/proveedores.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      try:
        srv_prov.crear(
          Proveedor(id=int(row['id']), nombre=row['nombre'], contacto=row['contacto'])
        )
      except ValueError:
        pass
  print("  ✅ Proveedores cargados.")

  # 3. Cargar Monedas
  with open('/content/price_manager/src/price_manager/migrations/csv/monedas.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      try:
        srv_mon.crear(
          Moneda(id=int(row['id']), nombre=row['nombre'])
        )
      except ValueError:
        pass
  print("  ✅ Monedas cargadas.")

  # 4. Cargar Tipos de Cotización
  with open('/content/price_manager/src/price_manager/migrations/csv/tipo_cotizaciones.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      try:
        srv_tipo_cot.crear(
          TipoCotizacion(id=int(row['id']), nombre=row['nombre'])
        )
      except ValueError:
        pass
  print("  ✅ Tipos de Cotización cargados.")

  # 5. Cargar Cotizaciones (depende de TipoCotizacion)
  with open('/content/price_manager/src/price_manager/migrations/csv/cotizaciones.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      try:
        tipo = srv_tipo_cot.obtener(int(row['tipo_id']))
        fecha = datetime.datetime.strptime(row['fecha'], '%Y-%m-%d').date()
        srv_cot.registrar_cotizacion(
          CotizacionDolar(valor=float(row['valor']), fecha=fecha, tipo=tipo)
        )
      except ValueError:
        pass
  print("  ✅ Cotizaciones de Dólar cargadas.")

  # 6. Cargar Productos (depende de Moneda, Categoria, Proveedor)
  with open('/content/price_manager/src/price_manager/migrations/csv/productos.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      try:
        moneda = srv_mon.obtener(int(row['precio_moneda_id']))
        categoria = srv_cat.obtener(int(row['categoria_id']))
        proveedor = srv_prov.obtener(int(row['proveedor_id']))
        fecha_precio = datetime.datetime.strptime(row['precio_fecha'], '%Y-%m-%d').date()

        precio = Precio(
          valor=float(row['precio_valor']), moneda=moneda, fecha=fecha_precio
        )
        srv_prod.crear(
          Producto(
            id=int(row['id']), nombre=row['nombre'], descripcion=row['descripcion'],
            precio=precio, categoria=categoria, proveedor=proveedor
          )
        )
      except ValueError:
        pass
  print("  ✅ Productos cargados.")

  # 7. Cargar Stock (depende de Producto)
  with open('/content/price_manager/src/price_manager/migrations/csv/stocks.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      try:
        # Asumimos que al registrar movimiento, si no hay stock, lo crea en 0 y luego suma
        # Para la precarga, simplemente registramos el movimiento inicial.
        srv_stock.registrar_movimiento(int(row['producto_id']), int(row['cantidad']))
      except ValueError:
        pass
  print("  ✅ Stocks cargados.")

  print("✅ Precarga de datos completada.")
