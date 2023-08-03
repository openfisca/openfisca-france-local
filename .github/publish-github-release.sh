#! /usr/bin/env bash

version=$(python setup.py --version)
changelog_content=$(python .github/get_changelog_content.py)

curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $1" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/openfisca/openfisca-france-local/releases \
  -d '{"tag_name":"'"$version"'","name":"'"$version"'","body":"'"$changelog_content"'","draft":true,"prerelease":false,"generate_release_notes":false}'
