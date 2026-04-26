# -*- coding: utf-8 -*-
"""Módulo de entidades del sistema Price Manager.

Define las clases de dominio que representan los objetos
de negocio del sistema, aplicando encapsulamiento mediante
propiedades y validaciones en los setters.
"""

import datetime

class Categoria:
  """Entidad que representa el rubro o categoría de un producto."""

  def __init__(self, id: int, nombre: str):
    """Inicializa una Categoria.

    Args:
        id (int): Identificador único numérico.
        nombre (str): Nombre descriptivo de la categoría.
    """
    self._id = id
    self.nombre = nombre

  @property
  def id(self) -> int:
    """Retorna el identificador único de la categoría."""
    return self._id

  @property
  def nombre(self) -> str:
    """Retorna el nombre de la categoría."""
    return self._nombre

  @nombre.setter
  def nombre(self, value: str):
    """Establece el nombre validando que no sea vacío.

    Raises:
        ValueError: Si el nombre está vacío o es solo espacios.
    """
    if not value or not str(value).strip():
      raise ValueError(
        "El nombre de la categoría no puede estar vacío."
      )
    self._nombre = value

  def __repr__(self) -> str:
    return f"Categoria(id={self._id}, nombre='{self._nombre}')"


class Proveedor:
  """Entidad que representa a un proveedor de mercadería."""

  def __init__(self, id: int, nombre: str, contacto: str):
    """Inicializa un Proveedor.

    Args:
        id (int): Identificador único del proveedor.
        nombre (str): Nombre legal del proveedor.
        contacto (str): Vía de contacto (email, teléfono, etc).
    """
    self._id = id
    self.nombre = nombre
    self.contacto = contacto

  @property
  def id(self) -> int:
    """Retorna el identificador único del proveedor."""
    return self._id

  @property
  def nombre(self) -> str:
    """Retorna el nombre legal del proveedor."""
    return self._nombre

  @nombre.setter
  def nombre(self, value: str):
    """Establece el nombre legal validando que no sea vacío.

    Raises:
        ValueError: Si el nombre está vacío.
    """
    if not value:
      raise ValueError(
        "El nombre legal del proveedor es obligatorio."
      )
    self._nombre = value

  @property
  def contacto(self) -> str:
    """Retorna la vía de contacto del proveedor."""
    return self._contacto

  @contacto.setter
  def contacto(self, value: str):
    """Establece la vía de contacto del proveedor."""
    self._contacto = value

  def __repr__(self) -> str:
    return (
      f"Proveedor(id={self._id}, nombre='{self._nombre}', "
      f"contacto='{self._contacto}')"
    )

class Moneda:
  """Entidad que representa un tipo de moneda del sistema."""

  def __init__(self, id: int, nombre: str):
    """Inicializa una Moneda.

    Args:
        id (int): Identificador único de la moneda.
        nombre (str): Nombre de la moneda (ej: 'Peso Argentino').
    """
    self._id = id
    self.nombre = nombre

  @property
  def id(self) -> int:
    """Retorna el identificador único de la moneda."""
    return self._id

  @property
  def nombre(self) -> str:
    """Retorna el nombre de la moneda."""
    return self._nombre

  @nombre.setter
  def nombre(self, value: str):
    """Establece el nombre de la moneda validando que no sea vacío.

    Raises:
        ValueError: Si el nombre está vacío.
    """
    if not value:
      raise ValueError("El tipo de moneda no puede estar vacío.")
    self._nombre = value

  def __repr__(self) -> str:
    return f"Moneda(id={self._id}, nombre='{self._nombre}')"


class TipoCotizacion:
  """Entidad que representa el tipo de cotización del dólar."""

  def __init__(self, id: int, nombre: str):
    """Inicializa un TipoCotizacion.

    Args:
        id (int): Identificador único del tipo de cotización.
        nombre (str): Nombre del tipo (ej: 'Blue', 'Oficial').
    """
    self._id = id
    self.nombre = nombre

  @property
  def id(self) -> int:
    """Retorna el identificador único del tipo de cotización."""
    return self._id

  @property
  def nombre(self) -> str:
    """Retorna el nombre del tipo de cotización."""
    return self._nombre

  @nombre.setter
  def nombre(self, value: str):
    """Establece el nombre del tipo de cotización."""
    self._nombre = value

  def __repr__(self) -> str:
    return (
      f"TipoCotizacion(id={self._id}, nombre='{self._nombre}')"
    )

