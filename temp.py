import pandas as pd
import os
import json
result = {
    "functionName":'MAX',
    "column":'longitude'
}
id = 'california_housing.csv'
try:
    id = os.path.join('static',id)
    pd =pd.read_csv(id)
    if(result['functionName']=='MAX'):
        print(pd[result['column']].max())
    elif(result['functionName']=='MIN'):
        print(pd[result['column']].min())
    elif(result['functionName']=='SUM'):
        print(pd[result['column']].sum())
    print('scam')
except:
    print('scam')