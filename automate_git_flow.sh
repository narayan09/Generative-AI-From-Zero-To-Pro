#!/bin/bash

set -e

FEATURE_BRANCH="$1"
MAIN_BRANCH="main"
DEV_BRANCH="develop"

if [ -z "$FEATURE_BRANCH" ]; then
  echo "❌ Please provide feature branch name"
  echo "Usage: ./automate_git_flow.sh feature-branch"
  exit 1
fi

echo ""
echo "🚀 Starting workflow for branch: $FEATURE_BRANCH"
echo ""

# Verify git repo
if [ ! -d ".git" ]; then
  echo "❌ Not inside git repository"
  exit 1
fi

# Check unresolved conflicts
if git diff --name-only --diff-filter=U | grep .; then
  echo "❌ Resolve merge conflicts first"
  exit 1
fi

# Save current changes
CURRENT_BRANCH=$(git branch --show-current)

if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Saving local changes..."

  git add .

  git commit -m "Auto save: $(date '+%Y-%m-%d %H:%M:%S')" || true
else
  echo "✅ No local changes"
fi

# Fetch latest
echo ""
echo "📥 Fetching latest remote changes..."
git fetch origin

# Update main
echo ""
echo "🔄 Updating main branch..."
git checkout "$MAIN_BRANCH"

git pull origin "$MAIN_BRANCH"

# Create or switch feature branch
echo ""
echo "🌿 Preparing feature branch..."

if git show-ref --verify --quiet refs/heads/"$FEATURE_BRANCH"; then
  git checkout "$FEATURE_BRANCH"
else
  git checkout -b "$FEATURE_BRANCH"
fi

# Sync with latest main
echo ""
echo "🔀 Merging latest main into feature branch..."

git merge "$MAIN_BRANCH" || {
  echo "❌ Merge conflict detected"
  exit 1
}

# Commit latest changes if any
if [ -n "$(git status --porcelain)" ]; then
  echo ""
  echo "📦 Committing latest changes..."

  git add .

  git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')" || true
fi

# Push feature branch
echo ""
echo "🚀 Pushing feature branch..."

git push -u origin "$FEATURE_BRANCH"

echo ""
echo "=================================================="
echo "Where would you like to merge feature branch?"
echo "=================================================="
echo "1 → main"
echo "2 → develop"
echo "3 → both main + develop"
echo "4 → feature branch only"
echo ""
read -p "Select option (1/2/3/4): " OPTION

# Merge into main
if [[ "$OPTION" == "1" || "$OPTION" == "3" ]]; then

  echo ""
  echo "🔄 Updating main branch..."

  git checkout "$MAIN_BRANCH"

  git pull origin "$MAIN_BRANCH"

  echo ""
  echo "🔀 Merging feature into main..."

  git merge "$FEATURE_BRANCH"

  echo ""
  echo "🚀 Pushing main..."

  git push origin "$MAIN_BRANCH"
fi

# Merge into develop
if [[ "$OPTION" == "2" || "$OPTION" == "3" ]]; then

  echo ""
  echo "🔄 Updating develop branch..."

  git checkout "$DEV_BRANCH"

  git pull origin "$DEV_BRANCH"

  echo ""
  echo "🔀 Merging feature into develop..."

  git merge "$FEATURE_BRANCH"

  echo ""
  echo "🚀 Pushing develop..."

  git push origin "$DEV_BRANCH"
fi

# Ask delete branch
echo ""
read -p "🗑️ Delete feature branch after merge? (y/n): " DELETE_OPTION

if [[ "$DELETE_OPTION" == "y" || "$DELETE_OPTION" == "Y" ]]; then

  git checkout "$MAIN_BRANCH"

  echo ""
  echo "🗑️ Deleting local feature branch..."

  git branch -D "$FEATURE_BRANCH"

  echo ""
  echo "🗑️ Deleting remote feature branch..."

  git push origin --delete "$FEATURE_BRANCH"
fi

echo ""
echo "✅ Workflow completed successfully!"
echo ""