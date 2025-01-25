class datavalidation():
    import pandas as pd
    import numpy as np
    def quanQual(dataset):
            quan=[]
            qual=[]
            for columnname in dataset.columns:
                if(dataset[columnname].dtype=='O'):
                    qual.append(columnname)
                else:
                    quan.append(columnname)       
            return quan,qual     
        

    def descriptive(dataset, quan):
        import pandas as pd
        import numpy as np
        # Create an empty DataFrame with specified rows (index) and columns
        descriptive = pd.DataFrame(index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "90%", "Q4:100%", 
                                          "IQR", "1.5Rule", "LesserOutlier", "GreaterOutlier", "Min", "Max"], 
                                   columns=quan)
        
        # Precompute dataset.describe() to avoid redundant calculations
        summary = dataset[quan].describe()
        
        for columnName in quan:
            # Compute descriptive statistics
            descriptive.loc["Mean", columnName] = dataset[columnName].mean()
            descriptive.loc["Median", columnName] = dataset[columnName].median()
            descriptive.loc["Mode", columnName] = dataset[columnName].mode().iloc[0]  # Safely get the first mode
            descriptive.loc["Q1:25%", columnName] = summary.at["25%", columnName]
            descriptive.loc["Q2:50%", columnName] = summary.at["50%", columnName]
            descriptive.loc["Q3:75%", columnName] = summary.at["75%", columnName]
            descriptive.loc["90%", columnName] = np.percentile(dataset[columnName], 90)
            descriptive.loc["Q4:100%", columnName] = summary.at["max", columnName]
            descriptive.loc["Min", columnName] = dataset[columnName].min()
            descriptive.loc["Max", columnName] = dataset[columnName].max()
            
            # Compute IQR and outlier thresholds
            IQR = descriptive.loc["Q3:75%", columnName] - descriptive.loc["Q1:25%", columnName]
            descriptive.loc["IQR", columnName] = IQR
            descriptive.loc["1.5Rule", columnName] = 1.5 * IQR
            descriptive.loc["LesserOutlier", columnName] = descriptive.loc["Q1:25%", columnName] - descriptive.loc["1.5Rule", columnName]
            descriptive.loc["GreaterOutlier", columnName] = descriptive.loc["Q3:75%", columnName] + descriptive.loc["1.5Rule", columnName]
        
        return descriptive
        
    def Outliers(quan,descriptive):
        Outliers=[]
        for columnName in quan:
            LesserOutlier=descriptive[columnName]["LesserOutlier"]
            GreaterOutlier=descriptive[columnName]["GreaterOutlier"]
            #if descriptive[columnName]["Min"]<descriptive[columnName]["LesserOutlier"]:
            if descriptive[columnName]["Min"]<LesserOutlier:
                print("Outliers")
                Outliers.append(columnName)
            #if descriptive[columnName]["Max"]>descriptive[columnName]["GreaterOutlier"]:
            if descriptive[columnName]["Max"]>GreaterOutlier:
                Outliers.append(columnName)
        return Outliers


    
     

    def replaces(dataset,descriptive,Outliers):
        for columnName in Outliers:
            LesserOutlier=descriptive[columnName]["LesserOutlier"]
            GreaterOutlier=descriptive[columnName]["GreaterOutlier"]
            #dataset[columnName][dataset[columnName]<descriptive[columnName]["LesserOutlier"]]=descriptive[columnName]["LesserOutlier"]
            #dataset[columnName][dataset[columnName]<LesserOutlier]=LesserOutlier
            dataset.loc[dataset[columnName] < LesserOutlier, columnName] = LesserOutlier
            #dataset[columnName][dataset[columnName]>descriptive[columnName]["GreaterOutlier"]]=descriptive[columnName]["GreaterOutlier"]
            #dataset[columnName][dataset[columnName]>GreaterOutlier]=GreaterOutlier                 
            dataset.loc[dataset[columnName] > GreaterOutlier, columnName] = GreaterOutlier
        return replaces()


        
  

    def freqTable(columnName,dataset):
        freqTable=pd.DataFrame(columns=["Unique_Value","Frequency","Relative_Frequency","Cumsum"])
        freqTable["Unique_Value"]=dataset[columnName].value_counts().index
        freqTable["Frequency"]=dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"]=freqTable["Frequency"]/103
        freqTable["Cumsum"]=freqTable["Relative_Frequency"].cumsum()
        return freqTable