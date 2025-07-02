import pandas as pd

# Country centroids (latitude, longitude)
# Source: https://gist.github.com/tadast/8827699 (cleaned for code use)
COUNTRY_COORDS = {
    "Australia": (-25.2744, 133.7751),
    "Brazil": (-14.2350, -51.9253),
    "China": (35.8617, 104.1954),
    "France": (46.6034, 1.8883),
    "Germany": (51.1657, 10.4515),
    "India": (20.5937, 78.9629),
    "Japan": (36.2048, 138.2529),
    "Russia": (61.5240, 105.3188),
    "UK": (55.3781, -3.4360),
    "USA": (37.0902, -95.7129)
}
def add_lat_lon(df):
    df["lat"] = df["Country"].map(lambda x: COUNTRY_COORDS.get(x, [None, None])[0])
    df["lon"] = df["Country"].map(lambda x: COUNTRY_COORDS.get(x, [None, None])[1])
    return df.dropna(subset=["lat", "lon"])
