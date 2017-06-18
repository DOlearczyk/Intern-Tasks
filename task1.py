import pandas as pd


def group_by(stream, field, success=None):
    """
    Function parsing log of satellite orbital launches
    :param stream stream: stream object
    :param str field: 'year' or 'month'
    :param bool success: default None
    :rtype: dict
    :return: Dictionary of aggregations
    """
    # Load data from stream to DataFrame. Only loading necessary columns.
    df = pd.read_fwf(stream,
                     widths=[13, 27, 15, 31, 26, 9, 23, 16, 33, 5, 19],
                     skiprows=2,
                     names=['Launch', 'Launch Date (UTC)', 'COSPAR',
                            'PL Name', 'Orig PL Name', 'SATCAT', 'LV Type',
                            'LV S/N', 'Site', 'Suc', 'Ref'],
                     usecols=[1, 9]
                     )
    # Filtering based on success param. Also removing empty rows.
    if success:
        df = df[df.Suc == 'S']
    else:
        if success is False:
            df = df[df.Suc == 'F']
        else:
            df = df.dropna()

    # Retrieve month or year from 'Launch Date (UTC)' column.
    if field == 'year':
        df['Launch Date (UTC)'] = df['Launch Date (UTC)'].apply(
            lambda x: x.split(' ')[0])
    else:
        df['Launch Date (UTC)'] = df['Launch Date (UTC)'].apply(
            lambda x: x.split(' ')[1])

    # Aggregate by field count.
    aggregations = df[
        'Launch Date (UTC)'].value_counts().sort_index().to_dict()
    return aggregations
