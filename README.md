Solar Orbiter Data Availability (SODA)
======================================

A tool to visualise the data availability of Solar Orbiter data products.
The dashboard can be viewed at https://www.davidstansby.com/soda/.

Usage
-----

`python run_soda.py` will run SODA, and create an updated `index.html` file.

Automatic deployment
--------------------
Github actions automatically deploys a new HTML file to the `pages` branch
every time a commit is pushed to the main branch.
