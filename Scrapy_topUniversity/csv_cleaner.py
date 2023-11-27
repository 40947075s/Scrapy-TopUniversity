import pandas as pd

"""
Remove all '=' and '+' from the csv file elements. 

- To add more files to clean, add the file name to the file_names list.
- To rename the output file, change the string in the df.to_csv() function.
"""

# TODO: Add all file names here
files = ["file_2021.csv", "file_2022.csv", "file_2023.csv", "file_2024.csv"]


def get_output_file_name(file_name):
    # TODO: Rename the output file by modifying the return string.
    # Example: return f"cleaned_{file_name}"

    # Or, to overwrite the input file, use:
    # return file_name
    return f"cleaned_{file_name}"


def data_clean(value):
    if pd.isnull(value):
        return "n/a"

    try:
        numeric_value = pd.to_numeric(value)
        return numeric_value
    except ValueError:
        pass

    cleaned_value = value.replace("=", "").replace("+", "")

    try:
        cleaned_value = pd.to_numeric(cleaned_value)
    except ValueError:
        # print(f"Could not convert {value} to numeric")
        pass

    return cleaned_value


if __name__ == "__main__":
    # clean data and create new csv files
    for file in files:
        df = pd.read_csv(file)

        df = df.drop_duplicates(subset="name", keep="first")
        df = df.apply(lambda x: x.map(data_clean))

        df.to_csv(get_output_file_name(file), index=False)

    # get intersection data of all files by university name
    output_files = [get_output_file_name(file) for file in files]

    common_universities = set(pd.read_csv(output_files[0])["name"])

    for file in output_files[1:]:
        current_universities = set(pd.read_csv(file)["name"])
        common_universities.intersection_update(current_universities)

    common_universities = list(common_universities)

    # filter data by common universities
    for file in output_files:
        df = pd.read_csv(file)
        filtered_df = df[df["name"].isin(common_universities)]

        filtered_df.to_csv(file, index=False)
