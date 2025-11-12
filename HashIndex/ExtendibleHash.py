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
    
    def hash(self,number:int):
        return f'{number:04b}'
    
    # Expands the directory by doubling its entries
    def expand(self):
        newTable = {}
        for idx, bucket in self.table.items():
            newTable["0"+idx] = bucket
            newTable["1"+idx] = bucket
        self.table = newTable
        self.globalDepth += 1
    
    def split(self,targetBucket, bucketHash):
        oldItems = targetBucket.items
        self.table["1"+bucketHash] = Bucket(targetBucket.localDepth+1)
        self.table["0"+bucketHash] = Bucket(targetBucket.localDepth+1)
        
        for i in oldItems:
            newBucketHash = self.hash(i)[-self.globalDepth:]
            newTargetBucket = self.table[newBucketHash]
            
            newTargetBucket.items.append(i)

    
    def insert(self,number:int):
        bucketHash = self.hash(number)[-self.globalDepth:]
        targetBucket = self.table[bucketHash]

        targetBucket.items.append(number)
        
        # In case of overflow
        if len(targetBucket.items) > self.bucketSize:
            print("Overflow!!")
            # If global depth needs to be increased
            if targetBucket.localDepth == self.globalDepth:
                self.expand()
                self.split(targetBucket,bucketHash)



    def print_buckets(self):
        for idx, bucket in self.table.items():
            print("Diretório " + idx + " ld " + str(bucket.localDepth))
            items = ""
            for b in bucket.items:
                items += str(b) + " "
            print(items)
