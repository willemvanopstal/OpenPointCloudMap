# ChronoCity

This is a fully built potree-package. You can both launch them from simply clicking the 'index.html' or run it from a webserver.

__Folder structure and Point clouds__   
You should check the 'index.html' for the pointclouds you want to load. Just by editing the paths. Do not change the names, these are used for selecting the active layers.

            Potree.loadPointCloud("pointclouds/AHN2/cloud.js", "AHN2", e1 => {
			viewer.scene.addPointCloud(e1.pointcloud);
			e1.pointcloud.visible = true;
		});
		
		Potree.loadPointCloud("pointclouds/AHN3/cloud.js", "AHN3", e2 => {
			viewer.scene.addPointCloud(e2.pointcloud);
			e2.pointcloud.visible = false;
		});

		Potree.loadPointCloud("pointclouds/AHN2-AHN3/cloud.js", "AHNDelta23", e => {
			viewer.scene.addPointCloud(e.pointcloud);
			e.pointcloud.visible = false;
		});

		Potree.loadPointCloud("pointclouds/AHN3-AHN2/cloud.js", "AHNDelta32", e => {
			viewer.scene.addPointCloud(e.pointcloud);
			e.pointcloud.visible = false;
		});  
    
__Console controls__  
All important interactions can be done within the GUI. There are also some other usefull command for more control. You can use these in your browser's webconsole;  

    getActivePC();                     # returns a list of the visible pointclouds [AHN2, AHN3, AHN23, AHN32]
    checkLayers(bool,bool,bool,bool)   # sets the visibility for all layers (AHN2, AHN3, AHN23, AHN32)
    toggleAHN()                        # toggles the view between AHN2 and AHN3
    saveAsImage()                      # saves the current view as a .png image (prompt)
    
__Change Detection__  
For the change-detection to work, it's needed to run the 'pylistener.py'. You can test if it's running properly by putting the following in your browser or http client;  
    
    localhost:12839/test
    
This version __does not support on-the-fly__ change detection. Before that to work you should uncomment a few lines in the 'pylistener.py';  

    ##import prepare_pointclouds
    '''
    wr_path = "E:\GIT_Projects\ChronoCity-CD-Server-Engine\Tools\LAS_Tools\clipping_polygon.txt"
    # Store the file
    with open(wr_path, 'w') as fn:
        for point in range(len(coord_dict)):
            fn.write(str(coord_dict[point][0]) + " " + str(coord_dict[point][1]) + "\n")
        fn.write(str(coord_dict[0][0]) + " " + str(coord_dict[0][1]) + "\n")
    '''
    ##prepare_pointclouds.init_pc_preparation(coordinate_list)  
    
__Dependencies__  
Of course, you need to have the associated programs installed on the right location.
* prepare_pointclouds.py
* laszip.exe
* lasclip.exe ....
* ...
* ...

    
    
