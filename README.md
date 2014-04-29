PySounds2
=========

My Python ripoff of Mark Rosenfelder's Sound Change Applier, in its second iteration, with a GUI.

Only works in Python 3.

testPySounds2.py is the command line interface; it has a help screen. 

PySoundsGUI.pyw is the GUI interface.

There are no unit tests (I hadn't discovered them yet when I wrote this) 
and things might not work. There are some features I never finished 
debugging, like negative environments.

I'm not going to put this code under official license. You can use and 
redistribute freely, but I'll ask that you add any modifications you 
make to this Git repository so I can see them.

No warranties. This is code from a time when I was even more immature 
than now, so it is overly commented and buggy.

## If you're not sure what this program is for...
...you're probably not a conlanger.

Conlangers are people who like making **con**structed **lang**uages, like Tolkien's Elvish languages or the Klingon language in Star Trek. This has become something of a trend in Hollywood recently; *Avatar*'s Na'vi and *Game of Thrones*'s Dothraki are two other notable constructed languages.

The thing is, languages in real life change over time, and not just in the words that people use. There's more difference between Hemingway and Shakespeare than *thou* and *thy*, as you know if you've ever tried to read Shakespeare, and even more difference between Hemingway and Chaucer. In Chaucer's time, the pronunciation of words was completely different than in Hemingway's time, even though the spelling makes them look a little bit similar. That's because the sounds of languages change over time, sometimes so much that we can't even call the two forms the same language anymore. Latin turned into French, Spanish, Italian, and Romanian; *Beowulf*'s Old English turned into Chaucer's Middle English, which become Shakespeare's Early Modern English. Even further back, there was a language called Proto-Indo European that turned into the ancestors of Latin, Old English, Sanskrit, and many other languages.

These sound changes aren't random or chaotic; they are governed by rules. Comparative linguists compare languages to find out if there's a set of sound change rules that could have turned one ancestor language into two related, sister languages.

The [Sound Change Applier](http://www.zompist.com/sounds.htm) is a C program written by Mark Rosenfelder of [zompist.com](http://www.zompist.com). It takes a file of sound change rules and a file of words in some language&mdash;constructed or natural, it doesn't care&mdash;and applies the rules to the words, mimicking the natural process of language evolution. It was an extremely useful program, but I had various frustrations with it. For one thing, categories of sounds had to be named with a single capital letter, and a lot of context-aware features weren't directly supported and had to be faked with categories. So it was common for me to run out of sensible category names and have to resort to ones that made no sense. There were also some features which could have been useful, but never seemed to work properly for me, like the -p command line option. Optional elements also only seemed to work about half the time.

After I got into programming and learned Python, I decided that enough was enough, and I was going to write my own. Python was clearly a better language than C for this sort of text-handling task, anyway; it even had regular expressions! So I took some time during my summer vacation and wrote my own Sound Change Applier.

This is not that program. This was my second attempt, after I had learned much about regular expressions, Python, and programming in general from my work on PySounds 1. The code is much better than the PySounds 1 code, though it still falls somewhat short of my current standard. But I'm proud to say that this program does work, and it supports Unicode, which solves about 93% of the trouble I had with the SCA, and it supports categories with full words for names, which solves another 6% of the trouble. I never did finish half the things I had planned for this; somewhere along the way, I stopped being interested in constructing languages and started to be more interested in programming, so this became a programming exercise for me, one that I never really finished.

Now Rosenfelder has released [sca2](http://www.zompist.com/sca2.html), a Javascript program that pretty much does everything I ever wanted PySounds 2 to do. So you should probably use that instead if you're after a serious conlanging tool. As for me, if I ever get back into conlanging, I'll be using PySounds 2, and maybe then this will become a program worthy of serious conlanging. 

## Todo
  - Rewrite the command line interface to use argparse.
  - Do validation on the arguments, e.g. check that the extensions are correct and that the files exist.
  - Don't have the GUI version write out to a file by default. Instead, use a radio button group that lets the
    user select between writing to a file and writing to screen. Also add a button 'Save to file' that lets the
    user save screen output to a file.
  - Change the colors on the GUI.
  - Make the file open dialogs start in the most recent directory.
  - Make a new icon. Nino is copyrighted.
