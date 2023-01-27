⚠️ This repository is now archived, and will not see any changes ⚠️

I no longer have time to update this now I am a Research Software Engineer. If you would like to see this maintained, and can find funding that can be sent to a UK university (UCL), please get in touch and I might be able to maintain and improve this as part of my day job!

Otherwise I'm very happy for someone to fork this and start maintaining it themselves.


Solar Orbiter Data Availability (SODA)
======================================

A tool to visualise the data availability of Solar Orbiter data products.
The dashboard can be viewed at https://www.davidstansby.com/soda/.

Usage
-----

`python run_soda.py` will run SODA, and create an updated static `index.html` file that can be uploaded to a server.

Automatic deployment
--------------------
Github actions automatically deploys a new HTML file to the `pages` branch
every time a commit is pushed to the main branch.

Feedback/support
----------------
If you have any problems or suggestions for SODA, please open an issue at https://github.com/dstansby/soda/issues.
I'm not currently accepting pull requests from others, but will happily take suggestions and implement them myself.
