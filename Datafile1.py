class datavalidation():
    
    def QualQuan():
        qual=[]
        quan=[]
        for columnName in dataset.columns:
            if (dataset[columnName].dtype=='O'):
                qual.append(columnName)
            else:
                quan.append(columnName)
        return qual,quan
            
    qual,quan=QualQuan()
        
   
    
    def descriptive():
        descriptive=pd.DataFrame(columns=quan,index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","90%","Q4:100%","IQR","1.5Rule",
                                                     "LesserOutlier","GreaterOutlier","Min","Max"])
        for columnName in quan:
            descriptive[columnName]["Mean"]=dataset[columnName].mean()
            descriptive[columnName]["Median"]=dataset[columnName].median()
            descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["90%"]=np.percentile(dataset[columnName],90)
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5Rule"]=1.5*(descriptive[columnName]["IQR"])
            descriptive[columnName]["LesserOutlier"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5Rule"]
            descriptive[columnName]["GreaterOutlier"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5Rule"]
        return descriptive
        
    descriptive=descriptive()

    def Outliers():
        Outliers=[]
        for columnName in quan:
            if descriptive[columnName]["Min"]<descriptive[columnName]["LesserOutlier"]:
                print("Outliers")
                Outliers.append(columnName)
            if descriptive[columnName]["Max"]>descriptive[columnName]["GreaterOutlier"]:
                Outliers.append(columnName)
        return Outliers
    
    Outliers=Outliers() 

    def replaces():
        for columnName in Outliers:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["LesserOutlier"]]=descriptive[columnName]["LesserOutlier"]
            dataset[columnName][dataset[columnName]>descriptive[columnName]["GreaterOutlier"]]=descriptive[columnName]["GreaterOutlier"]
        return replaces
        
    replaces=replaces()

    def freqTable(columnName,dataset):
        freqTable=pd.DataFrame(columns=["Unique_Value","Frequency","Relative_Frequency","Cumsum"])
        freqTable["Unique_Value"]=dataset[columnName].value_counts().index
        freqTable["Frequency"]=dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"]=freqTable["Frequency"]/103
        freqTable["Cumsum"]=freqTable["Relative_Frequency"].cumsum()
        return freqTable