# Download online news from several news websites
# Usage: python3 $0 --help
# Input: 1) desired news source 2) begin timestamp 3) end timestamp
# Output: All news in the specified time span from the given source, in JSON format
# Author: Po-Chuan Chien

from requests import get
from bs4 import BeautifulSoup as bs
from time import sleep
from argparse import ArgumentParser
from datetime import datetime, timedelta
from subprocess import check_output
from random import randint
import json
import re

def guard(begin, end):
    content = []
    while begin < end:
        b = bs(get(begin.strftime('https://www.theguardian.com/business/%Y/%b/%d/all')).text, 'lxml')
        for i in b.findAll('a', {'class': 'js-headline-text'}):
            try:
                news, record = bs(get(i['href']).text, 'lxml'), {}
                record['time'] = int(news.find('time')['data-timestamp'][:-3])
                if record['time'] > end.timestamp():
                    continue
                record['src'] = 'guardian'
                record['url'] = i['href']
                record['title'] = news.find('h1').text.strip()
                record['content'] = ' '.join(j.text for j in news.find('div', {'itemprop': 'articleBody'}).findAll('p'))
                content.append(record)
                sleep(1)
            except:
                pass
        begin += timedelta(1)
    print(json.dumps(content, ensure_ascii=False))

def nyt(begin, end):
    content = []
    while begin < end:
        b = bs(check_output(begin.strftime('w3m -dump_source https://www.nytimes.com/issue/todayspaper/%Y/%m/%d/todays-new-york-times | zcat'), shell=True), 'lxml')
        for i in b.findAll('section',{'class':'css-u82chm ebkl1p30'})[6].findAll('a')[1:]: # Business Day part
            try:
                news, record = bs(get('https://www.nytimes.com' + i['href']).text, 'lxml'), {}
                record['time'] = datetime.strptime(news.find('time')['datetime'], '%Y-%m-%d').timestamp()
                if record['time'] > end.timestamp():
                    continue
                record['src'] = 'nyt'
                record['url'] = 'https://www.nytimes.com' + i['href']
                record['title'] = news.find('h1').text.strip()
                record['content'] = ' '.join(j.text for j in news.findAll('p',{'class':'css-exrw3m evys1bk0'}))
                content.append(record)
                sleep(1)
            except:
                pass
        begin += timedelta(1)
    print(json.dumps(content, ensure_ascii=False))

def wsj(begin, end):
    content = []
    while begin < end:
        while True:
            b = bs(check_output(begin.strftime('w3m -dump_source https://www.wsj.com/print-edition/%Y%m%d/business'), shell=True), 'lxml')
            if b.findAll('div', class_='WSJTheme--list-item--1sRYOAZ-'):
                break
            else:
                sleep(randint(5, 10))
        for i in b.findAll('div', class_='WSJTheme--list-item--1sRYOAZ-'):
            try:
                i = i.find('a')
                i['href'] = re.sub('\?.*', '?mod=rsswn', i['href'])
                news, record = bs(check_output('w3m -dump_source ' + i['href'], shell=True), 'lxml'), {}
                record['time'] = int(datetime.strptime(re.sub('Updated', '', news.find('time').text).strip(), '%b. %d, %Y %H:%M %p ET').timestamp())
                if record['time'] > end.timestamp():
                    continue
                record['src'] = 'wsj'
                record['url'] = i['href']
                record['title'] = news.find('h1').text.strip()
                record['content'] = ' '.join(re.sub('\n', '', i.text).strip() for i in news.find('div', class_='article-content').findAll('p')[:-2])
                content.append(record)
                sleep(3)
            except:
                pass
        begin += timedelta(1)
    print(json.dumps(content, ensure_ascii=False))

parser = ArgumentParser(description='Return all news from SRC(s) from Unix time BEGIN to END.')
parser.add_argument('-s', '--source', type=str, metavar='SRC', nargs='+',
        choices=['guard', 'wsj', 'nyt'], help='One of guard, wsj, or nyt', required=True)
parser.add_argument('-f', '--from', dest='begin', type=int, metavar='BEGIN',
        help='Beginning timestamp of time span', required=True)
parser.add_argument('-t', '--to', dest='end', type=int, metavar='END',
        help='Ending timestamp of time span', required=True)
args = parser.parse_args()

begin = datetime.fromtimestamp(args.begin)
end = datetime.fromtimestamp(args.end)

for i in args.source:
    locals().get(i, lambda x, y: None)(begin, end)
