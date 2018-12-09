# Alfred Workflow for Word Counter App

![Word Counter Alfred Workflow Screenshot](https://github.com/markwk/alfred-workflow-wordcounterapp/blob/master/screenshot.jpg)

[Alfred 3 workflow](https://www.alfredapp.com/workflows/) for [Word Counter App](https://wordcounterapp.com/). View your word count stats from previous days and months in Alfred and export daily stats to CSV. 

## Installation

[Download Workflow from Packal](https://github.com/packal/repository/raw/master/com.markwk.alfred.wordcounter/word_counter.alfredworkflow), open and and install. 

(Alternatively [download workflow from github](https://github.com/markwk/alfred-workflow-wordcounterapp/raw/master/Word%20Counter.alfredworkflow)) 

## Usage

* `wcount` - this command will pull up recent stats.
* `wcexport` - export daily word count stats to CSV (example, ~/Documents/WordCounter/export.csv)
* `wchelp` - access links to help and posting bugs


## BONUS: Daily Popup Notification with Yesterday's Word Count

![Word Counter Popup Screenshot](https://github.com/markwk/alfred-workflow-wordcounterapp/blob/master/screenshot-yesterday-pop-up.png)

Want to receive a popup notification each morning with the previous day's workcount? The project contains a special file called "word_counter_yesterday_notify.py," and you can edit your crontab to run this script at a set time each day. Copy the file location and then [follow these steps to setup your Mac's crontab schedule](https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx.html).

## BONUS: Graphic / Chart of Previous Days Word Counter Stats

![Word Counter Data Report Example](https://github.com/markwk/alfred-workflow-wordcounterapp/blob/master/wordcounter-data-report-example.png)

* `report.py` can be used to generate a simple graphic or or chart of your previous days' word count stats. When running the command be sure to include the number of days and target directory for the generated graphic.  
* You'll need to have installed matplotlib library which you can install with the command `$ pip install matplotlib`. 
* Usage: `$ python report.py NUM_DAYS TARGET_DIR` like: `python report.py 7 /Users/my-user-name/Desktop/` 

## Thanks / Acknowledgements

- [deanishe](https://www.alfredforum.com/profile/5235-deanishe/) for the awesome [Python workflow library](http://www.deanishe.net/alfred-workflow/index.html)

## Releases and Versions

See [CHANGELOG](https://github.com/markwk/alfred-workflow-wordcounterapp/blob/master/CHANGELOG.md) for more information.

## To contribute

To contribute to the workflow please fork on github at https://github.com/markwk/alfred-workflow-wordcounterapp

## Creator: 

[Mark Koester](https://github.com/markwk/) | [www.markwk.com](http://www.markwk.com/)
