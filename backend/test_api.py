import sys
import json
from pathlib import Path

import requests


BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# Helper Functions
# ============================================================

def print_result(name, success, response=None, extra=None):
    status = "PASS" if success else "FAIL"

    print("\n" + "=" * 60)
    print(f"[{status}] {name}")

    if response is not None:
        print(f"Status Code: {response.status_code}")

        try:
            print("Response:")
            print(response.json())
        except ValueError:
            print("Response:")
            print(response.text)

    if extra is not None:
        print("Details:")
        print(extra)


# ============================================================
# Phase 1 - Health Tests
# ============================================================

def test_health():
    name = "GET /health"

    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=10,
        )

        success = response.status_code == 200

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Phase 1 - LLM Tests
# ============================================================

def test_llm_info():
    name = "GET /llm/info"

    try:
        response = requests.get(
            f"{BASE_URL}/llm/info",
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and "loaded" in data
            and "model_path" in data
            and "model_exists" in data
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_llm_status(expected_loaded=None):
    name = "GET /llm/status"

    try:
        response = requests.get(
            f"{BASE_URL}/llm/status",
            timeout=10,
        )

        success = response.status_code == 200

        if success and expected_loaded is not None:
            data = response.json()

            success = (
                data.get("loaded")
                == expected_loaded
            )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_load_model():
    name = "POST /llm/load"

    try:
        print("\nLoading model. This may take some time...")

        response = requests.post(
            f"{BASE_URL}/llm/load",
            timeout=300,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and data.get("loaded") is True
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_unload_model():
    name = "POST /llm/unload"

    try:
        response = requests.post(
            f"{BASE_URL}/llm/unload",
            timeout=60,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and data.get("loaded") is False
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Phase 1 - Chat Tests
# ============================================================

def test_chat():
    name = "POST /chat"

    payload = {
        "message": (
            "Reply with exactly: "
            "Local Codex is working"
        ),
        "temperature": 0.1,
        "max_tokens": 50,
    }

    try:
        print("\nGenerating AI response...")

        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=300,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and "response" in data
            and isinstance(
                data["response"],
                str,
            )
            and len(
                data["response"]
            ) > 0
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_chat_stream():
    name = "POST /chat/stream"

    payload = {
        "message": (
            "Say hello in one short sentence."
        ),
        "temperature": 0.1,
        "max_tokens": 50,
    }

    try:
        print("\nStreaming AI response...")

        response = requests.post(
            f"{BASE_URL}/chat/stream",
            json=payload,
            stream=True,
            timeout=300,
        )

        if response.status_code != 200:
            print_result(
                name,
                False,
                response,
            )
            return False

        received_tokens = []
        received_done = False

        for line in response.iter_lines(
            decode_unicode=True
        ):
            if not line:
                continue

            if line.startswith("data: "):
                data = line[6:]

                if data == "[DONE]":
                    received_done = True
                    break

                try:
                    token_data = json.loads(data)

                    if "token" in token_data:
                        token = (
                            token_data["token"]
                        )

                        received_tokens.append(
                            token
                        )

                        print(
                            token,
                            end="",
                            flush=True,
                        )

                except json.JSONDecodeError:
                    pass

        print()

        success = (
            len(received_tokens) > 0
            and received_done
        )

        print("\n" + "=" * 60)

        print(
            f"[{'PASS' if success else 'FAIL'}] "
            f"{name}"
        )

        print(
            f"Received tokens: "
            f"{len(received_tokens)}"
        )

        print(
            f"Received DONE: "
            f"{received_done}"
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_chat_validation():
    name = "POST /chat - Validation Test"

    payload = {
        "message": "",
        "temperature": 5,
        "max_tokens": -10,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=10,
        )

        success = (
            response.status_code == 422
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Phase 2 - Project Tests
# ============================================================

def test_create_project():
    name = "POST /projects"

    payload = {
        "name": "Automated Test Project",
        "description": (
            "Project created automatically "
            "by the Local Codex API test."
        ),
        "project_type": "python",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/projects",
            json=payload,
            timeout=20,
        )

        data = response.json()

        success = (
            response.status_code == 201
            and "id" in data
            and data.get("name")
            == payload["name"]
            and data.get("workspace_path")
            is not None
        )

        print_result(name, success, response)

        if success:
            return (
                True,
                data["id"],
                data["workspace_path"],
            )

        return False, None, None

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False, None, None


def test_workspace_exists(workspace_path):
    name = "Project Workspace Created"

    try:
        path = Path(workspace_path)

        exists = path.exists()

        is_directory = path.is_dir()

        src_exists = (
            path / "src"
        ).exists()

        tests_exists = (
            path / "tests"
        ).exists()

        readme_exists = (
            path / "README.md"
        ).exists()

        success = (
            exists
            and is_directory
            and src_exists
            and tests_exists
            and readme_exists
        )

        details = {
            "workspace_path": str(path),
            "workspace_exists": exists,
            "is_directory": is_directory,
            "src_exists": src_exists,
            "tests_exists": tests_exists,
            "readme_exists": readme_exists,
        }

        print_result(
            name,
            success,
            extra=details,
        )

        return success

    except Exception as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_readme_content(workspace_path):
    name = "Project README Created"

    try:
        readme_path = (
            Path(workspace_path)
            / "README.md"
        )

        if not readme_path.exists():

            print_result(
                name,
                False,
                extra={
                    "reason": (
                        "README.md does not exist."
                    )
                },
            )

            return False

        content = readme_path.read_text(
            encoding="utf-8",
        )

        success = (
            len(content.strip()) > 0
            and "Automated Test Project"
            in content
        )

        print_result(
            name,
            success,
            extra={
                "readme_path": str(readme_path),
                "content": content,
            },
        )

        return success

    except Exception as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_list_projects():
    name = "GET /projects"

    try:
        response = requests.get(
            f"{BASE_URL}/projects",
            timeout=10,
        )

        success = (
            response.status_code == 200
            and isinstance(
                response.json(),
                list,
            )
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_get_project(project_id):
    name = (
        f"GET /projects/{project_id}"
    )

    try:
        response = requests.get(
            f"{BASE_URL}/projects/{project_id}",
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("id")
            == project_id
            and data.get("workspace_path")
            is not None
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_update_project(project_id):
    name = (
        f"PUT /projects/{project_id}"
    )

    payload = {
        "name": (
            "Updated Automated Test Project"
        ),
        "description": (
            "This project was updated "
            "by the automated API test."
        ),
        "project_type": "python",
        "status": "active",
    }

    try:
        response = requests.put(
            f"{BASE_URL}/projects/{project_id}",
            json=payload,
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("id")
            == project_id
            and data.get("name")
            == payload["name"]
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_workspace_still_exists(workspace_path):
    name = (
        "Workspace Exists After Project Update"
    )

    try:
        path = Path(workspace_path)

        success = (
            path.exists()
            and path.is_dir()
        )

        print_result(
            name,
            success,
            extra={
                "workspace_path": str(path),
                "exists": path.exists(),
            },
        )

        return success

    except Exception as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_project_not_found():
    name = (
        "GET /projects/999999 "
        "- Not Found Test"
    )

    try:
        response = requests.get(
            f"{BASE_URL}/projects/999999",
            timeout=10,
        )

        success = (
            response.status_code == 404
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Phase 2 - File Management Tests
# ============================================================

def test_create_file(project_id):
    name = (
        f"POST /projects/{project_id}/files"
    )

    payload = {
        "path": "src/main.py",
        "content": (
            "def add(a, b):\n"
            "    return a + b\n\n\n"
            "def main():\n"
            "    result = add(2, 3)\n"
            "    print(f'Result: {result}')\n\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        ),
        "overwrite": False,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/projects/"
            f"{project_id}/files",
            json=payload,
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 201
            and data.get("success") is True
            and data.get("path")
            == payload["path"]
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_list_files(project_id):
    name = (
        f"GET /projects/{project_id}/files"
    )

    try:
        response = requests.get(
            f"{BASE_URL}/projects/"
            f"{project_id}/files",
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and isinstance(data, list)
            and any(
                item.get("path")
                == "src/main.py"
                for item in data
            )
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_read_file(project_id):
    name = (
        f"GET /projects/{project_id}"
        "/files/content"
    )

    params = {
        "path": "src/main.py"
    }

    try:
        response = requests.get(
            f"{BASE_URL}/projects/"
            f"{project_id}/files/content",
            params=params,
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("path")
            == "src/main.py"
            and "def add(a, b)"
            in data.get("content", "")
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_update_file(project_id):
    name = (
        f"PUT /projects/{project_id}"
        "/files/content"
    )

    params = {
        "path": "src/main.py"
    }

    payload = {
        "content": (
            "def add(a, b):\n"
            "    return a + b\n\n\n"
            "def subtract(a, b):\n"
            "    return a - b\n\n\n"
            "def main():\n"
            "    print(add(5, 3))\n"
            "    print(subtract(5, 3))\n\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
    }

    try:
        response = requests.put(
            f"{BASE_URL}/projects/"
            f"{project_id}/files/content",
            params=params,
            json=payload,
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and data.get("path")
            == "src/main.py"
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_verify_updated_file(project_id):
    name = (
        "Verify Updated File Content"
    )

    params = {
        "path": "src/main.py"
    }

    try:
        response = requests.get(
            f"{BASE_URL}/projects/"
            f"{project_id}/files/content",
            params=params,
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and "def subtract(a, b)"
            in data.get("content", "")
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_duplicate_file(project_id):
    name = (
        "POST File - Duplicate File Test"
    )

    payload = {
        "path": "src/main.py",
        "content": "Duplicate content",
        "overwrite": False,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/projects/"
            f"{project_id}/files",
            json=payload,
            timeout=10,
        )

        success = (
            response.status_code == 409
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_path_traversal(project_id):
    name = (
        "File Path Traversal Security Test"
    )

    payload = {
        "path": (
            "../../outside_workspace.txt"
        ),
        "content": (
            "This should never be created."
        ),
        "overwrite": False,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/projects/"
            f"{project_id}/files",
            json=payload,
            timeout=10,
        )

        success = (
            response.status_code == 403
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Phase 3 - Coding Agent Tests
# ============================================================

def test_coding_agent(project_id):
    """
    Test the Coding Agent with the existing
    project context.
    """

    name = (
        f"POST /projects/{project_id}/agent"
    )

    payload = {
        "task": (
            "Analyze the current project structure "
            "and explain what the existing Python "
            "code does. Suggest two improvements."
        ),
        "temperature": 0.2,
        "max_tokens": 512,
    }

    try:
        print(
            "\nRunning Coding Agent..."
        )

        response = requests.post(
            f"{BASE_URL}/projects/"
            f"{project_id}/agent",
            json=payload,
            timeout=300,
        )

        try:
            data = response.json()
        except ValueError:
            data = {}

        success = (
            response.status_code == 200
        )

        # Accept common response structures while
        # still ensuring the agent returned content.
        if success:

            response_text = (
                data.get("response")
                or data.get("result")
                or data.get("message")
                or data.get("content")
            )

            success = (
                isinstance(
                    response_text,
                    str,
                )
                and len(
                    response_text.strip()
                ) > 0
            )

        print_result(
            name,
            success,
            response,
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_coding_agent_project_not_found():
    """
    Verify the Coding Agent returns 404
    for a project that does not exist.
    """

    name = (
        "POST /projects/999999/agent "
        "- Not Found Test"
    )

    payload = {
        "task": (
            "Analyze this project."
        ),
        "temperature": 0.2,
        "max_tokens": 128,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/projects/"
            "999999/agent",
            json=payload,
            timeout=30,
        )

        success = (
            response.status_code == 404
        )

        print_result(
            name,
            success,
            response,
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_coding_agent_validation(project_id):
    """
    Verify request validation rejects
    an empty task and invalid parameters.
    """

    name = (
        "POST /projects/"
        f"{project_id}/agent "
        "- Validation Test"
    )

    payload = {
        "task": "",
        "temperature": 5,
        "max_tokens": -10,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/projects/"
            f"{project_id}/agent",
            json=payload,
            timeout=30,
        )

        success = (
            response.status_code == 422
        )

        print_result(
            name,
            success,
            response,
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Phase 2 - Remaining File Tests
# ============================================================

def test_delete_file(project_id):
    name = (
        f"DELETE /projects/{project_id}"
        "/files"
    )

    params = {
        "path": "src/main.py"
    }

    try:
        response = requests.delete(
            f"{BASE_URL}/projects/"
            f"{project_id}/files",
            params=params,
            timeout=10,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and data.get("path")
            == "src/main.py"
        )

        print_result(
            name,
            success,
            response,
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_deleted_file_not_found(project_id):
    name = (
        "GET Deleted File "
        "- Not Found Test"
    )

    params = {
        "path": "src/main.py"
    }

    try:
        response = requests.get(
            f"{BASE_URL}/projects/"
            f"{project_id}/files/content",
            params=params,
            timeout=10,
        )

        success = (
            response.status_code == 404
        )

        print_result(
            name,
            success,
            response,
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Project Deletion Tests
# ============================================================

def test_delete_project(project_id):
    name = (
        f"DELETE /projects/{project_id}"
    )

    try:
        response = requests.delete(
            f"{BASE_URL}/projects/"
            f"{project_id}",
            timeout=20,
        )

        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
        )

        print_result(
            name,
            success,
            response,
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_workspace_deleted(workspace_path):
    name = (
        "Project Workspace Deleted"
    )

    try:
        path = Path(workspace_path)

        success = (
            not path.exists()
        )

        print_result(
            name,
            success,
            extra={
                "workspace_path": str(path),
                "workspace_exists": (
                    path.exists()
                ),
            },
        )

        return success

    except Exception as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_deleted_project_not_found(project_id):
    name = (
        f"GET /projects/{project_id} "
        "After Delete"
    )

    try:
        response = requests.get(
            f"{BASE_URL}/projects/"
            f"{project_id}",
            timeout=10,
        )

        success = (
            response.status_code == 404
        )

        print_result(
            name,
            success,
            response,
        )

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


# ============================================================
# Test Runner
# ============================================================

def run_tests():

    print("=" * 60)

    print(
        "LOCAL CODEX - "
        "PHASE 1 + PHASE 2 + PHASE 3 API TESTS"
    )

    print("=" * 60)

    results = []

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    results.append(
        test_health()
    )

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------

    results.append(
        test_llm_info()
    )

    results.append(
        test_llm_status()
    )

    results.append(
        test_load_model()
    )

    results.append(
        test_llm_status(
            expected_loaded=True
        )
    )

    # --------------------------------------------------------
    # Chat
    # --------------------------------------------------------

    results.append(
        test_chat()
    )

    results.append(
        test_chat_stream()
    )

    results.append(
        test_chat_validation()
    )

    # --------------------------------------------------------
    # Projects + Workspaces
    # --------------------------------------------------------

    (
        project_created,
        project_id,
        workspace_path,
    ) = test_create_project()

    results.append(
        project_created
    )

    if (
        project_created
        and project_id is not None
        and workspace_path is not None
    ):

        # ----------------------------------------------------
        # Workspace
        # ----------------------------------------------------

        results.append(
            test_workspace_exists(
                workspace_path
            )
        )

        results.append(
            test_readme_content(
                workspace_path
            )
        )

        # ----------------------------------------------------
        # Projects
        # ----------------------------------------------------

        results.append(
            test_list_projects()
        )

        results.append(
            test_get_project(
                project_id
            )
        )

        # ----------------------------------------------------
        # Files
        # ----------------------------------------------------

        results.append(
            test_create_file(
                project_id
            )
        )

        results.append(
            test_list_files(
                project_id
            )
        )

        results.append(
            test_read_file(
                project_id
            )
        )

        results.append(
            test_update_file(
                project_id
            )
        )

        results.append(
            test_verify_updated_file(
                project_id
            )
        )

        results.append(
            test_duplicate_file(
                project_id
            )
        )

        results.append(
            test_path_traversal(
                project_id
            )
        )

        # ----------------------------------------------------
        # Phase 3 - Coding Agent
        #
        # Run BEFORE deleting the test file so
        # the agent has real project code to analyze.
        # ----------------------------------------------------

        results.append(
            test_coding_agent(
                project_id
            )
        )

        results.append(
            test_coding_agent_validation(
                project_id
            )
        )

        results.append(
            test_coding_agent_project_not_found()
        )

        # ----------------------------------------------------
        # Delete File
        # ----------------------------------------------------

        results.append(
            test_delete_file(
                project_id
            )
        )

        results.append(
            test_deleted_file_not_found(
                project_id
            )
        )

        # ----------------------------------------------------
        # Project Update
        # ----------------------------------------------------

        results.append(
            test_update_project(
                project_id
            )
        )

        results.append(
            test_workspace_still_exists(
                workspace_path
            )
        )

        results.append(
            test_project_not_found()
        )

        # ----------------------------------------------------
        # Delete Project
        # ----------------------------------------------------

        results.append(
            test_delete_project(
                project_id
            )
        )

        results.append(
            test_workspace_deleted(
                workspace_path
            )
        )

        results.append(
            test_deleted_project_not_found(
                project_id
            )
        )

    else:

        print(
            "\nSkipping remaining project, "
            "workspace, file, and Coding Agent "
            "tests because project creation failed."
        )

    # --------------------------------------------------------
    # Unload Model
    # --------------------------------------------------------

    results.append(
        test_unload_model()
    )

    results.append(
        test_llm_status(
            expected_loaded=False
        )
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    passed = sum(results)

    total = len(results)

    print(
        "\n" + "=" * 60
    )

    print(
        "TEST SUMMARY"
    )

    print(
        "=" * 60
    )

    print(
        f"Passed: {passed}/{total}"
    )

    if passed == total:

        print(
            "\nALL API, WORKSPACE, FILE, "
            "AND CODING AGENT TESTS PASSED! 🎉"
        )

        return 0

    print(
        "\nSOME TESTS FAILED."
    )

    return 1


if __name__ == "__main__":

    exit_code = run_tests()

    sys.exit(exit_code)