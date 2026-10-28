# Bitácora del grupo 3 - TP4

> Registro de avances, aportes de cada integrante, decisiones y pendientes.
> Solo se registran como realizadas las actividades efectivamente completadas.

---

## 👥 Integrantes

| Nombre | Usuario de GitHub | Rol en el grupo |
|--------|-------------------|-----------------|
| Facundo Daza | Shelldaza | Implementación de la demo, integración MCP, seguridad, pruebas y documentación técnica |
| Irineo Hiriart | IrineoHiriart215 | Investigación bibliográfica, artículo de revisión y póster |

Ambos participan en la revisión del trabajo, el registro de avances y la defensa.

## 🎯 Proyecto

- **Modalidad:** B — Artículo de Revisión del Estado del Arte.
- **Tema:** Inteligencia artificial aplicada al diagnóstico de redes mediante MCP y gemelos digitales.
- **Problema/objetivo:** Investigar cómo integrar IA y herramientas de administración de redes para diagnosticar problemas y evaluar correcciones en un entorno separado antes de recomendarlas para una red operativa.
- **Demostración:** Dos proyectos independientes en GNS3: EMPRESA, con acceso de lectura para la IA, y GEMELO, donde se permiten modificaciones controladas.

## 🗓️ Registro de avance

| Fecha | Qué se hizo | Quién | Commit |
|-------|-------------|-------|--------|
| Prueba previa - 09/10/2026 | Se implementó una prueba de concepto para ver la viabilidad del proyecto con un servidor MCP en Python conectado por SSH a un router MikroTik en GNS3. Se comprobó su funcionamiento desde ChatGPT mediante un túnel. | Facundo | Realizada localmente, sin commit. |
| Prueba previa - 09/10/2026 | Se cambió manualmente el nombre del router y se volvió a consultar mediante MCP para comprobar que la respuesta provenía del equipo en vivo. | Facundo | Realizada localmente, sin commit. |
| 26/10/2026 | Se definió la modalidad B y el alcance de una demo de diagnóstico con EMPRESA y GEMELO en GNS3. | Facundo | e1015cd |
| 26/10/2026 | Se propuso distribuir las responsabilidades: Facundo desarrolla la demo y aporta evidencias, mientras que Irineo prepara la investigación, el artículo y el póster. | Ambos | e1015cd  |
| 26/10/2026 | Se decidió excluir la sincronización automática del gemelo y el control de proyectos y nodos mediante la IA para reducir la complejidad. | Facundo | e1015cd |
| 27/10/2026 | Se configuró la identidad de Git y se agregaron en documento/fuentes.md las 10 fuentes iniciales con la cobertura de requisitos del artículo. | Irineo | d720509 |
| 27/10/2026 | Se creó demo/DesarrolloDemo.md y se documentó la Fase 0: topología, cableado, direccionamiento previsto, decisiones de diseño, seguridad y criterios de validación. Se definieron las fases restantes de implementación. | Facundo | 360a5e4 |
| 27/10/2026 | Se documentó la Fase 1 en demo/DesarrolloDemo.md y se incorporaron capturas de topología, identidades, IP estáticas, DHCP deshabilitado y acceso SSH. Se verificó que las direcciones de gestión quedan fuera del pool DHCP de VMnet1. | Facundo | bf59f3d |
| 27/10/2026 | Se configuraron las LAN, los enlaces internos, las loopbacks y las VPCS de EMPRESA. Se verificaron los tres enlaces entre routers en ambos sentidos y el acceso de cada host a su gateway, sin pérdidas en las pruebas. Se documentó F2 y se incorporaron ocho capturas. | Facundo | 19820b3 |
| 27/10/2026 | Se configuró OSPFv2 en área 0 con Router ID explícitos, interfaces pasivas y costos que favorecen R1–R3. Se verificaron dos vecinos FULL por router, rutas aprendidas y comunicación entre PC y SRV en ambos sentidos. Se documentó F3 y se incorporaron cinco capturas. | Facundo | 695761c |
| 28/10/2026 | Se configuró y documentó la seguridad de EMPRESA: cuentas y permisos, restricciones de gestión, servicios e interfaces sin uso deshabilitados, filtrado IPv4, bloqueo de entrada y tránsito IPv6 y autenticación OSPF SHA256. Se verificaron tráfico permitido y bloqueado, rechazo de escritura, prueba OSPF con clave incorrecta y recuperación, y acceso al puerto SSH desde orígenes autorizado y no autorizado. Se incorporaron 18 capturas y se documentaron las limitaciones. | Facundo | 64592db |

