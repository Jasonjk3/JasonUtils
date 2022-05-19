# -*- ecoding: utf-8 -*-
# @ModuleName: mapreduce.py
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2022/5/20
# @Desc:

# -*- ecoding: utf-8 -*-
# @ModuleName: test.py
# @Author: jason
# @Email: jasonforjob@qq.com
# @Time: 2022/5/19
# @Desc:
import time
from multiprocessing import Process,Manager
from abc import abstractmethod, ABCMeta


class MapReduce(metaclass=ABCMeta):
    """
    MapReduce接口类,必须实现map,reduce,run方法
    """
    @abstractmethod
    def map(self,**kwargs):
        """定义接口名，但不需要实现其功能，由继承此类的子类实现"""
        raise NotImplementedError('必须实现map,reduce,run方法')


    @abstractmethod
    def reduce(self,**kwargs):
        """定义接口名，但不需要实现其功能，由继承此类的子类实现"""
        raise NotImplementedError('必须实现map,reduce,run方法')

    @abstractmethod
    def run(self,**kwargs):
        """定义接口名，但不需要实现其功能，由继承此类的子类实现"""
        raise NotImplementedError('必须实现map,reduce,run方法')



# class MyMapReduce(MapReduce):
#
#     def map(self,lis,res_dict,index):  #Map函数进行分词并存储到列表
#         print('map',index)
#         for i in lis:
#             time.sleep(1)
#             res_dict[i]='2'
#
#     def reduce(self,res_dict):  #Reduce函数将结果汇总到字典中
#         print(res_dict)
#         return res_dict
#
#     def run(self,data):
#         start_time = time.time()
#         plist = []
#         res_dict = Manager().dict({})
#         for i in range(len(data)):  # 创建进程
#             p = Process(target=self.map, args=(data[i], res_dict,i))
#             plist.append(p)
#         for p in plist:
#             p.start()  # 启动进程
#         for p in plist:
#             p.join()  # 阻滞主进程
#         res = self.reduce(res_dict)  # 当Map进程全部完成之后Reduce进行结果归约
#         print('time2 = %f' % (time.time() - start_time))  # 测试总用时
#         return res

# if __name__=='__main__':
#     data = [[1,4,6],[2,8,43]]
#
#     MyMapReduce().run(data)