# KC Tenants Tech Team HW Assignment #1
## Spring 2025 Training Session

## Background

The KC Tenants Technology Team has been coordinating a "mini-course" for its members, focusing on teaching interested individuals Python, Git, and MySQL. One core component of learning is doing and to that that end, we created this set of files as a "practice problem" for course attendees to complete between sessions. 

This set of files includes an input file, a file to write your code in, and a testing suite so that you can gain instant feedback about your code! 

Generally speaking, this code project is a sample of a case where you have a set of data in a spreadsheet that you want to modify into a new format. In this case, you'll need to pull that data from the excel sheet into your code, modify it (see more below), and write it out to a new csv file on your computer.

## What Should I Do?

We have included an input CSV file which is comprised of some sample data from the Hotline project. That data is anonymized so we are not violating the privacy of the individuals who call the Hotline. The data is also reduced in scale to reduce the amount of information you have to sort through.

Your goal is to write code that intakes this input file, makes some modifications to the data from that file, and creates a new output CSV file with the modified data. We have included a system test (`system_test.py`) that will automatically run tests against your code and tell you if your software succeeded.  We have also included another type of test, a "unit test" (`unit_tests.py`) which tests individual aspects of your code.

*Note: If you wanted to, it _would_ be possible to "cheat" and make this testing framework automatically pass. Given the stated intention of this course is to learn, we assume you won't do that, but we won't take action to stop you!*


## What is the Problem Statement? 

Your code, which starts executing in `main()` in the file `main.py`, should import the data from the file `inputs/input.csv` and modify it. The modified data should be placed into a new output CSV file that is located in `outputs/output.csv`. The desired modifications are as follows:
- The output CSV should remove any cases whose Case Number are divisible by 9.
- The output CSV should format all gender tags in the same way. Specifically:
    - All tags that indicate `Female` should be updated as `Female (she/her)` in the output CSV.
    - All tags that indicate `Male` should  be updated as `Male (he/him)` in the output CSV.
- The output CSV should organize all the cases from the input file by Case Number, in ascending order, with one exception:
    - All cases with the landlord as `Mac` Properties should be listed above all cases where that isn't true. Within each group, all cases should be organized by Case Number in ascending order. Mac Properties might be recorded as any Landlord Entry that includes the text `mac`, regardless of case or any other surrounding text.

Here is a simplified sample of the correct ordering of the output data (to demonstrate how the ordering should work):

| Case Number | Landlord | 
|-|-| 
| 100 | Mac Properties |
| 154 | Mac Properties |
| 178 | Mac Properties |
| 98 | Matt McGee |
| 112 | Patrick Mahomes |
| 209 | Rhodes Conover | 


## I Wrote Some Code; Is It Right?

To tell if your code is right, you'll need to run the code! This section should help with that! 

### Running Python

