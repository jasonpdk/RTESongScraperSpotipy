# getAllRunner.py
# Form the URL's for a given RTE radio show and run the scraper. It loops through every day from start date to end date and runs the scraper for that date. If there is 
# nothing for the date RTE returns a 404, the scraper exits, and the loop here continues.
#
# Note: There is definitely a better way to do this than running the python command, this was just quick
#
# Jason Keane - jason@keane.id

import datetime
import subprocess

scriptToRun = "jcscrape.py" # The scrape script to run

stationName = "radio1"
showName = "john-creedon"

base = "https://www.rte.ie/" + stationName + "/" + showName + "/programmes/"

date = datetime.datetime(2013, 1, 1) # Start date (YYYY, MM, DD)
endDate = datetime.datetime(2020, 4, 12) # End date (YYYY, MM, DD)

print("Start Date: " + str(date))
print("End Date: " + str(endDate))

while date < endDate:
    # form the url
    url = base + str(date.year) + "/" + str('{:02d}'.format(date.month)) + str('{:02d}'.format(date.day))
    print(url)

    p = subprocess.run(["python", scriptToRun, url], stderr=subprocess.PIPE)

    returnCode = p.returncode
    if returnCode != 0:
        errorOutput = p.stderr.decode('utf-8').strip('\n')
        print("Scraper failure: " + errorOutput)
        if errorOutput == "Error adding to playlist!":
            exit("Playlist could be full! Last URL: " + url)

    date += datetime.timedelta(days=1)