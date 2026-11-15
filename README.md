# IA aplicada al diagnóstico de redes con MCP y un gemelo digital en GNS3

Trabajo Práctico Integrador N.º 4 de **Gestión Operativa y Seguridad en Redes**.  
Universidad Tecnológica Nacional — Facultad Regional La Plata.

**Modalidad:** B — Artículo de revisión del estado del arte.  
**Grupo:** 3.  
**Integrantes:** Facundo Daza e Irineo Hiriart.

## 1. Descripción

El trabajo estudia la integración de inteligencia artificial, Model Context Protocol (MCP) y gemelos digitales para asistir en el diagnóstico de problemas de red y evaluar posibles soluciones antes de recomendarlas para una red operativa.

La investigación se acompaña de una demostración en GNS3 con dos entornos independientes:

- **EMPRESA:** representa la red operativa. La IA dispone únicamente de acceso de lectura.
- **GEMELO:** entorno de prueba donde la IA puede reproducir problemas, modificar configuraciones y comprobar los resultados.

La aplicación de correcciones en EMPRESA queda a cargo de su administrador.

Ambas redes están emuladas en GNS3. No se utilizan equipos de una red de producción real.

## 2. Objetivos

- Investigar el estado del arte de la automatización de redes mediante IA y gemelos digitales.
- Analizar sus oportunidades, limitaciones y riesgos de seguridad.
- Implementar una demostración de diagnóstico mediante herramientas MCP.
- Reproducir un problema y probar su corrección en un entorno separado.
- Fundamentar las recomendaciones mediante configuraciones y pruebas observadas.
- Demostrar el uso de permisos diferenciados y controles de acceso.

## 3. Alcance de la demostración

Cada entorno incluye tres routers MikroTik CHR y dos hosts VPCS, con direccionamiento IPv4, enrutamiento OSPF y reglas de firewall.

Los proyectos y nodos se preparan e inician manualmente. La IA puede comparar EMPRESA y GEMELO y actualizar la configuración relevante del gemelo a solicitud del usuario o para reproducir el problema investigado, conservando las diferencias intencionales de gestión, identidades, MAC y credenciales.

La integración utiliza herramientas generales. No contiene una función específica que identifique o corrija la falla del escenario: la IA debe seleccionar las consultas, interpretar las respuestas y decidir qué cambios probar.

La demostración no incluye:

- Sincronización continua en segundo plano.
- Descubrimiento o incorporación automática de dispositivos.
- Creación, cableado o inicio de nodos mediante la IA.
- Aplicación automática de cambios sobre EMPRESA.
- Reversión automática de los cambios.
- Garantía de resolución de cualquier problema de red.

El gemelo permite evaluar el escenario reproducido. Una comparación parcial no demuestra equivalencia completa entre ambos entornos y sus resultados no garantizan el comportamiento bajo cualquier condición de producción.

## 4. Escenario de prueba

Una regla de firewall introducida manualmente bloquea el tráfico ICMP desde PC hacia el host que representa al servidor.

El procedimiento de demostración es:

1. Comprobar la conectividad inicial e introducir la falla en EMPRESA.
2. Solicitar a la IA que investigue el síntoma mediante MCP.
3. Consultar la configuración y el estado de los equipos.
4. Comparar y adaptar GEMELO cuando sea necesario para reproducir el problema.
5. Confirmar el bloqueo mediante pruebas desde los extremos y contadores del firewall.
6. Identificar y justificar una corrección.
7. Aplicar el cambio exclusivamente en GEMELO.
8. Repetir las pruebas y comprobar las restricciones relacionadas que deben conservarse.
9. Presentar un informe y una recomendación para el administrador.

Las pruebas desde GEMELO-PC y GEMELO-SRV pueden ejecutarse mediante MCP y contrastarse con los contadores del firewall.

En el ensayo documentado, la IA confirmó el bloqueo y verificó la recuperación de las respuestas después de deshabilitar la regla únicamente en GEMELO. EMPRESA conservó la falla.

La prueba valida conectividad ICMP. No acredita el funcionamiento de aplicaciones o servicios TCP y UDP.

Los comandos de preparación, limpieza y los resultados se documentan en la Fase 7 de [DesarrolloDemo.md](demo/DesarrolloDemo.md).

## 5. Tecnologías

