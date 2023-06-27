import os
import sys

sys.path.append(os.path.abspath("."))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Use engine for pandas connection to DB
from src.database.connect import engine

pdf_path = "C:/Users/Berzerk/Documents/GitHub/Bank_System_Practice/BSP/reports/rep2.pdf"
conn = engine.connect()

sql_query = """
select clients.id, clients.sex, clients.city, accounts.current_deposit
from clients inner join accounts
on clients.id = accounts.client_id 
order by accounts.current_deposit desc 
"""

df = pd.read_sql(sql_query, conn)
# df = df.head(25)
# dep_sex = df.groupby(["sex", "city"])["current_deposit"].agg("mean")

# f_sal = dep_sex["female"]
# m_sal = dep_sex["male"]

# with PdfPages(pdf_path) as export_pdf:
#     plt.figure(figsize=(12, 8))
#     plt.plot(f_sal, "bo", label="Women's average deposit")
#     plt.plot(m_sal, "ro", label="Men's average deposit")
#     plt.xticks(rotation=90)
#     plt.xlabel("City", fontsize="small", color="midnightblue")
#     plt.ylabel("Deposit", fontsize="small", color="midnightblue")
#     plt.title("Women's average deposit vs Men's in some cities")
#     plt.legend()
#     plt.grid()
#     export_pdf.savefig()
#     # plt.show()
#     plt.close()

# city_dep = df.groupby(["city"])["current_deposit"].agg(["mean"])
# labels = city_dep.index

# with PdfPages(pdf_path) as export_pdf:
#     plt.figure(figsize=(12, 9))
#     plt.bar(labels, city_dep["mean"], color=["b", "r", "y", "g", "c", "m", "k"])
#     plt.xlabel("City", fontsize="small", color="midnightblue")
#     plt.ylabel("Deposit", fontsize="small", color="midnightblue")
#     plt.xticks(rotation=90)
#     # plt.title("Вплив знанная англійської мови на зарплату", fontsize=10)
#     # plt.show()
#     export_pdf.savefig()
#     plt.close("all")

# dfc = df.groupby(["city"])["city"].count()
# nums = dfc.values
# labels = dfc.index

# with PdfPages(pdf_path) as export_pdf:
#     plt.figure(figsize=(12, 9))
#     plt.pie(
#         nums,
#         labels=labels,
#         shadow=True,
#         autopct="%.2f%%",
#         pctdistance=1.15,
#         labeldistance=1.35,
#     )

#     # plt.show()
#     export_pdf.savefig()
#     plt.close("all")

# print(np.sum(df.isnull()))
# print(pd.unique(df["city"]))
# df["current_deposit"].plot(kind="hist", title="City frequency", grid=True)
print(df.city)
