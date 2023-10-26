from cc3d.core.PySteppables import *
import numpy as np
import random


# This class is used to set the target volume of each cell type
class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        cellVol = 1000
        
        #this controls what each cell types' target volume will be
        #i.e how big it will grow before stoping
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
            
            # mcs: the monty carlo step of the simulation (time)
            if mcs > 1500 and random.random() < 0.00001 and cell.volume > 10:
               self.delete_cell(cell)
               
        
        # tracks the neighbor types of each EPI cell
        # will be used later to determine if there is a clump forming
        for cell in self.cell_list_by_type(self.EPI):
            
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            
            #print('Neighbor count for cell.id={} is {}'.format(cell.id, neighbor_count_by_type_dict))
            # cell is more likely to be killed if not neighboring the lumen
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
    
        # controls the rate of growth of the EPI cells
        # the other cells do not have a growth rate, they divide because of their initial volume
        # and are capped by their target volume
        for cell in self.cell_list_by_type(self.EPI):
            cell.targetVolume += 0.05
            #cell.targetSurface = 2.0*np.pi*np.sqrt(cell.targetVolume)



class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        # DIVISION OF EPI CELLS
        for cell in self.cell_list_by_type(self.EPI):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            
            # BEFORE 750 time steps the cells divide less frequently (helps control initial setup)
            if mcs < 750 and cell.volume>100 and random.random() < 0.01:
                cells_to_divide.append(cell)
            elif cell.volume>100 and random.random() < 0.1:
                cells_to_divide.append(cell)
            # if the neighbor is not the lumen, the chance for division is greater to make the simulation show more results
            elif 1 not in neighbor_count_by_type_dict:
                if cell.volume>25 and random.random() < 0.8:
                    cells_to_divide.append(cell)
                
        for cell in self.cell_list_by_type(self.MYO):
            if cell.volume>70: # the cell will divide if the cell has a volume greater than 70
                cells_to_divide.append(cell)
        
        for cell in self.cell_list_by_type(self.MEM):
            if cell.volume>30:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            # OTHER POSSIBLE WAYS TO DIVIDE CELLS
            # self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_minor_axis(cell)
            
           
            self.divide_cell_along_major_axis(cell)
            
            
            

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

        # declaring variables that will be used to find the position of each macrophage
        mac_X = 0.0
        mac_Y = 0.0
        
        # lower_bound and upper_bound is used in determining the direction of the MAC by using a random number generator
        lamX_lower_bound = 0.0
        lamX_upper_bound = 0.0 # 0.5 originally
        lamY_lower_bound = 0.0
        lamY_lower_bound = 0.0 # 0.5 originally
        num_of_mem_cells = 0
        pos_of_mems = []
        # this list has the position of the closest EPI cell to the corresponding MAC cell
        # this will be used to get the movement vectors for each MAC cell for best path
        pos_of_closest_epis = []
        # list of lists containing x and y vectors for the movements of each MAC cell
        mac_vectors = []

        # get position of macrophage
        for cell in self.cell_list_by_type(self.MAC):
            mac_X = cell.xCOM
            mac_Y = cell.yCOM
            # the initial value is set ridiculously high so it always passes the first if statement
            closest_epi = [10000000, 10000000] # the closest epithelial cell to the current MAC, it will be appended to pos_of_closest_epis
            #print(mac_X, ' ', mac_Y)
            
            # get position of macrophages and then position of epithelial cells
            # then use distance formula on coords to find closest one
            
            for epi_cell in self.cell_list_by_type(self.EPI):
                epi_X = epi_cell.xCOM
                epi_Y = epi_cell.yCOM
                
                if np.sqrt((epi_X - mac_X)**2+(epi_Y - mac_Y)**2) < np.sqrt((closest_epi[0] - mac_X)**2+(closest_epi[1] - mac_Y)**2):
                    
                    closest_epi[0] = epi_X
                    closest_epi[1] = epi_Y
                    
            if (mcs % 10 == 0):
                pos_of_closest_epis.append(closest_epi)
                print(closest_epi[0], ' ', closest_epi[1])
                
                
                
                
            
        # GOOD PROTOTYPE ON GETTING CLOSEST EPITHELIAL CELL POSITIONS
        # WILL HAVE TO DOUBLE CHECK LATER TO MAKE SURE IT IS WORKING AS INTENDED
        
        
        
        # get position and number of membrane cells
        for cell in self.cell_list_by_type(self.MEM):

            pos_of_mems.append((cell.xCOM, cell.yCOM))
        
        num_of_mem_cells = len(pos_of_mems)
            
        count = 0
        # this loop is responsible for taking the values and actually moving the macrophages
        for cell in self.cell_list_by_type(self.MAC):
            
            # use the modulos to control the individual cells in the list
            # i.e. this controls the first macrophage (order is clockwise)
            if count % 8 == 0:
                # force component pointing along X axis
                cell.lambdaVecX = 10.1 * random.uniform(0, 0)

                # force component pointing along Y axis
                cell.lambdaVecY = 10.1 * random.uniform(0, 0)
            elif count % 8 == 1:
                # force component pointing along X axis
                cell.lambdaVecX = 10.1 * random.uniform(0, 0)

                # force component pointing along Y axis
                cell.lambdaVecY = 10.1 * random.uniform(0, 0)
            elif count % 8 == 2:
                # force component pointing along X axis
                cell.lambdaVecX = 10.1 * random.uniform(0, 0)

                # force component pointing along Y axis
                cell.lambdaVecY = 10.1 * random.uniform(0, 0)
            else:
                # force component pointing along X axis
                cell.lambdaVecX = 10.1 * random.uniform(lamX_lower_bound, lamX_upper_bound)

                # force component pointing along Y axis
                cell.lambdaVecY = 10.1 * random.uniform(lamY_lower_bound, lamX_upper_bound)
            
            count = count + 1
            
            
            
            

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


####### THIS CLASS IS USED FOR THE GRAPH THAT SHOWS POSITION OF MEM ##########
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


######### THIS CLASS WILL BE USED TO MANAGE THE LINKS IN THE PYTHON STEPPABLE ##########
        
class FocalPointPlasticityCompartmentsParamsSteppable(SteppableBasePy):
    def __init__(self, frequency=1): #_simulator,
        '''
        constructor
        '''
        SteppableBasePy.__init__(self, frequency)
        # PLACE YOUR CODE BELOW THIS LINE
        # self.simulator = _simulator
        # self.focalPointPlasticityPlugin = CompuCell.getFocalPointPlasticityPlugin()
        # self.inventory = self.simulator.getPotts().getCellInventory()
        # self.cellList = CellList(self.inventory)
        

    def start(self):
        '''
        called once before first MCS
        '''
        # PLACE YOUR CODE BELOW THIS LINE
        

    def step(self, mcs):
        '''
        called every MCS or every "frequency" MCS (depending how it was instantiated in the main Python file)
        '''
        # PLACE YOUR CODE BELOW THIS LINE
                
        # for cell in self.cell_list_by_type(self.MEM):
            
            # for fppd in FocalPointPlasticityDataList(self.focalPointPlasticityPlugin, cell):
                # self.focalPointPlasticityPlugin.setFocalPointPlasticityParameters(cell, fppd.neighborAddress,
                                                                                                # 0.0, 0.0, 0.0)
            
        

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
