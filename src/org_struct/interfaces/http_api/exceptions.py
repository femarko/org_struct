from fastapi import (
    Request,
    HTTPException
)
from org_struct.domain.errors import (
    DepartmentNotFound,
    DepartmentCycleError,
    DepartmentNameConflict,
    ORMError,
    ORMIntegrityError,
)



def register_exception_handlers(app):
    @app.exception_handler(DepartmentNotFound)
    async def department_not_found_exception_handler(request: Request, exc: DepartmentNotFound):
        raise HTTPException(status_code=404, detail=str(exc))

    @app.exception_handler(DepartmentCycleError)
    async def department_cycle_exception_handler(request: Request, exc: DepartmentCycleError):
        raise HTTPException(status_code=409, detail=str(exc))

    @app.exception_handler(DepartmentNameConflict)
    async def department_name_conflict_exception_handler(request: Request, exc: DepartmentNameConflict):
        raise HTTPException(status_code=422, detail=str(exc))
    
    @app.exception_handler(ORMError)
    async def orm_error_exception_handler(request: Request, exc: ORMError):
        raise HTTPException(status_code=500, detail=str(exc))

    @app.exception_handler(ORMIntegrityError)
    async def orm_integrity_error_exception_handler(request: Request, exc: ORMIntegrityError):
        raise HTTPException(status_code=409, detail=str(exc))
    