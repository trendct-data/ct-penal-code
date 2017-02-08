import pandas as pd

def tables(url):
    return pd.read_html(url)

def table(url, i):
    return tables(url)[i];
