import math

class Model_Data:
    psi_n = []
    psi_t = []
    psi = []
    B_n = []
    B_t = []
    sigma_LH_n = []
    sigma_LH_t = []
    sigma_VH_n = []
    sigma_VH_t = []
    total_nodes = 0

    def init(body, constants):
        Model_Data.total_nodes = body.total_nodes
        for node in range(0, Model_Data.total_nodes):
            Model_Data.psi_n.append(constants.psi_start)
            Model_Data.psi_t.append(constants.psi_start)
            Model_Data.psi.append(constants.psi_start)
            Model_Data.B_n.append(0)
            Model_Data.B_t.append(0)
            Model_Data.sigma_LH_n.append(0)
            Model_Data.sigma_LH_t.append(0)
            Model_Data.sigma_VH_n.append(0)
            Model_Data.sigma_VH_t.append(0)

    def advance(constants, raw_data, variables):
        Model_Data.calculate_equivalent_stress(constants, raw_data)
        Model_Data.find_max_stress(variables)
        Model_Data.calculate_B_value(constants, variables)
        Model_Data.calculate_dN_value(constants, variables)
        Model_Data.calculate_N_value(variables)
        Model_Data.calculate_psi_value(constants, variables)
        Model_Data.find_max_psi(constants, variables)

    def calculate_equivalent_stress(constants, raw_data):
        Model_Data.normal_criterion(constants, raw_data)
        Model_Data.shear_criterion(constants, raw_data)

    def find_max_stress(variables):
        for node in range(0, Model_Data.total_nodes):
            if Model_Data.psi[node] >= 0:
                if Model_Data.sigma_LH_n[node] > variables.max_stress_n:
                    variables.max_stress_n = Model_Data.sigma_LH_n[node]
                    variables.max_stress_n_node = node
                if Model_Data.sigma_LH_t[node] > variables.max_stress_t:
                    variables.max_stress_t = Model_Data.sigma_LH_t[node]
                    variables.max_stress_t_node = node
        if variables.max_stress_t > variables.max_stress_n:
            variables.max_stress_node = variables.max_stress_t_node
        else:
            variables.max_stress_node = variables.max_stress_n_node

    def calculate_B_value(constants, variables):
        for node in range(0, Model_Data.total_nodes):
            psi_n = Model_Data.psi_n[node]
            psi_t = Model_Data.psi_t[node]
            sigma_VH_n = Model_Data.sigma_VH_n[node]
            sigma_LH_n = Model_Data.sigma_LH_n[node]
            sigma_VH_t = Model_Data.sigma_VH_t[node]
            sigma_LH_t = Model_Data.sigma_LH_t[node]
            Model_Data.B_n[node] = Model_Data.B_equation(psi_n, sigma_VH_n, sigma_LH_n, constants, variables, 'n')
            Model_Data.B_t[node] = Model_Data.B_equation(psi_t, sigma_VH_t, sigma_LH_t, constants, variables, 't')

    def calculate_dN_value(constants, variables):
        for node in range(0, Model_Data.total_nodes):
            B_n = Model_Data.B_n[node]
            B_t = Model_Data.B_t[node]
            psi_n = Model_Data.psi_n[node]
            psi_t = Model_Data.psi_t[node]
            dN_n = Model_Data.dN_equation(B_n, psi_n, constants, variables)
            dN_t = Model_Data.dN_equation(B_t, psi_t, constants, variables)
            if dN_n < dN_t:
                dN = dN_n
            else:
                dN = dN_t
            if dN < variables.min_dN:
                variables.min_dN = dN
        variables.dN = variables.min_dN
        if (variables.may_die_n + variables.may_die_t) == 0:
            variables.dN = 0

    def calculate_N_value(variables):
        variables.N += variables.dN

    def calculate_psi_value(constants, variables):
        for node in range(0, Model_Data.total_nodes):
            psi_n = Model_Data.psi_n[node]
            psi_t = Model_Data.psi_t[node]
            if (psi_n < 0) or (psi_t < 0):
                continue
            dN = variables.dN
            gamma = constants.gamma
            B_n = Model_Data.B_n[node]
            B_t = Model_Data.B_t[node]
            next_N_n = dN + Model_Data.dN_in_range_0_to_psi(B_n, gamma, psi_n)
            Model_Data.psi_n[node] = Model_Data.psi_equation(B_n, gamma, psi_n, next_N_n)
            next_N_t = dN + Model_Data.dN_in_range_0_to_psi(B_t, gamma, psi_t)
            Model_Data.psi_t[node] = Model_Data.psi_equation(B_t, gamma, psi_t, next_N_t)
            if Model_Data.psi_n[node] > Model_Data.psi_t[node]:
                Model_Data.psi[node] = Model_Data.psi_n[node]
            else:
                Model_Data.psi[node] = Model_Data.psi_t[node]

    def find_max_psi(constants, variables):
        for node in range(0, Model_Data.total_nodes):
            if constants.only_one_damage_mode == 1:
                Model_Data.leave_one_damage_mode(node, constants)
            psi_n = Model_Data.psi_n[node]
            psi_t = Model_Data.psi_t[node]
            if (psi_n > variables.max2_psi_n) and (psi_n <= variables.max_psi_n):
                variables.max2_psi_n = psi_n
            if psi_n > variables.max_psi_n:
                variables.max2_psi_n = variables.max_psi_n
                variables.max_psi_n = psi_n
                variables.max_psi_n_node = node
            if (psi_t > variables.max2_psi_t) and (psi_t <= variables.max_psi_t):
                variables.max2_psi_t = psi_t
            if psi_t > variables.max_psi_t:
                variables.max2_psi_t = variables.max_psi_t
                variables.max_psi_t = psi_t
                variables.max_psi_t_node = node
        if variables.max_psi_n > variables.max_psi_t:
            variables.max_psi_node = variables.max_psi_n_node
            variables.max_psi = variables.max_psi_n
        else:
            variables.max_psi_node = variables.max_psi_t_node
            variables.max_psi = variables.max_psi_t
    
    def normal_criterion(constants, raw_data):
        #SWT criterion
        sigma_1 = raw_data.sigma_1
        R = constants.R
        for node in range(0, Model_Data.total_nodes):
            if sigma_1[node] < 0:
                sigma_1[node] = 0
            dsigma_1 = sigma_1[node] * (1 - R)
            Model_Data.sigma_LH_n[node] = math.sqrt(sigma_1[node] * dsigma_1 / 2)
        Model_Data.sigma_VH_n = Model_Data.sigma_LH_n
    
    def shear_criterion(constants, raw_data):
        #CSV criterion
        sigma_1 = raw_data.sigma_1
        sigma_3 = raw_data.sigma_3
        R = constants.R
        for node in range(0, Model_Data.total_nodes):
            dsigma_1 = sigma_1[node] * (1 - R)
            dsigma_3 = sigma_3[node] * (1 - R)
            dsigma_n = (dsigma_1 + dsigma_3)/2
            dsigma_t = (dsigma_1 - dsigma_3)/2
            Model_Data.sigma_LH_t[node] = math.sqrt((dsigma_n / 2)**2 + 3*(dsigma_t / 2)**2)
        Model_Data.sigma_VH_t = Model_Data.sigma_LH_t

    def B_equation(psi, sigma_VH, sigma_LH, constants, variables, mode):
        gamma = constants.gamma
        N_min = constants.N_min
        beta_LH = constants.beta_LH
        beta_VH = constants.beta_VH
        sigma_B = constants.sigma_B
        sigma_U = constants.sigma_U
        sigma_UT = constants.sigma_UT
        sigma_gap = constants.sigma_gap
        may_die = 0
        if psi < 0:
            B = 0
        else:
            if sigma_VH < sigma_UT:
                B = 0
            elif sigma_VH < (sigma_U + sigma_gap):
                B = ((sigma_VH - sigma_UT)/(sigma_U + sigma_gap - sigma_UT))**(1/beta_VH) / 1e8 / 2 / (1 - gamma)
                may_die = 1
                variables.may_die_very_high += 1
            elif sigma_LH < sigma_B:
                B = ((sigma_LH - sigma_U)/(sigma_B - sigma_U))**(1/beta_LH) / N_min / 2 / (1 - gamma)
                may_die = 1
                variables.may_die_low_high += 1
            else:
                B = 1 / 2 / N_min / (1 - gamma)
                may_die = 1
                variables.may_die_static += 1
        if mode == 'n':
            variables.may_die_n += may_die
        if mode == 't':
            variables.may_die_t += may_die
        return B
    
    def dN_equation(B, psi, constants, variables):
        if B > 0:
            gamma = constants.gamma
            dN = Model_Data.dN_in_range_psi_to_1(B, gamma, psi)
            if dN > 1e15:
                dN = 1e15
            if psi <= constants.step_threshold:
                dN *= constants.step_multiplier
        else:
            dN = 1e15
        return dN
    
    def dN_in_range_psi_to_1(B, gamma, psi):
        return Model_Data.dN_in_range_0_to_1(B, gamma) - Model_Data.dN_in_range_0_to_psi(B, gamma, psi)

    def dN_in_range_0_to_1(B, gamma):
        return 1 / (2*B*(1 - gamma))

    def dN_in_range_0_to_psi(B, gamma, psi):
        if B > 0:
            return (2*psi**(1 - gamma) - psi**(2 - 2*gamma)) / (2*B*(1 - gamma))
        else:
            return 0

    def psi_equation(B, gamma, psi, next_N):
        psi_square = 1 + 2*B*next_N*(gamma - 1)
        if psi_square < 0:
            psi_square = 0
        psi_reciprocal_base = 1 - math.sqrt(psi_square)
        if psi_reciprocal_base > 0:
            psi_reciprocal = psi_reciprocal_base**(1/(gamma - 1))
        else:
            psi_reciprocal = 0
        if B < 0:
            return psi
        else:
            if psi_reciprocal <= 0:
                return psi
            else:
                return 1 / psi_reciprocal
            
    def leave_one_damage_mode(node, constants):
        if Model_Data.psi_t[node] > constants.disable_lower_psi_after and Model_Data.psi_t[node] > Model_Data.psi_n[node]:
            Model_Data.psi_n[node] = constants.psi_start
        if Model_Data.psi_n[node] > constants.disable_lower_psi_after and Model_Data.psi_n[node] > Model_Data.psi_t[node]:
            Model_Data.psi_t[node] = constants.psi_start
