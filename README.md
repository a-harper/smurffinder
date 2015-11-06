=====
SmurfFinder
=====

SmurfFinder is a Django app to find potential smurf accounts for Steam Users.

The app attempts to find a user's smurf (or main) account from their friends list. If the user is set to private but you find a friend of theirs, you can search by proxy using /smurf/proxy URL.

Quick start
-----------

Make sure you have the required packages & django apps. SmurfFinder requires SteamAPI, urllib2, fuzzywuzzy and Scipy.

1. Add "SmurfFinder" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'smurffinder',
    )

2. Include the SmurfFinder URLconf in your project urls.py like this::

    url(r'^smurf/', include('smurffinder.urls', namespace="smurffinder")),

3. Start the development server and visit http://127.0.0.1:8000/smurf
   
4. Start finding!
