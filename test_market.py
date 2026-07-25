import pandas as pd
import numpy as np

df = pd.read_csv("indicator_updates.csv")

print(df[df.isna().any(axis=1)].head(20))

print("\nNaN counts:")
print(df.isna().sum())