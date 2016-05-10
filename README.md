# Baby Names
Working with large amounts of information can require careful consideration of your choice of data structures and algorithms, to make sure you can process the data in a reasonable amount of time. For this assignment, you will work through an extended example of how the code you write can influence how much time you have to wait for your analysis results.

The data set you will be working with comes from the US Social Security Administration (SSA), which provides annual information about the popularity of particular names for babies. The SSA's [website](http://www.ssa.gov/OACT/babynames/) allows you to look up the popularity of a particular name, while also providing historical data for analysis. You will be developing a small script that generates a simple chart of a name's popularity over time, though the majority of your work will focus on loading and structuring the data.

Along the way, you'll practice using separate git **branches** to develop different iterations and improvements of your program. This will help you to save and compare different program approaches--even if those versions were developed by different people!


### Objectives
By completing this challenge you will practice and master the following skills:

* Continue loading and parsing real-world data
* Continue working with Python data structures (lists, dicts, tuples, etc.)
* Transforming data into alternative data structures
* Measuring and comparing the speed of different algorithms and data structures
* Using git branches and tags


## Setup
As you will do for all assignments in this course, you should start by forking and cloning this repository to your local machine. Repositories will contain starter code (if any), as well as the `SUBMISSION.md` file you will need to complete.

For this assignment, the repo includes a piece of a program `name_plotter.py` which you will need to complete. This code contains the majority of a function `plot_names()` which will generate a Plotly line plot for a given list of names. You will need to fill in the piece that actually plots the data, but all of the chart setup is provided for you.

The `name_plotter.py` program also includes a section at the bottom for you to call your functions and test your code (there is no provided command-line interface this time). Any code inside the `if __name__ == '__main__': `block will only be run when you run the script file from the command-line (e.g., `python3 name_plotter.py path/to/name/data/folder Joel Ada`; the first argument is the path to the folder of data you want to process, and the remaining arguments would be names you wanted to plot).

- Note that this structure means you can also import your script as a module into the interactive python shell, calling functions interactively. For example:

    ```
    $ python3
    Python 3.5.1 (default, Dec  6 2015, 01:38:48) 
    >>> from name_voyager import *
    >>> data = load_names_data('folder')
    >>> names_to_plot = ['Joel','Ada']
    >>> plot_names(data, names_to_plot)
    ```

