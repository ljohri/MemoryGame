This will create a light weight flask server
    install python and pip
    pip install flask-ask (the project is at Github: https://github.com/johnwheeler/flask-ask) this is the alexa ask library
    flask_ask documentaion is here: http://flask-ask.readthedocs.io/en/latest/
    use ngrok to allow access to the server locally
    templates.yaml holds the detailed intents for flask-ask

python memory_game.py

Go to developer.amazon.com and add the skill using intents.json as custom interaction model
Use samples utterences.txt for adding utterences to the skill
use https end point
enter the ngrok endpt
ssl certificate setting: My development endpoint is a subdomain of a domain that has a wildcard certificate from a certificate authority.
Test at https://echosim.io/


To add an intent/dialog using flask_ask
add to the intent schema and sample utterences on interaction model at developer.amazon.com
same intent schema has to be put on the intents.json on the python 

schema
sqlite> CREATE TABLE game(
   ...> device_id integer DEFAULT 0,
   ...> name text DEFAULT "ChotaKutta",
   ...> session text DEFAULT "INITIAL",
   ...> type text DEFAULT "number",
   ...> duration integer NOT NULL,
   ...> timeofday text NOT NULL,
   ...> PRIMARY KEY(timeofday)
   ...> );

database name memorygame.sq3db

ngrok http 5000

