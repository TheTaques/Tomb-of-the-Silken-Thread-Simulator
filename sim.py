from math import floor
import random


def new_airs():
    return random.randint(1, 100)


def success(chance):
    return random.random() <= chance


# starting values
neededProgress = 30
yourProgress = 1
nightmares = 0
rivalsProgress = 1
usedSupplies = 0
airs = new_airs()
playedSigns = 0
confrontedRival = 0
stranglingWillowAbsintheUsed = 0
crypticCluesUsed = 0
inklingsOfIdentityGained = 0
actions = 0
echosGained = 0

# FL constants
fl_difficultyScaler = .6
cautiousApproachDifficulty = 50
boldApproachDifficulty = 100
buccaneeringApproachDifficulty = 160
completionDifficulty = 60
confrontationDifficulty = 72

# Your stats
# This simulation assumes a minimum watchful of 84 and also having at least 17 supplies at all times during the
# expedition, so we can safely simulate "Other Rivals". It also does not account for stat changes.
watchful = 257+10
persuasive = 201
use_buccaneering_approach = True


def calc_chance(difficulty: int, pers: bool = False) -> int:
    # calculate chance
    x = persuasive if pers else watchful
    chance = fl_difficultyScaler * x / difficulty

    # convert to "integer chance" and round down
    chance = floor(chance * 100)

    # check if chance is below 1% and set to 1% if it is
    chance = chance if chance >= 1 else 1

    # check if chance is above 100% and set to 100% if it is
    chance = chance if chance <= 100 else 100

    # convert back to "float chance"
    chance /= 100

    return chance


def cautious_approach():
    global usedSupplies, yourProgress, rivalsProgress, airs, nightmares, actions

    actions += 1
    usedSupplies += 1
    airs = new_airs()

    if success(cautious_approach_chance):
        yourProgress += 1
        # account for chance of rival progressing here being rather low, as per comment on the wiki page
        # (4 increases in 22 actions)
        if success(.2):
            rivalsProgress += 1
    else:
        nightmares += 1
        rivalsProgress += 1


def bold_approach():
    global usedSupplies, yourProgress, rivalsProgress, airs, nightmares, actions

    actions += 1
    usedSupplies += 2
    airs = new_airs()
    rivalsProgress += random.randint(0, 1)

    if success(bold_approach_chance):
        yourProgress += 2
    else:
        nightmares += 1


def buccaneering_approach():
    global usedSupplies, yourProgress, rivalsProgress, airs, nightmares, actions

    actions += 1
    usedSupplies += 3
    airs = new_airs()

    if success(buccaneering_approach_chance):
        yourProgress += 3
        rivalsProgress += random.randint(0, 1)
    else:
        nightmares += 2
        rivalsProgress += random.randint(1, 2)


def play_approach():
    global yourProgress, use_buccaneering_approach, neededProgress
    if yourProgress < neededProgress - 2:
        buccaneering_approach() if use_buccaneering_approach else bold_approach()
    elif yourProgress == neededProgress - 2:
        bold_approach()
    elif yourProgress == neededProgress - 1:
        cautious_approach()
    else:
        Exception("Something went wrong...")


def a_sign():
    global playedSigns, yourProgress, airs, actions
    if airs >= 96:
        actions += 1
        yourProgress += 4
        airs = new_airs()
        playedSigns += 1
        return True
    else:
        return False


def other_rivals():
    global crypticCluesUsed, usedSupplies, rivalsProgress, actions
    # assume the "Other Rivals" check always succeeds
    actions += 1
    crypticCluesUsed += 20
    usedSupplies += 10
    rivalsProgress = 1


def confront_rival(confronted_rival_already):
    global confrontedRival, rivalsProgress, yourProgress, usedSupplies, stranglingWillowAbsintheUsed,\
        confrontation_chance, nightmares, actions, inklingsOfIdentityGained, crypticCluesUsed
    if rivalsProgress >= 10:
        if confronted_rival_already:
            other_rivals()
            return True
        confrontedRival += 1
        actions += 1
        stranglingWillowAbsintheUsed += 10
        usedSupplies += 10
        nightmares += 5
        if success(confrontation_chance):
            yourProgress += random.randint(3, 5)
            rivalsProgress = 1
        else:
            rivalsProgress += 1
            inklingsOfIdentityGained += 1
            other_rivals()
        return True
    else:
        return False


def complete_expedition():
    global neededProgress, yourProgress, rivalsProgress, airs, echosGained, usedSupplies, actions, nightmares, \
        crypticCluesUsed, stranglingWillowAbsintheUsed
    if yourProgress >= neededProgress:
        airs = new_airs()
        rivalsProgress = 1
        yourProgress = 1
        actions += 1

        if success(completion_chance):
            echosGained += 125
        else:
            echosGained += 62.5

        # retroactively pay for supplies
        while usedSupplies > 0:
            actions += 2
            echosGained -= 13.5
            usedSupplies -= 5

        # relieve nightmares by "Allow them to watch over your rest"
        while nightmares > 5:
            nightmares -= 6
            actions += 1

        # pay for cryptic clues
        echosGained -= 0.04 * crypticCluesUsed
        crypticCluesUsed = 0
        return True
    else:
        return False


def do_expedition():
    # add 1 action for starting the expedition
    global actions
    actions += 1
    confronted_rival_already = False
    while True:
        if confront_rival(confronted_rival_already):
            confronted_rival_already = True
        elif complete_expedition():
            break
        elif a_sign():
            pass
        else:
            play_approach()


if __name__ == '__main__':
    simulations = 1000000

    from time import perf_counter_ns

    print("Completing {} simulations...".format(simulations))
    startTime = perf_counter_ns()

    cautious_approach_chance = calc_chance(cautiousApproachDifficulty)
    bold_approach_chance = calc_chance(boldApproachDifficulty)
    buccaneering_approach_chance = calc_chance(buccaneeringApproachDifficulty)
    completion_chance = calc_chance(completionDifficulty)
    confrontation_chance = calc_chance(confrontationDifficulty, True)

    for x in range(0, simulations):
        do_expedition()

    endTime = perf_counter_ns()
    elapsedTime = endTime - startTime
    print("Done after {0:.4f} seconds\n".format(elapsedTime / 1000000000))

    print("Total echos gained: {}".format(echosGained))
    print("Total actions used: {}".format(actions))
    print("EPA: {}\n".format(echosGained / actions))
    print("EPA after accounting for SWA: {}\n".format((echosGained - 0.5 * stranglingWillowAbsintheUsed) / actions))

    print("Total actions: {}".format(actions))
    print("Actions per Expedition: {}\n".format(actions / simulations))

    print("Total 'A Sign' played: {}".format(playedSigns))
    print("Signs per Expedition: {}\n".format(playedSigns / simulations))

    print("Confronted Rivals: {}".format(confrontedRival))
    print("Confronted Rivals per Expedition: {}\n".format(confrontedRival / simulations))

    print("'Strangling Willow Absinthe' used: {}".format(stranglingWillowAbsintheUsed))
    print("'Strangling Willow Absinthe' per Expedition: {}\n".format(stranglingWillowAbsintheUsed / simulations))

    print("'Inklings of Identity' gained: {}".format(inklingsOfIdentityGained))
    print("'Inklings of Identity' per Expedition: {}\n".format(inklingsOfIdentityGained / simulations))
