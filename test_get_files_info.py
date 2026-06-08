from functions.get_files_info import get_files_info

# print the results of testing the function for debugging

print(get_files_info("calculator", "."))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))
print(get_files_info("calculator", "main.py"))