from .Bucket import Bucket
import pandas as pd
import random

class HashIndex:
    def __init__(self):
        self.globalDepth = 1 
        self.bucketSize = 4  
        self.table = {
            "0": Bucket(localDepth=1), 
            "1": Bucket(localDepth=1)
        }
    
    def hash(self, number: int):
        return f'{number:08b}'
    
    def expand(self):
        newTable = {}
        for idx, bucket in self.table.items():
            newTable["0" + idx] = bucket
            newTable["1" + idx] = bucket
            
        self.table = newTable
        self.globalDepth += 1
    

    def split(self, targetBucket, oldBucketHash, afterExpansion=False):
        oldItems = list(targetBucket.items) 
        targetBucket.items = [] 
        
        newLocalDepth = targetBucket.localDepth + 1
        targetBucket.localDepth = newLocalDepth
        newBucket = Bucket(newLocalDepth)
        
        suffix_comum_size = newLocalDepth - 1
        
        suffix_comum = oldBucketHash[-suffix_comum_size:] if suffix_comum_size > 0 else ""

        
        for hashKey in list(self.table.keys()):
            if hashKey[-suffix_comum_size:] == suffix_comum:
                if hashKey[-newLocalDepth] == '0':
                    self.table[hashKey] = targetBucket 
                elif hashKey[-newLocalDepth] == '1':
                    self.table[hashKey] = newBucket 
        
        
        for item in oldItems:
            newBucketHash = self.hash(item)[-self.globalDepth:]
            target = self.table[newBucketHash] 
            target.items.append(item)

    def insert(self, number: int):
        bucketHash = self.hash(number)[-self.globalDepth:]
            
        targetBucket = self.table[bucketHash]

        targetBucket.items.append(number)
        
        if len(targetBucket.items) > self.bucketSize:
            print("Overflow!!")
            
            if targetBucket.localDepth == self.globalDepth:
                oldBucketHash = bucketHash 
                self.expand() 
                self.split(targetBucket, oldBucketHash, afterExpansion=True) 
            else:
                self.split(targetBucket, bucketHash, afterExpansion=False)

    def print_buckets(self):
        data = []
        processed_buckets = set()

        for idx, bucket in self.table.items():
            if bucket not in processed_buckets:
                dirs = [k for k, v in self.table.items() if v is bucket]
                for d in dirs:  
                    data.append({
                        "Diretório": d,
                        "LocalDepth": bucket.localDepth,
                        "Itens": ", ".join(map(str, bucket.items)) if bucket.items else "-",
                        "Bucket ID": id(bucket)
                    })
                processed_buckets.add(bucket)

        df = pd.DataFrame(data, columns=["Diretório", "LocalDepth", "Itens", "Bucket ID"])
        pd.set_option("display.colheader_justify", "center")
        pd.set_option("display.width", 120)
        print(f"\n--- Estrutura do Hash Extensível (GlobalDepth={self.globalDepth}) ---")
        print(df.to_markdown(index=False, tablefmt="grid"))
