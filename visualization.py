#import matplotlib.pyplot as plt
#import seaborn as sns
from model import current_developers

def solved_defects(dataframe):
    return dataframe['Developer'][dataframe['Developer'].isin(current_developers)]
    
    