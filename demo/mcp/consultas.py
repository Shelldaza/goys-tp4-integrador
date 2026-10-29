"""Consultas RouterOS predefinidas mediante SSH de lectura."""

import argparse
import json
from datetime import datetime, timezone

from configuracion import (
    INVENTARIO,
    cargar_credenciales,
    obtener_equipo,
)
from conexion_ssh import ErrorSSH, _consultar_texto, conectar_lectura


CONSULTAS = {
    "identidad": "/system identity print",
    "version": ":put [/system resource get version]",
    "interfaces": "/interface print without-paging",
    "direcciones": "/ip address print without-paging",
    "rutas": "/ip route print without-paging",
    "ospf": "/routing ospf neighbor print detail without-paging",
    "ospf_config": (
        "/routing ospf interface-template print without-paging "
        "proplist=interfaces,area,type,cost,passive,auth,auth-id,comment"
    ),
    "firewall": "/ip firewall filter print without-paging",
    "contadores": "/ip firewall filter print stats without-paging",
}


def consultar_router(
    nombre: str,
    consulta: str,
    credenciales: dict[str, str],
) -> dict:
    equipo = obtener_equipo(nombre)

    if consulta not in CONSULTAS:
        raise ValueError("Consulta fuera de las operaciones permitidas.")

    with conectar_lectura(nombre, credenciales) as cliente:
        salida = _consultar_texto(cliente, CONSULTAS[consulta])

    return {
        "estado": "leido",
        "equipo": equipo.nombre,
        "ip": equipo.ip,
        "consulta": consulta,
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "salida": salida,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Consulta predefinida de un router del laboratorio."
    )
    parser.add_argument("equipo", choices=sorted(INVENTARIO))
    parser.add_argument("consulta", choices=sorted(CONSULTAS))
    argumentos = parser.parse_args()

    try:
        credenciales = cargar_credenciales()
        resultado = consultar_router(
            argumentos.equipo,
            argumentos.consulta,
            credenciales,
        )
        codigo = 0

    except (ErrorSSH, ValueError) as error:
        resultado = {
            "estado": "error",
            "equipo": argumentos.equipo,
            "consulta": argumentos.consulta,
            "detalle": str(error),
        }
        codigo = 1

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    return codigo


if __name__ == "__main__":
    raise SystemExit(main())