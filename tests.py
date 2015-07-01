#### Smart class with reference dictionary for terrain/items/creatures?
##from collections import defaultdict
##
##class KeepRefs(object):
##    __refs__ = defaultdict(dict)
##    def __init__(self,name):
##        self.__refs__[self.__class__][name]=self
##
##    @classmethod
##    def get_instances(cls,name):
##        return cls.__refs__[cls][name]
##
##class X(KeepRefs):
##    def __init__(self, name):
##        super(X, self).__init__(name)
##        self.name = name
##        self.bool= name=='x'
##
##x = X("x")
##y = X("y")

with open('load.py','r') as infile:
    i=1
    for l in infile:
        l=l.replace('terrain.T','')
        if 'terrain.' in l:
            print i
        i+=1
