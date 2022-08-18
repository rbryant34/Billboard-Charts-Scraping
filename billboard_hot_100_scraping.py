import requests, bs4, csv, datetime, time, random


def getBeautifulSoupChart(url):
    res = requests.get(url)
    res.raise_for_status()
    chart = bs4.BeautifulSoup(res.text, "lxml")
    return chart


def getTitles(bs4Object):
    titles = bs4Object.select('[class="chart-row__song"]')
    titlesList = [(title.getText()).strip() for title in titles]
    return titlesList


def getArtists(bs4Object):
    artists = bs4Object.select('[class="chart-row__artist"]')
    artistsList = [(artist.getText()).strip() for artist in artists]
    return artistsList


def getRanks(bs4Object):
    ranks = bs4Object.select('[class="chart-row__current-week"]')
    ranksList = [(rank.getText()).strip() for rank in ranks]
    return ranksList


def getChartDate(bs4Object):
    chartDate = chart.select('[datetime]')[0].getText()
    return chartDate


def buildChartDataList(chartDataList, titlesList, artistsList, ranksList, chartDate):
    if (len(titlesList) != len(artistsList)) or (len(titlesList) != len(ranksList)) or (len(artistsList) != len(ranksList)):
        print("Check week " + chartDate)
        return None
    for i in range(len(titlesList)):
        chartDataList.append([ranksList[i], titlesList[i], artistsList[i], chartDate])
    return chartDataList


def writeChartDataToCSV(filePath, chartDataList):
    with open(filePath, 'w', newline='') as billboardFile:
        billboardWriter = csv.writer(billboardFile)
        billboardWriter.writerows(chartDataList)


# Main Script
startComplete = time.time()
start_date_complete = datetime.date(2003, 2, 2)  #input the year, month, and date to start scraping from
end_date_complete = datetime.datetime.now().date()
chartDataList = list() # initialize list of lists to hold charts data
start_date_current = start_date_complete
counter = 0

while start_date_current < end_date_complete:
    start = time.time()
    date_string = datetime.datetime.strftime(start_date_current, "%Y-%m-%d")
    url = 'http://www.billboard.com/charts/hot-100/' + date_string
    try:
        chart = getBeautifulSoupChart(url)
    except:
        pauseLength = random.uniform(10, 20)  #wait to try get again after receiving a throttling error
        print("Pausing", pauseLength, "seconds because of throttling (HTTP Error 503)")
        time.sleep(pauseLength)
        chart = getBeautifulSoupChart(url)
    titlesList = getTitles(chart)
    artistsList = getArtists(chart)
    ranksList = getRanks(chart)
    chartDateString = getChartDate(chart)
    chartDate = datetime.datetime.strptime(chartDateString, "%B %d, %Y").date()
    chartDataList = buildChartDataList(chartDataList, titlesList, artistsList, ranksList, chartDate)
    start_date_current += datetime.timedelta(days=7)
    end = time.time()
    print(chartDate, "week pull:", end - start, "seconds")
    counter += 1
    pauseLength = random.uniform(0, 5)
    time.sleep(pauseLength)
  
writeChartDataToCSV('my_file.csv', chartDataList)

print("Weeks pulled:", counter)
endComplete = time.time()
print("Run time:", endComplete - startComplete, "seconds")