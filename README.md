# CommetAI

AI-powered project management system with GitHub integration.

Connect your repository, and every push automatically transforms into a clear picture of progress: the system verifies and deduplicates webhook events, retrieves change diffs, summarizes commits using an LLM, generates tasks, and closes completed ones.

**Live demo:** http://139.100.235.44:5173/  <!-- замените на домен с HTTPS -->

## How does this work

1. The user connects the repository via the GitHub App (OAuth).
2. GitHub sends a webhook for each push.
3. The backend verifies the event signature (HMAC SHA-256) and discards duplicates (deduplication by delivery ID via Redis).
4. For each commit, diffs are requested via the GitHub API.
5. The AI ​​service (OpenAI API, structured output) summarizes the changes.
6. Based on the summarization, new tasks are created and completed ones are closed.

## Tech stack

Python · FastAPI · SQLAlchemy (async) · Pydantic · PostgreSQL · Redis ·
OpenAI API GitHub API (App + OAuth + webhooks) Docker

## Key features

- **Webhooks Verification** - HMAC signature verification for each event,
  invalid requests are rejected before processing.
- **Deduplication** - GitHub can re-deliver an event; the delivery ID
  is stored in Redis, preventing duplicates from entering the pipeline.
- **Route → Service → Repository** - separation of request processing,
  business logic, and database operations. Each application (auth, board, ai) contains
  its own models, schemas, routes, and service.
- **Reusable AI Module** - LLM request logic is isolated
  in a separate application; only prompts (`prompts.py`) are specific.
- **Push processing is moved to a use case** (`process_push.py`) - orchestration
  of the entire pipeline in one place.

## Project structure

```
backend/
|-- config.py
|-- main.py
`-- src
    |-- ai          # LLM service: summarization, task generation
    |-- auth        # # JWT authentication, OAuth GitHub
    |-- board       # projects, tasks, webhooks processing
    `-- core        # database, middleware, exceptions
```

## Local Launch

The project uses a GitHub App (webhooks + OAuth), which requires a public
callback URL, so local launch is not supported.

The quickest way to see the project live is at: **[live demo](http://139.100.235.44:5173/)**.

## Планы развития

- [x] Deploy
- [ ] Group functionality
- [ ] Handling non-success pipeline events
