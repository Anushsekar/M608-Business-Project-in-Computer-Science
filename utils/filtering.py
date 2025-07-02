def filter_data(df, year, attack_types, country):
    out = df.copy()
    if year != 'All Years':
        out = out[out['Year'] == year]
    if attack_types and set(attack_types) != set(df['Attack Type'].unique()):
        out = out[out['Attack Type'].isin(attack_types)]
    if country != 'All':
        out = out[out['Country'] == country]
    return out