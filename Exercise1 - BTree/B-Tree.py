
def predecessor(self, x, i):
    j = len(x.c[i].keys)
    if x.c[i].leaf:
        temp = x.c[i].keys[j-1]
        x.c[i].keys.remove(temp)
        return temp
    else:
        self.predecessor(x.c[i], j+1)

def fusion(self, element, x, k, j):
    x.parent.c[k].append(x.parent.keys[k])
    x.keys.remove(element)
    x.parent.c[k].keys.extend(x.parent.c[j].keys)
    x.parent.c[j].keys.clear()
    x.parent.keys.remove(x.parent.keys[k])

def redistribution(self, element, k, j, index, x):
    temp = x.parent.keys[j]
    x.parent.keys.insert(j, x.parent.c[k].keys[index])
    x.parent.c[k].keys.remove(x.parent.c[k].keys[index])
    x.keys.append(temp)
    x.keys.remove(element)
    x.keys.sort()
