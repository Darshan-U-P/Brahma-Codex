import logging

from app.agents.project_context import (
    ProjectContextBuilder,
)
from app.llm.client import get_llama_client


logger = logging.getLogger(__name__)


class CodingAgent:
    """
    Coding Agent responsible for understanding
    projects and communicating with the local LLM.
    """

    def __init__(self):
        self.llm_client = get_llama_client()

        self.context_builder = (
            ProjectContextBuilder()
        )


    def is_model_loaded(self) -> bool:
        """
        Check whether the local LLM is loaded.
        """

        return self.llm_client.is_loaded()


    def generate_response(
        self,
        project,
        task: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> str:
        """
        Generate a coding response using the
        project context and local LLM.
        """

        if not self.is_model_loaded():
            raise RuntimeError(
                "Local LLM is not loaded. "
                "Load the model before running "
                "the Coding Agent."
            )

        context = (
            self.context_builder.build_context(
                project=project,
            )
        )

        system_prompt = (
            "You are Local Codex, an expert software "
            "engineering AI assistant.\n\n"
            "You analyze existing software projects and "
            "provide practical, technically accurate "
            "guidance.\n\n"
            "Rules:\n"
            "1. Carefully analyze the provided project "
            "context.\n"
            "2. Do not assume files exist if they are not "
            "listed.\n"
            "3. Respect the existing architecture where "
            "possible.\n"
            "4. Write practical and working code when "
            "code is requested.\n"
            "5. Explain important implementation "
            "decisions briefly.\n"
            "6. Do not claim that you modified files "
            "unless you actually have a tool that writes "
            "them.\n"
            "7. Always provide a useful, non-empty answer "
            "when sufficient context is available."
        )

        user_prompt = f"""
PROJECT CONTEXT
====================================================

{context}

====================================================
USER TASK
====================================================

{task}

====================================================

Analyze the project and answer the user's request.
"""

        logger.info(
            "Coding Agent processing task for "
            "project ID %s: %s",
            project.id,
            task[:100],
        )

        response = self.llm_client.chat(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        logger.debug(
            "Raw Coding Agent response: %s",
            response,
        )

        choices = response.get(
            "choices",
            [],
        )

        if not choices:
            raise RuntimeError(
                "Local LLM returned no response choices."
            )

        message = choices[0].get(
            "message",
            {},
        )

        content = message.get(
            "content",
            "",
        )

        if content is None:
            content = ""

        result = content.strip()

        if not result:
            raise RuntimeError(
                "Local LLM generated an empty response."
            )

        logger.info(
            "Coding Agent generated response "
            "with %s characters.",
            len(result),
        )

        return result