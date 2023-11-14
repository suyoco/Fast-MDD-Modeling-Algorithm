import time
import numpy as np

def BDDkiGen(ki, n):
    index = 0
    for y in range(ki):
        for x in range(n - ki + 1):
            if x == n - ki:
                E = "ZERO"
            else:
                E = index + 1
            if y == ki - 1:
                T = "ONE"
            else:
                T = index + n - ki + 1
            node = (x + y + 1, E, T)
            BDD_dict[index] = node
            index += 1
    return index


def MDDkiGen(i, M):
    index_ = 0
    for value in BDD_dict.values():
        MDD_node = ()
        MDD_node = MDD_node + (value[0],)
        for y in range(1, i + 1):
            MDD_node = MDD_node + (value[1],)
        for y in range(i + 1, M + 2):
            MDD_node = MDD_node + (value[2],)

        MDD_dict[index_] = MDD_node
        index_ += 1


def judge_equal(index1, index, node1, node2, new_node, combination_table):
    if index1 == index:
        new_node = new_node + (index,)
        combination_table[(node1, node2)] = index
        index += 1
    else:
        new_node = new_node + (index1,)


def ONE_and_node(node1, MDD_dict1, node2, MDD_dict2, index, MDDs):
    # print(node1,"AND",node2)
    if node1 == "ONE":
        node = node2
        MDD_dict = MDD_dict2
    else:
        node = node1
        MDD_dict = MDD_dict1
    new_node = (node[0],)
    for next_index in node[1:]:
        if next_index in ["ZERO", "ONE"]:
            new_node = new_node + (next_index,)
        else:
            if node1 == "ONE":
                if ("ONE", next_index) in combination_table:
                    new_node = new_node + (combination_table[("ONE", next_index)],)
                else:

                    index1, index = ONE_and_node("ONE", MDD_dict1, MDD_dict[next_index], MDD_dict, index, MDDs)
                    # judge_equal(index1,index,"ONE",next_index,new_node,combination_table)
                    if index1 == index:
                        new_node = new_node + (index,)
                        combination_table[("ONE", next_index)] = index
                        index += 1
                    else:
                        combination_table[("ONE", next_index)] = index1
                        new_node = new_node + (index1,)

            else:
                if (next_index, "ONE") in combination_table:

                    new_node = new_node + (combination_table[(next_index, "ONE")],)
                else:
                    index1, index = ONE_and_node(MDD_dict[next_index], MDD_dict, node2, MDD_dict2, index, MDDs)
                    # judge_equal(index1,index,next_index,"ONE",new_node,combination_table)

                    if index1 == index:
                        new_node = new_node + (index,)
                        combination_table[(next_index, "ONE")] = index
                        index += 1
                    else:
                        combination_table[(next_index, "ONE")] = index1

                        new_node = new_node + (index1,)
    if len(new_node) == M + 2:
        flag = 0
        index1 = 0
        for item_key, item_value in MDDs.items():
            if item_value == new_node:
                flag = 1
                index1 = item_key
                break
        if flag == 0:
            index1 = index
            MDDs[index] = new_node
            # print("MDDs=", MDDs)
        return index1, index


def node_and_node(node1, MDD1, node2, MDD2, index, MDDs):
    new_node = (node1[0],)

    ix = 1
    # print(node1, "AND", node2)
    for next_index1 in node1[1:]:
        if (next_index1, node2[ix]) in combination_table:
            new_node = new_node + (combination_table[(next_index1, node2[ix])],)
        else:
            if next_index1 == "ZERO" or node2[ix] == "ZERO":
                new_node = new_node + ("ZERO",)
            elif next_index1 == "ONE" and node2[ix] == "ONE":
                new_node = new_node + ("ONE",)
            elif next_index1 == "ONE":

                index1, index = ONE_and_node("ONE", MDD1, MDD2[node2[ix]], MDD2, index, MDDs)
                # judge_equal(index1, index, "ONE", node2[ix], new_node, combination_table)

                if index1 == index:
                    new_node = new_node + (index,)
                    combination_table[("ONE", node2[ix])] = index
                    index += 1
                else:
                    combination_table[("ONE", node2[ix])] = index1

                    new_node = new_node + (index1,)

            elif node2[ix] == "ONE":
                index1, index = ONE_and_node(MDD1[next_index1], MDD1, "ONE", MDD2, index, MDDs)
                # judge_equal(index1, index, next_index1, "ONE", new_node, combination_table)

                if index1 == index:
                    new_node = new_node + (index,)
                    combination_table[(next_index1, "ONE")] = index
                    index += 1
                else:
                    combination_table[(next_index1, "ONE")] = index1

                    new_node = new_node + (index1,)

            else:

                index1, index = node_and_node(MDD1[next_index1], MDD1, MDD2[node2[ix]], MDD2, index, MDDs)
                # judge_equal(index1, index, next_index1, node2[ix], new_node, combination_table)
                # print("index1,index==",index1,index)

                if index1 == index:
                    new_node = new_node + (index,)
                    combination_table[(next_index1, node2[ix])] = index
                    index += 1
                else:
                    combination_table[(next_index1, node2[ix])] = index1

                    new_node = new_node + (index1,)
        ix += 1

    if len(new_node) == M + 2:
        flag = 0
        index1 = index
        # print("new_node=", new_node)
        for item_key, item_value in MDDs.items():
            if item_value == new_node:
                flag = 1
                index1 = item_key
                break
        if flag == 0:
            MDDs[index] = new_node
            # print("MDDs=", MDDs)
            # print(index1,index)
        return index1, index


