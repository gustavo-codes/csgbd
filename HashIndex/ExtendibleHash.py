from .Bucket import Bucket
class HashIndex:
    def __init__(self):
        self.globalDepth = 1
        self.bucketSize = 3
        self.buckets = [Bucket()]
        self.table = {
            "0":Bucket(),
            "1":Bucket()
        }
    
    def hash(self,string:str):
        return ' '.join(format(ord(x), 'b') for x in string).replace(" ","")
    
    def expand(self):
        return
    
    def split(self):
        return
    
    def insert(self,string:str):
        bucketHash = self.hash(string)[-self.globalDepth:]
        targetBucket = self.table[bucketHash]
        
        if len(targetBucket.items) == self.bucketSize:
            if targetBucket.localDepth == self.globalDepth:
                self.expand()
                self.split()

        targetBucket.items.append(string)


    def print_buckets(self):
        for idx, bucket in self.table.items():
            print("Bucket " + idx)
            items = ""
            for b in bucket.items:
                items += b + " "
            print(items)
