from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# Inicializacion de la aplicacion FastAPI
app = FastAPI(
    title="API Lavanderia y Servicio - ADSO",
    description="API RESTful completa con operaciones CRUD para auditoria de servicios web",
    version="2.0.0"
)

# Modelo de Datos con pydantic para validacion automatica
class PrendaServicio(BaseModel):
    id: int
    cliente_propietario: str
    tipo_prenda: str
    costo_lavado: float
    listo_para_entrega: bool = True

# Modelo auxiliar para la actualizacion parcial o total
class ServicioUpdate(BaseModel):
    cliente_propietario: str
    tipo_prenda: str
    costo_lavado: float
    listo_para_entrega: bool

#Base de datos simulada  en memoria
db_lavanderia: List[PrendaServicio] = [
PrendaServicio(id=1, cliente_propietario="Dipper Tayron Pines", tipo_prenda="Camisa Manga larga azul", costo_lavado= 12800.00, listo_para_entrega=True),
PrendaServicio(id=2, cliente_propietario="Mabbel Samantha Pines", tipo_prenda="Blusa Manga corta roja", costo_lavado=16000.20, listo_para_entrega=False)
]

#--------------------------------------------------------------------
# ENDPOINTS / RUTAS DE LA API (CRUD COMPLETO)
#--------------------------------------------------------------------

# 1. READ ALL (obtener todos los servicios)
@app.get("/api/v1/servicios", response_model=List[PrendaServicio], status_code=status.HTTP_200_OK)
def obtener_todos_los_servicios():
    return db_lavanderia

#2. READ ONE (obtener una prenda especifica por ID)
@app.get("/api/v1/servicios/{servicio_id}", response_model=PrendaServicio, status_code=status.HTTP_200_OK)
def obtener_servicio_por_id(servicio_id: int):
    for servicio in db_lavanderia:
        if servicio.id == servicio_id:
            return servicio
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El servicio con ID {servicio_id} no existe en el sistema de la Lavanderia."
    )


#3. CREATE (Registrar una nueva Prenda)
@app.post("/api/v1/servicios", response_model=PrendaServicio, status_code=status.HTTP_201_CREATED)
def crear_nuevo_Servicio(servicio: PrendaServicio):
    # Validar si el ID ya existe
    for l in db_lavanderia:
     if l.id == servicio.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de registro: Ya existe un Servicio con el ID {servicio.id}."
        )
    db_lavanderia.append(servicio)
    return servicio

# 4. UPDATE (Actualizar un Servicio existente - Metodo PUT)
@app.put("/api/v1/servicios/{servicio_id}", response_model=PrendaServicio, status_code=status.HTTP_200_OK)
def actualizar_Servicio(servicio_id: int, datos_actualizados: ServicioUpdate):
    for index, servicio in enumerate(db_lavanderia):
        if servicio.id == servicio_id:
            Servicio_modificado = PrendaServicio(
                id=servicio_id,
                cliente_propietario=datos_actualizados.cliente_propietario,
                tipo_prenda=datos_actualizados.tipo_prenda,
                costo_lavado=datos_actualizados.costo_lavado,
                listo_para_entrega=datos_actualizados.listo_para_entrega
            )
            db_lavanderia[index] = Servicio_modificado
            return Servicio_modificado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El Servicio con ID {servicio_id} no fue encontrado."
    )

# 5. DELETE (Eliminar un libro de la biblioteca)
@app.delete("/api/v1/servicios/{servicio_id}", status_code=status.HTTP_200_OK)
def eliminar_Servicio(servicio_id: int):
    for index, servicio in enumerate(db_lavanderia):
        if servicio.id == servicio_id:
            db_lavanderia.pop(index)
            return {"mensaje": f"El Servicio con ID {servicio_id} fue eliminado exitosamente."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El Servicio con ID {servicio_id} no existe."
    ) 


    