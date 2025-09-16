import pandas as pd

def totalload(df, start_date, end_date):
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
    selected_names = {
        'PGE': 'Portland General Electric Company',
        'AVA': 'Avista Corporation',
        'GCPD': 'PUD No. 2 of Grant County, Washington',
        'PSEI': 'Puget Sound Energy, Inc.',
        'TPWR': 'City of Tacoma, Department of Public Utilities',
        'BPA': 'BPA',
        'DOPD': 'PUD No. 1 of Douglas County',
        'SCL': 'Seattle City Light',
        'CHPD': 'Public Utility District No. 1 of Chelan County',
        'PACW': 'PACW-TAC',   # this line is different from EICLoadanalysis.ipynb
        'Total': 'Total'
    }
    
    # Ensure datetime column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
        df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Filter by date range and company names, then aggregate
    filtered_df = df[
        (df['name'].isin(list(selected_names.values())[:-1])) & 
        (df['datetime'] >= pd.to_datetime(start_date)) & 
        (df['datetime'] <= pd.to_datetime(end_date))
    ]
    print("zones added: ", filtered_df['name'].unique())
    # Group by datetime and aggregate
    result = filtered_df.groupby('datetime').agg({'avgvalue': 'sum'}).rename(columns={'avgvalue': 'Total Load'})
    
    return result
