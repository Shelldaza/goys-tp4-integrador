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

![Topología de EMPRESA en GNS3 con routers, hosts y red de gestión](../capturas/fase0/01-topologia-empresa.png)

*Figura 1: Topología de EMPRESA y conexiones de gestión.*

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

### 1.1. Objetivo

Establecer nombres y direcciones estáticas de gestión para los tres routers, y comprobar su acceso mediante SSH desde Windows.

### 1.2. Inspección

Se consultaron las interfaces, direcciones y servicios disponibles:

```routeros
/system identity print
/interface print
/ip address print
/ip dhcp-client print
/ip service print
```

Se identificó `ether1` como interfaz de gestión y se comprobó que los routers disponen de una interfaz loopback nativa llamada `lo`.

### 1.3. Configuración de los routers

Los siguientes comandos permiten reproducir la configuración. Antes de ejecutar una instrucción `add`, se debe comprobar que la dirección no exista para evitar duplicados.

#### EMPRESA-R1

```routeros
/system identity set name=EMPRESA-R1
/ip address add address=192.168.57.10/24 interface=ether1 comment="Gestion fija MCP"
/ip dhcp-client disable [find where interface=ether1]
```

#### EMPRESA-R2

```routeros
/system identity set name=EMPRESA-R2
/ip address add address=192.168.57.11/24 interface=ether1 comment="Gestion fija MCP"
/ip dhcp-client disable [find where interface=ether1]
```

#### EMPRESA-R3

```routeros
/system identity set name=EMPRESA-R3
/ip address add address=192.168.57.12/24 interface=ether1 comment="Gestion fija MCP"
/ip dhcp-client disable [find where interface=ether1]
```

El comentario es una etiqueta administrativa y no afecta el funcionamiento de la dirección.

### 1.4. Decisiones tomadas

- **Identidades diferentes:** permiten reconocer cada router en las consolas y sesiones remotas. El nombre del nodo en GNS3 no reemplaza la identidad de RouterOS.
- **Direcciones estáticas:** mantienen accesos conocidos sin depender de concesiones DHCP.
- **Cliente DHCP deshabilitado en ether1:** evita recibir una dirección dinámica adicional en gestión. No implica deshabilitar DHCP en toda la red.
- **Interfaz dedicada a gestión:** separa el cableado de administración del utilizado para las LAN y los enlaces entre routers.

Las restricciones de acceso y los permisos definitivos se configurarán en la fase de seguridad.

### 1.5. Verificación

En cada router se ejecutaron:

```routeros
/system identity print
/ip address print
/ip dhcp-client print
```

Las capturas muestran el siguiente estado:

| Router | Identidad | Dirección en ether1 | Cliente DHCP |
|---|---|---|---|
| R1 | EMPRESA-R1 | 192.168.57.10/24 | Deshabilitado |
| R2 | EMPRESA-R2 | 192.168.57.11/24 | Deshabilitado |
| R3 | EMPRESA-R3 | 192.168.57.12/24 | Deshabilitado |

Las direcciones aparecen sin la bandera `D` de dinámicas. El cliente DHCP muestra la bandera `X` de deshabilitado.

Los valores `yes` en `USE-PEER-DNS` y `ADD-DEFAULT-ROUTE` son opciones del cliente; no indican que esté activo.

![Identidad, dirección estática y cliente DHCP deshabilitado en EMPRESA-R1](../capturas/fase1/01-gestion-r1.png)

*Figura 2: Configuración de gestión de EMPRESA-R1.*

![Identidad, dirección estática y cliente DHCP deshabilitado en EMPRESA-R2](../capturas/fase1/02-gestion-r2.png)

*Figura 3: Configuración de gestión de EMPRESA-R2.*

![Identidad, dirección estática y cliente DHCP deshabilitado en EMPRESA-R3](../capturas/fase1/03-gestion-r3.png)

*Figura 4: Configuración de gestión de EMPRESA-R3.*

### 1.6. Acceso SSH desde Windows

Cada conexión se realiza por separado:

```powershell
ssh admin@192.168.57.10
ssh admin@192.168.57.11
ssh admin@192.168.57.12
```

En el primer acceso, la huella de la clave de host debe verificarse antes de aceptarla.

Dentro de la sesión se consulta:

```routeros
/system identity print
```

La identidad debe coincidir con el router de destino. Para cerrar la sesión:

```routeros
/quit
```

Se comprobó el acceso a los tres routers. La siguiente captura muestra la conexión a EMPRESA-R2 como ejemplo representativo.

![Conexión SSH desde Windows a 192.168.57.11 y respuesta de identidad EMPRESA-R2](../capturas/fase1/04-acceso-ssh.png)

*Figura 5: Verificación del acceso de administración mediante SSH.*

Las contraseñas se ingresan localmente y no se incluyen en capturas ni archivos del repositorio.

