import numpy as np
import matplotlib.pyplot as plt

Rnum = 1000.0
x = np.linspace(0.0,1.0,num=8192)
dx = 1.0/np.shape(x)[0]

tsteps = np.linspace(0.0,2.0,num=400)
dt = 2.0/np.shape(tsteps)[0]

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
# This is the Burgers problem definition
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
def exact_solution(t):
    t0 = np.exp(Rnum/8.0)

    return (x/(t+1))/(1.0+np.sqrt((t+1)/t0)*np.exp(Rnum*(x*x)/(4.0*t+4)))

def collect_snapshots():
    snapshot_matrix = np.zeros(shape=(np.shape(x)[0],np.shape(tsteps)[0]))

    trange = np.arange(np.shape(tsteps)[0])
    for t in trange:
        snapshot_matrix[:,t] = exact_solution(tsteps[t])[:]

    snapshot_matrix_mean = np.mean(snapshot_matrix,axis=1)
    snapshot_matrix = (snapshot_matrix.transpose()-snapshot_matrix_mean).transpose()

    return snapshot_matrix, snapshot_matrix_mean

# Method of snapshots to accelerate
def method_of_snapshots(Y): #Mean removed
    '''
    Y - Snapshot matrix - shape: NxS
    '''
    new_mat = np.matmul(np.transpose(Y),Y)
    w, v = np.linalg.eig(new_mat)

    # Bases
    phi = np.matmul(Y,np.real(v))
    trange = np.arange(np.shape(Y)[1])
    phi[:,trange] = -phi[:,trange]/np.sqrt(np.abs(w)[:])

    return phi# POD modes

# SVD method
def svd_pod(Y): #Mean removed
    '''
    Y - Snapshot matrix - shape: NxS
    returns phi - left singular vectors
    '''
    u, s, v = np.linalg.svd(Y)

    return u# POD modes


# Collect data
total_data, total_data_mean = collect_snapshots()
num_snapshots = total_data.shape[1]
num_dof = total_data.shape[0]

# Generate serial POD with MOS
modes = method_of_snapshots(total_data)
# Check that this guy is close to one
print('Inner product of similar modes summed:',np.sum(np.matmul(modes[:,1:2].T,modes[:,1:2])))
# Check that this guy is close to zero
print('Inner product of dissimilar modes summed:',np.sum(np.matmul(modes[:,1:2].T,modes[:,2:3])))
np.save('Serial_Modes_MOS.npy',modes)

# Generate serial POD with SVD
modes = svd_pod(total_data)
# Check that this guy is close to one
print('Inner product of similar modes summed:',np.sum(np.matmul(modes[:,1:2].T,modes[:,1:2])))
# Check that this guy is close to zero
print('Inner product of dissimilar modes summed:',np.sum(np.matmul(modes[:,1:2].T,modes[:,2:3])))
np.save('Serial_Modes_SVD.npy',modes)
exit()

total_ranks = 6

npr = int(num_dof/total_ranks)

for i in range(total_ranks-1):
    rank_data = total_data[i*npr:(i+1)*npr,:]
    np.save('points_rank_'+str(i)+'.npy',rank_data)

i = total_ranks-1
rank_data = total_data[i*npr:,]

np.save('points_rank_'+str(total_ranks-1)+'.npy',rank_data)