import logging

from fastapi import APIRouter, HTTPException, status

from app.agents.coding_agent import CodingAgent
from app.database.session import SessionLocal
from app.models.project import Project
from app.schemas.agent import (
    AgentRequest,
    AgentResponse,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/projects",
    tags=["Coding Agent"],
)


@router.post(
    "/{project_id}/agent",
    response_model=AgentResponse,
)
async def run_coding_agent(
    project_id: int,
    request: AgentRequest,
):
    """
    Run the Coding Agent for a specific project.
    """

    db = SessionLocal()

    try:
        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Project with ID "
                    f"{project_id} not found."
                ),
            )

        agent = CodingAgent()

        if not agent.is_model_loaded():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Local LLM is not loaded. "
                    "Load the model using "
                    "POST /llm/load first."
                ),
            )

        response = agent.generate_response(
            project=project,
            task=request.task,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return AgentResponse(
            success=True,
            project_id=project.id,
            task=request.task,
            response=response,
        )

    except HTTPException:
        raise

    except Exception as error:
        logger.exception(
            "Coding Agent failed for project %s.",
            project_id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Coding Agent failed: "
                f"{str(error)}"
            ),
        )

    finally:
        db.close()