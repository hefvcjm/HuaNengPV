from main.src.framework.Execute import *
from main.src.application.diagnosis.General import *

data = 0


class ExecuteListener(OnExecuteListener):

    def on_success(self, result):
        global data
        print(result)
        if result:
            data = 1
        else:
            data = 0

    def on_failure(self, error):
        super().on_failure(error)


if __name__ == '__main__':
    execute = Execute()
    # 设置监听器
    execute.set_execute_listener(ExecuteListener())
    # 设置执行需要执行的算法
    execute.set_algorithm(ValueIsZero())
    # 执行
    for i in range(20):
        execute.set_data(data)
        execute.execute()
