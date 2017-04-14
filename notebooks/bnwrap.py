import time, os, csv, copy, pprint, openpnl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from functools import reduce as _reduce
import copy

class bn:

    def __init__(self):
        pass

    # Fetch the dataset if needed ....
    def download_if_needed(self, url, filename):
        if not os.path.isfile(filename):
            import urllib2
            resp = urllib2.urlopen(url)
            fd = open(filename,'w')
            fd.write(resp.read())
            fd.close()

    def dataset_fields(self, filename, skip_lines=0):

        # Load the dataset
        self.fd = open(filename,'r')
        self.fr = csv.reader(self.fd,delimiter=',')

        # Load in the headers to choose from ...
        for i in range(0,skip_lines+1):
            self.all_node_names = self.fr.next()

        print "All Available Fields"
        for i in range(0, len(self.all_node_names)):
            print i, self.all_node_names[i]

    def set_used_fields(self, field_list):
        self.node_idx = field_list
        self.node_names = map(lambda x: self.all_node_names[x], self.node_idx)
        pprint.pprint(zip(range(0,len(self.node_names)),self.node_names))

    def load_dataset(self, max_cardinality=20):

        self.node_vals  = {}
        self.node_card  = {}
        self.node_numeric = {}

        # populate node names
        for k in self.node_names:
            self.node_vals[k] = set([])

        # populate node values
        records = []
        for r in self.fr:
            if len(r) > 0:
                use_rec = map(lambda x: r[x], self.node_idx)
                records.append(use_rec)
                for i,k in enumerate(self.node_names):
                    self.node_vals[k].update([r[self.node_idx[i]]])

        # convert back to lists
        for k in self.node_names:
            self.node_vals[k] = list(self.node_vals[k])

        # populate node cardinality
        for k in self.node_names:
            self.node_card[k] = len(self.node_vals[k])

        print "Node Cardinality:"
        pprint.pprint(self.node_card)

        def is_numeric(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        # Find numeric fields
        for k in self.node_names:
            is_num = True
            self.node_numeric[k] = True
            for v in self.node_vals[k]:
                if not is_numeric(v):
                    self.node_numeric[k] = False

        print "Node Numeric:"
        pprint.pprint(self.node_numeric)

        # Quantize fields which meet our criteria ( is_numeric && card > max_card )
        self.qrecords = copy.copy(records)
        for i,k in enumerate(self.node_names):
            if self.node_numeric[k] and self.node_card[k] > max_cardinality:
                print "Quantize field: ", i, k, " %d -> %d "%( self.node_card[k], max_cardinality )
                old_vals = np.array(map(lambda x: float(x[i]), records))
                bins = np.linspace(min(old_vals), max(old_vals), max_cardinality-1)
                newvals = np.digitize(old_vals, bins, right=True)
                binstr = ['<%0.02f'%(bins[0])]
                for j in range(0,len(bins)-1):
                    binstr.append("%0.02f-%0.02f"%(bins[j],bins[j+1]))
                self.node_vals[k] = binstr
                for j in range(0,len(self.qrecords)):
                    self.qrecords[j][i] = binstr[newvals[j]]

                self.node_card[k] = max_cardinality
                self.node_vals[k] = binstr

    def to_numeric(self, shuffle=False):
        # Convert dataset to numeric form
        self.X = np.zeros([len(self.qrecords), len(self.node_names)], dtype='int32')
        for i in range(0,len(self.qrecords)):
            for j in range(0,len(self.node_names)):
                self.X[i,j] = self.node_vals[self.node_names[j]].index(self.qrecords[i][j])
        if shuffle:
            np.shuffle(self.X)

    def fit_bn_structure(self, max_fan_in=1, n_restarts=100, n_records=None):

        X_train = self.X
        if not n_records == None:
            X_train = self.X[0:n_records,:]

        # BN Structure Learning
        self.bn = openpnl.mkSkelBNet(map(lambda x: self.node_card[x], self.node_names))
        self.sl = openpnl.mkCMlStaticStructLearnHC(self.bn, max_fan_in, n_restarts)
        self.sl.SetPyData(self.bn, X_train)
        a = time.time()
        self.sl.Learn();
        b = time.time()
        print "Structure Learning Time: %f (s) "%(b-a)
        dag = self.sl.GetResultDAG();
        self.adjMat = dag.adjMatrix(len(self.node_names)**2).reshape([len(self.node_names),len(self.node_names)])
        self.numNodes = self.adjMat.shape[0]

    def plot_network(self, figsize=(8,6)):
        print self.adjMat
        import networkx as nx
        G = nx.DiGraph(self.adjMat)

        namemap = dict(zip(range(0,len(self.node_names)), map(lambda x,y: str(x)+" "+y, range(0,len(self.node_names)),self.node_names)))

        print "DAG Plot"
        lay = nx.spring_layout(G)

        with sns.axes_style("white"):
            plt.figure(figsize=figsize)
        nx.draw_networkx(G,
                 #pos=nx.random_layout(G),
                 #pos=nx.spring_layout(G),
                 #pos=nx.shell_layout(G),
                 pos=nx.fruchterman_reingold_layout(G),
                 #pos=nx.spectral_layout(G),
                 node_color='c',
                 labels=namemap,
                 arrows=True,
                 node_size=800)
        cur_axes = plt.gca()
        cur_axes.axes.get_xaxis().set_visible(False)
        cur_axes.axes.get_yaxis().set_visible(False)

    def edges(self):
        edges = []
        for i in range(self.numNodes):
            for j in range(self.numNodes):
                if self.adjMat[i,j]:
                    edges.append( (i,j) )
        return edges

    def edgedict(self):
        edgedict = {}
        for s,d in self.edges():
            if edgedict.has_key(s):
                edgedict[s].append(d)
            else:
                edgedict[s] = [d]
        for k in edgedict.keys():
            edgedict[k] = set(edgedict[k])
        return edgedict

    def define_network(self, edges):
        self.adjMat = np.zeros( (self.numNodes, self.numNodes), dtype=np.int32 )
        self.numNodes = self.adjMat.shape[0]
        for i,j in edges:
            self.adjMat[i,j] = 1
        print self.adjMat

    # Adapted from https://pypi.python.org/pypi/toposort/1.0
    def toposort(self, data):
        # Special case empty input.
        if len(data) == 0:
            return
        # Copy the input so as to leave it unmodified.
        data = data.copy()
        # Ignore self dependencies.
        for k, v in data.items():
            v.discard(k)
        # Find all items that don't depend on anything.
        extra_items_in_deps = _reduce(set.union, data.values()) - set(data.keys())
        # Add empty dependences where needed.
        data.update({item:set() for item in extra_items_in_deps})
        while True:
            ordered = set(item for item, dep in data.items() if len(dep) == 0)
            if not ordered:
                break
            yield ordered
            data = {item: (dep - ordered)
            for item, dep in data.items()
                if item not in ordered}
        if len(data) != 0:
            raise ValueError('Cyclic dependencies exist among these items: {}'.format(', '.join(repr(x) for x in data.items())))

    # Adapted from https://pypi.python.org/pypi/toposort/1.0
    def toposort_flatten(self, data, sort=True):
        result = []
        for d in self.toposort(data):
            result.extend((sorted if sort else list)(d))
        return result

    def topsort(self):
        self.topo_mapping = self.toposort_flatten(self.edgedict())[::-1]
        self.adjMat3 = np.zeros( (self.numNodes, self.numNodes), dtype=np.int32 )
        for i in range(0,self.numNodes):
            for j in range(0,self.numNodes):
                self.adjMat3[i,j] = self.adjMat[self.topo_mapping[i], self.topo_mapping[j]]

    def create_bn(self):
        pGraph = openpnl.CGraph.CreateNP(self.adjMat3)
        dag2 = openpnl.CDAG.Create(pGraph)

        # set up node types
        isDiscrete = True
        nA = [0]*(self.numNodes)

        nodeTypes = openpnl.pnlNodeTypeVector()
        nodeTypes.resize(self.numNodes)

        for i in range(self.numNodes):
            node_idx = self.topo_mapping[i]
            size = self.node_card[self.node_names[node_idx]]
            nodeTypes[i].SetType(isDiscrete, len(self.node_vals[self.node_names[node_idx]]))
            nA[i] = i
        nodeAssociation = openpnl.toConstIntVector(nA)

        print dag2.adjMatrix(len(self.node_names)**2).reshape([len(self.node_names),len(self.node_names)])

        # Create the Bayes Net with given top-sorted adjacency matrix
        self.bn = openpnl.CBNet.Create( self.numNodes, nodeTypes, nodeAssociation, dag2 )
        self.bn = openpnl.CBNet.CreateWithRandomMatrices(dag2,self.bn.GetModelDomain())

    def fit_bn_densities(self, num_records=None):

        X_train = self.X
        if not num_records == None:
            X_train = self.X[0:num_records,:]

        # CPD Learning
        pl = openpnl.CEMLearningEngine.Create(self.bn)
        pl.SetPyData(self.bn, X_train[0:,self.topo_mapping])

        pl.SetMaxIterEM(500)
        a = time.time()
        pl.Learn()
        b = time.time()
        print "CPD Learning Time: %f (s) "%(b-a)

    def node_indices(self):
        return zip(range(0,len(self.node_names)),self.node_names)

    def sample_density(self, enum=[0], evidence = {}, val_in_cond=True, engine='jtree'):

        # Which inference engine to use
        if engine == 'jtree':
            infeng = openpnl.CJtreeInfEngine.Create( self.bn )
        elif engine == 'pearl':
            infeng = openpnl.CPearlInfEngine.Create( self.bn )
        elif engine == 'naive':
            infeng = openpnl.CNaiveInfEngine.Create( self.bn )
        else:
            raise ValueError('unsupported inference engine')

        enum_idx = map(lambda x: self.topo_mapping.index(x), enum)

        ev = {}
        if(len(evidence)>0):
            nodes = list(evidence.keys())
            vals = list(evidence.values())

            node_idxs = map(lambda x: self.topo_mapping.index(x), nodes)

            a = np.vstack([node_idxs,vals]).astype('int32')
            infeng.enterEvidence(self.bn, a)

            for k,v in evidence.iteritems():
                nodename = self.node_names[k]
                nodeval =  self.node_vals[nodename][v]
                ev[nodename] = nodeval
        else:
            pass
            #ev = np.zeros([0,0],dtype='int32')
            #infeng.enterEvidence(bn, ev)

        # compute output shape
        shp = []
        for i in enum:
            shp.append(len(self.node_vals[self.node_names[i]]))



        targnames = map(lambda x: self.node_names[x], enum)
        if val_in_cond:
            expr = "P(%s | %s)"%( ",".join(targnames), ",".join(map(lambda x: "%s=%s"%(x[0],x[1]), ev.iteritems())))
        else:
            expr = "P(%s | %s)"%( ",".join(targnames), ",".join(map(lambda x: "%s"%(x[0]), ev.iteritems())))

        # inference and reshape ...
        return map(lambda x: self.node_names[x], enum), ev, expr, infeng.sampleNodes(enum_idx).reshape(shp)


    def plot_density_1d(self, enum=[0], evidence={}, log=False, engine='jtree'):
        assert(len(enum)==1)
        p,cond,expr,rv = self.sample_density(enum, evidence=evidence, engine=engine)
        fig, ax = plt.subplots()
        pvals = self.node_vals[p[0]]
        width = 0.5
        if log:
            rv = np.log10(rv)
        rects1 = ax.bar(range(0,len(pvals)), rv[0:len(pvals)], width, color='b')
        ax.set_xticks(np.array(range(0,len(pvals)))+width/2)
        ax.set_xticklabels(pvals, rotation=45)
        plt.xlabel(self.node_names[enum[0]])
        if log:
            plt.ylabel('log-probability density')
            plt.title('log10 '+expr)
        else:
            plt.ylabel('probability density')
            plt.title(expr)

    def plot_multidensity_1d(self, enum=[0], evidence=[{}], log=False, mode='bar', engine='jtree'):
        assert(len(enum)==1)
        N = len(evidence)
        agg_width = 0.8
        width = agg_width/N
        labels = []
        colors = ['b','g','r','c','m','y','k','w']
        rects = []
        fig, ax = plt.subplots()
        for i,ev in enumerate(evidence):
            p,cond,expr,rv = self.sample_density(enum, evidence=ev, val_in_cond=False, engine=engine)
            pvals = self.node_vals[p[0]]
            n1 = self.node_names[ev.keys()[0]]
            n2 = self.node_vals[n1][ev.values()[0]]
            if log:
                rv = np.log10(rv)
            if mode == 'bar':
                rects1 = ax.bar(np.array(range(0,len(pvals)))+width*i, rv[0:len(pvals)], width)
                #rects1 = ax.bar(np.array(range(0,len(pvals)))+width*i, rv[0:len(pvals)], width, color=colors[i])
                rects.append(rects1)
                labels.append(n2)
            else:
                plt.plot(rv[0:len(pvals)], label=n2)
        ax.set_xticks(np.array(range(0,len(pvals)))+width/2)
        ax.set_xticklabels(pvals, rotation=45)
        plt.xlabel(self.node_names[enum[0]])
        legend_label = '%s value'%(self.node_names[ev.keys()[0]])
        if mode == 'bar':
            plt.legend( rects, labels, title=legend_label )
        else:
            plt.legend(title=legend_label )
        if log:
            plt.ylabel('log-probability density')
            plt.title('log10 '+expr)
        else:
            plt.ylabel('probability density')
            plt.title(expr)

    def plot_density_2d(self, enum=[0], evidence={}, log=False, figsize=(10,8), engine='jtree'):
        assert(len(enum)==2)
        p,cond,expr,rv = self.sample_density(enum, evidence=evidence, engine=engine)
        with sns.axes_style("white"):
            fig, ax = plt.subplots(figsize=figsize)
        pvals0 = self.node_vals[p[0]]
        pvals1 = self.node_vals[p[1]]
        width = 0.5
        cmap=plt.cm.Blues
        if log:
            rv = np.log10(rv)
        im = ax.imshow(rv, interpolation='nearest', cmap=cmap, aspect='auto')
        lbls1 = map(lambda x: unicode(x, errors='ignore').encode('ascii', 'ignore'), self.node_vals[self.node_names[enum[0]]])
        lbls2 = map(lambda x: unicode(x, errors='ignore').encode('ascii', 'ignore'), self.node_vals[self.node_names[enum[1]]])
        #lbls2 = map(lambda x: x.encode('ascii', 'ignore'), self.node_vals[self.node_names[enum[1]]])
        tm1 = np.arange(len(lbls1))
        tm2 = np.arange(len(lbls2))
        plt.yticks(tm1, lbls1)
        plt.xticks(tm2, lbls2,rotation=45)
        plt.ylabel(self.node_names[enum[0]])
        plt.xlabel(self.node_names[enum[1]])
        plt.tight_layout()
        fig.colorbar(im)
        if log:
            plt.title('log10 '+expr)
        else:
            plt.title(expr)

    def print_expr(self, enum, evidence={}):
        a = time.time()
        p,cond,expr,rv = self.sample_density(enum, evidence)
        b = time.time()
        print 'Marginal variables: ',p
        print 'Evidence',cond
        print 'Probability expression',expr
        print 'Density',rv,len(rv)
        print 'Inference time: %f'%(b-a)