### Getting the Data
Once again, you'll be using unaltered "real-world" data to test your program with. You will need to [download the data set](https://www.ssa.gov/oact/babynames/names.zip) from the SSA's website at [https://www.ssa.gov/oact/babynames/limits.html](https://www.ssa.gov/oact/babynames/limits.html) (you're downloading the "National data"; we're not interested in a state-based breakdown). This is an **8mb** zip file, containing baby naming data for the years 1880 through 2015. It includes pretty much every baby name given in the United States over the past 135 years.

- You will need to unzip the contents of the file for processing (you can do this using Python, but it's easier/faster to unpack it manually).

- Please, **do not** add this directory to your git repository! In fact, you should add it to the `.gitignore` file so you don't accidentally commit and push it (which will make it really slow for us to download and grade).

The data can be found in multiple text files, each named in a format like `yob2015.txt`---the number in the filename represents the year of birth. Each file contains a list of baby names **ordered by popularity**---that is, the first name in the file is the most popular female name, the second name is the second most popular female name, etc. Female names are listed before male names, so the first male name listed in the file would be the most popular male name, etc.

Each name entry is a comma separated list that looks like has the following format:

```
Joel,M,2697
```

The first item is the name, the second is the sex (`M` for male and `F` for female), and the third is the total number of people born with that name in that year. Keep in mind we are interested in _both_ the total number of people with that name _and_ what rank that name is at (e.g., where the name falls in the file).

- Because of the content domain, this write-up will use the words "sex", "male", and "female" to refer to (reported) sex assigned at birth, acknowledging that this value may be distinct from a person's [gender identity or expression](http://www.transstudent.org/gender).

Note that the data just includes literally what people put on their SSA registration forms, so there are things like "A" and "Baby" recorded as names (the data is more cleaned up in the later years). We will not worry about that, and we will not combine names that are similar in some sense---"Cathy" and "Catherine" and "Kathryn" and "Katie" and "Kati" will all count as different names.


## Step 1: Loading the Data
Your first step will be to simply load the data into your computer's memory. Define a function (e.g.,**`load_names_data()`**) that takes as a parameter the location of the folder containing the name data (the `yob*.txt` files). It should also take a second ___optional___ parameter indicating the "maximum rank" of data to include (default to "all ranks"). This function should parse each of those files and return a single **`dictionary`** with all their contents (that is, _all_ the baby name data).

Note this dictionary should be structured in a **very specific way** so that the rest of the assignment follows properly. Each ___key___ in dictionary should be a particular year (as an integer). The ___value___ of each key should be a a **`list` of `tuples`**, where each tuple contains the name, the sex, the number of babies (count), and the rank of the name. So your dictionary should look something like:

```
{
    ...
    2015: [
        ('Emma', 'F', 20355, 1), 
        ('Olivia', 'F', 19553, 2), 
        ('Sophia', 'F', 17327, 3), 
        ...
        ('Zayne', 'M', 579, 498), 
        ('Bodhi', 'M', 578, 499), 
        ('Arjun', 'M', 574, 500),
        ...
    ]    
}
#the above data can be seen with 
#   print( data[2015][:3] + data[2015][-3:] )
#with a max ranks of 500.
```

- In effect, this function is just giving you the "raw" data without any real structuring, where each line in a file is going to be an item in a list for that year; and all the years are stored in a single dictionary. 

You can get a list of files in a folder using the [`os.listdir()`](https://docs.python.org/3/library/os.html#os.listdir). Function. Be careful to only process the `yob*.txt` files, and not anything else that might be in the directory.

As you iterate through each file, you'll need to keep track of which "rank" the particular line is at. A counter variable is a good way to do this---start at 1, and increase it for each line you process. You'll need to keep track of female and male names separately, or reset the counter when you get to the other sex (all female names are listed before all male names).

Remember to respond to the maximum ranks parameter, if specified. That is, if the max rank is `500`, then your dictionary should only include the top `500` most popular names of _each_ sex  per year.

- The `continue` keyword is a good way to have a loop "skip" if the rank is beyond your threshold.

- You should start by testing with a max ranks of `500`. This will give you a more reasonable 3437 name/sex entries, rather than the full set (which is more than 105k entries).

Finally, your method should keep track of _and print out_ the amount of time it takes to load and process all the files. For example:

```
$ python3 name_plotter.py path/to/name/data/folder
Loading files...
Done. Time to load: 1.559 seconds
```

You can get the current time (with usually millisecond precision) using the [`time.time()`](https://docs.python.org/3/library/time.html#time.time) function. Calling this function twice and subtracting the results will let you get time elapsed (e.g., like using a stopwatch).

Once this function is working, you should `add` and `commit` your work so far. In addition, you should [tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) your commit as `load-raw`. This will let us easily be able to find and go back to this version of your code.


## Step 2: Transforming Data
You've successfully loaded the data into memory, but we want to be able to keep track of the data by name and sex, not by year! Thus you'll need to **transform** that data so that it is organized in a more useful way.

In particular, we want each name-sex combo to be associated with the _counts_ and _ranks_ of each of the 135 years in the data set. That is, each name-sex entry needs to have a **`set`** (like a list or dict) of counts (one per year) and a **`set`** of ranks (one per year). Ideally, these will be encapsulated into some kind of "record", and thus our data can just be a list of these records

### Aside: Representing Records
So what data structure should you use to represent a record?

- A *`tuple`* would be highly appropriate (since the data is not going to change once it is assigned), but the syntax could get awkward since you'd need to remember which index contains which piece of information (that is, what does `data[entry][1][2015]` represent?)

- A *`dictionary`* might make this a bit better since we could replace indices with keys (`data[entry]['rank'][2015]`), but we still have the rather extreme "nesting" problem. We also lose the ability to compare records easily.

- We could improve on this by define a *`class`* (e.g., `NameRecord`). That will let us access values as attributes with dot notation, rather than with a bunch of brackets: `data[entry].ranks[2015]`. We'd need to provide methods to compare records.

- But we don't need to encapsulate any _behavior_ along with our data, so using a class is a bit overkill. Another "lightweight" solution would be to use a [NamedTuple](https://docs.python.org/3/library/collections.html#collections.namedtuple), which is like a cross between a `tuple` and a `class` in that you give each element of the tuple a "name" like an attribute.
    - This can be an elegant approach, hough using the attribute to access data in a NamedTuple will be _noticeably_ slower because it takes twice as much work (and we'll be accessing that data a lot). See [this thread](http://stackoverflow.com/questions/2646157/what-is-the-fastest-to-access-struct-like-object-in-python) for details.

In the end, you can use whichever data structure you feel is best to represent a "record"---pick an option and justify your decision in the `SUBMISSION.md` file.

### Your Task
This your task is to modify your program so that the `load_names_data()` function instead returns a **`list`** of "records", where each record represents _all_ the information (counts and ranks for all years) for a particular name-sex entry.

- **IMPORTANT!** This function _must_ return a **`list`** of records, not a dictionary: we'll look at using a dictionary later in the assignment (and explicitly compare the two options).

- You should retain the "raw" data loading code you've already written, and instead just add additional logic to the end of the function that "transforms" the raw data into record-structured data. Alternatively (and more cleanly), you could define a new function (e.g., `transform_data()`) that you call at the end of your `load` function in order to _transform_ the data before returning it.

This transformation process can be tricky: in general you'll want to iterate through all the tuples in each year of the raw data, making a new "record" item in your new list for each one. However,  what happens if you created a record for "Alice" in 1880, and then come across "Alice" again in 1881? You don't want to create a new record (because one record holds information for **all** the years)---instead, you want to update the existing "Alice" record to record the rank for 1881.

Thus you should consider the following the algorithm:

```
for each year
    for each tuple
        search through the current list of records for one that matches the tuple
        if record is found
            add that year's count and rank to the existing record
        else
            make a new record with that year's count and rank, and add to the list
```

(Other approaches may work, but this algorithm is the expected technique and will fit best with later steps).

- Make sure to stop searching (e.g., `break`) once you find the once you've found the record (for reasons that will become quickly apparent).

You'll also want to measure and print the **time to transform** the data, e.g.,:

```
Transforming data...
Done. Time to transform: 20.507 seconds
```

That 20 seconds is normal for this algorithm: I recommend testing with a max ranks of 500 or even 300 or 250 to keep your development time more reasonable.

Why does it take so long? Try printing out what year you're processing in the "outer" loop of the algorithm. What do you see about the amount of time it takes to read each year's file? Do you see it slowing down? Why is that?

- Try (temporarily) increasing the max ranks to 1000. What happens to the speed? Why?


## Step 3: Plot a Name!
Well it's excruciatingly slow (particularly with a large max ranks), but at least it works---the data is now structured so that we can achieve the goal of plotting name popularity over time.

Define a new function called **`find_name_record()`** that takes as parameters a list of name records, a name, and a sex. The function should _search_ the given record list and return the record that matches the given name and sex, or `None` if there is no such record.

- This should just be a basic linear search.

Next, fill in the indicated section of the provided `plot_names()` function so that it calls your function, and adds the values for each year to the Scatter plot trace. This should allow you to then plot the names as a line graph.

For fun: try plotting your own name! Other interesting names to plot (from Nick Parlante):

- Type in your parents or grandparents names. Names like Ethel and Mildred and Clarence may sound old fashioned---and they are! But wait long enough and they come back. Emma! Hannah!
- Michael is very popular. To see the growing Spanish speaking influence in the US, look at Miguel. For a more recent immigration, look at Muhammad and Samir.
- Apparently Biblical old-testament names came back in the 1970's. A reaction to the 1960's maybe? Try Rachel and Rebecca. The pattern seems to generalize: Sarah, Abraham, Adam. Eve and Moses are out of luck for some reason though.
- Why is Rock popular in 1950 and Trinity in 2000?

The sociology of baby naming is a really fascinating topic. Randall Munroe has a nice [writeup](http://blog.xkcd.com/2014/01/31/the-baby-name-wizard/) about the [Baby Name Wizard Blog](http://www.babynamewizard.com/blog) which explores some of these issues, and might be a nice inspiration for plotting.


## Step 4: Faster Searching
The code as it exist is way to slow. 20 seconds to load... and we're not even including the entire set of names! (Which means that less common names are missing, giving our data analysis a strong bias towards "traditional" Western---read: "white"---names).

So let's fix it.

### The Linear Search
The problem with the current transforming algorithm is that we need to **search** through an increasingly long list of records. Each time we see a new line in the file, we need to search through the entire list, and that can get slow. Since we've been using a **linear search**, making the list longer adds an equivalent length of time that we have to search (and since we have to search for each record, out speed is a linear function of the number of data points, of which there are like 25mb worth!

We'll start by making this linear search explicit. But to more easily compare the different approaches, we're going to want to have different versions of the code that we can jump between. Since ___git___ is designed for version control, you should use [git branches](https://www.atlassian.com/git/tutorials/using-branches/) to represent the different versions of your code.

Create and checkout new branch called `linear`:

```
git checkout -b linear
```

This will start a "new branch" of commits from your previous code (you'll want to have committed your changes before you branch). You can then switch between branches by using `git checkout branch-name` (use `git branches` to see a list of branches; you should have two at this point: `master` and `linear`).

Back to making the linear search explicit: you should have already written a linear search for  records in the form of the `find_name_record()` function! Look at your implementation of the data transformation and find the loop that searches the for a record (I know it's there). Then _refactor_ the code so that rather than using that loop, you call the `find_name_record()` linear search method instead.

- This adjustment should not actually change the functionality of your program though it may slow it down more since the computer now needs to move over to a different function to do the search. But we're about to make it better, I promise!

Once you've done this change on the `linear` branch, you should [`merge`](https://www.atlassian.com/git/tutorials/using-branches/git-merge) those changes back into your `master` branch. To do this, checkout the `master` branch and then use

```
git merge linear
```

to merge the `linear` branch into the current (`master`) branch. You might get a **merge conflict** if you've made other changes to the `master` branch; if so, you'll need to [resolve them](https://help.github.com/articles/resolving-a-merge-conflict-from-the-command-line/).

- This is how professional programming is done using git: you create a new branch to do further work on (thereby leaving the "old" version in working order), and then merge in the changes once they are ready to go.

- Don't delete the `linear` branch! We want to save it for posterity.


### The Binary Search
Linear searches are relatively slow (`O(n)`), so you should replace it with a much faster [**binary search**](https://en.wikipedia.org/wiki/Binary_search_algorithm) (`O(lg(n))`).

First, create and checkout another new branch called **`binary`** to represent the binary search version of your program (see above for details).

Then, on the `binary` branch, _refactor_ the code once again so that the algorithm uses a binary search to find records when processing each new line in the data files.

- A binary search only works on a **sorted** list, so you'll want to make sure to "re-sort" your list (e.g., with the `.sort()` or `sorted()` method) after you've added a new record to it. If you've used a `tuple` or a `NamedTuple` to represent the record this will work perfectly; you'll need to do some extra work if you're using a `dictionary` or a `class`.

- Replace the `find_name_record()` linear search with a _binary search_ implementation. See the lecture notes and the many examples online for this algorithm.

    - I recommend testing your binary search on the data that you've loaded linearly, and then replacing the linear search inside the transform code with your binary version instead. You may need to make a temporary `find_name_record_linear()` function to be able to do both types of searches at once.

Can you now load the top 1000 names? 2000? How long does it take? Have things improved?

Be sure and **merge** this `binary` branch back into the `master` branch, so that your master is up to date.

## Step 5: Fastest Searching
This is good, but we still can't get the entire list without waiting an unreasonable amount og time. Can we do better? Oh you bet we can.

Create and checkout a _third_ new branch called **`hashmap`** (a Hashmap is a computer science data name for a `dictionary`... which is what you're going to use).

On this new `hashmap` branch, edit the transformation algorithm so instead of returning a `list` of `tuples`, it instead returns a **`dict`** whose keys are `(name, sex)` tuples and whose values are the records (using whatever structure you wish).

- The algorithm will remain the same, but instead of needing to search for a record, you can simply look it up in the `dictionary` (the `.get()` method is useful here). If there is no matching record, simply add a new item to the dictionary with the appropriate key!

- Dictionaries provide **constant time** (`O(1)`) access, so looking stuff up is basically instantaneous; drastically faster than even the binary search!

You will also need to modify your `find_name_record()` function so it just looks up the key in the dictionary rather than doing a search. Yes, this function will have only one or two lines of code.

Now that looking up a record takes the same amount of time no matter how big the list grows, you can load the entire data set! How long does it take to transform the data now? Record your results in the `SUBMISSION.md` file.

Finally, remember to **merge** this `hashmap` branch back into the `master` branch. The `master` branch for your script should be able to work on the entire data set without taking an unreasonable amount of time.

And now that it runs reasonably quickly, you can plot name history and start asking questions about trends in baby naming over the last 135 years!


## Extensions
As an extra credit extension, you can improve upon the visualization generated by the `plot_names()` function. This is not just adding further styling/details/etc, but to make the visualization much more _interactive_.

My original plan for the assignment was to have you remake the wonderful [Name Voyager](http://www.babynamewizard.com/voyager#prefix=&sw=both&exact=false) visualization, but Plotly turned out to be in no way up to the task. Even the most basic interactions like being able to "select" a trace or dynamically search for data by typing into a textbook isn't supported. However, there are other (better?) visualization libraries out there, even in Python! For example, [Bokeh](http://bokeh.pydata.org/en/latest/) supports creating "widgets" like text boxes that can be used for interactivity. If you redo this visualization to make it interactive using something like Bokeh (or even by drawing elements by hand, using [Tkinter](https://wiki.python.org/moin/TkInter), you can earn significant extra credit.

- Note that we _will_ be using JavaScript---a web-based programming language---to do this kind of thing more near the end of the course, so you will have a chance to create interactive visualizations!


## Submit Your Solution
Remember to `add`, `commit`, and `push` your script once it's finished!

**IMPORTANT!** You will need to make sure to `push` _all_ 4 of your repository's branches to GitHub. If you just use `git push origin master` like we have in the past, you'll only push the `master` branch. Instead, use

```
git push origin --all
```

To push _all_ the branches to GitHub. You should be able to see each one individually by selecting it from the dropdown menu on your repo.

In order to submit you assignment, you  need to both `push` your completed solution (all branches) to your GitHub repository **and** submit a link to your repository to [Canvas](https://canvas.uw.edu/) (so that we know where to find your work)!

Before you submit your assignment, double-check the following:

1. Confirm that your program is completed and works without errors in all four versions. It should be able to run without errors. 
* Be sure and fill out the **`SUBMISSION.md`** included in the assignment directory, answering the questions. _Remember to fill out the table!_
* `commit` the final version of your work, and `push` your code to your GitHub repository.

Submit a a link to your GitHub repository via [this canvas page](https://canvas.uw.edu/courses/1041440/assignments/3208932).

The assignment is due on **Wed May 18 at 6:00 AM**.

### Grading Rubric
See the assignment page on Canvas for the grading rubric.

_Based on an assignment by Nick Parlante._