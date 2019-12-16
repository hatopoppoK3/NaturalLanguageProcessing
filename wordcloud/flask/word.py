import MeCab
from wordcloud import WordCloud


def create_cloud(texts, language):
    word_list = []
    if language == 'Japanese':
        tagger = MeCab.Tagger('-Ochasen')
        texts_line = texts.split('\n')
        for text in texts_line:
            node = tagger.parseToNode(text)
            while node:
                if node.feature.split(',')[0] == '名詞':
                    word_list.append(node.surface)
                node = node.next
    else:
        word_list.extend(texts.split(' '))
    input_texts = ' '.join(word_list)
    output_image = WordCloud(
        font_path='/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
        background_color="white",
        width=900, height=900,
        max_words=500,
        min_font_size=4,
        collocations=False
    ).generate(input_texts)
    output_image.to_file('./static/image/wordcloud.png')
