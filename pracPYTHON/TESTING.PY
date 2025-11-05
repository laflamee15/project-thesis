def create_name(first, last):
    first = first.capitalize()
    last = last.capitalize()
    return first + " " + last
fullname = create_name("Emman","Tenorio")
print(fullname)