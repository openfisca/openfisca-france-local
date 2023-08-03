changelog_file = open('CHANGELOG.md', 'r')

changelog_lines: list[str] = changelog_file.readlines()

is_last_content: bool = False

last_version_changes: str = ""

for line in changelog_lines:
    if line.startswith('## [') and not last_version_changes:
        is_last_content = True
    elif is_last_content and line.startswith('## ['):
        is_last_content = False
    elif is_last_content:
        last_version_changes += line

print(last_version_changes)
