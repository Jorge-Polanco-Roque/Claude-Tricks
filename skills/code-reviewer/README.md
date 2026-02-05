# Code Reviewer Skill

An expert code review agent that analyzes your code for bugs, security vulnerabilities, performance issues, accessibility problems, and best practices.

## Overview

This skill provides comprehensive, constructive code reviews focusing on:
- 🐛 **Correctness** - Bugs, logic errors, edge cases
- 🔒 **Security** - Vulnerabilities, XSS, injection attacks
- ⚡ **Performance** - Inefficiencies, memory leaks, optimizations
- ♿ **Accessibility** - WCAG compliance, keyboard navigation
- 📐 **Best Practices** - Code patterns, maintainability
- 🧪 **Testing** - Coverage, test quality

## Installation

The skill is located at:
```
.claude/skills/code-reviewer/
```

It will be automatically detected by Claude Code.

## Usage

### Invoke with Slash Command

```
/review
```

### Auto-Invocation

The skill automatically activates when you mention:
- "Review my code"
- "Check this component"
- "Is this code secure?"
- "Any bugs in this file?"
- "Review my changes"

### Specific File Review

```
/review src/components/Navbar.jsx
```

### Review Recent Changes

```
"Review my latest changes"
"Check what I just committed"
```

## Features

### 1. Multi-Category Analysis

The reviewer checks:
- **Bugs & Correctness** - Logic errors, null checks, edge cases
- **Security** - XSS, SQL injection, hardcoded secrets
- **Performance** - Re-renders, memory leaks, inefficient code
- **Accessibility** - Alt text, keyboard nav, ARIA labels
- **Best Practices** - DRY, SOLID, proper patterns
- **Testing** - Test coverage and quality

### 2. Severity-Based Prioritization

Issues are categorized by severity:

🚨 **Critical** - Must fix before merge
- Security vulnerabilities
- Data loss bugs
- Crashes/errors

⚠️ **High** - Should fix soon
- Performance problems
- Memory leaks
- Missing error handling

💡 **Medium** - Nice to have
- Code style issues
- Minor optimizations
- Better naming

ℹ️ **Low** - Optional
- Documentation
- Refactoring opportunities

### 3. Code Examples Provided

Every issue includes:
- ❌ **Current problematic code**
- ✅ **Suggested fix**
- 💡 **Explanation of why**

### 4. Positive Feedback

Not just criticism! The reviewer highlights:
- Well-written code
- Good patterns used
- Clever solutions

### 5. Framework-Specific Expertise

Special knowledge for:
- **React** - Hooks, performance, patterns
- **Node.js/Express** - Security, async handling
- **CSS** - Accessibility, responsive design
- **TypeScript** - Type safety

## Review Output Format

```markdown
# Code Review: [File/Feature Name]

## 📊 Summary
- Overall Quality: Good
- Files Reviewed: 3
- Issues Found: 5 (Critical: 0, High: 2, Medium: 2, Low: 1)

## ✅ Strengths
- Clean component structure
- Good prop validation with TypeScript
- Proper error handling

## 🚨 Critical Issues
[None found]

## ⚠️ High Priority Issues
### Issue 1: Missing useEffect Cleanup
**Location**: `Navbar.jsx:25`
**Problem**: Event listener not cleaned up
[Code example with fix]

## 💡 Suggestions
### Suggestion 1: Memoize Expensive Calculation
[Code example]

## 🎯 Next Steps
1. [ ] Fix event listener cleanup
2. [ ] Add error boundary
3. [ ] Consider memoization
```

## Specialized Reviews

### React Component Review

Checks for:
- ✅ Props validated (PropTypes/TypeScript)
- ✅ Proper hook dependencies
- ✅ No memory leaks
- ✅ Accessibility
- ✅ Performance optimizations
- ✅ Error boundaries
- ✅ Test coverage

### API/Backend Review

Checks for:
- ✅ Input validation
- ✅ Authentication/authorization
- ✅ SQL injection prevention
- ✅ Proper error handling
- ✅ Rate limiting
- ✅ Security headers

### CSS/Style Review

Checks for:
- ✅ Responsive design
- ✅ Color contrast (WCAG)
- ✅ No hardcoded values
- ✅ CSS variables
- ✅ prefers-reduced-motion

## Reference Documentation

The skill includes detailed references:

