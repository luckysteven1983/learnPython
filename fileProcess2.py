from headFirstPython import print_lol
import pickle

man = []
other = []
try:
    data = open('sketch.txt')
    for each_line in data:
        try:
            (role, line_spoken) = each_line.split(':', 1)
            line_spoken = line_spoken.strip()
            if role == 'man':
                man.append(line_spoken)
            elif role == 'other man':
                other.append(line_spoken)
        except ValueError:
            pass
    data.close()
except IOError:
    print('The data file is missing!')
print(man)
print(other)

##try:
##    man_file = open('man_data.txt', 'w')
##    other_file = open('other_data.txt', 'w')
##    print >> man_file, man
##    print >> other_file, other
##except IOError:
##    print('File error.')
##finally:
##    man_file.close()
##    other_file.close()

try:
##    with open('man_data.txt', 'w') as man_file:
##        print >> man_file, man
##    with open('other_data.txt', 'w') as other_file:
##        print >> other_file, other
    with open('man_data.txt', 'w') as man_file, open('other_data.txt', 'w') as other_file:
        print >> man_file, man
        print >> other_file, other
except IOError as err:
    print('File error: ' + str(err))

try:
    with open('man_data1.txt', 'wb') as man_file, open('other_data1.txt', 'wb') as other_file:
        pickle.dump(man, man_file)
        pickle.dump(other, other_file)
except IOError as err:
    print('File error: ' + str(err))
except pickle.PickleError as perr:
    print('Pickling error: ' + str(perr))


new_man = []
try:
    with open('man_data1.txt', 'rb') as man_file:
        new_man = pickle.load(man_file)
except IOError as err:
    print('File error: ' + str(err))
except pickle.PickleError as perr:
    print('Pickling error: ' + str(perr))

print_lol(new_man)
print '#### Single line output begins here: ####'
print(new_man[0])
print(new_man[2])
print(new_man[-2])
print '#### Single line output finish here: ####'

##with open('man_data.txt') as mdf:
##    print(mdf.readline())

##try:
##    with open('man_data.txt', 'w') as man_file:
##        print_lol(man, True, 1, man_file)
##except IOError as err:
##    print('File error:' + str(err))
    
try:
    data2 = open('missing.txt')
    print(data2.readline()),
except IOError as err:
    print('File error: ' + str(err))
finally:
    if 'data2' in locals():
        data2.close()

try:
    with open('its.txt', 'w') as data3:
        print >> data3, "It's..."
except IOError as err:
    print('File error: ' + str(err))