def find_root(MDD):
    root = ()
    for key,value in MDD.items():
        if value[0] == 1:
            root = value
            break
    return root,key

def compute_pr(root, index, MDDj, P, node_pr):
    Pr = 0.0
    for i in range(1, M + 2):
        if root[i] == "ZERO":
            Pr += 0
        elif root[i] == "ONE":
            Pr += P[root[0] - 1][i - 1]
        else:
            if root[i] in node_pr:
                # print("***********")
                Pr += P[root[0] - 1][i - 1] * node_pr[root[i]]
            else:
                # print("root[0]=",root[0])
                Pr += P[root[0] - 1][i - 1] * compute_pr(MDDj[root[i]],root[i], MDDj, P, node_pr)
                # print("PR__",Pr)
    node_pr[index] = Pr
    # print("node_pr=",node_pr)
    return Pr

if __name__ == '__main__':
    n = eval(input("输入元件数n："))
    M = eval(input("输入最大值状态M："))
    MDDkj = []
    # P =[[0.0500,0.0950,0.0684,0.7866],[0.0500,0.0950,0.0684,0.7866], [0.0300,0.0776,0.0446,0.8478], [0.0300,0.0776,0.0446,0.8478]]
    # 随机数生成概率矩阵
    P = []
    for i in range(n):
        component = np.random.dirichlet(np.ones(M + 1), size=1)
        component = np.around(component, M+1).tolist()
        component = component[0]
        component = component

        P.append(component)
    contruct_time = 0.0
    evaluate_time = 0.0
    for i in range(1, M + 1):
        print(f"创建系统状态≥{i}的MDD：")
        k = eval(input(f"输入k{i}:"))
        start_contruct = time.perf_counter()
        BDD_dict = {}
        MDD_dict = {}

        index = BDDkiGen(k, n)
        MDDkiGen(i, M)
        # print("MDD_dict=", MDD_dict)
        MDDkj.append(MDD_dict)

        end_contruct = time.perf_counter()
        contruct_time += (end_contruct-start_contruct)
    MDDsj = []
    MDD_cur = MDDkj[0]
    MDDsj.append(MDD_cur)
    count = []
    count.append(len(MDD_cur))


    # combine_time = 0.0
    start_combine = time.perf_counter()
    for i in range(1, len(MDDkj)):
        combination_table = {}
        root1 = find_root(MDD_cur)
        # print("---",i,MDDkj[i])
        root2 = find_root(MDDkj[i])
        index = 0
        MDDs = {}
        node_and_node(root1, MDD_cur, root2, MDDkj[i], index, MDDs)
        # print("*********",MDDs)
        count.append(len(MDDs))
        MDD_cur = MDDs

        MDDsj.append(MDDs)

    end_combine = time.perf_counter()
    combine_time = (end_combine-start_combine)

    for MDDj in MDDsj:
        root_, index_ = find_root(MDDj)
        start_evaluate = time.perf_counter()
        node_pr = {}
        pr = compute_pr(root_, index_, MDDj, P, node_pr)
        end_evaluate = time.perf_counter()
        evaluate_time += (end_evaluate - start_evaluate)
        print("pr=", '%.4f'%pr)

    print("construct_time=",'%.4f' % (contruct_time * 1000))
    print("combine_time=",'%.4f' % (combine_time * 1000))
    print("all_time=",'%.4f' % ((contruct_time+combine_time) * 1000))
    print("evaluate_time=",'%.4f' % (evaluate_time * 1000), "ms")


    print("count==", count)
