import os
import sys

class Fidesys:
    _workaround = 0
    _fidesys_component = 0
    def init():
        fidesys_path = r'C:\Program Files\Fidesys\CAE-Fidesys-6.1' # Расположение Фидесиса
        prep_paths = [os.path.join(fidesys_path, 'preprocessor', 'bin'),
                         os.path.join(fidesys_path, 'preprocessor', 'bin', 'plugins'),
                         os.path.join(fidesys_path, 'preprocessor', 'bin', 'acis', 'code', 'bin'),
                         os.path.join(fidesys_path, 'preprocessor', 'structure')] # Директории, где препроцессор
        for path in prep_paths:
            os.environ['PATH'] += os.pathsep + path # Добавление пути к препроцессору в PATH
            os.add_dll_directory(path)
            sys.path.append(path) # Добавление пути к препроцессору в PATH
        import fidesys # type: ignore # Библиотека Фидесиса
        Cubit.init()
        #global fc
        fc = fidesys.FidesysComponent() # Создание обязательного компонента Фидесис fc
        fc.init_application(prep_paths[0]) # !!!!!Инициализация для версий 5.1 (для 5.0 и ниже заменить на fc.initApplication(prep_paths[0]) )
        fc.start_up_no_args() # Запуск обязательного компонента Фидесис fc
        Fidesys._workaround = fidesys
        Fidesys._fidesys_component = fc

        #fidesys.cmd('brick x 1 y 10 z 1')
        #fidesys.cmd('create material {}'.format(1))
        #fidesys.cmd('modify material {} set property \'MODULUS\' value {}'.format(1, 1e10))
        #fidesys.cmd('modify material {} set property \'POISSON\' value {}'.format(1, 0.3))
        #fidesys.cmd('block {} add {} {}'.format(1, 'volume', 1))
        #fidesys.cmd('block {} material {} cs 1 element solid order 1'.format(1, 1))
        #fidesys.cmd('list block all')
        
    def cmd(string: str):
        Fidesys._workaround.cmd(string)

    def silent_cmd(string: str):
        Fidesys._workaround.silent_cmd(string)

class Cubit:
    _workaround = 0
    def init():
        fidesys_path = r'C:\Program Files\Fidesys\CAE-Fidesys-6.1' # Расположение Фидесиса
        prep_paths = [os.path.join(fidesys_path, 'preprocessor', 'bin'),
                         os.path.join(fidesys_path, 'preprocessor', 'bin', 'plugins'),
                         os.path.join(fidesys_path, 'preprocessor', 'bin', 'acis', 'code', 'bin'),
                         os.path.join(fidesys_path, 'preprocessor', 'structure')] # Директории, где препроцессор
        for path in prep_paths:
            os.environ['PATH'] += os.pathsep + path # Добавление пути к препроцессору в PATH
            os.add_dll_directory(path)
            sys.path.append(path) # Добавление пути к препроцессору в PATH
        import cubit # type: ignore # Библиотека препроцессинга
        cubit.init(['cubit', '-nojournal']) # Инициализация препроцессора
        Cubit._workaround = cubit

    def cmd(string: str):
        Cubit._workaround.cmd(string)

    def silent_cmd(string: str):
        Cubit._workaround.silent_cmd(string)
    
    def get_node_count() -> int:
        return Cubit._workaround.get_node_count()
    
    def get_tet_count() -> int:
        return Cubit._workaround.get_tet_count()
    
    def get_tri_count() -> int:
        return Cubit._workaround.get_tri_count()
    
    def get_quad_count() -> int:
        return Cubit._workaround.get_quad_count()
    
    def get_surface_element_count() -> int:
        return Cubit._workaround.get_surface_element_count()
    
    def get_nodal_coordinates(ID: int):
        return Cubit._workaround.get_nodal_coordinates(ID)

    def get_expanded_connectivity(element_type: str, ID: int):
        return Cubit._workaround.get_expanded_connectivity(element_type, ID)