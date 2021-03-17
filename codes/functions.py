from codes.requirements import *


def conversion(el,tot):
    '''
    Inputs
        - el: element of a list
        - tot: sum of all the elements in the list
        
    Returns
        - new: normalized element
    '''
    
    new = el/tot
    return new


def compute_max_operational_speed(row):
    '''
    Inputs
        - row: df row related to a vessel 
    
    Returns
        - max_op_speed: max operational speed for the vessel
    '''
    
    tot = sum(row)
    if tot > 0:
        row = [conversion(i,tot) for i in row] # normalization s.t. elements sum up to 1
    else:
        row = row # vessels whose 100% of time is spent under 3 knots
    #print(row)
    #print(sum(row))
    row = np.cumsum(row) 
    try:
        idx_max_op_speed = [n for n,i in enumerate(row) if i<=0.95 ][-1]
        max_op_speed = list_of_speeds[idx_max_op_speed]
    except:
        # for vessels that have already achieved 100% of sailing time in the first slot 3-3.5 
        # we put the min value of speed = 3 knots
        max_op_speed = 3 
    
    return max_op_speed


def real_prop_power(row):
    '''
    Inputs
        - row: df row related to a vessel
    Returns
        - result: real propulsion power demand for the vessel
    '''
    
    imo = row[0]
    max_op_speed = row[1]
    main_engine_p85 = row[2]
    design_speed = row[3]
    result = main_engine_p85 * (max_op_speed / design_speed)**3 
    return result


def check(row):
    '''
    Inputs
        - row: df row related to a vessel
    Returns
        - 1: if the vessel is EPL-addressable
        - 0 otherwise
    '''
    
    imo = row[0]
    max_op_speed = row[1]
    main_engine_p85 = row[2]
    design_speed = row[3]
    real_prop_p = row[4]
    ridotto = main_engine_p85 - (0.1)*main_engine_p85
    if ridotto >= real_prop_p:
        return 1
    else:
        return 0
    
    
def plot_frequency(epl_vessels_all_info,col, color, title,typo,x_lab):
    column = epl_vessels_all_info[col]
    column_freq = dict(Counter(column))
    column_freq = sorted(column_freq.items(), key=lambda x:x[1], reverse = True)
    x_pos = np.arange(1, len(column_freq)+1, 1)
    x = [x[0] for x in column_freq]
    y = [x[1] for x in column_freq]
    labels = x
    plt.figure(figsize=(10,8))
    plt.bar(x,y, color =color, 
            width = 0.7)
    plt.xticks(x, labels,rotation=80)
    plt.xlabel(x_lab)
    plt.ylabel('Frequency')
    plt.title(title)
    plt.savefig('results/{}_epl_addressable.png'.format(typo),bbox_inches = "tight")
    plt.show()
    
    
def plot_frequency2(epl_vessels_all_info,col, color, title):
    plt.figure(figsize=(20,10))
    column = epl_vessels_all_info[col]
    column_freq = dict(Counter(column))
    #print(column_freq)
    column_freq = sorted(column_freq.items(), key=lambda x:x[1], reverse = True)
    x_pos = np.arange(1, len(column_freq)+1, 1)
    x = [x[0] for x in column_freq]
    y = [x[1] for x in column_freq]
    labels = x
    plt.bar(x_pos,y, color =color, width = 0.7)
    plt.xticks(x_pos, labels,rotation=80)
    plt.xlabel('Country')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.savefig('results/costumers_epl_addressable.png')
    plt.show()
    
def plot_frequency3(epl_vessels_all_info):
    customers_dict = Counter(epl_vessels_all_info['Customer ID'].values) # dict of customers and related number of purchases
    customers_dict = sorted(customers_dict.items(), key=lambda x:x[1], reverse = True) # order the above dict
    customers_10purchase = customers_dict[:22] # dict of customers with at least 10 purchases
    keys = [t[0] for t in customers_10purchase]
    values = [t[1] for t in customers_10purchase]
    plt.figure(figsize=(10,8))
    x = np.arange(1,len(keys)+1, 1)
    plt.bar(x, values, color = 'orange',width = 0.7)
    plt.xticks(x, keys,rotation=80)
    plt.xlabel('ID')
    plt.ylabel('Frequency')
    plt.title('Customers ID with at least 10 purchases')
    plt.savefig('results/costumersid_epl_addressable.png')
    plt.show()