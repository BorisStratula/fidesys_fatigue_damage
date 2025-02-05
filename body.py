class Body:
    total_nodes = 0
    total_elems = 0
    elem_is_modified = []
    elem_is_dead = []
    elem_psi = []
    elem_verteces = []
    elem_ID = []
    elem_E = []
    elem_initial_E = []
    elem_initial_nu = []
    nodal_coords = []
    block_ID = []
    material_ID = []
    meshio_cells = []

    def init(fidesys, cubit, constants, fidesys_config):
        Body.add_geometry(fidesys, cubit, fidesys_config)
        Body.add_mesh(fidesys, fidesys_config)
        Body.init_variables(cubit, fidesys_config)
        Body.create_first_block(fidesys, constants, fidesys_config)
        Body.add_boundary_conditions(fidesys, fidesys_config)
        Body.extract_and_sort_geometry_data(cubit, fidesys_config)
    
    def advance(constants, fidesys, fidesys_config, model_data, variables):
        Body.apply_damage_to_elements(constants, model_data, variables)
        Body.modify_elem_material(constants, fidesys, fidesys_config)
    
    def add_geometry(fidesys, cubit, fidesys_config):
        if fidesys_config.action == 'create':
            fidesys.silent_cmd(fidesys_config.geometry)
        if fidesys_config.action == 'open':
            fidesys.silent_cmd(fidesys_config.geometry)
        if fidesys_config.action == 'import':
            cubit.silent_cmd(fidesys_config.geometry)

    def add_mesh(fidesys, fidesys_config):
        for mesh_command in fidesys_config.mesh:
            fidesys.silent_cmd(mesh_command)

    def init_variables(cubit, fidesys_config):
        Body.total_nodes = cubit.get_node_count()
        Body.total_elems = Body.get_elem_count(cubit, fidesys_config)
        for elem in range(0, Body.total_elems):
            Body.elem_is_modified.append(0)
            Body.elem_is_dead.append(0)
            Body.elem_psi.append(0)
            Body.elem_ID.append(0)
            Body.block_ID.append(0)
            Body.material_ID.append(0)
            Body.elem_E.append(0)
            Body.elem_initial_E.append(0)
            Body.elem_initial_nu.append(0)

    def create_first_block(fidesys, constants, fidesys_config):
        target_ID = fidesys_config.target_ID
        first_vacant_elem_ID = Body.total_elems + 1
        Body.create_material(fidesys, first_vacant_elem_ID, constants.E, constants.nu)
        Body.create_block(fidesys, fidesys_config, first_vacant_elem_ID, fidesys_config.body_type, target_ID, first_vacant_elem_ID)
        for elem in range(0, Body.total_elems):
            Body.elem_ID[elem] = elem + 1
            Body.block_ID[elem] = first_vacant_elem_ID
            Body.elem_E[elem] = constants.E
            Body.elem_initial_E[elem] = constants.E
            Body.elem_initial_nu[elem] = constants.nu
        Body.material_ID = Body.block_ID
        # experiment with inclusion
        rows = []

        # even spaced rectangular pattern
        # rows.append([ 12,  41,  55,  98, 188, 114,  92, 246, 192])
        # rows.append([534, 590, 562, 620, 625, 653, 717, 716, 209])
        # rows.append([641, 991, 1061, 961, 1007, 1038, 1043, 652, 310])
        # rows.append([577, 1078, 1234, 1279, 1284, 1293, 1131, 639, 303])
        # rows.append([491, 1176, 1377, 1412, 1405, 1403, 1197, 763, 156])

        # vertical specimen
        # rows.append([ 12,  41,  55,  98, 188, 114,  92, 246, 192])
        # rows.append([158, 275, 319, 383, 463, 515, 526, 529, 563])
        # rows.append([305, 635, 638, 648, 702, 747, 766, 806, 860])
        # rows.append([641, 991, 1061, 961, 1007, 1038, 1043, 906, 218])
        # rows.append([1220, 645, 901, 1083, 1169, 1174, 1192, 1205, 555])
        # rows.append([295, 670, 895, 1084, 1237, 1296, 1319, 1349, 1353])
        # rows.append([359, 725, 925, 1118, 1236, 1377, 1403, 1405, 1412])
        # rows.append([479, 729, 777, 1021, 1217, 1307, 1314, 1318, 1321])
        # rows.append([509, 734, 776, 898, 993, 998, 1009, 1018, 1030])
        # rows.append([51, 77, 135,175,187,236,345,349,384,432,489,505,513,521,545,581,770,713,1419,1438,1443,1473,1526,1539,1545,1547,1551])

        # verital on surface
        # rows.append([92,192,246,275,353,363,384,432,469,529,563,641,645,648])
        # rows.append([670,672,725,729,734,747,769,860,939,991,1061,1093,1143])
        # rows.append([1179,1181,1202,1205,1323,1375])
        # rows.append([61])

        # horizontal specimen
        # rows.append([10,11,53,55,92,94,115,124,188,192,194,205,229,234,343,384,487])
        # rows.append([498,510,511,521,523,539,554,569,581,638,645,648,662,667,687,713,725,734,747])
        # rows.append([749,750,766,793,801,815,816,818,915,1008,1012,1024,1025,1035])
        # rows.append([1049,1069,1070,1080,1097,1133,1146,1150,1158,1164,1174,1192,1197,1205,1211])
        # rows.append([1232,1336,1377,1401,1404,1405,1409])

        # diagonal specimen
        rows.append([230,244,254,574,585,593,646,673,783,813,846,852,861,877,952,981])
        rows.append([1068,1079,1118,1167,1244,1256,1257,1267,1310,1366,1385])
        
        defect_elems = []
        for row in rows:
            defect_elems += row
        for elem in defect_elems:
            E = constants.E * 0.1
            nu = constants.nu
            Body.elem_initial_E[elem] = E
            Body.elem_initial_nu[elem] = nu
            Body.elem_is_modified[elem] = 1
            Body.move_elem_into_new_block(elem + 1, fidesys, fidesys_config, E, nu)
            Body.modify_material(fidesys, elem + 1, E, nu)

    def add_boundary_conditions(fidesys, fidesys_config):
        boundary_conditions = fidesys_config.boundary_conditions
        for command in boundary_conditions:
            fidesys.silent_cmd(command)

    def extract_and_sort_geometry_data(cubit, fidesys_config):
        Body.nodal_coords = Body.extract_nodal_coords(cubit)
        Body.elem_verteces = Body.extract_element_verteces(cubit, fidesys_config)
        Body.meshio_cells = Body.verteces_list_to_meshio_cells(fidesys_config)

    def apply_damage_to_elements(constants, model_data, variables):
        nodes_to_make_psi_negative = []
        for elem in range(0, Body.total_elems):
            if Body.elem_is_dead[elem] == 1:
                continue
            nodes = Body.elem_verteces[elem]
            nodes = map(lambda i : i + 1, nodes)
            max_psi = 0
            for node in nodes:
                i = node - 1
                if model_data.psi[i] > max_psi:
                    max_psi = model_data.psi[i]
                if model_data.psi[i] > constants.max_acceptable_psi:
                    nodes_to_make_psi_negative.append(i)
            Body.elem_psi[elem] = max_psi
        for node in nodes_to_make_psi_negative:
            if model_data.psi[node] > 0:
                Body.increment_dead_nodes_counter(model_data, node, variables)
                Body.make_node_damage_negative(model_data, node)

    def modify_elem_material(constants, fidesys, fidesys_config):
        #E = constants.E
        #nu = constants.nu
        for elem in range(0, Body.total_elems):
            E = Body.elem_initial_E[elem]
            nu = Body.elem_initial_nu[elem]
            if Body.elem_is_dead[elem] == 1:
                continue
            if constants.psi_start >= Body.elem_psi[elem]:
                continue
            if Body.elem_is_modified[elem] == 0:
                Body.move_elem_into_new_block(elem + 1, fidesys, fidesys_config, E, nu)
                Body.elem_is_modified[elem] = 1
            modified_E = Body.E_of_psi(Body.elem_psi[elem], constants, E)
            Body.modify_material(fidesys, elem + 1, modified_E, nu)
            if Body.elem_psi[elem] > constants.max_acceptable_psi:
                Body.elem_is_dead[elem] = 1
            

    
    def get_elem_count(cubit, fidesys_config):
        elem_type = fidesys_config.element
        if elem_type == 'tet':
            return cubit.get_tet_count()
        if elem_type == 'tri':
            return cubit.get_tri_count()
        if elem_type == 'map':
            return cubit.get_quad_count()
        print('unknown element type in get_elem_count')
        exit()
        
    def create_material(fidesys, material_ID, E, nu):
        fidesys.silent_cmd('create material {}'.format(material_ID))
        fidesys.silent_cmd('modify material {} set property \'MODULUS\' value {}'.format(material_ID, E))
        fidesys.silent_cmd('modify material {} set property \'POISSON\' value {}'.format(material_ID, nu))

    def create_block(fidesys, fidesys_config, block_ID, target_type, target_ID, material_ID):
        if fidesys_config.dimensions == '3D':
            target_category = 'solid'
        if fidesys_config.dimensions == '2D':
            target_category = 'plane'
        fidesys.silent_cmd('block {} add {} {}'.format(block_ID, target_type, target_ID))
        fidesys.silent_cmd('block {} material {} cs 1 element {} order 1'.format(block_ID, material_ID, target_category))

    def extract_nodal_coords(cubit):
        nodal_coords = []
        for node in range(0, Body.total_nodes):
            vector3 = cubit.get_nodal_coordinates(node + 1)
            nodal_coords.append(list(vector3))
        return nodal_coords
    
    def extract_element_verteces(cubit, fidesys_config):
        elem_verteces = []
        element = fidesys_config.element
        for elem in range(0, Body.total_elems):
            vector_n = cubit.get_expanded_connectivity(element, elem + 1)
            vector_n = map(lambda i : i - 1, vector_n)
            elem_verteces.append(list(vector_n))
        return elem_verteces
    
    def verteces_list_to_meshio_cells(fidesys_config):
        meshio_element = 0
        element = fidesys_config.element
        if element == 'tet':
            meshio_element = 'tetra'
        if element == 'tri':
            meshio_element = 'triangle'
        if element == 'map':
            meshio_element = 'quad'
        if meshio_element == 0:
            print('element type is not specified for meshio')
            exit()
        meshio_cells = [(meshio_element, Body.elem_verteces)]
        return meshio_cells
    
    def increment_dead_nodes_counter(model_data, node, variables):
        if model_data.psi_n[node] > model_data.psi_t[node]:
            variables.total_dead_nodes_n += 1
        else:
            variables.total_dead_nodes_t += 1
        variables.total_dead_nodes += 1

    def make_node_damage_negative(model_data, node):
        model_data.psi_n[node] = -1
        model_data.psi_t[node] = -1
        model_data.psi[node]   = -1

    def move_elem_into_new_block(element, fidesys, fidesys_config, E, nu):
        original_block_ID = Body.total_elems + 1
        element_type = fidesys_config.element
        fidesys.silent_cmd('block {} remove {} {}'.format(original_block_ID, element_type, element))
        Body.create_material(fidesys, element, E, nu)
        Body.create_block(fidesys, fidesys_config, element, element_type, element, element)
        Body.block_ID[element - 1] = element
        Body.material_ID[element - 1] = element

    def E_of_psi(psi, constants, initial_E):
        if psi < constants.max_acceptable_psi:
            return initial_E * (1 - constants.psi_stretch * psi)**constants.psi_power
        else:
            return constants.E_dead
        
    def modify_material(fidesys, material_ID, E, nu):
        fidesys.silent_cmd('modify material {} set property \'MODULUS\' value {}'.format(material_ID, E))
        fidesys.silent_cmd('modify material {} set property \'POISSON\' value {}'.format(material_ID, nu))
        Body.elem_E[material_ID - 1] = E

        