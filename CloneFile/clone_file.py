
NUMBER_OF_CLONES = 20

f_in = open('input.txt', 'r')
lines = f_in.readlines()
text = ''
i = 1

print 'Cloning:'
while (i <= NUMBER_OF_CLONES):

    for line in lines:
        text += line

    print str(i)
    i += 1

f_in.close()

f_out = open('input_' + str(NUMBER_OF_CLONES) + 'x.txt', 'w')
f_out.write(text)
f_out.close()

print 'DONE!'