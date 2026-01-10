# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### Added
- Initial release of Multi-Agent LangFuse System
- Researcher and Reviewer agents with sequential workflow
- Serper API integration for web search
- Interactive user questioning with `ask_user` tool
- Full LangFuse observability with granular spans
- Amazon Bedrock Nova Pro v1.0 integration
- Centralized configuration management in `config.py`
- Comprehensive error handling and logging system
- Complete test suite with >80% coverage
- Production-ready project structure
- Detailed README with setup and usage instructions
- Environment variable validation
- Log rotation with file and console handlers

### Security
- Removed hardcoded API keys
- Added environment variable-based configuration
- Created .gitignore to prevent credential leakage

## [Unreleased]

### Planned
- Add support for additional LLM providers
- Implement retry logic for API calls
- Add async/parallel agent execution option
- Create web UI for workflow interaction
- Add support for custom tool development
- Implement agent memory and context persistence
- Add multi-language support
