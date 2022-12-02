
# new:
#
# (1) or(DNF1, DNF2)
#     or(or(d11, ..., d1n), or(d21,..., d2n))   == or(d11,...,d2n)
# (2) exists(vars, DNF)
#     exists(vars, or(d1, ..., dn))   == or(exists(vars, d1),.., exists(vars, dn))
# (3) and(DNF1, DNF2)
#     and(or(d11, ..., d1n), or(d21,..., d2n))   == or(and(d11,d21),..., and(d1n,d2n))


from program import program as pg
import pddl 




def build_DNF_program(program):

    def recurse(program):

        if len(program.parts)==0:
            return pg.NondeterministicProgram([program])
        else:
            new_parts = [ recurse(part) for part in program.parts]


        # Rule (1): Associativity of disjunction.
        if isinstance(program, pg.NondeterministicProgram):
            result_parts = []
            for part in new_parts:
                result_parts.extend(part.parts)
            return pg.NondeterministicProgram(result_parts)

        # Rule (2): Distributivity disjunction/existential quantification.
        if isinstance(program, pg.PiProgram):
            parameters = program.parameters
            result_parts = [pg.PiProgram(parameters, (part,))
                            for part in new_parts[0].parts]
            return pg.NondeterministicProgram(result_parts)

        # Rule (3): Distributivity disjunction/conjunction.
        assert isinstance(program, pg.SequentailProgram)

        result_parts = new_parts.pop(0).parts
        while new_parts:
            previous_result_parts = result_parts
            result_parts = []
            parts_to_distribute = new_parts.pop(0).parts
            for part1 in previous_result_parts:
                for part2 in parts_to_distribute:
                    result_parts.append(pg.SequentailProgram((part1,part2)))
        return pg.NondeterministicProgram(result_parts)

    result = recurse(program).simplified()
    return result



# [4] Pull existential quantifiers out of conjunctions and group them.
#
# After removing universal quantifiers and creating the disjunctive form,
# only the following (representatives of) rules are needed:
# (1) exists(vars, exists(vars', phi))  ==  exists(vars + vars', phi)
# (2) and(phi, exists(vars, psi))       ==  exists(vars, and(phi, psi)),
#       if var does not occur in phi as a free variable.


def move_pi_quantifiers(program):

    def recurse(program):

        if len(program.parts)>0:
            parts = [recurse(part) for part in program.parts]
        else:
            return pg.SequentailProgram([program])

        # Rule (1): Combine nested quantifiers.
        if isinstance(program, pg.PiProgram):
            new_parameters = program.parameters
            new_part = parts[0]
            if isinstance(new_part, pg.PiProgram):
                new_parameters += new_part.parameters
                new_part = new_part.parts[0]
            return pg.PiProgram(new_parameters, (new_part,))

        # Rule (2): Pull quantifiers out of conjunctions.
        assert isinstance(program, pg.SequentailProgram)
        new_parameters = []
        new_parts = []
        for part in parts:
            if isinstance(part, pg.PiProgram):
                new_parameters += part.parameters
            new_parts+= part.parts

        new_seq_program = pg.SequentailProgram(new_parts)


        if new_parameters == list():
            return new_seq_program
        else:
            return pg.PiProgram(new_parameters, (new_seq_program,))

    return recurse(program)



def split_nondeterministic(program):

    if isinstance(program, pg.NondeterministicProgram):
        return program.parts
    else:
        return (program,)




def eliminate_pi_quantifiers(program):

    if isinstance(program, pg.PiProgram):
        return program.parameters, program.parts[0]
    else:
        return [], program


############################################################################################################################################


# After removing universal quantifiers, the (k-ary generalization of the)
# following rules suffice for doing that:
# (1) or(phi, or(psi, psi'))      ==  or(phi, psi, psi')
# (2) exists(vars, or(phi, psi))  ==  or(exists(vars, phi), exists(vars, psi))
# (3) and(phi, or(psi, psi'))     ==  or(and(phi, psi), and(phi, psi'))

#
# we can only handle condition which only has existential quantifiers
#
def build_DNF(condition):
    def recurse(condition):
        disjunctive_parts = []
        other_parts = []
        for part in condition.parts:
            part = recurse(part)
            if isinstance(part, pddl.Disjunction):
                disjunctive_parts.append(part)
            else:
                other_parts.append(part)
        if not disjunctive_parts:
            return condition

        # Rule (1): Associativity of disjunction.
        if isinstance(condition, pddl.Disjunction):
            result_parts = other_parts
            for part in disjunctive_parts:
                result_parts.extend(part.parts)
            return pddl.Disjunction(result_parts)

        # Rule (2): Distributivity disjunction/existential quantification.
        if isinstance(condition, pddl.ExistentialCondition):
            parameters = condition.parameters
            result_parts = [pddl.ExistentialCondition(parameters, (part,))
                            for part in disjunctive_parts[0].parts]
            return pddl.Disjunction(result_parts)

        # Rule (3): Distributivity disjunction/conjunction.
        assert isinstance(condition, pddl.Conjunction)
        result_parts = [pddl.Conjunction(other_parts)]
        while disjunctive_parts:
            previous_result_parts = result_parts
            result_parts = []
            parts_to_distribute = disjunctive_parts.pop().parts
            for part1 in previous_result_parts:
                for part2 in parts_to_distribute:
                    result_parts.append(pddl.Conjunction((part1, part2)))
        return pddl.Disjunction(result_parts)

    return recurse(condition).simplified()


