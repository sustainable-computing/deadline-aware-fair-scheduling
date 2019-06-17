import numpy as np
import scipy.io as spio
import DSSStartup
from matplotlib import pyplot as plt
import sys

tol = 1e-08
inf = 1e8

def log(x):
    return np.array([-inf if e <= 0.0 else np.log(e) for e in x])


def reciprocal(x):
    return np.array([inf if e <= 0.0 else 1.0 / e for e in x])


def f(x):
    shift = 500
    return np.array([0.0 if e <= -shift else e + shift + 1 for e in x])

def jain_index(x):
    x = np.array(x)
    sqr_sum = np.sum(x**2)
    if sqr_sum <= tol:
        return 1.0
    return (np.sum(x)**2)/(len(x)*sqr_sum)

def save_dict(file_name, dict_):
    f = open(file_name, 'w')
    f.write(str(dict_))
    f.close()


def load_dict(file_name):
    f = open(file_name, 'r')
    data = f.read()
    f.close()
    return eval(data)


def load(argv):
    dss_path = 'master33Full.dss'
    mat_path = 'PQ1DayF20.mat'
    env_path = 'env/default_env.txt'
    for i in range(1, len(argv)):
        name = argv[i]
        if '.dss' in name:
            dss_path = name
        elif '.mat' in name:
            mat_path = name
        elif '.txt' in name:
            env_path = name

    return (
     DSSStartup.dssstartup(dss_path), spio.loadmat(mat_path, squeeze_me=True), load_dict(env_path))

def autolabel(rects, ax, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


def fig_compare(result_path, env):
    result = load_dict(result_path)
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
            temp.append(jain_index(result[key][subKey]['ev_power']))
        temp = np.array(temp)

        jain_means.append(np.average(temp))
        jain_std.append(np.std(temp))

    ind = np.arange(len(jain_means))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, jain_means, width, yerr=jain_std,
                    label='Jain Index')
    #rects2 = ax.bar(ind + width/2, women_means, width, yerr=women_std,
    #                label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Values')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind)
    #ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    ax.set_xticklabels(algo_name)
    ax.legend()
    
    autolabel(rects1, ax, "left")
    #autolabel(rects2, ax, "right")

    fig.tight_layout()

    plt.show()
    
    
def fig_trans_load_vs_time(result_path, trans, slot=60, env=None):
    result = load_dict(result_path)
    x = []
    for key in result:
        for subKey in result[key]:
            x.append(subKey)

        break

    x = np.array(x)
    x = np.sort(x)
    
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
    plt.title('Transformer Loading: #' + str(trans))
    plt.xlabel('Time Slots (1 slot = ' + str(slot) + ' sec)')
    plt.ylabel('kVA')
    plt.show()


def fig_soc_vs_time(result_path, usr_type, algo, slot=60):
    result = load_dict(result_path)
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

                temp = np.array(temp)
                y[0].append(np.average(temp[0]))
                legend.append('usr_type ' + str(0))
                y[1].append(np.average(temp[1]))
                legend.append('usr_type ' + str(1))
                y[2].append(np.average(temp[2]))
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


if __name__ == '__main__':
    env = load_dict('env/static.txt')
    #fig_soc_vs_time('result/test.txt', (env['evDriverType']), algo='decentral')
    #fig_trans_load_vs_time('result/static.txt', trans=1, slot=60, env=env)
    fig_compare('result/static.txt', env)

