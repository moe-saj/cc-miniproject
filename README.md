# MiniProject

REST API created using Flask for Cloud Computing.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libraries:

```bash
pip install Flask
pip install requests
pip install cassandra-driver
```

## Set Up
To run, please ensure that an instance of CassandraDB exists and has the pokemon.csv data loaded. This can be done by following part 2 in week 10's lab.

The current address for the instance is 127.0.0.1:9042 (i.e. localhost), so please ensure that Cassandra is running locally. If Cassandra is running elsewhere, please ensure you update the contact_point on line 5.

Once set up, the code can be run locally using:
```bash
python cw.py
```

## Endpoints
```python
/pokemon/<name> - supports GET, PUT and DELETE to fetch, update and remove Pokemon, respectively.
/pokemon/all - fetches all Pokemon.
/pokemon/new - creates new a Pokemon.
```



