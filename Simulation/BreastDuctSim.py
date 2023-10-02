
from cc3d import CompuCellSetup
        


from BreastDuctSimSteppables import ConstraintInitializerSteppable

CompuCellSetup.register_steppable(steppable=ConstraintInitializerSteppable(frequency=1))



from BreastDuctSimSteppables import BreastDuctSim

CompuCellSetup.register_steppable(steppable=BreastDuctSim(frequency=1))




from BreastDuctSimSteppables import GrowthSteppable

CompuCellSetup.register_steppable(steppable=GrowthSteppable(frequency=1))




from BreastDuctSimSteppables import MitosisSteppable

CompuCellSetup.register_steppable(steppable=MitosisSteppable(frequency=1))




from BreastDuctSimSteppables import CellMovementSteppable
CompuCellSetup.register_steppable(steppable=CellMovementSteppable(frequency=1))


        
from BreastDuctSimSteppables import PostionPlotSteppable
CompuCellSetup.register_steppable(steppable=PostionPlotSteppable(frequency=1))


        
from BreastDuctSimSteppables import FocalPointPlasticityCompartmentsParamsSteppable
CompuCellSetup.register_steppable(steppable=FocalPointPlasticityCompartmentsParamsSteppable(frequency=1))

CompuCellSetup.run()
