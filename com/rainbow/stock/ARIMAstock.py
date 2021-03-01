import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import configparser
import os
import codecs
import logging
class ARIMA:
    def __init__(self,path):
        self.path=path
        root_dir = os.path.dirname(os.path.abspath('.'))
        cf = configparser.ConfigParser()
        cf.readfp(codecs.open(root_dir + "\\"+self.path+"\\config.ini", "r", "utf-8-sig"))
        self.user_token = cf.get("ARIMA", "user_token")
        self.ts_code = cf.get("ARIMA", "ts_code")
        self.start_date = cf.get("ARIMA", "start_date")
        self.train_date = cf.get("ARIMA", "train_date")
        self.savepath = cf.get("ARIMA", "csvpath")+"\\"+self.ts_code+"\\"
        self.diffNum = float(cf.get("ARIMA", "diffNum"))
        self.p = int(cf.get("ARIMA", "p"))
        self.d = int(cf.get("ARIMA", "d"))
        self.q = int(cf.get("ARIMA", "q"))
        falg = os.path.exists(self.savepath)
        if (falg == False):
            try:
                os.makedirs(self.savepath)
                print("创建根目录成功，根目录：" + self.savepath)
            except:
                print("创建文件夹失败，根目录已存在")


    def main(self):
        sns.set_style("whitegrid",{"font.sans-serif":['KaiTi', 'Arial']})
        ts.set_token(self.user_token)
        pro = ts.pro_api()
        data=pro.query('daily', ts_code=self.ts_code, start_date=self.start_date)
        data.to_csv(self.savepath+self.ts_code+'.csv')
        f = open(self.savepath+self.ts_code+'.csv')
        df=pd.read_csv(f,index_col=2,parse_dates=[2])
        df.index=pd.to_datetime(df.index)

        stock_week=df['close'].resample('W-TUE').mean()
        stock_train=stock_week['2017':'2021'].dropna()
        stock_train.plot(figsize=(12,8))
        plt.title('股市每日收盘价')
        sns.despine()
        plt.savefig(self.savepath +self.ts_code + '_close.png')

        stock_diff=stock_train.diff(self.diffNum).dropna() #对数据进行差分，目的使数据平缓,满足平稳性的要求
        plt.figure()
        plt.plot(stock_diff)
        plt.title(str(self.diffNum)+'阶差分')
        plt.savefig(self.savepath + self.ts_code + '_diff.png')

        from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
        acf=plot_acf(stock_diff,lags=20)
        plt.title('ACF')
        plt.plot(str(acf))
        plt.savefig(self.savepath + self.ts_code + '_ACF.png')

        pacf=plot_pacf(stock_diff,lags=20)
        plt.title('PACF')
        plt.plot(str(pacf))
        plt.savefig(self.savepath + self.ts_code + '_PACF.png')


        from statsmodels.tsa.arima_model import ARIMA
        model=ARIMA(stock_train,order=(self.p,self.d,self.q),freq='W-TUE')#训练模型,order表示（p,d,q）
        result=model.fit()
        pred=result.predict(self.train_date,dynamic=True,typ='levels')

        plt.figure(figsize=(6,6))
        plt.xticks(rotation=45)
        plt.title('股票价格预测')
        plt.plot(pred)
        plt.plot(stock_train)
        plt.savefig(self.savepath + self.ts_code + '_价格预测.png')

if __name__=="__main__":
    ARIMA("stock").main()