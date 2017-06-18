# -*- coding: utf-8 -*-
import json
import os
import laspy
from voxel_grid import VoxelGrid
from multiprocessing import Pool
import time
import pc_parser
import shutil


def clipper(args):
    print "Start the clipping"
    t, files_path, prm, coordinate_list = args

    # The path where the point_cloud_list will be stored (this list is needed in case the area belongs to many tiles)
    clipper_path = prm[t][3][0] + 'Tools\\LAS_Tools\\'

    # Prepare the CMD command
    c5 = " -merged -odir " + files_path + " -o "
    poly = " -poly " + clipper_path + "clipping_polygon.shp -donuts"

    # Find the Tile candidates based on the selected area.
    clip_candidates = []

    with open(prm[t][3][1] + prm[t][2] + "sources.json") as data_file:
        data = json.load(data_file)

    # For every tile:
    for point_cloud in data['sources']:
        if point_cloud['bounds']['min'][1] < coordinate_list['max'][1] \
                and coordinate_list['min'][1] < point_cloud['bounds']['max'][1] \
                and point_cloud['bounds']['min'][0] < coordinate_list['max'][0] \
                and coordinate_list['min'][0] < point_cloud['bounds']['max'][0]:

            # Add the tile into the clipping candidates
            clip_candidates.append(prm[t][3][1] + prm[t][2] + "source/" + point_cloud['name'])

            # Stop searching within this tile
            pass

    # Store the file
    with open(clipper_path + prm[t][0], 'w') as clp:
        for point_cloud in clip_candidates:
            clp.write(point_cloud+"\n")

    clip_command = clipper_path + "lasclip.exe -lof " + clipper_path + prm[t][0] + poly + c5 + prm[t][1]

    # Execute the clipping in a new process
    process = os.popen(clip_command)
    process.close()

def change_detection(files_path, prm, diff_uid):
    # Set the distance threshold. This will also be the voxel size
    change_detection_threshold = 5

    # Square the distance because during calculations no square root will be computed
    cd_thresh = change_detection_threshold ** 2

    # Grab all of the points from the file.
    pc_a_file = laspy.file.File(files_path + prm["t1"][1], mode="r")

    # Grab all of the points from the file.
    pc_b_file = laspy.file.File(files_path + prm["t2"][1], mode='r')

    # This is the 1st prepared point cloud
    pc_a = (pc_a_file.x, pc_a_file.y, pc_a_file.z)
    print "Number of points in 1st point cloud:", len(pc_a[0])

    # This is the 2nd prepared point cloud
    pc_b = (pc_b_file.x, pc_b_file.y, pc_b_file.z)
    print "Number of points in 2nd point cloud:", len(pc_b[0])

    print "Start building the voxel grid"
    # Get the origin point that will be used to build the Voxel Grid, from the combined minimum extents
    origin_point = pc_parser.combined_extent(pc_a_file.header, pc_b_file.header)

    # Generate a Voxel Grid object, based on a voxel size and the origin corner point.
    voxel_grid = VoxelGrid(origin_point, change_detection_threshold)

    # Fill the grid with the points
    pc_parser.prepare_grid(voxel_grid, (pc_a, pc_b))

    print "Start detecting 1st difference"
    # Detect 1st change order between point clouds and return the needed arrays
    diff_BA = pc_parser.detect_changes(voxel_grid, 1, 0, cd_thresh)

    if len(diff_BA[0]) > 0:
        # Prepare the file paths
        save_path = "{0}Point_Clouds\\temp\\t2t1_{1}.las".format(prm["t2"][3][0], diff_uid)
        print "1", save_path
        # Store the differences from the new point cloud to the old one
        pc_parser.store_diffs(diff_BA, pc_b_file, save_path)

        # Publish the new calculated differences
        command21 = prm["t2"][3][0] + 'Tools\\PotreeConverter_1.5RC_windows_64bit\\PotreeConverter.exe ' + \
                    save_path + ' -o ' + prm["t2"][3][1] + \
                    'pointclouds\\AHN3-AHN2 --output-format LAZ --projection "+proj=somerc ' \
                    '+lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel ' \
                    '+towgs84=674.4,15.1,405.3,0,0,0,0 +units=m +no_defs" --incremental'

        process = os.popen(command21)
        process.close()

    # Close files
    pc_b_file.close()

    print "Start detecting 2nd difference"
    # Detect 2nd change order between point clouds and return the needed arrays
    diff_AB = pc_parser.detect_changes(voxel_grid, 0, 1, cd_thresh)

    if len(diff_AB[0]) > 0:
        # Prepare the file paths
        save_path = "{0}Point_Clouds\\temp\\t1t2_{1}.las".format(prm["t1"][3][0], diff_uid)
        print "2", save_path
        # Store the differences from the old point cloud to the new one
        pc_parser.store_diffs(diff_AB, pc_a_file, save_path)

        # Publish the new calculated differences   sys_par[1]
        command12 = prm["t1"][3][0] + 'Tools\\PotreeConverter_1.5RC_windows_64bit\\PotreeConverter.exe ' \
                    + save_path + ' -o ' + prm["t1"][3][1] + \
                    'pointclouds\\AHN2-AHN3 --output-format LAZ --projection "+proj=somerc ' \
                    '+lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel ' \
                    '+towgs84=674.4,15.1,405.3,0,0,0,0 +units=m +no_defs" --incremental'

        process = os.popen(command12)
        process.close()

    # Close files
    pc_a_file.close()


def init_pc_preparation(coords, diff_uid, sys_par):
    startTime = time.time()

    # Set the paths and names for the 2 point clouds that will be compared
    temp_files_path = sys_par[0] + "Point_Clouds\\temp\\"

    prmt = {"t1": ["t1_pc_list.txt", 't1_clip.las', "pointclouds\AHN2/", sys_par],
            "t2": ["t2_pc_list.txt", 't2_clip.las', "pointclouds\AHN3/", sys_par]}

    # Initiate the 2 parallel clipping processes
    p = Pool(2)
    p.map(clipper, [('t1', temp_files_path, prmt, coords), ('t2', temp_files_path, prmt, coords)])

    # Execute the change detection
    change_detection(temp_files_path, prmt, diff_uid)

    folder = temp_files_path
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    endTime = time.time()
    print "Finished in:", endTime - startTime
