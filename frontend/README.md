# Marketing Agency Frontend

Svelte-based UI for executing marketing skills.

## Quick Start

### Development

```bash
# Install dependencies
npm install

# Start dev server (with API proxy)
npm run dev
```

Open http://localhost:3000

### With Docker

```bash
# From repo root
docker-compose up
```

- Frontend: http://localhost:3000
- API: http://localhost:8080

## Features

- **Skill Selection**: Browse and select from 23 marketing skills organized by category
- **Example Presets**: Pre-built task templates for common use cases
- **Context Fields**: Add key-value pairs to provide additional context
- **Content Input**: Paste content for audits and analysis
- **Structured Results**: View output, alternatives, and recommendations
- **Copy to Clipboard**: One-click copy of results

## Project Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── api.ts      # API client and skill metadata
│   │   └── presets.ts  # Example task presets
│   ├── routes/
│   │   ├── +layout.svelte   # App layout
│   │   ├── +page.svelte     # Main execution page
│   │   └── skills/
│   │       └── +page.svelte # Skills listing
│   ├── app.css         # Global styles
│   └── app.html        # HTML template
├── static/             # Static assets
├── Dockerfile          # Production container
└── package.json
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `/api` (proxied) |
| `ORIGIN` | Allowed origin for CORS | `http://localhost:3000` |

## Building for Production

```bash
# Build
npm run build

# Preview production build
npm run preview
```

## Deployment

### Cloud Run

```bash
# Deploy frontend (requires API to be deployed first)
./deploy/deploy-frontend.sh
```

### Docker

```bash
docker build -t marketing-agency-frontend .
docker run -p 3000:3000 \
  -e VITE_API_URL=http://your-api-url \
  -e ORIGIN=http://your-frontend-url \
  marketing-agency-frontend
```

## Development Notes

### API Proxy

In development, requests to `/api/*` are proxied to `http://localhost:8080/*`. This is configured in `vite.config.ts`.

### Adding Presets

Add new example tasks in `src/lib/presets.ts`:

```typescript
{
  skill: 'skill-name',
  name: 'Preset Display Name',
  task: 'Task description...',
  context: {
    key: 'value'
  },
  content: 'Optional content to analyze'
}
```

### Styling

Global styles are in `src/app.css`. Component-specific styles use Svelte's scoped CSS.

CSS variables for theming:
- `--color-bg`: Background color
- `--color-text`: Text color
- `--color-accent`: Primary accent color
- `--color-border`: Border color
