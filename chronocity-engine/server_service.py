from flask import Flask
from flask import request
from flask import Response
import prepare_pointclouds
from shapely.geometry import mapping, Polygon, shape
import fiona

app = Flask(__name__)

# This is a testing route. It will return a response saying it is active.
#  If the server is not active, of course no response will be given
@app.route('/test', methods=['GET'])
def testService():
    response = Response("The ChronoCity-service is ACTIVE.")  # This is the response-variable, with Response() from flask
    response.headers['Access-Control-Allow-Origin'] = '*'  # This is important to let javascript accept the response

    return response  # Then simply return the Response() object


def handle_coords(polygon, sys_par):

    # Set the history-clip shapefile path
    pth = sys_par[0] + 'Clips\\clips.shp'

    # Get all previous clipping history as a merged Polygon geometry
    try:
        with fiona.open(pth) as c:
            multi_old = shape(c[0]['geometry'])

            # Increase the clipping counter by one more
            fname = str(int(c[0]['properties']['id'])+1)
    except:
        # There is no previous polygon in the history.. So build an empty one to begin with.
        multi_old = Polygon()
        fname = str(1)

    # Clean the user's input of coordinates
    geom = [(float(p1[0]), float(p1[1])) for p1 in [p0.split(", ") for p0 in polygon[1:-1].split(")(")]]

    # If the user's polygon is not valid, reduce-correct it.
    poly = Polygon(geom).buffer(0)

    # Remove from it, all previously used clipping areas
    fin_polygon = poly.difference(multi_old)
    multi_new = poly.union(multi_old)

    if not fin_polygon.is_empty:

        clip_path = "Tools/LAS_Tools/clipping_polygon.shp"

        # Write a new Shapefile to be used as the new single clip polygon
        with fiona.open(sys_par[0]+clip_path, 'w', 'ESRI Shapefile',
                        {'geometry': 'Polygon', 'properties': {'id': 'int'}}) as c:
            c.write({'geometry': mapping(fin_polygon), 'properties': {'id': 0}})

        # Get the boundaries of the new (clean) clipping area
        bb = poly.bounds

        coordinate_list = {"max": [bb[2], bb[3]], "min": [bb[0], bb[1]]}

        # Replace the history clipping shapefile
        with fiona.open(sys_par[0]+'Clips/clips.shp', 'w', 'ESRI Shapefile',
                        {'geometry': 'Polygon', 'properties': {'id': 'int'}}) as c:
            c.write({'geometry': mapping(multi_new), 'properties': {'id': fname}})

        # Continue with the point cloud preparation.
        prepare_pointclouds.init_pc_preparation(coordinate_list, fname, sys_par)

        # Get the centroid of the area
        cent = fin_polygon.centroid

        return str(cent.x), str(cent.y), str(0)  #, str("Change-detection process has started.")

    # The requested differences have probably been already calculated
    else:
        # Get the centroid of the area
        cent = poly.centroid

        return str(cent.x), str(cent.y), str(0)


# This (below) is where the GET-requests ends up. It will return a response to the javascript request.
#
# The HTTP request from Javascript comes in just after @app.route.
# The request is now sending only one parameter: 'coords'. That parameter is grabbed by request.args['coords']
# The parameter for the polygon is setup like this:
#
# coords = (x1, y1, z1)(x2, y2, z2)(x3, y3, z3)    type[string]

# It is sorted so; point1, point2, point3 etc.
# These are also still sent with the request. So this could happen; (p1,p2,p2,p3,p4) (and happens)

@app.route('/', methods=['GET'])
def showWKT():

    if 'coords' in request.args:
        coords = request.args['coords']

        # Store the system parameters to pass them throughout the processing.
        sys_par = (serv_path, potree_path)

        (ax, ay, az) = handle_coords(coords, sys_par)  # Here, the above function is called using the variable
        middle = ax + ', ' + ay + ', ' + az
        # The return values are stored in another one.

    response = Response(middle)  # This is the response-variable, with Response() from flask
    response.headers['Access-Control-Allow-Origin'] = '*'  # This is important to let javascript accept the response

    return response  # Then simply return the Response() object

if __name__ == '__main__':
    #port = raw_input('Specify service running port (e.g. "12839"): ')
    print "You can test if the service is running by visiting this address: http://localhost:12839/test"
    port = 12839

    #serv_path = raw_input('Specify the change detection service path: (e.g. "E:\\ChronoCity-CD-Server-Engine\\")')
    serv_path = "C:\\geo1007\\apache-tomcat-8.5.14\\webapps\\OPCM\\chronocity-engine\\"

    #potree_path = raw_input('Specify the Potree path: (e.g. "C:\\apache-tomcat-8.5.14\\webapps\\chronocity\\")')
    potree_path = "C:\\geo1007\\apache-tomcat-8.5.14\\webapps\\OPCM\\chronocity-viewer\\"

    app.run('', port)
