"""
Hypack LNW_Clip Removes excess lines from Hypack LNW.
Utility for removing lines from a Hypack LNW file. Takes as input an LNW for a channel that has lines spacing of 100 ft.
Outputs an LNW with spacing that varies depending on whether the channel is a straight section or a bend.
"""

def main():
    '''
    Step 1. load in LNW
    Step 2. choose a section to keep and then remove all lines before and after the specified section
    Step 3. remove all odd numbered lines
    step 4. detect which lines are on a bend
    Step 5. remove 200 and 800 numbered lines from straight sections, keep all even lines on the bend
    step 6. write the remaining lines to a new LNW file
    '''

    # Initialization variables
    WorkingDirectory = "/home/roger/Documents/Python/LNW_Clip/"
    lnw_file = "GI_02_HIB.lnw"
    lnw_out_file = lnw_file.split(',')
    print(f"lnw_out_file is {lnw_file}")
    lnw_path = WorkingDirectory + lnw_file

    lnw_out_path = WorkingDirectory + lnw_out_file[0] + "_out.lnw"
    print(f"line output path is {lnw_out_path}")
    start_line = "170+000"
    end_line = "190+000"


    # step 1
    lnw = load_lnw(lnw_path)
    #print_lnw(lnw)


    # step 2
    reach = extract_reach(lnw, start_line, end_line)
    # moved this function call toward the end. so it is
    # the last thing to do before writing to file
    total_lines = count_total_lines(reach)

    # step 3
    reach_bends = detect_bend(reach, total_lines)

    # step 4 remove odd lines
    reach_copy = (remove_odds(reach))

    #print(reach_bends)
    # need to
    total_lines = count_total_lines(reach_copy)
    # write the lines to a new LNW file
    write_lnw(reach_copy, total_lines, lnw_out_path)

def load_lnw(lnw_path):

    with open(lnw_path) as f:
        lnw = [x.rstrip() for x in f] # remove line breaks

    return lnw

def print_lnw(lnw):
    for line in lnw:
        print (line)

def extract_reach(lnw, start_line, end_line):
    # create local variables to build the text of the line as it occurs in the LNW file
    # this is done for botht he start line and the end line
    start_line = "LNN " + start_line
    end_line = "LNN " + end_line

    # subtract 3 from the start because the data for the Hypack line starts 3 spaces before the Hypack line number
    start_line_index = lnw.index(start_line) - 3
    # add 12 to the  because the data for the Hypack line starts 3 spaces before the Hypack line number
    end_line_index = lnw.index(end_line) + 13

    print(f"Start line index is {start_line_index}")
    print(f"end line index is {end_line_index}")

    # returns the reach
    reach = lnw[start_line_index: end_line_index]
    return reach

def count_total_lines(reach):
    # calculate the total number of lines
    total_lines = len(reach) / 16
    return total_lines


def detect_bend(reach, total_lines):
    # initialize the bearing variable for comparing
    previous_bearing = reach[11].split(" ")
    next_bearing = str(0)
    reach_bends = []
    count = 0
    bend_count = 0
    strait_count = 0

    for x in range(11, len(reach)-16, 16):
        count = count + 1
        #print(f"line count {count}")
        #print(f"x is {x}")
        bearing = reach[x].split(" ")
        #print(bearing[1])

        # Why is this getting an out of bounds error?
        if count +16 < len(reach):
            next_bearing = reach[x + 16].split(" ")
            #print (f"next bearing {next_bearing[1]}")

            if bearing[1] == next_bearing[1] and bearing[1] != previous_bearing[1]:
                strait_count = strait_count + 1
                #print(f"beginning of straight section!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: {strait_count}")
                #print("begin straight")

            elif bearing[1] == previous_bearing[1]:

                strait_count = strait_count + 1
                #print("straight")
                #print(f"count of straight section: {strait_count}")


            else:
                bend_count = bend_count + 1
                reach_bends.append(reach[x- 7])

                #print(f"count of bend: {bend_count}")
                #print("bend")
        else:
            exit

        previous_bearing = bearing
    print("found all bends")
    return reach_bends

def remove_odds(reach):
    # remove odd ending lines (100, 300, 500, 700, 900)
    reach_copy = reach
    odds = {'100', '300', '500', '700', '900'}
    for line in reach_copy:
        #if line[0:3] != "Lnn":


        if line[0:3] == "LNN":
            line_split = line.split("+")
            print (line_split[1])
            if line_split[1] in odds:
                print(f"Deleting odd line {str(line_split[0])}+{str(line_split[1])}")
                del reach_copy[(line.index(reach_copy)-3):(line.index(reach_copy) +12)]

    #print(reach_copy)

    return(reach_copy)

def remove_cs(reach, reach_bends):
    # only remove lines that end with 100, 200, 300, 500, 700 800, 900.
    # if lines are on a bend, remove odd lines (100, 300, 500, 700, 900).
    pass





def write_lnw(reach, total_lines, lnw_out_path):

    with open(lnw_out_path, "w") as out_f:
        # insert the LNS tag with total lines at the beginning of the reach list
        reach.insert(0, "LNS " + str(int(total_lines)))

        for line in reach:
            out_f.write(line + "\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


