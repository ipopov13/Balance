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

import glob

files=glob.glob('*.py')
for f in files:
    with open(f,'r') as infile:
        i=1
        for l in infile:
            if 'movement' in l:
                print f,i
                break
            i+=1
