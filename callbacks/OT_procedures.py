from data.OT_constants import COURSES

# Funcția care returnează cursurile unei universități
def get_dict_key_from_value(val, my_dict):
   
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return print(f"for value {val} key doesn't exist")

# Funcția care returnează cursurile unei universități
def get_courses_for_university(university_name):
    return COURSES.get(university_name, [])

