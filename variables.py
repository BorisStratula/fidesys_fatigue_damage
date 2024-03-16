class Variables:
    # state describing variables
    total_dead_nodes   = 0
    total_dead_nodes_n = 0
    total_dead_nodes_t = 0
    max_stress_n_node = 0
    max_stress_t_node = 0
    max_stress_node = 0
    max_psi_n_node = 0
    max_psi_t_node = 0
    max_psi_node = 0
    dN = 0
    N = 0

    # miscelaneous variables
    may_die_very_high = 0
    may_die_low_high = 0
    may_die_static = 0
    nodes_to_kill_n = 0
    nodes_to_kill_t = 0
    min_stress_n = 1e15
    min_stress_t = 1e15
    max_stress_n = 0
    max_stress_t = 0
    max2_psi_n = 0
    max2_psi_t = 0
    max_psi_n = 0
    max_psi_t = 0
    may_die_n = 0
    may_die_t = 0
    min_dN = 1e15
    max_psi = 0

    def advance():
        Variables.reset()
    
    def reset():
        Variables.may_die_very_high = 0
        Variables.may_die_low_high = 0
        Variables.may_die_static = 0
        Variables.nodes_to_kill_n = 0
        Variables.nodes_to_kill_t = 0
        Variables.min_stress_n = 1e15
        Variables.min_stress_t = 1e15
        Variables.max_stress_n = 0
        Variables.max_stress_t = 0
        Variables.max2_psi_n = 0
        Variables.max2_psi_t = 0
        Variables.max_psi_n = 0
        Variables.max_psi_t = 0
        Variables.may_die_n = 0
        Variables.may_die_t = 0
        Variables.min_dN = 1e15
        Variables.max_psi = 0