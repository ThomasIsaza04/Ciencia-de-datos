from enum import Enum
import sqlite3
from typing import List, Optional
from . import schemas


# --- CRUD REMITENTE ---
def create_remitente(
    conn: sqlite3.Connection, remitente: schemas.RemitenteCreate
) -> schemas.RemitenteResponse:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO remitentes (numero_documento, nombre_completo, email, telefono, direccion)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            remitente.numero_documento,
            remitente.nombre_completo,
            remitente.email,
            remitente.telefono,
            remitente.direccion,
        ),
    )
    conn.commit()
    remitente_id = cursor.lastrowid
    return get_remitente(conn, remitente_id)


def get_remitente(
    conn: sqlite3.Connection, remitente_id: int
) -> Optional[schemas.RemitenteResponse]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM remitentes WHERE id = ?", (remitente_id,)
    )
    row = cursor.fetchone()
    if row:
        return schemas.RemitenteResponse(**dict(row))
    return None


def get_remitentes(
    conn: sqlite3.Connection, skip: int = 0, limit: int = 100
) -> List[schemas.RemitenteResponse]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM remitentes LIMIT ? OFFSET ?", (limit, skip)
    )
    rows = cursor.fetchall()
    return [schemas.RemitenteResponse(**dict(row)) for row in rows]


def update_remitente(
    conn: sqlite3.Connection,
    remitente_id: int,
    remitente_data: schemas.RemitenteUpdate,
) -> Optional[schemas.RemitenteResponse]:
    db_remitente = get_remitente(conn, remitente_id)
    if not db_remitente:
        return None

    update_dict = remitente_data.model_dump(exclude_unset=True)
    if not update_dict:
        return db_remitente

    fields = ", ".join([f"{key} = ?" for key in update_dict.keys()])
    values = list(update_dict.values()) + [remitente_id]

    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE remitentes SET {fields} WHERE id = ?", values
    )
    conn.commit()

    return get_remitente(conn, remitente_id)


def delete_remitente(conn: sqlite3.Connection, remitente_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM remitentes WHERE id = ?", (remitente_id,))
    conn.commit()
    return cursor.rowcount > 0


# --- CRUD RADICADO ---
def create_radicado(
    conn: sqlite3.Connection, radicado: schemas.RadicadoCreate
) -> schemas.RadicadoResponse:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO radicados (numero_radicado, asunto, tipo_radicado, estado, remitente_id)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            radicado.numero_radicado,
            radicado.asunto,
            radicado.tipo_radicado.value,
            radicado.estado.value,
            radicado.remitente_id,
        ),
    )
    conn.commit()
    radicado_id = cursor.lastrowid
    return get_radicado(conn, radicado_id)


def get_radicado(
    conn: sqlite3.Connection, radicado_id: int
) -> Optional[schemas.RadicadoResponse]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM radicados WHERE id = ?", (radicado_id,))
    row = cursor.fetchone()

    if row:
        radic_dict = dict(row)
        remitente = get_remitente(conn, radic_dict["remitente_id"])
        return schemas.RadicadoResponse(**radic_dict, remitente=remitente)
    return None


def get_radicados(
    conn: sqlite3.Connection, skip: int = 0, limit: int = 100
) -> List[schemas.RadicadoResponse]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM radicados LIMIT ? OFFSET ?", (limit, skip)
    )
    rows = cursor.fetchall()

    resultado = []
    for row in rows:
        radic_dict = dict(row)
        remitente = get_remitente(conn, radic_dict["remitente_id"])
        resultado.append(
            schemas.RadicadoResponse(**radic_dict, remitente=remitente)
        )

    return resultado


def update_radicado(
    conn: sqlite3.Connection,
    radicado_id: int,
    radicado_data: schemas.RadicadoUpdate,
) -> Optional[schemas.RadicadoResponse]:
    db_radicado = get_radicado(conn, radicado_id)
    if not db_radicado:
        return None

    update_dict = radicado_data.model_dump(exclude_unset=True)
    if not update_dict:
        return db_radicado

    for key, val in update_dict.items():
        if isinstance(val, Enum):
            update_dict[key] = val.value

    fields = ", ".join([f"{key} = ?" for key in update_dict.keys()])
    values = list(update_dict.values()) + [radicado_id]

    cursor = conn.cursor()
    cursor.execute(f"UPDATE radicados SET {fields} WHERE id = ?", values)
    conn.commit()

    return get_radicado(conn, radicado_id)


def delete_radicado(conn: sqlite3.Connection, radicado_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM radicados WHERE id = ?", (radicado_id,))
    conn.commit()
    return cursor.rowcount > 0