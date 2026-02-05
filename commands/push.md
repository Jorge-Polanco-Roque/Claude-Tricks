# Push to Remote Repository

You are a Git automation assistant. Your task is to commit all changes and push them to the remote repository.

## Remote Repository
- URL: https://github.com/Jorge-Polanco-Roque/Italian_Restaurant_Site.git
- Branch: main

## Your Task

Follow these steps in order:

1. **Check Git Status**
   - Run `git status` to see what files have changed
   - Show the user a summary of changes

2. **Review Changes**
   - Run `git diff` to show what has changed (if reasonable size)
   - Identify the type of changes (new features, bug fixes, updates, etc.)

3. **Stage All Changes**
   - Run `git add .` to stage all changes
   - Confirm what files were staged

4. **Create Commit Message**
   - Analyze the changes and create a descriptive commit message
   - Format: `<type>: <description>`
   - Types: feat, fix, docs, style, refactor, test, chore
   - Example: `feat: add dark mode toggle to navbar`
   - Include the co-authored line:
   ```
   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

5. **Commit Changes**
   - Run the git commit with the message
   - Use heredoc format for multi-line messages

6. **Push to Remote**
   - Run `git push origin main`
   - Confirm successful push

7. **Summary**
   - Show the commit SHA
   - Show the remote URL
   - Confirm that changes are now in GitHub

## Important Notes

- NEVER commit sensitive files (.env, credentials, API keys)
- Check .gitignore is properly configured
- If there are no changes, inform the user
- If push fails, explain the error and suggest solutions
- Always show the user what will be committed before committing

## Example Output

After completion, provide a summary like:

```
✅ Changes pushed successfully to GitHub!

📝 Commit: abc1234 - "feat: update CLAUDE.md with port configuration"
🌐 Remote: https://github.com/Jorge-Polanco-Roque/Italian_Restaurant_Site.git
🔗 View on GitHub: https://github.com/Jorge-Polanco-Roque/Italian_Restaurant_Site/commit/abc1234
```
