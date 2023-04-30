import numpy as np
import matplotlib.pyplot as plt
import os

path = os.path.abspath("C:\\Users\\xiang\\Documents\\2023Spring\\9413\\VMIPS_project\\final_report\\picture")
dpi = 600

# vdmBanks descending 5 4 3 2 1
vdmBanks = np.array([3,7,10,13,16])
dp_vdmBanks = np.array([4620,2408,1910,1812,1812])
fc_vdmBanks = np.array([765192,401672,320264,304392,304392])
conv_vdmBanks = np.array([694786,402647,335087,343825,317575])

# numLanes 2 3 1 4 5
numLanes = np.array([1,2,4,6,10])
dp_numLanes = np.array([2536,2054,1812,1721,1661])
fc_numLanes = np.array([427272,345352,304392,288776,278536])
conv_numLanes = np.array([378823,337991,317575,309294,304190])

# queueDepth 2 1 3 4 5
queueDepth = np.array([2,4,6,8,10])
dp_queueDepth = np.array([1812,1812,1812,1812,1812])
fc_queueDepth = np.array([304392,304392,304392,304392,304392])
conv_queueDepth = np.array([317575,317575,317575,317575,317575])

# vlsPipelineDepth 2 3 1 4 5
vlsPipelineDepth = np.array([3,5,11,13,17])
dp_vlsPipelineDepth = np.array([1580,1638,1812,1870,2033])
fc_vlsPipelineDepth = np.array([261384,272136,304392,315144,344072])
conv_vlsPipelineDepth = np.array([234434,251938,317575,343829,399468])

# pipelineDepthMul 2 3 1 4 5
pipelineDepthMul = np.array([3,7,12,16,20])
dp_pipelineDepthMul = np.array([1740,1772,1812,1844,1876])
fc_pipelineDepthMul = np.array([295176,299272,304392,308488,312584])
conv_pipelineDepthMul = np.array([311950,314450,317575,320075,322575])

# pipelineDepthAdd 1 2 3 4 5
pipelineDepthAdd = np.array([2,5,8,11,14])
dp_pipelineDepthAdd = np.array([1812,1854,1896,1938,1980])
fc_pipelineDepthAdd = np.array([304392,312840,321288,329736,338184])
conv_pipelineDepthAdd = np.array([317575,328903,340231,351559,362887])

def data_plot(x_axis, y_axis, x_label, file_name):
    plt.plot(x_axis, y_axis[0], 'o-', label='Dot product')
    plt.plot(x_axis, y_axis[1], 'o-', label='Fully Connected Layer')
    plt.plot(x_axis, y_axis[2], 'o-', label='Convolution')
    plt.yscale('log')
    plt.xlabel(x_label)
    plt.ylabel('# Cycle')
    plt.legend()
    plt.grid()
    plt.savefig(os.path.abspath(os.path.join(path, file_name)), dpi=dpi)
    plt.close()

# Plot for vdmBanks
data_plot(x_axis=vdmBanks, y_axis=[dp_vdmBanks, fc_vdmBanks, conv_vdmBanks], x_label='# Vector Data Memory Bank', file_name='vdmBanks')

# Plot for numLanes
data_plot(x_axis=numLanes, y_axis=[dp_numLanes, fc_numLanes, conv_numLanes], x_label='# Vector Data Memory Bank', file_name='numLanes')

# Plot for queueDepth
data_plot(x_axis=queueDepth, y_axis=[dp_queueDepth, fc_queueDepth, conv_queueDepth], x_label='Queue Depth', file_name='queueDepth')

# Plot for vlsPipelineDepth
data_plot(x_axis=vlsPipelineDepth, y_axis=[dp_vlsPipelineDepth, fc_vlsPipelineDepth, conv_vlsPipelineDepth], x_label='Vector L/S Pipeline Depth', file_name='vlsPipelineDepth')

# Plot for pipelineDepthMul
data_plot(x_axis=pipelineDepthMul, y_axis=[dp_pipelineDepthMul, fc_pipelineDepthMul, conv_pipelineDepthMul], x_label='Multiplication Pipeline Depth', file_name='pipelineDepthMul')

# Plot for pipelineDepthAdd
data_plot(x_axis=pipelineDepthAdd, y_axis=[dp_pipelineDepthAdd, fc_pipelineDepthAdd, conv_pipelineDepthAdd], x_label='Addition Pipeline Depth', file_name='pipelineDepthAdd')