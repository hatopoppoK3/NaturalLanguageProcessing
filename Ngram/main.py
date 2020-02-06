import MeCab

tagger = MeCab.Tagger('-Owakati')


def simple_ngram(N, string):
    gram = []
    if N == 1:
        for i in range(0, len(string)):
            gram.append(string[i])
    else:
        for i in range(N, len(string)):
            gram.append(string[i-N:i+1])
    return gram


def word_ngram(N, string):
    word_list = tagger.parse(string).split(' ')
    gram = []
    if N == 1:
        gram = word_list
    else:
        for i in range(N, len(word_list)):
            gram.append(''.join((word_list[i-N:i])))
    return gram


if __name__ == '__main__':
    N = int(input())
    string = str(input())
    gram = word_ngram(N, string)
    print(*gram, sep=',')
