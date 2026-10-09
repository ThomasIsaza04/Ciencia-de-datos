import sqlite3
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/remitentes", tags=["Remitentes"])


@router.post(
    "/",
    response_model=schemas.RemitenteResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_remitente(
    remitente: schemas.RemitenteCreate,
    db: sqlite3.Connection = Depends(get_db),
):
    try:
        return crud.create_remitente(db, remitente)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="El número de documento ya está registrado.",
        )


@router.get("/", response_model=List[schemas.RemitenteResponse])
def listar_remitentes(
    skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)
):
    return crud.get_remitentes(db, skip=skip, limit=limit)


@router.get("/{remitente_id}", response_model=schemas.RemitenteResponse)
def obtener_remitente(
    remitente_id: int, db: sqlite3.Connection = Depends(get_db)
):
    res = crud.get_remitente(db, remitente_id)
    if not res:
        raise HTTPException(
            status_code=404, detail="Remitente no encontrado"
        )
    return res


@router.put("/{remitente_id}", response_model=schemas.RemitenteResponse)
def actualizar_remitente(
    remitente_id: int,
    remitente: schemas.RemitenteUpdate,
    db: sqlite3.Connection = Depends(get_db),
):
    res = crud.update_remitente(db, remitente_id, remitente)
    if not res:
        raise HTTPException(
            status_code=404, detail="Remitente no encontrado"
        )
    return res


@router.delete("/{remitente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_remitente(
    remitente_id: int, db: sqlite3.Connection = Depends(get_db)
):
    if not crud.delete_remitente(db, remitente_id):
        raise HTTPException(
            status_code=404, detail="Remitente no encontrado"
        )