"""Typer base cli interface to allow the user to interact with the udppf system"""

import os
import signal
from pathlib import Path
from typing import Annotated
import typer
from UDPPFunctionTranslator import UDPPFunctionTranslator
from flask import Flask, request, jsonify,make_response
import time
import multiprocessing

app_typer = typer.Typer()

app_flask = Flask(__name__)

flask_server: multiprocessing.Process = None

PIPELINES_FOLDER = str(Path(str(os.path.dirname(__file__))).parent.joinpath("pipelines"))
TMP_FOLDER = str(Path(PIPELINES_FOLDER).joinpath("generated/"))

terminate_flask: bool = False

def signal_andler(signum, frame):
    global terminate_flask
    terminate_flask = True
    time.sleep(4)
    exit(1)
signal.signal(signal.SIGINT, signal_andler)


@app_flask.route("/")
def index():
    return "<p>Hello, World!</p>"



def flask_server_task(_config: dict):
    host:str = _config.get("host", "0.0.0.0")
    port: int = _config.get("port", 5000)
    debug: bool = _config.get("debug", False)

    # TODO SET STATIC FOLDER
    #
    app_flask.run(host=host, port=port, debug=debug)




@app_typer.command()
def launch(ctx: typer.Context, port: int = 5555, host: str = "0.0.0.0", flask_debug: bool = True):
    global terminate_flask
    #flask_server.start()
    flask_config = {"port": port, "host": host, "debug":flask_debug}
    flask_server:multiprocessing.Process = multiprocessing.Process(target=flask_server_task, args=(flask_config,))
    flask_server.start()

    while( not terminate_flask):
        if typer.prompt("Terminate  [Y/n]", 'y') == 'y':
            break


    # STOP
    flask_server.terminate()
    flask_server.join()



@app_typer.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    pass
    #Path(PIPELINES_FOLDER).mkdir(parents=True, exist_ok=True)
    #Path(TMP_FOLDER).mkdir(parents=True, exist_ok=True)






if __name__ == "__main__":
    app_typer()
