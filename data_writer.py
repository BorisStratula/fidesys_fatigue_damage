import os
import meshio

class Data_Writer:
    def init(solution_dir_path):
        Data_Writer.prepare_dir(solution_dir_path)

    def advance(global_step, body, raw_data, model_data, constants, pathes, variables):
        file_index = Data_Writer.add_prefix_zeroes_to_length(global_step, constants.total_steps)
        file_name = 'data_{}.vtu'.format(file_index)
        Data_Writer.write_text_log(pathes, global_step, variables)
        Data_Writer.write_solution_file(body, raw_data, model_data, pathes, file_name, variables)
        Data_Writer.combine_solution_files(pathes, global_step, constants)
    
    def prepare_dir(dir_path):
        try:
            os.mkdir(dir_path)
        except:
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                os.remove(file_path)

    def add_prefix_zeroes_to_length(value, max_value):
        result_str = ''
        for i in range(0,(len(str(max_value)) - len(str(value)))):
            result_str += '0'
        result_str += str(value)
        return result_str
    
    def write_text_log(pathes, global_step, variables):
        dir_path = pathes.solution_dir
        file = open(os.path.join(dir_path, 'solution_info.txt'), 'a')
        file.write('========== step info ==========\n')
        file.write('           step = {}'.format(global_step) + '\n')
        file.write('      max psi n = {}'.format(variables.max_psi_n) + '\n')
        file.write('     max2 psi n = {}'.format(variables.max2_psi_n) + '\n')
        file.write('      max psi t = {}'.format(variables.max_psi_t) + '\n')
        file.write('     max2 psi t = {}'.format(variables.max2_psi_t) + '\n')
        file.write('nodes to kill n = {}'.format(variables.nodes_to_kill_n) + '\n')
        file.write('nodes to kill t = {}'.format(variables.nodes_to_kill_t) + '\n')
        file.write('   dead nodes n = {}'.format(variables.total_dead_nodes_n) + '\n')
        file.write('   dead nodes t = {}'.format(variables.total_dead_nodes_t) + '\n')
        file.write(' kill something = {}'.format(0) + ' str(vars.kill_something)' + '\n')
        file.write('              N = {:E}'.format(variables.N) + '\n')
        file.write('             dN = {:E}'.format(variables.dN) + '\n')
        file.write('   max stress N = {:E}'.format(variables.max_stress_n) + '\n')
        file.write('   max stress T = {:E}'.format(variables.max_stress_t) + '\n')
        file.write('      may die N = {}'.format(variables.may_die_n) + '\n')
        file.write('      may die T = {}'.format(variables.may_die_t) + '\n')
        file.write('   dead node ID = {}'.format(0) + ' str(vars.dead_node_ID)' + '\n')
        file.write('   max psi node = {}'.format(variables.max_psi_node) + '\n')
        file.write('max stress node = {}'.format(variables.max_stress_node) + '\n')
        file.write('\n')
        file.close()

    def write_solution_file(body, raw_data, model_data, pathes, file_name, variables):
        dir_path = pathes.solution_dir
        point_data = {
            'Coordinates': body.nodal_coords,
            'node ID': raw_data.node_ID,
            'Principal Stress': Data_Writer.splice_lists(raw_data.sigma_1, raw_data.sigma_3),
            'Equivalent Stress': Data_Writer.splice_lists(model_data.sigma_LH_n, model_data.sigma_LH_t),
            'B': Data_Writer.splice_lists(model_data.B_n, model_data.B_t),
            'node psi': Data_Writer.splice_lists(model_data.psi_n, model_data.psi_t, model_data.psi),
        }
        cell_data = {
            'State': [Data_Writer.splice_lists(body.elem_is_modified, body.elem_is_dead)],
            'elem psi': [body.elem_psi],
            'ID': [Data_Writer.splice_lists(body.elem_ID, body.material_ID, body.block_ID)],
            'Young modulus': [body.elem_E],
        }
        results = meshio.Mesh(
            body.nodal_coords,
            body.meshio_cells,
            point_data,
            cell_data
        )
        file_path = os.path.join(dir_path, file_name)
        results.write(file_path)
        Data_Writer.append_result_file_with_cycles_number(file_path, variables)
        Data_Writer.append_result_file_with_suffixes(file_path)

    def splice_lists(*args):
        lists_provided = len(args)
        list_size = len(args[0])
        result = []
        for line in range(0, list_size):
            new_line = []
            for list in range(0, lists_provided):
                new_line.append(args[list][line])
            result.append(new_line)
        return result
    
    def combine_solution_files(pathes, global_step, constants):
        project_dir_path = pathes.project_dir
        solution_string  = r'<?xml version="1.0"?>' + '\n'
        #solution_string += r'<VTKFile type="Collection" version="0.1" byte_order="LittleEndian" compressor="vtkZLibDataCompressor">' + '\n'
        solution_string += r'<VTKFile type="Collection" byte_order="LittleEndian">' + '\n'
        solution_string += r'  <Collection>' + '\n'
        for step in range(0, global_step + 1):
            #data_string = return_zeroes_filled_string(i, vars.total_steps)
            data_string = Data_Writer.add_prefix_zeroes_to_length(step, constants.total_steps)
            solution_string += '    <DataSet step="{}" part="0" file="solution/data_{}.vtu" name="Asmb: Part: Matl:ELASTIC"/>\n'.format(step, data_string)
        solution_string += r'  </Collection>' + '\n'
        solution_string += r'</VTKFile>'
        solution_file = open(os.path.join(project_dir_path, 'solution.pvd'), 'w')
        solution_file.write(solution_string)
        solution_file.close()

    def append_result_file_with_cycles_number(file_path, variables):
        file = open(file_path, 'r')
        new_file_content = ''
        content_to_add = ''
        content_to_add += '\
        <FieldData>\n\
        <DataArray type="Float64" Name="Cycles" NumberOfTuples="1" format="ascii">\n\
        {}\n\
        </DataArray>\n\
        </FieldData>\n'.format(variables.N)
        paste_done = 0
        for line in file:
            new_file_content += line
            if paste_done == 0:
                if line.find('<UnstructuredGrid>') >= 0:
                    new_file_content += content_to_add
                    paste_done = 1
        file.close()
        file = open(file_path, 'w')
        file.write(new_file_content)
        file.close()

    def append_result_file_with_suffixes(file_path):
        Data_Writer.add_suffixes_into_results(file_path, 'Name="Principal Stress"', ['1', '3'])
        Data_Writer.add_suffixes_into_results(file_path, 'Name="Equivalent Stress"', ['SWT', 'CSV'])
        Data_Writer.add_suffixes_into_results(file_path, 'Name="B"', ['n', 't'])
        Data_Writer.add_suffixes_into_results(file_path, 'Name="node psi"', ['n', 't', 'max'])
        Data_Writer.add_suffixes_into_results(file_path, 'Name="State"', ['modified', 'dead'])
        Data_Writer.add_suffixes_into_results(file_path, 'Name="ID"', ['tet', 'material', 'block'])

    def add_suffixes_into_results(file_path, looking_for, suffixes_to_add):
        file = open(file_path, 'r')
        temp_string = ''
        text_to_add = ''
        for i in range(0, len(suffixes_to_add)):
            text_to_add += 'ComponentName' + str(i) + '="' + suffixes_to_add[i] + '" '
        for line in file:
            pos1 = line.find(looking_for)
            if pos1 >= 0:
                pos2 = line.find('format=')
                temp_line = line[0:pos2] + text_to_add + line[pos2:len(line)]
                temp_string += temp_line
            else:
                temp_string += line
        file.close()
        file = open(file_path, 'w')
        file.write(temp_string)
        file.close()