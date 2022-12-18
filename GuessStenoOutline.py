class stenoObject:
    def __init__(self, df, row):
        self.numStrokes = len.iloc[row]['strokes']
        self.numSyllables =  len.iloc[row]['syllables']


def GuessForOneStrokeTooFew(df):
    if "syllables" not in df.columns.tolist():
        return df
    else:
        pass
