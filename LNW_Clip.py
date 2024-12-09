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
    lnw_out_file = lnw_file.split('.')
    print(f"lnw_out_file is {lnw_file}")
    lnw_path = WorkingDirectory + lnw_file

    lnw_out_path = WorkingDirectory + lnw_out_file[0] + "_out.lnw"
    print(f"line output path is {lnw_out_path}")
    start_line = "162+000"
    end_line = "320+000"


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
    # print statement for testing
    print(reach_bends)

    # step 4 remove odd lines
    #reach_copy = (remove_odds(reach))
    reach = remove_odds(reach)
    # print statement for testing
    # print(reach)
    reach = remove_cs(reach, reach_bends)

    total_lines = count_total_lines(reach)
    # write the lines to a new LNW file
    write_lnw(reach, total_lines, lnw_out_path)
    #write_lnw(reach_bends, total_lines, lnw_out_path)

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
        print(bearing[1])

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
                reach_bends.append(reach[x-8])
                #reach_bends.append(bearing)
                #reach_bends.append(bearing[0]+bearing[1]+bearing[2])
                #reach_bends.append(reach[x-8])

                #print(f"count of bend: {bend_count}")
                #print(f"bend {bearing}")
        else:
            exit

        previous_bearing = bearing
    print("found all bends")
    print(reach_bends)
    return(reach_bends)

def remove_odds(reach):
    # remove odd ending lines (100, 300, 500, 700, 900)
    #reach_copy = reach
    odds = {'100', '300', '500', '700', '900'}

    for index, line in enumerate(reach):

        if line[0:3] == "LNN":
            line_split = line.split("+")
            # print statement for testing
            #print (line_split[1])

            if line_split[1] in odds:
                print(f"Deleting odd line {str(line_split[0])}+{str(line_split[1])}")
                del reach[index -3: index +13]

    #print statement for testing
    #print(reach_copy)

    return(reach)

def remove_cs(reach, reach_bends):
    # Removes the extra lines in straight sections that are not needed for conditional surveys.
    # This is to be run after the function to remove_odds(reach).
    # Removes lines that end in 200 or 800.

    cs_not = {'200', '800'}

    for index, line in enumerate(reach):

        if line[0:3] == "LNN":
            line_split = line.split("+")
            # print statement for testing
            # print (line_split[1])

            if line not in reach_bends and line_split[1] in cs_not:
                print(f"Deleting line {str(line_split[0])}+{str(line_split[1])}")
                del reach[index - 3: index + 13]
                #if line_split[1] in cs_not:
                #    print(f"Deleting line {str(line_split[0])}+{str(line_split[1])}")
                #    del reach[index - 3: index + 13]

    return(reach)

def write_lnw(reach, total_lines, lnw_out_path):

    with open(lnw_out_path, "w") as out_f:
        # insert the LNS tag with total lines at the beginning of the reach list
        reach.insert(0, "LNS " + str(int(total_lines)))

        for line in reach:
            out_f.write(line + "\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


