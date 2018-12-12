from fabric.api import local
from fabric.decorators import task


@task(alias='run')
def run_flask(port="5000"):
    local("FLASK_APP=web/app.py FLASK_DEBUG=1 python -m flask run -p %s" % port)
