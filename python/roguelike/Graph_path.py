



class PATH:

    def __init__(self, price = None):
        self.price =  price
        self.path = []
    def __str__(self):
        return f'{self.price}'
##    def update(self, price, path):

class GRAPH:

    @classmethod
    def map(cls, mat, available = None, metric = None):
        if available==None:
            available = lambda x: 0<=x[0]<len(mat) and 0<=x[1]<len(mat[0])
        if metric == None:
            metric = lambda x, y: ((x[0]-y[0])**2+(x[1]-y[1])**2)**(1/2)
        vs = len(mat)*len(mat[0])
        ret = [[None for i in range(vs)] for j in range(vs)]
        print(len(mat), len(mat[0]))
        print(len(ret), len(ret[0]))
        for i in range(len(mat)):
            for j in range(len(mat[i])):
##                neighbours = []
                for n in [-1, 0, 1]:
                    for m in ([-1, 0, 1] if n!=0 else [-1, 1]):
                        if available([i+n, j+m]):
##                            print('--\n', i*len(mat[0])+j, i+n, j+m, (i+n)*len(mat[0])+j+m)
##                            if n**2+m**2==2:
##                                ret[i*len(mat)+j][(i+n)*len(mat)+j+m] = 2**(1/2)
                            ret[i*len(mat[0])+j][(i+n)*len(mat[0])+j+m] = metric((i, j), (i+n, j+m))
        return cls(ret)

    def __init__(self, graph):
        self.graph = graph
        self.paths = [[PATH(0 if i==j else None) for i in range(len(self.graph[0]))] for j in range(len(self.graph))]

    def solve(self):
        for start in range(len(self.graph)):
            # actual = start
            nset = [start]
            # print(nset)
            while nset!=[]:
                next_set = []
                for actual in nset:
                    # print('-', actual)
                    for neighbour in [i for i in range(len(self.graph)) if self.graph[actual][i] != None]:
                        # print(neighbour)
                        if self.paths[start][neighbour].price == None or self.paths[start][actual].price+self.graph[actual][neighbour]<self.paths[start][neighbour].price:
                            self.paths[start][neighbour].path =  self.paths[start][actual].path+[neighbour]
                            self.paths[start][neighbour].price = self.paths[start][actual].price+self.graph[actual][neighbour]
                            next_set.append(neighbour)
                nset = next_set

if __name__=='__main__':
    g = GRAPH([[None,  10,  30,  50,  10],
               [None,None,None,None,None],
               [None,None,None,None,  10],
               [None,  40,  20,None,None],
               [10  ,None,  10,  30,None]])
    g.solve()
    for i in g.paths:
        for j in i:
            print(j.path)
        print()











