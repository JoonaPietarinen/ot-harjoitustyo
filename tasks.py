from invoke import task
import sys

IS_WINDOWS = sys.platform.startswith("win")
SEP = " & " if IS_WINDOWS else "; "


@task
def run(ctx):
    ctx.run("python3 src/main.py", pty=not IS_WINDOWS)


@task
def test(ctx):
    ctx.run("pytest src", pty=not IS_WINDOWS)


@task
def coverage_report(ctx):
    cmd = f"coverage run --branch -m pytest src{SEP}coverage html"
    ctx.run(cmd, pty=not IS_WINDOWS)