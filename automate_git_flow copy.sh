#!/bin/bash
# automate_git_flow.sh
# Usage: ./automate_git_flow.sh feature-branch

FEATURE_BRANCH=$1

if [ -z "$FEATURE_BRANCH" ]; then
  echo "❌ Please provide the feature branch name."
  echo "Usage: ./automate_git_flow.sh feature-branch"
  exit 1
fi

echo "🚀 Starting workflow for branch: $FEATURE_BRANCH"

# 1. Work on feature branch
git checkout $FEATURE_BRANCH
git add .
git commit -m "Auto: Completed feature implementation"

# 2. Sync with develop before merging
git checkout develop
git pull origin develop
git checkout $FEATURE_BRANCH
git merge develop || {
  echo "⚠️ Merge conflicts detected — please resolve manually."
  exit 1
}

git add .
git commit -m "Auto: Resolved conflicts with develop" || true
git push origin $FEATURE_BRANCH

# 3. Merge feature into develop
git checkout develop
git merge $FEATURE_BRANCH
git push origin develop

# 4. Merge develop into main
git checkout main
git pull origin main
git merge develop
git push origin main

# 5. Sync all branches
git checkout develop
git merge main
git push origin develop

git checkout $FEATURE_BRANCH
git merge develop
git push origin $FEATURE_BRANCH

echo "✅ Workflow completed successfully!"
