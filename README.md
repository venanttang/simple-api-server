# simple-api-server

This simple-api-server project is an exercise on how to build a simple HTTP API server quickly.

For simplicity and time in budget, we would use SQLite for demo purpose. With well awareness of the limitation on SQLite in write performance,
We introduce a write queue and other performance optimization in making it a sound choice for IoT device or relatively lower resource environment.
- For resource-constrained environment (e.g. IoT or non-high traffic API server), we picked SQLite as it is serverless and light in weight.
It is ideal for low resource consumption and simple in setup.
- For higher usage on the API server (e.g. microservices), it is easy for our code to switch to use MySQL or PostgreSQL with SQLModel by changing the create_engine() in the code. For detail, please refer to the documentation on how to integrate of that specific SQL server accordingly.

As said, it is better to integrate and use MySQL or other SQL server for higher traffic use cases.


## Requirements
- python3.13+
##### Note: This project was developed and maintained on MacOS. However, it should run fine on Linux with Python 3.13+. If not, please contact me for the fix. You are advised to use 'venv' for virtual environment for python. Please install & activate it if you haven't done that yet. 


## Installation

Step 1: Download the source code to your local directory of your machine 
```bash
git clone https://github.com/venanttang/simple-api-server.git
```

Step 2: Open the command prompt (e.g. terminal app for mac user) and go to the "simple-api-server" directory
```bash
cd simple-api-server
```

Step 3: Install it and it will install all the required libraries accordingly.
```bash
pip install -r requirements.txt
```



## Usage
Once the installation is done:

Step 1: Go to the project folder (if you are not)
```bash
cd simple-api-server
```

Step 2: Run the app.
```bash
uvicorn main:app --reload
```

You will see some log like below.
```
INFO:     Will watch for changes in these directories: ['/Users/xxxx/CodeLab/SimpleAPIServer']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [3823] using StatReload
2025-04-28 11:31:45 - main.py:21 - INFO - debug=False
2025-04-28 11:31:45 - main.py:125 - INFO - Starting write queue processing thread...
2025-04-28 11:31:45 - main.py:107 - INFO - Starting up write queue...
INFO:     Started server process [3825]
INFO:     Waiting for application startup.
2025-04-28 11:31:45 - main.py:66 - INFO - Starting up the SimpleAPIServer application...
INFO:     Application startup complete.
```

There you go. The Simple API Server is started up successfully. You can start fetching API request for the JSON data from the Simple API Server through port 8000. More detail information would be showed in [API Design](API_DESIGN.md).

## API Design
For [API Design](API_DESIGN.md), please check the link accordingly.

## Roadmap
- Authorization or API gateway would be needed
- API rate limit per IP would be needed and make it configurable so that a certain API may be expected to have a higher traffic rate than others
- Better support on switching between SQLite and MySQL (or PostgreSQL)
- Make the max size of write queue to be configurable
- Dynamically & smartly adjust the write queue size according to policy and available memory

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

