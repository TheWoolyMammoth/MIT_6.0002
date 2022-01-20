###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import copy

#================================
# Part A: Transporting Space Cows
#================================
def simple_sort(cow_names,cow_weights):
    """
    takes the two lists consisting of cow names and weights and sorts the cows from heaviest to lightest
    """

    track_names=copy.deepcopy(cow_names)
    track_weight=copy.deepcopy(cow_weights)
    sorted_names = []
    sorted_weights = []
    i=len(cow_names)
    while i > 0:
        max_val=max(track_weight)
        index=track_weight.index(max_val)
        cow_in_position=track_names[index]
        sorted_names.append(cow_in_position)
        sorted_weights.append(max_val)
        track_names.remove(cow_in_position)
        track_weight.remove(max_val)
        i-=1
    return sorted_names,sorted_weights



# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_data = open(filename,"r")
    cows_dict={}
    for line in cow_data:
        #print(line,end='\n')
        #removing newline and whitespace from line when splitting the two fields up
        split_line=line.rstrip().split(",")
        #converted the weight into an integer
        cows_dict[split_line[0]]=int(split_line[1])
    #print(cows_dict)
    cow_data.close()
    return cows_dict
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    start=time.time()
    names=[]
    weights=[]
    trips=[]
    for key in cows:
        # print(key)
        names.append(key)
        # print(cows[key])
        weights.append(cows[key])
    names,weights=simple_sort(names,weights)
    # print(names)
    # print(weights)
    # print(cows)
    cows_to_move=len(names)
    been_transported=[]
    while cows_to_move > 0:
        trip_weight = 0
        trip = []
        for cow in names:
            if cow not in been_transported:
                curr_cow_weight=weights[names.index(cow)]
                trip_weight+=curr_cow_weight
                if trip_weight <= limit:
                    trip.append(cow)
                    been_transported.append(cow)
                    cows_to_move-=1
                elif trip_weight > limit:
                    trip_weight-=curr_cow_weight
        # print(trip,trip_weight)
        trips.append(trip)
    end=time.time()
    runtime=end-start
    print("Time to Complete Greedy Method:", round(runtime,3))
    return trips


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    start=time.time()
    # trip is good when set to 0 (default), 1 if an individual trip exceeds limit
    trip_is_good=0
    trips_within_limit = []
    run_is_good=0
    for run in get_partitions(cows):
        # print(run)
        for trip in run:
            # print(trip)
            trip_weight=0
            for cow_name in trip:
                # print(cow_name)
                trip_weight+=cows[cow_name]
            if trip_weight > limit:
                run_is_good=1
                break
        if run_is_good == 1:
            run_is_good=0
            continue
        else:
            trips_within_limit.append(run)
    # count=0
    # for trip in trips_within_limit:
    #     count+=1
    #     print(trip)
    # print(count)
    # print(trips_within_limit)
    # for trip in trips_within_limit:
    #     print(trip)
    curr_best_trip=[]
    for run in trips_within_limit:
        len_curr_run=len(run)
        len_best_trip=len(curr_best_trip)
        if len_best_trip==0:
            curr_best_trip.append(run)
        else:
            if len_curr_run < len_best_trip:
                curr_best_trip.clear()
                curr_best_trip.append(run)
    # print(cows)
    # print(curr_best_trip)
    end=time.time()
    runtime=end-start
    print("Time to Complete Brute Force:",round(runtime,2))
    return curr_best_trip


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows=load_cows("ps1_cow_data.txt")
    list=greedy_cow_transport(cows)
    # print(list)
    print("Number of Trips to Complete Using Greedy:",len(list))
    list=brute_force_cow_transport(cows)
    # print(list)
    print("Numer of Trips to Complete Using Brute Force:",len(list[0]))




cows=load_cows("ps1_cow_data.txt")
# print(greedy_cow_transport(cows))
# brute_force_cow_transport((cows))
compare_cow_transport_algorithms()
print("--------")
cows=load_cows("ps1_cow_data_2.txt")
# greedy_cow_transport(cows)
# brute_force_cow_transport((cows))
compare_cow_transport_algorithms()