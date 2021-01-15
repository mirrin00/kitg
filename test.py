a = [1,2,3,-1,5,-1]
a = [v for v in a if v > 0]
a.remove([2,5])
print(a)