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
            self.head=0
            self.queue= []
        else:
            self.length=length
            self.head=head
            self.queue=queue.copy()
    
    def __str__(self):
        return (''.join(self.queue) + "\nhead: " + str(self.head))

    def addItem(self, link):
        if self.peak()!=link:
            if len(self.queue) < self.length:
                self.queue.append(link)
            else:
                self.queue[self.head] = link
            self.head+=1
            self.head = self.head % self.length
    
    def getQueue(self):
        if len(self.queue)==0:
            return []

        h = self.head % len(self.queue)
        q = []
        for i in range(0, len(self.queue)):
            #print("h: ", h)
            q.append(self.queue[h])
            h+=1
            h = h % len(self.queue)
        return q

    def getTail(self):
        if len(self.queue)==0:
            return []
        return self.getQueue()[:-1]

    def peak(self):
        if len(self.queue)>0:
            h = (self.head-1) % self.length
            return self.queue[h]
        else:
            return None

    def toJSON(self):
        d = {
            "head" : self.head,
            "length" : self.length,
            "queue": self.queue,
        }
        return json.dumps(d)

