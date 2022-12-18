import pandas as pd

import  PreProcessEclipse
import PreprocessCaseCat
import re
DataFolder = 'Data Sources/'

NoahPath = DataFolder + "NCollinDict1.txt"
ChrisPath = DataFolder +"Personal Dictionary_D_1.rtf"
FrancenePath = DataFolder +"sunny_D_1.rtf"

#Make NoahDF
NoahDF = PreProcessEclipse.MakeBasicStenoDataFrame(PreProcessEclipse.ProcessTextFile(NoahPath)) #?Two different function names for Eclipse and Case, possibly the same functionality though.
#NoahDF = PreProcessEclipse.AddStrokesColumn(NoahDF)

#ChrisDF
ChrisDF = PreprocessCaseCat.MakeStenoDf( PreprocessCaseCat.HandleRTF(ChrisPath) )

#Francene
FranceneDF = PreprocessCaseCat.MakeStenoDf(PreprocessCaseCat.HandleRTF(FrancenePath))

NoahReady1 = pd.read_csv('Data Sources/NoahReady1.csv' , low_memory=False )
if __name__ == '__main__':
    print()
    print(NoahDF.head())
    print()
    print(ChrisDF.head(22))