### 1.7. Resultado 

Los tres routers quedaron identificados y accesibles mediante sus direcciones estáticas de gestión.

Se comprobó que VMnet1 utiliza el rango DHCP
192.168.57.128–192.168.57.254. Las direcciones estáticas
de EMPRESA y las previstas para GEMELO quedan fuera de ese rango.

![Rango DHCP de VMnet1 en VMware](../capturas/fase1/05-rango-dhcp.png)

*Figura 6: Rango DHCP de la red de gestión.*
Esta fase verifica el acceso de administración. La conectividad entre LAN se comprobará después de configurar el direccionamiento interno y OSPF.

La cuenta `admin` se utiliza temporalmente durante el armado. Las cuentas definitivas y las restricciones de servicios se configurarán en la fase 4.

## Fase 2 — Direccionamiento interno y hosts

### 2.1. Objetivo

Asignar direcciones a las LAN, los enlaces entre routers, las loopbacks y los hosts. Verificar conectividad entre vecinos directos antes de configurar OSPF.

### 2.2. Configuración de los routers

Se conservaron las direcciones de gestión de `ether1`. Las direcciones internas se asignaron según el diseño de F0.

Los siguientes comandos documentan la configuración aplicada. No deben repetirse sin comprobar las entradas existentes.

#### EMPRESA-R1

```routeros
/ip address add address=10.10.0.1/24 interface=ether2 comment="F2 LAN usuarios"
/ip address add address=10.0.12.1/30 interface=ether3 comment="F2 enlace R1-R2"
/ip address add address=10.0.13.1/30 interface=ether4 comment="F2 enlace R1-R3"
/ip address add address=10.255.0.1/32 interface=lo comment="F2 loopback R1"
```

#### EMPRESA-R2

```routeros
/ip address add address=10.0.12.2/30 interface=ether3 comment="F2 enlace R2-R1"
/ip address add address=10.0.23.1/30 interface=ether4 comment="F2 enlace R2-R3"
/ip address add address=10.255.0.2/32 interface=lo comment="F2 loopback R2"
```

#### EMPRESA-R3

```routeros
/ip address add address=10.20.0.1/24 interface=ether2 comment="F2 LAN servidor"
/ip address add address=10.0.23.2/30 interface=ether3 comment="F2 enlace R3-R2"
/ip address add address=10.0.13.2/30 interface=ether4 comment="F2 enlace R3-R1"
/ip address add address=10.255.0.3/32 interface=lo comment="F2 loopback R3"
```

### 2.3. Configuración de los hosts

#### EMPRESA-PC

```text
ip 10.10.0.10 255.255.255.0 10.10.0.1
save
```

#### EMPRESA-SRV

```text
ip 10.20.0.10 255.255.255.0 10.20.0.1
save
```

Se configuraron direcciones estáticas para mantener extremos conocidos durante las pruebas. Cada gateway corresponde al router de su propia LAN.

El comando `save` conserva la configuración de VPCS para futuros inicios. No se configuró DNS porque las pruebas utilizan direcciones IP.

Las loopbacks usan `/32` para representar una dirección de cada router; posteriormente se utilizarán como referencia para los Router ID de OSPF.

### 2.4. Verificación de direcciones y rutas

En cada router se consultaron:

```routeros
/ip address print without-paging
/ip route print without-paging
```

Se verificaron las direcciones asignadas y la presencia de rutas conectadas activas. Estas rutas permiten alcanzar las redes directamente conectadas; todavía no proporcionan comunicación entre las LAN remotas.

![Direcciones y rutas conectadas de EMPRESA-R1](../capturas/fase2/01-direcciones-r1.png)

*Figura 7: Direccionamiento y rutas conectadas de EMPRESA-R1.*

![Direcciones y rutas conectadas de EMPRESA-R2](../capturas/fase2/02-direcciones-r2.png)

*Figura 8: Direccionamiento y rutas conectadas de EMPRESA-R2.*

![Direcciones y rutas conectadas de EMPRESA-R3](../capturas/fase2/03-direcciones-r3.png)

*Figura 9: Direccionamiento y rutas conectadas de EMPRESA-R3.*

### 2.5. Pruebas entre routers

Se ejecutaron pings con dirección de origen explícita para comprobar cada enlace de datos.

#### Desde R1

```routeros
/ping address=10.0.12.2 src-address=10.0.12.1 count=5
/ping address=10.0.13.2 src-address=10.0.13.1 count=5
```

#### Desde R2

```routeros
/ping address=10.0.12.1 src-address=10.0.12.2 count=5
/ping address=10.0.23.2 src-address=10.0.23.1 count=5
```

#### Desde R3

```routeros
/ping address=10.0.23.1 src-address=10.0.23.2 count=5
/ping address=10.0.13.1 src-address=10.0.13.2 count=5
```

