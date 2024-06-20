import pandas as pd

mvps = pd.read_csv("mvps.csv")
mvps = mvps[["Player", "Year", "Pts Won", "Pts Max", "Share"]]

players = pd.read_csv("players.csv")
del players["Unnamed: 0"]
del players["Rk"]
players["Player"] = players["Player"].str.replace("*", "", regex=False)

def single_row(df):
    if df.shape[0] == 1:
        return df
    else:
        row = df[df["Tm"] == "TOT"]
        row["Tm"] = df.iloc[-1,:]["Tm"]
        return row
    
players = players.groupby(["Player", "Year"]).apply(single_row)
players.index = players.index.droplevel()
players.index = players.index.droplevel()

combined = players.merge(mvps, how="outer", on=["Player", "Year"])
combined[["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)

teams = pd.read_csv("teams.csv")
teams["Team"] = teams["Team"].str.replace("*", "", regex=False)

nicknames = {}

with open("nicknames.csv") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev,name = line.replace("\n", "").split(",")
        nicknames[abbrev] = name

combined["Team"] = combined["Tm"].map(nicknames)

stats = combined.merge(teams, how="outer", on=["Team", "Year"])
del stats["Unnamed: 0"]
stats["GB"] = stats["GB"].str.replace("—", "0")
stats = stats.apply(pd.to_numeric, errors="ignore")

# stats.to_csv("player_mvp_stats.csv")

highest_scoring = stats[stats["G"] > 70].sort_values("PTS", ascending=False).head(10)
highest_scoring_year = stats.groupby("Year").apply(lambda x: x.sort_values("PTS", ascending=False).head(1))
print(highest_scoring_year)