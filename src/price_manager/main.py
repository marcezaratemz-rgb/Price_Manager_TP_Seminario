# -*- coding: utf-8 -*-
"""Módulo principal del sistema Price Manager.

Punto de entrada, configuración de la arquitectura,
la inyección de dependencias y el inicio de la aplicación.
"""

from price_manager.repositories.repositories import (
  RepositorioCategoria, RepositorioProveedor, RepositorioMoneda,
  RepositorioTipoCotizacion, RepositorioProducto,
  RepositorioStock, RepositorioCotizacionDolar
)
from price_manager.services.services import (
  ServicioCategoria, ServicioProveedor, ServicioMoneda,
  ServicioTipoCotizacion, ServicioProducto,
  ServicioStock, ServicioCotizacionDolar
)
from price_manager.preload_data.preload_data import (
  importar_datos_por_defecto
)
from price_manager.ui.console import ConsoleUI


def main(import_default_data=False):
  """Función principal que inicia el sistema.

  Args:
      import_default_data (bool): Si es True, carga los datos de los CSV.
  """
  # ==========================================
  # 1. ARQUITECTURA: CREACIÓN DE REPOSITORIOS
  # ==========================================
  repo_cat = RepositorioCategoria()
  repo_prov = RepositorioProveedor()
  repo_mon = RepositorioMoneda()
  repo_tipo_cot = RepositorioTipoCotizacion()
  repo_prod = RepositorioProducto()
  repo_stock = RepositorioStock()
  repo_cot = RepositorioCotizacionDolar()

  # ==========================================
  # 2. ARQUITECTURA: INYECCIÓN A SERVICIOS
  # ==========================================
  srv_cat = ServicioCategoria(repo_cat)
  srv_prov = ServicioProveedor(repo_prov)
  srv_mon = ServicioMoneda(repo_mon)
  srv_tipo_cot = ServicioTipoCotizacion(repo_tipo_cot)
  srv_prod = ServicioProducto(repo_prod, srv_cat, srv_prov)
  srv_stock = ServicioStock(repo_stock, srv_prod)
  srv_cot = ServicioCotizacionDolar(repo_cot, srv_tipo_cot)

  # Diccionario central de servicios para facilitar el paso de dependencias
  servicios = {
    "categoria": srv_cat,
    "proveedor": srv_prov,
    "moneda": srv_mon,
    "tipo_cotizacion": srv_tipo_cot,
    "producto": srv_prod,
    "stock": srv_stock,
    "cotizacion_dolar": srv_cot
  }

  # ==========================================
  # 3. MÓDULO DE PRECARGA (REQUERIMIENTO SPRINT)
  # ==========================================
  if import_default_data:
    importar_datos_por_defecto(servicios)

  # ==========================================
  # 4. INSTANCIACIÓN Y ARRANQUE DE LA UI
  # ==========================================
  ui = ConsoleUI(servicios)
  ui.run()

if __name__ == "__main__":
  main(import_default_data=True)
