poses = []
dx = 154
dy = 102.4

basex = 1740
basey = 150
for i in range(11):
    x = basex - dx*i
    y = basey
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 9):
    x = basex
    y = basey + dy * i
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 11):
    x = basex + dx*i
    y = basey
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 7):
    x = basex
    y = basey - dy*i
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 7):
    x = basex - dx*i
    y = basey
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 3):
    x = basex
    y = basey + dy*i
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 2):
    x = basex - dx * i
    y = basey
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 3):
    x = basex
    y = basey + dy*i
    poses.append([x, y])

basex = x
basey = y
for i in range(1, 4):
    x = basex + dx * i
    y = basey
    poses.append([x, y])

import json
print(len(poses))
with open('position.json', 'w') as f :
    json.dump(poses, f, indent=2)
