import sys
import re
import webCrawler
import queryEngine
import pickle
import os


def menu(build_complete):
    options = ["-build", "-restore", "-exit"]
    print ("___  ___")
    print ("|  \/  |")
    print ("| .  . | ___ _ __  _   _")
    print ("| |\/| |/ _ \ '_ \| | | |")
    print ("| |  | |  __/ | | | |_| |")
    print ("\_|  |_/\___|_| |_|\__,_|")
    print("\n")
    print ("-build   (Create the Poodle database)")
    print ("-restore (Retrieve last Poodle session)")
    print ("-exit    (Exit from Poodle)")

    if build_complete:
        options.extend(["-dump", "-search", "-print"])
        print ("-dump    (Save the Poodle database)")
        print ("-search  (Search crawled pages)")
        print ("-print   (Show index, graph and ranks files)")

    return options


def dump(index, ranks, graph):
    # Creating the dictionary with data already retrieved
    dump_data = {}
    dump_data['graph'] = graph
    dump_data['pageRanks'] = ranks
    dump_data['index'] = index

    # Creating dump text file
    fout = open("dumpData.txt", "w")
    pickle.dump(dump_data, fout)
    fout.close()

    print ("Data has been saved")


def restore():
    if os.path.exists("dumpData.txt"):
        fin = open("dumpData.txt", "r")
        dump_data = pickle.load(fin)
        fin.close()
    else:
        return False

    return dump_data


def print_all(graph, index, ranks):
    print(" _____                 _")
    print("|  __ \               | |")
    print("| |  \/_ __ __ _ _ __ | |__ ")
    print("| | __| '__/ _` | '_ \| '_ \ ")
    print("| |_\ \ | | (_| | |_) | | | |")
    print(" \____/_|  \__,_| .__/|_| |_|")
    print("                | |          ")
    print("                |_|          ")
    print("\n")
    print graph

    print(" _           _           ")
    print("(_)         | |          ")
    print(" _ _ __   __| | _____  __")
    print("| | '_ \ / _` |/ _ \ \/ /")
    print("| | | | | (_| |  __/>  <")
    print("|_|_| |_|\__,_|\___/_/\_\"")
    print("\n")
    print index

    print("______            _")
    print("| ___ \          | | ")
    print("| |_/ /__ _ _ __ | | _____")
    print("|    // _` | '_ \| |/ / __|")
    print("| |\ \ (_| | | | |   <\__ \"")
    print("\_| \_\__,_|_| |_|_|\_\___/")
    print("\n")
    print ranks


def exit_menu():
    sys.exit()


# Should only be completed after build is done
def search(index, rank, build_complete):
    # Checking that the user has entered input
    print(" _____                     _ ")
    print("/  ___|                   | |   ")
    print("\ `--.  ___  __ _ _ __ ___| |__")
    print(" `--. \/ _ \/ _` | '__/ __| '_ \ ")
    print("/\__/ /  __/ (_| | | | (__| | | |")
    print("\____/ \___|\__,_|_|  \___|_| |_|")

    while True:
        user_query = raw_input("\nPlease enter a search term ('-menu' to exit) >>")
        if len(user_query) > 0:
            if user_query == '-menu':
                break
            else:
                user_query_list = re.findall(r"[\w']+", user_query.lower())
                queryEngine.search(user_query_list, rank, index)

        else:
            print "\nNothing was entered"


def build():
    index, ranks, graph = webCrawler.crawler()

    return index, ranks, graph


def get_user_input(build_complete):
    while True:
        options_menu = menu(build_complete)
        user_input = raw_input("\nWhat would you like to do (-exit to exit)")

        # Removing white space
        user_input = user_input.strip(" ")

        if user_input in options_menu:
            break
        else:
            print "\nInvalid option\n"

    return user_input


def main():
    build_complete = False
    while True:
        user_input = get_user_input(build_complete)
        if user_input == "-build":
            index, ranks, graph = build()
            build_complete = True

        elif user_input == "-search" and build_complete:
            search(index, ranks, build_complete)

        elif user_input == "-dump" and build_complete:
            dump(index, ranks, graph)

        elif user_input == "-restore":
            dump_data = restore()

            if dump_data == False:
                print ("No data has been previously saved.")

            else:
                index = dump_data['index']
                ranks = dump_data['pageRanks']
                graph = dump_data['graph']
                build_complete = True

        elif user_input == "-print" and build_complete:
            print_all(graph, index, ranks)

        elif user_input == "-exit":
            exit_menu()


if __name__ == '__main__':
    main()
