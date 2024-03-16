class Constants:
    #calculation options
    total_steps = 0

    #material constants
    E = 0
    nu = 0
    beta_VH = 0
    beta_LH = 0
    sigma_B = 0
    sigma_U = 0
    sigma_UT = 0
    sigma_gap = 0

    #model constants
    psi_start = 0
    max_acceptable_psi = 0.99
    psi_stretch = 0.10
    psi_twist   = 0.95
    E_dead = 1e-6
    gamma = 0.1
    R = 0
    psi_power = 1
    step_threshold = 0.95
    step_multiplier = 0.5
    max_psi_to_apply = 0.9
    N_min = 1e+4
    
    #model settings
    only_one_damage_mode = 0
    disable_lower_psi_after = 0.1