# simple-api-server

This simple-api-server project is an exercise on how to build a simple HTTP API server quickly.

For simplicity and time in budget, we would use SQLite for demo purpose. With well awareness of the limitation on SQLite in write performance,
We introduce a write queue and other performance optimization in making it a sound choice for IoT device or relatively lower resource environment.
- For resource-constrained environment (e.g. IoT or non-high traffic API server), we picked SQLite as it is serverless and light in weight.
It is ideal for low resource consumption and simple in setup.
- For higher usage on the API server (e.g. microservices), it would be better to switch to MySQL or PostgreSQL. With the help of SQLModel, it helps us in building a loosely coupled DB connection by just changing the create_engine() string in the code. 

For detail, please refer to the documentation on how to integrate of that specific SQL server accordingly.


## Requirements
- python3.13+


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

Step 4: Install uvicorn
```bash
pip install uvicorn
```

step 5: Install sqlalchemy
'''bash
pip install sqlalchemy
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
- Under SQLite, we should introduce one memory instance and one backup instance. With that, it will further help in terms of read & write performance of the database by using memory instance. The backup instance would be used as a master copy of the memory instance so that it would be updated periodically. 

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

