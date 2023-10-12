#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programming
Final assignment: Bagagekluizen
(c) 2023 Hogeschool Utrecht,
Constantijn van Hartesveldt (constantijn@vanhartesveldt.nl)
you will proberly need more files which you can get here: https://github.com/cvanh/fa_prog
"""

import builtins
import collections
import sys
import traceback
import pandas as pd

# the helper functions
# from utils.find_unused_lockers import find_unused_lockers
# from utils.check_pincode import check_pincode
# from utils.csv import read_csv , write_csv


# the amount of lockers that are allowed to exist
max_lockers = 12

def read_csv() -> pd.DataFrame:
    csv_headers =  ["id", "keycode"]
    csv = pd.read_csv("./fa_testkluizen.txt", names=csv_headers, sep=";") 
    
    # soms is keycode aleen maar een getal en pandas zet dit dan automatish om in een int maar we willen een string voor de comperisons 
    csv["keycode"] =  csv["keycode"].astype(str)

    return csv

def write_csv(csv: pd.DataFrame) -> None:
    csv.to_csv("./fa_testkluizen.txt", sep=";",index=False,header=False)


def find_unused_lockers(max_lockers = 12):
    """finds the missing intergers whithin an array

    Args: 
        arr (array): the array where the missing intergers should be found
        size: (int): the biggest interger that should exist 
    """
    csv = read_csv() 

    used_lockers = csv["id"].to_numpy()
    
    used_lockers.sort()

    unused = []

    for item in range(max_lockers + 1) :
        # we want to skip 0 because we want locker 1-12
        if item == 0:
            continue

        if item not in used_lockers:
            unused.append(item)
    return unused


def aantal_kluizen_vrij():
    """
    Bepaal hoeveel kluizen er nog vrij zijn. Er zijn in totaal 12 kluizen,
    dus 12 min het aantal kluizen dat in het bestand staat, moet de uitkomst
    van deze functie zijn.

    Returns:
        int: Het aantal vrije kluizen.
    """

    # find the lockers that arent used
    unused_lockers = find_unused_lockers()

    # because len counts from 1 and not 0 we need to subtract 1 
    amount_unused_lockers = (len(unused_lockers))

    return int(amount_unused_lockers)


def nieuwe_kluis():
    """
    Indien er nog kluizen vrij zijn, moet de gebruiker de mogelijkheid krijgen
    om een kluiscode in te voeren. Deze kluiscode moet uit minimaal 4 tekens bestaan,
    en de puntkomma (';') mag er niet in voorkomen.

    Als de kluiscode ongeldig is, is de returnwaarde van deze functie -1.
    Als er geen vrije kluizen meer zijn, is de returnwaarde van deze functie -2.

    Als er nog vrij kluizen zijn, en de kluiscode is geldig, dan koppelt deze functie
    de kluiscode aan een nog beschikbare kluis, en schrijft deze combinatie weg naar
    een tekstbestand. De returnwaarde van de functie is dan gelijk aan het toegekende
    kluisnummer.

    Returns:
        int: het toegekende kluisnummer of foutcode -1 of -2
    """
    free_lockers = find_unused_lockers() 

    # check if there are unused lockers
    if len(free_lockers) == 0:
        return -2

    pincode = input("locker code?: ")

    # validate if ; is in the pincode or the pincode is shorter than 4
    if(";" in pincode or len(pincode) < 4):
        return -1

    csv = read_csv()

     # check if there is space left for new lockers 
    if len(csv) == 12:
        return -2

   # create new locker entry 
    new_locker = pd.DataFrame({
        # take the first free locker and use that one
        "id": [free_lockers[-0]],
        "keycode": [pincode]
    })

    # add the locker to the existing lockers
    csv = pd.concat([new_locker,csv])

    write_csv(csv)

    return free_lockers[-0] 


def kluis_openen():
    """
    Laat de gebruiker een kluisnummer invoeren, en direct daarna de bijbehorende
    kluiscode. Indien deze combinatie voorkomt in het tekstbestand met de kluizen
    die in gebruik zijn, is het resultaat van de functie True, anders False.

    Returns:
        bool: True als de ingevoerde combinatie correct is, anders False
    """
    locker_id = int(input("locker id?"))
    locker_keycode = input("locker keycode")

    csv = read_csv()

    # find locker that the user wants
    locker_by_id = csv.loc[csv["id"] == locker_id]
    # check if the password matches with the stored password
    user_locker = locker_by_id.loc[locker_by_id["keycode"] == locker_keycode]

    # format to the format school wants 
    locker = not user_locker.empty

    return locker


def kluis_teruggeven():
    """
    Laat de gebruiker een kluisnummer invoeren, en direct daarna de bijbehorende
    kluiscode. Indien deze combinatie voorkomt in het tekstbestand met de kluizen
    die in gebruik zijn, moet deze combinatie/regel uit het tekstbestand verwijderd
    worden.

    Als het lukt om de combinatie te vinden en te verwijderen, is het resultaat
    van de functie True, anders False.

    Returns:
        bool: True als er een kluiscombinatie verwijderd werd, anders False
    """
    locker_id = int(input("locker id?"))
    locker_keycode = input("locker keycode")

    csv = read_csv()

    if len(csv) == 0:
        return False

    # check if user is allowed to remove the row and the row exists
    matched_lockers = csv.query("@locker_id == id").query("@locker_keycode == keycode") 

    # if matched lockers is empty that means that the user has entered the wrong pincode or locker id
    if matched_lockers.empty:
        return False

    row_exists = not matched_lockers.empty 

    if row_exists:
        # drop axis 1/row by id
        csv = csv.drop(csv[csv.id == locker_id].index) 
        write_csv(csv)

    return row_exists


def development_code():
    prompt = """
    select something you want to do and type its number and press enter

    1 Ik wil weten hoeveel kluizen nog vrij zijn
    2 Ik wil een nieuwe kluis
    3 Ik wil een kluis openen
    4 Ik geef mijn kluis terug 
    """
    inst = int(input(prompt))

    match inst:
        case 1:
            aantal_kluizen_vrij()
        case 2:
            nieuwe_kluis()
        case 3:
            kluis_openen()
        case 4:
            kluis_teruggeven()
        case other:
            print("no valid input given")
            exit()


def module_runner():
    # development_code()  # Comment deze regel om je 'development_code' uit te schakelen
    __run_tests()       # Comment deze regel om de HU-tests uit te schakelen


"""
==========================[ HU TESTRAAMWERK ]================================
Hieronder staan de tests voor je code -- daaraan mag je niets wijzigen!
"""


def __my_assert_args(function, args, expected_output, check_type=False):
    """
    Controleer of gegeven functie met gegeven argumenten het verwachte resultaat oplevert.
    Optioneel wordt ook het return-type gecontroleerd.
    """
    argstr = str(args).replace(',)', ')')
    output = function(*args)

    # Controleer eerst het return-type (optioneel)
    if check_type:
        msg = f"Fout: {function.__name__}{argstr} geeft geen {type(expected_output).__name__} terug als return-type"
        assert type(output) is type(expected_output), msg

    # Controleer of de functie-uitvoer overeenkomt met de gewenste uitvoer
    if str(expected_output) == str(output):
        msg = f"Fout: {function.__name__}{argstr} geeft {output} ({type(output).__name__}) " \
              f"in plaats van {expected_output} (type {type(expected_output).__name__})"
    else:
        msg = f"Fout: {function.__name__}{argstr} geeft {output} in plaats van {expected_output}"

    if type(expected_output) is float and isinstance(output, (int, float, complex)):
        # Vergelijk bij float als return-type op 7 decimalen om afrondingsfouten te omzeilen
        assert round(output - expected_output, 7) == 0, msg
    else:
        assert output == expected_output, msg


def __out_of_input_error():
    raise AssertionError(
        "Fout: er werd in de functie vaker om input gevraagd dan verwacht.")


def __my_test_file():
    return "fa_testkluizen.txt"


def __check_line_in_testfile(line, testfile=__my_test_file()):
    with open(testfile, 'r') as dummy_file:
        for file_line in dummy_file.readlines():
            if line.strip() == file_line.strip():
                return True

    return False


def __create_test_file(safes, testfile=__my_test_file()):
    kluis_mv_ev = 'kluis' if len(safes) == 1 else 'kluizen'
    print(
        f"Voor testdoeleinden wordt bestand {testfile} aangemaakt met {len(safes)} {kluis_mv_ev}... ", end="")

    try:
        with open(testfile, 'w') as dummy_file:
            for number, code in safes:
                dummy_file.write(f"{number};{code}\n")
    except:
        print(
            f"\nFout: bestand {testfile} kon niet worden aangemaakt. Python-error:")
        print(traceback.format_exc())
        sys.exit()

    print("Klaar.")


def __create_fake_open(original_open):
    def fake_open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        return original_open(__my_test_file(), mode=mode, buffering=buffering, encoding=encoding, errors=errors,
                             newline=newline, closefd=closefd, opener=opener)
    return fake_open


def test_aantal_kluizen_vrij():
    function = aantal_kluizen_vrij

    case = collections.namedtuple('case', 'safes')
    testcases = [case(((11, "6754"),)),
                 case(((11, "6754"), (1, "geheim"), (12, "z@terd@g"))),
                 case(((1, "0000"), (3, "0000"), (5, "0000"), (7, "0000"), (9, "0000"), (11, "0000"),
                       (2, "0000"), (4, "0000"), (6, "0000"), (8, "0000"), (10, "0000"), (12, "0000")))]

    for test in testcases:
        __create_test_file(test.safes)

        original_open = builtins.open
        builtins.open = __create_fake_open(original_open)

        try:
            expected_output = 12 - len(test.safes)
            __my_assert_args(function, (), expected_output )
            __my_assert_args(function, (), expected_output, check_type=True)
        finally:
            builtins.open = original_open


def test_nieuwe_kluis():
    function = nieuwe_kluis

    case = collections.namedtuple(
        'case', 'safes simulated_input possible_outputs')
    testcases = [case(((11, "6754"), (12, "z@terd@g")), ["geheim"], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                 case(((1, "0000"), (3, "0000"), (5, "0000"), (7, "0000"), (9, "0000"), (11, "0000"),
                       (2, "0000"), (4, "0000"), (6, "0000"), (8, "0000"), (10, "0000"), (12, "0000")), ["geheim"], [-2]),
                 case(((1, "0000"), (3, "0000"), (5, "0000"), (7, "0000"), (9, "0000"), (11, "0000"),
                       (2, "0000"), (4, "0000"), (6, "0000"), (8, "0000"), (12, "0000")), ["geheim"], [10]),
                 case(((1, "0000"), (3, "0000"), (5, "0000"), (8, "0000"), (10, "0000"), (12, "0000"),
                       (2, "0000"), (4, "0000"), (6, "0000"), (9, "0000"), (11, "0000")), ["geheim"], [7]),
                 case(((2, "0000"), (4, "0000"), (6, "0000"), (8, "0000"), (10, "0000"), (12, "0000"),
                       (3, "0000"), (5, "0000"), (7, "0000"), (9, "0000"), (11, "0000")), ["geheim"], [1]),
                 case(((1, "0000"), (3, "0000")), ["abc"], [-1]),
                 case(((1, "0000"), (3, "0000")), ["geheim;"], [-1])]

    for test in testcases:
        __create_test_file(test.safes)

        original_open = builtins.open
        builtins.open = __create_fake_open(original_open)

        original_input = builtins.input
        simulated_input = test.simulated_input.copy()
        simulated_input.reverse()
        builtins.input = lambda prompt="": simulated_input.pop() if len(
            simulated_input) > 0 else __out_of_input_error()

        try:
            output = function()

            assert isinstance(
                output, int), f"Fout: {function.__name__}() geeft {type(output).__name__} in plaats van int. Check evt. {__my_test_file()}"
            assert output in test.possible_outputs, f"Fout: {function.__name__}() geeft {output}, maar mogelijke outputs zijn alleen: {test.possible_outputs}"

            # if all possible safenumbers are positive, a new safenumber should be registered by now
            if all(possible_safe_number > 0 for possible_safe_number in test.possible_outputs):
                free_safes = aantal_kluizen_vrij()
                expected_free_safes = 12 - (len(test.safes) + 1)

                msg = f"Fout: {function.__name__}() geeft aan dat een nieuwe kluis (nummer {output}) gereserveerd is, maar " \
                      f"daarna geeft aantal_kluizen_vrij() {free_safes} ipv {expected_free_safes}. Check evt. {__my_test_file()}"

                assert free_safes == expected_free_safes, msg

            if output >= 0:
                msg = f"Fout: {function.__name__}() geeft aan dat kluis {output} gereserveerd is (ww: '{test.simulated_input[-1]}'), " \
                      f"maar {__my_test_file()} bevat daarna geen regel met \"{output};{test.simulated_input[-1]}\"."

                assert __check_line_in_testfile(
                    f"{output};{test.simulated_input[-1]}"), msg

        except AssertionError as ae:
            raise AssertionError(
                f"{ae.args[0]}\n -> Info: gesimuleerde input voor deze test: {test.simulated_input}.") from ae
        finally:
            builtins.input = original_input
            builtins.open = original_open


def test_kluis_openen():
    function = kluis_openen

    case = collections.namedtuple(
        'case', 'safes simulated_input expected_output')
    testcases = [case(((11, "6754"), (12, "z@terd@g")), ["11", "1234"], False),
                 case(((11, "6754"), (12, "z@terd@g")), ["11", "6754"], True),
                 case(((11, "6754"), (12, "z@terd@g")),
                      ["12", "z@terd@g"], True),
                 case(((11, "6754"), (12, "z@terd@g")), ["10", "6754"], False),
                 case(((11, "geheim"),), ["1", "geheim"], False),
                 case(((12, "geheim"),), ["2", "geheim"], False),
                 case(((1, "1235"), (2, "6543"), (3, "7856")), ["1", "6543"], False)]

    for test in testcases:
        __create_test_file(test.safes)

        original_open = builtins.open
        builtins.open = __create_fake_open(original_open)

        original_input = builtins.input
        simulated_input = test.simulated_input.copy()
        simulated_input.reverse()
        builtins.input = lambda prompt="": simulated_input.pop() if len(
            simulated_input) > 0 else __out_of_input_error()

        try:
            __my_assert_args(
                function, (), test.expected_output, check_type=True)
        except AssertionError as ae:
            raise AssertionError(
                f"{ae.args[0]}\n -> Info: gesimuleerde input voor deze test: {test.simulated_input}.") from ae
        finally:
            builtins.input = original_input
            builtins.open = original_open


def test_kluis_teruggeven():
    function = kluis_teruggeven

    case = collections.namedtuple(
        'case', 'safes simulated_input expected_output')
    testcases = [case(((11, "6754"), (12, "z@terd@g")), ["11", "1234"], False),
                 case((), ["1", "geheim"], False),
                 case(((11, "6754"), (12, "z@terd@g")),
                      ["12", "z@terd@g"], True),
                 case(((11, "6754"), (12, "z@terd@g")), ["11", "6754"], True),
                 case(((11, "6754"),), ["11", "6754"], True),
                 case(((11, "geheim"),), ["1", "geheim"], False),
                 case(((12, "geheim"),), ["2", "geheim"], False),
                 case(((1, "1235"), (2, "6543"), (3, "7856")), ["1", "6543"], False)]

    for test in testcases:
        __create_test_file(test.safes)

        original_open = builtins.open
        builtins.open = __create_fake_open(original_open)

        original_input = builtins.input
        simulated_input = test.simulated_input.copy()
        simulated_input.reverse()
        builtins.input = lambda prompt="": simulated_input.pop() if len(
            simulated_input) > 0 else __out_of_input_error()

        try:
            __my_assert_args(
                function, (), test.expected_output, check_type=True)

            if test.expected_output:  # safe should be available again
                free_safes = aantal_kluizen_vrij()
                expected_free_safes = 12 - (len(test.safes) - 1)

                msg = f"Fout: {function.__name__}() geeft aan dat kluis (nummer {test.simulated_input[0]}) vrijgegeven is, maar " \
                      f"daarna geeft aantal_kluizen_vrij() {free_safes} ipv {expected_free_safes}."

                assert free_safes == expected_free_safes, msg

        except AssertionError as ae:
            raise AssertionError(
                f"{ae.args[0]}\n -> Info: gesimuleerde input voor deze test: {test.simulated_input}.") from ae
        finally:
            builtins.input = original_input
            builtins.open = original_open


def __run_tests():
    """ Test alle functies. """
    test_functions = [test_aantal_kluizen_vrij,
                      test_nieuwe_kluis,
                      test_kluis_openen,
                      # Uncomment de regel hieronder om ook de optionele functie kluis_teruggeven te testen:
                      test_kluis_teruggeven
                      ]

    try:
        for test_function in test_functions:
            func_name = test_function.__name__[5:]

            print(
                f"\n======= Test output '{test_function.__name__}()' =======")
            test_function()
            print(f"Je functie {func_name} werkt goed!")

        print("\nGefeliciteerd, alles lijkt te werken!")
        print("Lever je werk nu in op Canvas...")

    except AssertionError as e:
        print(e.args[0])
    except Exception as e:
        print(f"Fout: er ging er iets mis! Python-error: \"{e}\"")
        print(traceback.format_exc())


if __name__ == '__main__':
    module_runner()
