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
            if cell.type == self.MAC:
                cell.targetVolume = .05*cellVol
            
                

class BreastDuctSim(SteppableBasePy):

    def __init__(self,frequency=1):

        SteppableBasePy.__init__(self,frequency)
 

    # CELL KILLER CODE/ LIMITS NUMBER OF EACH CELL TYPE
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
               
        ############# NEIGHBOR TRACKING CODE FOR LATER USE #################
        # for cell in self.cell_list_by_type(self.EPI):
            # # PLACE YOUR CODE BELOW THIS LINE
            # neighbor_list = self.get_cell_neighbor_data_list(cell)
            # neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            # #print('Neighbor count for cell.id={} is {}'.format(cell.id, neighbor_count_by_type_dict))
            # if 1 not in neighbor_count_by_type_dict:
                # print(neighbor_count_by_type_dict)


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
        
        # for cell in self.cell_list_by_type(self.MEM):
            # cell.targetVolume += 150./2000.
            # if mcs> 100:
                # cell.targetVolume -= 150./2000.



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


class CellMovementSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        '''
        constructor
        '''
        SteppableBasePy.__init__(self, frequency)
        

    def start(self):
        
        print("CellMovementSteppable: This function is called once before simulation")

    def step(self, mcs):
        '''
        called every MCS or every "frequency" MCS (depending how it was instantiated in the main Python file)
        '''
        # Make sure ExternalPotential plugin is loaded
        # negative lambdaVecX makes force point in the positive direction
        # THIS CONTROLS THE MOVEMENT OF THE MACROPHAGE

        mac_X = 0.0
        mac_Y = 0.0
        lamX_lower_bound = 0.0
        lamX_upper_bound = 0.0 # 0.5 originally
        lamY_lower_bound = 0.0
        lamY_lower_bound = 0.0 # 0.5 originally
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
        '''
        this function may be called at the end of simulation - used very infrequently though
        '''        
        
        return

    def on_stop(self):
        '''
        this gets called each time user stops simulation
        '''        
        
        return


class PostionPlotSteppable(SteppableBasePy):
    
    def __init__(self, frequency=10):
        SteppableBasePy.__init__(self, frequency)


    def start(self):
        # make a plot of the cells positions
        self.plot_win = self.add_new_plot_window(title='MEM COM Track',
                                                 x_axis_title='X', x_scale_type='linear',
                                                 y_axis_title='Y', y_scale_type='linear',
                                                 grid=False)
        self.plot_win.add_plot("Track", style='dot', color='white', size=1)
        # make some dots to force the plot to autoscale like we want (0,0),(100,100)
        # arguments are (name of the data series, x, y)
        self.plot_win.add_data_point("Track",0,    0)
        self.plot_win.add_data_point("Track",0,  200)
        self.plot_win.add_data_point("Track",200,  0)
        self.plot_win.add_data_point("Track",200,200)


    def step(self, mcs):
         
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
                    
        if mcs % 100 == 0:
            self.plot_win.erase_all_data()
            self.plot_win.add_data_point("Track",0,    0)
            self.plot_win.add_data_point("Track",0,  200)
            self.plot_win.add_data_point("Track",200,  0)
            self.plot_win.add_data_point("Track",200,200)
      
      
class LinkSteppable(SteppableBasePy):
    
        
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)
        def start(self):
            
            print("link steppable is working")
            
        def step(self, mcs):
            # LAMBDA = 2
            # TARGET_DISTANCE = 0
            # MAX_DISTANCE = 1000
            if (mcs > 1000):
                for cell in self.cell_list_by_type(self.MEM):
                        # Make sure FocalPointPlacticity plugin is loaded
                        # Arguments are:
                        # initiator: CellG, initiated: CellG, lambda_distance: float, target_distance: float, max_distance: float
                    link = self.new_fpp_link(cell, cell, 10)
                        
                        
                        
                    