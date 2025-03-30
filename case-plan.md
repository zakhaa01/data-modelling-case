# Nastusha's 2nd engineering project

- API requests
    - Pythonshell script
        - With parametrised querying
        - API read
        - Output payload (probably JSON) to pd.Dataframe
        - Clean it and transform (if needed)
        - Load to PostgresQL
    - Python Unit Tests
        - For API calls
        - For separate functions
- DBT
    - 3 layer model
        - Raw (not in DBT! Handled by API ETL Pipeline)
        - Staging
        - Marts
    - Tests
    - Postgresql adapter
- Airflow DAG
    - API pythonshell -> DBT

- API Exploration
    - API Documentation
        - What data can be fetched from API
        - What format of payload
            - Input
            - Output
        - Pick what data you want to use
            - 2-3 data sources
            - Should be joinable (logically connected)
        - Find API Endpoints and methods for chosen data
    - Exploratory Data Analysis
        - Test batches read
            - Test joins

- Git config for a remote github remository!
