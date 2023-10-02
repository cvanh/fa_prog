import pandas as pd 

csv_headers =  ["id", "keycode"]

def read_csv() -> pd.DataFrame:
    csv = pd.read_csv("./fa_testkluizen.txt", names=csv_headers, sep=";") 

    # TODO:here lies the issue, we need to use the id as the index
    # csv.set_index('id',inplace=True)
    print(csv)

    return csv

def write_csv(csv: pd.DataFrame) -> None:
    # csv.reset_index().set_index('id')
    csv.to_csv("./fa_testkluizen.txt", sep=";",index=False,header=False)
    