"""Conexiones SSH de lectura a equipos del inventario."""

import json
import logging
from contextlib import contextmanager
from pathlib import Path

import paramiko

from configuracion import (
    INVENTARIO,
    cargar_credenciales,
    obtener_equipo,
    seleccionar_credencial,
)


logging.getLogger("paramiko").setLevel(logging.WARNING)

KNOWN_HOSTS = Path.home() / ".ssh" / "known_hosts"


class ErrorSSH(RuntimeError):
    """Error de conexion o validacion, sin incluir secretos."""


def _consultar_texto(cliente: paramiko.SSHClient, comando: str) -> str:
    """Funcion interna; los comandos proceden del codigo del servidor."""
    entrada, salida, errores = cliente.exec_command(comando, timeout=15)
    entrada.close()

    try:
        texto = salida.read().decode("utf-8", errors="replace").strip()
        error = errores.read().decode("utf-8", errors="replace").strip()
        estado = salida.channel.recv_exit_status()

        marcas_error = (
            "failure:",
            "syntax error",
            "bad command name",
            "expected end of command",
            "not enough permissions",
            "input does not match",
        )

        if estado != 0 or error or any(
            marca in texto.lower() for marca in marcas_error
        ):
            raise ErrorSSH("RouterOS rechazo la consulta.")

        return texto
    finally:
        salida.channel.close()


@contextmanager
def conectar_lectura(nombre: str, credenciales: dict[str, str]):
    equipo = obtener_equipo(nombre)
    credencial = seleccionar_credencial(equipo, credenciales)

    if not KNOWN_HOSTS.is_file():
        raise ErrorSSH(
            "No existe known_hosts. Registrar y verificar "
            "las claves de host mediante SSH local."
        )

    cliente = paramiko.SSHClient()

    try:
        cliente.load_host_keys(str(KNOWN_HOSTS))
        cliente.set_missing_host_key_policy(paramiko.RejectPolicy())

        cliente.connect(
            hostname=equipo.ip,
            port=22,
            username=credencial.usuario,
            password=credencial.password,
            look_for_keys=False,
            allow_agent=False,
            timeout=10,
            auth_timeout=10,
            banner_timeout=15,
            channel_timeout=15,
        )

        identidad = _consultar_texto(
            cliente, ":put [/system identity get name]"
        )
        mac = _consultar_texto(
            cliente,
            ':put [/interface ethernet get '
            '[find where name="ether1"] mac-address]',
        ).upper()

        if identidad != equipo.nombre:
            raise ErrorSSH("La identidad no coincide con el inventario.")

        if mac != equipo.mac_gestion:
            raise ErrorSSH("La MAC de gestion no coincide con el inventario.")

        yield cliente

    except paramiko.BadHostKeyException:
        raise ErrorSSH(
            "La clave de host cambio. Verificarla localmente."
        ) from None

    except paramiko.AuthenticationException:
        raise ErrorSSH(
            "Fallo la autenticacion de la cuenta de lectura."
        ) from None

    except (paramiko.SSHException, OSError, EOFError):
        raise ErrorSSH(
            "Fallo SSH: comprobar conectividad y clave de host registrada."
        ) from None

    finally:
        cliente.close()


def verificar_conexiones() -> bool:
    credenciales = cargar_credenciales()
    correcto = True

    for nombre, equipo in INVENTARIO.items():
        try:
            with conectar_lectura(nombre, credenciales):
                resultado = {
                    "equipo": nombre,
                    "ip": equipo.ip,
                    "usuario": "mcp_ro",
                    "estado": "verificado",
                    "comprobaciones": [
                        "clave_host",
                        "autenticacion",
                        "identidad",
                        "mac_gestion",
                    ],
                }

        except (ErrorSSH, ValueError) as error:
            correcto = False
            resultado = {
                "equipo": nombre,
                "estado": "error",
                "detalle": str(error),
            }

        print(json.dumps(resultado, ensure_ascii=False), flush=True)

    return correcto


if __name__ == "__main__":
    try:
        exito = verificar_conexiones()
    except ValueError as error:
        raise SystemExit(str(error)) from None

    raise SystemExit(0 if exito else 1)