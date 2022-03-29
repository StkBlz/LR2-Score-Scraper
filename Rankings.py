from flask import Response
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import urllib.request, json 

class Rankings:
    def __init__(self):
        self.title = ''
        self.df = {}
        self.plot = ''

    # Dataframe from md5 
    def createDf(self, md5):
        #parse html
        response = requests.get('http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&bmsmd5={}'.format(md5) )
        response.encoding = 'SHIFT-JIS'
        soup = BeautifulSoup(response.content, 'html.parser')

        #title
        self.title = soup.select('h1')[0].text

        #df
        table = soup.findAll('table')
        table = table[-1]

        records = []
        columns = []
        for tr in table.findAll("tr"):
            ths = tr.findAll("th")
            if ths != []:
                for each in ths:
                    columns.append(each.text)
            else:
                trs = tr.findAll("td")
                record = []
                for each in trs:
                    try:
                        text = each.text
                        record.append(text)
                    except:
                        text = each.text
                        record.append(text)
                records.append(record)

        self.df = pd.DataFrame(data=records, columns = columns).dropna()
        self.df.rename(columns={'順位':'#', 'プレイヤー': 'PLAYER', '段位':'GRADE', 'クリア':'CLEAR TYPE', 'ランク':'RANK', 'スコア':'SCORE', 'コンボ':'COMBO'},inplace=True)
        self.plot = self.plotFigure()
        self.df.drop(['score','本体'],axis=1, inplace=True)

    # Dataframe from searching
    def createSearchDf(self, search):
        url = 'http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=search&keyword={}&sort=playcount_desc'.format(search.replace(' ','%20'))
        response = requests.get(url)
        response.encoding = 'SHIFT-JIS'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        records = []
        columns = []
        for tr in table.findAll("tr"):
            ths = tr.findAll("th")
            if ths != []:
                for each in ths:
                    columns.append(each.text)
            else:
                trs = tr.findAll("td")
                record = []
                for each in trs:
                    try:
                        link = each.find('a')['href']
                        text = each.text
                        record.append(link)
                        record.append(text)
                    except:
                        text = each.text
                        record.append(text)
                records.append(record)
        columns.insert(1, 'CHART')

        self.df = pd.DataFrame(data=records, columns = columns)
        self.df['CHART'] = self.df['CHART'].replace({'\D+':''}, regex = True)
        #self.df.drop(['プレイ人数', 'クリア人数', 'プレイ回数', '平均プレイ回数'],axis=1, inplace=True)
        self.df = self.df[['ジャンル', 'タイトル', 'CHART', 'アーティスト']]
        self.df.rename(columns={'ジャンル':'GENRE', 'タイトル':'TITLE','アーティスト':'ARTIST'},inplace=True)


    # Plot figure, ret: base64 encoded png
    def plotFigure(self):
        fontprop = FontProperties(fname='.fonts/MSGothic.ttf', size=10)
        fig, ax = plt.subplots(figsize=(12,4))

        #plt.title('Top 25', fontsize=25, font_properties=fontprop)
        plt.xticks(fontsize=15,font_properties=fontprop)
        #plt.xlabel(fontsize=15,xlabel='Player', font_properties=fontprop)
        plt.ylabel(fontsize=15, ylabel='Score', font_properties=fontprop)
        fig.autofmt_xdate(rotation=45)
        plt.tight_layout()
        fig.subplots_adjust(bottom=0.3)


        self.df['score'] = self.df['SCORE'].replace({'/.+':''}, regex=True).astype(int)

        x = self.df.nlargest(25,'score').PLAYER
        y = self.df.nlargest(25,'score').score
        ax.bar(x, y)

        img = io.BytesIO()
        FigureCanvas(fig).print_png(img)
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')
    
    

'''
rank = Rankings()
rank.getTable('https://stellabms.xyz/sl/score.json')'''