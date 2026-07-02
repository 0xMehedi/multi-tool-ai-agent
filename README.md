# Multi-Tool AI Agent for Bangladesh

An intelligent AI agent that answers questions about Bangladeshi institutions, hospitals, restaurants, and general knowledge using a combination of SQLite databases and web search.

## Architecture

```
User Input → LLM (Gemini) → Tool Selection → Database/Web Search → Response
                                    ↓
                          ┌─────────────────────┐
                          │   Available Tools     │
                          │  ┌─────────────────┐  │
                          │  │ Institutions DB  │  │
                          │  ├─────────────────┤  │
                          │  │  Hospitals DB   │  │
                          │  ├─────────────────┤  │
                          │  │ Restaurants DB  │  │
                          │  ├─────────────────┤  │
                          │  │  Web Search     │  │
                          │  └─────────────────┘  │
                          └─────────────────────┘
```

## Features

- **Natural Language to SQL**: Ask questions in plain English; the LLM generates appropriate SQL queries
- **Three Specialized Databases**: Institutions, Hospitals, and Restaurants in Bangladesh
- **Web Search Fallback**: Uses Tavily or DuckDuckGo for questions outside database scope
- **Interactive CLI**: Rich terminal interface with colored output
- **Automatic Setup**: Downloads, cleans, and converts datasets to SQLite on first run
- **Safety**: Blocks destructive SQL operations (DROP, DELETE, UPDATE, etc.)
- **Comprehensive Logging**: All queries, tool calls, and errors are logged

## Technologies

- Python 3.11+
- LangChain & LangGraph
- Google Gemini 2.0 Flash
- SQLAlchemy + SQLite
- Pandas
- Rich (CLI)
- Pydantic
- DuckDuckGo Search / Tavily

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multi-tool-ai-agent.git
cd multi-tool-ai-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional
```

Get a Google API key from [Google AI Studio](https://aistudio.google.com/).

### 5. Run the Application

```bash
python app.py
```

The application will automatically:
1. Check if databases exist
2. Download datasets from HuggingFace (if needed)
3. Inspect, clean, and convert CSV to SQLite
4. Start the interactive chat

## Manual Dataset Setup

If automatic download fails, manually download the CSV files:

1. Go to each dataset page on HuggingFace:
   - [Institutions](https://huggingface.co/datasets/Mahadih534/Institutional-Information-of-Bangladesh)
   - [Hospitals](https://huggingface.co/datasets/Mahadih534/all-bangladeshi-hospitals)
   - [Restaurants](https://huggingface.co/datasets/Mahadih534/Bangladeshi-Restaurant-Data)

2. Download the CSV files and place them in `data/csv/`:
   - `data/csv/institutions.csv`
   - `data/csv/hospitals.csv`
   - `data/csv/restaurants.csv`

3. Run the application again.

## Usage

### Interactive Chat

```bash
python app.py
```

Type your questions in natural language. The agent selects the appropriate tool automatically.

### Example Queries

| Category | Query |
|----------|-------|
| Institutions | How many government institutions are in Rajshahi? |
| Institutions | List universities in Dhaka. |
| Hospitals | List hospitals in Dhaka. |
| Hospitals | How many hospitals have ICU facilities? |
| Hospitals | Top hospitals in Chattogram. |
| Restaurants | Top restaurants in Sylhet. |
| Restaurants | Restaurants serving biryani in Dhaka. |
| Web Search | What is the healthcare policy of Bangladesh? |
| Web Search | Difference between public and private hospitals. |

### Commands

- `quit`, `exit`, `q` - Exit the application
- `help` - Show example queries

## Project Structure

```
multi-tool-ai-agent/
├── agent/
│   ├── prompt.py          # System prompt for the LLM
│   ├── create_agent.py    # LangGraph agent factory
│   ├── router.py          # State graph router
│   └── memory.py          # Conversation memory
├── config/
│   ├── settings.py        # Project settings & env vars
│   └── logging_config.py  # Logging configuration
├── data/
│   ├── csv/               # Raw & cleaned CSV files
│   └── db/                # SQLite database files
├── logs/
│   └── app.log            # Application logs
├── scripts/
│   ├── download_datasets.py  # HuggingFace dataset downloader
│   ├── inspect_dataset.py    # Dataset inspection & reporting
│   ├── clean_dataset.py      # Data cleaning pipeline
│   └── csv_to_sqlite.py      # CSV to SQLite converter
├── tools/
│   ├── sql_executor.py    # SQLite connection manager
│   ├── helper.py          # SQL validation & helpers
│   ├── database_tool_base.py  # Base database tool class
│   ├── institution_tool.py    # Institutions database tool
│   ├── hospital_tool.py       # Hospitals database tool
│   ├── restaurant_tool.py     # Restaurants database tool
│   └── web_search_tool.py     # Web search tool
├── tests/
│   ├── test_helper.py
│   ├── test_sql_executor.py
│   ├── test_tools.py
│   └── test_agent.py
├── app.py                 # Main CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google Gemini API key |
| `TAVILY_API_KEY` | No | Tavily Search API key (falls back to DuckDuckGo) |

## Known Limitations

- The quality of SQL generation depends on the LLM's understanding of the database schema
- Large datasets may take time to download and process on first run
- DuckDuckGo search may have rate limits for frequent queries
- The agent cannot modify database records (intentionally restricted)

## Future Improvements

- Add more database sources (population, economy, education statistics)
- Implement streaming responses
- Add a web API layer (FastAPI)
- Docker support
- More sophisticated SQL validation with AST parsing
- Support for multiple LLM providers (OpenAI, Anthropic, etc.)

## License

MIT License - see the [LICENSE](LICENSE) file for details.
