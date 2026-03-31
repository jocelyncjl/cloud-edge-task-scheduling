from flask import Flask
import multiprocessing
import time
import os

app = Flask(__name__)

processes = []
load_started = False

def cpu_burner():
    while True:
        start = time.time()
        while time.time() - start < 0.08:
            pass
        time.sleep(0.02)

@app.route("/start")
def start_load():
    global load_started, processes

    if load_started:
        return "Load already running.\n"

    num_procs = 2
    load_started = True

    for _ in range(num_procs):
        p = multiprocessing.Process(target=cpu_burner)
        p.start()
        processes.append(p)

    return f"Started CPU load with {num_procs} processes\n"

@app.route("/stop")
def stop_load():
    global load_started, processes

    for p in processes:
        p.terminate()
        p.join()

    processes = []
    load_started = False

    return "Stopped all CPU load processes.\n"


@app.route('/work')
def work():
    start = time.time()
    while time.time() - start < 0.2:  
        pass
    return "Work task completed\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6060)