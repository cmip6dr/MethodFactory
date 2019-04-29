


class Add(object):
  """MethodFactory.Add will add the method provided on instantiation to a class object provided on calling an instance. It is designed for use as a decorator.

  USAGE
  -----

  def m1(self,x):
    print ('%s received' % x )

  @Add(m1,name='test')
  class C1(object):
    pass

  c = c1()
  c.test( 'Message' )

  DISCUSSION
  ----------

  This is equivalent to calling setattr after defining the class and before instantiating, but using the decorator makes the scope of the definition of the class clearer.
  """


  def __init__(self,method,name=None):
    self.method = method
    self.name = name
    if name == None:
      self.name = method.__name__

  def __call__(self,cls):
    setattr(cls, self.name, self.method)
    return cls

class EmptyLinkList(Exception):
  """List of links is empty"""

class BaseException(Exception):
  """Basic exception for general use in code."""

  def __init__(self,msg):
    self.msg = 'scope:: %s' % msg

  def __str__(self):
    return repr( self.msg )

  def __repr__(self):
    return self.msg

class InvalidCodeWordArgument(BaseException):
  """An argument does not match any of the listed values"""


getLinksOnEmptyValid = [ 'False', 'raise', 'return' ]
getLinksOnNonEmptyValid = [ 'True', 'uid', 'item' ]

def getLinks(self,filter=None,onEmpty='return',onNonEmpty='uid',flatten=False):
  """Return dictionary of records linking to this record.
  
  Args
  ----
  filter:
  onEmpty: indicates action to be taken when dictionary is empty. Options are:
             'False': return false
             'raise': raise an exception
             'return': return the empty dictionary

  onNonEmpty: indicates action to be taken when dictionary is NOT empty. Options are:
             'True': return True
             'uid': return uids in a dictionary
             'item': return items in a dictionary
  
  """

  if onEmpty not in getLinksOnEmptyValid:
    raise InvalidCodeWordArgument( 'onEmpty value: %s not in valid list: %s' % (onEmpty, getLinksOnEmptyValid ) )
  if onNonEmpty not in getLinksOnNonEmptyValid:
    raise InvalidCodeWordArgument( 'onNonEmpty value: %s not in valid list: %s' % (onNonEmpty, getLinksOnNonEmptyValid ) )

  ee = {}
  for k in self._inx.iref_by_sect[self.uid].a.keys():
    if filter == None or k in filter:
      if len( self._inx.iref_by_sect[self.uid].a[k] ) > 0:
        ee[k] = self._inx.iref_by_sect[self.uid].a[k]

  if len(ee.keys()) == 0:
    if onEmpty == 'False':
      return False
    elif onEmpty == 'return':
      return {}
    else:
      raise EmptyLinkList()
  else:
    if onEmpty == 'True':
      return True
    elif onEmpty == 'uid':
      if flatten:
        l0 = []
        for k,ll in ee.items():
          l0 += ll
        return l0
      else:
        return ee
    else:
      ll = []
      for k,l0 in ee.items():
        for u in l0:
          ll.append( self._inx.uid.get( u, False ) )
        if not flatten:
          ee[k] = ll
          ll = []
      if not flatten:
        return ee
      else:
        return ll
 
    return ee
