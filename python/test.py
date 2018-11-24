d = {'a':1,'b':4,'c':2}
print(sorted(d.items(),key = lambda x:x[1],reverse = True))
mydict_new = dict([val,key] for key,val in d.items())
print(mydict_new)