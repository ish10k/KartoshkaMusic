import json
class SongQueue():
    head = 0
    length = 0
    queue = []
    def __init__(self, length, head=None, queue=None):
        #if allows us to have two different constructors
        if head==None:
            #new sq constructor
            self.length=length
        else:
            self.length=length
            self.head=head
            self.queue=queue
    
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
        return self.getQueue()[0]

    def toJSON(self):
        d = {
            "head" : self.head,
            "length" : self.length,
            "queue": self.queue,
        }
        return json.dumps(d)

'''
sq = SongQueue(3)
sq.addItem("1")
sq.addItem("2")
sq.addItem("3")
sq.addItem("4")
sq.addItem("5")

print(sq.getQueue())
print(sq.peak())
'''