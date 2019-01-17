from fabric.api import local
from fabric.decorators import task


@task(alias='run')
def run_flask(port="5000"):
    local("FLASK_APP=run.py FLASK_DEBUG=1 python -m flask run -p %s" % port)


@task
def npm_install():
    local("cd frontend && npm install")

@task
def npm():
    local("cd frontend && npm run serve")

@task
def build():
    local("cd frontend && npm run build")


@task
def test():
    local("pytest --ignore=frontend/node_modules")
