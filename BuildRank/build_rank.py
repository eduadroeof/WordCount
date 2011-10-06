
f_in = open('input.txt')
f_out = open('output.txt', 'w')
dict = {}

# Get all words and its number
for line in f_in.readlines():
    elements = line.strip().split()
    dict[elements[0]] = int(elements[1])

f_in.close()

items = dict.values()
items.sort()

i = len(items) - 1
current_value = items[i]
last_value = -1;
keys = dict.keys()

while(i >= 0):

    # Check if this number had already been searched
    if current_value != last_value:

        # Get all keys
        for key in keys:

            # Check if the value of current key is equal to the current number
            if dict[key] == current_value:
                f_out.write(key + ' ' + str(dict[key]) + '\n')

    i -= 1
    last_value = current_value
    current_value = items[i]

f_out.close()

  