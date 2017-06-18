# -*- coding: utf-8 -*-
import laspy
import copy


def combined_extent(pc1, pc2):
    """
    Get the origin point (minimum extent) of both point clouds combined
    This will be used during the generation of the Voxel Grid
    """

    # Create a dictionary extent
    extent = {"min_X": min(pc1.min[0], pc2.min[0]),
              "min_Y": min(pc1.min[1], pc2.min[1]),
              "min_Z": min(pc1.min[2], pc2.min[2])}
    return extent


def prepare_grid(grid, point_clouds):
    """Build point indices and fill the voxel Grid with them"""
    for pc_id, pc in enumerate(point_clouds):

        # For every point in the given point cloud
        for pt_index in range(len(pc[0])):
            # Add points to the Grid
            grid.add_point(pt_index, pc[0][pt_index], pc[1][pt_index], pc[2][pt_index], pc_id)


# Initiate the change detection procedure.
def detect_changes(grid, pc1, pc2, cd_thresh):
    """This function returns 2 lists: One with the indices of the changed points and one with the distances"""

    # The lists that will hold the changes
    changed_points = []
    distances = []
    red = []
    green = []
    blue = []

    # For every voxel-neighborhood inside the pc1 point cloud:
    for voxel_id, neighborhood in grid.voxels[pc1].iteritems():

        # For every point within the voxel-neighborhood (that is inside the pc1 point cloud):
        for pt1_idx, pt1 in neighborhood.iteritems():

            # Set a very high arbitrary number, that will always "lose" during a possible comparison
            min_dist = 1000000000

            # For every cross-point-cloud point that the generator will yield:
            for pt2 in grid.neighbor_finder(pc2, voxel_id):

                # Calculate the (squared) distance
                d = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 + (pt1[2] - pt2[2]) ** 2)

                # If the distance is even lower than the current minimum, do an update:
                if d < min_dist:
                    min_dist = d

                # If a point has been found to be closer than our threshold,
                # it means that there is no significant change that interests us
                if min_dist < cd_thresh:
                    break

            # If the threshold was not utilized, it means that the minimum distance is still "above" it.
            # That means that the point has been changed
            if min_dist > cd_thresh:
                changed_points.append(pt1_idx)

                # 25: The (square) distance threshold, 150: Tthe minimum base color
                # 6: The ratio between the selected min-max range distance and min-max color range (e.g. 6 times bigger)
                #gradient = int(150 - ((min_dist - 25) / 3.75))
                #if gradient < 0:
                    #gradient = 0

                if pc1:
                    red.append(0)
                    green.append(250)
                else:
                    red.append(250)
                    green.append(0)
                blue.append(0)

    return changed_points, red, green, blue


def store_diffs(diff, pc1_file, file_path):
    """This function stores the calculated differences in a las file"""
    changed_points, red, green, blue = diff

    hdr = copy.copy(pc1_file.header)

    hdr.pt_dat_format_id = 2

    output_file = laspy.file.File(file_path, mode="w", header=hdr)

    output_file.header.scale = pc1_file.header.scale
    output_file.points = pc1_file.points[changed_points]

    output_file.red = red
    output_file.green = green
    output_file.blue = blue

    output_file.close()