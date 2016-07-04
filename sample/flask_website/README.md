# QuadrigaCX Python API

- quadriga/ is a Python package that interfaces with the QuadrigaCX API (v2).
  - You will need to create a config file in order to use the authenticated API actions.  There's a sample.
  - That file should look something like this:

      [authentication]  
      client_id=0000  
      key=yOurKeY  
      secret=Y0Ur53crr3T142351236  

- app.py is a Flask server which provides a web interface for the API functions.

- lobject/ is a package I made during the course of creating this API, and I have added it to my personal toolbox but it isn't available anywhere but this package.
