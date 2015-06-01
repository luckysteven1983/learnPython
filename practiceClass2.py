class AthleteList(list):
    def __init__(self, a_name, a_dob=None, a_times=[]):
        # The code to initialize a "Athlete" object.
        list.__init__([])
        self.name = a_name
##        print(a_name)
        self.dob = a_dob
##        print(a_dob)
        self.extend(a_times)
##        print(a_times)
    def top3(self):
        return(sorted(set([sanitize(t) for t in self]))[0:3])

def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)
    (mins, secs) = time_string.split(splitter)
    return(mins + '.' + secs)

def get_coach_data(filename):
    try:
        with open(filename) as f:
            data = f.readline()
        templ = data.strip().split(',')
        return(AthleteList(templ.pop(0), templ.pop(0), templ))
    except IOError as ioerr:
        print('File error: ' + str(ioerr))
        return(None)
james = get_coach_data('james2.txt')
print(james.name + "'s fastest times are: " + str(james.top3()))

vera = AthleteList('Vera vi')
vera.append('1.31')
print(vera.top3())
vera.extend(['2.22', '1-21', '2:22'])
print(vera.top3())
