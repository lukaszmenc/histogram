import re


def remove_non_numeric(data, test_step_name):
    for index, row in data.iterrows():
        if isinstance(data.at[index, test_step_name], str):
            new_value = re.sub(r"[^\d\.]", "", data.at[index, test_step_name])
            data.at[index, test_step_name] = new_value
    return data


def prepare_data(df, test_step_name):
    test_step_data = df[[test_step_name]]
    test_step_data = test_step_data[test_step_data[test_step_name].notna()]
    test_step_data = remove_non_numeric(test_step_data, test_step_name)
    return test_step_data
