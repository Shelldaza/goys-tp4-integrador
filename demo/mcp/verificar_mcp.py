"""Verificacion local del protocolo MCP y sus consultas de lectura."""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE = Path(__file__).resolve().parent


def obtener_datos(resultado) -> dict:
    if resultado.isError:
        raise RuntimeError("La herramienta devolvio un error.")

    for bloque in resultado.content:
        if bloque.type == "text":
            datos = json.loads(bloque.text)
            if isinstance(datos, dict):
                return datos

    raise RuntimeError("La herramienta no devolvio el objeto esperado.")


async def verificar() -> None:
    parametros = StdioServerParameters(
        command=sys.executable,
        args=[str(BASE / "servidor_mcp.py")],
    )

    async with stdio_client(parametros) as (lectura, escritura):
        async with ClientSession(lectura, escritura) as sesion:
            await sesion.initialize()
            print("OK: sesion MCP inicializada.", flush=True)

            listado = await sesion.list_tools()
            nombres = {herramienta.name for herramienta in listado.tools}

            if nombres != {"listar_routers", "consultar_router"}:
                raise RuntimeError("El conjunto de herramientas no coincide.")

            print("OK: solo se publican las dos herramientas de lectura.",
                  flush=True)

            inventario = await sesion.call_tool("listar_routers", {})
            if inventario.isError:
                raise RuntimeError("Fallo la consulta del inventario.")

            print("OK: listar_routers responde mediante MCP.", flush=True)

            for equipo in ("EMPRESA-R1", "GEMELO-R1"):
                resultado = await sesion.call_tool(
                    "consultar_router",
                    {"equipo": equipo, "consulta": "identidad"},
                )
                datos = obtener_datos(resultado)

                if (
                    datos.get("estado") != "leido"
                    or datos.get("equipo") != equipo
                    or datos.get("salida", "").strip() != f"name: {equipo}"
                ):
                    raise RuntimeError(
                        f"Respuesta de identidad inesperada para {equipo}."
                    )

                print(f"OK: identidad de {equipo} consultada mediante MCP.",
                      flush=True)

            rechazado = await sesion.call_tool(
                "consultar_router",
                {"equipo": "FUERA-DEL-INVENTARIO", "consulta": "identidad"},
            )
            if not rechazado.isError:
                raise RuntimeError("Se acepto un equipo no permitido.")

            print("OK: equipo fuera del inventario rechazado.", flush=True)

            rechazado = await sesion.call_tool(
                "consultar_router",
                {"equipo": "GEMELO-R1", "consulta": "comando_libre"},
            )
            if not rechazado.isError:
                raise RuntimeError("Se acepto una consulta no permitida.")

            print("OK: consulta fuera de la lista rechazada.", flush=True)

    print("Verificacion MCP completada. No se modificaron routers.")


if __name__ == "__main__":
    try:
        asyncio.run(asyncio.wait_for(verificar(), timeout=120))
    except Exception as error:
        print(
            f"Verificacion incompleta: {type(error).__name__}.",
            file=sys.stderr,
        )
        raise SystemExit(1) from None