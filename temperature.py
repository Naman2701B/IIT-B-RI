from scipy import io
import matplotlib.pyplot as plt

file = io.loadmat("C:/Users/ashok/Desktop/IIT RESEARCH/Task 4/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Case_2_P0.25B_Output/OLFA_185337_17-05-2024_R_T/TEMP_17-05-24_19-04/TEMP.mat")

def D3Plot_TA(outputfolder,selectedtsnapindex,conductorlist,radioflag):
    ax = plt.figure().add_subplot(2,1,projection='3d')
    
    # zticks = []
    # for i in range(0, len(zvalue)):
    #         zticks.append([])
    #         for j in range(0, len(zvalue[i])):
    #             zticks[i].append(zvalue[i][j])
    #             zvalue[i][j] = calculateTime(zvalue[i][j])
    #     zvalue = np.array(zvalue)
    #     zticks = np.array(zticks)
    #     super_y_axis = np.array(super_y_axis)
    #     ax.plot_surface(xvalues, zvalue, super_y_axis,  edgecolor='royalblue')
    #     ax.view_init(elev=20, azim=-145, roll=0)
    #     zvaluestoshow=[]
    #     ztickstoshow =[]
    #     for i in range(0, len(zvalue)):
    #         for j in range(0, len(zticks)):
    #             zvaluestoshow.append(zvalue[i][j])
    #             ztickstoshow.append(zticks[i][j])
    #     ax.set_yticks(zvaluestoshow, ztickstoshow)
    #     ax.set(xlabel='Distance (km)',ylabel='Time Snaps', zlabel=conductors[selectedconductors]+" Voltage (kV)" if radioflag == 0 else conductors[selectedconductors]+" Current (kA)")
    #     # plt.legend()
    #     plt.title("Load Flow Analysis 3D")