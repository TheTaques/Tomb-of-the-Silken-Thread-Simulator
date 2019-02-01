from math import floor
import random


def new_airs():
    return random.randint(0, 127)


def success(chance):
    return random.random() < chance


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

# your stats
# this simulation assumes a minimum watchful of 84 and also having at least 17 supplies at all times during the
# expedition. it also does not account for stat changes.
watchful = 189
persuasive = 158


def calc_success_chances():
    global fl_difficultyScaler, cautiousApproachDifficulty, boldApproachDifficulty, buccaneeringApproachDifficulty, \
        watchful, cautious_approach_chance, bold_approach_chance, buccaneering_approach_chance, \
        completion_chance, persuasive, confrontation_chance

    # calculate chances
    cautious_approach_chance = fl_difficultyScaler * watchful / cautiousApproachDifficulty
    bold_approach_chance = fl_difficultyScaler * watchful / boldApproachDifficulty
    buccaneering_approach_chance = fl_difficultyScaler * watchful / buccaneeringApproachDifficulty
    completion_chance = fl_difficultyScaler * watchful / 60
    confrontation_chance = fl_difficultyScaler * persuasive / 72

    # convert to "integer chance" and round down
    cautious_approach_chance = floor(cautious_approach_chance * 100)
    bold_approach_chance = floor(bold_approach_chance * 100)
    buccaneering_approach_chance = floor(buccaneering_approach_chance * 100)
    completion_chance = floor(completion_chance * 100)
    confrontation_chance = floor(confrontation_chance * 100)

    # check if chance is below 1% and set to 1% if it is
    cautious_approach_chance = cautious_approach_chance if cautious_approach_chance >= 1 else 1
    bold_approach_chance = bold_approach_chance if bold_approach_chance >= 1 else 1
    buccaneering_approach_chance = buccaneering_approach_chance if buccaneering_approach_chance >= 1 else 1
    completion_chance = completion_chance if completion_chance >= 1 else 1
    confrontation_chance = confrontation_chance if confrontation_chance >= 1 else 1

    # check if chance is above 100% and set to 100% if it is
    cautious_approach_chance = cautious_approach_chance if cautious_approach_chance <= 100 else 100
    bold_approach_chance = bold_approach_chance if bold_approach_chance <= 100 else 100
    buccaneering_approach_chance = buccaneering_approach_chance if buccaneering_approach_chance <= 100 else 100
    completion_chance = completion_chance if completion_chance <= 100 else 100
    confrontation_chance = confrontation_chance if confrontation_chance <= 100 else 100

    # convert back to "float chance"
    cautious_approach_chance /= 100
    bold_approach_chance /= 100
    buccaneering_approach_chance /= 100
    completion_chance /= 100
    confrontation_chance /= 100


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
    global yourProgress
    if yourProgress < 28:
        bold_approach()
    elif yourProgress == 28:
        bold_approach()
    elif yourProgress == 29:
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


def confront_rival():
    global confrontedRival, rivalsProgress, yourProgress, usedSupplies, stranglingWillowAbsintheUsed,\
        confrontation_chance, nightmares, actions, inklingsOfIdentityGained, crypticCluesUsed
    if rivalsProgress >= 10:
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
            # we assume the "Other Rivals" part always succeeds
            crypticCluesUsed += 20
            usedSupplies += 10
            rivalsProgress = 1
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

    while True:
        if confront_rival():
            pass
        elif complete_expedition():
            break
        elif a_sign():
            pass
        else:
            play_approach()


if __name__ == '__main__':
    simulations = 100000

    calc_success_chances()

    from time import time_ns
    from datetime import timedelta

    print("Starting to do {} simulations...".format(simulations))
    startTime = time_ns()

    for x in range(0, simulations):
        do_expedition()

    endTime = time_ns()
    elapsedTime = endTime - startTime
    elapsedTime = timedelta(microseconds=elapsedTime / 1000)
    print("Done after {}\n".format(elapsedTime))

    print("Total echos gained: {}".format(echosGained))
    print("Total actions used: {}".format(actions))
    print("EPA: {}\n".format(echosGained / actions))

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
