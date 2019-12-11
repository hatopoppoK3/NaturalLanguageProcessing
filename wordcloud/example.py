import codecs
import matplotlib.pyplot as plt
import MeCab
from wordcloud import WordCloud

tagger = MeCab.Tagger('-Owakati')
text = '今日はいい天気ですね'
result = tagger.parse(text)
print(result)

tagger = MeCab.Tagger('-Ochasen')
result = tagger.parse(text)
print(result)

node = tagger.parseToNode(text)
while node:
    surface = node.surface
    feature = node.feature
    print(surface)
    print(feature)
    print('-'*20)
    node = node.next

word_list = []
with codecs.open('wordcloud/rashomon.txt', 'r', encoding='shift-jis') as fp:
    tagger = MeCab.Tagger('-Ochasen')
    for text_line in fp:
        node = tagger.parseToNode(text_line)
        while node:
            if node.feature.split(',')[0] == '名詞':
                word_list.append(node.surface)
            node = node.next

input_texts = ' '.join(word_list)

wordcloud = WordCloud(
    font_path='/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
    width=900, height=600,
    background_color="white",
    max_words=500,
    min_font_size=4,
    collocations=False
).generate(input_texts)
plt.figure(figsize=(15, 12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
