import sqlite3
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/radicados", tags=["Radicados"])


@router.post(
    "/",
    response_model=schemas.RadicadoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_radicado(
    radicado: schemas.RadicadoCreate, db: sqlite3.Connection = Depends(get_db)
):
    remitente = crud.get_remitente(db, radicado.remitente_id)
    if not remitente:
        raise HTTPException(
            status_code=400, detail="El remitente especificado no existe."
        )
    try:
        return crud.create_radicado(db, radicado)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="El número de radicado ya se encuentra registrado.",
        )


@router.get("/", response_model=List[schemas.RadicadoResponse])
def listar_radicados(
    skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)
):
    return crud.get_radicados(db, skip=skip, limit=limit)


@router.get("/{radicado_id}", response_model=schemas.RadicadoResponse)
def obtener_radicado(
    radicado_id: int, db: sqlite3.Connection = Depends(get_db)
):
    res = crud.get_radicado(db, radicado_id)
    if not res:
        raise HTTPException(status_code=404, detail="Radicado no encontrado")
    return res


@router.put("/{radicado_id}", response_model=schemas.RadicadoResponse)
def actualizar_radicado(
    radicado_id: int,
    radicado: schemas.RadicadoUpdate,
    db: sqlite3.Connection = Depends(get_db),
):
    res = crud.update_radicado(db, radicado_id, radicado)
    if not res:
        raise HTTPException(status_code=404, detail="Radicado no encontrado")
    return res


@router.delete("/{radicado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_radicado(
    radicado_id: int, db: sqlite3.Connection = Depends(get_db)
):
    if not crud.delete_radicado(db, radicado_id):
        raise HTTPException(status_code=404, detail="Radicado no encontrado")