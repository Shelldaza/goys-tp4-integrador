# IA aplicada al diagnóstico de redes con MCP y un gemelo digital en GNS3

Trabajo Práctico Integrador N.º 4 de **Gestión Operativa y Seguridad en Redes**, 

Universidad Tecnológica Nacional - Facultad Regional La Plata.

**Modalidad:** B: Artículo de revisión del estado del arte.  
**Integrantes:** Facundo Daza e Irineo Hiriart.

## 1. Descripción

El trabajo estudia la integración de inteligencia artificial, Model Context Protocol (MCP) y gemelos digitales para asistir en el diagnóstico de problemas de red y evaluar posibles soluciones antes de recomendarlas para una red operativa.

La investigación se acompaña de una demostración en GNS3 con dos entornos:

- **EMPRESA:** representa la red operativa. La IA dispone de acceso de lectura.
- **GEMELO:** reproduce manualmente la configuración relevante de EMPRESA y permite probar modificaciones.

Ambas redes están emuladas en GNS3. No se utilizan equipos de una red de producción real.

## 2. Objetivos

- Investigar el estado del arte de la automatización de redes mediante IA y gemelos digitales.
- Analizar sus oportunidades, limitaciones y riesgos de seguridad.
- Implementar una demostración de diagnóstico mediante herramientas MCP.
- Probar una corrección en un entorno separado antes de recomendarla.
- Demostrar el uso de permisos diferenciados y controles de acceso.

## 3. Alcance de la demostración

Cada entorno contempla tres routers MikroTik CHR y dos hosts VPCS, con direccionamiento IPv4, enrutamiento OSPF y reglas de firewall.

Los proyectos y nodos se preparan e inician manualmente. La configuración relevante y la falla se reproducen manualmente en GEMELO.

La demostración no incluye:

- Sincronización automática entre EMPRESA y GEMELO.
- Descubrimiento o incorporación automática de dispositivos.
- Creación, cableado o inicio de nodos mediante la IA.
- Aplicación automática de cambios sobre EMPRESA.
- Resolución general de cualquier problema de red.

El gemelo permite evaluar el escenario reproducido. Sus resultados no constituyen una garantía para cualquier condición de producción.

## 4. Escenario de prueba

Una regla incorrecta de firewall bloquea el tráfico ICMP entre una PC y el host que representa al servidor.

El procedimiento de demostración es:

1. Comprobar que ambos entornos presentan el mismo problema.
2. Solicitar a la IA que investigue el síntoma.
3. Consultar interfaces, direcciones, rutas, vecinos OSPF y reglas de firewall mediante MCP.
4. Identificar y justificar una corrección.
5. Probar el cambio exclusivamente en GEMELO.
6. Verificar que se recupera la comunicación permitida.
7. Comprobar que un destino protegido continúa bloqueado.
8. Entregar una recomendación para el administrador.

Las pruebas de ping se ejecutan manualmente desde VPCS y se contrastan con los contadores del firewall. La validación es asistida: no se automatizan las pruebas de los hosts.

Durante la demostración, EMPRESA conserva la falla para evidenciar que la corrección se aplicó únicamente en GEMELO.

## 5. Tecnologías

| Tecnología | Función |
|---|---|
| GNS3 | Ejecutar los dos entornos de laboratorio |
| MikroTik CHR / RouterOS 7 | Enrutamiento, filtrado y administración |
| VPCS | Generar tráfico ICMP para las pruebas |
| OSPF | Intercambiar rutas entre los routers |
| Firewall de RouterOS | Aplicar permisos y restricciones de tráfico |
| Python | Implementar el servidor y las herramientas MCP |
| MCP | Permitir que la IA invoque herramientas del laboratorio |
| Paramiko y SSH | Consultar y configurar los routers |
| ChatGPT | Analizar resultados y utilizar las herramientas disponibles |
| tunnel-client | Conectar el servidor MCP local con ChatGPT |
| Git y GitHub | Versionar código, documentación y evidencias |

Las versiones concretas utilizadas se registrarán al completar las pruebas de integración.

## 6. Seguridad

La propuesta incorpora los siguientes controles:

- Cuenta dedicada de lectura para consultar EMPRESA.
- Credenciales independientes para operar sobre GEMELO.
- Herramientas MCP con destinos y operaciones restringidos.
- Ausencia de una herramienta genérica para ejecutar comandos arbitrarios.
- Verificación de claves de host SSH.
- Restricción del acceso de administración al equipo autorizado.
- Separación de las redes de datos de ambos entornos.
- Credenciales fuera del repositorio y de los argumentos enviados por la IA.
- Registro de las operaciones realizadas.
- Verificación de que la corrección conserva los bloqueos requeridos.

La cuenta de GEMELO necesita permisos de escritura de RouterOS. La restricción a una operación concreta se implementa además en el código MCP, no equivale a un permiso nativo de RouterOS limitado a una única regla.

Estos controles se consideran implementados únicamente después de verificarlos y guardar sus evidencias.

## 7. Estado del proyecto

### Prueba de concepto realizada

