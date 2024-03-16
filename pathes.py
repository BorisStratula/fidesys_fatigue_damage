import os

class Pathes:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    solution_dir = os.path.join(project_dir, 'solution')
    debug_solution_file = os.path.join(project_dir, 'debug.pvd')
    debug_results_file = os.path.join(project_dir, 'debug', 'case1_step0001_substep0001.vtu')
