# Desarrollo de la demostración — TP4

## Fase 0 — Diseño de la red

### 0.1. Objetivo y alcance

La demostración utiliza dos proyectos independientes en GNS3:

- **EMPRESA:** representa la red operativa y permite consultas de lectura.
- **GEMELO:** reproduce el escenario y permite probar correcciones.

Se investigará un bloqueo de firewall, se probará una solución en GEMELO y se entregará una recomendación sin modificar EMPRESA.

El gemelo se preparará manualmente. No se implementarán sincronización automática, descubrimiento de dispositivos ni control del inicio de nodos.

### 0.2. Topología y dispositivos

Cada proyecto tendrá tres MikroTik CHR, dos VPCS, un switch de gestión y una Cloud conectada a la red Host-only.

| Equipo | Función |
|---|---|
| R1 | Conecta la LAN de usuarios |
| R2 | Proporciona un camino alternativo |
| R3 | Conecta la LAN del servidor |
| PC | Inicia las pruebas de conectividad |
| SRV | Representa el destino de las pruebas |
| Switch y Cloud | Permiten administrar los routers desde Windows |

Los routers forman un triángulo. El enlace R1–R3 será el camino principal y R1–R2–R3 será la alternativa.

SRV es un VPCS: se comprobará conectividad ICMP, no servicios de aplicación.

### 0.3. Cableado

El esquema se repite en ambos proyectos con dispositivos independientes.

| Extremo A | Interfaz A | Extremo B | Interfaz B |
|---|---|---|---|
| PC | Ethernet0 | R1 | ether2 |
| SRV | Ethernet0 | R3 | ether2 |
| R1 | ether3 | R2 | ether3 |
| R2 | ether4 | R3 | ether3 |
| R1 | ether4 | R3 | ether4 |
| R1 | ether1 | Switch de gestión | Puerto 0 |
| R2 | ether1 | Switch de gestión | Puerto 1 |
| R3 | ether1 | Switch de gestión | Puerto 2 |
| Switch de gestión | Puerto 3 | Cloud | Interfaz Host-only |

En GNS3, `e0` corresponde a `ether1` de RouterOS, `e1` a `ether2`, y así sucesivamente. En R2, `ether2` queda libre.

**Evidencia pendiente:** incorporar una captura de la topología completa, con nombres y enlaces visibles, acompañada de una leyenda numerada.

### 0.4. Plan de direccionamiento

#### Gestión

Se reservará `ether1` para administración.

| Router | EMPRESA | GEMELO |
|---|---|---|
| R1 | 192.168.57.10/24 | 192.168.57.20/24 |
| R2 | 192.168.57.11/24 | 192.168.57.21/24 |
| R3 | 192.168.57.12/24 | 192.168.57.22/24 |

Se eligen IP estáticas para mantener accesos conocidos y evitar depender de concesiones DHCP. Las direcciones deberán estar libres y fuera del pool DHCP.

Se deshabilitará únicamente el cliente DHCP de estas interfaces para evitar una segunda dirección dinámica innecesaria. Esto no impide usar DHCP en otras redes.

#### Redes internas

| Segmento | Extremo A | Extremo B |
|---|---|---|
| LAN usuarios — 10.10.0.0/24 | R1 ether2: 10.10.0.1 | PC: 10.10.0.10 |
| LAN servidor — 10.20.0.0/24 | R3 ether2: 10.20.0.1 | SRV: 10.20.0.10 |
| R1–R2 — 10.0.12.0/30 | R1 ether3: 10.0.12.1 | R2 ether3: 10.0.12.2 |
| R2–R3 — 10.0.23.0/30 | R2 ether4: 10.0.23.1 | R3 ether3: 10.0.23.2 |
| R1–R3 — 10.0.13.0/30 | R1 ether4: 10.0.13.1 | R3 ether4: 10.0.13.2 |

PC utilizará gateway `10.10.0.1` y SRV, `10.20.0.1`.

Los enlaces entre routers usarán `/30` porque necesitan dos direcciones de host. Las LAN usarán `/24` para mantener un esquema sencillo y diferenciar usuarios de servidores.

#### Loopbacks

| Router | Dirección en lo | Router ID |
|---|---|---|
| R1 | 10.255.0.1/32 | 10.255.0.1 |
| R2 | 10.255.0.2/32 | 10.255.0.2 |
| R3 | 10.255.0.3/32 | 10.255.0.3 |

