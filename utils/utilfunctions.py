import pandas as pd

def formatseveritylist(a):
    x,y=a
    lis=[]
    lis.append(x)
    lis.append(y)
    return lis

def seggregation(a):
    x,y=a
    if(y is not None and x is not None):
        if 'policy' in y.lower() or 'stp' in x.lower() or ('policy' in x.lower() and 'claim' not in x.lower()) :
            if 'transact' in x.lower():
                return pd.Series(['TransACT','Policy'],index=['Seggregation','Application'])
            elif 'applicant' in x.lower():
                return pd.Series(['Account','Policy'],index=['Seggregation','Application'])
            elif 'skins' in x.lower() or 'align' in x.lower() or 'javascript' in x.lower() or 'ajax' in x.lower():
                return pd.Series(['Skins','Policy'],index=['Seggregation','Application'])
            elif 'premium' in x.lower() or 'pric' in x.lower() or 'rerate' in x.lower() or 're-rate' in x.lower():
                return pd.Series(['Rating','Policy'],index=['Seggregation','Application'])
            elif 'privilege' in x.lower() or 'useradmin' in x.lower() or 'roles' in x.lower() or 'entity' in x.lower():
                return pd.Series(['UserAdmin','Policy'],index=['Seggregation','Application'])
            elif 'risk' in x.lower():
                return pd.Series(['Risk','Policy'],index=['Seggregation','Application'])
            elif 'form' in x.lower() or 'doc' in x.lower():
                return pd.Series(['Forms','Policy'],index=['Seggregation','Application'])
            elif 'search' in x.lower():
                return pd.Series(['Search','Policy'],index=['Seggregation','Application'])
            elif 'rate' in x.lower() and 'table' in x.lower():
                return pd.Series(['Rate Table','Policy'],index=['Seggregation','Application'])
            elif 'shred' in x.lower():
                return pd.Series(['Shred','Policy'],index=['Seggregation','Application'])
            elif 'party' in y.lower() or 'ofac' in x.lower() or 'geo' in x.lower():
                return pd.Series(['Integration','Party'],index=['Seggregation','Application'])
            elif 'stp' in y.lower() or 'stp' in x.lower():
                return pd.Series(['STP','Policy'],index=['Seggregation','Application'])
            else:
                return pd.Series(['PolicyOther','Policy'],index=['Seggregation','Application'])
        elif 'billing' in y.lower() or 'billing' in x.lower():
            if 'invoice' in x.lower():
                return pd.Series(['Invoice','Billing'],index=['Seggregation','Application'])
            elif 'disbursement' in x.lower():
                return pd.Series(['Disbursement','Billing'],index=['Seggregation','Application'])
            elif 'payment' in x.lower() or 'transfer' in x.lower():
                return pd.Series(['Payment','Billing'],index=['Seggregation','Application'])
            elif 'schedule' in x.lower():
                return pd.Series(['ScheduleActivity','Billing'],index=['Seggregation','Application'])
            elif 'commission' in x.lower():
                return pd.Series(['Commission','Billing'],index=['Seggregation','Application'])
            elif 'pcn' in x.lower() or 'pcn' in x.lower():
                return pd.Series(['PCN','Billing'],index=['Seggregation','Application'])
            elif 'receivable' in x.lower():
                return pd.Series(['Receivable','Billing'],index=['Seggregation','Application'])
            elif 'shred' in x.lower():
                return pd.Series(['Shred','Billing'],index=['Seggregation','Application'])
            elif 'user admin' in x.lower():
                return pd.Series(['UserAdmin','Policy'],index=['Seggregation','Application'])
            elif 'reports' in x.lower() and 'billing' in y.lower():
                return pd.Series(['Reports','Billing'],index=['Seggregation','Application'])
            elif 'party' in x.lower() or 'ofac' in x.lower() or 'geo' in x.lower():
                return pd.Series(['Integration','Party'],index=['Seggregation','Application'])
            elif 'agency' in x.lower() or 'tier' in x.lower():
                return pd.Series(['Agency Party','Party'],index=['Seggregation','Application'])
            else:
                return pd.Series(['BillingOther','Billing'],index=['Seggregation','Application'])
        elif 'claim' in y.lower() or 'claim' in x.lower():
            if 'party' in x.lower() or 'ofac' in x.lower() or 'geo' in x.lower():
                return pd.Series(['Integration','Party'],index=['Seggregation','Application'])
            elif 'coverage' in x.lower():
                return pd.Series(['CoverageMatch','Claims'],index=['Seggregation','Application'])
            elif 'attach' in x.lower():
                return pd.Series(['AttachPolicy','Claims'],index=['Seggregation','Application'])
            else:
                return pd.Series(['ClaimsOther','Claims'],index=['Seggregation','Application'])
        elif 'party' in y.lower() or 'party' in x.lower():
            if 'search' in x.lower():
                return pd.Series(['Search','Party'],index=['Seggregation','Application'])
            elif 'role' in x.lower():
                return pd.Series(['Role','Party'],index=['Seggregation','Application'])
            elif 'duplicate' in x.lower():
                return pd.Series(['Duplicate Party','Party'],index=['Seggregation','Application'])
            elif 'address' in x.lower() or 'location' in x.lower():
                return pd.Series(['Party Location','Party'],index=['Seggregation','Application'])
            elif 'add' in x.lower():
                return pd.Series(['Add Party','Party'],index=['Seggregation','Application'])
            elif 'ssn' in x.lower() or 'npi' in x.lower() or 'ein' in x.lower():
                return pd.Series(['Demographics','Party'],index=['Seggregation','Application'])
            elif 'phone' in x.lower() or 'npi' in x.lower() or 'ein' in x.lower():
                return pd.Series(['Phone Number','Party'],index=['Seggregation','Application'])
            else:
                return pd.Series(['PartyOther','Party'],index=['Seggregation','Application'])
        else:
            return pd.Series(['Other','Other'],index=['Seggregation','Application'])
    else:
        return pd.Series(['Other','Other'],index=['Seggregation','Application'])

def Estimation(a):
    sev,est=a
    if(est is None):
        if(sev=='1 - Low'):
            return 'Simple'
        if(sev=='2 - Medium'):
            return 'Medium'
        if(sev=='3 - High'):
            return 'Complex'
        if(sev=='4 - Critical'):
            return 'Complicated'
    elif(est is not None):
        if(est<=8):
            return "Simple"
        elif(est>8 and est<=16):
            return "Medium"
        elif(est>16 and est<=24):
            return "Complex"
        elif(est>24):
            return "Complicated"

def missing_values_treatment(dataframe):
    dataframe['Developer'][dataframe['Developer'].isna()]='No Developer'
    dataframe['Severity'][dataframe['Severity'].isna()]='2 - Medium'
    dataframe['Estimate'][dataframe['Estimate'].isna()]=None
    return dataframe