## Running the project
### Setup up virtual env

```
python3 -m venv ./env
source env/bin/activate
```

### Install dependencies
```
pip3 install -r requirements.txt
```

### Setup Postgres database
```
createdb flyyur-app
```
Updates the credentials on `application/config.py` where you will see the config variable `SQLALCHEMY_DATABASE_URI`.

Export some flask variables.
```
export FLASK_APP=application/app.py
export FLASK_ENV=development
```

Now use migrations to setup the database tables
```
python3 -m flask db migrate
python3 -m flask db upgrade
```

### Run the server
```
python3 -m flask run
```
Access the app at [http://127.0.0.1:5000](http://127.0.0.1:5000)