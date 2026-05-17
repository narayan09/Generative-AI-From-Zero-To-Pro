#!/bin/bash

set -e

FEATURE_BRANCH="$1"
BASE_BRANCH="main"

if [ -z "$FEATURE_BRANCH" ]; then
  echo "❌ Please provide feature branch name"
  echo "Usage: ./automate_git_flow.sh feature-branch"
  exit 1
fi

echo "🚀 Starting workflow for branch: $FEATURE_BRANCH"

# Verify git repository
if [ ! -d ".git" ]; then
  echo "❌ Not inside a git repository"
  exit 1
fi

# Check unresolved merge conflicts
if git diff --name-only --diff-filter=U | grep .; then
  echo "❌ Resolve merge conflicts first"
  exit 1
fi

# Auto save current changes BEFORE branch switch
CURRENT_BRANCH=$(git branch --show-current)

if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Saving local changes on $CURRENT_BRANCH..."

  git add .

  git commit -m "Auto save before sync: $(date '+%Y-%m-%d %H:%M:%S')" || true
fi

# Fetch latest remote
echo "📥 Fetching latest changes..."
git fetch origin

# Update main branch
echo "🔄 Updating main branch..."
git checkout "$BASE_BRANCH"

git pull origin "$BASE_BRANCH"

# Create or switch feature branch
if git show-ref --verify --quiet refs/heads/"$FEATURE_BRANCH"; then
  echo "✅ Switching to existing feature branch..."
  git checkout "$FEATURE_BRANCH"
else
  echo "🆕 Creating new feature branch..."
  git checkout -b "$FEATURE_BRANCH"
fi

# Merge latest main
echo "🔀 Syncing feature branch with main..."

if ! git merge "$BASE_BRANCH"; then
  echo ""
  echo "❌ Merge conflict detected"
  echo "Resolve conflicts manually"
  exit 1
fi

# Add latest changes
if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Adding latest changes..."

  git add .

  echo "💾 Creating commit..."

  git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')" || true
else
  echo "✅ No new changes"
fi

# Push feature branch
echo "🚀 Pushing feature branch..."

git push -u origin "$FEATURE_BRANCH"

echo ""
echo "✅ Feature branch synced successfully!"
echo ""
echo "🌐 Create Pull Request:"
echo "https://github.com/narayan09/Generative-AI-From-Zero-To-Pro/pulls"
echo ""
echo "🗑️ Delete branch after merge:"
echo "git branch -D $FEATURE_BRANCH"
echo "git push origin --delete $FEATURE_BRANCH"
echo ""