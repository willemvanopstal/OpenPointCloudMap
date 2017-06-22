## Demo
A functional online demo can be found at: www.chronocity.net
_(22-6-2017)_  

Before executing a change detection, make sure the service is running by browsing to www.chronocity.net:12839/test  

# ChronoCity

__Installation__
1. Install a (local) webserver. E.g. Apache Tomcat
2. Install all Python dependencies (see next section)
3. Download this entire repositery as .zip
4. Extract the zip into your webserver-webapps directory. Make sure the paths look like: <code>webapps/OPCM/chronocity-engine/..</code> and <code>webapps/OPCM/chronocity-viewer/..</code>
5. Download the AHN datasets in potree-structure here: <code>download</code>
6. Extract the two folders <code>AHN2</code> and <code>AHN3</code> and put them both under <code>chronocity-viewer/pointclouds/</code>
7. Get a LAStools license-file (.txt) and save it under <code>chronocity-engine/Tools/LAS_tools</code>
8. The ChronoCity-viewer is ready to view. You can access it through your webserver and browse to <code>domain:port/OPCM/</code>

__Python Dependencies__
For the server-side running correctly, you should also make sure you have the following dependencies installed on your Python interpreter;
- fiona
- laspy
- flask
- copy
- os
- json
- multiprocessing
- time
- shutil
- shapely

__Setup__

1. In <code>/OPCM/chronocity-engine/server_service.py</code> at the bottom you should replace the two paths <code> serv_path</code> and <code>potree_path</code> with the path to the two installations folders like below. Be aware of the double '\\' ! The server listens to port _12839_ by default, but you can specify it yourself if needed.


        port = 12839
        serv_path = "C:\\geo1007\\apache-tomcat-8.5.14\\webapps\\OPCM\\chronocity-engine\\"
        potree_path = "C:\\geo1007\\apache-tomcat-8.5.14\\webapps\\OPCM\\chronocity-viewer\\"

2. Run the <code>server_service.py</code> to start the server. You can test if it is running correctly by browsing to <code>localhost:12839/test</code> in your browser. It will return the message _ACTIVE_ if it is running.

3. The viewer runs on port _8080_ by default and relies on the default value for the server-side. If you have changed the default port, you should edit <code>OPCM/chronocity-viewer/build/potree/potree.js</code> and search for _localhost:_. Replace the entries with your custom ports.

__Console controls__
All important interactions can be done within the GUI. There are also some other usefull command for more control. You can use these in your browser's webconsole;

    getActivePC();                     # returns a list of the visible pointclouds [AHN2, AHN3, AHN23, AHN32]
    checkLayers(bool,bool,bool,bool)   # sets the visibility for all layers (AHN2, AHN3, AHN23, AHN32)
    toggleAHN()                        # toggles the view between AHN2 and AHN3
    saveAsImage()                      # saves the current view as a .png image (prompt)
    
