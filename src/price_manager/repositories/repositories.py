# -*- coding: utf-8 -*-
"""Módulo de repositorios para el sistema Price Manager.

Implementa el patrón repositorio para la persistencia de datos
en archivos binarios (.pkl) utilizando la librería pickle.
"""

import abc
import os
import pickle
import datetime
from typing import TypeVar, Generic, List, Optional

# Importamos las entidades
from price_manager.entities.entities import (
  Categoria, Proveedor, Moneda, TipoCotizacion,
  Precio, Producto, CotizacionDolar, Stock
)

T = TypeVar('T')

# ==========================================================
# INTERFACES REQUERIDAS
# ==========================================================

class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz genérica para operaciones CRUD."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T: pass

  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]: pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]: pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T: pass

  @abc.abstractmethod
  def eliminar(self, id: int) -> bool: pass


class IRepositorioStock(abc.ABC):
  """Interfaz específica para el repositorio de Stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock: pass

  @abc.abstractmethod
  def leer_por_producto(self, producto_id: int) -> Optional[Stock]: pass

  @abc.abstractmethod
  def actualizar(self, stock: Stock) -> Stock: pass

  @abc.abstractmethod
  def eliminar(self, producto_id: int) -> bool: pass


class IRepositorioCotizacionDolar(abc.ABC):
  """Interfaz específica para el repositorio de Cotización Dólar."""

  @abc.abstractmethod
  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar: pass

  @abc.abstractmethod
  def leer_por_tipo_y_fecha(
    self, tipo_id: int, fecha: datetime.date
  ) -> Optional[CotizacionDolar]: pass

  @abc.abstractmethod
  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]: pass

  @abc.abstractmethod
  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar: pass

  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool: pass


# ==========================================================
# REPOSITORIO BASE PERSISTENTE
# ==========================================================

class RepositorioBasePersistente(IRepositorio[T]):
  """Implementación base de CRUD con persistencia vía Pickle."""

  def __init__(self, archivo_db: str):
    # Ruta absoluta para entorno Colab
    self._filepath = os.path.join("/content/price_manager/db", archivo_db)
    self._data: dict[int, T] = {}

    # Asegurar que el directorio de la base de datos exista
    os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
    self._cargar()

  def _cargar(self):
    """Carga los datos desde el archivo binario."""
    if os.path.exists(self._filepath) and os.path.getsize(self._filepath) > 0:
      with open(self._filepath, 'rb') as f:
        self._data = pickle.load(f)

  def _guardar(self):
    """Guarda los datos en el archivo binario."""
    with open(self._filepath, 'wb') as f:
      pickle.dump(self._data, f)

  def crear(self, entidad: T) -> T:
    if entidad.id in self._data:
      raise ValueError(f"Ya existe una entidad con el ID {entidad.id}")
    self._data[entidad.id] = entidad
    self._guardar()
    return entidad

  def leer_por_id(self, id: int) -> Optional[T]:
    return self._data.get(id)

  def leer_todos(self) -> List[T]:
    return list(self._data.values())

  def actualizar(self, entidad: T) -> T:
    if entidad.id not in self._data:
      raise ValueError(
        f"No existe la entidad con ID {entidad.id} para actualizar."
      )
    self._data[entidad.id] = entidad
    self._guardar()
    return entidad

  def eliminar(self, id: int) -> bool:
    if id not in self._data:
      raise ValueError(
        f"No se encontró la entidad con ID {id} para eliminar."
      )
    del self._data[id]
    self._guardar()
    return True


# ==========================================================
# REPOSITORIOS CONCRETOS
# ==========================================================

class RepositorioCategoria(RepositorioBasePersistente[Categoria]):
  def __init__(self):
    super().__init__("categorias.pkl")

class RepositorioProveedor(RepositorioBasePersistente[Proveedor]):
  def __init__(self):
    super().__init__("proveedores.pkl")

class RepositorioMoneda(RepositorioBasePersistente[Moneda]):
  def __init__(self):
    super().__init__("monedas.pkl")

class RepositorioTipoCotizacion(RepositorioBasePersistente[TipoCotizacion]):
  def __init__(self):
    super().__init__("tipo_cotizaciones.pkl")

class RepositorioProducto(RepositorioBasePersistente[Producto]):
  def __init__(self):
    super().__init__("productos.pkl")

class RepositorioStock(IRepositorioStock):
  """Implementación específica para Stock (usando producto_id como clave)."""

  def __init__(self):
    self._filepath = os.path.join("/content/price_manager/db", "stocks.pkl")
    self._data: dict[int, Stock] = {}
    os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
    self._cargar()

  def _cargar(self):
    if os.path.exists(self._filepath) and os.path.getsize(self._filepath) > 0:
      with open(self._filepath, 'rb') as f:
        self._data = pickle.load(f)

  def _guardar(self):
    with open(self._filepath, 'wb') as f:
      pickle.dump(self._data, f)

  def crear(self, stock: Stock) -> Stock:
    if stock.producto_id in self._data:
      raise ValueError(
        f"Ya existe stock para el producto {stock.producto_id}"
      )
    self._data[stock.producto_id] = stock
    self._guardar()
    return stock

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    return self._data.get(producto_id)

  def actualizar(self, stock: Stock) -> Stock:
    if stock.producto_id not in self._data:
      raise ValueError(
        "No se encuentra stock asignado a ese producto para actualizar."
      )
    self._data[stock.producto_id] = stock
    self._guardar()
    return stock

  def eliminar(self, producto_id: int) -> bool:
    if producto_id in self._data:
      del self._data[producto_id]
      self._guardar()
      return True
    return False

class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
  """Implementación específica para Cotización Dólar (clave: tipo_fecha)."""

  def __init__(self):
    self._filepath = os.path.join(
      "/content/price_manager/db", "cotizaciones.pkl"
    )
    self._data: dict[str, CotizacionDolar] = {}
    os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
    self._cargar()

  def _generar_clave(self, tipo_id: int, fecha: datetime.date) -> str:
    return f"{tipo_id}_{fecha.strftime('%Y-%m-%d')}"

  def _cargar(self):
    if os.path.exists(self._filepath) and os.path.getsize(self._filepath) > 0:
      with open(self._filepath, 'rb') as f:
        self._data = pickle.load(f)

  def _guardar(self):
    with open(self._filepath, 'wb') as f:
      pickle.dump(self._data, f)

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    clave = self._generar_clave(cotizacion.tipo.id, cotizacion.fecha)
    if clave in self._data:
      raise ValueError(
        "Ya existe una cotización de ese tipo para la fecha indicada."
      )
    self._data[clave] = cotizacion
    self._guardar()
    return cotizacion

  def leer_por_tipo_y_fecha(
    self, tipo_id: int, fecha: datetime.date
  ) -> Optional[CotizacionDolar]:
    return self._data.get(self._generar_clave(tipo_id, fecha))

  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
    return [
      cot for clave, cot in self._data.items()
      if clave.startswith(f"{tipo_id}_")
    ]

  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    clave = self._generar_clave(cotizacion.tipo.id, cotizacion.fecha)
    if clave not in self._data:
      raise ValueError(
        "No se encuentra la cotización especificada para actualizar."
      )
    self._data[clave] = cotizacion
    self._guardar()
    return cotizacion

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    clave = self._generar_clave(tipo_id, fecha)
    if clave in self._data:
      del self._data[clave]
      self._guardar()
      return True
    return False
