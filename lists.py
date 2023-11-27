
import csv
import pandas as pd

def to_uppercase(items:list) -> list:
    uppercase_list = []
    for i in items:
        try:
            upper = i.upper()
            uppercase_list.append(upper)
        except AttributeError as e:
            print(f'ERROR: {i} {e}')
    
    return uppercase_list


def to_csv(data, filename, orientation='row'):
    if orientation == 'row':
        with open(filename, 'w', newline='\n') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(data)
            
    if orientation=='col':
        df = pd.DataFrame(data={"column": data})
        df.to_csv(filename, sep=',' ,index=True)
        
        
