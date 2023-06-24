Usage
------
We are using the Poetry dependency manager instead of pip/requirements.txt. To install a new dependency, for example, run ``poetry add spotipy`` rather than ``pip install spotipy``.

Installation
------------
Run these commands once.

``pip install --user poetry``

``cd ece-496-ml-and-ai-music/intune-server``

``poetry install``

Running the Server
------

``cd ece-496-ml-and-ai-music/intune-server/intune-server``

On mac/linux: ``export FLASK_APP=app``

On windows: ``set FLASK_APP=app``

``poetry run flask run``
