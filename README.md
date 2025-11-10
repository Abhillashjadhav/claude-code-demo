# Claude Multi-Agent Demo

A starter project demonstrating Claude's multi-agent workflow capabilities for collaborative software development.

## Overview

This project showcases how multiple specialized Claude agents work together to build software:
- **Planner** - Designs features and writes specifications
- **Implementer** - Writes code based on specifications
- **Tester** - Runs tests and reports issues
- **Doc-Writer** - Maintains documentation

## Project Structure

```
claude-code-demo/
├── .claude/
│   └── agents/          # Agent configuration files
│       ├── planner.md       # Plans features and requirements
│       ├── implementer.md   # Implements code changes
│       ├── tester.md        # Runs tests and reports issues
│       └── doc-writer.md    # Updates documentation
├── docs/
│   └── requirements.md  # Feature requirements and specifications
├── src/                 # Source code (empty - ready for your project!)
├── tests/              # Test files (empty - ready for your tests!)
├── CHANGELOG.md        # Project changelog
├── Requirements.txt    # Python dependencies
└── README.md          # This file
```

## The Multi-Agent Workflow

### How It Works

1. **Planning Phase**
   - You request a feature
   - The **Planner** agent analyzes requirements
   - Specifications are written to `docs/requirements.md`

2. **Implementation Phase**
   - The **Implementer** agent reads the specifications
   - Code is written in `src/` and tests in `tests/`
   - Changes are focused and minimal

3. **Testing Phase**
   - The **Tester** agent runs the test suite
   - Reports failures with clear diagnostics
   - Suggests fixes if needed

4. **Documentation Phase**
   - The **Doc-Writer** agent updates documentation
   - `CHANGELOG.md` is maintained
   - Ensures docs match actual implementation

### Agent Roles

**Planner Agent** (`tools: Read, Write, Grep, Glob`)
- Reads existing code and docs
- Writes feature specifications
- Defines test cases and edge cases
- Does NOT modify source code

**Implementer Agent** (`tools: Read, Edit, Write, Grep, Glob, Bash`)
- Implements features from specs
- Makes focused code changes
- Runs tests after changes
- Does NOT modify requirements

**Tester Agent** (`tools: Read, Bash, Grep, Glob`)
- Runs test suite
- Reports failures clearly
- Suggests minimal fixes
- Does NOT edit files

**Doc-Writer Agent** (`tools: Read, Write, Grep, Glob`)
- Updates documentation
- Maintains changelog
- Ensures accuracy
- Does NOT change code

## Getting Started

This is an empty project template. Here's how to use it:

### 1. Define Your Project

Update `Requirements.txt` with your dependencies:
```bash
# Example for a web API:
flask
pytest
requests
```

### 2. Request Your First Feature

Simply describe what you want to build:
- "Create a REST API with user authentication"
- "Build a CLI tool for file processing"
- "Implement a data pipeline with validation"

### 3. Watch the Agents Work

The multi-agent system will:
1. Plan the feature
2. Implement the code
3. Write and run tests
4. Update documentation

### 4. Iterate and Expand

Continue adding features by describing what you need. The agents will maintain consistency and quality throughout.

## Example Workflow

```
You: "Create a simple calculator API with add and subtract endpoints"

Planner: Updates docs/requirements.md with specifications
Implementer: Creates src/calculator.py and tests/test_calculator.py
Tester: Runs pytest and reports results
Doc-Writer: Updates CHANGELOG.md with new features
```

## Why Multi-Agent?

- **Separation of Concerns:** Each agent has a specific role
- **Quality Assurance:** Built-in testing and documentation
- **Maintainability:** Clear specs and updated docs
- **Consistency:** Structured workflow for all features

## Ready to Start?

This project is now ready for your first feature request. Just describe what you'd like to build!

## License

MIT License - See LICENSE file for details
