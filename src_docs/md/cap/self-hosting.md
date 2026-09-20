# Self-hosting Vexy Screensese Web

*How to deploy Vexy Screensese Web on your own infrastructure*

Vexy Screensese Web is the web application for uploading and sharing recordings — the same codebase, as an AGPL fork, that powers Cap.so.
You can upload videos to it from the dashboard or from Vexy Screensese Desktop.

## Quick Start (One Command)

The fastest way to self-host Vexy Screensese is with Docker Compose. This single command will start everything you need:

```bash
git clone -b modified https://github.com/vexyart/vexy-screensese-cap.git
cd vexy-screensese-cap
docker compose up -d
```

That's it! Vexy Screensese will be available at `http://localhost:3000`.

> **Security Notice for Production Deployments**
>
> The default `docker-compose.yml` includes placeholder secrets for quick local testing. **If you're deploying to a public server or production environment**, you must change these values. See the [Production Checklist](#production-checklist) below.

Login links will appear in the logs since email isn't configured:
```bash
docker compose logs cap-web
```

## Deployment Options

### Option 1: Docker Compose (Recommended)

Best for VPS, home servers, or any Docker-capable host.

**What's included:**
- Vexy Screensese Web application
- Media server (FFmpeg processing)
- MySQL database
- MinIO (S3-compatible storage)

**Steps:**
1. Clone the repository
2. Run `docker compose up -d`
3. Access Vexy Screensese at `http://localhost:3000`

> **Note:** The main `docker-compose.yml` builds the media server from source, so a full clone of the repository is required. The Coolify compose file uses a pre-built image from `ghcr.io` instead.

**Custom configuration:**

Create a `.env` file to customize your deployment:

```bash
# Public URL (required for production)
CAP_URL=https://cap.yourdomain.com

# S3 public URL (for video playback)
S3_PUBLIC_URL=https://s3.yourdomain.com

# Optional: Custom ports
CAP_PORT=3000
MINIO_PORT=9000

# Optional: Custom passwords (auto-generated if not set)
MYSQL_PASSWORD=your-secure-password
MINIO_ROOT_PASSWORD=your-minio-password
```

### Option 2: Coolify

For Coolify users, use `docker-compose.coolify.yml` which includes environment variable placeholders:

1. Create a new Docker Compose project in Coolify
2. Point to the Vexy Screensese repository
3. Set compose file to `docker-compose.coolify.yml`
4. Configure environment variables in Coolify's UI
5. Deploy

> **Note:** The Coolify compose file uses slightly different environment variable names: `WEB_URL` instead of `CAP_URL`, and `S3_PUBLIC_ENDPOINT` instead of `S3_PUBLIC_URL`.

## Connecting Vexy Screensese

1. Open Vexy Screensese settings
2. Set 'Vexy Screensese Server URL' to your deployment URL (e.g., `https://cap.yourdomain.com`)
3. Uploads will now go to your self-hosted instance

## Email Configuration

By default, login links are printed to the server logs. To send emails:

