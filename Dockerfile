FROM microsoft/windowsservercore

ENV APP_DIR='/app'
WORKDIR APP_DIR
ENV PYTHONPATH=$APP_DIR:$PYTHONPATH

COPY requirements.txt .
RUN ["python", "-m", "pip", "install", "requirements.txt"]

COPY . .

CMD ["python3", "run_spider.py"]

"""
Step 6/8 : RUN ["python", "-m", "pip", "install", "requirements.txt"]
 ---> Running in 3d3c7840c9a2
container 3d3c7840c9a2ca50bbbba7c8ee662dd75c2405c5fe414594911199866b316b96 encountered an error during CreateProcess: failure in a Windows system call: Systém nemůže nalézt uvedený soubo
r. (0x2)
[Event Detail:  Provider: 00000000-0000-0000-0000-000000000000] extra info: {"CommandLine":"python -m pip install requirements.txt","WorkingDirectory":"C:\\APP_DIR","Environment":{"APP_D
IR":"/app","PYTHONPATH":"/app:"},"CreateStdInPipe":true,"CreateStdOutPipe":true,"CreateStdErrPipe":true,"ConsoleSize":[0,0]}
"""