

##with open('mydata.pickle', 'wb') as mysavedata:
##          pickle.dump([1, 2, 'three'], mysavedata)
##
##with open('mydata.picke, 'rb') as myrestoredata:
##          a_list = pickle.load(myrestoredata)
##
##print(a_list)
def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)
    (mins, secs) = time_string.split(splitter)
    return(mins + '.' + secs)

##with open('james.txt') as jaf:
##    data = jaf.readline()
##james = data.strip().split(',')
##with open('julie.txt') as juf:
##    data = juf.readline()
##julie = data.strip().split(',')
##with open('mikey.txt') as mif:
##    data = mif.readline()
##mikey = data.strip().split(',')
##with open('sarah.txt') as saf:
##    data = saf.readline()
##sarah = data.strip().split(',')
def get_coach_data(filename):
    try:
        with open(filename) as f:
            data = f.readline()
        return(data.strip().split(','))
    except IOError as ioerr:
        print('File error: ' + str(ioerr))
        return(None)

sarah = get_coach_data('sarah2.txt')
(sarah_name, sarah_dob) = sarah.pop(0), sarah.pop(0)
print(sarah_name + "'s fastest times are: " +
      str(sorted(set([sanitize(t) for t in sarah]))[0:3]) +
      ", and his/her birthday is: " + sarah_dob)
##clean_james = []
##clean_julie = []
##clean_mikey = []
##clean_sarah = []

##for each_t in james:
##    clean_james.append(sanitize(each_t))
##for each_t in julie:
##    clean_julie.append(sanitize(each_t))
##for each_t in mikey:
##    clean_mikey.append(sanitize(each_t))
##for each_t in sarah:
##    clean_sarah.append(sanitize(each_t))

##clean_james = [sanitize(each_t) for each_t in james]
##clean_julie = [sanitize(each_t) for each_t in julie]
##clean_mikey = [sanitize(each_t) for each_t in mikey]
##clean_sarah = [sanitize(each_t) for each_t in sarah]
##
##print(sorted(clean_james, reverse = True))
##print(sorted(clean_julie))
##print(sorted(clean_mikey))
##print(sorted(clean_sarah))
##james = sorted([sanitize(t) for t in james], reverse = True)

##unique_james = []
##for each_t in james:
##    if each_t not in unique_james:
##        unique_james.append(each_t)
##print(unique_james[0:3])

##james = get_coach_data('james.txt')
##james = sorted([sanitize(t) for t in james])
##print(sorted(set(james))[0:3])