| Tecnología | Función |
|---|---|
| GNS3 3.0.6 y GNS3 VM sobre VMware | Ejecutar los dos entornos de laboratorio |
| MikroTik CHR / RouterOS 7.16 | Enrutamiento, filtrado y administración |
| VPCS 0.8.3 | Representar los extremos y ejecutar pruebas de conectividad |
| OSPFv2 | Intercambiar rutas entre los routers |
| Firewall de RouterOS | Aplicar permisos y restricciones de tráfico |
| Python 3.13 y FastMCP | Implementar el servidor y las herramientas MCP |
| MCP | Permitir que la IA invoque herramientas del laboratorio |
| Paramiko y SSH | Consultar y configurar los routers |
| Consolas Telnet de VPCS | Operar los extremos de GEMELO |
| ChatGPT | Investigar el problema y utilizar las herramientas disponibles |
| Secure MCP Tunnel y tunnel-client | Conectar el servidor MCP local con ChatGPT |
| Git y GitHub | Versionar código, documentación y evidencias |

Las dependencias de Python se encuentran en [requirements.txt](demo/mcp/requirements.txt).

## 6. Seguridad

La implementación incorpora:

- Cuenta `mcp_ro` con permisos de lectura y SSH para consultar los routers.
- Acceso administrativo con `netadmin` exclusivamente en GEMELO desde el MCP.
- Destinos limitados al inventario y rechazo de EMPRESA en la capa administrativa.
- Verificación de claves de host SSH, identidad y MAC de gestión.
- Restricción del acceso SSH al equipo administrador autorizado.
- Separación de los segmentos de datos de EMPRESA y GEMELO.
- Filtrado IPv4 para proteger la gestión y controlar el tráfico del escenario.
- Autenticación OSPF con HMAC-SHA256.
- Servicios, mecanismos de acceso MAC e interfaces sin uso deshabilitados.
- Reglas de descarte de entrada y tránsito IPv6.
- Archivo `.env` y claves personales de OpenAI excluidos del repositorio.

La IA dispone de comandos administrativos generales en GEMELO. Puede modificar su configuración o interrumpir su acceso; la consola de GNS3 permite la recuperación manual.

PC y SRV son simuladores VPCS. Sus consolas Telnet no tienen autenticación propia ni cifran el tráfico, por lo que deben permanecer dentro del entorno de administración de GNS3.

Las credenciales son exclusivas del laboratorio y se entregan por un canal privado. Los proyectos portables conservan la configuración persistente de sus equipos.

Los controles, sus pruebas y limitaciones se documentan en la Fase 4 de [DesarrolloDemo.md](demo/DesarrolloDemo.md).

## 7. Integración MCP

El servidor publica cuatro herramientas:

| Herramienta | Alcance |
|---|---|
| `listar_routers` | Consultar el inventario de routers |
| `consultar_router` | Ejecutar comandos con `mcp_ro` en EMPRESA y GEMELO |
| `ejecutar_comando_gemelo` | Ejecutar comandos con `netadmin` en los routers de GEMELO |
| `ejecutar_comando_vpcs` | Operar las consolas de GEMELO-PC y GEMELO-SRV |

Las credenciales se cargan localmente y no se solicitan como argumentos de las herramientas.

El servidor incluye instrucciones para investigar con evidencias, reproducir el problema antes de corregirlo, validar los resultados y presentar un informe breve en Markdown dentro del chat. Estas instrucciones orientan a la IA; el formato y la completitud del informe se revisan durante los ensayos.

## 8. Estado del proyecto

Se completaron:

- Construcción y configuración de EMPRESA y GEMELO.
- Direccionamiento, OSPF y controles de seguridad.
- Separación de acceso de lectura y administración.
- Herramientas MCP generales para routers y consolas VPCS.
- Configuración y arranque del túnel local.
- Integración y pruebas desde ChatGPT.
- Diagnóstico y corrección del escenario de firewall en GEMELO.
- Tres ejecuciones completas y comprobación de una duración de 3–5 minutos.
- Grabación de una ejecución como respaldo.
- Distribución de los proyectos portables y reproducción de la integración en otra computadora.

El avance detallado, los aportes y las referencias a commits se registran en [progreso.md](progreso.md).

## 9. Estructura del repositorio

