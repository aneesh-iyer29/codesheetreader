# codesheetreader
This program converts Codebusters Questions from a Google Sheets Masterdoc to Latex, allowing for easy collaboration and a professional, formatted look. Advantages include the use of a dyslexia friendly font and the delocalization of the formatted test document.

To use, make a copy of this sheet: https://docs.google.com/spreadsheets/d/1XnOdkZioY0s10qt-8lDSdHjRs0mzWC2tmbFxVboDeoA/edit?usp=drive_web&ouid=114000520835446303801 and fill it out according to the instructions

Download the script and the sgb-words file, which is written in python and will automatically format the test in LaTex from this sheet. To use the script, I would recommend running it in Jupyter Notebook, as this already has the libraries necessary. Otherwise, you can run it in console with VScode or some other IDE. 

To run the script, download the sheet as an xlsx file and upload it into the same folder as this program and the sgb-words file.

When you run the program, it will prompt you for 3 items:

1. Test file (it will automatically make a directory if it doesn't exist)
2. Key file (same as above, these are both .txt files)
3. Sheet with ciphers (.xlsx, what you downloaded and put into the folder, if the name of your sheet has spaces you can type that in the input box)

After this, you must make a copy of this Overleaf project (https://overleaf.com/read/yxjtjdcgykgp#aa9620), paste the output of the test file from above below the \begin{questions} on the test document and paste the output of the key file below the \begin{questions} on the key document. Edit the necessary questions on the key document that don't provide enough information (such as the key for extract problems and the cryptarithm numbers). Finally, you must move the first question output by the program to the slot for the timed question and verify that there are no major issues with the formatting on the test.					 				

During competition, the use of this scoresheet (https://docs.google.com/spreadsheets/d/1h1R41eBoE3XqVG6Q-ygBFfwU0ZS2NAwi_5mee_JKS6E/edit?usp=drive_link) is advised to reduce mistakes and automatically tally scores, formatted to provide to the appropriate scoremaster
