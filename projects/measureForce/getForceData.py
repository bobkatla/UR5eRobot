import subprocess

h = "10.10.10.7"

subprocess.check_output(["python", "../commonSources/extractData/record.py", "--host", str(h), "--samples", "1", "--frequency", "5", "--config", "../commonSources/extractData/config/testforce.xml"])