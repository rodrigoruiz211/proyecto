# Deploy Flutter web (frontend/ver) to GitHub Pages

This project includes two deployment options for the Flutter web frontend located in `frontend/ver`.

1) Automatic (recommended): GitHub Actions
----------------------------------------
- A workflow is provided at `.github/workflows/deploy_frontend.yml`.
- It triggers on pushes to `main` / `master` and on manual dispatch.
- It installs Flutter, runs `flutter pub get`, builds `flutter build web --release`, and publishes `frontend/ver/build/web` to the `gh-pages` branch using `peaceiris/actions-gh-pages`.
- To enable, push this repository to GitHub (default branch `main`) and the workflow will run automatically. The action uses `${{ secrets.GITHUB_TOKEN }}` so no extra token is required.

2) Manual (local) deployment script
----------------------------------
- A helper script `frontend/ver/deploy.sh` builds the web app and publishes the `build/web` output to branch `gh-pages` using `git worktree`.
- Usage (from repository root):

  cd frontend/ver
  ./deploy.sh

- Requirements:
  - `git` configured and remote `origin` pointing to your GitHub repo.
  - `flutter` installed locally and in PATH.

Notes and tips
--------------
- GitHub Pages will serve the content from the `gh-pages` branch. The workflow/script both push to that branch.
- If you prefer using Netlify or Vercel, you can instead upload the folder `frontend/ver/build/web` there.
- If your repo uses a different default branch (e.g. `master`), the workflow also listens to `master` pushes.

Troubleshooting
---------------
- If the GH Action fails because Flutter isn't found, ensure the action `subosito/flutter-action@v2` is up-to-date or pin a specific version.
- If the manual script fails due to `git worktree add` errors, make sure the `gh-pages` branch isn't already checked out elsewhere locally.

