:: Run the web app

::set FLASK_APP=app
::flask run

pushd app

start app.py

start "" http://localhost:5000

popd