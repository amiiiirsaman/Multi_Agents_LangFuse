# Multi-Agent LangFuse System

A production-ready multi-agent system using CrewAI, Amazon Bedrock (Nova Pro), and LangFuse for observability. This system implements a researcher-reviewer workflow that gathers web evidence and produces well-sourced answers.

## Features

- 🤖 **Multi-Agent Architecture**: Researcher and Reviewer agents working sequentially
- 🔍 **Web Search Integration**: Serper API for real-time web search
- 👤 **Human-in-the-Loop**: Interactive user questioning capability
- 📊 **Full Observability**: LangFuse integration for complete tracing
- ☁️ **AWS Bedrock Integration**: Uses Amazon Nova Pro v1.0
- 🛡️ **Production Ready**: Error handling, logging, and configuration management

## Architecture

```
User Question
    ↓
Researcher Agent (asks clarifying questions + web search)
    ↓
Review Agent (synthesizes final answer with sources)
    ↓
Final Answer with Sources
```

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- Serper API key
- LangFuse account

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/amiiiirsaman/Multi_Agents_LangFuse.git
   cd Multi_Agents_LangFuse
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your actual API keys and credentials.

## Configuration

All configuration is centralized in `src/config.py`. Key settings:

- **API Keys**: Serper, LangFuse, AWS credentials
- **LLM Settings**: Model, temperature, max tokens
- **Trace Settings**: User ID, session ID, project name
- **Logging**: Log level and directory

See [.env.example](.env.example) for all available environment variables.

## Usage

### Basic Usage

```bash
cd src
python main.py
```

The system will:
1. Ask you clarifying questions about your query
2. Search the web using Serper
3. Produce a final answer with cited sources
4. Track everything in LangFuse

### Example Interaction

```
Starting CrewAI workflow...

[ENGINE QUESTION] What would you like to know?
[YOUR ANSWER] What are the latest developments in AI safety?

[Agent: Researcher] Searching the web...
[Agent: Reviewer] Synthesizing final answer...

=== Final Crew Result ===
{
  "final_answer": "Recent developments in AI safety include...",
  "sources": [
    {"type": "serper", "detail": "openai.com", "role": "Primary source"},
    {"type": "user", "detail": "User query", "role": "Question definition"}
  ]
}
```

## Project Structure

```
Multi_Agents_LangFuse/
├── src/
│   ├── main.py              # Entry point with LangFuse integration
│   ├── agents_and_tasks.py  # Agent and task definitions
│   ├── tools.py             # Tool implementations
│   ├── config.py            # Configuration management
│   └── requirements.txt     # Python dependencies
├── tests/
│   ├── test_tools.py        # Unit tests for tools
│   ├── test_agents.py       # Integration tests for agents
│   └── conftest.py          # Pytest configuration
├── logs/                    # Application logs (auto-created)
├── .env.example             # Example environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Components

### Agents

- **Researcher**: Gathers evidence using web search and user interaction
  - Tools: `ask_user`, `search_tool`
  - Output: JSON with user question, search query, results, and provisional answer

- **Reviewer**: Synthesizes final answer with proper source attribution
  - Tools: None (reasoning only)
  - Output: JSON with final answer and source list

### Tools

- **ask_user**: Interactive console-based user questioning
- **search_tool**: Serper API integration for web search

## Observability

All agent interactions are traced in LangFuse:

- **Traces**: One per workflow run
- **Spans**: Granular tracking of agent actions and tool calls
- **Metadata**: User ID, session ID, tags for filtering
- **Outputs**: Complete agent responses and results

Access your traces at your LangFuse dashboard.

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tools.py -v
```

## Logging

Logs are written to:
- Console: INFO level and above
- File: `logs/app.log` with rotation

Configure log level via `LOG_LEVEL` environment variable.

## Error Handling

The system includes comprehensive error handling:

- API call failures with retries
- Missing environment variables validation
- User input validation
- Graceful degradation for non-critical failures

## Development

### Adding a New Tool

1. Define the tool in `src/tools.py`
2. Add proper docstrings and type hints
3. Add unit tests in `tests/test_tools.py`
4. Register with the appropriate agent in `agents_and_tasks.py`

### Adding a New Agent

1. Define in `src/agents_and_tasks.py`
2. Assign appropriate tools
3. Create corresponding tasks
4. Add integration tests
5. Update crew configuration

## Troubleshooting

### Common Issues

**"Missing required environment variables"**
- Ensure all required variables in `.env` are set
- Check `.env.example` for reference

**"AWS credentials not found"**
- Verify AWS credentials in `.env`
- Ensure IAM permissions for Bedrock access

**"Serper API error"**
- Check API key validity
- Verify account quota

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Observability by [LangFuse](https://langfuse.com/)
- LLM powered by Amazon Bedrock Nova Pro
- Search powered by [Serper](https://serper.dev/)

## Support

For issues and questions:
- GitHub Issues: [Report a bug](https://github.com/amiiiirsaman/Multi_Agents_LangFuse/issues)
- Email: [Your contact info]

---

**Version**: 1.0.0  
**Last Updated**: January 2026
