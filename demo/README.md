## Requisitos de red y acceso

El laboratorio utiliza una red de gestión Host-only
192.168.57.0/24. Las cuentas y el firewall de los routers permiten
administración por SSH únicamente desde 192.168.57.1.

Para reproducirlo en otra computadora se debe:

1. Instalar GNS3 y el entorno de virtualización compatible.
2. Importar los proyectos con los discos necesarios.
3. Configurar el adaptador Host-only del equipo administrador con
   192.168.57.1/24 y conectar la Cloud de GNS3 a ese adaptador.
4. Comprobar que la subred no se solape con otras redes del equipo
   y que las IP estáticas de los routers estén disponibles.
5. Preparar las credenciales locales mediante el procedimiento de
   instalación. Las contraseñas y el archivo .env no se incluyen
   en el repositorio.
6. Verificar el acceso SSH y ejecutar las pruebas documentadas.

Si se utiliza otra dirección para el administrador, deben adaptarse
tanto las restricciones de las cuentas como las reglas del firewall.
El cambio debe realizarse desde la consola de GNS3 para evitar perder
el acceso remoto.

La portabilidad a otra computadora está pendiente de validación.