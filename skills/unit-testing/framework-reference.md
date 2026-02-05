# Testing Framework Reference Guide

## Vitest (Recommended for Vite Projects)

### Why Vitest?
- Lightning fast with Vite's transformation pipeline
- Jest-compatible API (easy migration)
- ESM, TypeScript, JSX support out of the box
- Built-in coverage with c8
- Component testing support

### Installation
```bash
npm install -D vitest @vitest/ui
npm install -D @testing-library/react @testing-library/jest-dom jsdom
```

### Configuration (vitest.config.js)
```javascript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/']
    }
  },
})
```

### Setup File (src/test/setup.js)
```javascript
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

afterEach(() => {
  cleanup()
})
```

### Example Test
```javascript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App Component', () => {
  it('renders welcome message', () => {
    render(<App />)
    expect(screen.getByText(/welcome/i)).toBeInTheDocument()
  })
})
```

### Common Commands
```bash
vitest                    # Run in watch mode
vitest run                # Run once
vitest --ui               # Open UI
vitest --coverage         # Generate coverage
vitest --reporter=verbose # Detailed output
vitest MyComponent        # Run specific test
```

---

## Jest

### Why Jest?
- Most popular JavaScript testing framework
- Zero config for most projects
- Powerful mocking capabilities
- Snapshot testing
- Great documentation and community

### Installation
```bash
npm install -D jest @testing-library/react @testing-library/jest-dom
npm install -D @types/jest  # For TypeScript
npm install -D babel-jest @babel/preset-env @babel/preset-react
```

### Configuration (jest.config.js)
```javascript
export default {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.js'],
  moduleNameMapper: {
    '\\.(css|less|scss)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
  ],
}
```

### Common Commands
```bash
jest                      # Run all tests
jest --watch              # Watch mode
jest --coverage           # Coverage report
jest --verbose            # Detailed output
jest MyComponent          # Run specific test
```

---

## pytest (Python)

### Why pytest?
- Simple, Pythonic syntax
- Powerful fixtures
- Excellent plugin ecosystem
- Clear assertion messages
- Parallel test execution

### Installation
```bash
pip install pytest pytest-cov pytest-mock
```

### Configuration (pytest.ini)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

### Example Test
```python
import pytest
from myapp import calculate_total

def test_calculate_total():
    result = calculate_total([1, 2, 3])
    assert result == 6

def test_calculate_total_empty():
    result = calculate_total([])
    assert result == 0

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_data):
    assert len(sample_data) == 5
```

### Common Commands
```bash
pytest                    # Run all tests
pytest -v                 # Verbose
pytest --cov=.            # Coverage
pytest -k "test_name"     # Run specific test
pytest --maxfail=1        # Stop after first failure
pytest -x                 # Stop on first failure
```

---

## React Testing Library Patterns

### Querying Elements
```javascript
// Preferred queries (accessible)
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText(/email/i)
screen.getByText(/welcome/i)

// Alternative queries
screen.getByTestId('custom-element')
screen.getByPlaceholderText(/search/i)

// Query variants
getBy...    // Throws error if not found
queryBy...  // Returns null if not found
findBy...   // Returns Promise (for async)
```

### User Interactions
```javascript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

it('handles button click', async () => {
  const user = userEvent.setup()
  render(<MyComponent />)

  const button = screen.getByRole('button')
  await user.click(button)

  expect(screen.getByText(/clicked/i)).toBeInTheDocument()
})
```

### Async Testing
```javascript
it('loads data', async () => {
  render(<DataComponent />)

  // Wait for element to appear
  const heading = await screen.findByRole('heading', { name: /data/i })
  expect(heading).toBeInTheDocument()

  // Wait for element to disappear
  await waitForElementToBeRemoved(() => screen.queryByText(/loading/i))
})
```

---

## Coverage Targets

### Industry Standards
- **80%+ overall coverage**: Good baseline
- **100% critical paths**: Authentication, payments, data validation
- **60%+ UI components**: Hard to test everything
- **90%+ business logic**: Core functionality

### What to Prioritize
1. **Critical business logic** (highest priority)
2. **Security-sensitive code** (auth, permissions)
3. **Data transformations** (parsers, formatters)
4. **Error handling** (edge cases)
5. **User interactions** (forms, buttons)

### What to Skip
- Third-party libraries (already tested)
- Configuration files
- Type definitions
- Simple getters/setters

---

## Test Organization

### File Naming Conventions
```
src/
├── components/
│   ├── Button.jsx
│   └── Button.test.jsx         # Co-located
├── utils/
│   ├── formatDate.js
│   └── formatDate.spec.js      # Alternative naming
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

### Test Structure (AAA Pattern)
```javascript
describe('Component/Function Name', () => {
  it('should do something specific', () => {
    // Arrange - Set up test data
    const input = 'test'

    // Act - Execute the behavior
    const result = myFunction(input)

    // Assert - Verify the outcome
    expect(result).toBe('expected')
  })
})
```

---

## Common Testing Anti-Patterns

### ❌ Don't Test Implementation Details
```javascript
// Bad - testing internal state
expect(component.state.count).toBe(5)

// Good - testing behavior
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### ❌ Don't Use Too Many Mocks
```javascript
// Bad - over-mocking makes tests brittle
jest.mock('./everything')

// Good - only mock external dependencies
jest.mock('axios')
```

### ❌ Don't Write Flaky Tests
```javascript
// Bad - timing-dependent
setTimeout(() => expect(x).toBe(y), 100)

// Good - wait for conditions
await waitFor(() => expect(x).toBe(y))
```

---

## Debugging Failed Tests

### Step-by-Step Process
1. **Read error message carefully** - Often tells you exactly what's wrong
2. **Check line numbers** - Find where test failed
3. **Add debug output** - `screen.debug()` or `console.log()`
4. **Check test isolation** - Run single test alone
5. **Verify test data** - Ensure setup is correct
6. **Check async handling** - Use `await` properly
7. **Review recent changes** - What changed since tests passed?

### Useful Debug Commands
```javascript
// React Testing Library
screen.debug()                    // Print entire DOM
screen.debug(element)             // Print specific element
screen.logTestingPlaygroundURL()  // Get interactive query builder

// Vitest/Jest
console.log(result)               // Debug values
expect.objectContaining({...})    // Partial matching
expect.any(Type)                  // Type checking
```

---

## Quick Reference Commands

### Vitest
| Command | Description |
|---------|-------------|
| `vitest` | Run in watch mode |
| `vitest run` | Run once and exit |
| `vitest --ui` | Open web UI |
| `vitest --coverage` | Generate coverage |
| `vitest MyComponent` | Run specific test |

### Jest
| Command | Description |
|---------|-------------|
| `jest` | Run all tests |
| `jest --watch` | Watch mode |
| `jest --coverage` | Generate coverage |
| `jest -t "test name"` | Run by pattern |
| `jest --verbose` | Detailed output |

### pytest
| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest --cov` | Coverage report |
| `pytest -k "name"` | Run by keyword |
| `pytest -x` | Stop on first fail |
