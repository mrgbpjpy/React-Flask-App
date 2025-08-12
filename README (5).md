# React ↔ Flask Messages App

A minimal example of a **React** frontend communicating with a **Flask** backend using **CORS**.  
Supports:
- `GET /api/health` – API health check
- `GET /api/messages` – list messages
- `POST /api/messages` – create a new message

The frontend shows a status banner, a simple form, and a list of messages.

---

## Architecture

```
react-frontend/
  src/
    App.jsx        # Main React UI
    api.js         # API wrapper
flask-backend/
  app.py           # Flask API server with CORS enabled
```

> React falls back to `https://fxgsyc-5000.csb.app` if `REACT_APP_API_URL` is not set.

---

## Backend (Flask)

**Features:**
- CORS restricted to a specific origin (`FRONTEND_ORIGIN`)
- In-memory messages store (`MESSAGES`)
- Explicit `OPTIONS` route for CORS preflight
- `after_request` adds CORS headers to every response

**Routes:**
- `GET /api/health` → `{ "status": "ok", "service": "flask" }`
- `GET /api/messages` → returns a JSON list of messages
- `POST /api/messages` → accepts `{ "text": "..." }` and returns the created message

**Run locally:**
```bash
# Create virtual environment
python -m venv .venv
# Activate (Windows PowerShell)
. .venv/Scripts/Activate.ps1
# macOS/Linux
# source .venv/bin/activate

# Install dependencies
pip install Flask flask-cors

# Start server
python app.py
# Running at http://0.0.0.0:5000
```

**Example Requests:**
```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/messages
curl -X POST -H "Content-Type: application/json" \
     -d '{"text":"Hello from curl"}' \
     http://localhost:5000/api/messages
```

---

## Frontend (React)

**Highlights:**
- `useEffect` loads API health and messages on startup
- `useState` stores status, text input, and messages
- Sends POST requests to create messages
- Uses `REACT_APP_API_URL` if set, otherwise defaults to deployed API

**Run locally:**
```bash
npm install
# Set backend API URL
# Windows PowerShell:
setx REACT_APP_API_URL "http://localhost:5000"
# macOS/Linux:
# export REACT_APP_API_URL="http://localhost:5000"

# Start dev server
npm start
# or with Vite:
# npm run dev
```

---

## Environment Variables

**Frontend**
- `REACT_APP_API_URL` — URL of the backend API.

**Backend**
- `FRONTEND_ORIGIN` — Allowed CORS origin. In `app.py` it’s set to `"https://8gxv3h.csb.app"`.

---

## Troubleshooting

1. **CORS errors**  
   - Make sure `FRONTEND_ORIGIN` matches your frontend’s URL exactly.
2. **OPTIONS requests failing**  
   - Keep the explicit `OPTIONS` route for `/api/messages`.
3. **HTTPS mixed content**  
   - If frontend is HTTPS, backend must also be served over HTTPS.

---

## Security (Production)

- Use a real database instead of in-memory lists.
- Validate and sanitize all inputs.
- Restrict CORS to trusted domains only.
- Disable `debug=True` in production.
- Serve over HTTPS.

---

## Deployment

- **Backend**: Deploy with Gunicorn or another WSGI server, possibly behind Nginx.
- **Frontend**: Build and host static files (Vercel, Netlify, S3, etc.).
- Update `REACT_APP_API_URL` in frontend to point to deployed backend.

---

## Git Commands to Push

```bash
git init
git branch -M main
git remote add origin https://github.com/mrgbpjpy/C-WindowOS_Master_Template.git
git add .
git commit -m "Add React ↔ Flask Messages App"
git push -u origin main
```

If the remote already has history:
```bash
git pull --rebase --allow-unrelated-histories origin main
# resolve any conflicts
git push -u origin main
```

---

## License

MIT