| Prueba | Resultado observado |
|---|---|
| R1 → R2 | 5 enviados, 5 recibidos |
| R2 → R1 | 5 enviados, 5 recibidos |
| R2 → R3 | 5 enviados, 5 recibidos |
| R3 → R2 | 5 enviados, 5 recibidos |
| R1 → R3 | 5 enviados, 5 recibidos |
| R3 → R1 | 5 enviados, 5 recibidos |

Los tres enlaces respondieron en ambos sentidos, sin pérdidas en estas pruebas.

![Pruebas desde R1 hacia sus vecinos R2 y R3](../capturas/fase2/06-ping-vecinos-r1.png)

*Figura 10: Verificación de los enlaces desde EMPRESA-R1.*

![Pruebas desde R2 hacia sus vecinos R1 y R3](../capturas/fase2/07-ping-vecinos-r2.png)

*Figura 11: Verificación de los enlaces desde EMPRESA-R2.*

![Pruebas desde R3 hacia sus vecinos R2 y R1](../capturas/fase2/08-ping-vecinos-r3.png)

*Figura 12: Verificación de los enlaces desde EMPRESA-R3.*

### 2.6. Pruebas de los hosts

En cada VPCS se consultó su configuración y se realizó un ping al gateway.

#### EMPRESA-PC

```text
show ip
ping 10.10.0.1
```

#### EMPRESA-SRV

```text
show ip
ping 10.20.0.1
```

| Host | Dirección | Gateway | Resultado observado |
|---|---|---|---|
| EMPRESA-PC | 10.10.0.10/24 | 10.10.0.1 | 5 respuestas de 5 |
| EMPRESA-SRV | 10.20.0.10/24 | 10.20.0.1 | 5 respuestas de 5 |

![Configuración de EMPRESA-PC y ping a su gateway](../capturas/fase2/04-pc-gateway.png)

*Figura 13: Conectividad de EMPRESA-PC con R1.*

![Configuración de EMPRESA-SRV y ping a su gateway](../capturas/fase2/05-srv-gateway.png)

*Figura 14: Conectividad de EMPRESA-SRV con R3.*

### 2.7. Resultado

Quedaron configuradas las direcciones internas y las loopbacks de los tres routers, junto con las direcciones y gateways de las dos VPCS.

Se comprobó conectividad en ambos sentidos de los enlaces entre routers y desde cada host hacia su gateway.

La comunicación entre LAN se verificará en F3, después de configurar OSPF.

## Fase 3 — Enrutamiento OSPF

### 3.1. Objetivo

Intercambiar rutas entre los tres routers mediante OSPF y comprobar la comunicación entre las LAN, utilizando el enlace directo R1–R3 como camino preferido.

### 3.2. Configuración aplicada

Se creó una instancia OSPFv2 por router y se utilizaron las direcciones de las loopbacks como Router ID. Los tres equipos pertenecen al área backbone `0.0.0.0`.

Los comandos ya fueron aplicados. Antes de repetir instrucciones `add`, comprobar las entradas existentes para evitar duplicados.

#### EMPRESA-R1

```routeros
/routing ospf instance add name=ospf-v2 version=2 router-id=10.255.0.1
/routing ospf area add name=backbone instance=ospf-v2 area-id=0.0.0.0
/routing ospf interface-template add area=backbone interfaces=ether3 type=ptp cost=20 comment="F3 R1-R2"
/routing ospf interface-template add area=backbone interfaces=ether4 type=ptp cost=10 comment="F3 R1-R3"
/routing ospf interface-template add area=backbone interfaces=ether2 passive cost=1 comment="F3 LAN usuarios"
/routing ospf interface-template add area=backbone interfaces=lo passive cost=1 comment="F3 loopback R1"
```

#### EMPRESA-R2

```routeros
/routing ospf instance add name=ospf-v2 version=2 router-id=10.255.0.2
/routing ospf area add name=backbone instance=ospf-v2 area-id=0.0.0.0
/routing ospf interface-template add area=backbone interfaces=ether3 type=ptp cost=20 comment="F3 R2-R1"
/routing ospf interface-template add area=backbone interfaces=ether4 type=ptp cost=20 comment="F3 R2-R3"
/routing ospf interface-template add area=backbone interfaces=lo passive cost=1 comment="F3 loopback R2"
```

#### EMPRESA-R3

```routeros
/routing ospf instance add name=ospf-v2 version=2 router-id=10.255.0.3
/routing ospf area add name=backbone instance=ospf-v2 area-id=0.0.0.0
/routing ospf interface-template add area=backbone interfaces=ether3 type=ptp cost=20 comment="F3 R3-R2"
/routing ospf interface-template add area=backbone interfaces=ether4 type=ptp cost=10 comment="F3 R3-R1"
/routing ospf interface-template add area=backbone interfaces=ether2 passive cost=1 comment="F3 LAN servidor"
/routing ospf interface-template add area=backbone interfaces=lo passive cost=1 comment="F3 loopback R3"
```

