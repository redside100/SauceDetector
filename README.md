## Sauce Detector

This is a proof of concept! Everything was hacked together in less than 48 hours, from sheer boredom.

This uses nagadomi's cascade classifier: https://github.com/nagadomi/lbpcascade_animeface (I may have ripped their
example detector and changed a few things)

To compile and run, you need Python 3.7+. This only works on Windows, as it uses win32api.
All dependencies are in requirements.txt, you can run `pip install -r requirements.txt`. 

This won't work without an imgur API client ID. 
You'll need to register an application and get one from their site: https://api.imgur.com/oauth2/addclient,
then put your client ID into a file called `client_id` in the root directory.

Finally, run it with `python sauce.py`. Hold `shift + f` for one second when hovering over a box
to crop, upload and reverse search the selection in a new tab.
