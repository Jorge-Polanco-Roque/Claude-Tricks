# React Code Review Patterns

## Common React Anti-Patterns

### 1. Missing Dependencies in useEffect

```javascript
// ❌ Bad
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, []) // Missing userId dependency!

  return <div>{user?.name}</div>
}

// ✅ Good
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId]) // Correctly includes userId

  return <div>{user?.name}</div>
}
```

### 2. State Updates After Unmount

```javascript
// ❌ Bad - Memory leak
function DataFetcher() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetchData().then(result => {
      setData(result) // Component might be unmounted!
    })
  }, [])

  return <div>{data}</div>
}

// ✅ Good - Cleanup prevents memory leak
function DataFetcher() {
  const [data, setData] = useState(null)

  useEffect(() => {
    let isMounted = true

    fetchData().then(result => {
      if (isMounted) {
        setData(result)
      }
    })

    return () => {
      isMounted = false
    }
  }, [])

  return <div>{data}</div>
}
```

### 3. Inline Function Props (Performance)

```javascript
// ❌ Bad - Creates new function every render
function TodoList({ items }) {
  return items.map(item => (
    <TodoItem
      key={item.id}
      onDelete={() => deleteItem(item.id)} // New function every render!
    />
  ))
}

// ✅ Good - Memoized callback
function TodoList({ items }) {
  const handleDelete = useCallback((id) => {
    deleteItem(id)
  }, [])

  return items.map(item => (
    <TodoItem
      key={item.id}
      onDelete={() => handleDelete(item.id)}
    />
  ))
}

// ✅ Even Better - Pass stable reference
function TodoList({ items }) {
  const handleDelete = useCallback((id) => {
    deleteItem(id)
  }, [])

  return items.map(item => (
    <TodoItem
      key={item.id}
      item={item}
      onDelete={handleDelete}
    />
  ))
}
```

### 4. Missing Keys in Lists

```javascript
// ❌ Bad - Using index as key
{items.map((item, index) => (
  <div key={index}>{item.name}</div>
))}

// ❌ Bad - No key at all
{items.map(item => (
  <div>{item.name}</div>
))}

// ✅ Good - Stable unique key
{items.map(item => (
  <div key={item.id}>{item.name}</div>
))}
```

### 5. Prop Drilling

```javascript
// ❌ Bad - Props passed through many levels
function App() {
  const [user, setUser] = useState(null)
  return <Layout user={user} setUser={setUser} />
}

function Layout({ user, setUser }) {
  return <Sidebar user={user} setUser={setUser} />
}

function Sidebar({ user, setUser }) {
  return <UserMenu user={user} setUser={setUser} />
}

// ✅ Good - Use Context
const UserContext = createContext()

function App() {
  const [user, setUser] = useState(null)
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout />
    </UserContext.Provider>
  )
}

function UserMenu() {
  const { user, setUser } = useContext(UserContext)
  return <div>{user?.name}</div>
}
```

### 6. Unnecessary State

```javascript
// ❌ Bad - Derived state stored separately
function Cart({ items }) {
  const [total, setTotal] = useState(0)

  useEffect(() => {
    setTotal(items.reduce((sum, item) => sum + item.price, 0))
  }, [items])

  return <div>Total: ${total}</div>
}

// ✅ Good - Calculate during render
function Cart({ items }) {
  const total = items.reduce((sum, item) => sum + item.price, 0)

  return <div>Total: ${total}</div>
}

// ✅ Even Better - Memoize if expensive
function Cart({ items }) {
  const total = useMemo(
    () => items.reduce((sum, item) => sum + item.price, 0),
    [items]
  )

  return <div>Total: ${total}</div>
}
```

### 7. Non-Accessible Components

```javascript
// ❌ Bad - Not keyboard accessible
function Modal({ onClose, children }) {
  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content">
        {children}
        <span onClick={onClose}>×</span>
      </div>
    </div>
  )
}

// ✅ Good - Fully accessible
function Modal({ onClose, children, title }) {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [onClose])

  return (
    <div
      className="modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="modal-content">
        <h2 id="modal-title">{title}</h2>
        {children}
        <button
          onClick={onClose}
          aria-label="Close modal"
        >
          ×
        </button>
      </div>
    </div>
  )
}
```

### 8. Missing Error Boundaries

```javascript
// ❌ Bad - No error handling
function App() {
  return (
    <div>
      <Header />
      <MainContent />
      <Footer />
    </div>
  )
}

// ✅ Good - Error boundary protects app
class ErrorBoundary extends React.Component {
  state = { hasError: false }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>
    }
    return this.props.children
  }
}

function App() {
  return (
    <ErrorBoundary>
      <div>
        <Header />
        <MainContent />
        <Footer />
      </div>
    </ErrorBoundary>
  )
}
```

### 9. Direct DOM Manipulation

```javascript
// ❌ Bad - Bypassing React
function Component() {
  const handleClick = () => {
    document.getElementById('message').innerHTML = 'Clicked!'
  }

  return (
    <div>
      <button onClick={handleClick}>Click</button>
      <div id="message"></div>
    </div>
  )
}

// ✅ Good - React way
function Component() {
  const [message, setMessage] = useState('')

  const handleClick = () => {
    setMessage('Clicked!')
  }

  return (
    <div>
      <button onClick={handleClick}>Click</button>
      <div>{message}</div>
    </div>
  )
}
```

### 10. Massive Components

```javascript
// ❌ Bad - Component does too much
function ProductPage() {
  // 500 lines of code...
  return (
    <div>
      {/* Complex header logic */}
      {/* Product details logic */}
      {/* Reviews logic */}
      {/* Related products logic */}
      {/* Footer logic */}
    </div>
  )
}

// ✅ Good - Extracted into smaller components
function ProductPage() {
  return (
    <div>
      <ProductHeader />
      <ProductDetails />
      <ProductReviews />
      <RelatedProducts />
      <ProductFooter />
    </div>
  )
}
```

## React Performance Patterns

### useMemo for Expensive Calculations

```javascript
// ✅ Good
function ProductList({ products, filters }) {
  const filteredProducts = useMemo(() => {
    return products.filter(p =>
      p.category === filters.category &&
      p.price >= filters.minPrice &&
      p.price <= filters.maxPrice
    )
  }, [products, filters])

  return filteredProducts.map(p => <Product key={p.id} {...p} />)
}
```

### React.memo for Preventing Re-renders

```javascript
// ✅ Good
const ExpensiveComponent = React.memo(({ data }) => {
  // Complex rendering logic
  return <div>{data}</div>
})

// Only re-renders if data actually changes
```

### Code Splitting with React.lazy

```javascript
// ✅ Good
const HeavyComponent = React.lazy(() => import('./HeavyComponent'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  )
}
```

## Accessibility Checklist for React

- [ ] All images have meaningful alt text
- [ ] Forms have labels associated with inputs
- [ ] Buttons have accessible names
- [ ] Interactive elements are keyboard accessible
- [ ] Focus is managed properly (modals, menus)
- [ ] ARIA attributes used when needed
- [ ] Color is not the only way to convey information
- [ ] Text has sufficient contrast (4.5:1)
- [ ] Animations respect prefers-reduced-motion

## Testing React Components

```javascript
// ✅ Good test - Tests behavior
describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com')
    await userEvent.type(screen.getByLabelText(/password/i), 'password123')
    await userEvent.click(screen.getByRole('button', { name: /login/i }))

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    })
  })
})
```
