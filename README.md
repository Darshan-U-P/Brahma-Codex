
# Local Codex

> A local AI-powered software development platform designed to progressively evolve from a local coding assistant into an autonomous software development environment.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Project Vision](#project-vision)
- [Current Development Status](#current-development-status)
- [Core Goals](#core-goals)
- [Technology Stack](#technology-stack)
- [Hardware Environment](#hardware-environment)
- [Current AI Model](#current-ai-model)
- [Current Architecture](#current-architecture)
- [Project Structure](#project-structure)
- [Completed Features](#completed-features)
- [API Endpoints](#api-endpoints)
- [Workspace System](#workspace-system)
- [Security Features](#security-features)
- [Automated Testing](#automated-testing)
- [Development Roadmap](#development-roadmap)
- [Detailed Phase Status](#detailed-phase-status)
- [How to Run](#how-to-run)
- [How to Test](#how-to-test)
- [Current Milestone](#current-milestone)
- [Future Architecture](#future-architecture)
- [Final Vision](#final-vision)

---

# Project Overview

Local Codex is a software development platform powered by a **local Large Language Model (LLM)**.

The purpose of the project is to build a system capable of helping create many different types of software, including:

- Python applications
- Websites
- Web applications
- REST APIs
- Backend systems
- Desktop applications
- Command-line tools
- Development tools
- System software
- C and C++ projects
- Experimental operating system projects

The system uses local AI models instead of requiring cloud AI services.

The long-term project vision is similar in concept to AI-assisted development environments and coding agents, but with a focus on:

- Local execution
- Local models
- User control
- Modular architecture
- Extensible agents
- Automated software development workflows

---

# Project Vision

The final goal is to create an AI-powered system capable of transforming a software idea into a working project.

The high-level workflow will eventually be:

```text
User Idea
    │
    ▼
Requirement Analysis
    │
    ▼
Project Planning
    │
    ▼
Project Creation
    │
    ▼
AI Code Generation
    │
    ▼
File Generation
    │
    ▼
Terminal Execution
    │
    ▼
Build
    │
    ▼
Testing
    │
    ▼
Debugging
    │
    ▼
Code Review
    │
    ▼
Improvement
    │
    ▼
Working Software
```

The project will gradually move from a simple local LLM interface to a more advanced autonomous software development environment.

---

# Current Development Status

## Overall Status

```text
PHASE 1   → COMPLETED
PHASE 2   → COMPLETED
PHASE 3   → COMPLETED (File System + Read-Only Coding Agent)
PHASE 4   → NOT STARTED
PHASE 5   → NOT STARTED
PHASE 6   → NOT STARTED
PHASE 7   → NOT STARTED
PHASE 8   → NOT STARTED
PHASE 9   → NOT STARTED
PHASE 10  → NOT STARTED
PHASE 11  → NOT STARTED
PHASE 12  → NOT STARTED
PHASE 13  → NOT STARTED
```

## Current Milestone

```text
CURRENT POSITION:

PHASE 1 → COMPLETED
        ↓
PHASE 2 → COMPLETED
        ↓
PHASE 3 → COMPLETED: FILE SYSTEM + READ-ONLY CODING AGENT
    ↓
PHASE 4 → NEXT: TERMINAL EXECUTION
```

---

# Core Goals

Local Codex is being developed to eventually support the following capabilities.

## Local AI

- Run LLMs locally
    
- Load GGUF models
    
- Switch between models
    
- Configure model settings
    
- Configure GPU usage
    
- Generate responses
    
- Stream responses
    
- Use models for coding tasks
    

## Project Management

- Create projects
    
- Manage project metadata
    
- Create workspaces
    
- Manage files
    
- Manage directories
    
- Track project state
    

## AI Coding

- Analyze project context
    
- Understand existing code
    
- Generate new code
    
- Modify existing code
    
- Create multiple files
    
- Plan implementation steps
    

## Terminal Integration

- Execute commands
    
- Capture command output
    
- Capture errors
    
- Manage processes
    
- Run project tools
    

## Testing

- Generate tests
    
- Execute tests
    
- Analyze failures
    
- Suggest fixes
    
- Apply approved fixes
    

## Debugging

- Analyze errors
    
- Read stack traces
    
- Locate relevant files
    
- Generate fixes
    
- Re-run tests
    

## Autonomous Development

Eventually, the system should support a workflow where multiple AI agents cooperate.

For example:

```text
Planner Agent
      │
      ▼
Coding Agent
      │
      ▼
Testing Agent
      │
      ▼
Debugging Agent
      │
      ▼
Review Agent
      │
      ▼
Final Result
```

---

# Technology Stack

## Backend

The current backend uses:

- Python
    
- FastAPI
    
- Pydantic
    
- SQLite
    

## Local AI

The current local AI stack uses:

- llama.cpp
    
- llama-cpp-python
    
- GGUF model format
    

## API

The backend exposes a REST API using FastAPI.

The API can currently handle:

- Health checks
    
- LLM management
    
- Chat requests
    
- Streaming responses
    
- Project management
    
- Workspace management
    
- File management

- Coding Agent requests

- Read-only project context analysis
    

---

# Hardware Environment

The current development machine configuration is approximately:

```text
RAM:
32 GB

GPU:
NVIDIA RTX 3050 Ti

GPU VRAM:
4 GB

CPU:
Intel Core i7
```

Because the GPU has limited VRAM, the current configuration is designed to allow a significant portion of model inference to run using system RAM and CPU, with optional GPU acceleration depending on the installed `llama-cpp-python` backend and configuration.

---

# Current AI Model

The currently configured model is:

```text
Qwen2.5-Coder-7B-Instruct
```

Model format:

```text
GGUF
```

Current quantization:

```text
Q4_K_M
```

The model file currently used by the project is:

```text
qwen2.5-coder-7b-instruct-q4_k_m.gguf
```

This model is being used as the initial local coding model for Local Codex.

---

# Current Architecture

The current architecture is:

```text
┌──────────────────────────────┐
│          Client              │
│                              │
│  Browser / Postman / Future  │
│  Desktop IDE / Frontend      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        FastAPI Backend       │
│                              │
│         app/main.py          │
└──────────────┬───────────────┘
               │
       ┌───────┼────────┐
       │       │        │
       ▼       ▼        ▼
┌──────────┐ ┌───────┐ ┌──────────┐
│   LLM    │ │Projects│ │  Files   │
│   API    │ │   API  │ │   API    │
└────┬─────┘ └───┬───┘ └────┬─────┘
     │           │          │
     ▼           ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ llama.cpp│ │ SQLite   │ │ Workspace│
│ Local LLM│ │ Database │ │ File Sys │
└──────────┘ └──────────┘ └──────────┘
```

---

# Project Structure

The current project structure is approximately:

```text
local-codex/
│
├── README.md
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── files.py
│   │   │   ├── health.py
│   │   │   ├── llm.py
│   │   │   └── projects.py
│   │   │
│   │   ├── core/
│   │   │   │
│   │   │   ├── config.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   │
│   │   ├── database/
│   │   │   │
│   │   │   ├── init_db.py
│   │   │   └── ...
│   │   │
│   │   ├── llm/
│   │   │   │
│   │   │   ├── client.py
│   │   │   └── ...
│   │   │
│   │   ├── models/
│   │   │   │
│   │   │   └── ...
│   │   │
│   │   ├── schemas/
│   │   │   │
│   │   │   ├── file.py
│   │   │   ├── project.py
│   │   │   └── ...
│   │   │
│   │   ├── services/
│   │   │   │
│   │   │   └── ...
│   │   │
│   │   └── main.py
│   │
│   ├── local_codex.db
│   │
│   └── test_api.py
│
├── models/
│   │
│   └── qwen2.5-coder-7b-instruct-q4_k_m.gguf
│
└── workspace/
    │
    └── Project workspaces are created here
```

The structure will expand as new phases are implemented.

---

# Completed Features

## PHASE 1 — Local LLM Foundation

### Status

```text
COMPLETED
```

---

## Backend Foundation

Completed:

- FastAPI application
    
- Application configuration
    
- Logging
    
- Exception handling
    
- Health endpoint
    
- Root endpoint
    
- API router structure
    

---

## Local LLM Integration

Completed:

- Local model configuration
    
- GGUF model support
    
- llama.cpp integration
    
- `llama-cpp-python` integration
    
- Model loading
    
- Model unloading
    
- Model status checking
    
- Model information endpoint
    
- Local text generation
    

---

## LLM Endpoints

### Get LLM Status

```text
GET /llm/status
```

Example response:

```json
{
  "loaded": true
}
```

---

### Get LLM Information

```text
GET /llm/info
```

Example information includes:

```json
{
  "loaded": false,
  "model_path": "path/to/model.gguf",
  "model_exists": true,
  "context_size": 8192,
  "gpu_layers": 0
}
```

---

### Load Model

```text
POST /llm/load
```

Example response:

```json
{
  "success": true,
  "loaded": true,
  "message": "Model loaded successfully."
}
```

---

### Unload Model

```text
POST /llm/unload
```

Example response:

```json
{
  "success": true,
  "loaded": false,
  "message": "Model unloaded successfully."
}
```

---

# Chat System

## Normal Chat

Endpoint:

```text
POST /chat
```

Example request:

```json
{
  "message": "Explain Python",
  "temperature": 0.7,
  "max_tokens": 500
}
```

Example response:

```json
{
  "response": "Python is a programming language..."
}
```

---

## Streaming Chat

Endpoint:

```text
POST /chat/stream
```

The endpoint supports streamed AI output.

The client receives response chunks and eventually receives:

```text
data: [DONE]
```

---

## Input Validation

The API validates:

- Empty messages
    
- Invalid temperatures
    
- Invalid token counts
    

Invalid requests correctly return:

```text
HTTP 422
```

---

# PHASE 2 — Project Management

### Status

```text
COMPLETED FOR CURRENT IMPLEMENTED SCOPE
```

The project management system currently provides the foundation required for future coding agents.

---

# Database

The backend currently uses SQLite.

Database file:

```text
backend/local_codex.db
```

The database stores project information.

Project information includes fields such as:

- ID
    
- Name
    
- Description
    
- Project type
    
- Status
    
- Workspace path
    
- Creation time
    
- Update time
    

---

# Project Management Features

Completed:

- Create project
    
- List projects
    
- Get project
    
- Update project
    
- Delete project
    
- Handle missing projects
    
- Manage project metadata
    

---

# Project Endpoints

## Create Project

```text
POST /projects
```

Example request:

```json
{
  "name": "My Application",
  "description": "My first Local Codex project",
  "project_type": "python"
}
```

The API creates:

- A database project record
    
- A workspace directory
    
- A `src` directory
    
- A `tests` directory
    
- A project README file
    

---

## List Projects

```text
GET /projects
```

Returns a list of available projects.

---

## Get Project

```text
GET /projects/{project_id}
```

Returns project information.

---

## Update Project

```text
PUT /projects/{project_id}
```

Updates project metadata.

---

## Delete Project

```text
DELETE /projects/{project_id}
```

Deletes:

- Project database record
    
- Project workspace
    

---

# Workspace System

Each project automatically receives its own workspace.

Example:

```text
workspace/
│
└── automated-test-project-1/
    │
    ├── README.md
    │
    ├── src/
    │
    └── tests/
```

Example workspace path:

```text
workspace/automated-test-project-1
```

The workspace system provides the file foundation required for the future Coding Agent.

---

# File Management

### Status

```text
COMPLETED
```

The backend can currently manage project files.

---

# File Features

Completed:

- Create file
    
- Read file content
    
- Update file
    
- Delete file
    
- List files
    
- List directories
    

---

# Create File

Endpoint:

```text
POST /projects/{project_id}/files
```

Example use:

```text
src/main.py
```

The file is created inside the project's workspace.

---

# List Files

Endpoint:

```text
GET /projects/{project_id}/files
```

Example response structure:

```json
[
  {
    "path": "README.md",
    "name": "README.md",
    "type": "file",
    "size": 90
  },
  {
    "path": "src",
    "name": "src",
    "type": "directory",
    "size": null
  }
]
```

---

# Read File Content

Endpoint:

```text
GET /projects/{project_id}/files/content
```

The API returns:

- File path
    
- File content
    

---

# Update File

Endpoint:

```text
PUT /projects/{project_id}/files/content
```

The API updates an existing project file.

---

# Delete File

Endpoint:

```text
DELETE /projects/{project_id}/files
```

The API deletes an existing file from the project workspace.

---

# Security Features

The current file system includes important security protections.

## Path Traversal Protection

The API prevents attempts to access files outside the project workspace.

Example blocked attempt:

```text
../../some-sensitive-file
```

The API returns:

```text
HTTP 403
```

with an error similar to:

```text
Access outside the project workspace is not allowed.
```

---

## Duplicate File Protection

The system prevents accidental creation of an already existing file.

Example result:

```text
HTTP 409
```

Example message:

```text
File already exists: src/main.py
```

---

# Automated Testing

The project currently contains an automated API testing script.

Location:

```text
backend/test_api.py
```

The test script uses:

```text
requests
```

to communicate with the running FastAPI backend.

---

# Current Test Coverage

The automated test suite currently verifies:

## Health

- Health endpoint
    

## LLM

- LLM information
    
- Initial model status
    
- Model loading
    
- Loaded model status
    
- Model unloading
    
- Unloaded model status
    

## Chat

- Normal AI response
    
- Streaming AI response
    
- Streaming completion
    
- Request validation
    

## Projects

- Project creation
    
- Project listing
    
- Project retrieval
    
- Project update
    
- Missing project handling
    
- Project deletion
    
- Deleted project handling
    

## Workspaces

- Workspace creation
    
- Workspace directory validation
    
- `src` directory creation
    
- `tests` directory creation
    
- README generation
    
- Workspace persistence after metadata update
    
- Workspace deletion
    

## Files

- File creation
    
- File listing
    
- File content retrieval
    
- File updates
    
- Updated content verification
    
- Duplicate file protection
    
- Path traversal protection
    
- File deletion
    
- Deleted file validation
    

---

# Latest Test Result

The latest recorded test run successfully passed:

```text
Passed: 30/30
```

Result:

```text
ALL API, WORKSPACE, AND FILE TESTS PASSED!
```

This confirms that the currently implemented foundation is working correctly.

---

# Development Roadmap

Local Codex is divided into thirteen major phases.

```text
PHASE 1  → Local LLM Foundation
PHASE 2  → Project Management
PHASE 3  → Coding Agent
PHASE 4  → Terminal Execution
PHASE 5  → Build/Test/Debug
PHASE 6  → Software Generator
PHASE 7  → Multi-Agent System
PHASE 8  → Multiple App Types
PHASE 9  → Full Visual IDE
PHASE 10 → Model Management
PHASE 11 → Advanced Integrations
PHASE 12 → Systems & OS Development
PHASE 13 → Autonomous Software Factory
```

---

# Detailed Phase Status

---

# PHASE 1 — Local LLM Foundation

## Status

```text
COMPLETED
```

## Completed

- FastAPI backend
    
- Local LLM integration
    
- llama.cpp support
    
- GGUF model support
    
- Qwen2.5-Coder integration
    
- Model load API
    
- Model unload API
    
- Model status API
    
- Model information API
    
- Chat API
    
- Streaming chat API
    
- Request validation
    
- Logging
    
- Exception handling
    
- Automated tests
    

## Remaining Improvements

Possible future improvements:

- GPU configuration API
    
- Performance metrics
    
- Model warm-up
    
- Multiple context profiles
    
- Better prompt templates
    
- Conversation memory
    
- Token usage metrics
    

---

# PHASE 2 — Project Management

## Status

```text
COMPLETED FOR CURRENT FOUNDATION
```

## Completed

- SQLite database
    
- Project creation
    
- Project listing
    
- Project retrieval
    
- Project update
    
- Project deletion
    
- Workspace creation
    
- Workspace deletion
    
- README generation
    
- Source directory creation
    
- Test directory creation
    
- File creation
    
- File reading
    
- File updates
    
- File deletion
    
- File listing
    
- Path traversal protection
    
- Duplicate file protection
    

## Remaining Improvements

Possible future improvements:

- Project templates
    
- Project settings
    
- Project dependencies
    
- Project configuration files
    
- Project history
    
- File versioning
    
- Project backups
    
- Workspace import
    
- Workspace export
    

---

# PHASE 3 — Coding Agent

## Status

```text
COMPLETED
```

Phase 3 delivers the File System + Read-Only Coding Agent foundation.

The Coding Agent can inspect a project and use the local LLM to provide coding guidance without modifying files or executing commands.

---

## Implemented Architecture

```text
User Request
      │
      ▼
Coding Agent
      │
    ├── Collect project metadata and file context
      │
    ├── Analyze existing readable files
      │
    ├── Build a coding prompt
      │
    ├── Send the request to the local LLM
      │
    ├── Return the generated text response
      │
      └── Return Structured Result
```

---

## Completed Features

### Agent Architecture

Implemented modules:

```text
app/
└── agents/
    ├── agent.py
    ├── project_context.py
    └── coding_agent.py
```

---

### Project Context Collection

The agent collects:

- Project ID
    
- Project name
    
- Description
    
- Project type
    
- Workspace path
    
- Existing file list
    
- Relevant file contents
    

---

### Prompt Construction

The system constructs coding prompts using:

```text
System Instructions
        +
Project Information
        +
Existing Files
        +
User Request
```

---

### Read-Only LLM Analysis

The agent sends project context and the user's task to the local LLM and returns a non-empty text response. It explicitly does not claim to modify files.

Example request:

```json
{
  "plan": "Create a calculator application",
  "files": [
    {
      "path": "src/main.py",
      "content": "..."
    }
  ]
}
```

---

### File System Safety

The agent reads project files for context only. File creation, updates, deletion, and path traversal protections remain controlled by the existing File Management API.

---

### Agent API

The implemented endpoint is:

```text
POST /projects/{project_id}/agent
```

Example request:

```json
{
  "task": "Create a Python calculator application"
}
```

---

The endpoint validates the project, confirms that the local model is loaded, and returns the project ID, task, and generated response.

---

### Automated Agent Tests

The API test suite verifies:

- Successful Coding Agent responses
- Request validation
- Missing project handling
- Integration with project and file workflows

Phase 3 does not yet include structured multi-file generation, file modification, terminal execution, or automated testing and debugging.
    

---

# PHASE 4 — Terminal Execution

## Status

```text
NOT STARTED
```

## Main Goal

Allow Local Codex to execute development commands.

---

## Planned Features

- Execute commands
    
- Select working directory
    
- Capture stdout
    
- Capture stderr
    
- Capture exit codes
    
- Command timeout
    
- Process management
    

Example:

```text
python src/main.py
```

Example workflow:

```text
Coding Agent
      │
      ▼
Generate Code
      │
      ▼
Terminal Service
      │
      ▼
Execute Command
      │
      ▼
Capture Output
```

---

## Important Security Work

Terminal execution must be carefully designed.

Planned controls may include:

- Workspace restrictions
    
- Command allowlists or policies
    
- Timeouts
    
- Process limits
    
- Explicit user approval for sensitive actions
    

---

# PHASE 5 — Build/Test/Debug

## Status

```text
NOT STARTED
```

## Main Goal

Allow the system to automatically test generated software and analyze failures.

---

## Planned Features

- Run tests
    
- Run build commands
    
- Capture errors
    
- Analyze stack traces
    
- Identify relevant files
    
- Ask AI to suggest fixes
    
- Apply approved fixes
    
- Re-run tests
    

Workflow:

```text
Generate Code
      │
      ▼
Run Tests
      │
      ▼
Pass?
 ┌────┴────┐
 │         │
YES       NO
 │         │
 ▼         ▼
Done    Analyze Error
              │
              ▼
          Generate Fix
              │
              ▼
          Run Tests Again
```

---

# PHASE 6 — Software Generator

## Status

```text
NOT STARTED
```

## Main Goal

Generate complete software projects from high-level requirements.

---

## Planned Features

- Requirement analysis
    
- Software planning
    
- Project structure generation
    
- Multi-file code generation
    
- Dependency planning
    
- Configuration generation
    
- Documentation generation
    

Example request:

```text
Create a task management REST API using Python.
```

The system should eventually generate:

```text
project/
│
├── src/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── models/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# PHASE 7 — Multi-Agent System

## Status

```text
NOT STARTED
```

## Main Goal

Create specialized AI agents that cooperate.

---

## Planned Agents

### Planning Agent

Responsible for:

- Requirement analysis
    
- Architecture planning
    
- Task decomposition
    

### Coding Agent

Responsible for:

- Code generation
    
- Code modification
    
- File generation
    

### Testing Agent

Responsible for:

- Test generation
    
- Test execution
    
- Failure analysis
    

### Debugging Agent

Responsible for:

- Error analysis
    
- Fix generation
    
- Validation
    

### Review Agent

Responsible for:

- Code review
    
- Quality checks
    
- Architecture feedback
    

---

## Planned Multi-Agent Workflow

```text
User Request
      │
      ▼
Planning Agent
      │
      ▼
Coding Agent
      │
      ▼
Testing Agent
      │
      ├──── PASS ────► Review Agent
      │
      └──── FAIL
              │
              ▼
        Debugging Agent
              │
              ▼
         Testing Agent
```

---

# PHASE 8 — Multiple App Types

## Status

```text
NOT STARTED
```

## Planned Application Types

### Python Applications

- Scripts
    
- Automation tools
    
- CLI applications
    

### Web Applications

- Frontend projects
    
- Backend projects
    
- Full-stack applications
    

### APIs

- REST APIs
    
- Local services
    

### Desktop Applications

Possible technologies:

- PySide
    
- PyQt
    
- Tkinter
    
- Other supported frameworks
    

### Mobile Applications

Potential future support:

- Flutter
    
- React Native
    
- Other frameworks
    

### System Projects

- C projects
    
- C++ projects
    
- Rust projects
    
- Build systems
    

---

# PHASE 9 — Full Visual IDE

## Status

```text
NOT STARTED
```

## Main Goal

Create a graphical development environment.

---

## Planned Features

- Project explorer
    
- File tree
    
- Code editor
    
- AI chat
    
- Agent task panel
    
- Integrated terminal
    
- Build output
    
- Test output
    
- Error viewer
    
- Model selection
    

Concept:

```text
┌───────────────────────────────────────────────┐
│ Local Codex                                  │
├───────────────┬───────────────────────────────┤
│ File Explorer │ Code Editor                   │
│               │                               │
│ project/      │ def main():                   │
│ ├── src       │     print("Hello")            │
│ └── tests     │                               │
│               │                               │
├───────────────┴───────────────────────────────┤
│ AI Assistant / Agent Output                   │
├───────────────────────────────────────────────┤
│ Terminal                                      │
└───────────────────────────────────────────────┘
```

---

# PHASE 10 — Model Management

## Status

```text
NOT STARTED
```

## Planned Features

- Multiple model support
    
- Model selection
    
- Model configuration
    
- Model profiles
    
- Context configuration
    
- GPU layer configuration
    
- CPU configuration
    
- Model information
    
- Model performance monitoring
    

Possible model categories:

```text
Coding Model
General Model
Planning Model
Small Fast Model
Large High-Quality Model
```

---

# PHASE 11 — Advanced Integrations

## Status

```text
NOT STARTED
```

## Planned Features

- Git integration
    
- GitHub integration
    
- Package management
    
- Dependency installation
    
- Build tool integration
    
- External development tools
    

Potential workflows:

```text
Generate Code
      │
      ▼
Run Tests
      │
      ▼
Git Commit
      │
      ▼
Push to Remote Repository
```

Such actions should use appropriate permissions and user controls.

---

# PHASE 12 — Systems & OS Development

## Status

```text
NOT STARTED
```

## Main Goal

Expand Local Codex toward system-level development workflows.

---

## Planned Areas

- C development
    
- C++ development
    
- Rust development
    
- Build systems
    
- Cross-compilation
    
- Toolchain management
    
- Low-level project workflows
    
- Experimental operating system development
    

Potential project support:

```text
Operating System Project
│
├── boot/
├── kernel/
├── drivers/
├── memory/
├── filesystem/
└── build/
```

This phase focuses on providing development workflows and tooling support. It does not imply unrestricted autonomous execution of arbitrary system-level operations.

---

# PHASE 13 — Autonomous Software Factory

## Status

```text
NOT STARTED
```

## Final Goal

The final vision is an advanced system that can coordinate software development tasks.

The workflow may eventually look like:

```text
USER IDEA
    │
    ▼
REQUIREMENT ANALYSIS
    │
    ▼
PROJECT PLANNING
    │
    ▼
ARCHITECTURE DESIGN
    │
    ▼
TASK DECOMPOSITION
    │
    ▼
CODE GENERATION
    │
    ▼
FILE GENERATION
    │
    ▼
DEPENDENCY SETUP
    │
    ▼
BUILD
    │
    ▼
TEST
    │
    ├──── PASS ────► REVIEW
    │
    └──── FAIL
              │
              ▼
            DEBUG
              │
              ▼
            REBUILD
              │
              ▼
             TEST
              │
              ▼
         WORKING SOFTWARE
```

The system should remain modular and user-controlled.

---

# Future Architecture

The future backend architecture may evolve toward:

```text
app/
│
├── agents/
│   ├── planner_agent.py
│   ├── coding_agent.py
│   ├── testing_agent.py
│   ├── debugging_agent.py
│   └── review_agent.py
│
├── api/
│   ├── chat.py
│   ├── projects.py
│   ├── files.py
│   ├── agents.py
│   ├── terminal.py
│   ├── builds.py
│   └── models.py
│
├── core/
│   ├── config.py
│   ├── logging.py
│   ├── exceptions.py
│   └── security.py
│
├── database/
│   ├── init_db.py
│   ├── projects.py
│   ├── tasks.py
│   └── history.py
│
├── llm/
│   ├── client.py
│   ├── prompts.py
│   ├── parser.py
│   └── model_manager.py
│
├── services/
│   ├── project_service.py
│   ├── file_service.py
│   ├── terminal_service.py
│   ├── build_service.py
│   └── workspace_service.py
│
├── schemas/
│   ├── project.py
│   ├── file.py
│   ├── agent.py
│   └── terminal.py
│
└── main.py
```

The exact structure may change as the project evolves.

---

# API Endpoints

## System

### Root

```text
GET /
```

### Health

```text
GET /health
```

---

# LLM

### Model Status

```text
GET /llm/status
```

### Model Information

```text
GET /llm/info
```

### Load Model

```text
POST /llm/load
```

### Unload Model

```text
POST /llm/unload
```

---

# Chat

### Generate Response

```text
POST /chat
```

### Stream Response

```text
POST /chat/stream
```

---

# Projects

### Create Project

```text
POST /projects
```

### List Projects

```text
GET /projects
```

### Get Project

```text
GET /projects/{project_id}
```

### Update Project

```text
PUT /projects/{project_id}
```

### Delete Project

```text
DELETE /projects/{project_id}
```

---

# Files

### Create File

```text
POST /projects/{project_id}/files
```

### List Files

```text
GET /projects/{project_id}/files
```

### Read File Content

```text
GET /projects/{project_id}/files/content
```

### Update File Content

```text
PUT /projects/{project_id}/files/content
```

### Delete File

```text
DELETE /projects/{project_id}/files
```

---

# How to Run the Backend

## 1. Activate the Python Environment

From PowerShell:

```powershell
.\venv_cuda\Scripts\activate
```

---

## 2. Navigate to the Backend

Example:

```powershell
cd "D:\all project\Projects\AI projects\ai assentent\local-codex\backend"
```

---

## 3. Start the Server

Run:

```powershell
uvicorn app.main:app --reload
```

The server should start at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically provides API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The interactive API documentation can be used to test endpoints manually.

---

# How to Run Automated Tests

Make sure the FastAPI server is running.

Open another PowerShell terminal.

Activate the environment if necessary:

```powershell
.\venv_cuda\Scripts\activate
```

Navigate to the backend:

```powershell
cd "D:\all project\Projects\AI projects\ai assentent\local-codex\backend"
```

Run:

```powershell
python test_api.py
```

---

# Expected Test Flow

The test suite currently performs operations similar to:

```text
Health Check
    │
    ▼
LLM Information
    │
    ▼
Check Model Status
    │
    ▼
Load Model
    │
    ▼
Chat Test
    │
    ▼
Streaming Test
    │
    ▼
Validation Test
    │
    ▼
Create Project
    │
    ▼
Verify Workspace
    │
    ▼
Verify README
    │
    ▼
Create File
    │
    ▼
Read File
    │
    ▼
Update File
    │
    ▼
Verify Update
    │
    ▼
Security Tests
    │
    ▼
Delete File
    │
    ▼
Update Project
    │
    ▼
Delete Project
    │
    ▼
Verify Workspace Deleted
    │
    ▼
Unload Model
```

---

# Completed Test Result

The latest known successful automated test result is:

```text
Passed: 30/30

ALL API, WORKSPACE, AND FILE TESTS PASSED!
```

---

# What Is Completed?

## Completed Now

```text
✓ Local FastAPI backend

✓ Local LLM foundation

✓ llama.cpp integration

✓ Qwen2.5-Coder GGUF model

✓ Model loading

✓ Model unloading

✓ Model status

✓ Model information

✓ Normal chat

✓ Streaming chat

✓ Input validation

✓ SQLite database

✓ Project creation

✓ Project listing

✓ Project retrieval

✓ Project updates

✓ Project deletion

✓ Automatic workspace creation

✓ Automatic src directory

✓ Automatic tests directory

✓ Automatic project README

✓ Workspace deletion

✓ File creation

✓ File reading

✓ File updates

✓ File deletion

✓ File listing

✓ Duplicate file protection

✓ Path traversal protection

✓ Read-only Coding Agent

✓ Project context collection

✓ Coding Agent API

✓ Automated API tests

✓ 30/30 automated tests passing
```

---

# What Is Next?

The immediate next task is:

# PHASE 4 — Terminal Execution

The first objective is:

```text
Add controlled terminal execution within project workspaces.

Commands must use workspace restrictions, timeouts, process limits, and explicit user controls.
```

Planned areas include:

```text
Terminal service
Command execution policy
Output and error capture
Process management
```

---

# Development Principles

Local Codex should follow several important principles.

## Local First

Prefer local execution where practical.

---

## Modular Architecture

Major systems should remain separated.

Examples:

```text
LLM
Projects
Files
Agents
Terminal
Testing
Build System
```

---

## Test Before Moving Forward

Before considering a major feature complete:

```text
Implement
    ↓
Run Server
    ↓
Test Manually
    ↓
Run Automated Tests
    ↓
Fix Errors
    ↓
Continue
```

---

## Incremental Development

The project should be built in small, testable steps.

Avoid trying to build all phases simultaneously.

---

## Safety and User Control

As the project gains terminal and automation capabilities, potentially destructive operations should be designed with clear boundaries, permissions, and user control.

---

# Final Vision

The long-term vision of Local Codex is:

```text
┌─────────────────────────────────────────────┐
│                LOCAL CODEX                  │
│                                             │
│       Local AI Software Development         │
├─────────────────────────────────────────────┤
│                                             │
│  User Request                               │
│       │                                     │
│       ▼                                     │
│  Planning Agent                             │
│       │                                     │
│       ▼                                     │
│  Coding Agent                               │
│       │                                     │
│       ▼                                     │
│  File & Project System                      │
│       │                                     │
│       ▼                                     │
│  Terminal & Build System                    │
│       │                                     │
│       ▼                                     │
│  Testing Agent                              │
│       │                                     │
│       ▼                                     │
│  Debugging Agent                            │
│       │                                     │
│       ▼                                     │
│  Review Agent                               │
│       │                                     │
│       ▼                                     │
│  Working Software                           │
│                                             │
└─────────────────────────────────────────────┘
```

The system is intended to evolve step by step into a powerful local AI-assisted software development environment.

---

# Current Position

```text
╔══════════════════════════════════════════╗
║                                          ║
║             LOCAL CODEX                  ║
║                                          ║
║   PHASE 1  ██████████ COMPLETED          ║
║   PHASE 2  ██████████ COMPLETED          ║
║                                          ║
║   PHASE 3  ██████████ COMPLETED          ║
║   PHASE 4  ░░░░░░░░░░                    ║
║   PHASE 5  ░░░░░░░░░░                    ║
║   PHASE 6  ░░░░░░░░░░                    ║
║   PHASE 7  ░░░░░░░░░░                    ║
║   PHASE 8  ░░░░░░░░░░                    ║
║   PHASE 9  ░░░░░░░░░░                    ║
║   PHASE 10 ░░░░░░░░░░                    ║
║   PHASE 11 ░░░░░░░░░░                    ║
║   PHASE 12 ░░░░░░░░░░                    ║
║   PHASE 13 ░░░░░░░░░░                    ║
║                                          ║
║        NEXT: TERMINAL EXECUTION          ║
║                                          ║
╚══════════════════════════════════════════╝
```

---

# License

License information will be added when the project is prepared for public release.

---

# Project Status

**Local Codex is currently under active development.**

Current completed foundation:

```text
Local LLM
+
Project Management
+
Workspace Management
+
File Management
+
Automated Testing
```

Next development milestone:

```text
PHASE 4 — TERMINAL EXECUTION
```

This README reflects the **current state of the project based on the work completed so far**. Phase 3, **File System + Read-Only Coding Agent**, is complete. The next implementation milestone is Phase 4, **Terminal Execution**.