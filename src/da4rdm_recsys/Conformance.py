import pm4py
import sys


def check_conformance(log_network, log_to_confirm, fitness_type):
    try:
        net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log_network)
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in creating petri net for conformance check.")

    try:
        if fitness_type.lower() == "token":
            token_based_fitness = pm4py.conformance_diagnostics_token_based_replay(log_to_confirm, net, initial_marking,
                                                                               final_marking)
            return token_based_fitness[0]['trace_is_fit']
        elif fitness_type.lower() == "alignment":
            alignment_based_fitness = pm4py.fitness_alignments(log_to_confirm, net, initial_marking, final_marking)
            if alignment_based_fitness['averageFitness'] == 1.0:
                return True
            else:
                return False
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in calculating fitness.")
