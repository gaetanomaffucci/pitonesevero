from math import ceil

    def split(self, x):
        i = ceil(len(x._keys)/2) - 1

        #case root without children
        if x.parent == None and x.isleaf():


            y = BTreeNode(self.t)
            y.insert_key(x._keys[i])
            y.parent = None
            self.root = y

            z = BTreeNode(self.t)
            z.insert_keys(x._keys[(i + 1):])
            z.parent = y

            del x._keys[i:]

            y._c.append(x)
            y._c.append(z)


        #root with children
        elif x.parent==None and not x.isleaf():

            #z containz keys from i+1 till end
            z = BTreeNode(self.t)
            z._keys=x._keys[(i + 1):]
            z._c = x._c[(i+1):]
            for i in range(0, len(z._c)):
                z._c[i].parent = z


            #y contains the median key and becames the new root
            y = BTreeNode(self.t)
            y.insert_key(x._keys[i])
            z.parent = y

            y._c.append(x)
            y._c.append(z)
            x.parent = y

            del x._keys[i:]
            del x._c[i+1:]

            self.root = y

        #Since overflow occurred in x we must split x
        else:
            temp=x._keys[i]
            x.parent.insert_key(temp)

            z = BTreeNode(self.t)
            z.insert_keys(x._keys[(i + 1):])
            z._c=x._c[(i+1):]
            z.parent=x.parent

            x._keys = x._keys[0:i]
            x._c=x._c[0:(i+1)]

            (node, index) = self.search(temp, x.parent)

            x.parent._c.insert(i+1, z)

            if x.parent.isfull():
                self.split(x.parent)

    def delete(self, element):

        #search in which node and posizion in this is the element searched
        x,i = self.search(element, None)

        #CASE 1: node "x" is not leaf search predecessor of element
        if not x.leaf:
            #methos takes as parameters the node "x" and position "i"
            pred = self.predecessor(x, i)
            #in the position "i" of element in the node "x", we take the predecessor founded
            x.keys.insert(i, pred)
            self.delete(pred)

        #CASE 2: node "x" is leaf
        else:
            #CASE 2.1: the leaf contains >t-1 keys ---> can delete the element from node "x"
            if len(x.keys) > self.t - 1:
                x.keys.remove(element)
            #CASE 2.2: the leaf contains t-1 keys ---> in this case there are others two cases
            elif len(x.keys) == self.t - 1:
                # need to found index "j" that indicates the position of list c of node parent
                for j in range (0,len(x.parent.keys)+1):
                    if x.parent.c[j].keys[0] == x.keys[0]:
                        if j != 0:
                            k = j - 1
                        else:
                            k = j + 1
                        break
                #CASE 2.2.1: redistribute the keys with adjacent sibling
                # adjacent sibling is to left
                if len(x.parent.c[k].keys) > self.t - 1 and k == j - 1:
                    j = k
                    index = len(x.parent.c[k].keys) - 1
                    self.redistribution(element, k, j, index, x)
                # adjacent sibling is to right
                elif len(x.parent.c[k].keys) > self.t - 1 and k == j + 1:
                    index = 0
                    self.redistribution(element, k, j, index, x)
                #CASE 2.2.2: fusion with adjacent sibling
                # adjacent sibling is to left
                elif len(x.parent.c[k].keys) == self.t - 1 and k == j - 1:
                    self.fusion(element, x, k, j)
                # adjacent sibling is to right
                elif len(x.parent.c[k].keys) == self.t - 1 and k == j + 1:
                    self.fusion(element, x, j, k)

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



#test
b = BTree(2)

for i in range(1,12):
    b.insert(i)
    #b.print_node(b.root)


b.print_node(b.root)