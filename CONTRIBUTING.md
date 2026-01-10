# Contributing to Multi-Agent LangFuse System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Multi_Agents_LangFuse.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up your development environment (see below)

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r src/requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

## Code Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for all modules, classes, and functions

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When validation fails
    """
```

### Code Organization

- One class or major function per file when appropriate
- Group related functionality in modules
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tools.py -v
```

### Writing Tests

- Write tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Use fixtures from `conftest.py` for common test data
- Mock external API calls

Example:
```python
def test_ask_user_valid_input():
    """Test ask_user with valid user input."""
    with patch('builtins.input', return_value='Paris'):
        result = ask_user("What is the capital of France?")
        assert result == 'Paris'
```

## Making Changes

### Adding a New Tool

1. Define the tool in `src/tools.py`
2. Add comprehensive docstrings
3. Add error handling and logging
4. Write unit tests in `tests/test_tools.py`
5. Update README if user-facing

### Adding a New Agent

1. Define in `src/agents_and_tasks.py`
2. Assign appropriate tools and LLM config
3. Create corresponding tasks
4. Write integration tests in `tests/test_agents.py`
5. Update documentation

### Modifying Configuration

1. Update `src/config.py` with new variables
2. Add to `.env.example` with example values
3. Update README configuration section
4. Write tests for new config validation

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(tools): add new data extraction tool

Add a tool for extracting structured data from web pages
using BeautifulSoup. Includes error handling and tests.

Closes #123
```

## Pull Request Process

1. **Before submitting**:
   - Ensure all tests pass
   - Update documentation
   - Add tests for new features
   - Follow code style guidelines
   - Update CHANGELOG.md if applicable

2. **Submitting**:
   - Create a pull request against the `main` branch
   - Fill out the PR template completely
   - Link related issues
   - Request review from maintainers

3. **After review**:
   - Address all review comments
   - Keep the PR up to date with main branch
   - Squash commits if requested

## Issue Guidelines

### Reporting Bugs

Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

### Requesting Features

Include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if applicable)
- Any alternatives considered

## Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Error handling implemented
- [ ] Logging added for important operations
- [ ] Type hints included
- [ ] Docstrings complete and accurate

## Questions?

Feel free to open an issue for:
- Questions about contributing
- Clarification on guidelines
- Discussion of major changes

Thank you for contributing! 🎉
