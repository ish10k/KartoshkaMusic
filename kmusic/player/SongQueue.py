class SongQueue():
    head = 0
    length = 0
    queue = []
    def __init__(self, length):
        #if allows us to have two different constructors
        self.length=length
    
    def __str__(self):
        return (''.join(self.queue) + "\nhead: " + str(self.head))

    def addItem(self, link):
        if len(self.queue) < self.length:
            self.queue.append(link)
        else:
            self.queue[self.head] = link
        self.head+=1
        if self.head==self.length:
            self.head=0
    
    def getQueue(self):
        h = self.head-1
        q = []
        for i in range(0, len(self.queue)):
            q.append(self.queue[h])
            h+=1
            if h==len(self.queue):
                h=0
        return q

    def peak(self):
        print(self.getQueue()[0])
        return self.getQueue()[0]

'''
sq = SongQueue(10)
sq.addItem("test")
#sq.addItem("hello")
#sq.addItem("bye")
#sq.addItem("shrek")

print(sq.getQueue())
print(sq.peak())
'''