# [3] Split conditions at the outermost disjunction.
def split_disjunctions(condition):

    if isinstance(condition, pddl.Disjunction):
        return condition.parts
    else:
        return (condition,)

def split_conjunctions(condition):
    if isinstance(condition, pddl.Conjunction):
        return condition.parts
    else:
        return (condition,)



# [4] Pull existential quantifiers out of conjunctions and group them.
#
# After removing universal quantifiers and creating the disjunctive form,
# only the following (representatives of) rules are needed:
# (1) exists(vars, exists(vars', phi))  ==  exists(vars + vars', phi)
# (2) and(phi, exists(vars, psi))       ==  exists(vars, and(phi, psi)),
#       if var does not occur in phi as a free variable.

def move_existential_quantifiers(condition):
    def recurse(condition):
        existential_parts = []
        other_parts = []
        for part in condition.parts:
            part = recurse(part)
            if isinstance(part, pddl.ExistentialCondition):
                existential_parts.append(part)
            else:
                other_parts.append(part)
        if not existential_parts:
            return condition

        # Rule (1): Combine nested quantifiers.
        if isinstance(condition, pddl.ExistentialCondition):
            new_parameters = condition.parameters + existential_parts[0].parameters
            new_parts = existential_parts[0].parts
            return pddl.ExistentialCondition(new_parameters, new_parts)

        # Rule (2): Pull quantifiers out of conjunctions.
        assert isinstance(condition, pddl.Conjunction)
        new_parameters = []
        new_conjunction_parts = other_parts
        for part in existential_parts:
            new_parameters += part.parameters
            new_conjunction_parts += part.parts
        new_conjunction = pddl.Conjunction(new_conjunction_parts)
        return pddl.ExistentialCondition(new_parameters, (new_conjunction,))

    return recurse(condition).simplified()


############################################################################################################################################

# [1] Remove universal quantifications from conditions.
#
# Replace, in a top-down fashion, <forall(vars, phi)> by <not(not-all-phi)>,
# where <not-all-phi> is a new axiom.
#
# <not-all-phi> is defined as <not(forall(vars,phi))>, which is of course
# translated to NNF. The parameters of the new axioms are exactly the free
# variables of <forall(vars, phi)>.

def test_condition_remove_universal_quantifiers(condition, type_map, task):

    def recurse(condition):
        # Uses new_axioms_by_condition and type_map from surrounding scope.
        if isinstance(condition, pddl.UniversalCondition):
            axiom_condition = condition.negate()
            parameters = sorted(axiom_condition.free_variables())
            typed_parameters = tuple(pddl.TypedObject(v, type_map[v]) for v in parameters)
            axiom = new_axioms_by_condition.get((axiom_condition, typed_parameters))
            if not axiom:
                condition = recurse(axiom_condition)
                axiom = task.add_axiom(list(typed_parameters), condition)
                new_axioms_by_condition[(condition, typed_parameters)] = axiom
            return pddl.NegatedAtom(axiom.name, parameters)
        else:
            new_parts = [recurse(part) for part in condition.parts]
            return condition.change_parts(new_parts)

    new_axioms_by_condition = {}
    if condition.has_universal_part():
        condition = recurse(condition)
        return condition
    else:
        return condition




############################################################################################################################################

#
# given a sequential program of the form a1;...; an, detect those test actions, and translate them into DNF, and split them.
# sequence
#
# 
import copy
#
#



def get_restricted_sequential_programs(seq_program, type_map, task):


    def recurse(sequence, cur_sequence, the_list):

        if len(sequence) == len(cur_sequence):
            the_list.append(pg.SequentailProgram(cur_sequence))
        else:
            cur_index = len(cur_sequence)
            cur_action = sequence[cur_index]

            if isinstance(cur_action, pg.SimpleAction):

                cur_sequence.append(cur_action)
                return recurse(sequence, cur_sequence, the_list)

            assert isinstance(cur_action, pg.TestAction)

            condition = test_condition_remove_universal_quantifiers(cur_action.condition, type_map, task)
            simple_conditions = [move_existential_quantifiers(c) for c in split_disjunctions(build_DNF(condition))]
            simple_test_actions = [pg.TestAction(sc) for sc in simple_conditions]

            for sta in simple_test_actions:
                copy_cur_sequence = copy.copy(cur_sequence)
                copy_cur_sequence.append(sta)

                recurse(sequence, copy_cur_sequence, the_list)

    restricted_sequential_programs = list()
    
    if isinstance(seq_program, pg.SimpleAction):
        recurse([seq_program], list(), restricted_sequential_programs)
    else:
        recurse(seq_program.parts, list(), restricted_sequential_programs)

    return restricted_sequential_programs


############################################################################################################################################

##
#  given a restricted sequential program, eliminate quantifiers in test actions
#
#

def eliminate_test_action_quantifiers(seq_program): 

    paras = list()
    new_parts = list()

    for action in seq_program.parts:
        if isinstance(action, pg.SimpleAction):
            new_parts.append(action)
            continue

        assert isinstance(action, pg.TestAction)
        if isinstance(action.condition, pddl.ExistentialCondition):
            paras += action.condition.parameters
            new_condition = action.condition.parts[0]
            new_parts.append(pg.TestAction(new_condition))
        else:
            new_parts.append(action)

    return paras, pg.SequentailProgram(new_parts)