1. Create an account at [Resend](https://resend.com)
2. Add these environment variables:
   ```bash
   RESEND_API_KEY=re_xxxxx
   RESEND_FROM_DOMAIN=yourdomain.com
   ```

## Optional Features

### AI Features

For video transcription and AI features (titles, summaries, chapters,
transcript translation, and docs Ask AI):

```bash
ASSEMBLY_API_KEY=your-key    # Transcription
GROQ_API_KEY=your-key        # AI features
OPENAI_API_KEY=your-key      # AI features
ANTHROPIC_API_KEY=your-key   # AI features
```

When `AI_PROVIDER` is not set, AI providers are auto-detected from whichever
keys are present. Generation features (titles, summaries, chapters,
translation) prefer Groq → OpenAI → Anthropic; chat features (the support
messenger and docs Ask AI) prefer Anthropic → OpenAI → Groq. Earlier
providers are preferred; later ones are automatic fallbacks.

To pick a provider explicitly, set `AI_PROVIDER` to one of `assemblyai`,
`openai`, `anthropic`, `groq`, or `openai-compatible`. Any other configured
providers stay in the chain as fallbacks.

```bash
AI_PROVIDER=assemblyai
```

`assemblyai` reuses your existing `ASSEMBLY_API_KEY` via the AssemblyAI LLM
Gateway, so one key covers transcription and AI features. It is never
auto-detected: transcription-only instances don't start incurring LLM charges
unless you opt in, and opting in bills LLM tokens to the same AssemblyAI
account as transcription.

`openai-compatible` works with any OpenAI-compatible endpoint such as Ollama,
OpenRouter, or LM Studio. It requires `AI_BASE_URL` and `AI_MODEL` (and
`AI_API_KEY` if your endpoint needs one):

```bash
AI_PROVIDER=openai-compatible
AI_BASE_URL=http://localhost:11434/v1
AI_MODEL=llama3.3
AI_API_KEY=your-key          # If the endpoint requires one
```

Each provider has sensible default models. You can override them per role for
the provider selected by `AI_PROVIDER`:

```bash
AI_MODEL=your-model          # Generation: titles, summaries, chapters, translation
AI_CHAT_MODEL=your-model     # Support chat
AI_STREAM_MODEL=your-model   # Streaming docs Ask AI
```

For the AssemblyAI EU gateway, set
`AI_BASE_URL=https://llm-gateway.eu.assemblyai.com/v1`. The EU gateway only
serves Claude and Gemini models, so you must also override `AI_MODEL` and
`AI_STREAM_MODEL` (the defaults are OpenAI-family models that are US-only).

### Google OAuth

```bash
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
```

### Apple OAuth

Create a Sign in with Apple Services ID, register
`https://your-domain.example/api/auth/callback/apple` as its return URL, and
generate a client-secret JWT:

```bash
APPLE_CLIENT_ID=your-services-id
APPLE_CLIENT_SECRET=your-client-secret-jwt
```

Apple client-secret JWTs expire, so rotate the secret before its configured
expiration date.

## Production Checklist

> **Critical: Change Default Secrets Before Going Public**
>
> The default `docker-compose.yml` contains **hardcoded placeholder secrets** that are visible in the public repository. Anyone who knows you're using Vexy Screensese with defaults could potentially:
>
> - **Forge authentication sessions** (via `NEXTAUTH_SECRET`)
> - **Decrypt sensitive database fields** (via `DATABASE_ENCRYPTION_KEY`)
> - **Spoof webhook requests** (via `MEDIA_SERVER_WEBHOOK_SECRET`)
>
> This is fine for local development or testing on a private network, but **you must generate unique secrets before exposing Vexy Screensese to the internet**.

**Generate secure secrets:**
```bash
openssl rand -hex 32
```

Run this command three times to generate values for:
- `NEXTAUTH_SECRET`
- `DATABASE_ENCRYPTION_KEY`
- `MEDIA_SERVER_WEBHOOK_SECRET`

**Full production checklist:**

- [ ] Set secure passwords: `MYSQL_PASSWORD`, `MINIO_ROOT_PASSWORD`
- [ ] Set secure secrets: `DATABASE_ENCRYPTION_KEY`, `NEXTAUTH_SECRET`, `MEDIA_SERVER_WEBHOOK_SECRET`
- [ ] Set `CAP_URL` to your public URL
- [ ] Set `S3_PUBLIC_URL` to your MinIO/S3 public URL
- [ ] Configure a reverse proxy (nginx, Caddy, Traefik) with SSL
- [ ] Set up email with Resend
- [ ] Configure backups for MySQL and MinIO volumes

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Cap Desktop   │────▶│    Cap Web      │
└─────────────────┘     │   (port 3000)   │
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
             ┌──────────┐ ┌──────────┐ ┌──────────┐
             │  MySQL   │ │  MinIO   │ │  Media   │
             │ (3306)   │ │ (9000)   │ │  Server  │
             └──────────┘ └──────────┘ └──────────┘
```

## Environment Variables Reference

See [`packages/env/server.ts`](https://github.com/CapSoftware/Cap/blob/main/packages/env/server.ts) for all available options.

## Troubleshooting

**Can't access Vexy Screensese after starting:**
```bash
docker compose logs cap-web
```

**Database migration issues:**
```bash
docker compose down -v  # Warning: deletes data
docker compose up -d
```

**Reset everything:**
```bash
docker compose down -v
docker compose up -d
```

## Support

If you encounter issues with self-hosting:
- [Open a GitHub issue](https://github.com/vexyart/vexy-screensese/issues/new)
- Check existing issues for solutions

We do not offer direct support for self-hosted deployments.
