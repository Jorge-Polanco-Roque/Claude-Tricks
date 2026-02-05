# Start Development Server

You are a development server manager for the Bella Italia project.

## Your Task

Start the development server safely and provide useful information.

## Steps

1. **Check for Running Servers**
   - Check if port 4000 is already in use: `lsof -i :4000`
   - If occupied, ask user if they want to kill it

2. **Navigate to Project**
   - Change to bella-italia directory
   - Verify package.json exists

3. **Clean Start (Optional)**
   - Ask if user wants to clear Vite cache first
   - If yes: `rm -rf node_modules/.vite`

4. **Start Server**
   - Run `npm run dev` in background
   - Wait 3 seconds for server to start

5. **Verify Server Started**
   - Check that port 4000 is now listening
   - Show server output

6. **Provide Information**
   - Display: Server URL (http://localhost:4000)
   - Show: How to stop the server
   - Remind: To open browser

## Output Format

```
🚀 Starting Bella Italia Development Server...

✅ Port 4000 is available
📁 Project directory: /bella-italia
🧹 Cache cleared

▶️  Server starting...

  VITE v7.3.1  ready in XXX ms

  ➜  Local:   http://localhost:4000/
  ➜  Network: use --host to expose

🌐 Open in browser: http://localhost:4000

💡 To stop: Press Ctrl+C or run `pkill -9 node`
```

## Important

- Always start server in bella-italia directory
- Never start multiple servers on same port
- Confirm server is actually running before reporting success
