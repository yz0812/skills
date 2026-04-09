#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ALLOWED_PROPERTIES = {
    'name',
    'description',
    'license',
    'allowed-tools',
    'metadata',
    'compatibility',
    'argument-hint',
    'disable-model-invocation',
    'user-invocable',
    'model',
    'effort',
    'context',
    'agent',
    'hooks',
    'paths',
    'shell',
}

BOOL_FIELDS = {'disable-model-invocation', 'user-invocable'}
STRING_FIELDS = {
    'name', 'description', 'license', 'compatibility', 'argument-hint',
    'model', 'effort', 'context', 'agent', 'shell'
}
LIST_OR_STRING_FIELDS = {'allowed-tools', 'paths'}
DICT_FIELDS = {'metadata', 'hooks'}
EFFORT_VALUES = {'low', 'medium', 'high', 'max'}
CONTEXT_VALUES = {'fork'}
SHELL_VALUES = {'bash', 'powershell'}


def parse_scalar(value: str):
    value = value.strip()
    if value in ('true', 'false'):
        return value == 'true'
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def parse_simple_yaml(frontmatter_text: str):
    data = {}
    lines = frontmatter_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith(' ') or line.startswith('\t'):
            raise ValueError(f'Unexpected indentation: {line}')
        if ':' not in line:
            raise ValueError(f'Invalid frontmatter line: {line}')
        key, raw = line.split(':', 1)
        key = key.strip()
        raw = raw.strip()
        if not key:
            raise ValueError(f'Invalid frontmatter key: {line}')
        if raw:
            data[key] = parse_scalar(raw)
            i += 1
            continue

        block = []
        i += 1
        while i < len(lines):
            nested = lines[i]
            if not nested.strip():
                block.append(nested)
                i += 1
                continue
            if not (nested.startswith(' ') or nested.startswith('\t')):
                break
            block.append(nested)
            i += 1

        meaningful = [b for b in block if b.strip()]
        if not meaningful:
            data[key] = ''
            continue

        if all(b.lstrip().startswith('- ') for b in meaningful):
            items = []
            for b in meaningful:
                item = b.lstrip()[2:].strip()
                items.append(parse_scalar(item))
            data[key] = items
            continue

        nested_dict = {}
        for b in meaningful:
            stripped = b.lstrip()
            if ':' not in stripped:
                raise ValueError(f'Invalid nested frontmatter line: {b}')
            nk, nv = stripped.split(':', 1)
            nested_dict[nk.strip()] = parse_scalar(nv.strip()) if nv.strip() else ''
        data[key] = nested_dict
    return data


def validate_skill(skill_path: str):
    skill_path = Path(skill_path)
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, 'SKILL.md not found'

    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, 'No YAML frontmatter found'

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, 'Invalid frontmatter format'

    try:
        frontmatter = parse_simple_yaml(match.group(1))
    except ValueError as e:
        return False, f'Invalid YAML in frontmatter: {e}'

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get('name')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > 64:
        return False, f'Name is too long ({len(name)} characters). Maximum is 64 characters.'

    description = frontmatter.get('description')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if not description:
        return False, 'Description cannot be empty'
    if '<' in description or '>' in description:
        return False, 'Description cannot contain angle brackets (< or >)'
    if len(description) > 1024:
        return False, f'Description is too long ({len(description)} characters). Maximum is 1024 characters.'

    for key in STRING_FIELDS & frontmatter.keys():
        if not isinstance(frontmatter[key], str):
            return False, f"{key} must be a string, got {type(frontmatter[key]).__name__}"

    for key in BOOL_FIELDS & frontmatter.keys():
        if not isinstance(frontmatter[key], bool):
            return False, f"{key} must be a boolean, got {type(frontmatter[key]).__name__}"

    for key in LIST_OR_STRING_FIELDS & frontmatter.keys():
        value = frontmatter[key]
        if not isinstance(value, (str, list)):
            return False, f"{key} must be a string or list, got {type(value).__name__}"
        if isinstance(value, list) and not all(isinstance(item, str) for item in value):
            return False, f'{key} list items must all be strings'

    for key in DICT_FIELDS & frontmatter.keys():
        value = frontmatter[key]
        if not isinstance(value, dict):
            return False, f"{key} must be a mapping, got {type(value).__name__}"

    if 'effort' in frontmatter and frontmatter['effort'] not in EFFORT_VALUES:
        return False, f"effort must be one of: {', '.join(sorted(EFFORT_VALUES))}"

    if 'context' in frontmatter and frontmatter['context'] not in CONTEXT_VALUES:
        return False, f"context must be one of: {', '.join(sorted(CONTEXT_VALUES))}"

    if 'shell' in frontmatter and frontmatter['shell'] not in SHELL_VALUES:
        return False, f"shell must be one of: {', '.join(sorted(SHELL_VALUES))}"

    if frontmatter.get('agent') and frontmatter.get('context') != 'fork':
        return False, 'agent requires context: fork'

    return True, 'Skill is valid!'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python scripts/validate_skill.py <skill_directory>')
        sys.exit(1)
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
