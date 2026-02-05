# Project Status Check

You are a project status reporter. Provide a comprehensive overview of the Bella Italia project.

## Your Task

Provide a detailed status report including:

1. **Git Status**
   - Current branch
   - Changed files
   - Uncommitted changes
   - Latest commit info

2. **Development Server**
   - Check if server is running (`lsof -i :4000`)
   - Show server URL if running
   - Suggest starting if not running

3. **Dependencies**
   - Run `npm outdated` to check for updates
   - Show current versions of main dependencies (React, Vite, React Router)

4. **Project Structure**
   - List main directories and file counts
   - Confirm all critical files exist (vite.config.js, package.json, etc.)

5. **Recent Activity**
   - Show last 3 git commits
   - Identify what was worked on recently

## Output Format

Provide a clean, organized report with emojis for readability:

```
📊 BELLA ITALIA - PROJECT STATUS

🌿 Git Status
├─ Branch: main
├─ Changed: 3 files
└─ Last Commit: abc1234 - "feat: update documentation"

🚀 Development Server
├─ Status: ✅ Running
└─ URL: http://localhost:4000

📦 Dependencies
├─ React: 19.2.0 ✅
├─ Vite: 7.3.1 ✅
└─ React Router: 7.13.0 ✅

📁 Project Structure
├─ Components: 1 file
├─ Pages: 3 files
├─ Assets: 5 images
└─ Status: ✅ Complete

📝 Recent Activity
└─ Last 3 commits shown below...
```
