data = open('sketch.txt')
for each_line in data:
    (role, line_spoken) = each_line.split(':')
    print(role),
    print('said:'),
    print(line_spoken),
