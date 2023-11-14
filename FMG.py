import time
import numpy as np

# 定义节点类 用于记录节点值和边等关系
class Point(object):#括号中是派生的其它基类，若有多个用逗号隔开
    def __init__(self, value, j, cal_fake_value=True,):#这是构造方法，当创建类的（实例）对象时，会自动调用，从而实现对类进行初始化操作
        #self类似Java里面的this，代表对象自己。
        self.value = value
        self.j = j
        if cal_fake_value == False:
            self.split_tuple_indexs_by_fake_value()
        else:
            self.split_tuple_indexs()  # 根节点计算fakevalue
        self.son_point = {}


    def cal_label(self):
        self.all_0 = False
        if self.value[-1] != 0:
            self.label1 = True
        else:
            self.label1 = False
        if min(self.value[self.indexs[-1]:self.j + 1]) == 0:
            self.cal_01 = True
        else:
            self.cal_01 = False


    def split_tuple_indexs_by_fake_value(self):
        self.fake_value = self.value

        if len(self.value)>2:
            self.indexs = []
            self.indexs_values = []
            for i in range(self.j, 0, -1):
                val = self.fake_value[i]
                if self.fake_value[i] != 0:
                    self.indexs_values.insert(0, val)
                    self.indexs.insert(0, i)


    def split_tuple_indexs(self):

        if len(self.value)>2:
            self.fake_value = self.value
            self.indexs = []
            self.indexs_values = []
            tmp_max = self.fake_value[-1]
            for i in range(self.j, 0, -1):
                val = self.fake_value[i]
                if val <= tmp_max and i != self.j:
                    self.fake_value[i] = 0
                elif val != 0:
                    val_before = self.fake_value[i-1]
                    if len(self.indexs_values)>0:
                        # 当前已有真实最大值
                        self.indexs_values.insert(0, val)
                        self.indexs.insert(0, i)
                    elif val_before <= val:
                        self.indexs_values.insert(0, val)
                        self.indexs.insert(0, i)
                    elif i == 1:
                        self.indexs_values.insert(0, val)
                        self.indexs.insert(0, i)
                    tmp_max = val

            # print('点的最大值索引切分值：', self.indexs_values)
            # print('点的最大值索引切分索引：', self.indexs)
            # print('========寻找最大索引，生成fake值：', self.fake_value, self.value)
        else:
            self.fake_value = [i-1 for i in self.value]
            # print('元祖仅有两个值', self.fake_value)


    def cal_ori_value(self, roots):
        max_root_value = self.fake_value.copy()
        for i in range(len(max_root_value)):
            if max_root_value[i] != 0:
                max_root_value[i] = max_root_value[i]-1

        tmp_p = Point(max_root_value, self.j)
        if self.all_0 == False:
            self.son_point[tuple(max_root_value)] = [roots]
        else:
            self.son_point[tuple(tmp_p.fake_value)] = [i for i in range(roots, self.j + 1)]
        self.last_brother = tmp_p.value


    def cal_01_func(self):
        tmp_label = True
        if max(self.value[self.indexs[-1]:self.j + 1]) == 0:
            self.all_0 = True

        for ix in range(self.j, self.indexs[-1], -1):
            if tmp_label == True:
                if self.label1 == False:
                    self.cal_ori_value([i for i in range(ix, self.j+1)])
                    tmp_label = False
            else:
                self.cal_value_by_brother(ix)
                break
        # print('计算最后一个最大值到最大边的子节点值', self.son_point)


    def cal_value_by_brother(self, ix):
        if type(ix) == int:
            if self.all_0 == True and ix == self.indexs[-1]:
                pass
            else:
                for i in range(ix, self.indexs[-1], -1):
                    self.last_brother[i+1] = self.last_brother[i+1] + 1
                    tmp_p = Point(self.last_brother,  self.j)
                    self.son_point[tuple(tmp_p.fake_value)] = [i] # fake
                    # self.son_point[tuple(self.last_brother)] = [i]
        else:
            # 计算除末尾外的最大值
            tmp_roots = ix[-1]
            for i in range(ix[-1], ix[0]-1, -1):
                if i in ix:
                    if i != ix[-1]:
                        if tmp_roots == ix[-1]:
                            tmp_roots += 1
                        self.last_brother[tmp_roots-1] = self.last_brother[tmp_roots-1] + 1
                        tmp_p = Point(self.last_brother,  self.j)
                        self.son_point[tuple(tmp_p.fake_value)] = [i for i in range(i, tmp_roots-1)]
                        tmp_roots = i+1
                    elif i == ix[-1] and self.all_0 != True:
                        if self.indexs[-1] != self.j:
                            tmp_roots = ix[-1] + 1
                            self.last_brother[tmp_roots] = self.last_brother[tmp_roots] + 1
                            tmp_p = Point(self.last_brother,  self.j)
                            self.son_point[tuple(tmp_p.fake_value)] = [i for i in range(i, tmp_roots)]
                        else:
                            tmp_roots = ix[-1]



    def cal_head_roots(self):
        if self.value[0] != self.indexs_values[0]:
            self.last_brother[self.indexs[0]] = self.last_brother[self.indexs[0]] + 1
            tmp_p = Point(self.last_brother,  self.j)
            self.son_point[tuple(tmp_p.fake_value)] = [i for i in range(self.indexs[0])]


    def cal_ONE_head(self):
        if self.value[0] != 1:
            self.last_brother = self.fake_value
            self.last_brother[0] = self.last_brother[0] - 1
            tmp_p = Point(self.last_brother,  self.j)
            self.son_point[tuple(tmp_p.fake_value)] = [i for i in range(self.indexs[0])]

    def cal_len2(self):
        if self.value[-1] == 1:
            self.son_point['ONE'] = 1
            if self.value[0] != 1:
                self.fake_value[1] += 1
                self.son_point[tuple(self.fake_value)] = 0
        else:
            self.son_point[tuple(self.fake_value)] = 1
            if self.value[0]!=self.value[1]:
                self.fake_value[1] += 1
                self.son_point[tuple(self.fake_value)] = 0


    def get_all_root_value(self):
        if len(self.value) == 2:
            self.cal_len2()
        else:
            self.cal_label()
            if max(self.indexs_values) != 1:
                if self.label1 == True:
                    self.cal_ori_value(self.j) # 计算最大值边对应的子节点 第j条边

                if self.cal_01:
                    # print('当前末尾含0')
                    self.cal_01_func()
                else:
                    # print('当前末尾不含0')
                    self.cal_value_by_brother(self.j-1)

                if self.all_0 == True:
                    # print('采用常规方式计算最后一位次大值节点值')
                    self.cal_ori_value(self.indexs[-1])

                self.cal_value_by_brother(self.indexs)
                self.cal_head_roots()
            else:
                self.son_point['ONE'] = [i for i in range(self.indexs[0], self.j + 1)]
                self.cal_ONE_head()
            # print('======本次节点值 计算完成')

