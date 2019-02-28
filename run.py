import os
from backend import create_app

if __name__ == "__main__":
    # fh=open("/var/run/alterspace/flask.pid", 'w')
    # fh.write(str(os.getpid()))
    # fh.close()
    app = create_app()
    app.run(threaded=True)

