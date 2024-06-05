SPORTweet Dashboard

Overview

The SPORTweet Dashboard is a front-end application designed to categorize and display tweets related to different sports. The dashboard processes tweets one by one, categorizing them into five sections: Soccer, Football, Basketball, Rugby, and Other. Additionally, it features interactive elements such as trendline graphs and a word cloud representing the popularity of various sports.

Features
Categorized Tweets: Tweets are categorized into Soccer, Football, Basketball, Rugby, and Other.
Rolling Graphs: Trendlines for Soccer, Football, Basketball, and Rugby are displayed as rolling graphs.
Word Cloud: Shows the popularity of sports keywords (soccer, football, basketball, rugby, volleyball, cricket, tennis, and baseball).
Interactive Labels: Labels double as buttons to collapse or expand tweet blocks and graphs.
Technologies Used
Python: For processing tweets and backend logic.
HTML: For creating the structure of the homepage.
CSS: For styling the dashboard.
JavaScript: For interactivity and integrating with ECA software.
ECA Software: Pre-determined software for communication between Python and HTML.
Project Structure
sportweet.py: Python script for processing tweet data.
index.html: HTML script for the homepage.
CSS files: Multiple files for styling the dashboard.
Setup Instructions
To set up the SPORTweet Dashboard, follow these steps:

Extract Files: Extract all files from the attached ZIP file into a folder.
Add Tweet Collection: Drag the sports tweet collection text file into the folder and name it sports.txt. The Python program references this file by this name.
Open Command Prompt:
Navigate to the folder containing the extracted files.
Type python neca.py -s sportweet.py and press ENTER.
Open Browser:
Use Mozilla Firefox for best results.
In the search bar, type localhost:8080.
View Dashboard: The dashboard should now be displaying on your browser window.
Notes
Browser Compatibility: Mozilla Firefox is recommended as it ensures consistent display across most devices. Other browsers may cause elements to appear distorted or not display properly.
