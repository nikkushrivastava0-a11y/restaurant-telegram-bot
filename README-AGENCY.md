# Noida Restaurant Web Studio — free preview

This repository branch `agency-preview-2026` is **isolated from `main`** and is used only to deploy an agency website preview on the free Render plan. Three original demo restaurant concepts are served at `/samples/modern/`, `/samples/bold/`, `/samples/minimal/`.

The website is not associated with real restaurants. All concept brands, copy and gallery illustrations are fictional.

## WhatsApp status

`SEND_ENABLED=false` disables ALL WhatsApp outbound messaging. Webhook requires signed official Meta requests and will reject unsigned posts. There is no lead import, mass sending, cold outreach, or follow-up scheduler. Enabling inbound replies requires an official Meta Cloud API account, verified token/app secret, phone ID, consent policy, human escalation and verified commercial hosting. This preview intentionally does not enable sending.

## Render

Use Python service, build: `pip install -r requirements.txt`, start: `uvicorn app:app --host 0.0.0.0 --port $PORT`. Plan: **free**. Env `SEND_ENABLED=false`. Region Singapore. The free instance sleeps after inactivity, so it is not suitable for always-on production WhatsApp webhooks.

## Run locally

`python -m pip install -r requirements.txt`

`uvicorn app:app --reload`

Open `/health`, `/`, `/samples/modern/`, `/samples/bold/`, `/samples/minimal/`. No API keys required for preview.

## Hosting and billing

Do not activate paid tiers or paid databases without explicit owner approval. No Google Places API key is configured. No actual lead outreach or sales have occurred.
