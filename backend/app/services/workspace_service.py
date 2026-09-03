import re
import shutil
from pathlib import Path


from app.core.config import settings


class WorkspaceService:
    """Manage Local Codex project workspaces."""

    def __init__(self):
        self.workspace_root = Path(
            settings.WORKSPACE_ROOT
        ).resolve()

        self.workspace_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def create_safe_name(name: str) -> str:
        """Convert a project name into a safe folder name."""

        safe_name = name.strip().lower()

        safe_name = re.sub(
            r"[^a-z0-9]+",
            "-",
            safe_name,
        )

        safe_name = safe_name.strip("-")

        if not safe_name:
            safe_name = "untitled-project"

        return safe_name

    def get_project_path(
        self,
        project_name: str,
        project_id: int | None = None,
    ) -> Path:
        """
        Generate a unique workspace path.

        The project ID is included when available to prevent
        duplicate project names from colliding.
        """

        safe_name = self.create_safe_name(
            project_name
        )

        if project_id is not None:
            safe_name = (
                f"{safe_name}-{project_id}"
            )

        return (
            self.workspace_root
            / safe_name
        )

    def create_workspace(
        self,
        project_name: str,
        project_id: int,
        project_type: str = "general",
    ) -> Path:
        """Create the project workspace structure."""

        project_path = self.get_project_path(
            project_name=project_name,
            project_id=project_id,
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Core directories
        (project_path / "src").mkdir(
            exist_ok=True
        )

        (project_path / "tests").mkdir(
            exist_ok=True
        )

        # README
        readme_path = project_path / "README.md"

        if not readme_path.exists():
            readme_content = (
                f"# {project_name}\n\n"
                f"Project Type: {project_type}\n\n"
                "Created and managed by Local Codex.\n"
            )

            readme_path.write_text(
                readme_content,
                encoding="utf-8",
            )

        return project_path

    def delete_workspace(
        self,
        workspace_path: str,
    ) -> bool:
        """Delete a project workspace safely."""

        path = Path(workspace_path).resolve()

        # Safety check: never delete outside workspace root.
        if (
            path != self.workspace_root
            and self.workspace_root not in path.parents
        ):
            raise ValueError(
                "Refusing to delete a path outside "
                "the workspace root."
            )

        if not path.exists():
            return False

        shutil.rmtree(path)

        return True

    def workspace_exists(
        self,
        workspace_path: str,
    ) -> bool:
        """Check whether a workspace exists."""

        return Path(
            workspace_path
        ).exists()


workspace_service = WorkspaceService()