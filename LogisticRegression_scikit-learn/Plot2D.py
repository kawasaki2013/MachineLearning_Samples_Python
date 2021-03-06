# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy
from matplotlib.colors import ListedColormap


class Plot2D(object):
    """
    ２次元の図を描写をサポートする関数群からなるクラス
    """
    
    def __init__( self ):
        self.mainTitle = "mainTitle"

    def drawDiscriminantRegions( dat_X, dat_y, classifier, list_test_idx=None, resolusion= 0.02 ):
        """ 識別器 [classifier] による識別領域を色分けで描写する """
        
        plt.clf()    # 現在の図をクリア

        # 識別クラス数に対応したMAPの作成（最大５クラス対応）
        tuple_makers = ( "s","x","+","^","v" )                          # タプル（定数リスト）
        tuple_colors = ( "red","blue","lightgreen", "gray", "cyan" )    # 塗りつぶす色を表すタプル（定数リスト）
        numClass = len( numpy.unique(dat_y) )                           # numpy.unique() : 指定したarray変数の要素の重複をなくしたものを返す,更にlen() でユニークな値の数取得
        cmap = ListedColormap( tuple_colors[0:numClass] )               # plt.scatter() の引数で使用

        # plot the decision surface
        x1_min = dat_X[:, 0].min() - 1
        x1_max = dat_X[:, 0].max() + 1
        x2_min = dat_X[:, 1].min() - 1
        x2_max = dat_X[:, 1].max() + 1

        meshgrids = numpy.meshgrid(                                     # マス目を作る ( 戻り値:numpy.ndarray )
                        numpy.arange( x1_min, x1_max, resolusion ),     # numpy.arang(): min~max by resolution
                        numpy.arange( x2_min, x2_max, resolusion )
                    )
        # 入力データ datX のx1軸、x2軸の値の全ての組み合わせ
        xx1 = meshgrids[0]
        xx2 = meshgrids[1]

        # ? 値の全ての組み合わせを１次元配列に変換 numpy.array( [xx1.ravel(), xx2.ravel()] ) し、
        # classifierに設定されている predict（予想）を実行
        Z = classifier.predict( 
                numpy.array( [xx1.ravel(), xx2.ravel()] ).T
            )
        # ? 予測結果を元のグリッドポイントサイズに変換
        Z = Z.reshape( xx1.shape )  # numpy.ndarray の属性 shape は，各次元ごとの配列の大きさをまとめたタプルで指定

        # 等高線plotで識別領域を塗りつぶす
        plt.contourf( xx1, xx2, Z, alpha=0.4, cmap=cmap )

        # 図の軸の範囲指定
        plt.xlim( xx1.min(), xx1.max() )
        plt.ylim( xx2.min(), xx2.max() )

        # 識別クラス毎に、入力データ dat_X, dat_y の散布図 plot
        for (idx, cl) in enumerate( numpy.unique(dat_y) ): # enumerate():idx と共に clもloop
            plt.scatter(
                x = dat_X[dat_y == cl, 0], 
                y = dat_X[dat_y == cl, 1],
                alpha = 0.8, 
                c = cmap(idx),
                edgecolor = 'black',
                marker = tuple_makers[idx],
                label = cl
            )

        # テスト用サンプルデータを強調表示
        if (list_test_idx != None):
            X_test = dat_X[list_test_idx, :]
            y_test = dat_y[list_test_idx]
            plt.scatter(
                X_test[:, 0], X_test[:, 1],
                c='',
                alpha=1.0,
                edgecolor='black',
                linewidths=1,
                marker='o',
                s=55, 
                label='test set'
            )

        plt.tight_layout()

        return
