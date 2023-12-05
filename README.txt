########### OPENING TWEDIT ###########

1. open terminal
2. type "cd CompuCell3D\"
3. type "./twedit++.command"
4. CC3D project
5. Open project
6. Click on the .cc3d file and open

The project is now open on twedit


########### CODING IN TWEDIT ###########

click on CC3D python on the top bar for prebuilt block of code

make sure to press control s or command s to save

you can comment out parts of the code using control / or command /



########### RUNNING SIMULAITON ###########

To run the simulation using twedit:

right click on the folder in the left section on twedit
click open in player


To run the simulation in terminal:

1. open terminal
2. type "cd CompuCell3D\"
3. type "./compucell3d.command"
4. open the folder to run the simulation



########### WHAT TO EDIT WHEN MODIFYING THE CODE ###########

NOTE ON CHANGING VALUES IN IF STATEMENTS:
- mcs: the time step of the simulation when the event starts
- random.random: generates a number between 0.0 and 1.0, to make an event more likely, make the number random.random must be less than greater
- cell.volume: controls the size the cells must be for an event to happen

XML FILE: 

Initial Position and Area of Cells:
- found in the XML file
- inside the UniformInitializer block of code
- EX: if you want to remove the macrophages from the simulation you would comment out the code in the UniformInitializer that is of type MAC

Contact Energies Between Cells:
-found in the XML file
-inside the Contact block of code
- EX: making the contact energy between Medium and LUM means they are not attracted to each other

Adding a New Cell Type:
- found in the XML file
- found in the CellType block of code
- when making a new cell type make sure to add the respective values for its contact energies


PYTHON STEPPABLES FILE:

ConstraintInitializer Class:
- controls the target volume of each cell type
- all of the volumes are relative to the cell volume
- to change the volumes of a cell type change the coefficient that is being multiplied by the constant (cellVol)

BreastDuctSim Class:
- contains the code for the cell killer

GrowthSteppable Class:
- controls the growth rate of cells
- only applies to the EPI cells since we don't want them to stop dividing
- to increase the rate of growth make the target volume increase by a larger value

MitosisSteppable Class:
- controls the preliferation of cells
- the division of each cell type is in their own respective for loop
- to modify the preliferation rates, change the if statements how it is described at the top of this section

CellMovementSteppable Class:
- Controls the movement of the MAC cells
- For information on how to edit it, refer to the comments in the class

PositionPlotSteppable Class:
- This class is for testing purposes which was used for CellMovementSteppable Class
- Editing it will not change the simulation so it is best to not touch it

FocalPointPlasticity Class
- This was going to be used to make MEM impermiable but was not used. It will be deleted in future versions


MAIN PYTHON FILE:
- this file should not be edited unless a new class is added to the python steppable file