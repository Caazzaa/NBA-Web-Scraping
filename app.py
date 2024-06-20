import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

years = list(range(1991, 2022))

stats = pd.read_csv("player_mvp_stats.csv")

del stats["Unnamed: 0"]
stats = stats.fillna(0)

predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Year',
       'W', 'L', 'W/L%', 'GB', 'PS/G',
       'PA/G', 'SRS']

train = stats[stats["Year"] < 2021]
test = stats[stats["Year"] == 2021]

reg = Ridge(alpha=.1)
reg.fit(train[predictors], train["Share"])
Ridge(alpha=.1)

def find_ap(combination):
    actual = combination.sort_values("Share", ascending=False).head(5)
    predicted = combination.sort_values("predictions", ascending=False)
    ps = []
    found = 0
    seen = 1
    for index, row in predicted.iterrows():
        if row["Player"] in actual["Player"].values:
            found += 1
            ps.append(found/seen)
        seen += 1
    return sum(ps) / len(ps)

def add_ranks(combination):
    combination = combination.sort_values("Share", ascending=False)
    combination["Rk"] = list(range(1, combination.shape[0]+1))
    combination = combination.sort_values("predictions", ascending=False)
    combination["Predicted_Rk"] = list(range(1, combination.shape[0]+1))
    combination["Diff"] = combination["Rk"] - combination["Predicted_Rk"]
    return combination

def backtest(stats, model, year, predictors):
    aps = []
    all_predictions = []
    for year in years[5:]:
        train = stats[stats["Year"] < year]
        test = stats[stats["Year"] == year]
        reg.fit(train[predictors], train["Share"])
        predictions = reg.predict(test[predictors])
        predictions = pd.DataFrame(predictions, columns=["predictions"], index=test.index)
        combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)
        combination = add_ranks(combination)
        all_predictions.append(combination)
        aps.append(find_ap(combination))
    return sum(aps) / len(aps), aps, all_predictions

mean_ap, aps, all_predictions = backtest(stats, reg, years[5:], predictors)
print(mean_ap)

ranking = add_ranks(all_predictions[1])
ranking = ranking[ranking["Rk"] < 6].sort_values("Diff", ascending=False)

every_pred = pd.concat(all_predictions)
print(every_pred[every_pred["Rk"] <= 5].sort_values("Diff").head(10))

important_stats = pd.concat([pd.Series(reg.coef_), pd.Series(predictors)], axis=1).sort_values(0, ascending=False)
print(important_stats)

stat_ratios = stats[["PTS", "AST", "STL", "BLK", "3P", "Year"]].groupby("Year").apply(lambda x: x/x.mean())
print(stat_ratios)

stats[["PTS_T", "AST_R", "STL_R", "BLK_R", "3P_R"]] = stat_ratios[["PTS", "AST", "STL", "BLK", "3P"]].values
predictors += ["PTS_T", "AST_R", "STL_R", "BLK_R", "3P_R"]
mean_ap, aps, all_predictions = backtest(stats, reg, years[5:], predictors)
print(mean_ap)
