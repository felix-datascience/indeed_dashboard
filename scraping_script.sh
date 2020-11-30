#!/bin/bash
# Script for running scraper, putting scraped data file in project directory
# and pushing changes to GitHub

YearStart=`date +%Y`
MonthStart=`date +%m`
DayStart=`date +%d`
HourStart=`date +%H`
MinuteStart=`date +%M`
SecondStart=`date +%S`
DateStart=$"$YearStart-$MonthStart-$DayStart"
TimeStampStart=$"[$DateStart $HourStart:$MinuteStart:$SecondStart]"

ProjectRootFolder=$"/home/pi/indeed_dashboard_deployed"
ScraperFolder=$"/home/pi/indeed_dashboard_tools/scraper"
DataFolder=$"$ProjectRootFolder/data"
FileName=$"$DataFolder/$YearStart-$MonthStart-$DayStart.json"

# Print message when starting
echo "$TimeStampStart Start scraping script..."

# Check if file already exists


# Change directory to where scraper is located
cd $ScraperFolder

# Scraping
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl jobs -o $FileName
#sleep 5
#touch $FileName

# Change directory to root directory of project
cd $ProjectRootFolder

# Add new file to stage area, commit and push to GitHub repository
CommitMessage=$"Automatic commit: Add scraped date from $DateStart"
#CommitMessage=$"Data pipeline test run $TimeStampStart"
git pull
git add .
git commit -m "$CommitMessage"
git push

# Print message when done
YearEnd=`date +%Y`
MonthEnd=`date +%m`
DayEnd=`date +%d`
HourEnd=`date +%H`
MinuteEnd=`date +%M`
SecondEnd=`date +%S`
DateEnd=$"$YearEnd-$MonthEnd-$DayEnd"
TimeStampEnd=$"[$DateEnd $HourEnd:$MinuteEnd:$SecondEnd]"
echo "$TimeStampEnd Done"
