with open('uuids', 'r') as f:
    uuids = f.readlines()


poppable_uuids = uuids[:]

for i in range(len(uuids)):
    poppable_uuids = uuids[:]
    test = poppable_uuids.pop(i)
    if test in poppable_uuids:
        print('Error: id clash')
