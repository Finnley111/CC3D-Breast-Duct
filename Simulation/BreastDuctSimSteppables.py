from cc3d.core.PySteppables import *
import numpy as np
import random


class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        cellVol = 1000
        for cell in self.cell_list:
            cell.lambdaVolume = 15
            if cell.type == self.LUM:
                cell.targetVolume = .6*cellVol
            if cell.type == self.EPI:
                cell.targetVolume = .35*cellVol
            if cell.type == self.MYO:
                cell.targetVolume = .35*cellVol
            if cell.type == self.MEM:
                cell.targetVolume = .4*cellVol
            if cell.type == self.MAC_A:
                cell.targetVolume = .05*cellVol
            if cell.type == self.MAC_B:
                cell.targetVolume = .05*cellVol
                
                
    
    # def step(self,mcs):
        # for cell in self.cell_list_by_type(self.MEM):
            # if mcs > 1500 and random.random() < 0.00001 and cell.volume > 10:
               # self.delete_cell(cell)
               
        # for cell in self.cell_list_by_type(self.EPI):
            
            # neighbor_list = self.get_cell_neighbor_data_list(cell)
            # neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            # #print('Neighbor count for cell.id={} is {}'.format(cell.id, neighbor_count_by_type_dict))
            # if 1 not in neighbor_count_by_type_dict:
                # if random.random() < 0.01 and cell.volume > 15:
                    # self.delete_cell(cell)
            
            # if mcs > 1500 and random.random() < 0.0008 and cell.volume > 70:
               # self.delete_cell(cell)
               
               
               
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        # for cell in self.cell_list_by_type(self.EPI):
            # cell.targetVolume -= 3./2000.
            
        for cell in self.cell_list_by_type(self.MAC_A):
            cell.targetVolume += 150./2000.
            if cell.targetVolume> 100:
                cell.targetVolume -= 150./2000.
                
                
        
    
        # for cell in self.cell_list:
            # cell.lambdaVecX = 10.1 * uniform(-0.5, 0.5)
            # cell.lambdaVecY = 10.1 * uniform(-0.5, 0.5)
            
            # if mcs % 10 == 0:
                # for cell in self.cell_list_by_type(self.MEM):
                    # # using the plot:
                    # self.plot_win.add_data_point("Track",cell.xCOM,cell.yCOM)  # don't need int's
        
        for cell in self.cell_list_by_type(self.EPI):
            pixel_list = self.get_cell_pixel_list(cell)
            for pixel_tracker_data in pixel_list:
                x = pixel_tracker_data.pixel.x
                y = pixel_tracker_data.pixel.y
                
                #watch chemotaxis, define postion, define a hole
        
       
        lamX_lower_bound = -0.5
        lamX_upper_bound = 10.5 # 0.5 originally
        lamY_lower_bound = -0.5
        lamY_lower_bound = 10.5 # 0.5 originally
        for cell in self.cell_list_by_type(self.MAC_A):
            # force component pointing along X axis
            cell.lambdaVecX = 10.1 * random.uniform(lamX_lower_bound, lamX_upper_bound)

            # force component pointing along Y axis
            cell.lambdaVecY = 10.1 * random.uniform(lamY_lower_bound, lamX_upper_bound)

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):
        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.EPI, self.MYO,self.MEM):
            if cell.volume>30:
                cells_to_divide.append(cell)
        
        

        for cell in cells_to_divide:

            # self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)
        

        
            
        
    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2                 

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        # if self.parent_cell.type==1:
            # self.child_cell.type=2
        # else:
            # self.child_cell.type=1
            
        # Turns all voxels of SOURCE_CELL into voxels of DESTINATION_CELL
        # This function will merge the cells regardless of the distance between them.
        # It won't update the DESTINATION_CELL target volume.
        # Use with care.
        # self.merge_cells(SOURCE_CELL, self.MIC)


        