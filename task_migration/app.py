from flask import Flask
import subprocess
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Cloud Node Service"

@app.route('/compute-heavy')
def compute_heavy():
    try:
        num_cores = os.cpu_count() 
        # print(f"Number of cores: {num_cores}")
        # target_cores =int(num_cores)
        duration = 600
        subprocess.Popen(['stress-ng', '--cpu', str(num_cores), '--cpu-method', 'matrixprod', '--cpu-load', '80', '--timeout', str(duration)])
        return f"Started stress with {num_cores} threads for {duration} seconds!", 200

    except Exception as e:
        return f"Error occurred: {str(e)}", 500

@app.route('/stop')
def stop_stress():
    global stress_process
    if stress_process and stress_process.poll() is None:
        stress_process.terminate()
        stress_process.wait(timeout=5)
        stress_process = None
        return "Stopped stress-ng process successfully.", 200
    else:
        return "No stress-ng process is currently running.", 200

@app.route('/work')
def work():
    start = time.time()
    while time.time() - start < 0.2:  
        pass
    return "Work task completed\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)