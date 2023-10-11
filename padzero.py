# -*- coding: utf-8 -*-
# 
# Copyright (c) 2023~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import re
import sys
from pathlib import Path

import typer
import rich


def _collect_files(path: str) -> list[Path]:
    return [x for x in Path(path).iterdir() if x.is_file()]

def _detect_patterns(sources: list[str]):
    if not sources:
        return []

    patterns: list[list[dict]] = []
    for source in sources:
        parts = []
        for index, part in enumerate(re.split(r'(\d+)', source)):
            part_item = {
                'text': part
            }
            if index % 2 == 1:
                part_item.update(number=int(part))
            parts.append(part_item)
        patterns.append(parts)

    if len(set(len(x) for x in patterns)) != 1:
        # some items does not have same length
        raise NotImplementedError

    for index in reversed(range(1, len(patterns[0]), 2)):
        if len(set(x[index]['number'] for x in patterns)) == 1:
            for parts in patterns:
                parts[index-1]['text'] = ''.join(
                    x['text'] for x in parts[index-1:index+2]
                )
                parts.pop(index) # pop current
                parts.pop(index) # pop next

    # if no numbers, raise error:
    if all('number' not in x for x in patterns[0]):
        raise NotImplementedError

    assert len(set(len(x) for x in patterns)) == 1
    assert len(set(len([y for y in x if 'number' in y]) for x in patterns)) == 1

    return patterns

def _patterns_use_template(patterns: list[list[dict]], template: str):
    template_parts = template.split('*')

    for pattern in patterns:
        for x, y in zip(template_parts, [y for y in pattern if 'number' not in y], strict=True):
            y['text'] = x

    return patterns

def _convert(pattern: list[dict], zeros: int, color: bool):
    def fill(num: int):
        num_str = str(num)
        count = max(zeros - len(num_str), 0)
        padding = '0' * count
        if color:
            padding = f'[green]{padding}[/green]'
        return padding + num_str

    parts = [
        fill(x['number']) if 'number' in x else x['text']
        for x in pattern
    ]

    return ''.join(parts)

def app(path: str, width: int = None, template: str = None):
    files = _collect_files(path)

    patterns = _detect_patterns([x.stem for x in files])

    if template is not None:
        _patterns_use_template(patterns, template)

    if width is None:
        width = 1 + len(
            str(max(y['number'] for x in patterns for y in x if 'number' in y))
        )

    print_stdout = rich.console.Console(file=sys.stdout).print

    results = [
        (_convert(x, width, color=False), y, _convert(x, width, color=True))
        for x, y in zip(patterns, files, strict=True)
    ]
    results.sort()

    for _, file, colored_newname in results:
        print_stdout(f'{file.name} -> ' + colored_newname + file.suffix)

    if input('Press Y to rename...: ').lower() == 'y':
        for newname, file, _ in results:
            file.rename(file.with_name(newname + file.suffix))

def main(argv=None):
    typer.run(app)

if __name__ == '__main__':
    sys.exit(main() or 0)