Las pruebas previas se registran retrospectivamente. Completar sus fechas y referencias a commits cuando se disponga de esos datos.

## 🚧 Pendientes / decisiones

### Decisiones tomadas

- [x] Elegir modalidad B.
- [x] Definir el tema del trabajo.
- [x] Utilizar GNS3 para representar tanto la red operativa como el gemelo.
- [x] Mantener EMPRESA con acceso de lectura para la IA.
- [x] Permitir pruebas de corrección únicamente en GEMELO.
- [x] Preparar e iniciar los proyectos manualmente.
- [x] Excluir la sincronización automática del gemelo.
- [x] Entregar una recomendación sin aplicar cambios automáticamente sobre EMPRESA.

### Pendientes

- [x] Completar el usuario de GitHub de Irineo.
- [x] Confirmar aceptación del reparto de tareas entre ambos.
- [ ] Verificar colaboradores del grupo y docentes en el repositorio.
- [x] Incorporar y revisar el README 
- [x] Documentar el diseño de la demo y las fases de implementación.
- [x] Documentar la Fase 1 e incorporar capturas de la configuración de gestión.
- [x] Configurar el direccionamiento interno, las loopbacks y las VPCS de EMPRESA.
- [x] Verificar y documentar F2 con sus capturas.
- [x] Configurar OSPF y comprobar conectividad entre las LAN.
- [x] Documentar F3 e incorporar sus capturas.
- [x] Configurar y documentar la seguridad de EMPRESA.
- [x] Verificar permisos, filtrado y autenticación OSPF mediante pruebas positivas y negativas.
- [ ] Aplicar y verificar los permisos definitivos de la integración: lectura en EMPRESA y modificaciones controladas en GEMELO.
- [ ] Preparar GEMELO y verificar su independencia y equivalencia con EMPRESA.
- [ ] Implementar las herramientas MCP definitivas.
- [ ] Preparar una falla reproducible de firewall.
- [ ] Verificar diagnóstico, corrección en GEMELO y conservación de los bloqueos requeridos.
- [ ] Ejecutar al menos tres pruebas completas y registrar resultados.
- [ ] Preparar capturas y grabación de respaldo.
- [ ] Investigar y seleccionar las referencias bibliográficas.
- [ ] Redactar y revisar el artículo de modalidad B.
- [ ] Diseñar y revisar el póster A1.
- [ ] Completar el checklist oficial y ensayar la presentación.

## 📝 Notas

- La conexión MCP con un router ya fue comprobada como prueba de concepto. Esto no significa que la demo completa esté implementada.
- El gemelo se prepara manualmente y reproduce únicamente el escenario definido. Su equivalencia debe comprobarse antes de las pruebas.
- El escenario propuesto consiste en una regla incorrecta de firewall que bloquea ICMP entre dos hosts.
- Las pruebas desde VPCS serán manuales y se contrastarán con los contadores del firewall.
- La interacción con ChatGPT mediante el túnel requiere Internet. Se preparará una grabación local como respaldo.
- No se subirán contraseñas, claves, imágenes de máquinas virtuales ni archivos pesados al repositorio.
- Cada integrante registrará sus aportes reales y realizará commits con su propia identidad.
- El artículo y el póster deberán distinguir las funcionalidades implementadas de las propuestas como trabajo futuro.