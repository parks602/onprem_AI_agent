# onprem_AI_agent — LangChain-Based CS Auto-Response Agent

**[🇰🇷 한국어 README](./README.md)**

> **Automating game customer support with on-premises LLM + Function Calling**
> Production Project at Gravity Co. | Python · LangChain · Ollama · FastAPI · MSSQL · ClickHouse

---

## Overview

`onprem_AI_agent` is an on-premises AI agent that automates game customer support inquiries using LangChain and Function Calling — without any external API dependency.

### The Problem It Solved

Game operations staff had to request data from the DB team every time a user submitted an inquiry, creating a **1–2 day bottleneck** for even simple lookup requests (e.g., "Did this user receive their item?").

The root cause wasn't the lack of automation — it was that operations staff had no direct access to game data. This agent eliminates that gap.

### Results

| Metric | Before | After |
|--------|--------|-------|
| Response time | 1–2 days | Under 10 minutes |
| Simple inquiry automation | 0% | **85%** |

---

## System Architecture

```
User Inquiry (text)
        ↓
[Inquiry Classifier]
  → Categorize into: Payment / Account / Item / Event / Security
        ↓
[get_category_tools(category)]
  → Auto-select Function Calling tools for the category
        ↓
[Function Calling Executor]
  → Query MSSQL / ClickHouse directly with parameterized queries
        ↓
[Response Generator]
  → Generate draft response + expose retrieved data to operator
  → Return "Data retrieval failed" if no results found
```

---

## Tool Categories

The agent automatically selects tools based on inquiry category via `get_category_tools()`:

### Payment Tools (`PAYMENT_TOOLS`)
| Tool | Description |
|------|-------------|
| `user_payment_history` | Full payment history for a user |
| `user_payment_history_by_date` | Payment history within a date range |
| `user_refund_history` | Refund history for a user |

### Account Tools (`ACCOUNT_TOOLS`)
| Tool | Description |
|------|-------------|
| `get_account_info` | Character list and recent login records |
| `get_character_info` | Character details |
| `get_character_item_usage` | Character item usage logs |

### Item Tools (`ITEM_TOOLS`)
| Tool | Description |
|------|-------------|
| `get_item_log` | Item acquisition logs |
| `get_use_item_log` | Item usage logs |

### Event Tools (`EVENT_TOOLS`)
| Tool | Description |
|------|-------------|
| `get_event_item_usage` | Event item usage history |

### Security Tools (`SECURITY_TOOLS`)
| Tool | Description |
|------|-------------|
| `get_login_log` | Login history for a user |

### Auto Tool Registration

```python
def get_category_tools(category):
    tools = {
        "결제": PAYMENT_TOOLS,    # Payment
        "계정": ACCOUNT_TOOLS,    # Account
        "아이템": ITEM_TOOLS,     # Item
        "이벤트": EVENT_TOOLS,    # Event
        "보안": SECURITY_TOOLS,   # Security
        "기타": OTHER_TOOLS,      # Other
    }
    return tools[category]
```

---

## Security Design

### Dual SQL Injection Defense

LLM-generated parameters could introduce SQL injection risk. Two layers of defense are applied:

**Layer 1 — Parameterized Queries**
```python
# ❌ Dangerous: direct string interpolation
query = f"SELECT * FROM users WHERE user_id = {user_id}"

# ✅ Safe: parameterized query
query = "SELECT * FROM users WHERE user_id = ?"
cursor.execute(query, (user_id,))
```

**Layer 2 — Pydantic Type Validation**
```python
class PaymentHistoryInput(BaseModel):
    user_id: int           # Must be integer — string injection blocked
    start_date: datetime   # Must be valid datetime format
    end_date: datetime
```

All parameters are strictly typed before reaching the database. Invalid types are rejected before query execution.

### Hallucination Prevention

- Retrieved data is **always exposed alongside the draft response** — operators can verify the source data directly
- When DB query returns no results: explicitly returns **"Data retrieval failed"** instead of allowing LLM to fabricate an answer
- Query timeout: auto-terminates queries running longer than 3 minutes

---

## Key Technical Details

### Game-Specific Entity Recognition

Game user inquiries frequently use abbreviated item names and community slang (e.g., "불검" instead of "전설의 불꽃 검"). To handle this:

1. Built a **synonym dictionary** mapping slang/abbreviations to official item names
2. Constructed an **ontology** so unrecognized terms are treated as potential item name candidates
3. When an unknown term appears → retrieve top-10 similar items by cosine similarity → join with user's actual history → return only items the user actually owns

This approach significantly improved query success rate for ambiguous user inputs.

### ClickHouse Integration

ClickHouse was introduced to handle large-scale game log queries that conflicted with MSSQL batch jobs:

- Conducted PoC with benchmark query comparisons
- Presented performance results to management → received server approval
- Migrated high-volume log queries to ClickHouse, resolving MSSQL contention

---

## Project Structure

```
onprem_AI_agent/
├── core/
│   ├── classifier.py        # Inquiry category classification
│   └── tools/
│       ├── payment_tools.py
│       ├── account_tools.py
│       ├── item_tools.py
│       ├── event_tools.py
│       └── security_tools.py
├── db/
│   ├── mssql_client.py      # MSSQL connection (parameterized queries)
│   └── clickhouse_client.py # ClickHouse connection
├── llm/
│   └── client.py            # Ollama LLM abstraction layer
├── routers/
│   └── inquiry.py           # FastAPI router
├── app.py                   # FastAPI application entry point
├── main.py                  # CLI runner
└── requirements.txt
```

---

## Installation & Usage

### 1. Clone Repository

```bash
git clone https://github.com/parks602/onprem_AI_agent.git
cd onprem_AI_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# .env
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=phi4:latest

MSSQL_HOST=your_host
MSSQL_USER=your_user
MSSQL_PASSWORD=your_password
MSSQL_DATABASE=your_db

CLICKHOUSE_HOST=your_host
CLICKHOUSE_PORT=8123
```

### 4. Run

```bash
# FastAPI server
uvicorn app:app --reload --port 8000

# CLI test
python main.py
```

---

## Tech Stack

| Area | Technology |
|------|-----------|
| Agent Framework | LangChain |
| LLM Serving | Ollama (phi-4, on-premises) |
| API | FastAPI (async) |
| Game DB | MSSQL |
| Log Analytics | ClickHouse |
| Validation | Pydantic |
| Language | Python 3.11 |

---

## On-Premises Design Rationale

All LLM inference runs locally via Ollama — no external API calls. This was a hard requirement:

- Game user data cannot leave the internal network
- Cloud LLM APIs (OpenAI, Anthropic) are not permitted under the company's security policy
- GGUF-quantized models run stably on limited GPU hardware

---

*Production AI system built at Gravity Co. — independently designed, implemented, and operated*
