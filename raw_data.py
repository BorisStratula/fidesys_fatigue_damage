import meshio

class Raw_Data:
    node_ID = []
    sigma_1 = []
    sigma_3 = []
    total_nodes = 0

    def init(body):
        Raw_Data.total_nodes = body.total_nodes
        for node in range(0, Raw_Data.total_nodes):
            Raw_Data.node_ID.append(node + 1)
            Raw_Data.sigma_1.append(0)
            Raw_Data.sigma_3.append(0)

    def advance(pathes):
        Raw_Data.reset()
        Raw_Data.fetch_nodal_data(pathes)
        pass

    def reset():
        for node in range(0, Raw_Data.total_nodes):
            Raw_Data.sigma_1[node] = -1e10
            Raw_Data.sigma_3[node] = -1e10

    def fetch_nodal_data(pathes):
        debug_results_file_path = pathes.debug_results_file
        meshio_data = meshio.read(debug_results_file_path)
        raw_node_ID = meshio_data.point_data['Node ID']
        raw_nodal_stress = meshio_data.point_data['Stress']
        nodal_data_mode = 'max'
        if nodal_data_mode == 'max':
            for i in range(0, len(raw_nodal_stress)):
                index = raw_node_ID[i] - 1
                if raw_nodal_stress[i][7] > Raw_Data.sigma_1[index]:
                    Raw_Data.sigma_1[index] = raw_nodal_stress[i][7]
                if raw_nodal_stress[i][9] > Raw_Data.sigma_3[index]:
                    Raw_Data.sigma_3[index] = raw_nodal_stress[i][9]