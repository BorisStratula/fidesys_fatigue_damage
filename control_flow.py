from body           import *
from config_loader  import *
from constants      import *
from data_writer    import *
from fidesys_config import *
from fidesys_init   import *
from model_data     import *
from pathes         import *
from raw_data       import *
from solver         import *
from timer          import *
from variables      import *

class Control_Flow:
    timer1 = 0
    timer2 = 0
    timer3 = 0

    def init():
        Control_Flow.timer1 = Timer()
        Control_Flow.timer2 = Timer()
        Control_Flow.timer3 = Timer()
        Control_Flow.timer1.start()
        Config_Loader.fetch()
        Config_Loader.extract_constants(Constants)
        Config_Loader.extract_fidesys_config(Fidesys_Config)
        Fidesys.init()
        Solver.init(Fidesys, Fidesys_Config)
        Body.init(Fidesys, Cubit, Constants, Fidesys_Config)
        print('nodes = {}, elements = {}'.format(Body.total_nodes, Body.total_elems))
        Raw_Data.init(Body)
        Model_Data.init(Body, Constants)
        Data_Writer.init(Pathes.solution_dir)
        print('init done')

    def calculate():
        for global_step in range(0, Constants.total_steps):
            print('========== global step {} =========='.format(global_step))
            Control_Flow.timer2.start()
            Solver.advance(Fidesys, Pathes)
            Control_Flow.timer2.stop()
            Control_Flow.timer3.start()
            Variables.advance()
            Raw_Data.advance(Pathes)
            Model_Data.advance(Constants, Raw_Data, Variables)
            Body.advance(Constants, Fidesys, Fidesys_Config, Model_Data, Variables)
            Data_Writer.advance(global_step, Body, Raw_Data, Model_Data, Constants, Pathes, Variables)
            Control_Flow.timer3.stop()
            Control_Flow.timer2.info('solver')
            Control_Flow.timer3.info('data processing')
        print('calculation done')

    def deinit():
        print('deinit done')
        Control_Flow.timer1.stop()
        Control_Flow.timer1.info('total')
        Control_Flow.timer2.info('solver')
        Control_Flow.timer3.info('data processing')
        r2 = Control_Flow.timer2.cumulative_time/Control_Flow.timer1.cumulative_time
        r3 = Control_Flow.timer3.cumulative_time/Control_Flow.timer1.cumulative_time
        print('computation time ratio: fidesys {:.3f}, python {:.3f}, misc {:.3f}'
          .format(r2, r3, 1 - r2 - r3))