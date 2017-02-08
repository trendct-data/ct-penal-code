import grab, json, re
import pandas as pd

tbls = grab.tables("https://cga.ct.gov/2015/rpt/2015-R-0046.htm")

examples = []

def classify(row,tp):
    off_type = None
    class_type = None
    # if "felon" in row["classification"].lower():
    #     off_type = "felony"
    # elif "misdemeanor" in row["classification"].lower():
    #     off_type = "misdemeanor"
    off_type = tp
    
    if "class a" in row["classification"].lower():
        class_type = "A"
    elif "class b" in row["classification"].lower():
        class_type = "B"
    elif "class c" in row["classification"].lower():
        class_type = "C"
    elif "class d" in row["classification"].lower():
        class_type = "D"
    elif "class e" in row["classification"].lower():
        class_type = "E"
    elif "unclassified" in row["classification"].lower():
        class_type = "unclassified"

    charge = None

    s = re.search(r'.*\((.*-.*)\).*',row["offense"].lower());
    if s:
        # print "GOOD: ", row["offense"].lower()
        # print s.group(1)
        charge = s.group(1)
        pass
    else:
        pass
        # print "BAD: ", row ["offense"].lower()x
    
        
    if class_type != None and off_type != None and charge != None:
        examples.append({
            "type":off_type,
            "class":class_type,
            "offense":row["offense"],
            "statute":charge
            })

    
        
def clean_min(row_min):
    # Haven't implemented yet -- don't need this data for current project
    return row_min

def process(df, outfile):
    df = df.copy()
    df.columns = "classification","offense","minimum"
    df[df.columns[0]] = df[df.columns[0]].fillna(method='ffill')
    # df["minimum"] = df.apply(lambda x: clean_min(x["minimum"]), axis=1)
    # df.to_csv("output/" + outfile + ".csv", encoding="UTF-8")
    # df.to_json("output/" + outfile + ".json", orient='records')

    for index, row in df.iterrows():
        classify(row, outfile)

    open("output/" + outfile + "-examples.json",'w').write(json.dumps(examples))

    ex_df = pd.DataFrame(examples)
    ex_df.to_csv("output/" + outfile + "-examples.csv",index=False,encoding="UTF-8")

    print len(ex_df.index)
    
fel = tbls[1]
mis = tbls[2]


process(mis, "misdemeanor")
process(fel, "felony")
