# analysis-news

## TODO

1. 文字雲
1. 情感分析（？）（政治分類）
1. 時間分析
1. 統計分析
1. 詞性分析
1. 作者分析
1. 視覺化結果

## Pre request

1. pip

```bash
pip install -U ckiptagger

# tensorflow
pip install -U tf
```

1. Download tensorflow model files

select one

```url
http://ckip.iis.sinica.edu.tw/data/ckiptagger/data.zip
https://drive.google.com/drive/folders/105IKCb88evUyLKlLondvDBoh7Dy_I1tm
https://drive.google.com/drive/folders/15BDjL2IaX3eYdFVzT422VwCb743Hrbi3
```

## Usage

```bash
# 啟動 app
python app.py
```

```bash
# 分析結果
# 五分鐘內的單詞出現次數
python bash.py pos5

# 五分鐘內的實體出現次數
python bash.py ner5

# 一小時內的實體出現次數
python bash.py ner60

# 二十四內的實體出現次數
python bash.py ner24
```

## 參考資料

-----相關套件-----

[jieba](https://github.com/fxsjy/jieba)

[HanLP](https://github.com/hankcs/HanLP)

[snownlp](https://github.com/isnowfy/snownlp)


### CKIP Lab

https://ckip.iis.sinica.edu.tw/resource

[ckiptagger](https://github.com/ckiplab/ckiptagger)

[ckip-transformers](https://github.com/ckiplab/ckip-transformers)

[ckipnlp](https://github.com/ckiplab/ckipnlp)

----相關文章-----

[以 jieba 與 gensim 探索文本主題：五月天人生無限公司歌詞分析 ( I )](https://medium.com/pyladies-taiwan/%E4%BB%A5-jieba-%E8%88%87-gensim-%E6%8E%A2%E7%B4%A2%E6%96%87%E6%9C%AC%E4%B8%BB%E9%A1%8C-%E4%BA%94%E6%9C%88%E5%A4%A9%E4%BA%BA%E7%94%9F%E7%84%A1%E9%99%90%E5%85%AC%E5%8F%B8%E6%AD%8C%E8%A9%9E%E5%88%86%E6%9E%90-i-cd2147b89083)

[如何用Python做情感分析？](https://bookdown.org/wshuyi/dive-into-data-science-practically/nlp-in-python.html)

[【不是工程師，也可以作文本分析】用 R 與 Python 語言，七步驟解決文本挖掘的一切痛苦](https://buzzorange.com/techorange/2017/03/03/rmakeyoueasy/)

[Day 06 - 用中研院 CKIP Transformers 做中文斷詞，台灣國語不再結巴 - 親手打造推薦系統](https://ithelp.ithome.com.tw/articles/10295882)