class Precio:
  """Value Object que representa el precio de un producto.

  Contiene el valor monetario, la moneda y la fecha de
  última actualización. El valor no puede ser negativo.
  """

  def __init__(
    self,
    valor: float,
    moneda: 'Moneda',
    fecha: datetime.date
  ):
    """Inicializa un Precio.

    Args:
        valor (float): Valor del precio (debe ser >= 0).
        moneda (Moneda): Instancia de la moneda asociada.
        fecha (datetime.date): Fecha de última actualización.
    """
    self.valor = valor
    self.moneda = moneda
    self.fecha = fecha

  @property
  def valor(self) -> float:
    """Retorna el valor del precio."""
    return self._valor

  @valor.setter
  def valor(self, value: float):
    """Establece el valor del precio validando que no sea negativo.

    Raises:
        ValueError: Si el valor es negativo.
    """
    if value < 0:
      raise ValueError(
        "La regla de negocio marca que un Precio "
        "no puede ser negativo."
      )
    self._valor = value

  @property
  def moneda(self) -> 'Moneda':
    """Retorna la moneda asociada al precio."""
    return self._moneda

  @moneda.setter
  def moneda(self, value: 'Moneda'):
    """Establece la moneda validando el tipo de objeto.

    Raises:
        TypeError: Si el valor no es una instancia de Moneda.
    """
    if not isinstance(value, Moneda):
      raise TypeError(
        "El atributo moneda debe de ser del tipo 'Moneda'."
      )
    self._moneda = value

  @property
  def fecha(self) -> datetime.date:
    """Retorna la fecha de última actualización del precio."""
    return self._fecha

  @fecha.setter
  def fecha(self, value: datetime.date):
    """Establece la fecha de última actualización."""
    self._fecha = value

  def __repr__(self) -> str:
    return (
      f"Precio(valor={self._valor}, "
      f"moneda={self._moneda.nombre}, fecha={self._fecha})"
    )

class CotizacionDolar:
  """Entidad que registra la cotización diaria del dólar.

  El valor siempre debe ser positivo mayor a cero. Se asocia
  a un TipoCotizacion para diferenciar 'Blue', 'Oficial', etc.
  """

  def __init__(
    self,
    valor: float,
    fecha: datetime.date,
    tipo: 'TipoCotizacion'
  ):
    """Inicializa una CotizacionDolar.

    Args:
        valor (float): Valor de la cotización (debe ser > 0).
        fecha (datetime.date): Fecha de la cotización.
        tipo (TipoCotizacion): Tipo de cotización asociada.
    """
    self.valor = valor
    self.fecha = fecha
    self.tipo = tipo

  @property
  def valor(self) -> float:
    """Retorna el valor de la cotización."""
    return self._valor

  @valor.setter
  def valor(self, value: float):
    """Establece el valor validando que sea positivo mayor a cero.

    Raises:
        ValueError: Si el valor es menor o igual a cero.
    """
    if value <= 0:
      raise ValueError(
        "La cotización del dólar debe ser siempre "
        "un valor positivo mayor a cero."
      )
    self._valor = value

  @property
  def fecha(self) -> datetime.date:
    """Retorna la fecha de la cotización."""
    return self._fecha

  @fecha.setter
  def fecha(self, value: datetime.date):
    """Establece la fecha de la cotización."""
    self._fecha = value

  @property
  def tipo(self) -> 'TipoCotizacion':
    """Retorna el tipo de cotización asociada."""
    return self._tipo

  @tipo.setter
  def tipo(self, value: 'TipoCotizacion'):
    """Establece el tipo de cotización validando el tipo de objeto.

    Raises:
        TypeError: Si el valor no es una instancia de TipoCotizacion.
    """
    if not isinstance(value, TipoCotizacion):
      raise TypeError(
        "Debe ser una instancia válida de TipoCotizacion."
      )
    self._tipo = value

  def __repr__(self) -> str:
    return (
      f"CotizacionDolar(valor={self._valor}, "
      f"fecha={self._fecha}, tipo={self._tipo.nombre})"
    )

