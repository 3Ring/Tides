**Async Web-Scraper using Python, Selenium, and asyncio**

**How to to use:**

1. In Linux From the root of this repo:
   1. Create python virtual environment: `python -m venv tides`
   1. Activate the venv: `source tides/scripts/activate`
   1. Install dependencies: `pip install -r requirements.txt`
   1. Run Scraper: `python main.py`
   1. Optionally you may add a commandline argument to specifiy how many browsers to create: `python main.py 4` (the default is 3)

**Project Specifications:**

- Main page to scrape: "https://www.tide-forecast.com/"
- Load the tide forecast page for each location and extract information on low tides that occur after sunrise and before sunset. Return the time and height for each daylight low tide.    
- Locations:
  - Half Moon Bay, California
  - Huntington Beach, California
  - Providence, Rhode Island
  - Wrightsville Beach, North Carolina

**High Level Thoughts on the Project:**

- I attempted to write this program in a way that assumed it would be part of a larger infrastucture. This is why I used asyncio, which would be needlessly complex for a scraper that only touches four sites. The `Browser` class from which the `Tides` inherits was my attempt to show this project as part of that larger picture. The `Browser` class contains all of the general purpose methods like getting elements from the DOM and navigation. I had already created something like this for a different project which I borrowed code from. You can see it [HERE:](https://github.com/3Ring/Chronicler/tree/integration_testing/tests/integration/browser) 
- The information is returned this format: `[{'Half Moon Bay': [('7:02AM', '1.78ft'), ('5:35PM', '2.13ft')]}, {'Wrightsville Beach': [('2:30PM', '-0.2ft')]}, {'Huntington Beach': [('3:49PM', '3.08ft')]}, {'Providence': [('2:22PM', '0ft')]}]` Currently this program only prints out the information. It would be easy however to change it to any other format.
- Web-scrapers are inherently fragile programs, and to improve this (and if it were to be used in a professional environment) I would want to impliment unit tests as well and custom Exceptions for different areas for better logging and debugging. Another thought would be to have the program automatically attempt the program again upon failure for a preset amount of times, while possibly trying different browser brands.
- An edgecase that could potentially return incorrect information may occur when the scraper is run very near the end of the day for the local time and would result in the program returning data for the previous day. This can be avoided by always knowing when the program will be run, or by only returning low tides at least a couple minutes in the future that are the same day.

