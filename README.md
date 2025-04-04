# BSL Anki Deck

This is forked from [sandbach's repo](https://github.com/sandbach/bsl-gcse), and lets you input your own words into the file bslvocabv1.csv. Please go to their repo to learn more!

useful links:

- [Anki](https://docs.ankiweb.net)
- [SignBSL.com](https://www.signbsl.com/)
- [Anki documentation about importing notes with CSV files](https://docs.ankiweb.net/importing/text-files.html)

# Input CSV

The input file (inputwords.csv) has different words, each having a ranking (essential, more frequent, frequent, less frequent), which determines the order of the Anki cards. They also have a category. The code should work without these, if you just want to add a word per line.

# Variables

you can choose to delete the current words on the output csv or not by toggling the variable csv_cleared_at_start.
you can change what the input file and output file is by changing INPUT_CSV and OUTPUT_CSV.
I haven't added a way to not include any missed words, but these are easily deleteable in Anki, as all missed words are tagged with 'NOTFOUND'.

# Output CSV

the output csv has the following items: headword, definition, example, video_url, video_title, url, tags

if a word cant be found on signbsl, it's definition will be 'TRANSLATION NOT FOUND', and it will also be tagged 'NOTFOUND'.
