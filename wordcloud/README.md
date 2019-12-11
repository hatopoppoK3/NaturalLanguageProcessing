# WordCloud
## 目的
---
日本語の文章を形態素解析してそれをWordCloudの形で表示する。今回は芥川龍之介の「羅生門」について行ってみる。
## 準備
---
- MeCabなどのPythonのライブラリのインストール  
  `pip install mecab-python3 matplotlib codecs wordcloud`
- WordCloud作成時に使用する日本語fontのインストール  
  `sudo apt-get install fonts-ipafont-gothic`
- 青空文庫から「羅生門」を拾ってくる  ]
  `wget https://www.aozora.gr.jp/cards/000879/files/127_ruby_150.zip`
  `unzip 127_ruby_150.zip`
## コードについて
---
MeCabについてはこちらのサイトでお願いします。[](http://taku910.github.io/mecab/)  
羅生門についてはテキストを読み込み、それを1行ずつ形態素解析を行い、その単語が名詞である場合はリストに追加する。その後に、取得した名詞を' '.join(list)でstr型に変換し、WordCloudに渡す。それによって、WordCloudが生成され、matplotlibで出力をしたものである。
