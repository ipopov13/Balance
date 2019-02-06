MESSAGE point of view

Message/Objects (type)
- GetPlayerCommand/Loop to UI (query)
- ExecuteCommand/Loop to World (command, World will change)
-- TranslateCommandToIntent/World to Player (command, Player will change)
-- GetView/World to Player (command, World.View will change)
- DisplayView/Loop to UI (query)

The change in Scene can be any combination of:
- movement of creatures
- adding messages
- changing the UI
- changing the mode of operation (movement, look-around)
- displaying the inventory/character/crafting/etc. screen
All of these changes require further input from the player, and can be thought of as another run through the main message chain above.
To be able to supply all these views Scene has to have different modes of operation (provide views into different parts of the game: game-world, character stats of the plugged player, inventory of the plugged player, etc). It's not really a Scene, it's a View abstract superclass!

ABSTRACT INTERFACES
Presentable: implements the __str__() method that supplies a string describing the object. The string can be multi-line and the UI has to decide how to arrange all the items it has received on the screen based on the current View's requirements.

CLASSES

planned_tag(inheritances) name /comment

Message driven:
*UI /visual IO, manages the (private) Console object.
*(Presentable) World /game high level data management, specific world parameter values for each location (explicit or lazily discoverable through an algorithm)
View /abstract class covering all content that can be visualized on the screen following a player command and using the current active Being. Implements the interface needed to organize Presentable objects for rendering by the UI. Has hooks (that have to be filled by the subclasses) for requirements for visualization that are used by the UI to display each subclass instance (multiPageAllowed?, fixed size of elements by ID, etc.). There can be standard views (available for all Beings: scene, inventory, charsheet) and specialized views (defined for Beings with specific properties: crafting, research, spells)
(View) Scene /multi-object array (a.k.a. "current location") data management (environment and objects: "immobile" and "mobile" objects)
(View) Inventory /a View into the external properties of a Being object and its interface for structuring those properties (like inventory slots) - other objects that are attached to it for in-game reasons. The interface is really an internal property that has an undefined range of values and can be filled by any object that implements the respective interface.
(View) CharacterSheet /a View into the internal properties of a Being object that cannot be added or removed by gameplay, only modified in value in a certain predefined range. Some properties are not visible if they are not initialized (and thus not displayable)
(View) AvailableViews /a View listing all available Views for the current active (a.k.a. player-controlled) Being, with option for switching to each one.
(Presentable) GameObject /abstract class for all game objects that are not tile properties
(Gameobject) Item /passive subclass of game objects, containing only passive properties and methods (weight, hp, etc.)
*(Gameobject) Being /active abstract subclass of game objects, common active properties and methods (move, attack, pick up, interact with environment)

Emergent properties/functionalities:
1) Due to any Being being pluggable in standard Views like Inventory/CharSheet a hidden debugging feature can be to switch to another Being to view its specific instance properties!

Expected:
(Presentable) Environment /abstract class for terrains and effects (tile properties)
(Environment) Terrain /passive tile properties that define available actions for actors
(Environment) Effect /active visible or invisible tile properties that make modifications to actions or actors
(Presentable) InventoryInterface /abstract class for the Inventory slot properties. Objects that can be attached to a specific interface have to implement it (helmets and hats implement the HeadSlot interface, almost any object that can be held implements the HandSlot interface, etc)
(Presentable) CharacterProperty /abstract class for properties shown in a CharacterSheet View. Each subclass has a single instance with an IsInitialized? property, a range, and a current value within that range. Presenting strings return the actual visual representation.

Needed?:
Tile /the smallest physical spot in the game world, the place taken up by a regular size actor/item
(Being) Npc /computer controlled actives implementing the movement algorithms and other AI :P
(Being) Player /player controlled active instance with IO hooks for actions

MAIN LOOP
If an action causes a cascade of changes they can be returned by world.run() and will be run before another command is gotten from the player. Example is player character death: the world returns a death command that is evaluated, causing the world to go to the "game over" screen and change world.isAlive to False, breaking the loop.
