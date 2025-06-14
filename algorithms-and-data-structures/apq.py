#The following Python files are required to run the evaluations: apq.py, graph.py, evaluation.py

class Element:
    """ An element with a key and value. """
    
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __eq__(self, other):
        """ Return True if this key equals the other key. """
        return self._key == other._key

    def __lt__(self, other):
        """ Return True if this key is less than the other key. """
        return self._key < other._key

    def _wipe(self):
        """ Set the instance variables to None. """
        self._key = None
        self._value = None
        self._index = None

    def key(self):
        """ Return the element's key (priority). """
        return self._key

class HeapAPQ:
    '''
    Adaptable Priority Queue
    '''

    def __init__(self):
        """ Create an APQ with no elements. """
        self._heap = []
        self._size = 0
        
    def __str__(self):
        """ Return a breadth-first string of the values. """
        outstr = '['
        index = 0
        for elt in self._heap:
            outstr += str(index) \
                      + ':' + str(elt._value) \
                      + ':' + str(elt._key) + ','
            index += 1
        return outstr + ']'

    #Methods for Priority Queue ADT

    def add(self, key, value):
        """ Add Element(key,value) to the heap. """
        e = Element(key, value, self._size)
        self._heap.append(e)
        self._upheap(self._size)
        self._size += 1
        return e

    def min(self):
        """ Return the min priority key,value. """
        if self._size:
            return self._heap[0]._key, self._heap[0]._value
        return None, None

    def remove_min(self):
        """ Remove and return the min priority key,value. """
        returnvalue = None
        returnkey = None
        if self._size > 0:
            returnkey = self._heap[0]._key
            returnvalue = self._heap[0]._value
            self._heap[0]._wipe()
            if self._size > 1: #if other items, restructure
                self._heap[0] = self._heap[-1]
                self._heap[0]._index = 0        #Fixed
                self._heap.pop()
                self._size -= 1
                self._downheap(0)
            else:
                self._heap.pop()
                self._size -= 1
        return returnkey, returnvalue

    def length(self):
        """ Return the number of items in the heap. """
        return self._size
    
    #Methods for Adaptable Priority Queue ADT

    def update_key(self, element, new_key):
        old_key = element._key
        element._key = new_key
        if element._key > old_key:
            self._downheap(element._index)
        elif element._key < old_key:
            self._upheap(element._index)

    def get_key(self, element):
        return element._key

    def remove(self, element):
        key = element._key
        value = element._value
        i = element._index
        element._wipe()
        self._heap[i], self._heap[self.size-1] = self._heap[self.size-1], self._heap[i]
        self._heap.pop()
        self._size -= 1
        self._heap[i]._index = i
        self._downheap(i)
        return key, value

    #Private methods

    def _left(self, posn):
        """ Return the index of the left child of elt at index posn. """
        return 1 + 2*posn

    def _right(self, posn):
        """ Return the index of the right child of elt at index posn. """
        return 2 + 2*posn

    def _parent(self, posn):
        """ Return the index of the parent of elt at index posn. """
        return (posn - 1)//2
    
    def _upheap(self, posn):
        """ Bubble the item in posn in the heap up to its correct place. """
        if posn > 0 and self._upswap(posn, self._parent(posn)):
            self._upheap(self._parent(posn))

    def _upswap(self, posn, parent):
        """ If heap elt at posn has lower key than parent, swap. """
        if self._heap[posn] < self._heap[parent]:
            self._heap[posn], self._heap[parent] = self._heap[parent], self._heap[posn]
            self._heap[posn]._index = posn
            self._heap[parent]._index = parent
            return True
        return False

    def _downheap(self, posn):
        """ Bubble the item in posn in the heap down to its correct place. """
        #find minchild position
        #if minchild is in the heap
        #    if downswap with minchild is true
        #        downheap minchild
        minchild = self._left(posn)
        if minchild < self._size:
            if (minchild + 1 < self._size and
                self._heap[minchild]._key > self._heap[minchild + 1]._key):
                minchild +=1
            if self._downswap(posn, minchild):
                self._downheap(minchild)

    def _downswap(self, posn, child):
        """ If healp elt at posn has lower key than child, swap; else return False. """
        #Note: this could be merged with _upswap to provide a general
        #heapswap(first, second) method, which swaps if the element
        #first has lower key than the element second
        if self._heap[posn]._key > self._heap[child]._key:
            self._heap[posn], self._heap[child] = self._heap[child], self._heap[posn]
            self._heap[posn]._index = posn
            self._heap[child]._index = child
            return True
        return False

class ListAPQ:
    def __init__(self):
        self._body = []

    def add(self, key, value):
        e = Element(key, value, len(self._body))
        self._body.append(e)
        return e

    def remove_min(self):
        min = 0
        for i in range(1, len(self._body)):
            if self._body[i] < self._body[min]:
                min = i
        returnkey = self._body[min]._key
        returnvalue = self._body[min]._value

        self._body[min]._wipe()

        self._body[min] = self._body[-1]
        self._body[min]._index = min

        self._body.pop()

        return returnkey, returnvalue

    def update_key(self, element, new_key):
        element._key = new_key

    def length(self):
        return len(self._body)
