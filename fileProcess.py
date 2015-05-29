#import os

#if os.path.exists('sketch.txt'):
try:
    data = open('sketch.txt')
    for each_line in data:
    #    if each_line.find(':') >= 0:
    #    if not each_line.find(':') == -1:
        try:
            (role, line_spoken) = each_line.split(':', 1)
            print(role),
            print('said:'),
            print(line_spoken),
        except ValueError:
            pass
    #        print('#### Catch exception here! ####')
    data.close()
#else:
except IOError:
    print('The data file is missing!')
