"""Actualizacion y correccion de la falla exclusivamente en GEMELO-R1."""

import argparse
import json
from threading import Lock

from configuracion import cargar_credenciales
from conexion_ssh import (
    ErrorSSH,
    _consultar_texto,
    conectar_escritura,
)
from firewall_gemelo import (
    CAMPOS_OPERATIVOS,
    COMANDO_LECTURA,
    REGLA_FALLA,
    es_verdadero,
    leer_forward,
)


BLOQUEO = Lock()

BASE_ESPERADA = [
    {
        "comment": "TP4-NO-MGMT-IN",
        "chain": "forward",
        "action": "drop",
        "in-interface": "ether1",
    },
    {
        "comment": "TP4-NO-MGMT-OUT",
        "chain": "forward",
        "action": "drop",
        "out-interface": "ether1",
    },
    {
        "comment": "TP4-FWD-EST",
        "chain": "forward",
        "action": "accept",
        "connection-state": "established,related",
    },
    {
        "comment": "TP4-FWD-INVALID",
        "chain": "forward",
        "action": "drop",
        "connection-state": "invalid",
    },
    {
        "comment": "TP4-FWD-PERMITIDO",
        "chain": "forward",
        "action": "accept",
        "protocol": "icmp",
        "src-address": "10.10.0.10",
        "dst-address": "10.20.0.10",
    },
    {
        "comment": "TP4-FWD-DROP",
        "chain": "forward",
        "action": "drop",
    },
]

FALLA_ESPERADA = {
    "comment": REGLA_FALLA,
    "chain": "forward",
    "action": "drop",
    "protocol": "icmp",
    "src-address": "10.10.0.10",
    "dst-address": "10.20.0.10",
}

COMANDO_AGREGAR = (
    '/ip firewall filter add chain=forward action=drop '
    'protocol=icmp src-address=10.10.0.10 dst-address=10.20.0.10 '
    'comment="TP4-FWD-FALLA" '
    'place-before=[find where chain="forward" '
    'and comment="TP4-FWD-EST"]'
)

COMANDO_QUITAR = (
    '/ip firewall filter remove '
    '[find where chain="forward" and comment="TP4-FWD-FALLA"]'
)


def normalizar(regla: dict) -> dict:
    copia = {
        campo: valor
        for campo, valor in regla.items()
        if campo not in CAMPOS_OPERATIVOS
    }

    for campo in ("disabled", "log"):
        if campo in copia:
            copia[campo] = es_verdadero(copia[campo])
            if not copia[campo]:
                del copia[campo]

    if copia.get("log-prefix") == "":
        del copia["log-prefix"]

    for campo in ("src-address", "dst-address"):
        valor = copia.get(campo)
        if isinstance(valor, str) and valor.endswith("/32"):
            copia[campo] = valor[:-3]

    return copia


def validar(reglas: list[dict]) -> list[dict]:
    if not isinstance(reglas, list) or not reglas:
        raise ValueError("No se recibio una lista de reglas.")

    resultado = []
    for regla in reglas:
        if not isinstance(regla, dict):
            raise ValueError("Formato de regla inesperado.")

        if any(
            es_verdadero(regla.get(campo, False))
            for campo in ("dynamic", "invalid")
        ):
            raise ValueError("Hay reglas dinamicas o invalidas.")

        resultado.append(normalizar(regla))

    comentarios = [regla.get("comment") for regla in resultado]
    if any(not isinstance(nombre, str) for nombre in comentarios):
        raise ValueError("Hay reglas sin comentario valido.")

    if len(comentarios) != len(set(comentarios)):
        raise ValueError("Hay comentarios de reglas duplicados.")

    base = [
        regla for regla in resultado
        if regla["comment"] != REGLA_FALLA
    ]
    if base != BASE_ESPERADA:
        raise ValueError(
            "Las reglas base o su orden difieren del escenario aprobado. "
            "No se aplicaron cambios."
        )

    fallas = [
        regla for regla in resultado
        if regla["comment"] == REGLA_FALLA
    ]
    if fallas:
        if fallas[0] != FALLA_ESPERADA:
            raise ValueError(
                "La regla de falla tiene campos inesperados "
                "o esta deshabilitada. Se requiere revision."
            )

        if comentarios.index(REGLA_FALLA) != 2:
            raise ValueError(
                "La falla debe estar despues del aislamiento de gestion "
                "y antes de TP4-FWD-EST."
            )

    return resultado


def leer_en_sesion(cliente) -> list[dict]:
    texto = _consultar_texto(cliente, COMANDO_LECTURA)

    try:
        reglas = json.loads(texto)
    except json.JSONDecodeError:
        raise ValueError("RouterOS no devolvio un JSON valido.") from None

    return validar(reglas)


def ejecutar_accion(
    accion: str,
    credenciales: dict[str, str],
) -> dict:
    if accion not in {"actualizar", "corregir"}:
        raise ValueError("Accion fuera del alcance permitido.")

    with BLOQUEO:
        empresa = None

        if accion == "actualizar":
            empresa = validar(
                leer_forward("EMPRESA-R1", credenciales)
            )
            objetivo = empresa
        else:
            objetivo = BASE_ESPERADA

        anterior = validar(
            leer_forward("GEMELO-R1", credenciales)
        )

        if anterior == objetivo:
            return {
                "estado": "sin_cambios",
                "accion": accion,
                "equipo": "GEMELO-R1",
                "falla_presente": any(
                    r["comment"] == REGLA_FALLA for r in anterior
                ),
                "modificaciones_aplicadas": False,
            }

        with conectar_escritura("GEMELO-R1", credenciales) as cliente:
            if leer_en_sesion(cliente) != anterior:
                raise ValueError(
                    "GEMELO cambio durante la preparacion. "
                    "Repetir la comparacion."
                )

            if empresa is not None:
                vigente = validar(
                    leer_forward("EMPRESA-R1", credenciales)
                )
                if vigente != empresa:
                    raise ValueError(
                        "EMPRESA cambio durante la preparacion. "
                        "Repetir la comparacion."
                    )

            agregar = any(
                regla["comment"] == REGLA_FALLA
                for regla in objetivo
            )
            comando = COMANDO_AGREGAR if agregar else COMANDO_QUITAR

            try:
                _consultar_texto(cliente, comando)
                posterior = leer_en_sesion(cliente)
            except (ErrorSSH, ValueError):
                raise ErrorSSH(
                    "No se pudo confirmar el resultado de la escritura. "
                    "Consultar GEMELO antes de repetir la accion."
                ) from None

            if posterior != objetivo:
                raise ErrorSSH(
                    "La comprobacion posterior no coincide con el objetivo. "
                    "Revisar GEMELO antes de continuar."
                )

        return {
            "estado": "actualizado" if accion == "actualizar" else "corregido",
            "accion": accion,
            "equipo": "GEMELO-R1",
            "regla": REGLA_FALLA,
            "falla_presente": agregar,
            "reglas_base_verificadas": True,
            "modificaciones_aplicadas": True,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Actualiza o corrige la falla en GEMELO-R1."
    )
    parser.add_argument("accion", choices=("actualizar", "corregir"))
    argumentos = parser.parse_args()

    try:
        resultado = ejecutar_accion(
            argumentos.accion,
            cargar_credenciales(),
        )
        codigo = 0
    except (ErrorSSH, ValueError) as error:
        resultado = {"estado": "error", "detalle": str(error)}
        codigo = 1

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    raise SystemExit(codigo)