#
### Día 1 — Ejercicio 01: Configuración del repositorio y estructura de directorios
  * Inicialización del repositorio Git en la rama Sprint_1.
  * Creación de la estructura de directorios del proyecto según la especificación.
  * Configuración del archivo README.md con objetivo e introducción del Sprint 1.
  * Creación de requirements.txt.
  * Creación de CHANGELOG.md.

### Día 2 — Ejercicio 02: Definición de entidades del dominio
  * Implementación de entities.py con las clases del dominio.
  * Encapsulamiento con propiedades y setters.
  * Validaciones de negocio: precio no negativo, stock >= 0.
  * Type hints y documentación PEP8.

###  Día 3 — Ejercicio 03: Repositorios con persistencia en CSV
  * Implementación de repositories.py con la interfaz abstracta IRepositorio.
  * Repositorios concretos: RepositorioCategoria, RepositorioProveedor, RepositorioMoneda, RepositorioTipoCotizacion, RepositorioProducto, RepositorioStock y RepositorioCotizacionDolar.
",
  * CRUD completo en cada repositorio con persistencia en archivos CSV.

###  Día 4 — Ejercicio 04: Capa de servicios con lógica de negocio
  * Implementación de services.py con servicios para cada entidad del dominio.
  * Validaciones de negocio: stock no puede quedar negativo, relaciones entre entidades verificadas antes de la creación.
  * Método actualizar_precio y registrar_movimiento con lógica de negocio.

###  Día 5 — Ejercicio 05: Archivos de importación de datos (migrations/csv)
  * Implementación de preload_data.py con función cargar_datos_iniciales.
  * Datos precargados: 10 categorías, 10 proveedores, 10 monedas, 7 tipos de cotización, 10 productos, registros de stock y 10 cotizaciones históricas.
  * La precarga es idempotente: solo carga si los CSV están vacíos o no existen.