def cal_gap(point):
    node_dict = {}  # 存储全局图结构
    tmp_dict = []  # 存储当前待计算节点值
    del_tmp_dict = [] # 存储已经计算过的子节点
    j = len(point)-1
    root = Point(point, j)
    root.get_all_root_value()
    node_dict.update({tuple(root.value): root.son_point})
    tmp_dict = [key for key in root.son_point.keys() if key != 'ONE']

    while len(tmp_dict) > 0:
        # print('开始递归计算子节点值', tmp_dict[-1])
        tmpv1 = tmp_dict[-1]
        root = Point(list(tmpv1), j, cal_fake_value=False)
        root.get_all_root_value()
        del_tmp_dict.append(tmpv1)
        node_dict.update({tuple(root.value): root.son_point})
        tmp_dict_ = [key for key in root.son_point.keys() if
                     key != 'ONE' and key not in tmp_dict and key not in del_tmp_dict]
        tmp_dict.pop()  # 移除当前已计算过的节点
        tmp_dict = tmp_dict_ + tmp_dict
        # print('=======================查看当前图结构', gap)

    # print('------------查看当前总图结构', node_dict, '字典大小', len(node_dict))
    count.append(len(node_dict))



if __name__ == '__main__':


    input = [5,4,3,2,1]
    m = 10
    count = []
    start = time.perf_counter()
    for i in range(2, len(input)+1):
        gap = input[:i]
        # print('---------------------开始计算第', i-1, '个图:', gap)
        cal_gap(gap)
    end = time.perf_counter()
    print('construct_time = ','%.4f'%((end-start)*1000),'ms')
    print(count)

