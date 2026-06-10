from functions.get_files_info import get_files_info

# print the results of testing the function for debugging

# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))
# print(get_files_info("calculator", "main.py"))




def print_indented_result(header_text: str, files_info_string: str):
    print(header_text)
    for line in files_info_string.split("\n"):
        if line[:5] == "Error":
            print(f"    {line}")
        else:
            print(f"  {line}")


# new print statements


print_indented_result("Result for current directory:", get_files_info("calculator", "."))

print_indented_result("Result for 'pkg' directory:", get_files_info("calculator", "pkg"))

print_indented_result("Result for '/bin' directory:", get_files_info("calculator", "/bin"))

print_indented_result("Result for '../' directory:", get_files_info("calculator", "../"))