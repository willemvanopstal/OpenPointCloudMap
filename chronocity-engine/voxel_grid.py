class VoxelGrid(object):

    def __init__(self, orig, size):
        """ Initiates the creation of the voxel grid object"""
        self.origin = orig
        self.size = size
        self.voxels = {0: {}, 1: {}}  # a dictionary to store the voxels and their points

    def add_point(self, point_index, pt_x, pt_y, pt_z, point_cloud):
        """Adds a point array to the correct voxel, by converting its x,y and z coordinates to the voxel_id"""

        # XYZ voxel distance from origin
        vox_x = int((pt_x - self.origin['min_X']) / self.size)
        vox_y = int((pt_y - self.origin['min_Y']) / self.size)
        vox_z = int((pt_z - self.origin['min_Z']) / self.size)

        voxel_id = "{0}_{1}_{2}".format(vox_x, vox_y, vox_z)

        # If the generated voxel id (in the specific point cloud) exists, there will be no exception:
        try:
            # Add the point into the point dictionary
            self.voxels[point_cloud][voxel_id][point_index]= (pt_x, pt_y, pt_z)

        # Else: voxel does not exists. Create it and add the point to it.
        except:
            # First addition of the point into the point dictionary
            self.voxels[point_cloud][voxel_id] = {point_index:(pt_x, pt_y, pt_z)}

    def neighbor_finder(self, point_cloud, voxel_id):
        """This function takes advantage of a cubic-expansion searching algorithm"""
        base_x, base_y, base_z = [int(i) for i in voxel_id.split("_")]

        stop = False

        # Store which voxels have been discovered in order to avoid reusing them
        voxels_found = {}

        # Start from the second iteration in order to prevent the voxel being returned alone
        current_iteration = 2
        double_depth = current_iteration * 2  #

        x_counter = 1
        y_counter = 1
        z_counter = 1

        # Dimension X
        while True:

            if x_counter % 2 == 0:
                x = x_counter / -2
            else:
                x = x_counter / 2

            # Dimension Y
            while True:

                if y_counter % 2 == 0:
                    y = y_counter / -2
                else:
                    y = y_counter / 2

                # Dimension Z
                while True:

                    if z_counter % 2 == 0:
                        z = z_counter / -2
                    else:
                        z = z_counter / 2

                    # Check if this voxel has been discovered before
                    if not (x, y, z) in voxels_found:
                        voxels_found[(x, y, z)] = None
                        vox_id = "{0}_{1}_{2}".format(base_x+x, base_y+y, base_z+z)

                        # Check if the neighborhood exists:
                        if vox_id in self.voxels[point_cloud]:

                            # A point has been found so the cubic searching can be stopped.
                            stop = True

                            # For every point in the parsed voxel:
                            for point in self.voxels[point_cloud][vox_id].values():
                                # Return the point
                                yield point

                    z_counter += 1

                    if z_counter == double_depth:
                        z_counter = 1
                        break

                y_counter += 1

                if y_counter == double_depth:
                    y_counter = 1
                    break

            x_counter += 1

            if x_counter == double_depth:
                x_counter = 1

                # First iteration circle ended.
                # Preparing the next one:
                double_depth = (current_iteration + 1) * 2
                current_iteration += 1

            # Expansion Stopper
            if stop:
                break