To run Python, you need to first install Python. If you're using a Mac or Linux to do this work, Python is built directly into your Operating System so you don't need to do any installation. If you're on Windows, you'll want to download and install the package from the [Python website](https://www.python.org/downloads/windows/). Ensure you download the newest, stable version of Python 3 (not 2). If you're not sure which one that is, just grab the most emphasized link on the page and/or reach out to Rhodes or Isaac for guidance. 

To confirm that Python is available to use, open up Command Prompt on Windows or Terminal on Mac and type in: 

```python```

If successful, it should open a Python "shell", which should update your terminal window to look something like: 

```
Python 3.10.11 (v3.10.11:7d4cc5aa85, Apr  4 2023, 19:05:19) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
In the prompt after `>>>` you can type any Python command you'd like, but you don't need to: you've already confirmed that you've installeed Python!

If the `python` command does not work. Instead, try `python3`! This is often caused if your system has reserved the `python` command for the old version of Python (Python 2).

Once you've achieved this, in your standard Terminal or Command Prompt window, [navigate to the directory](#navigating-in-your-terminal) where this package of files is contained. Once in the same directory as `hello_world.py`, type `python hello_world.py` into the prompt and it should should back: 

```
"Hi! This is Rhodes from the past talking to you!"
```

In this case, you have just "run" a python script I wrote that just prints that message out to you! You can open that file and see how I did it (it's a single line). Feel free to change the message in `hello_world.py` and run it again!


### Running Tests

So, you've written some code and you're wondering if you're on the right track. The best way to know is to **run some tests** to see if the thing does what you think it should do! You could do that entirely manually (i.e, visually inspecting if it's right), or you could write automated tests to do it for you! Fortunately, we're not going to ask you to write automated tests yourself, we've written them for you!

We've created two types of tests. The first is `unit tests`, which help you test individual aspects of your code. That way, if you have a mistake that's relatively minor, you can quickly identify where the issue is and try to fix it. The second type of test is a `system test` that tests the final CSV file you generate matches the correct CSV that I generated in advance! If so, you've achieved your goal! This is the one to run if you think you're 100% done (if it passes, you've done it)!

#### Some Debugging Basics

Both types of test should give direct feedback about what is or isn't working about your system. If you've run a test and discovered an error, it's good to remember that the error could either occur in your code (because you've made a mistake in your code that caused it stop running) or in the testing framework (because your code runs, but produces incorrect results). Generally, we refer to issues that cause your code to stop as "errors" and issues where the code finishes but is wrong as "bugs". This is not universal, but helpful. The error messages you receive should indicate where the error occurred, including a file name, and line number! Start there and try to figure out what went wrong! If you can't, you can always reach out to Isaac and Rhodes with a picture of the error and a picture of the code that it says failed! 


#### Running System Test

To run the System Test, all you need to do is run the following command from your Terminal Window: `python system_test.py`. You do not need to provide any other information, it will automatically run and print results to you in the Terminal Window directly! 



#### Running Unit Tests

Unit Tests were designed slightly differently than System Tests. The System Tests were written entirely in Python that Rhodes wrote, and it runs your entire script and just checks that the CSV file you created matches the correct one that Rhodes generated. Nothing too fancy.

On the other hand, the Unit Tests, in real time, generates a bunch of sample data for your code to modify (without worrying about the file manipulation) and gives it to the code directly. It does this a bunch of times over and checks that your code is right in a wide variety of scenarios. It uses a Python Library called `hypothesis` (code written by other people) to automatically generate this test data and run the test for you.

**DO NOT WORRY!** You DO NOT need to figure out how to install `hypothesis` yourself. Instead, Isaac made a special environment that allows you to install a separate tool to handle all the un-fun parts _for you_. 

To run the unit tests, do the following:
1. Install `uv`, using this command: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Once installed, restart your Terminal Window. 
    - Note: On Mac, you'll need to actually "Quit" the window or it won't work. 
3. Navigate to the package of files we've provided and run the command: `uv run unit_tests.py`. This will automatically install all packages and run the tests against your code. 

If you have any questions, feel free to reach out to either Isaac or Rhodes.


## Some Good Resources

For more information, check out:

- [W3 Schools](https://www.w3schools.com/python/default.asp)




And of course, you can ALWAYS reach out to Isaac and Rhodes on Signal for some insight! We would _love_ to help you debug the issue and/or clarify points of confusion! :)





## Additional Guidance:

This section just contains extra information you might find useful. Feel free to ignore it if it is not helpful.

#### Navigating in Your Terminal

To navigate to a particular directory, you'll need two primary commands: One to change your current directory, and one to read out the contents of your current directory.

To read the contents of your current directory, type `ls` (as in "List") on Mac or Linux, and `dir` (as in "Directory") on Windows. Each will print out a list of all files and directories inside your current file. Using this, you can identify where you need to navigate.

To change to a new directory, type `cd` (as in, "Change Directory") on any machine followed by the directory you want to go into. For example, `cd inputs`. This will change the active directory and you will see this reflected if you type `dir`/`ls` again. 