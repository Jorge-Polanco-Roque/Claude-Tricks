# Unit Testing Skill

A comprehensive Claude Code skill for running, analyzing, and setting up unit tests across multiple testing frameworks.

## Overview

This skill helps you:
- ✅ Run tests with any framework (Vitest, Jest, pytest, etc.)
- 📊 Analyze test results and generate coverage reports
- 🔍 Debug and fix failing tests
- 🚀 Set up testing frameworks from scratch
- 📝 Create test files from templates

## Installation

This skill is already installed in your project at:
```
.claude/skills/unit-testing/
```

## Usage

### Invoke with Slash Command

Simply type `/test` in Claude Code to activate the skill:

```
/test
```

### Auto-Invocation

The skill automatically activates when you mention testing-related tasks:
- "Run the tests"
- "Fix failing tests"
- "Set up testing for my project"
- "Generate coverage report"
- "Why are my tests failing?"

## Supported Frameworks

### JavaScript/TypeScript
- **Vitest** - Recommended for Vite projects
- **Jest** - Most popular testing framework
- **Mocha** + Chai
- **Jasmine**
- **Testing Library** (React, Vue, Svelte)
- **Cypress** - E2E testing
- **Playwright** - E2E testing

### Python
- **pytest** - Recommended
- **unittest** - Built-in
- **nose2**

### Other Languages
- **Go** - `go test`
- **Rust** - `cargo test`
- **Java** - JUnit, TestNG
- **C#** - NUnit, xUnit

## Features

### 1. Automatic Framework Detection

The skill detects your testing setup automatically:
```bash
# Checks package.json, requirements.txt, go.mod, etc.
# Identifies installed testing frameworks
# Uses appropriate commands for your setup
```

### 2. Smart Test Execution

Runs tests with the right options:
```bash
# For Vitest
vitest run              # One-time run
vitest                  # Watch mode
vitest --coverage       # With coverage

# For Jest
jest                    # Run all
jest --watch            # Watch mode
jest --coverage         # With coverage

# For pytest
pytest                  # Run all
pytest -v               # Verbose
pytest --cov            # With coverage
```

### 3. Result Analysis

Provides clear summaries:
```
📊 TEST SUMMARY
├─ Framework: Vitest
├─ Tests Run: 42
├─ Passed: 40 ✅
├─ Failed: 2 ❌
├─ Coverage: 87.3%
└─ Duration: 3.21s
```

### 4. Failure Debugging

Helps fix failing tests:
1. Identifies the failing test
2. Reads the test file
3. Reads the source code
4. Explains the issue
5. Proposes specific fixes
6. Verifies the fix works

### 5. Framework Setup

Configures testing from scratch:
1. Detects your project type
2. Recommends appropriate framework
3. Installs dependencies
4. Creates configuration files
5. Creates setup files
6. Generates example tests
7. Verifies setup works

## Directory Structure

```
.claude/skills/unit-testing/
├── SKILL.md                          # Main skill definition
├── README.md                         # This file
├── framework-reference.md            # Detailed framework docs
└── templates/
    ├── vitest-react-component.test.jsx
    ├── vitest-utility-function.test.js
    ├── jest-react-component.test.jsx
    └── pytest-example.py
```

## Example Workflows

### Example 1: Running Tests

**User:** "Run the tests"

**Skill will:**
1. Detect testing framework
2. Run `npm test` or equivalent
3. Parse output
4. Show summary with pass/fail counts

### Example 2: Fixing Failures

**User:** "Fix the failing tests"

**Skill will:**
1. Run tests to identify failures
2. Read each failing test file
3. Read the source code being tested
4. Analyze the root cause
5. Propose specific code changes
6. Re-run tests to verify fixes

### Example 3: Setting Up Testing

**User:** "I need to add tests to my React project"

**Skill will:**
1. Detect it's a Vite + React project
2. Recommend Vitest
3. Install: `vitest`, `@testing-library/react`, `jsdom`
4. Create `vitest.config.js`
5. Create test setup file
6. Create example component test
7. Run the example test to verify

### Example 4: Coverage Report

**User:** "Show me test coverage"

**Skill will:**
1. Run tests with coverage flag
2. Parse coverage table
3. Highlight files with low coverage (<80%)
4. Suggest which files need more tests

## Configuration

### Customizing Framework Detection Order

The skill checks for frameworks in this order:
1. Vitest (for Vite projects)
2. Jest
3. Mocha
4. pytest (for Python)
5. Go test (for Go)
6. Cargo test (for Rust)

### Customizing Coverage Thresholds

The skill uses these coverage targets:
- **80%+** overall coverage - Good baseline
- **100%** critical paths - Auth, payments, validation
- **60%+** UI components
- **90%+** business logic

## Templates

The skill includes ready-to-use templates:

### Vitest React Component Test
```javascript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MyComponent from './MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByRole('heading')).toBeInTheDocument()
  })
})
```

### Utility Function Test
```javascript
import { describe, it, expect } from 'vitest'
import { myFunction } from './utils'

describe('myFunction', () => {
  it('handles normal input', () => {
    expect(myFunction('test')).toBe('expected')
  })
})
```

### Python pytest Test
```python
import pytest

def test_my_function():
    result = my_function("input")
    assert result == "expected"
```

## Best Practices

The skill follows testing best practices:

1. **Test behavior, not implementation**
   - Tests what users see, not internal state
   - Uses accessible queries (getByRole, getByText)

2. **Keep tests isolated**
   - Each test runs independently
   - No shared state between tests

3. **Use descriptive test names**
   - Clear what's being tested
   - Easy to identify failures

4. **Handle async properly**
   - Uses `await` for async operations
   - Uses `findBy` queries for async elements

5. **Don't over-mock**
   - Only mock external dependencies
   - Test real behavior when possible

## Troubleshooting

### Tests Won't Run

**Check:**
- Dependencies installed: `npm install`
- Config file exists: `vitest.config.js` or `jest.config.js`
- Test files named correctly: `*.test.js` or `*.spec.js`

### Tests Failing Unexpectedly

**Try:**
- Run single test: `vitest MyComponent`
- Check test isolation: Tests may depend on each other
- Verify async handling: Add `await` where needed
- Clear cache: `rm -rf node_modules/.vite`

### Coverage Not Generating

**Check:**
- Coverage package installed: `@vitest/coverage-v8` or `jest coverage`
- Coverage configured in config file
- Run with coverage flag: `--coverage`

## Advanced Usage

### Run Specific Tests
```bash
vitest MyComponent           # Run by file name
jest -t "test name"          # Run by test name
pytest -k "keyword"          # Run by keyword
```

### Watch Mode
```bash
vitest                       # Auto-detects changes
jest --watch                 # Interactive watch
pytest --watch               # Requires pytest-watch
```

### Debug Mode
```bash
vitest --reporter=verbose    # Detailed output
jest --verbose               # Show all tests
pytest -vv                   # Very verbose
```

## Contributing

To improve this skill:

1. **Add new framework support**
   - Update `SKILL.md` with detection logic
   - Add to `framework-reference.md`
   - Create template in `templates/`

2. **Add new templates**
   - Create template file in `templates/`
   - Document in README

3. **Improve detection logic**
   - Update framework detection order
   - Add new file patterns

## Resources

- [Vitest Documentation](https://vitest.dev)
- [Jest Documentation](https://jestjs.io)
- [Testing Library](https://testing-library.com)
- [pytest Documentation](https://docs.pytest.org)

## License

This skill is part of your Claude Code setup and can be modified as needed.

---

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Author:** Created with Claude Code