- Conexión de un servidor MCP local con un router MikroTik en GNS3.
- Consulta del nombre del router mediante SSH.
- Integración con ChatGPT mediante un túnel.
- Verificación de lectura en vivo después de cambiar manualmente el nombre del router.
- Se confirma la viabilidad del proyecto.

### Pendiente de implementación y validación

- Preparar los proyectos EMPRESA y GEMELO.
- Configurar direccionamiento, OSPF y firewall.
- Implementar y verificar los permisos definitivos.
- Incorporar las herramientas MCP del escenario.
- Ejecutar las pruebas positivas y negativas.
- Repetir la demostración al menos tres veces.
- Preparar las evidencias y la grabación de respaldo.

El avance detallado se registra en `progreso.md`

## 8. Estructura del repositorio

| Ubicación | Contenido |
|---|---|
| `README.md` | Descripción e instrucciones generales |
| `progreso.md` | Bitácora de aportes, decisiones y avances |
| `templates/` | Plantillas y checklist de la cátedra |
| `documento/` | Artículo final en PDF y su fuente editable |
| `poster/` | Póster A1 editable y PDF |
| `demo/` | Código, dependencias y configuraciones de ejemplo |
| `capturas/` | Evidencias de funcionamiento y seguridad |
| `diagramas/` | Diagramas de arquitectura y topología |

## 9. Reproducción del laboratorio

### Requisitos

- GNS3 y su entorno de virtualización funcionando.
- Imagen MikroTik CHR 7.16 obtenida desde una fuente oficial.
- VPCS disponible en GNS3.
- Python compatible con las dependencias del proyecto.
- Cliente SSH.
- Acceso a Internet para utilizar ChatGPT y el túnel MCP.

Las imágenes de máquinas virtuales, credenciales y ejecutables no se incluyen en el repositorio.

### Clonar el repositorio

```powershell
git clone https://github.com/Shelldaza/goys-tp4-integrador.git
cd goys-tp4-integrador
```

### Preparar la demo

La implementación está en desarrollo. Una vez incorporados los archivos y comprobada la integración, se completará esta sección con:

1. Versiones y recursos utilizados.
2. Topología y tabla de direccionamiento.
3. Configuración de cada router y host.
4. Instalación de dependencias Python.
5. Configuración del inventario y las credenciales locales.
6. Inicio del servidor MCP y del túnel.
7. Introducción de la falla.
8. Pruebas de diagnóstico, corrección y restauración.

Las instrucciones finales deberán permitir repetir el escenario sin depender de conversaciones previas.

## 10. Evidencias y resultados

Se documentarán las siguientes comprobaciones:

| Comprobación | Evidencia esperada |
|---|---|
| Red operativa durante la falla | Vecinos OSPF FULL y rutas presentes |
| Bloqueo inicial | Ping fallido y contador de la regla |
| Lectura real mediante MCP | Respuestas identificadas por equipo |
| Restricción de EMPRESA | Intento de escritura rechazado |
| Corrección en GEMELO | Regla modificada y ping recuperado |
| Seguridad conservada | Destino protegido bloqueado y contador de descarte |
| EMPRESA sin cambios | Regla del incidente activa y ping fallido |
| Repetibilidad | Registro de tres ejecuciones completas |

Los resultados se incorporarán después de realizar las pruebas. La conectividad ICMP no se presentará como validación de una aplicación o servicio TCP.

## 11. Dependencia de Internet y respaldo

GNS3, los routers y las pruebas locales pueden funcionar sin Internet.

La interacción con ChatGPT mediante el túnel requiere conectividad. Para la feria se preparará una grabación local de una ejecución completa, acompañada de capturas y resultados.

El material grabado se identificará como tal y se comprobará su reproducción sin conexión.

## 12. Organización del trabajo

| Integrante | Responsabilidades principales |
|---|---|
| Facundo Daza | Laboratorio GNS3, servidor MCP, controles de seguridad, pruebas, evidencias e instrucciones de reproducción |
| Irineo Hiriart | Investigación bibliográfica, artículo de revisión y póster |
| Ambos | Bitácora, revisión cruzada, conclusiones y defensa |

Cada integrante realiza commits con su identidad. Los cambios se trabajan en ramas y se revisan mediante pull requests.

## 13. Entregables

- Artículo de modalidad B de 5–7 páginas, en PDF y con fuente editable.
- Póster A1 en formato editable y PDF.
- Demostración de 3–5 minutos.
- Código y configuraciones documentados.
- Capturas y resultados verificables.
- Grabación de respaldo.
- Bitácora de participación del grupo.
- Checklist de entrega completo.

## 14. Trabajo futuro

- Actualización automática de la configuración del gemelo.
- Incorporación de nuevos dispositivos.
- Automatización de pruebas desde los hosts.
- Evaluación de servicios de aplicación.
- Ampliación de los escenarios de falla.
- Evaluación de alternativas de IA local.

Estas capacidades quedan fuera de la demostración inicial.

## 15. Referencias

Las referencias bibliográficas completas se incluyen en el artículo de `documento/`.

El artículo debe incorporar al menos seis referencias verificables, incluyendo un trabajo académico, documentación técnica oficial y un RFC o estándar, con un formato de citación consistente.