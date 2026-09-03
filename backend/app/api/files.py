from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.project import Project
from app.schemas.file import (
    FileContentResponse,
    FileCreate,
    FileOperationResponse,
    FileResponse,
    FileUpdate,
)
from app.services.file_service import file_service


router = APIRouter(
    prefix="/projects/{project_id}/files",
    tags=["Files"],
)


def get_project_or_404(
    project_id: int,
    db: Session,
) -> Project:
    """Get a project or raise a 404 error."""

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found.",
        )

    if not project.workspace_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Project with ID {project_id} "
                "does not have a workspace."
            ),
        )

    return project


@router.get(
    "",
    response_model=list[FileResponse],
)
def list_project_files(
    project_id: int,
    db: Session = Depends(get_db),
):
    """List all files and directories in a project."""

    project = get_project_or_404(
        project_id,
        db,
    )

    try:
        return file_service.list_files(
            project.workspace_path
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=f"Failed to list files: {str(error)}",
        ) from error


@router.get(
    "/content",
    response_model=FileContentResponse,
)
def read_project_file(
    project_id: int,
    path: str,
    db: Session = Depends(get_db),
):
    """
    Read a file.

    Example:
    GET /projects/1/files/content?path=src/main.py
    """

    project = get_project_or_404(
        project_id,
        db,
    )

    try:
        content = file_service.read_file(
            project.workspace_path,
            path,
        )

        return {
            "path": path,
            "content": content,
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except IsADirectoryError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error


@router.post(
    "",
    response_model=FileOperationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_file(
    project_id: int,
    file_data: FileCreate,
    db: Session = Depends(get_db),
):
    """Create a new file inside a project workspace."""

    project = get_project_or_404(
        project_id,
        db,
    )

    try:
        file_service.create_file(
            workspace_path=project.workspace_path,
            relative_path=file_data.path,
            content=file_data.content,
            overwrite=file_data.overwrite,
        )

        return {
            "success": True,
            "message": "File created successfully.",
            "path": file_data.path,
        }

    except FileExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=f"Failed to create file: {str(error)}",
        ) from error


@router.put(
    "/content",
    response_model=FileOperationResponse,
)
def update_project_file(
    project_id: int,
    path: str,
    file_data: FileUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing file.

    Example:
    PUT /projects/1/files/content?path=src/main.py
    """

    project = get_project_or_404(
        project_id,
        db,
    )

    try:
        file_service.update_file(
            workspace_path=project.workspace_path,
            relative_path=path,
            content=file_data.content,
        )

        return {
            "success": True,
            "message": "File updated successfully.",
            "path": path,
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except IsADirectoryError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail=str(error),
        ) from error


@router.delete(
    "",
    response_model=FileOperationResponse,
)
def delete_project_file(
    project_id: int,
    path: str,
    db: Session = Depends(get_db),
):
    """
    Delete a file.

    Example:
    DELETE /projects/1/files?path=src/main.py
    """

    project = get_project_or_404(
        project_id,
        db,
    )

    try:
        file_service.delete_file(
            workspace_path=project.workspace_path,
            relative_path=path,
        )

        return {
            "success": True,
            "message": "File deleted successfully.",
            "path": path,
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except IsADirectoryError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail=str(error),
        ) from error