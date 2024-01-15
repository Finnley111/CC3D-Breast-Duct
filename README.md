# CC3D-Breast-Duct

## Twedit Usage Guide

### Opening Twedit

1. Open terminal.
2. Type `cd CompuCell3D/`.
3. Type `./twedit++.command`.
4. Select 'CC3D project'.
5. Choose 'Open project'.
6. Click on the `.cc3d` file to open.

The project is now open in Twedit.

### Coding in Twedit

- Click on 'CC3D Python' on the top bar for prebuilt blocks of code.
- Remember to save your work using `Ctrl + S` or `Cmd + S`.
- You can comment out parts of the code using `Ctrl + /` or `Cmd + /`.

## Running Simulation

### Using Twedit

- Right-click on the folder in the left section of Twedit.
- Select 'Open in Player'.

### Using Terminal

1. Open terminal.
2. Type `cd CompuCell3D/`.
3. Type `./compucell3d.command`.
4. Open the folder to run the simulation.

## Editing Code Guidelines

### Notes on Modifying IF Statements

- `mcs`: Time step of the simulation when the event starts.
- `random.random()`: Generates a number between 0.0 and 1.0. To make an event more likely, increase the threshold.
- `cell.volume`: Controls the size the cells must be for an event to happen.

### XML File

**Initial Position and Area of Cells:**
- Found in the `UniformInitializer` block.
- Example: To remove macrophages, comment out the corresponding code in `UniformInitializer` of type `MAC`.

**Contact Energies Between Cells:**
- Located in the `Contact` block.
- Example: Setting the contact energy between `Medium` and `LUM` to indicate non-attraction.

**Adding a New Cell Type:**
- Located in the `CellType` block.
- Ensure to add respective values for its contact energies.

### Python Steppables File

**ConstraintInitializer Class:**
- Sets target volume for each cell type.
- Change the coefficient multiplied by the constant (`cellVol`) to adjust volumes.

**BreastDuctSim Class:**
- Contains code for the cell killer.

**GrowthSteppable Class:**
- Manages growth rate of cells, primarily `EPI` cells.
- Increase target volume increment to boost growth rate.

**MitosisSteppable Class:**
- Governs cell proliferation.
- Modify the proliferation rates as described in the initial notes.

**CellMovementSteppable Class:**
- Manages movement of `MAC` cells.
- Refer to comments in the class for editing guidance.

**PositionPlotSteppable Class:**
- Used for testing `CellMovementSteppable`.
- Avoid editing as it doesn't impact the simulation.

**FocalPointPlasticity Class:**
- Intended for making `MEM` impermeable, but not used in current versions.

### Main Python File

- Avoid editing unless adding new classes to the Python steppable file.
