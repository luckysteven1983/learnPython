print 'Hello World!'
try:
    print 'try...'
    r = 10 / 2
    print 'result:', r
except ZeroDivisionError, e:
    print 'except:', e
finally:
    print 'finally...'
print 'END'
