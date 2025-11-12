#!/usr/bin/env bash
set -euo pipefail

# Script to build Flutter web and publish to gh-pages using git worktree.
# Run from project root or from within frontend/ver. Example:
#   cd frontend/ver && ./deploy.sh

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "Installing dependencies..."
flutter pub get

echo "Building Flutter web..."
flutter build web --release

BRANCH=gh-pages
BUILD_DIR=build/web

if [ ! -d "$BUILD_DIR" ]; then
  echo "Build directory $BUILD_DIR not found. Build failed?"
  exit 1
fi

# Ensure we're inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository. Publish manually or initialize git."
  exit 1
fi

TMP_DIR=$(mktemp -d)

echo "Using temporary worktree: $TMP_DIR"

git fetch origin

# create branch if doesn't exist
if ! git show-ref --verify --quiet refs/heads/$BRANCH; then
  echo "Branch $BRANCH does not exist locally. Creating an orphan branch..."
  git checkout --orphan $BRANCH
  git rm -rf . >/dev/null 2>&1 || true
  git clean -fdx
  git commit --allow-empty -m "Create $BRANCH branch"
  git push origin $BRANCH
  git checkout -
fi

# Add worktree (if branch already checked out elsewhere this may fail)
git worktree add --detach "$TMP_DIR" $BRANCH

# Copy built files
rm -rf "$TMP_DIR"/*
cp -r "$BUILD_DIR"/* "$TMP_DIR"/

cd "$TMP_DIR"

git add --all
if git commit -m "Publish Flutter web build"; then
  echo "Pushing to origin/$BRANCH..."
  git push origin $BRANCH
else
  echo "No changes to publish."
fi

# Clean up
cd "$ROOT_DIR"
git worktree remove "$TMP_DIR" || true
rm -rf "$TMP_DIR"

echo "Done. Frontend published to branch $BRANCH."
