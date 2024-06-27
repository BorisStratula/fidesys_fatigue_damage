class Solver:
    def init(fidesys, fidesys_config):
        for setup_command in fidesys_config.setup:
            fidesys.silent_cmd(setup_command)

    def advance(fidesys, pathes):
        debug_solution_file_path = pathes.debug_solution_file
        #Solver.save_project(fidesys)
        Solver.solve(fidesys, debug_solution_file_path)
    
    def solve(fidesys, debug_solution_file_path):
        fidesys.silent_cmd('calculation start path "{}"'.format(debug_solution_file_path))

    def save_project(fidesys):
        fidesys.silent_cmd('save "C:/Archive/Work/ICAD/2024/modeling/fidesys_slm/fidesys_test.fds" overwrite')
        return
