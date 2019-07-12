#!/usr/bin/env python3

import subprocess
import os

from dataclasses import dataclass
from typing import List

import click


@dataclass
class Workspace:
    name: str
    working_dir: str = "~"
    cmd: List[str] = lambda: ["pipenv", "run", "nvim"]


workspaces = [
    Workspace(
        name="Deploy",
        cmd=["zsh"],
    ),
    Workspace(
        name="Analytics",
        working_dir="~/dev/forter/analytics/src",
    ),
    Workspace(
        name="Pybolts",
        working_dir="~/dev/pybolts-infra",
    ),
    Workspace(
        name="Velocity",
        working_dir="~/dev/velocity",
    ),
    Workspace(
        name="Forter",
        working_dir="~/dev/forter/storm",
        cmd=["pipenv", "run", "nvim"],
    ),
    Workspace(
        name="Session Persistence",
        working_dir="~/dev/sessions_persistence",
    ),
    Workspace(
        name="Crons",
        working_dir="~/dev/crons",
    ),
    Workspace(
        name="Crons DSL",
        working_dir="~/dev/crons_dsl",
        cmd=["nvim"],
    ),
    Workspace(
        name="Notes",
        working_dir="~/Documents/notes",
        cmd=["nvim"],
    ),
    Workspace(
        name="Config",
        working_dir="~/.local/MyConfigs",
        cmd=["nvim"],
    ),
]


@click.command()
@click.argument(
    "name",
    default="",
)
def main(name):
    matches = sorted(
        [
            w
            for w in workspaces
            if w.name.lower().startswith(name.lower())
        ],
        key=lambda w: w.name,
    )
    if len(matches) == 0:
        click.echo(f"No workspace matches `{name}`")
        return
    if len(matches) > 1:
        str_matches = ''.join(
            f"\n - {w.name}"
            for w in matches
        )
        click.echo(f"Possible matches:{str_matches}")
        return
    match = matches[0]
    subprocess.run(
        [
            "tmux",
            "-f",
            os.path.expanduser("~/.config/tmux/config"),
            "new",
            "-s",
            match.name,
        ] + match.cmd,
        cwd=os.path.expanduser(match.working_dir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).check_returncode()


if __name__ == "__main__":
    main()
