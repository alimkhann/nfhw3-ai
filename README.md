# Multi-Agent Habit Coaching System

**Purpose:**
This project demonstrates an agent-to-agent (A2A) architecture where two AI agents—one generating daily habit tasks and another validating user proofs—communicate via a WebSocket router. The user interacts through a simple CLI:

1. Send a habit to **Agent A**
2. Receive Easy/Medium/Hard tasks
3. Submit proof of completion to **Agent B** for validation

---

## Project Structure

* **`ws_server.py`**
  WebSocket router using the **`websockets`** library. It handles `register:<name>` and forwards `send:<recipient>:<content>` messages between clients.

* **`agent_a_task_creator.py`**
  Pydantic AI agent (`Agent("openai:gpt-3.5-turbo")`) registering as **`task_creator`**. Generates Easy/Medium/Hard tasks via WebSocket.

* **`agent_b_task_validator.py`**
  LangChain‑Gemini agent (`ChatGoogleGenerativeAI`) registering as **`task_validator`**. Validates user proofs and sends results back to **`user`**.

* **`user_cli.py`**
  CLI script registering as **`user`**. Sends a habit to **`task_creator`**, displays tasks, then sends proof to **`task_validator`** and prints the validation.

---

## Prerequisites

1. **Python 3.10+**

2. **Virtual Environment**
   Create and activate a venv before running scripts:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   # .\.venv\Scripts\Activate.ps1 # Windows PowerShell
   ```

3. **Dependencies** (in `requirements.txt`):

   ```text
   websockets
   pydantic_ai
   langchain-google-genai
   langchain-openai
   python-dotenv
   ```

4. **Environment Variables** (add to `.env` in project root):

   ```text
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=AIzaSy...
   ```

   * The **`ChatGoogleGenerativeAI`** class expects `GOOGLE_API_KEY` for Gemini authentication.

---

## Setup & Execution

1. **Activate the virtual environment** (if not already active):

   ```bash
   source .venv/bin/activate      # macOS/Linux
   # .\.venv\Scripts\Activate.ps1 # Windows PowerShell
   ```

2. **Install Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the WebSocket server** (ping disabled to avoid 1011 timeouts):

   ```bash
   python ws_server.py
   ```

4. **Run agents in separate terminals**:

   * **Agent A (task\_creator)**:

     ```bash
     python agent_a_task_creator.py
     ```
   * **Agent B (task\_validator)**:

     ```bash
     python agent_b_task_validator.py
     ```

5. **Launch the User CLI**:

   ```bash
   python user_cli.py
   ```

---

## Flow Summary

1. **User → Agent A**

   ```text
   send:task_creator:<habit>
   ```

   Agent A replies with Easy/Medium/Hard tasks.

2. **User → Agent B**

   ```text
   send:task_validator:<proof>
   ```

   Agent B returns a validation message.

3. **WebSocket Server**
   Routes messages by registration names: **`task_creator`**, **`task_validator`**, **`user`**.

---

**Enjoy exploring the multi-agent habit coaching workflow!**
