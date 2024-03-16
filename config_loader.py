import json

class Config_Loader:
    config = 0

    def fetch():
        path = 'config/setup.json'
        problem_name = Config_Loader.open_json_file(path)
        problem_name = problem_name['problem']
        problem_name_path = 'config/{}.json'.format(problem_name)
        Config_Loader.config = Config_Loader.open_json_file(problem_name_path)

    def open_json_file(path: str):
        text_file = open(path)
        json_file = json.load(text_file)
        text_file.close()
        return json_file
    
    def extract_constants(constants):
        all_materials = Config_Loader.open_json_file('config/materials.json')
        material_name = Config_Loader.config['material']
        for material in all_materials:
            if material['name'] == material_name:
                break
        constants.total_steps = Config_Loader.config['total_steps']
        constants.E = material['E']
        constants.nu = material['nu']
        constants.beta_VH = material['beta_VH']
        constants.beta_LH = material['beta_LH']
        constants.sigma_B = material['sigma_B']
        constants.sigma_U = material['sigma_U']
        constants.sigma_UT = material['sigma_UT']
        constants.sigma_gap = (constants.sigma_B - constants.sigma_U)*pow(10, -5*constants.beta_LH)

    def extract_fidesys_config(fidesys_config):
        all_commands = Config_Loader.config
        fidesys_config.setup = all_commands['setup']
        fidesys_config.dimensions = all_commands['dimensions']
        fidesys_config.element = all_commands['element']
        fidesys_config.body_type = all_commands['body_type']
        fidesys_config.mesh = all_commands['mesh']
        fidesys_config.action = all_commands['action']
        fidesys_config.geometry = all_commands['geometry']
        fidesys_config.boundary_conditions = all_commands['boundary_conditions']
        fidesys_config.target_ID = all_commands['target_ID']