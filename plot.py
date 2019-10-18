import numpy as np
import utility as util

from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, FuncFormatter)

def format_func(value, tick_number):
    t = int(value//6)
    return str(t) + ":00"
    if t==2 or t==4 or t==6 or t==8 or t==10:
        return str(t) + ":00 am"
    if t==0:
        return str(t+12) + ":00 am"
    if t > 12 and (t-12)%2 == 0:
        return str(t-12) + ":00 pm"
    return "" 
        
def fig_trans_load_vs_time(result_path, trans, env=None):
    result = util.load_dict(result_path)
    '''
    temp = []
    for i in result['base_load']:
        temp.append(np.amin(np.array(env['transRating'])/np.array(result['base_load'][i]['trans_load'])))
    print(np.amax(np.array(temp)))
    '''
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

    #fig.add_subplot(221)
    linewidth=1.0
    legend = []
    y = 100*np.ones(len(x))
    
    legend.append('max')
    plt.plot(x,y,'--',linewidth=linewidth)

    for key in result:
        if key=='llf' or key=='edf' or key=='central' or key=='base_load':
            continue
        y = []
        legend.append(key)
        for i in x:
            y.append(result[key][i]['n_iter'])

        y = np.array(y)
        if key=='base_load':
            plt.plot(x, y,linewidth=linewidth, alpha=0.3)
        else:
            plt.plot(x, y,linewidth=linewidth)

    plt.legend(legend)

    plt.title('# of iterations required for 95% convergence')
    plt.xlabel('Time')
    plt.ylabel('# of iterations')
 
    plt.xticks(rotation=30)
    plt.show()
    
def fig_trans_load_subplot(result_path, trans_list, env):
    result = util.load_dict(result_path)

    x = []
    for key in result:
        for subKey in result[key]:
            x.append(subKey)

        break
    
    x = np.array(x)
    x = np.sort(x)
    
    plt.rcParams.update({'font.size': 24})
    fig, ax = plt.subplots(sharex=True, sharey=True)
    
    #ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
    #ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_ticks([])
    ax.xaxis.set_ticks([])
    ax.set_xlabel('\nTime')
    ax.set_ylabel('MVA\n')

    #fig.add_subplot(221)
    linewidth=1.0
    
    ii = 1
    for trans in trans_list:
        ax = fig.add_subplot(len(trans_list), 1, ii)
        
        if trans==0:
            ax.xaxis.set_major_locator(MultipleLocator(24))
            ax.xaxis.set_major_formatter(FuncFormatter(format_func))

            ax.xaxis.set_minor_locator(MultipleLocator(12))
        else:
            ax.get_xaxis().set_visible(False)

        
        legend = []
        #legend.append('')
        
        for key in result:
            if key=='LLF' or key=='EDF':
                continue
            y = []
            legend.append(key)
            for i in x:
                y.append(result[key][i]['trans_load'][(3 * trans + 0)] + result[key][i]['trans_load'][(3 * trans + 1)] + result[key][i]['trans_load'][(3 * trans + 2)])

            y = np.array(y)/1000
            if key=='Base Load':
                plt.plot(x, y,linewidth=linewidth, alpha=0.3)
            else:
                plt.plot(x, y,linewidth=linewidth)
        if ii == 1:
            #plt.legend()
            #plt.legend(legend, loc='upper left')
            plt.legend(legend)
        '''
        if trans==0:
            plt.title('Substation Loading')
        else:
            plt.title('Transformer (#'+ str(trans)+')'+' Loading')
        '''
        y = 3*env['transRating'][3*trans]*np.ones(len(x))/1000
        plt.plot(x,y,'--',linewidth=linewidth)

        #plt.xticks(rotation=30)
        #plt.yticks([])
        
        ii += 1
   
    plt.show()
    #plt.savefig('trans210.png')

def autolabel(rects, ax, xpos='center', h_offset=0):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    
    offset = {'center': 0, 'right': 1, 'left': -1}
    
    labels = ["{}".format(round(i.get_height(),2)) for i in rects]
    #labels = ['' if e=='1.0' else e for e in labels]
    #print(labels)
    '''
    for rect, label in zip(rects, labels):
        height = round(rect.get_height(), 2)
        ax.text(rect.get_x() + rect.get_width() / 2, height + 10, label,
                color='red', fontweight='bold', ha='center', va='top')
    '''
    
    for rect in rects:
        height = round(rect.get_height(), 2)
        height_str = '{}'.format(height)
        if height_str=='1.0':
            height_str = ''
        ax.annotate(height_str,
                    xy=(rect.get_x() + rect.get_width() / 2, height+h_offset),
                    xytext=(offset[xpos]*3, 10),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='center')
    return height

def fig_compare(result_path, last_slot, env):
    output = {}
    result = util.load_dict(result_path)
    #men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
    #women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
    fig, ax = plt.subplots()
    for user_type in [1]:
        output[user_type] = {}
        jain_means = []
        jain_std = []
        
        soc_means = []
        soc_std = []

        if user_type==-1:
            battery = np.array(env['battery'])
        else:
            battery = np.array([env['battery'][i] for i in range(0, env['evNumber']) if env['evDriverType'][i]==user_type])
        #print(len(battery))
        
        algo_name = []
        for key in result:
            if key == 'Base Load':
                continue
                
            output[user_type][key] = {}
            algo_name.append(key)
                
            temp = []
            for subKey in result[key]:
                #if key=='central':
                    #print(result[key][subKey]['x'])
                if user_type==-1:
                    value = result[key][subKey]['x']
                else:
                    c = result[key][subKey]['connected']
                    l = len(c)
                    value = [result[key][subKey]['x'][i] for i in range(0,l) if env['evDriverType'][c[i]]==user_type]
                    '''
                    if 'w' in result[key][subKey]:
                        w = [result[key][subKey]['w'][i] for i in range(0,l) if env['evDriverType'][c[i]]==user_type]
                    else:
                        w = np.ones(len(value)).tolist()
                    '''
                temp.append(util.jain_index(value))

            temp = np.array(temp)
            output[user_type][key]['jain'] = (np.average(temp), np.std(temp))
            jain_means.append(np.average(temp))
            jain_std.append(np.std(temp))

            if user_type==-1:
                remaining_demand = np.array(result[key][last_slot]['remaining_demand'])
            else:
                remaining_demand = np.array([result[key][last_slot]['remaining_demand'][i] for i in range(0, env['evNumber']) if env['evDriverType'][i]==user_type])

            #print(key)
            #print(remaining_demand)

            temp = (battery - remaining_demand)/battery
            count = 0
            #print(key)
            #print(temp)
            for i in range(len(temp)):
                if temp[i] >= 0.9:
                    count+=1
            
            output[user_type][key]['soc'] = (count/len(temp), 0.0)
            soc_means.append(count/len(temp))
            soc_std.append(0.0)

        ind = np.arange(len(jain_means))  # the x locations for the groups
        width = 0.3  # the width of the bars

        if user_type == 0:
            rec = ax.bar(ind - width/2, jain_means, width, yerr=jain_std,
                        label='Jain Index:Conservative', hatch='/')
            h_offset = autolabel(rec, ax)
            rec = ax.bar(ind - width/2, soc_means, width, yerr=soc_std,
                         bottom=jain_means, label='% of EV:Conservative')
            autolabel(rec, ax, h_offset=h_offset)
        else:
            rec = ax.bar(ind + width/2, jain_means, width, yerr=jain_std,
                        label='Jain Index:Risk Taker', hatch='*')
            h_offset = autolabel(rec, ax)
            rec = ax.bar(ind + width/2, soc_means, width, yerr=soc_std,
                         bottom=jain_means, label='% of EV:Risk Taker')
            autolabel(rec, ax, h_offset=h_offset)

        
        
        #autolabel(rects1, ax, "left")
        #autolabel(rects2, ax, "right")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Values')
    '''
    if user_type==-1:
        ax.set_title('Performances for all EVs')
    elif user_type==0:
        ax.set_title('Performances for Conservative EVs')
    elif user_type==1:
        ax.set_title('Performances for Risk-Taking EVs')
    else:
        ax.set_title('Performances for DishonestRisk-Taker EVs')
    '''
    ax.set_xticks(ind)
    #ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    ax.set_xticklabels(algo_name)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=5, fancybox=True, shadow=True)    
    #fig.tight_layout()
    #plt.show()
    print(output)
    util.save_dict('data_risk_taker.txt', output)
    #plt.savefig('compare_0_all_risk')
'''
def fig_compare_merge(algo_name, jain, soc):
    for key in jain:
        ind = np.arange(len(jain[key]['mean']))  # the x locations for the groups
        break

    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    for key in jain:
    rects1 = ax.bar(ind - width/2, jain_means, width, yerr=jain_std,
                    label='Jain Index', hatch='/')
    rects2 = ax.bar(ind + width/2, soc_means, width, yerr=soc_std,
                    bottom=jain_means, label='% of EV with\n $\geq$90% SoC')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Values')
    if user_type==-1:
        ax.set_title('Performances for all EVs')
    elif user_type==0:
        ax.set_title('Performances for Conservative EVs')
    elif user_type==1:
        ax.set_title('Performances for Risk-Taking EVs')
    else:
        ax.set_title('Performances for DishonestRisk-Taker EVs')
    ax.set_xticks(ind)
    #ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    ax.set_xticklabels(algo_name)
    ax.legend()
    
    autolabel(rects1, ax, "left")
    autolabel(rects2, ax, "right")

    fig.tight_layout()

    plt.show()
    #plt.savefig('compare_0_all_risk')
'''
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
    simu_params = util.load_dict('simu_params.txt')
    #env = util.load_dict('env/large.txt')
    env = util.load_dict(simu_params['env_path'])
    
    #fig_soc_vs_time(simu_params['save_path'], (env['evDriverType']), algo='central')
    #fig_trans_load_vs_time(simu_params['save_path'], trans=0, env=env)
    fig_trans_load_subplot(simu_params['save_path'], trans_list=[1,0], env=env)
    #fig_compare(simu_params['save_path'], 143, env)
    #fig_conv_ana('result/meta_large.txt')

