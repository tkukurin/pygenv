"""Wraps global environment maintenance."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['err', 'out', 'info', 'tell', 'ProcResult', 'sprun', 'GlobalEnv', 'env_make_activate', 'cli']

# %% ../nbs/00_core.ipynb 4
import typer
from functools import partial
import json
import os
from pprint import pformat
import sys
from pathlib import Path
import subprocess as sproc

import subprocess
from dataclasses import dataclass, field
from rich import print
from rich.console import Console

err = Console(stderr=True)
out = Console(stderr=False)

# informational vs output data
# e.g. `tell` is meant to be piped or consumed by another script
# `info` is just hack to replace logging
info = err.log
tell = lambda *a: out.log(*a) if any(a) else None


@dataclass
class ProcResult:
    ok: bool
    out: str
    err: str
    raw: None | sproc.CompletedProcess = field(repr=False, default=None)


def sprun(*args, guard: bool = True, **kwargs) -> ProcResult:
    try:
        result = subprocess.run(
            tuple(map(str, args)),
            capture_output=True,
            text=False,  # Keep raw output as bytes
            **kwargs
        )
    except Exception as e:
        if not guard:
            raise
        info(f"Failed:\n$ {args}\n  {e}")
        return ProcResult(False, "", "", None)
    return ProcResult(
        ok=result.returncode == 0,
        out=result.stdout.decode('utf-8', errors='replace').strip() if result.stdout else "",
        err=result.stderr.decode('utf-8', errors='replace').strip() if result.stderr else "",
        raw=result,
    )


class GlobalEnv:
    """instance of a globally managed environment
    """

    BASE = Path("~/tk/uv").expanduser() 

    def __init__(self, name: str):
        self.name = name
        self.path = self.BASE / name

    def activate_path(self, shell = None) -> Path:
        shell = shell or os.path.basename(os.getenv('SHELL', '/bin/bash'))
        for n, activate_file in ({
            'bash': 'activate',
            'zsh': 'activate',
            'fish': 'activate.fish',
            'csh': 'activate.csh',
        }).items():
            if shell.startswith(n):
                break  # fix for "fishlogin"
        return self.path / "bin" / activate_file
    
    def validate(env, shell = None):
        feats = dict(
            has_py = (env.path / "bin" / "python").exists(),
            has_activate = env.activate_path(shell).exists(),
            activate = env.activate_path(shell),
            py = sprun(
                str(env.path / "bin" / "python"),
                "--version"
            ).out,
            detail = dict(
                libs=json.loads(sprun("pip", "list", "--format=json").out or "[]"),
            )
        )
        is_valid = all(v for k, v in feats.items() if k.startswith("has"))
        return is_valid, feats



_OPT_VERBOSE = typer.Option(
    0, "--verbose", "-v", count=True, envvar="TK_PYGENV_DEBUG", max=1)

_OPT_CONFIG = typer.Option(
    # vscode suggestion: {"python.venvFolders": ["~/tk/uv/"]}
    Path("~/tk/uv").expanduser(), "--basedir", "-b", resolve_path=True, dir_okay=True, file_okay=False, envvar="TK_PYGENV_BASE"
)

def env_make_activate(
    name: str,
    verbose: int = _OPT_VERBOSE,
    basedir: Path = _OPT_CONFIG,
):
    GlobalEnv.BASE = Path(basedir)

    outs = None
    env = GlobalEnv(name)

    valid, feats = env.validate()
    if valid:
        outs = feats["activate"]
    elif not env.path:
        info(f"Nothing found on {env.path}. Creating...")
        created = sprun("uv", "venv", env.path)
        info(f"{created.ok=}")
    else:
        info(f"{env.path} seems to exist as non-Python venv.")
        return None, ""
    
    if not verbose:
        feats.pop("detail", None)
    info(f"Env feats:\n{pformat(feats)}")
    return env, outs


def cli():
    _, outs = typer.run(env_make_activate)
    tell(outs)

