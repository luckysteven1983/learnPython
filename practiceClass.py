class Athlete:
    def __init__(self, a_name, a_dob=None, a_times=[]):
        # The code to initialize a "Athlete" object.
##        a = Athlete()
##        b = Athlete()
##        c = Athlete()
##        d = Athlete()
        self.name = a_name
        self.dob = a_dob
        self.times = a_times
##        sarah = Athlete('Sarah Sweeney','2002-6-17',['2:58','2.58','2:39','2-25','2-55','2:54','2.18','2:55','2:55','2:22','2-21','2.22'])
##        james = Athlete('James Jones')
    def top3(self):
        return(sorted(set([sanitize(t) for t in self.times]))[0:3])
    def add_time(self, time_value):
        self.times.append(time_value)
    def add_times(self, list_of_times):
        self.times.extend(list_of_times)

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
        return(Athlete(templ.pop(0), templ.pop(0), templ))
    except IOError as ioerr:
        print('File error: ' + str(ioerr))
        return(None)
james = get_coach_data('james2.txt')
print(james.name + "'s fastest times are: " + str(james.top3()))

vera = Athlete('Vera vi')
vera.add_time('1.31')
print(vera.top3())
vera.add_times(['2.22', '1-21', '2:22'])
print(vera.top3())

class NamedList(list):
    def __init__(self, a_name):
        list.__init__([])
        self.name = a_name
johnny = NamedList("John Paul Jones")
johnny.append("Bass Player")
johnny.extend(['Composer', 'Arranger', 'Musician'])
for attr in johnny:
    print(johnny.name + " is a " + attr + ".")


