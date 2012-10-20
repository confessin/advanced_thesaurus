advanced_thesaurus
==================

An Advanced thesaurus which gets words meaning 1 level down.

This will take up a list of keywords as argument and return a list of all keywords which can be built using thesaurus.

For example: 

    Normal Synonyms for word "car"
    auto, automobile, bucket, buggy, bus, clunker, compact, convertible, conveyance, coupe, gas guzzler, hardtop, hatchback, heap*, jalopy, jeep, junker, limousine, machine, motor, motorcar, pickup, ride*, roadster, sedan, station wagon, subcompact, touring car, truck, van, wagon, wheels, wreck* 

    Advanced Synonyms
    cars , auto, automobile, cable car, car, elevator car, gondola, machine, motorcar, railcar, railroad car, railway car, Model T, S.U.V., SUV, Stanley Steamer, ambulance, baggage car, beach waggon, beach wagon, bus, cab, cabin car, caboose, carriage, club car, coach, compact, compact car, convertible, coupe, cruiser, electric, electric automobile, electric car, estate car, freight car, gas guzzler, guard's van, hack, handcar, hardtop, hatchback, heap, horseless carriage, hot rod, hot-rod, jalopy, jeep, landrover, limo, limousine, loaner, lounge car, luggage van, mail car, minicar, minivan, pace car, passenger car, patrol car, phaeton, police car, police cruiser, prowl car, race car, racer, racing car, roadster, runabout, saloon, secondhand car, sedan, slip carriage, slip coach, sport car, sport utility, sport utility vehicle, sports car, squad car, station waggon, station wagon, stock car, subcompact, subcompact car, taxi, taxicab, tender, tourer, touring car, two-seater, used-car, van, waggon, wagon


Example Usage
==================

Get Thesaurus words for a set source of words.
    Example Usage: python core/thes_wordnet.py iron_man -n human -n officer --exclude-hyponyms
    
This would get all synonyms of iron man and permute over it. It will also exclude the human and officer context.


Requisites:
nltk
wordnet corpus of nltk
Python 2.7
