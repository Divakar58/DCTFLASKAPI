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
        if 'policy' in y.lower() or ('policy' in x.lower() and 'claim' not in x.lower()) :
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
            elif 'risk' in x.lower() or 'line' in x.lower():
                return pd.Series(['Risk','Policy'],index=['Seggregation','Application'])
            elif 'form' in x.lower() or 'doc' in x.lower():
                return pd.Series(['Forms','Policy'],index=['Seggregation','Application'])
            elif 'search' in x.lower():
                return pd.Series(['Search','Policy'],index=['Seggregation','Application'])
            elif 'rate' in x.lower() and 'table' in x.lower():
                return pd.Series(['RateTable','Policy'],index=['Seggregation','Application'])
            elif 'shred' in x.lower() and 'policy' in y.lower():
                return pd.Series(['Shred','Policy'],index=['Seggregation','Application'])
            elif 'policy' in y.lower() or 'usdot' in x.lower() or 'probil' in x.lower() or 'mvr' in x.lower():
                return pd.Series(['Integrations','Policy'],index=['Seggregation','Application'])
            elif 'policy' in y.lower() or ('key' in x.lower() and 'missing' in x.lower()):
                return pd.Series(['Table','Policy'],index=['Seggregation','Application'])
            elif 'policy' in y.lower() or ('object' in x.lower() and 'reference' in x.lower()):
                return pd.Series(['CBO','Policy'],index=['Seggregation','Application'])
            else:
                return pd.Series(['PolicyOther','Policy'],index=['Seggregation','Application'])
        elif 'billing' in y.lower() or 'billing' in x.lower():
            if 'invoice' in x.lower():
                return pd.Series(['Invoice','Billing'],index=['Seggregation','Application'])
            elif 'disbursement' in x.lower():
                return pd.Series(['Disbursement','Billing'],index=['Seggregation','Application'])
            elif 'payment' in x.lower() or 'transfer' in x.lower():
                return pd.Series(['Payment','Billing'],index=['Seggregation','Application'])
            elif 'shred' in x.lower() and 'billing' in y.lower():
                return pd.Series(['Shred','Billing'],index=['Seggregation','Application'])
            elif 'schedule' in x.lower():
                return pd.Series(['ScheduleActivity','Billing'],index=['Seggregation','Application'])
            elif 'commission' in x.lower():
                return pd.Series(['Commission','Billing'],index=['Seggregation','Application'])
            elif 'pcn' in x.lower() and 'billing' in x.lower():
                return pd.Series(['PCN','Billing'],index=['Seggregation','Application'])
            elif 'receivable' in x.lower():
                return pd.Series(['Receivable','Billing'],index=['Seggregation','Application'])
            elif 'user admin' in x.lower() or 'access' in x.lower():
                return pd.Series(['UserAdmin','Policy'],index=['Seggregation','Application'])
            elif 'reports' in x.lower() and 'billing' in y.lower():
                return pd.Series(['Reports','Billing'],index=['Seggregation','Application'])
            elif 'party' in x.lower() or 'ofac' in x.lower() or 'geo' in x.lower():
                return pd.Series(['Integrations','Party'],index=['Seggregation','Application'])
            elif 'agency' in x.lower() or 'tier' in x.lower():
                return pd.Series(['AgencyParty','Party'],index=['Seggregation','Application'])
            else:
                return pd.Series(['BillingOther','Billing'],index=['Seggregation','Application'])
        elif 'claim' in y.lower() or 'claim' in x.lower():
            if 'party' in x.lower() or 'ofac' in x.lower() or 'geo' in x.lower():
                return pd.Series(['Integrations','Party'],index=['Seggregation','Application'])
            elif 'coverage' in x.lower():
                return pd.Series(['CoverageMatch','Claims'],index=['Seggregation','Application'])
            elif 'attach' in x.lower():
                return pd.Series(['AttachPolicy','Claims'],index=['Seggregation','Application'])
            elif 'fnol' in x.lower():
                return pd.Series(['FNOL','Claims'],index=['Seggregation','Application'])
            elif 'search' in x.lower():
                return pd.Series(['Claims search','Claims'],index=['Seggregation','Application'])
            elif 'event' in x.lower():
                return pd.Series(['Event','Claims'],index=['Seggregation','Application'])
            elif 'line' in x.lower():
                return pd.Series(['Line','Claims'],index=['Seggregation','Application'])
            elif 'cloning' in x.lower() or 'clone' in x.lower():
                return pd.Series(['Cloning','Claims'],index=['Seggregation','Application'])
            elif 'reopen' in x.lower() and 'claim' in x.lower():
                return pd.Series(['Reopenclaims','Claims'],index=['Seggregation','Application'])
            elif 'medicare' in x.lower():
                return pd.Series(['Medicareclaims','Claims'],index=['Seggregation','Application'])
            elif 'payment' in x.lower() and 'payment transfer' in x.lower():
                return pd.Series(['claims payments','Claims'],index=['Seggregation','Application'])
            elif 'deduct' in x.lower() and 'claim' in x.lower():
                return pd.Series(['Deductiables','Claims'],index=['Seggregation','Application'])
            else:
                return pd.Series(['ClaimsOther','Claims'],index=['Seggregation','Application'])
        elif 'party' in y.lower() or 'party' in x.lower():
            if 'search' in x.lower():
                return pd.Series(['Search','Party'],index=['Seggregation','Application'])
            elif 'role' in x.lower():
                return pd.Series(['Role','Party'],index=['Seggregation','Application'])
            elif 'duplicate' in x.lower():
                return pd.Series(['DuplicateParty','Party'],index=['Seggregation','Application'])
            elif 'address' in x.lower() and 'work' in x.lower():
                return pd.Series(['Work with Address','Party'],index=['Seggregation','Application'])
            elif 'address' in x.lower() and 'work' not in x.lower():
                return pd.Series(['Party Address','Party'],index=['Seggregation','Application'])
            elif '360' in x.lower() :
                return pd.Series(['Party360','Party'],index=['Seggregation','Application'])
            elif 'add' in x.lower():
                return pd.Series(['Add Party','Party'],index=['Seggregation','Application'])
            elif 'ssn' in x.lower() or 'npi' in x.lower() or 'ein' in x.lower():
                return pd.Series(['Demographics','Party'],index=['Seggregation','Application'])
            elif 'phone' in x.lower():
                return pd.Series(['Phone Number','Party'],index=['Seggregation','Application'])
            elif 'market' in x.lower() :
                return pd.Series(['Marketing','Party'],index=['Seggregation','Application'])
            elif 'risk' in x.lower() and 'manage' in x.lower():
                return pd.Series(['RiskManagement','Party'],index=['Seggregation','Application'])
            else:
                return pd.Series(['PartyOther','Party'],index=['Seggregation','Application'])
        else:
            return pd.Series(['Other','Other'],index=['Seggregation','Application'])
    else:
        return pd.Series(['Other','Other'],index=['Seggregation','Application'])

def Estimation(a):
    sev,est=a
    if(est is None):
        if('low' in sev.lower()):
            return 'Simple'
        elif('medium' in sev.lower()):
            return 'Medium'
        elif('high' in sev.lower()):
            return 'Complex'
        elif('critical' in sev.lower()):
            return 'Complicated'
        else:
            print(sev,"incomplete severity")
    elif(est is not None):
        if(est<=8):
            return "Simple"
        elif(est>8 and est<=16):
            return "Medium"
        elif(est>16 and est<=24):
            return "Complex"
        elif(est>24):
            return "Complicated"
        else:
            print(sev,"incomplete severity")
    else:
        print(est,sev,"incomplete")

def missing_values_treatment(dataframe):
    dataframe['Developer'][dataframe['Developer'].isna()]='No Developer'
    dataframe['Severity'][dataframe['Severity'].isna()]='Medium'
    dataframe['Estimate'][dataframe['Estimate'].isna()]=None
    dataframe['Tester'][dataframe['Tester'].isna()]='No Tester'
    return dataframe