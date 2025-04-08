from invoke import task


@task
def start(ctx):
    ctx.run("python src/index.py", pty=True)


@task
def tests(ctx):
    ctx.run("pytest src", pty=True)


@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage html", pty=True)
    ctx.run("open htmlcov/index.html", pty=True)


@task
def build(ctx):
    ctx.run("python src/build.py", pty=True)


@task
def pylint(ctx):
    ctx.run("pylint src", pty=True)