class Producto:
  """Entidad central del sistema que representa un artículo de venta.

  Cada producto está asociado a una instancia de Precio,
  una Categoria y un Proveedor.
  """

  def __init__(
    self,
    id: int,
    nombre: str,
    descripcion: str,
    precio: 'Precio',
    categoria: 'Categoria',
    proveedor: 'Proveedor'
  ):
    """Inicializa un Producto.

    Args:
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        descripcion (str): Descripción detallada del producto.
        precio (Precio): Instancia de Precio asociada.
        categoria (Categoria): Categoría del producto.
        proveedor (Proveedor): Proveedor del producto.
    """
    self._id = id
    self.nombre = nombre
    self.descripcion = descripcion
    self.precio = precio
    self.categoria = categoria
    self.proveedor = proveedor

  @property
  def id(self) -> int:
    """Retorna el identificador único del producto."""
    return self._id

  @property
  def nombre(self) -> str:
    """Retorna el nombre del producto."""
    return self._nombre

  @nombre.setter
  def nombre(self, value: str):
    """Establece el nombre validando que no sea vacío.

    Raises:
        ValueError: Si el nombre está vacío.
    """
    if not value:
      raise ValueError(
        "El producto debe tener un nombre válido asignado."
      )
    self._nombre = value

  @property
  def descripcion(self) -> str:
    """Retorna la descripción del producto."""
    return self._descripcion

  @descripcion.setter
  def descripcion(self, value: str):
    """Establece la descripción del producto."""
    self._descripcion = value

  @property
  def precio(self) -> 'Precio':
    """Retorna el precio del producto."""
    return self._precio

  @precio.setter
  def precio(self, value: 'Precio'):
    """Establece el precio validando el tipo de objeto.

    Raises:
        TypeError: Si el valor no es una instancia de Precio.
    """
    if not isinstance(value, Precio):
      raise TypeError(
        "El precio asignado no posee el formato de "
        "objeto Precio correspondiente."
      )
    self._precio = value

  @property
  def categoria(self) -> 'Categoria':
    """Retorna la categoría del producto."""
    return self._categoria

  @categoria.setter
  def categoria(self, value: 'Categoria'):
    """Establece la categoría validando el tipo de objeto.

    Raises:
        TypeError: Si el valor no es una instancia de Categoria.
    """
    if not isinstance(value, Categoria):
      raise TypeError(
        "Debe ser una instancia de la clase Categoria."
      )
    self._categoria = value

  @property
  def proveedor(self) -> 'Proveedor':
    """Retorna el proveedor del producto."""
    return self._proveedor

  @proveedor.setter
  def proveedor(self, value: 'Proveedor'):
    """Establece el proveedor validando el tipo de objeto.

    Raises:
        TypeError: Si el valor no es una instancia de Proveedor.
    """
    if not isinstance(value, Proveedor):
      raise TypeError(
        "Debe asignarse mediante una instancia de Proveedor."
      )
    self._proveedor = value

  def __repr__(self) -> str:
    return (
      f"Producto(id={self._id}, nombre='{self._nombre}', "
      f"categoria='{self._categoria.nombre}')"
    )


class Stock:
  """Entidad que vincula un Producto con su cantidad disponible.

  La cantidad nunca puede resultar en un valor negativo.
  """

  def __init__(
    self,
    producto_id: int,
    cantidad: int = 0,
    almacen: str = "Central"
  ):
    """Inicializa un registro de Stock.

    Args:
        producto_id (int): ID del producto al que se vincula.
        cantidad (int): Cantidad disponible (por defecto 0).
        almacen (str): Nombre del almacén (por defecto 'Central').
    """
    self.producto_id = producto_id
    self.almacen = almacen
    self.cantidad = cantidad

  @property
  def producto_id(self) -> int:
    """Retorna el ID del producto asociado al stock."""
    return self._producto_id

  @producto_id.setter
  def producto_id(self, value: int):
    """Establece el ID del producto asociado."""
    self._producto_id = value

  @property
  def almacen(self) -> str:
    """Retorna el nombre del almacén."""
    return self._almacen

  @almacen.setter
  def almacen(self, value: str):
    """Establece el nombre del almacén."""
    self._almacen = value

  @property
  def cantidad(self) -> int:
    """Retorna la cantidad disponible en stock."""
    return self._cantidad

  @cantidad.setter
  def cantidad(self, value: int):
    """Establece la cantidad validando que no sea negativa.

    Raises:
        ValueError: Si la cantidad resultante es negativa.
    """
    if value < 0:
      raise ValueError(
        "Alerta crítica: La cantidad de stock operado "
        "no puede resultar en un valor negativo."
      )
    self._cantidad = value

  def __repr__(self) -> str:
    return (
      f"Stock(producto_id={self._producto_id}, "
      f"cantidad={self._cantidad}, almacen='{self._almacen}')"
    )
