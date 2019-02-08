Tree of dependence:

Balance -> PlayerController
PlayerController -> View, Scene, World
View -> Interface?(not created yet)
Scene -> none
World -> GameObject

See the documentation strings in each class for details.

ABSTRACT INTERFACES

Presentable: implements the __str__() method that supplies a string describing the object. The string can be multi-line and the UI has to decide how to arrange all the items it has received on the screen based on the current View's requirements.