### [react-patterns.md](react-patterns.md)
- Common React anti-patterns
- Performance optimization patterns
- Accessibility guidelines
- Testing best practices

### [security-checklist.md](security-checklist.md)
- XSS prevention
- SQL injection prevention
- Authentication/authorization
- Secure file uploads
- Common vulnerabilities

## Example Reviews

### Example 1: Simple Component Review

**User:** "Review my Button component"

**Reviewer:**
```markdown
# Code Review: Button Component

## 📊 Summary
Overall Quality: Good
Issues Found: 2 (Medium: 1, Low: 1)

## ✅ Strengths
- Clean, simple implementation
- Good prop types

## 💡 Suggestions
### Missing Accessibility
Add aria-label for icon-only buttons
[Shows code fix]
```

### Example 2: Security Review

**User:** "Is this login form secure?"

**Reviewer:**
```markdown
# Code Review: Login Form

## 🚨 Critical Issues
### Issue 1: Password Stored in Plain Text
**Severity**: Critical
**Location**: `api/auth.js:15`
[Shows hashing solution]

### Issue 2: No Rate Limiting
**Severity**: Critical
**Location**: `routes/login.js:8`
[Shows rate limit implementation]
```

## Best Practices

The reviewer follows these principles:

1. **Be Constructive** - Explain WHY, not just WHAT
2. **Be Specific** - Point to exact lines with examples
3. **Be Educational** - Share resources and learning
4. **Be Balanced** - Highlight good code too
5. **Be Practical** - Consider effort vs benefit
6. **Be Kind** - Remember the human behind the code

## Review Checklist

Before completing a review, the agent verifies:

- [ ] All relevant files reviewed
- [ ] Security vulnerabilities checked
- [ ] Accessibility verified
- [ ] Performance analyzed
- [ ] Specific examples provided
- [ ] Issues prioritized clearly
- [ ] Positive feedback included
- [ ] Actionable next steps given
- [ ] Respectful language used

## When to Use

### ✅ Use This Skill When:
- You've written new code and want feedback
- Before creating a pull request
- After implementing a feature
- When debugging mysterious issues
- Learning best practices
- Improving code quality

### ❌ Don't Use For:
- Automated style formatting (use Prettier/ESLint)
- Simple syntax errors (IDE will catch these)
- Generating new code (use main Claude)

## Configuration

The skill runs in a **fork context**, meaning it:
- Runs independently without cluttering main conversation
- Can perform deep analysis
- Returns comprehensive report

## Tips for Best Results

1. **Be Specific**: "Review the authentication logic in `auth.js`"
2. **Provide Context**: "This is a public-facing login form"
3. **Ask Questions**: "Is this secure?" or "Will this perform well?"
4. **Review Small Chunks**: 400 lines or less per review

## Common Issues Caught

### React Projects
- Missing useEffect dependencies
- Memory leaks from event listeners
- Performance issues (unnecessary re-renders)
- Accessibility violations
- Missing error boundaries

### Security
- XSS vulnerabilities
- Hardcoded API keys
- SQL injection risks
- Missing authentication
- Insecure file uploads

### Performance
- Large bundle sizes
- Unoptimized images
- Inefficient algorithms
- Memory leaks

## Learning Resources

The reviewer may reference:
- [React Docs](https://react.dev)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web.dev](https://web.dev)
- [MDN Web Docs](https://developer.mozilla.org)

## Troubleshooting

**Issue**: Review is too generic

**Solution**: Be more specific about what to review
```
❌ "Review my code"
✅ "Review Navbar.jsx for accessibility issues"
```

**Issue**: Review takes too long

**Solution**: Review smaller chunks of code
```
❌ Review entire codebase (1000+ files)
✅ Review recent changes (3-5 files)
```

## Contributing

To improve this skill:

1. **Add new patterns** to `react-patterns.md`
2. **Update security checklist** in `security-checklist.md`
3. **Enhance SKILL.md** with new review categories
4. **Share feedback** on what reviews are most helpful

## Version History

**v1.0.0** - Initial release
- React component reviews
- Security analysis
- Performance checks
- Accessibility validation
- Best practices review

---

**Remember**: The goal of code review is to help developers improve, not to find fault. Every suggestion is an opportunity to learn and grow as a developer.

🚀 **Happy Reviewing!**
