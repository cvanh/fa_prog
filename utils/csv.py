import pandas as pd 

csv_headers =  ["id", "keycode"]

def read_csv() -> pd.DataFrame:
    return pd.read_csv("./fa_testkluizen.txt", names=csv_headers, sep=";") 

def write_csv(csv: pd.DataFrame) -> None:
    print(csv)
    csv.to_csv("./fa_testkluizen.txt", sep=";",index=False,header=False)
    