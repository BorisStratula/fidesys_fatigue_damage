class Solver:
    def init(fidesys, fidesys_config):
        for setup_command in fidesys_config.setup:
            fidesys.silent_cmd(setup_command)

    def advance(fidesys, pathes):
        debug_solution_file_path = pathes.debug_solution_file
        Solver.solve(fidesys, debug_solution_file_path)
    
    def solve(fidesys, debug_solution_file_path):
        fidesys.silent_cmd('calculation start path "{}"'.format(debug_solution_file_path))
