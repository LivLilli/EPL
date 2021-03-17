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