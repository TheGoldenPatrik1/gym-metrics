import panel as pn

def get_associated_dates(data, value, key):
    associated_dates = data.loc[data[key] == value, 'date']
    if len(associated_dates) == 0:
        return ""
    if len(associated_dates) > 1:
        return f" ({len(associated_dates)} instances)"
    associated_dates = associated_dates.iloc[0]
    associated_dates = str(associated_dates).replace(" 00:00:00", "")
    return f" ({associated_dates})"

def stat_table(data, key, exercise=False):
    # Calculate the statistics
    total = data[key].sum()
    average = data[key].mean()
    max_val = data[key].max()
    max_date = get_associated_dates(data, max_val, key)
    min_val = data[key].min()
    min_date = get_associated_dates(data, min_val, key)
    std = data[key].std()

    # Generate the exercise name values, if necessary
    row1 = "" if not exercise else "| Exercise "
    row2 = "" if not exercise else "|-------"
    row3 = "" if not exercise else f"| {exercise} "

    # Display the frequency statistics in a table
    table = f"{row1}| Total | Average | Max | Min | Standard Deviation |\n"
    table += f"{row2}|-------|---------|-----|-----|-----|\n"
    table += f"{row3}| {total:,} | {round(average, 2):,} | {max_val:,}{max_date} | {min_val:,}{min_date} | {round(std, 2):,} |"

    return pn.pane.Markdown(table)