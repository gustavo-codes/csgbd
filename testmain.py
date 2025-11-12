from HashIndex.ExtendibleHash import HashIndex

table = HashIndex()

table.insert(1)
table.insert(2)
table.insert(3)
table.insert(4)
table.insert(5)
table.insert(7)

table.print_buckets()