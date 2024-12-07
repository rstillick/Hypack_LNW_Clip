A utility for removing lines from a Hypack LNW file. 

Input
Takes as input an LNW for a channel that has lines spacing of 100 ft.  

Parameters
1. Specify the range of lines you need to keep for the survey reach.
2. Line spacing
	- Conditional survey (default), 000, 400, 600, plus oddballs,transition lines; 200 ft spacing on bends.
	- Evens and oddballs. 

Output
Outputs an LNW with spacing that varies depending on whether the channel is a straight section or a bend.