import logging
from pathlib import Path


logger = logging.getLogger(__name__)


class ProjectContextBuilder:
    """
    Builds project context for the Coding Agent.

    The context includes project metadata and the
    current workspace file structure.
    """

    def build_context(
        self,
        project,
        max_file_content_length: int = 4000,
    ) -> str:
        """
        Build a text representation of the project
        that can be provided to the local LLM.
        """

        workspace_path = project.workspace_path

        context_parts = [
            "PROJECT INFORMATION",
            f"Name: {project.name}",
            f"Description: {project.description or 'No description provided.'}",
            f"Project Type: {project.project_type}",
            f"Status: {project.status}",
            f"Workspace Path: {workspace_path or 'Not available'}",
            "",
        ]

        if not workspace_path:
            context_parts.append(
                "WORKSPACE STATUS: No workspace is configured."
            )

            return "\n".join(context_parts)

        workspace = Path(workspace_path)

        if not workspace.exists():
            context_parts.append(
                "WORKSPACE STATUS: Workspace directory does not exist."
            )

            return "\n".join(context_parts)

        context_parts.append(
            "PROJECT FILE STRUCTURE"
        )

        file_paths = self._get_file_paths(
            workspace
        )

        if not file_paths:
            context_parts.append(
                "The workspace is currently empty."
            )
        else:
            for file_path in file_paths:
                context_parts.append(
                    f"- {file_path}"
                )

        context_parts.append("")
        context_parts.append(
            "IMPORTANT FILE CONTENTS"
        )

        file_contents = self._get_file_contents(
            workspace=workspace,
            max_file_content_length=max_file_content_length,
        )

        if not file_contents:
            context_parts.append(
                "No readable files found."
            )
        else:
            context_parts.extend(
                file_contents
            )

        return "\n".join(context_parts)

    def _get_file_paths(
        self,
        workspace: Path,
    ) -> list[str]:
        """
        Get all file and directory paths inside
        the workspace.
        """

        paths = []

        try:
            for path in sorted(
                workspace.rglob("*")
            ):
                relative_path = path.relative_to(
                    workspace
                )

                if path.is_dir():
                    paths.append(
                        f"{relative_path}/"
                    )
                else:
                    paths.append(
                        str(relative_path)
                    )

        except OSError as error:
            logger.error(
                "Failed to read workspace structure: %s",
                error,
            )

        return paths

    def _get_file_contents(
        self,
        workspace: Path,
        max_file_content_length: int,
    ) -> list[str]:
        """
        Read text file contents from the workspace.

        Large files are truncated to avoid sending
        excessive context to the LLM.
        """

        contents = []

        ignored_directories = {
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "node_modules",
            "dist",
            "build",
        }

        try:
            for path in sorted(
                workspace.rglob("*")
            ):
                if not path.is_file():
                    continue

                relative_path = path.relative_to(
                    workspace
                )

                if any(
                    part in ignored_directories
                    for part in relative_path.parts
                ):
                    continue

                content = self._read_text_file(
                    path=path,
                    max_length=max_file_content_length,
                )

                if content is None:
                    continue

                contents.append(
                    self._format_file_content(
                        relative_path=str(
                            relative_path
                        ),
                        content=content,
                    )
                )

        except OSError as error:
            logger.error(
                "Failed to read project files: %s",
                error,
            )

        return contents

    @staticmethod
    def _read_text_file(
        path: Path,
        max_length: int,
    ) -> str | None:
        """
        Read a text file safely.

        Returns None when the file cannot be read
        as text.
        """

        try:
            content = path.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:
            return None

        except OSError:
            return None

        if len(content) > max_length:
            content = (
                content[:max_length]
                + "\n\n"
                + "[FILE CONTENT TRUNCATED]"
            )

        return content

    @staticmethod
    def _format_file_content(
        relative_path: str,
        content: str,
    ) -> str:
        """
        Format file contents for LLM context.
        """

        return (
            f"\n--- FILE: {relative_path} ---\n"
            f"{content}\n"
            f"--- END FILE: {relative_path} ---\n"
        )