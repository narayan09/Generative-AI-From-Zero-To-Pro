#!/bin/bash
<<<<<<< HEAD
=======
# automate_git_flow.sh
# git checkout -b feature-login
# Usage: ./automate_git_flow.sh feature-branch
>>>>>>> ea5fd49 (Updated git automation script)

FEATURE_BRANCH="$1"

if [ -z "$FEATURE_BRANCH" ]; then
  echo "Please provide feature branch name"
  exit 1
fi

echo "Starting workflow for: $FEATURE_BRANCH"

git checkout "$FEATURE_BRANCH"

git add .

git commit -m "Auto: Completed feature implementation"

git checkout develop
git pull origin develop

git checkout "$FEATURE_BRANCH"

git merge develop || {
  echo "Merge conflicts detected"
  exit 1
}

git add .

git commit -m "Auto: Resolved conflicts with develop" || true

git push origin "$FEATURE_BRANCH"

git checkout develop

git merge "$FEATURE_BRANCH"

git push origin develop

git checkout main

git pull origin main

git merge develop

git push origin main

git checkout develop

git merge main

git push origin develop

git checkout "$FEATURE_BRANCH"

git merge develop

git push origin "$FEATURE_BRANCH"

echo "Workflow completed!"