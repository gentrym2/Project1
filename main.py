"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Mackenna Gentry"
__email__ = "gentrym2@myerau.edu"
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare


def search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Basic search strategy goes like this:
    - until the provided list is empty.
    - remove the 1st item from the provided file_list
    - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
    - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
    As a result we have a list, each item of that list is a list,
    each of those lists contains files that have the same content
    """
    lol = []
    while 0 < len(file_list):
        duplicates = list(filter(lambda x: compare(file_list[0], x), file_list))
        if 1 < len(duplicates):
            lol.append(duplicates)
        file_list = list(filter(lambda x: not compare(file_list[0], x), file_list))
    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """
    # remove items with unique file size(getsize) from file_list
    file_sizes = list(map(getsize, file_list))
    filtered_file_sizes = list(filter(lambda x: 1 < file_sizes.count(x), file_sizes))
    return search(file_list)


def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    if 0 < len(lol):
        print("== == Duplicate File Finder Report == ==")
        ll = max(lol, key=len)
        ll.sort()
        print(f'The file with the most duplicates is: {ll[0]}')
        print(f'Here are its {len(ll)-1} copies:')
        for i in range(1, len(ll)):
            print(ll[i])
        ll = max(lol, key=lambda x: len(x) * getsize(x[0]))
        ll.sort()
        print(f'The most disk space {(len(ll)-1) * getsize(ll[0])} could be recovered, by deleting copies of this file: {ll[0]}')
        print(f'Here are its {len(ll) - 1} copies:')
        for i in range(1, len(ll)):
            print(ll[i])
    else:
        print("No duplicates found")


if __name__ == '__main__':
    path = join(".", "images")

    # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path))) # 1st step: calling all_files, 2nd step calling search
    print(f"Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now w/ a faster search implementation:")

    # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")
