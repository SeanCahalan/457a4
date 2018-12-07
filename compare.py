
decoded = open('decoded.txt', 'r')
unencoded = open('unencoded.txt', 'r')

dlines = [line for line in decoded]
ulines = [line for line in unencoded]

e = 0
for i in xrange(len(ulines)):
    if i >= len(dlines):
        e += 1
    elif dlines[i] != ulines[i]:
        e += 1
    

print str(e) + " / " + str(len(ulines)) + " incorrect"
print str( float(e)/len(ulines) ) + "%"

unencoded.close()
decoded.close()