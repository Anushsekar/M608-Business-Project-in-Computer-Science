import pandas as pd
from config import DATA_DIR

def load_data():
    df = pd.read_csv(f"{DATA_DIR}/Global_Cybersecurity_Threats_2015-2024 2.csv")
    loss_df = pd.read_csv(f"{DATA_DIR}/LossFromNetCrime.csv")
    return df, loss_df
