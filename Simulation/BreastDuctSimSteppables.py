from cc3d.core.PySteppables import *
import numpy as np
import random

# This class is used to set the target volume of each cell type
class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        cellVol = 1000
        
        for cell in self.cell_list:
            
            cell.lambdaVolume = 10
            if cell.type == self.LUM:
                cell.targetVolume = .6*cellVol
            if cell.type == self.EPI:
                cell.targetVolume = .4*cellVol
            if cell.type == self.MYO:
                cell.targetVolume = .5*cellVol
            if cell.type == self.MEM:
                cell.targetVolume = .4*cellVol
            
                

class BreastDuctSim(SteppableBasePy):

    def __init__(self,frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        cellVol = 1000
        for cell in self.cell_list:
            cell.lambdaVolume = 10
            if cell.type == self.LUM:
                cell.targetVolume = .6*cellVol
            if cell.type == self.EPI:
                cell.targetVolume = .4*cellVol
            if cell.type == self.MYO:
                cell.targetVolume = .5*cellVol
            if cell.type == self.MEM:
                cell.targetVolume = .4*cellVol
            if cell.type == self.MAC:
                cell.targetVolume = .05*cellVol
        
        # make a plot of the cells positions
        self.plot_win = self.add_new_plot_window(title='MEM COM Track',
                                                 x_axis_title='X', x_scale_type='linear',
                                                 y_axis_title='Y', y_scale_type='linear',
                                                 grid=False)
        self.plot_win.add_plot("Track", style='dot', color='white', size=1)
        # make some dots to force the plot to autoscale like we want (0,0),(100,100)
        # arguments are (name of the data series, x, y)
        self.plot_win.add_data_point("Track",0,    0)
        self.plot_win.add_data_point("Track",0,  100)
        self.plot_win.add_data_point("Track",100,  0)
        self.plot_win.add_data_point("Track",100,100)

    def step(self,mcs):
        for cell in self.cell_list_by_type(self.MEM):
            
            if mcs > 1500 and random.random() < 0.00001 and cell.volume > 10:
               self.delete_cell(cell)
               
               
        for cell in self.cell_list_by_type(self.EPI):
            
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            
            #print('Neighbor count for cell.id={} is {}'.format(cell.id, neighbor_count_by_type_dict))
            if 1 not in neighbor_count_by_type_dict:
                if random.random() < 0.01 and cell.volume > 15:
                    self.delete_cell(cell)
            
            if mcs > 1500 and random.random() < 0.0008 and cell.volume > 70:
               self.delete_cell(cell)
              
              
        # This is not really needed, can delete later same with code above that create the graph
        # just tracking the center of "MEM" type every 100th MCS
        if mcs % 10 == 0:
            for cell in self.cell_list_by_type(self.MEM):
                # using the plot:
                # THIS TRACKS THE CENTER OF MASS OF MEM
                #self.plot_win.add_data_point("Track",cell.xCOM,cell.yCOM)
                
                # THIS TRACKS EACH PIXEL OF MEM
                pixel_list = self.get_cell_pixel_list(cell)
                for pixel_tracker_data in pixel_list:
                    x = pixel_tracker_data.pixel.x
                    y = pixel_tracker_data.pixel.y
                    self.plot_win.add_data_point("Track",x,y)
                        
               
        # Make sure ExternalPotential plugin is loaded
        # negative lambdaVecX makes force point in the positive direction
        # THIS CONTROLS THE MOVEMENT OF THE MACROPHAGE

        mac_X = 0.0
        mac_Y = 0.0
        lamX_lower_bound = -0.5
        lamX_upper_bound = 10.5 # 0.5 originally
        lamY_lower_bound = -0.5
        lamY_lower_bound = 10.5 # 0.5 originally
        num_of_mem_cells = 0
        pos_of_mems = []

        # get position of macrophage
        for cell in self.cell_list_by_type(self.MAC):
            mac_X = cell.xCOM
            mac_Y = cell.yCOM
            print(mac_X, ' ', mac_Y)
            
        # LOOK UP: HOW TO GET THE VECTOR FROM TWO POINTS TO CONTROL THE DIRECTION OF THE MACROPHAGE
            
        
        # get position and number of membrane cells
        for cell in self.cell_list_by_type(self.MEM):

            pos_of_mems.append((cell.xCOM, cell.yCOM))
        
        num_of_mem_cells = len(pos_of_mems)
            
        
        
        for cell in self.cell_list_by_type(self.MAC):
            # force component pointing along X axis
            cell.lambdaVecX = 10.1 * random.uniform(lamX_lower_bound, lamX_upper_bound)

            # force component pointing along Y axis
            cell.lambdaVecY = 10.1 * random.uniform(lamY_lower_bound, lamX_upper_bound)

    def finish(self):
        """
        Finish Function is called after the last MCS
        """

    def on_stop(self):
        # this gets called each time user stops simulation
        return


class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
    
        for cell in self.cell_list_by_type(self.EPI):
            cell.targetVolume += 0.05
            #cell.targetSurface = 2.0*np.pi*np.sqrt(cell.targetVolume)
            
        # iterating over cells of type 1
        # list of  cell types (capitalized)
        
        
        # for cell in self.cell_list_by_type(self.MEM):
            # pixel_list = self.get_cell_pixel_list(cell)
            # for pixel_tracker_data in pixel_list:
                # # you can access/manipulate cell properties here
                # x = pixel_tracker_data.pixel.x
                # y = pixel_tracker_data.pixel.y
                
                


class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):
        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.EPI):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            
            if mcs < 750 and cell.volume>100 and random.random() < 0.01:
                cells_to_divide.append(cell)
            elif cell.volume>100 and random.random() < 0.1:
                cells_to_divide.append(cell)
            elif 1 not in neighbor_count_by_type_dict:
                if cell.volume>25 and random.random() < 0.8:
                    cells_to_divide.append(cell)
                
        for cell in self.cell_list_by_type(self.MYO):
            if cell.volume>70:
                cells_to_divide.append(cell)
        
        for cell in self.cell_list_by_type(self.MEM):
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
        
            

from cc3d.core.PySteppables import *
import numpy as np


        
class NeighborTrackerSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        '''
        constructor
        '''
        SteppableBasePy.__init__(self, frequency)
        # PLACE YOUR CODE BELOW THIS LINE
        

    def start(self):
        '''
        called once before first MCS
        '''
        # PLACE YOUR CODE BELOW THIS LINE
        
        print("NeighborTrackerSteppable: This function is called once before simulation")

    def step(self, mcs):
        '''
        called every MCS or every "frequency" MCS (depending how it was instantiated in the main Python file)
        '''
        
        for cell in self.cell_list_by_type(self.EPI):
            # PLACE YOUR CODE BELOW THIS LINE
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            #print('Neighbor count for cell.id={} is {}'.format(cell.id, neighbor_count_by_type_dict))
            if 1 not in neighbor_count_by_type_dict:
                print(neighbor_count_by_type_dict)

    def finish(self):
        '''
        this function may be called at the end of simulation - used very infrequently though
        '''        
        # PLACE YOUR CODE BELOW THIS LINE
        
        return

    def on_stop(self):
        '''
        this gets called each time user stops simulation
        '''        
        # PLACE YOUR CODE BELOW THIS LINE
        
        return
