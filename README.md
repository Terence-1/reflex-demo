# reflex-demo

A test page built with  [Reflex](https://reflex.dev).

## Setup & Run

```bash
# 1. Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Sync dependencies
uv sync

# 3. Set database URL
export DB_URL="postgresql://..."

# 4. Run the app
uv run reflex run
```

Open `http://localhost:3000` in your browser.
