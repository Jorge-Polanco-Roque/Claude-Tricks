# Security Review Checklist

## Critical Security Issues

### 1. XSS (Cross-Site Scripting)

```javascript
// 🚨 CRITICAL - XSS vulnerability
function UserComment({ comment }) {
  return <div dangerouslySetInnerHTML={{ __html: comment }} />
}

// ✅ SAFE - Escape user input
function UserComment({ comment }) {
  return <div>{comment}</div> // React escapes by default
}

// ✅ SAFE - Sanitize if HTML is needed
import DOMPurify from 'dompurify'

function UserComment({ comment }) {
  const sanitized = DOMPurify.sanitize(comment)
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />
}
```

### 2. Hardcoded Secrets

```javascript
// 🚨 CRITICAL - Exposed API key
const API_KEY = 'sk_live_12345abcdef'
fetch(`https://api.example.com/data?key=${API_KEY}`)

// ✅ SAFE - Use environment variables
const API_KEY = process.env.REACT_APP_API_KEY
fetch(`https://api.example.com/data?key=${API_KEY}`)

// ⚠️ WARNING: Client-side code is ALWAYS visible
// For sensitive keys, use a backend proxy
```

### 3. SQL Injection (Backend)

```javascript
// 🚨 CRITICAL - SQL injection
app.get('/user', (req, res) => {
  const query = `SELECT * FROM users WHERE id = ${req.query.id}`
  db.query(query) // NEVER DO THIS!
})

// ✅ SAFE - Parameterized query
app.get('/user', (req, res) => {
  const query = 'SELECT * FROM users WHERE id = ?'
  db.query(query, [req.query.id])
})
```

### 4. Authentication Issues

```javascript
// 🚨 CRITICAL - No authentication
app.post('/api/delete-user', (req, res) => {
  deleteUser(req.body.userId)
  res.json({ success: true })
})

// ✅ SAFE - Verify authentication
app.post('/api/delete-user', authenticateUser, (req, res) => {
  if (req.user.id !== req.body.userId && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Unauthorized' })
  }
  deleteUser(req.body.userId)
  res.json({ success: true })
})
```

### 5. CORS Misconfiguration

```javascript
// 🚨 CRITICAL - Allows any origin
app.use(cors({
  origin: '*',
  credentials: true // DANGEROUS with wildcard origin!
}))

// ✅ SAFE - Specific origins
app.use(cors({
  origin: ['https://yourapp.com', 'https://www.yourapp.com'],
  credentials: true
}))
```

### 6. Insecure Password Storage

```javascript
// 🚨 CRITICAL - Plain text passwords
const user = {
  email: 'user@example.com',
  password: req.body.password // NEVER store plain text!
}

// ✅ SAFE - Hash passwords
const bcrypt = require('bcrypt')
const hashedPassword = await bcrypt.hash(req.body.password, 10)
const user = {
  email: 'user@example.com',
  password: hashedPassword
}
```

### 7. JWT Token Issues

```javascript
// 🚨 CRITICAL - Weak secret
const token = jwt.sign({ userId: 1 }, 'secret')

// 🚨 CRITICAL - No expiration
const token = jwt.sign({ userId: 1 }, process.env.JWT_SECRET)

// ✅ SAFE - Strong secret + expiration
const token = jwt.sign(
  { userId: 1 },
  process.env.JWT_SECRET, // Use strong random secret
  { expiresIn: '1h' }
)
```

### 8. Open Redirects

```javascript
// 🚨 CRITICAL - Open redirect
app.get('/redirect', (req, res) => {
  res.redirect(req.query.url) // Can redirect anywhere!
})

// ✅ SAFE - Whitelist allowed URLs
const ALLOWED_REDIRECTS = ['/dashboard', '/profile', '/settings']

app.get('/redirect', (req, res) => {
  const url = req.query.url
  if (ALLOWED_REDIRECTS.includes(url)) {
    res.redirect(url)
  } else {
    res.status(400).json({ error: 'Invalid redirect' })
  }
})
```

### 9. Missing Input Validation

```javascript
// 🚨 CRITICAL - No validation
app.post('/api/create-user', (req, res) => {
  const user = createUser(req.body) // Accepts any data!
})

// ✅ SAFE - Validate all inputs
const { z } = require('zod')

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().min(18).max(120)
})

