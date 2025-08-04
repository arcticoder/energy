#!/bin/bash

for dir in */; do
  cd "$dir" || continue

  # Extract owner/repo from remote URL
  repo_url=$(git remote get-url origin 2>/dev/null)
  if [[ "$repo_url" =~ github.com[:/](.+)/(.+?)(\.git)?$ ]]; then
    owner="${BASH_REMATCH[1]}"
    repo="${BASH_REMATCH[2]}"    
    repo="${repo%.git}"

    echo "Enabling discussions for $owner/$repo..."
    gh api --method PATCH "/repos/$owner/$repo" \
      -f has_discussions=true >/dev/null && echo "✔ Done" || echo "✖ Failed"
    echo "API call: gh api --method PATCH /repos/$owner/$repo -f has_discussions=true"
  else
    echo "⚠ No valid GitHub remote found in $dir"
  fi

  cd ..
done