En esta versión de RouterOS, las interfaces pasivas se configuran con `passive`, sin `=yes`.

### 3.3. Decisiones tomadas

- **Área única:** los tres routers pertenecen al backbone; no se requiere un diseño multiárea para este laboratorio.
- **Router ID explícitos:** permiten identificar los equipos de forma estable.
- **Enlaces punto a punto:** cada enlace conecta dos routers, por lo que se utiliza `type=ptp`, sin elección de DR y BDR.
- **Interfaces pasivas:** las LAN y loopbacks se anuncian sin formar vecindades por ellas.
- **Gestión excluida:** no se creó una plantilla para `ether1` ni se redistribuyeron todas las redes conectadas.
- **Costos diferenciados:** el enlace R1–R3 tiene costo 10 y cada enlace por R2 tiene costo 20. Esto favorece el camino directo.

Las interfaces pasivas de LAN y loopback tienen costo 1. La autenticación OSPF no se configura en esta fase.

### 3.4. Verificación de vecinos y rutas

Se consultaron:

```routeros
/routing ospf neighbor print detail without-paging
/routing ospf interface print detail without-paging
/ip route print without-paging
```

Se comprobó que cada router tiene dos vecinos en estado `Full`:

| Router | Vecinos y sus Router ID |
|---|---|
| R1 | R2 — 10.255.0.2 y R3 — 10.255.0.3 |
| R2 | R1 — 10.255.0.1 y R3 — 10.255.0.3 |
| R3 | R1 — 10.255.0.1 y R2 — 10.255.0.2 |

Las LAN y loopbacks aparecen como pasivas. `ether1` no participa en OSPF.

Las rutas aprendidas se identifican con la bandera `o`. Las rutas activas muestran además la bandera `A`.

| Router | Red remota | Siguiente salto observado |
|---|---|---|
| R1 | 10.20.0.0/24 | 10.0.13.2, por ether4 |
| R2 | 10.10.0.0/24 | 10.0.12.1, por ether3 |
| R2 | 10.20.0.0/24 | 10.0.23.2, por ether4 |
| R3 | 10.10.0.0/24 | 10.0.13.1, por ether4 |

En R2 se observaron dos rutas de igual costo hacia `10.0.13.0/30`, identificadas con `+` de ECMP. Corresponden a caminos por R1 y R3; no son entradas duplicadas incorrectamente.

![Vecinos OSPF y rutas de EMPRESA-R1](../capturas/fase3/01-ospf-rutas-r1.png)

*Figura 15: Vecindades y rutas de EMPRESA-R1.*

![Vecinos OSPF y rutas de EMPRESA-R2](../capturas/fase3/02-ospf-rutas-r2.png)

*Figura 16: Vecindades y rutas de EMPRESA-R2.*

![Vecinos OSPF y rutas de EMPRESA-R3](../capturas/fase3/03-ospf-rutas-r3.png)

*Figura 17: Vecindades y rutas de EMPRESA-R3.*

### 3.5. Comunicación entre las LAN

Desde EMPRESA-PC:

```text
ping 10.20.0.10
trace 10.20.0.10
```

Desde EMPRESA-SRV:

```text
ping 10.10.0.10
```

| Prueba | Resultado |
|---|---|
| PC → SRV | 5 respuestas de 5 |
| SRV → PC | 5 respuestas de 5 |

El traceroute desde PC mostró:

| Salto | Dirección | Equipo |
|---|---|---|
| 1 | 10.10.0.1 | R1 |
| 2 | 10.0.13.2 | R3 |
| 3 | 10.20.0.10 | SRV |

Se confirmó el uso del enlace directo R1–R3.

La respuesta final `Destination port unreachable` corresponde al puerto UDP cerrado utilizado por traceroute. El destino fue alcanzado; no representa una falla del enrutamiento.

![Ping y traceroute desde EMPRESA-PC hacia EMPRESA-SRV](../capturas/fase3/04-pc-srv-trace.png)

*Figura 18: Comunicación hacia SRV y comprobación del camino principal.*

![Ping desde EMPRESA-SRV hacia EMPRESA-PC](../capturas/fase3/05-srv-pc.png)

*Figura 19: Comunicación desde la LAN del servidor hacia la LAN de usuarios.*

### 3.6. Resultado

Los tres routers establecieron vecindades FULL y aprendieron las redes remotas mediante OSPF.

Se verificó comunicación entre los hosts en ambos sentidos y preferencia del enlace directo R1–R3. La red de gestión quedó excluida del protocolo.

La recuperación ante caída del enlace principal no se ensayó en esta fase. El siguiente paso será aplicar las políticas de seguridad.

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
