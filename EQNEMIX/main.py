# Main module for EQNEMIX
# EQNEMIX/main.py
import numpy as np
import matplotlib.pyplot as plt
from nllgrid import NLLGrid
import geopandas as gpd


class eqnegrid:
   def __init__(self, fileextent='extent.shp', inputsrc=4326, outputcrs=3587, 
                  filesp='Vsp.npy',files='vs.npy', filep='vp.npy', deltadist=1000, **kwargs):
        """
        Constructor to initialize the EQNEGRID class.

        :param fileextent: Extension file, default is 'extent.shp'
        :param inputsrc: Input source, default is 4326
        :param outputcrs: Output coordinate reference system, default is 3587
        :param filesp: Numpy file, default is 'Vsp.npy'
        :param filep: P file, default is ''vp.npy'
        :param files: S file, default is 'vs.npy'
        :param deltadist: Number of cells in the grid, is the value in meters, default is 1000
        :param kwargs: Additional optional parameters.
        """
        self.fileextent = fileextent
        self.inputsrc = inputsrc
        self.outputcrs = outputcrs
        self.filesp = filesp
        self.filep = filep
        self.files = files
        self.deltadist = deltadist
        gdf = gpd.read_file(fileextent)
        self.inputcrs= gdf.crs
        gdf = gdf.to_crs(epsg=self.outputcrs)
        polygon = gdf.geometry.iloc[0]
        self.minx, self.miny, self.maxx, self.maxy = polygon.bounds
        #print(f"minx: {minx}, miny: {miny}")
        self.length_x = self.maxx - self.minx
        self.length_y = self.maxy - self.miny
        self.elements_x = int(self.length_x // self.deltadist)
        self.elements_y = int(self.length_y // self.deltadist)
        self.max_elements = max(self.elements_x, self.elements_y)
        #print(f"Elements in x: {elements_x}, Elements in y: {elements_y}")
        self.nx = self.max_elements
        self.ny = self.max_elements
        self.nz = self.max_elements
        
        self.dx, self.dy, self.dz = self.deltadist, self.deltadist,self.deltadist  
        self.x_orig=self.minx
        self.y_orig=self.miny
        self.z_orig=0
        self.gridp = NLLGrid(
        nx=self.nx, ny=self.ny, nz=self.nz,
        dx= self.dx, dy=self.dy, dz=self.dz,
        x_orig=self.x_orig, y_orig=self.y_orig, z_orig=self.z_orig

        )
        self.gridp.orig_lat = 0.0  # Asigna un valor predeterminado adecuado
        self.gridp.orig_lon = 0.0  # Asigna un valor predeterminado adecuado
        self.gridp.map_rot = 0.0   # Asigna un valor predeterminado adecuado
        self.gridp.proj_name = 'SIMPLE'  #

        self.gridp.init_array() 
        self.grids = NLLGrid(
        nx=self.nx, ny=self.ny, nz=self.nz,
        dx=self.dx, dy=self.dy, dz=self.dz,
        x_orig=self.x_orig, y_orig=self.y_orig, z_orig=self.z_orig
        )
        self.grids.orig_lat = 0.0  # Asigna un valor predeterminado adecuado
        self.grids.orig_lon = 0.0  # Asigna un valor predeterminado adecuado
        self.grids.map_rot = 0.0   # Asigna un valor predeterminado adecuado
        self.grids.proj_name = 'SIMPLE'  # Asegúrate de que esta proyección esté definida y sea válida

        self.grids.init_array()

        self.gridp.float_type = 'FLOAT'  
        self.gridp.type = 'VELOCITY'  
        self.gridp.proj_name = 'SIMPLE'
        self.gridp.basename = 'Vp_grid'
        self.grids.float_type = 'FLOAT'  
        self.grids.type = 'VELOCITY'  
        self.grids.proj_name = 'SIMPLE'
        self.grids.basename = 'Vs_grid'
        self.grids.map_rot=0
        self.gridp.map_rot=0



   def print_variables(self):
        """
        Print Variables
        """
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")

   def print(*args, **kwargs):
         print_variables("EQNEMIX PARAMETERS:", *args, **kwargs)
   def savefiles(self,basefile):
        """
        Save al the files for next step

       :param basefile: 'Prefix for hdr and buf'

        
        """
        self.gridp.basename = basefile+'vp'
        self.grids.basename = basefile+'vs'
        self.gridp.write_hdr_file()
        self.gridp.write_buf_file()
        self.grids.write_hdr_file()
        self.grids.write_buf_file()
        new_velp = self.gridp.array
        new_vels = self.grids.array
        np.save(self.filep, new_velp)
        np.save(self.files, new_vels)
 
 
