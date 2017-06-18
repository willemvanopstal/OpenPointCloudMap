# ChronoCity

__Installation__  
1. Install a (local) webserver. E.g. Apache Tomcat
2. Install all Python dependencies (see next section)
3. Download this entire repositery as .zip
4. Extract the zip into your webserver-webapps directory. Make sure the paths look like: <code>webapps/OPCM/chronocity-engine/..</code> and <code>webapps/OPCM/chronocity-viewer/..</code>
5. Download the AHN datasets in potree-structure here: <code>download</code>
6. Extract the two folders <code>AHN2</code> and <code>AHN3</code> and put them both under <code>chronocity-viewer/pointclouds/</code>
7. Get a LAStools license-file (.txt) and save it under <code>chronocity-engine/Tools/LAS_tools</code>
8. The ChronoCity-viewer is ready to view. You can access it through your webserver and browse to <code>/OPCM/chronocity-viewer/index.html</code>

__Python Dependencies__  
For the server-side running correctly, you should also make sure you have the following dependencies installed on your Python interpreter;  
- fiona
- laspy
- flask
- 







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
