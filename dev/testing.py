from klustakwik2 import *
from pylab import *
import time
import cPickle as pickle
import os
from random import sample

fname, shank = '../temp/testsmallish', 4

log_to_file(fname+'.klg', 'debug')
log_suppress_hierarchy('klustakwik', inclusive=False)

if os.path.exists(fname+'.pickle'):
# if False:
    start_time = time.time()
    data = pickle.load(open(fname+'.pickle', 'rb'))
    print 'load from pickle:', time.time()-start_time
else:
    start_time = time.time()
    raw_data = load_fet_fmask_to_raw(fname, shank)
    print 'load_fet_fmask_to_raw:', time.time()-start_time
    data = raw_data.to_sparse_data()
    pickle.dump(data, open(fname+'.pickle', 'wb'), -1)
    
print 'Number of spikes:', data.num_spikes
print 'Number of unique masks:', data.num_masks

# def callback(name, iter):
#     if name=='':
#         print 'Finished iteration', iter

kk = KK(data)#, iteration_callback=callback)

# if os.path.exists(fname+'.clu.'+str(shank)):
if False:
    print 'Loading clusters from file'
    clusters = loadtxt(fname+'.clu.'+str(shank), skiprows=1, dtype=int)
else:
    print 'Generating clusters'
    kk.cluster(100)
    clusters = kk.clusters
    savetxt(fname+'.clu.'+str(shank), clusters, '%d', header=str(amax(clusters)), comments='')

kk.clusters = clusters
kk.reindex_clusters()

num_to_show = 200

for cluster in xrange(kk.num_clusters_alive):
    if cluster % 4 == 0:
        figure()
    maskimg = []
    spikes = kk.get_spikes_in_cluster(cluster)
    if len(spikes)>num_to_show:
        spikes = sample(spikes, num_to_show)
    for spike in spikes:
        row = zeros(kk.num_features)
        unmasked = data.unmasked[data.unmasked_start[spike]:data.unmasked_end[spike]]
        row[unmasked] = data.masks[data.values_start[spike]:data.values_end[spike]]
        maskimg.append(row)
    if len(maskimg)==0:
        continue
    maskimg = array(maskimg)
    subplot(2, 2, cluster%4 + 1)
    imshow(maskimg, origin='lower left', aspect='auto', interpolation='nearest')
    gray()
    title(cluster)
show()
