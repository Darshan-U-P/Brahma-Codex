from pathlib import Path
from typing import Any


class FileService:
    """Service for safely managing project workspace files."""

    def _get_safe_path(
        self,
        workspace_path: str,
        relative_path: str,
    ) -> Path:
        """
        Resolve a file path and ensure it remains inside
        the project workspace.
        """

        workspace = Path(workspace_path).resolve()

        if not workspace.exists():
            raise FileNotFoundError(
                f"Workspace does not exist: {workspace}"
            )

        if not workspace.is_dir():
            raise NotADirectoryError(
                f"Workspace is not a directory: {workspace}"
            )

        if not relative_path or not relative_path.strip():
            raise ValueError(
                "File path cannot be empty."
            )

        requested_path = (
            workspace / relative_path
        ).resolve()

        try:
            requested_path.relative_to(workspace)

        except ValueError as error:
            raise PermissionError(
                "Access outside the project workspace "
                "is not allowed."
            ) from error

        return requested_path

    def list_files(
        self,
        workspace_path: str,
    ) -> list[dict[str, Any]]:
        """
        List all files and directories inside a workspace.
        """

        workspace = Path(workspace_path).resolve()

        if not workspace.exists():
            raise FileNotFoundError(
                f"Workspace does not exist: {workspace}"
            )

        if not workspace.is_dir():
            raise NotADirectoryError(
                f"Workspace is not a directory: {workspace}"
            )

        items = []

        for path in sorted(
            workspace.rglob("*")
        ):
            relative_path = path.relative_to(
                workspace
            )

            items.append(
                {
                    "path": relative_path.as_posix(),
                    "name": path.name,
                    "type": (
                        "directory"
                        if path.is_dir()
                        else "file"
                    ),
                    "size": (
                        path.stat().st_size
                        if path.is_file()
                        else None
                    ),
                }
            )

        return items

    def read_file(
        self,
        workspace_path: str,
        relative_path: str,
    ) -> str:
        """Read a text file from the workspace."""

        file_path = self._get_safe_path(
            workspace_path,
            relative_path,
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {relative_path}"
            )

        if not file_path.is_file():
            raise IsADirectoryError(
                f"Path is not a file: {relative_path}"
            )

        return file_path.read_text(
            encoding="utf-8",
        )

    def create_file(
        self,
        workspace_path: str,
        relative_path: str,
        content: str = "",
        overwrite: bool = False,
    ) -> Path:
        """
        Create a new file inside the workspace.
        """

        file_path = self._get_safe_path(
            workspace_path,
            relative_path,
        )

        if file_path.exists() and not overwrite:
            raise FileExistsError(
                f"File already exists: {relative_path}"
            )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return file_path

    def update_file(
        self,
        workspace_path: str,
        relative_path: str,
        content: str,
    ) -> Path:
        """Update an existing file."""

        file_path = self._get_safe_path(
            workspace_path,
            relative_path,
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {relative_path}"
            )

        if not file_path.is_file():
            raise IsADirectoryError(
                f"Path is not a file: {relative_path}"
            )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return file_path

    def delete_file(
        self,
        workspace_path: str,
        relative_path: str,
    ) -> None:
        """Delete a file inside the workspace."""

        file_path = self._get_safe_path(
            workspace_path,
            relative_path,
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {relative_path}"
            )

        if not file_path.is_file():
            raise IsADirectoryError(
                f"Path is not a file: {relative_path}"
            )

        file_path.unlink()


file_service = FileService()