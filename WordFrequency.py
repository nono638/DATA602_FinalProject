import pandas as pd

WordFreqPath = "Data Sources/unigram_freq.csv"
WordFreq = pd.read_csv(WordFreqPath)
WordFreq.rename(columns={'word':"Word"}, inplace= True)


if __name__ == '__main__':
    print(WordFreq.head())
    print("{:,}".format(len(WordFreq)) )