app.post('/api/create-user', (req, res) => {
  try {
    const validatedData = userSchema.parse(req.body)
    const user = createUser(validatedData)
    res.json(user)
  } catch (error) {
    res.status(400).json({ error: error.errors })
  }
})
```

### 10. File Upload Vulnerabilities

```javascript
// 🚨 CRITICAL - No validation
app.post('/upload', upload.single('file'), (req, res) => {
  // Accepts any file type!
  res.json({ filename: req.file.filename })
})

// ✅ SAFE - Validate file type and size
const multer = require('multer')

const upload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB max
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'image/gif']
    if (!allowed.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'))
    }
    cb(null, true)
  }
})
```

## Medium Priority Security Issues

### 1. Rate Limiting Missing

```javascript
// ⚠️ WARNING - No rate limiting
app.post('/api/login', (req, res) => {
  // Vulnerable to brute force attacks
})

// ✅ BETTER - Add rate limiting
const rateLimit = require('express-rate-limit')

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts'
})

app.post('/api/login', loginLimiter, (req, res) => {
  // Protected from brute force
})
```

### 2. Missing HTTPS

```javascript
// ⚠️ WARNING - HTTP only
app.listen(3000)

// ✅ BETTER - Force HTTPS in production
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    if (req.header('x-forwarded-proto') !== 'https') {
      return res.redirect(`https://${req.header('host')}${req.url}`)
    }
    next()
  })
}
```

### 3. Sensitive Data in Logs

```javascript
// ⚠️ WARNING - Logging sensitive data
console.log('User login:', req.body) // Contains password!

// ✅ BETTER - Redact sensitive fields
const { password, ...safeData } = req.body
console.log('User login:', safeData)
```

### 4. Missing Security Headers

```javascript
// ⚠️ WARNING - No security headers
app.use(express.json())

// ✅ BETTER - Use helmet
const helmet = require('helmet')

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:']
    }
  }
}))
```

## Frontend Security Checklist

- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] No hardcoded secrets or API keys
- [ ] Environment variables prefixed correctly (REACT_APP_, VITE_, etc.)
- [ ] External links use `rel="noopener noreferrer"`
- [ ] No `eval()` or `Function()` with user input
- [ ] Local storage doesn't contain sensitive data
- [ ] Cookies use `httpOnly` and `secure` flags
- [ ] Form validation on both client and server
- [ ] No sensitive data in URL parameters
- [ ] Dependencies regularly updated (npm audit)

## Backend Security Checklist

- [ ] All inputs validated and sanitized
- [ ] SQL queries use parameterization
- [ ] Passwords hashed with bcrypt/argon2
- [ ] JWT tokens have expiration
- [ ] Authentication required on protected routes
- [ ] Authorization checks for user actions
- [ ] CORS configured properly
- [ ] Rate limiting on sensitive endpoints
- [ ] HTTPS enforced in production
- [ ] Security headers configured (helmet)
- [ ] Error messages don't leak sensitive info
- [ ] File uploads validated (type, size)
- [ ] Database connections use environment variables
- [ ] Sessions stored securely (Redis, not memory)
- [ ] Logs don't contain passwords/tokens

## Common Vulnerability Patterns

### ReDoS (Regular Expression Denial of Service)

```javascript
// 🚨 CRITICAL - Vulnerable to ReDoS
const regex = /^(a+)+$/
userInput.match(regex) // Can hang with 'aaaaaaaaaaaaaaaaX'

// ✅ SAFE - Use simple, non-backtracking regex
const regex = /^a+$/
```

### Prototype Pollution

```javascript
// 🚨 CRITICAL - Prototype pollution
function merge(target, source) {
  for (let key in source) {
    target[key] = source[key]
  }
}

// Attacker can do: {"__proto__": {"isAdmin": true}}

// ✅ SAFE - Check for prototype keys
function merge(target, source) {
  for (let key in source) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      continue
    }
    target[key] = source[key]
  }
}
```

## Tools for Security Review

- **npm audit** - Check for vulnerable dependencies
- **Snyk** - Automated security scanning
- **OWASP ZAP** - Web app security scanner
- **SonarQube** - Code quality and security
- **Lighthouse** - Includes security checks
- **SecurityHeaders.com** - Check HTTP headers

## Emergency Response

If you find a **CRITICAL** security issue:

1. **🚨 STOP** - Don't merge the code
2. **📢 ALERT** - Notify the team immediately
3. **🔒 FIX** - Provide exact fix in review
4. **✅ VERIFY** - Ensure fix is implemented
5. **📝 DOCUMENT** - Add to security checklist

Remember: Security bugs are not a reflection of the developer's skill. They're learning opportunities for the entire team.
