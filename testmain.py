from HashIndex.ExtendibleHash import HashIndex

table = HashIndex()

table.insert("michael")
table.insert("Boc")
table.insert("Boc")
table.insert("Boc")

table.print_buckets()