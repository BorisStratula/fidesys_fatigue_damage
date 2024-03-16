from control_flow import *

def main() -> str:
    Control_Flow.init()
    Control_Flow.calculate()
    Control_Flow.deinit()
    return 'program exited sucessfully'

print(main())