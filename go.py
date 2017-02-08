import grab

tbls = grab.tables("https://cga.ct.gov/2015/rpt/2015-R-0046.htm")



def clean_min(row_min):
    # Haven't implemented yet -- don't need this data for current project
    return row_min

def process(df, outfile):
    df = df.copy()
    df.columns = "classification","offense","minimum"
    df[df.columns[0]] = df[df.columns[0]].fillna(method='ffill')
    # df["minimum"] = df.apply(lambda x: clean_min(x["minimum"]), axis=1)
    df.to_csv("output/" + outfile + ".csv", encoding="UTF-8")
    df.to_json("output/" + outfile + ".json", orient='records')
    
fel = tbls[1]
mis = tbls[2]


process(mis, "misdemeanors-2016")
process(fel, "felonies-2016")
