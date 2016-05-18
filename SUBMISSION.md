# Baby Names

The below questions should be answered regarding your submission!

##### What data structure did you use to represent a name record? Why was that the correct choice? #####
> I used Named Tuple = (Name,sex,year{}). Year is dictionary whose keys are years and values are counts and ranks.This structure was the correct choice since it contains all the essential data and is also easy to retrieve the records by name-sex combo for each year,for plotting data. 


##### Fill in the below table to record the amount of _clock time_ it took your computer to "transform" the loaded raw data using each of the three techniques for the given maximum rank (see assignment for details). Cells with an `X` can be left blank; you don't need to test those situations. Note that your times may different from others'  depending on the speed of your machine, etc.#####

| Max Rank:        | 250 | 500 | 1000 | 2000 | All |
|------------------|-----|-----|------|------|-----|
| Linear Search    | 20  |  100| 300  |   X  |  X  |
| Binary Search    | 20  |  70 |  120 | 300  |  X  |
| Hashmap (`dict`) | 15  |  30 |  90  |  250 | 400 |


##### Briefly explain the above results. #####
> The method of using dictionaries for holding the records significantly reduced the time needed to transform. It was also easier to search. 


##### Did you receive help from any other sources (classmates, etc)? If so, please list who (be specific!). #####
> No


##### Approximately how many hours did it take you to complete this assignment? #####
> 2 days


##### On a scale of 1 (too easy) to 10 (too challenging), how difficult was this assignment? #####
> 9


##### Did you encounter any problems in this assignment we should warn students about in the future? How can we make the assignment better? #####
> No
