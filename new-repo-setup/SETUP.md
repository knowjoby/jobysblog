# Setup Instructions

All files in this folder belong in `knowjoby/Ai-product-managers-blog`.

## Push to new repo (run once from your machine)

```bash
# Clone the new repo
git clone https://github.com/knowjoby/Ai-product-managers-blog.git
cd Ai-product-managers-blog

# Copy all files from this folder into the cloned repo
cp -r path/to/new-repo-setup/. .

# Commit and push
git add .
git commit -m "feat: initial Jekyll blog with AI PM roadmaps and daily post automation"
git push origin main
```

## Enable GitHub Pages (do this once on GitHub)

1. Go to repo **Settings → Pages**
2. Set **Source** to `GitHub Actions`
3. The `pages.yml` workflow will handle all future deploys on push to main

## How the daily post automation works

- **Workflow:** `.github/workflows/daily-post.yml` runs at 8 AM UTC every day
- **Model:** Microsoft Phi-3.5-mini-instruct via GitHub Models API (free, no API key needed)
- **Auth:** Uses the built-in `GITHUB_TOKEN` — no setup required
- **Topics:** Rotates through 30 pre-seeded topics in `data/topics_queue.json`, cycling beginner → advanced → expert
- **Post limit:** 1 post per day (enforced by date check in the script)
- **Word limit:** Under 500 words per post

## Trigger a post manually

Go to **Actions → Daily AI PM Post → Run workflow** to generate a post immediately.

## Add more topics

Edit `data/topics_queue.json` and add objects to the `topics` array:

```json
{"level": "beginner", "title": "Your Topic Here", "status": "pending"}
```

Levels: `beginner`, `advanced`, `expert`
