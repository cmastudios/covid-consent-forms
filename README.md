Consent Form Management Portal
==============================



Customizing Settings
--------------------

1. Create a file in covidconsent/settings called local.py.
2. Add `from .development import *` to base your changes on the dev config, or otherwise if basing on production.
3. Add your overrides to local.py
4. Set the environment variable `DJANGO_SETTINGS_MODULE=covidconsent.settings.local` and run the app.

