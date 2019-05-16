import pandas as pd
import numpy as np
import datetime
import math
import os
import matplotlib.pyplot as plt
from pylab import rcParams
plt.style.use('ggplot')

"""
How to use

plot.figplot( x=[0, 1, 2, 3, 4, 5], y=[0, 1, 2, 3, 4, 5],\
             x_name='x_name',y_name='y_name',title='title',size1= 60, size2=50, fontsize=70, y_range_min=12,y_range_max=12)

"""



class PSO_plot:

    def __init__(self):
        self.x= np.array([ 0, 1, 2, 3, 4, 5])
        self.y= np.array([ 0, 1, 2, 3, 4, 5])
        self.x_name="X name"
        self.y_name="Y name"
        self.title="title"
        self.size1=10
        self.size2=10
        self.fontsize=10
        self.y_range_min=0
        self.y_range_m1x=100
        self.subplot1=2
        self.subplot2=2
        self.subplot3=2
        print('Please input values as follow.')
        print('figplot(x,y,x_name,y_name,title,size1,size2,fontsize,grid,y_range_min, y_range_max,subplot1,subplot2,subplot3)')
        print('figplot(x,y1,y2,x_name,y1_name,y2_name,title,size1,size2,fontsize,y_range_min, y_range_max,subplot1,subplot2,subplot3)')
        print(vars(self))

    def explanation(self):
        print('Please input values as follow.')
        print('figplot(x,y,x_name,y_name,title,size1,size2,fontsize,grid,y_range_min, y_range_max,subplot1,subplot2,subplot3)')
        print('figplot(x,y1,y2,x_name,y1_name,y2_name,title,size1,size2,fontsize,y_range_min, y_range_max,subplot1,subplot2,subplot3)')
        print(vars(self))

    def figplot(self,x,y,x_name,y_name,title,size1,size2,fontsize,y_range_min, y_range_max,subplot1,subplot2,subplot3):

        rcParams['figure.figsize'] = size1,size2
        plt.rcParams["font.size"] = fontsize

        fig = plt.figure()
        ax1 = fig.add_subplot(subplot1,subplot2,subplot3)
        ax1.plot(x, y, color='Black',linestyle='solid', linewidth = 2, label=y_name)
        ax1.set_ylim([y_range_min, y_range_max])
        ax1.set_title(title)
        ax1.set_xlabel(x_name)
        ax1.set_ylabel(y_name)
        ax1.set_xticklabels(x,rotation=0, size="small")
        # 軸目盛の設定
        plt.grid(which='major', color='black',linestyle='--')
        # 軸目盛ラベルの回転
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=0);

        plt.legend(title="LABEL NAME")
        plt.figure(dpi=400)
        plt.tight_layout(False)

    def figplot2(self,x,y1,y2,x_name,y1_name,y2_name,title,size1,size2,fontsize,y_range_min, y_range_max,subplot1,subplot2,subplot3):

        rcParams['figure.figsize'] = size1,size2
        plt.rcParams["font.size"] = fontsize

        fig = plt.figure()
        ax1 = fig.add_subplot(subplot1,subplot2,subplot3)
        ax1.plot(x, y1, color='Black',linestyle='solid', linewidth = 2, label=y1_name)
        ax1.plot(x, y2, color='red',linestyle='--', linewidth = 2, label=y2_name)
        ax1.set_ylim([y_range_min, y_range_max])
        ax1.set_title(title)
        ax1.set_xlabel(x_name)
        ax1.set_ylabel(y1_name)
        ax1.set_xticklabels(x,rotation=0, size="small")
        # 軸目盛の設定
        plt.grid(which='major', color='black',linestyle='--')
        # 軸目盛ラベルの回転
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=90);

        plt.legend(title="LABEL NAME")
        plt.figure(dpi=400)
        plt.tight_layout()


    def easyplot(self,x,y):
        # プロット
        plt.plot(x, y, label="test")

        # 凡例の表示
        plt.legend()

        # プロット表示(設定の反映)
        plt.show()