Se utilizará la interfaz `lo` nativa de los CHR y se configurarán los Router ID explícitamente.

Las IP internas se repetirán en GEMELO porque sus redes de datos estarán separadas de EMPRESA. Las direcciones de gestión serán diferentes para acceder simultáneamente a ambos entornos.

### 0.5. Enrutamiento

Se utilizará OSPFv2 en el área backbone `0.0.0.0`.

| Enlace | Costo por extremo |
|---|---|
| R1–R3 | 10 |
| R1–R2 | 20 |
| R2–R3 | 20 |

Los costos favorecerán el enlace directo R1–R3. OSPF se elige para intercambiar rutas y disponer de un camino alternativo sin configurar rutas estáticas para cada destino.

Las vecindades se formarán únicamente entre routers. Las LAN y loopbacks serán pasivas; la red de gestión no participará en OSPF.

Se verificarán vecinos FULL, rutas a las LAN remotas y preferencia del camino principal. La autenticación OSPF queda fuera de esta configuración inicial.

### 0.6. Seguridad y separación de entornos

Se aplicarán estos controles:

- SSH restringido al equipo administrador autorizado.
- Cuentas específicas y deshabilitación de servicios innecesarios.
- Lectura en EMPRESA y modificaciones controladas en GEMELO durante la demo.
- Bloqueo del tránsito entre las redes de datos y la interfaz de gestión.
- Contraseñas fuera del repositorio y de las capturas.

No se conectarán entre sí las LAN de ambos proyectos ni se crearán bridges entre gestión y datos.

GEMELO tendrá nodos, discos, identidades y credenciales independientes. Antes de utilizarlo se comprobará que reproduce la configuración relevante y el comportamiento de EMPRESA.

### 0.7. Falla y criterios de éxito

Se introducirá en R1 una regla que bloquee por error ICMP desde `10.10.0.10` hacia `10.20.0.10`. Los enlaces y OSPF permanecerán funcionando.

La política del laboratorio permitirá ese tráfico, pero bloqueará desde PC el acceso a la loopback de R3 (`10.255.0.3`). Este segundo destino permitirá verificar que la corrección conserva una restricción de seguridad.

| Comprobación tras corregir GEMELO | Resultado esperado |
|---|---|
| GEMELO-PC → 10.20.0.10 | Responde |
| GEMELO-PC → 10.255.0.3 | Sigue bloqueado |
| OSPF y rutas de GEMELO | Continúan operativos |
| EMPRESA-PC → 10.20.0.10 | Sigue bloqueado |

Se contrastarán los pings con los contadores del firewall. Un timeout por sí solo no demuestra que una regla esté bloqueando tráfico.

La solución será válida si recupera la comunicación permitida sin eliminar los bloqueos requeridos. No se aceptará desactivar todo el firewall.

Las pruebas desde VPCS serán manuales. Se realizarán tres recorridos completos y se preparará una grabación de respaldo.

## Fase 1 — Identificación y acceso de gestión

Se documentarán nombres, IP estáticas, deshabilitación del cliente DHCP y acceso SSH, con sus comandos y capturas.

## Fase 2 — Direccionamiento interno y hosts

Pendiente: configurar LAN, enlaces, loopbacks y VPCS. Comprobar conectividad entre vecinos directos.

## Fase 3 — Enrutamiento OSPF

Pendiente: configurar OSPF y costos. Verificar vecinos FULL, rutas y comunicación entre LAN.

## Fase 4 — Seguridad

Pendiente: configurar cuentas, restricciones de gestión y firewall. Comprobar accesos permitidos y bloqueados.

## Fase 5 — Preparación del gemelo

Pendiente: crear una copia independiente, adaptar su gestión y verificar la equivalencia del escenario.

## Fase 6 — Integración de IA mediante MCP

Pendiente: documentar las herramientas definitivas, con lectura en EMPRESA y modificaciones controladas en GEMELO.

## Fase 7 — Escenario de falla y validación

Pendiente: introducir la falla en ambos entornos, diagnosticarla y probar la corrección únicamente en GEMELO.

## Fase 8 — Ensayos y respaldo

Pendiente: registrar tres ejecuciones completas, ajustar la demo a 3–5 minutos y comprobar el respaldo grabado.