| Ubicación | Contenido |
|---|---|
| `README.md` | Presentación y alcance del proyecto |
| `progreso.md` | Bitácora de aportes, decisiones y avances |
| `templates/` | Plantillas y checklist de la cátedra |
| `documento/` | Artículo y material bibliográfico |
| `poster/` | Póster y archivos de presentación |
| `demo/README.md` | Instalación y reproducción del laboratorio |
| `demo/DesarrolloDemo.md` | Desarrollo por fases, comandos y pruebas |
| `demo/Archivos-GNS3/` | Proyectos portables EMPRESA y GEMELO |
| `demo/mcp/` | Servidor MCP, conexiones, herramientas y verificaciones |
| `capturas/` | Evidencias de funcionamiento y seguridad |
| `diagramas/` | Diagramas de arquitectura y topología |

## 10. Reproducción del laboratorio

Clonar el repositorio:

```bash
git clone https://github.com/Shelldaza/goys-tp4-integrador.git
cd goys-tp4-integrador
```

Seguir la [guía de instalación de la demo](demo/README.md), que incluye:

1. Importación de los proyectos GNS3.
2. Preparación de la red Host-only.
3. Comprobación de identidades, MAC y acceso SSH.
4. Creación del entorno virtual e instalación de dependencias.
5. Configuración local de credenciales y consolas.
6. Verificaciones del MCP.
7. Creación, configuración e inicio del túnel.
8. Conexión y primera prueba desde ChatGPT.

Cada instalación necesita su propio entorno virtual, archivo `.env` y perfil local del túnel. El ejecutable `tunnel-client.exe` se obtiene por separado.

La disponibilidad de conexiones MCP y del túnel debe comprobarse en la cuenta utilizada.

## 11. Evidencias y resultados

La documentación incluye comprobaciones de:

- Vecindades y rutas OSPF.
- Comunicaciones permitidas y bloqueadas.
- Lectura permitida y escritura rechazada con `mcp_ro`.
- Autenticación OSPF y recuperación de una vecindad tras restaurar su clave.
- Acceso SSH desde el origen autorizado y bloqueo desde el origen no autorizado ensayado.
- Consultas a routers y acceso a las consolas mediante MCP.
- Reproducción del bloqueo ICMP en GEMELO.
- Recuperación de conectividad después de corregir únicamente GEMELO.
- Conservación de EMPRESA sin modificaciones por parte de la IA.

Las evidencias y los límites de cada comprobación se presentan en [DesarrolloDemo.md](demo/DesarrolloDemo.md). Las pruebas respaldan los comportamientos observados; no constituyen una auditoría completa de seguridad.

## 12. Dependencia de Internet y respaldo

GNS3, los routers y las pruebas locales pueden funcionar sin Internet. La interacción con ChatGPT mediante Secure MCP Tunnel requiere conectividad.

Se grabó una ejecución como respaldo y se realizaron ensayos completos de la demostración.

**Video:** [Ver demostración grabada](https://drive.google.com/drive/u/0/folders/1o1cRteSKecS5OazFFu4jLJMQ6N6zNgUc)

Para utilizar el respaldo sin Internet, debe descargarse previamente y conservarse una copia local.

## 13. Organización del trabajo

| Integrante | Responsabilidades principales |
|---|---|
| Facundo Daza | Laboratorio GNS3, servidor MCP, controles de seguridad, pruebas, evidencias e instrucciones de reproducción |
| Irineo Hiriart | Investigación bibliográfica, artículo de revisión y póster |
| Ambos | Bitácora, revisión cruzada, conclusiones y defensa |

Cada integrante realiza commits con su identidad. Los cambios se trabajan en ramas y se revisan mediante pull requests.

## 14. Entregables

- Artículo de modalidad B de 5–7 páginas, en PDF y con fuente editable.
- Póster A1 en formato editable y PDF.
- Demostración de 3–5 minutos.
- Código y configuraciones documentados.
- Capturas y resultados verificables.
- Grabación de respaldo.
- Bitácora de participación del grupo.
- Checklist de entrega de la cátedra.

## 15. Trabajo futuro

- Evaluar sincronización continua del gemelo.
- Incorporar nuevos dispositivos y escenarios de falla.
- Evaluar servicios de aplicación además de ICMP.
- Incorporar verificadores de configuración.
- Evaluar mecanismos de reversión automática.
- Evaluar alternativas de IA local.

Estas ampliaciones no forman parte de las capacidades validadas en el escenario actual.

## 16. Referencias

Las referencias bibliográficas se encuentran en [documento/](documento/).

El artículo reúne trabajos académicos, documentación técnica oficial y referencias de arquitectura y protocolos, con un formato de citación consistente.