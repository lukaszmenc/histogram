import re
import io
import matplotlib.pyplot as plt
import pandas as pd


def remove_non_numeric(data, column_name):
    for index, row in data.iterrows():
        if isinstance(data.at[index, column_name], str):
            new_value = re.sub(r"[^\d\.]", "", data.at[index, column_name])
            data.at[index, column_name] = new_value
    return data


def prepare_data(df, test_step_name):
    test_step_data = df[[test_step_name]]
    test_step_data = test_step_data[test_step_data[test_step_name].notna()]
    test_step_data = remove_non_numeric(test_step_data, test_step_name)
    return test_step_data


def dominant(a):
    a = a[0].tolist()
    unique_a = set(a)
    result = 0
    occur_ = 0
    for x in unique_a:
        occur = a.count(x)
        if occur > occur_:
            result = x
            occur_ = occur

    return result


def calculate_coeffs(values, lsl, usl):
    values = pd.DataFrame(values)
    try:
        mu = round(float(values.mean()), 3)
        sigma = round(float(values.std()), 2)
        maximum = round(float(values.max()), 3)
        minimum = round(float(values.min()), 3)
        domin = round(dominant(values), 3)

        if sigma != 0:
            process_capability = round((usl - lsl) / (6 * sigma), 2)
            process_capability_upper = round((usl - mu) / (3 * sigma), 3)
            process_capability_lower = round((mu - lsl) / (3 * sigma), 3)
        else:
            process_capability = 0
            process_capability_upper = 0
            process_capability_lower = 0

        process_capability_index = min(
            process_capability_lower, process_capability_upper
        )

    except TypeError:
        return False

    return {
        "Cp": process_capability,
        "CPU": process_capability_upper,
        "CPL": process_capability_lower,
        "Cpk": process_capability_index,
        "mu": mu,
        "sigma": sigma,
        "min": minimum,
        "max": maximum,
        "dominant": domin,
    }


def draw_vertical_line(text, value, color="g", linestyle="dashed"):
    plt.annotate(
        text,
        xy=(value, 0.88),
        xytext=(0, 0),
        xycoords=("data", "figure fraction"),
        textcoords="offset points",
        size=10,
        ha="center",
        va="top",
        style="italic",
    )
    plt.axvline(value, color=color, linestyle=linestyle, linewidth=1)


def histogram(data, column_name, lsl, usl, minimum=None, maximum=None):
    values = [float(item) for item in data[column_name].tolist()]

    if minimum:
        if float(minimum) > lsl:
            minimum = lsl
        values = [value for value in values if value >= float(minimum)]

    if maximum:
        if float(maximum) < usl:
            maximum = usl
        values = [value for value in values if value <= float(maximum)]

    coeffs = calculate_coeffs(values, lsl, usl)

    plt.rcdefaults()

    draw_vertical_line("LSL", lsl)
    draw_vertical_line("USL", usl)

    if coeffs:
        draw_vertical_line("µ", coeffs["mu"], "y", "solid")

    plt.hist(x=values, bins=30, color="#0504aa", alpha=0.7)
    plt.grid(axis="y", alpha=0.75)

    plt.title(f"{column_name}", pad=25)
    figw, figh = 8.0, 4.5
    plt.subplots_adjust(
        left=1 / figw, right=1 - 1 / figw, bottom=1 / figh, top=1 - 1 / figh
    )

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")

    plt.close()

    return buffer, coeffs
