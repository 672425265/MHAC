from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class txt_to_input(object):
    def __init__(self):
        self.dir = 'data_restaurant/'

    def convert_text_to_input(self, name=""):
        text_file = self.dir + name + "_text_token.txt"
        input_text_file = self.dir + name + "_text_input.txt"
        sen_max_length = -100

        rf = open(text_file, 'r')
        wf = open(input_text_file, 'w')
        while True:
            line = rf.readline()
            if line == "":
                break
            line = line.lower()
            line = line.replace("\n", "")
            line = line.replace('n\'t', 'not')
            line = line.replace('\'ve', 'have')
            line = line.replace('\'ll', 'will')
            line = line.replace('\'re', 'are')
            line = line.replace('\'m', 'am')
            line = line.replace('/', ' / ')
            line = line.replace('-', ' ')
            line = line.replace('!', ' ')
            line = line.replace('?', ' ')
            line = line.replace('+', ' ')
            line = line.replace('*', ' ')
            while "  " in line:
                line = line.replace('  ', ' ')
            while ",," in line:
                line = line.replace(',,', ',')
            line = line.strip()
            line = line.strip('.')
            line = line.strip()
            temp = line.count(' ') + 1
            if temp > sen_max_length:
                sen_max_length = temp
            wf.write(line + "\n")
        wf.close()
        rf.close()

        return sen_max_length

    def convert_aspect_to_input(self, name='', tk=None):
        aspect_text_file = self.dir + name + "_aspects_text_token.txt"
        aspect_text_index_file = self.dir + name + "_aspects_text_index.txt"
        aspect_text_input_file = self.dir + name + "_aspects_text_input.txt"

        aspect_max_length = -1

        aspect_texts = []
        rf = open(aspect_text_file, 'r')
        wf = open(aspect_text_input_file, 'w')
        while True:
            line = rf.readline()
            if line == "":
                break
            line = line.lower()
            line = line.replace("\n", "")
            line = line.replace('n\'t', 'not')
            line = line.replace('\'ve', 'have')
            line = line.replace('\'ll', 'will')
            line = line.replace('\'re', 'are')
            line = line.replace('\'m', 'am')
            line = line.replace('/', ' / ')
            line = line.replace('-', ' ')
            line = line.replace('!', ' ')
            line = line.replace('?', ' ')
            line = line.replace('+', ' ')
            line = line.replace('*', ' ')
            while "  " in line:
                line = line.replace('  ', ' ')
            while ",," in line:
                line = line.replace(',,', ',')
            line = line.strip()
            line = line.strip('.')
            line = line.strip()
            temp = line.count(' ') + 1
            if temp > aspect_max_length:
                aspect_max_length = temp
            wf.write(line + "\n")
            aspect_texts.append(line)
        rf.close()
        wf.close()
        aspect_texts = tk.texts_to_sequences(aspect_texts)
        self.write_index_to_file(inputs=aspect_texts, file=aspect_text_index_file)
        print("max length of aspect is " + str(aspect_max_length))
        return aspect_texts

    def convert_aspect_to_label(self, name='', class_ids={}, sentences=[]):
        ###not only gain aspect label, but also get sentence inputs
        aspect_label_file = self.dir + name + "_aspects_label.txt"
        aspect_label_index_file = self.dir + name + "_aspects_label_index.txt"
        text_index_file = self.dir + name + "_text_index.txt"
        rf = open(aspect_label_file, 'r')
        wf = open(aspect_label_index_file, 'w')

        labels = []
        sen_inputs = []
        while True:
            line = rf.readline()
            if line == "":
                break
            line = line.split("#")
            label = class_ids[line[0]]
            wf.write(str(label) + "\n")
            line_index = int(line[1])
            labels.append(label)
            sen_inputs.append(sentences[line_index])
        rf.close()
        wf.close()
        self.write_index_to_file(inputs=sen_inputs, file=text_index_file)
        return labels

    def read_text_file(self, name):
        input_text_file = self.dir + name + "_text_input.txt"
        rf = open(input_text_file, 'r')
        inputs = []
        while True:
            line = rf.readline()
            line = line.replace("\n", "")
            line.strip()
            if line == "":
                break
            inputs.append(line)
        rf.close()
        return inputs

    @staticmethod
    def convert_input_to_index(train_inputs=[], test_inputs=[], max_sen_length=100):
        print("start convert text to index.")
        tk = Tokenizer(num_words=10000, filters="", split=" ")
        tk.fit_on_texts(train_inputs)
        tk.fit_on_texts(test_inputs)
        train_text_inputs = tk.texts_to_sequences(train_inputs)
        test_text_inputs = tk.texts_to_sequences(test_inputs)
        train_text_inputs = pad_sequences(train_text_inputs, maxlen=max_sen_length, padding='post')
        test_text_inputs = pad_sequences(test_text_inputs, maxlen=max_sen_length, padding='post')
        return train_text_inputs, test_text_inputs, tk

    @staticmethod
    def write_index_to_file(inputs=[], file=''):
        wf = open(file, 'w')
        for line in inputs:
            for index in line:
                wf.write(str(index) + " ")
            wf.write("\n")
        wf.close()

    def write_word_index(self, word_index={}):
        word_index_file = self.dir + "word_index.txt"
        wf = open(word_index_file, 'w')
        for word, index in word_index.items():
            wf.write(word + " " + str(index) + "\n")
        wf.close()

if __name__ == '__main__':
    x = txt_to_input()
    print("========== converting text to normal text ============")
    train_max = x.convert_text_to_input(name='train')
    test_max = x.convert_text_to_input(name='test')
    print("======= finish converting text to normal text ========")
    max_len = max([train_max, test_max])
    print("The max length of sentence is " + str(max_len) + ".")  # 78 // 82
    print("========== converting normal text to index ===========")
    train_sen_inputs = x.read_text_file(name='train')
    test_sen_inputs = x.read_text_file(name='test')
    train_sen_inputs, test_sen_inputs, tk = txt_to_input.convert_input_to_index(train_inputs=train_sen_inputs,
                                                                                 test_inputs=test_sen_inputs,
                                                                                 max_sen_length=max_len)
    print("====== finish converting normal text to index ========")
    x.write_word_index(word_index=tk.word_index)
    print("========== converting aspect text to index ===========")
    x.convert_aspect_to_input(name='train', tk=tk)
    x.convert_aspect_to_input(name='test', tk=tk)
    print("====== finish converting aspect text to index ========")
    ids = dict(negative=0, positive=1, neutral=2, conflict=3)  # we don't read examples of 'conflict' in example reader.
    print("========== getting sentence index input and aspect label ===========")
    x.convert_aspect_to_label(name='train', class_ids=ids, sentences=train_sen_inputs)
    x.convert_aspect_to_label(name='test', class_ids=ids, sentences=test_sen_inputs)
    print("======= finish getting sentence index input and aspect label =======")