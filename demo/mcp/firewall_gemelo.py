"""Lectura y comparacion del firewall del escenario. Sin escrituras."""

import json

from configuracion import cargar_credenciales
from conexion_ssh import ErrorSSH, _consultar_texto, conectar_lectura


REGLAS_BASE = {
    "TP4-FWD-EST",
    "TP4-FWD-INVALID",
    "TP4-FWD-PERMITIDO",
    "TP4-FWD-DROP",
}

REGLA_FALLA = "TP4-FWD-FALLA"

REGLAS_GESTION = {
    "TP4-NO-MGMT-IN",
    "TP4-NO-MGMT-OUT",
}

REGLAS_ADMITIDAS = REGLAS_BASE | REGLAS_GESTION | {REGLA_FALLA}

CAMPOS_OPERATIVOS = {
    ".id", "bytes", "packets", "dynamic", "invalid",
}

COMANDO_LECTURA = (
    ":put [:serialize to=json "
    '[/ip firewall filter print as-value where chain="forward"]]'
)

def es_verdadero(valor) -> bool:
    return valor is True or str(valor).lower() in {"true", "yes"}


def leer_forward(
    nombre: str,
    credenciales: dict[str, str],
) -> list[dict]:
    if nombre not in {"EMPRESA-R1", "GEMELO-R1"}:
        raise ValueError("El escenario de firewall utiliza unicamente R1.")

    with conectar_lectura(nombre, credenciales) as cliente:
        texto = _consultar_texto(cliente, COMANDO_LECTURA)

    try:
        reglas = json.loads(texto)
    except json.JSONDecodeError:
        raise ValueError("RouterOS no devolvio un JSON valido.") from None

    if not isinstance(reglas, list) or not reglas:
        raise ValueError("No se encontro una lista de reglas forward.")

    normalizadas = []
    comentarios = set()

    for regla in reglas:
        if not isinstance(regla, dict):
            raise ValueError("Formato de regla inesperado.")

        comentario = regla.get("comment")
        if comentario not in REGLAS_ADMITIDAS:
            raise ValueError(
                "Hay reglas forward fuera del alcance previsto. "
                "Se requiere revision antes de actualizar."
            )

        if comentario in comentarios:
            raise ValueError("Hay comentarios de reglas duplicados.")

        if regla.get("chain") != "forward":
            raise ValueError("Se recibio una regla fuera de forward.")

        if es_verdadero(regla.get("dynamic", False)):
            raise ValueError("No se admiten reglas dinamicas en el escenario.")

        if es_verdadero(regla.get("invalid", False)):
            raise ValueError("Hay una regla invalida en el escenario.")

        comentarios.add(comentario)
        normalizadas.append({
            campo: valor
            for campo, valor in regla.items()
            if campo not in CAMPOS_OPERATIVOS
        })

    if not (REGLAS_BASE | REGLAS_GESTION).issubset(comentarios):
        raise ValueError("Faltan reglas base o de aislamiento de gestion.")

    return normalizadas


def comparar_firewall(credenciales: dict[str, str]) -> dict:
    empresa = leer_forward("EMPRESA-R1", credenciales)
    gemelo = leer_forward("GEMELO-R1", credenciales)

    por_nombre_empresa = {r["comment"]: r for r in empresa}
    por_nombre_gemelo = {r["comment"]: r for r in gemelo}

    diferencias = []
    for nombre in sorted(por_nombre_empresa.keys() | por_nombre_gemelo.keys()):
        original = por_nombre_empresa.get(nombre)
        copia = por_nombre_gemelo.get(nombre)

        if original != copia:
            diferencias.append({
                "regla": nombre,
                "empresa": original,
                "gemelo": copia,
            })

    orden_empresa = [r["comment"] for r in empresa]
    orden_gemelo = [r["comment"] for r in gemelo]

    coincide = not diferencias and orden_empresa == orden_gemelo

    return {
        "estado": "equivalente_en_alcance" if coincide else "diferencias",
        "alcance": "Reglas IPv4 forward de R1 admitidas para el escenario.",
        "orden_empresa": orden_empresa,
        "orden_gemelo": orden_gemelo,
        "orden_coincide": orden_empresa == orden_gemelo,
        "diferencias": diferencias,
        "modificaciones_aplicadas": False,
    }


if __name__ == "__main__":
    try:
        resultado = comparar_firewall(cargar_credenciales())
        codigo = 0
    except (ErrorSSH, ValueError) as error:
        resultado = {"estado": "error", "detalle": str(error)}
        codigo = 1

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    raise SystemExit(codigo)