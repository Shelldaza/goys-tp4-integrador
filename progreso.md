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
| 26/10/2026 | Se definió la modalidad B y el alcance de una demo de diagnóstico con EMPRESA y GEMELO en GNS3. | Facundo | Por completar |
| 26/10/2026 | Se propuso distribuir las responsabilidades: Facundo desarrolla la demo y aporta evidencias, mientras que Irineo prepara la investigación, el artículo y el póster. | Ambos | Por completar |
| 26/10/2026 | Se decidió excluir la sincronización automática del gemelo y el control de proyectos y nodos mediante la IA para reducir la complejidad. | Facundo | Por completar |
| 27/10/2026 | Se configuró la identidad de Git y se agregaron en documento/fuentes.md las 10 fuentes iniciales con la cobertura de requisitos del artículo. | Irineo | Por completar |
| 27/10/2026 | Se reunieron y verificaron 9 fuentes (artículos científicos, RFC, Internet-Draft del IRTF, documentación oficial y guía de seguridad) y se registraron en documento/fuentes.md con su cobertura de requisitos. | Irineo | Rama documentos-irineo |
| 27/10/2026 | Se descartó una fuente comunitaria (servidor MCP para GNS3) por no tener autor ni fecha verificables y para ajustar la extensión del artículo; se actualizó fuentes.md. | Irineo | Rama documentos-irineo |
| 27/10/2026 | Se redactó en Word online el borrador del artículo de modalidad B (resumen, secciones 1 a 5 y referencias en APA 7). Pendiente: Figura 1 y actualización de la sección 3.4. | Irineo | Todavía no subido al repo |

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
- [ ] Incorporar y revisar el README 
- [ ] Construir los dos entornos de GNS3.
- [ ] Configurar direccionamiento, OSPF, firewall y permisos diferenciados.
- [ ] Implementar las herramientas MCP definitivas.
- [ ] Preparar una falla reproducible de firewall.
- [ ] Verificar diagnóstico, corrección en GEMELO y conservación de los bloqueos requeridos.
- [ ] Ejecutar al menos tres pruebas completas y registrar resultados.
- [ ] Preparar capturas y grabación de respaldo.
- [x] Investigar y seleccionar las referencias bibliográficas.
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