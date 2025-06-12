# SI NO SE CONSIGUE INSTALAR LA VERSION DE C++
from pyBKT.models import Model
import pandas as pd


df = pd.read_csv("../data/as.csv", encoding='latin1')


# df["problem_set_type"]
print(df.shape)
# Get 10% of the data
df = df.sample(frac=0.01, random_state=1)
print(df.shape)
df.to_csv("../data/as_red.csv", index=False)

model = Model()
model.fit(data_path="data/as_red.csv")
print(model.params().loc[("Polynomial Factors")])

