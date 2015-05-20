movies = ["holy grail", 1975, "Terry Jones", 91,
               ["Graham Chapman", ["Michael Palin", "John cleese",
                      "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

#print movies

def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print each_item

print_lol(movies)
