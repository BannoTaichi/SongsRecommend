# conda install seaborn (0.13.2)
# 参考資料
# https://qiita.com/sayuyuyu/items/4ca06a851fca41f6b270（相関分析）
import numpy as numpy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df_score = pd.read_csv(
        "songs.csv",
        index_col="name",
        usecols=[
            "name",
            "key",
            "mode",
            "danceability",
            "acousticness",
            "energy",
            "instrumentalness",
            "loudness",
            "speechiness",
            "tempo",
            "valence",
        ],
    )

    df_corr = df_score.corr()
    sns.set_context(context="talk")
    fig = plt.subplots(figsize=(8, 8))
    sns.heatmap(df_corr, annot=True, fmt=".1f", cmap="bwr", vmin=-1, vmax=1)
    plt.show()
