import numpy as np
import utility as util

from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, FuncFormatter)

def format_func(value, tick_number):
    t = int(value//6)
    if t==2 or t==4 or t==6 or t==8 or t==10:
        return str(t) + ":00 am"
    if t==12:
        return str(t) + ":00 pm"
    if t > 12 and (t-12)%2 == 0:
        return str(t-12) + ":00 pm"
    return "" 
        
def fig_trans_load_vs_time(result_path, trans, env=None):
    result = util.load_dict(result_path)
    x = []
    for key in result:
        for subKey in result[key]:
            x.append(subKey)

        break
    
    x = np.array(x)
    x = np.sort(x)
    
    fig, ax = plt.subplots()

    ax.xaxis.set_major_locator(MultipleLocator(6))
    ax.xaxis.set_major_formatter(FuncFormatter(format_func))

    ax.xaxis.set_minor_locator(MultipleLocator(1))

    
    linewidth=1.0
    legend = []
    y = 3*env['transRating'][3*trans]*np.ones(len(x))
    
    legend.append('rating')
    plt.plot(x,y,'--',linewidth=linewidth)
    for key in result:
        #if key=='llf' or key=='edf':
        #    continue
        y = []
        legend.append(key)
        for i in x:
            y.append(result[key][i]['trans_load'][(3 * trans + 0)] + result[key][i]['trans_load'][(3 * trans + 1)] + result[key][i]['trans_load'][(3 * trans + 2)])

        y = np.array(y)
        if key=='base_load':
            plt.plot(x, y,linewidth=linewidth, alpha=0.3)
        else:
            plt.plot(x, y,linewidth=linewidth)

    plt.legend(legend)

    plt.title('Transformer (#'+ str(trans)+')'+' Loading')
    plt.xlabel('Time')
    plt.ylabel('kVA')
 
    plt.xticks(rotation=30)
    plt.show()

def autolabel(rects, ax, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = round(rect.get_height(), 2)
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


def fig_compare(result_path, user_type, last_slot, env):
    result = util.load_dict(result_path)
    #men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
    #women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
    jain_means = []
    jain_std = []
    
    soc_means = []
    soc_std = []
    
   
    
    algo_name = []
    for key in result:
        if key == 'base_load':
            continue
        algo_name.append(key)
        temp = []
        for subKey in result[key]:
            ev_power = []
            for i in range(0, env['evNumber']):
                if env['evDriverType'][i] == user_type:
                    ev_power.append(result[key][subKey]['ev_power'][i])
            temp.append(util.jain_index(ev_power))

        temp = np.array(temp)

        jain_means.append(np.average(temp))
        jain_std.append(np.std(temp))
        
        remaining_demand = []
        battery = []

        for i in range(0, env['evNumber']):
           if env['evDriverType'][i] == user_type:
               remaining_demand.append(result[key][last_slot]['remaining_demand'][i])
               battery.append(env['battery'][i])

        remaining_demand = np.array(remaining_demand)/60.0
        battery = np.array(battery)
        print(key)
        print(remaining_demand)

        temp = (battery - remaining_demand)/battery
        count = 0
        #print(key)
        #print(temp)
        for i in range(len(temp)):
            if temp[i] >= 0.95:
                count+=1
        
        soc_means.append(count/len(temp))
        soc_std.append(0.0)

    ind = np.arange(len(jain_means))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, jain_means, width, yerr=jain_std,
                    label='Jain Index', hatch='/')
    rects2 = ax.bar(ind + width/2, soc_means, width, yerr=soc_std,
                    label='% of EV with\n >95% SoC')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Values')
    ax.set_title('Performances')
    ax.set_xticks(ind)
    #ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    ax.set_xticklabels(algo_name)
    ax.legend()
    
    autolabel(rects1, ax, "left")
    autolabel(rects2, ax, "right")

    fig.tight_layout()

    plt.show()


def fig_soc_vs_time(result_path, usr_type, algo, slot=60):
    result = util.load_dict(result_path)
    x = []
    for key in result:
        for subKey in result[key]:
            x.append(subKey)

        break

    x = np.array(x)
    x = np.sort(x)
    legend = []
    for key in result:
        if key == algo:
            y = [[], [], []]
            temp = [[], [], []]
            for i in x:
                rd = result[key][i]['remaining_demand']
                for j in range(0, len(rd)):
                    temp[usr_type[j]].append(rd[j])

                temp_ = np.array(temp)
                y[0].append(np.average(temp_[0]))
                legend.append('usr_type ' + str(0))
                y[1].append(np.average(temp_[1]))
                legend.append('usr_type ' + str(1))
                y[2].append(np.average(temp_[2]))
                legend.append('usr_type ' + str(2))

            y = np.array(y) / 3600.0
            plt.plot(x, y[0])
            plt.plot(x, y[1])
            plt.plot(x, y[2])
            plt.legend(legend)

    plt.title('Remaining Demand: ' + algo)
    plt.xlabel('Time Slots (1 slot = ' + str(slot) + ' sec)')
    plt.ylabel('kWh')
    plt.show()

def fig_conv_ana(result_path):
    result = load_dict(result_path)['decentral']
    x = []
    for key in result['gamma']:
        x.append(key)

    x = np.array(x)
    x = np.sort(x)
    
    linewidth=1.0
    y = []
    
    for key in x:
        y.append(result['gamma'][key])
        
    #plt.legend([])
    plt.plot(x, y)
    plt.title('95% Convergence')
    plt.xlabel('gamma')
    plt.ylabel('iter')
    plt.show()

if __name__ == '__main__':
    env = util.load_dict('env/static.txt')
    fig_soc_vs_time('result/test.txt', (env['evDriverType']), algo='llf')
    #fig_trans_load_vs_time('result/test.txt', trans=2, env=env)
    #fig_compare('result/test.txt', 1, 100, env)
    #fig_conv_ana('result/meta_large.txt')

