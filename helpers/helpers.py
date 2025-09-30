import pandas as pd
import pytz
def utc_to_local(utc_dt, timezone_str):
    if timezone_str is None:
        return utc_dt
    tz = pytz.timezone(timezone_str)
    return utc_dt.astimezone(tz)

def Zone_names(source='RTLOAD'):
    if source not in ['RTLOAD', 'EIA930_DEMAND']:
        raise ValueError("source must be either 'RTLOAD' or 'EIA930_DEMAND'")
    selected_names = {
        'PGE': 'Portland General Electric Company',
        'AVA': 'Avista Corporation',
        # 'GCPD': 'PUD No. 2 of Grant County, Washington',
        'PSEI': 'Puget Sound Energy, Inc.',
        'TPWR': 'City of Tacoma, Department of Public Utilities',
        'BPA': 'BPA',
        # 'DOPD': 'PUD No. 1 of Douglas County',
        'SCL': 'Seattle City Light',
        'AVRN': 'AVRN',
        'IDCO': 'Idaho Power Company',
        # 'CHPD': 'Public Utility District No. 1 of Chelan County',
        'PACW': 'PACW-TAC' if source=='RTLOAD' else 'PacifiCorp West',   # this line is different from EICLoadanalysis.ipynb
        # 'Total': 'Total'
    }
    return selected_names

def totalload(df, start_date=None, end_date=None):
    """
    Calculate the total load for selected utility companies within a given date range.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the load data with 'name', 'datetime', and 'avgvalue' columns
    start_date : str
        Start date in 'YYYY-MM-DD HHam/pm' format
    end_date : str
        End date in 'YYYY-MM-DD HHam/pm' format

    Returns:
    --------
    pandas.DataFrame
        DataFrame with datetime index and 'Total Load' column
    """
    # Define selected utility companies
    selected_names = Zone_names()
    
    # Ensure datetime column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
        df['datetime'] = pd.to_datetime(df['datetime'])
    if (start_date is None) and (end_date is None):
        filtered_df = df[df['name'].isin(list(selected_names.values()))]
    else:
        filtered_df = df[
            (df['name'].isin(list(selected_names.values())[:-1])) & 
            (df['datetime'] >= pd.to_datetime(start_date)) & 
            (df['datetime'] <= pd.to_datetime(end_date))
        ]
    print("zones added: ", filtered_df['name'].unique())
    # Group by datetime and aggregate
    result = filtered_df.groupby('datetime').agg({'avgvalue': 'sum'})
    
    return result
