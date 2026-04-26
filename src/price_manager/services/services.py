# -*- coding: utf-8 -*-
"""Módulo de servicios para el sistema Price Manager.

Contiene la lógica de negocio del sistema, la
interacción entre las entidades y los repositorios.
"""

from typing import List, Optional
import datetime

# Importamos las entidades
from price_manager.entities.entities import (
  Categoria, Proveedor, Moneda, TipoCotizacion,
  Precio, Producto, CotizacionDolar, Stock
)

# Importamos las abstracciones de los repositorios
from price_manager.repositories.repositories import (
  IRepositorio, IRepositorioStock, IRepositorioCotizacionDolar,
  RepositorioCategoria, RepositorioProveedor, RepositorioMoneda,
  RepositorioTipoCotizacion, RepositorioProducto,
  RepositorioStock, RepositorioCotizacionDolar
)


class ServicioBase:
  """Clase base genérica para servicios con operaciones CRUD simples."""

  def __init__(self, repositorio: IRepositorio):
    self._repositorio = repositorio

  def crear(self, entidad):
    return self._repositorio.crear(entidad)

  def obtener(self, id: int):
    entidad = self._repositorio.leer_por_id(id)
    if not entidad:
      raise ValueError(f"No se pudo encontrar el registro con ID {id}")
    return entidad

  def listar_todos(self) -> list:
    return self._repositorio.leer_todos()

  def actualizar(self, entidad):
    # Valida que exista antes de intentar actualizar
    existe = self._repositorio.leer_por_id(entidad.id)
    if not existe:
      raise ValueError("No se puede actualizar algo que no existe.")
    return self._repositorio.actualizar(entidad)

  def eliminar(self, id: int):
    existe = self._repositorio.leer_por_id(id)
    if not existe:
      raise ValueError(f"No existe el ID {id} para eliminar.")
    return self._repositorio.eliminar(id)

class ServicioCategoria(ServicioBase):
  def __init__(self, repositorio: RepositorioCategoria):
    super().__init__(repositorio)


class ServicioProveedor(ServicioBase):
  def __init__(self, repositorio: RepositorioProveedor):
    super().__init__(repositorio)


class ServicioMoneda(ServicioBase):
  def __init__(self, repositorio: RepositorioMoneda):
    super().__init__(repositorio)


class ServicioTipoCotizacion(ServicioBase):
  def __init__(self, repositorio: RepositorioTipoCotizacion):
    super().__init__(repositorio)

class ServicioProducto(ServicioBase):
  """Servicio para gestión de productos con validación de relaciones."""

  def __init__(
    self,
    repo_producto: RepositorioProducto,
    srv_categoria: ServicioCategoria,
    srv_proveedor: ServicioProveedor
  ):
    super().__init__(repo_producto)
    self._srv_categoria = srv_categoria
    self._srv_proveedor = srv_proveedor

  def crear(self, producto: Producto) -> Producto:
    # Validamos que la categoría y proveedor existan
    self._srv_categoria.obtener(producto.categoria.id)
    self._srv_proveedor.obtener(producto.proveedor.id)
    return super().crear(producto)

  def actualizar(self, producto: Producto) -> Producto:
    # Repetimos validación de relaciones
    self._srv_categoria.obtener(producto.categoria.id)
    self._srv_proveedor.obtener(producto.proveedor.id)
    return super().actualizar(producto)


class ServicioStock:
  """Servicio para gestión de inventario."""

  def __init__(
    self,
    repo_stock: RepositorioStock,
    srv_producto: ServicioProducto
  ):
    self._repo_stock = repo_stock
    self._srv_producto = srv_producto

  def registrar_movimiento(self, producto_id: int, cantidad: int) -> int:
    """Suma o resta stock. Valida que el resultado no sea negativo."""
    # 1. Asegurar que el producto exista
    self._srv_producto.obtener(producto_id)

    # 2. Buscar stock actual o inicializar en 0
    stock_actual = self._repo_stock.leer_por_producto(producto_id)
    if not stock_actual:
      stock_actual = Stock(producto_id=producto_id, cantidad=0)
      self._repo_stock.crear(stock_actual)

    # 3. Actualizar cantidad (la entidad valida que no sea < 0)
    nuevo_valor = stock_actual.cantidad + cantidad
    stock_actual.cantidad = nuevo_valor

    # 4. Guardar cambios
    self._repo_stock.actualizar(stock_actual)
    return stock_actual.cantidad

  def obtener_stock(self, producto_id: int) -> int:
    """Retorna la cantidad de stock para un producto."""
    self._srv_producto.obtener(producto_id)
    stock = self._repo_stock.leer_por_producto(producto_id)
    return stock.cantidad if stock else 0


class ServicioCotizacionDolar:
  """Servicio para gestión de cotizaciones del dólar."""

  def __init__(
    self,
    repo_cotizacion: RepositorioCotizacionDolar,
    srv_tipo_cot: ServicioTipoCotizacion
  ):
    self._repo_cotizacion = repo_cotizacion
    self._srv_tipo_cot = srv_tipo_cot

  def registrar_cotizacion(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Registra una nueva cotización validando el tipo."""
    self._srv_tipo_cot.obtener(cotizacion.tipo.id)
    return self._repo_cotizacion.crear(cotizacion)

  def obtener_historico(self, tipo_id: int) -> List[CotizacionDolar]:
    """Retorna el histórico de cotizaciones para un tipo."""
    self._srv_tipo_cot.obtener(tipo_id)
    return self._repo_cotizacion.leer_historico_por_tipo(tipo_id)
