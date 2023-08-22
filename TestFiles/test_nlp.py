import nltk
from nltk.stem import WordNetLemmatizer

def lemmatize_word(word):
    # 初始化WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # 进行词形还原
    lemma_word = lemmatizer.lemmatize(word)

    return lemma_word

# 示例单词
word = "running"

# 将单词改为原形
lemma_word = lemmatize_word(word)

# 输出结果
print("原始单词：", word)
print("原形单词：", lemma_word)
