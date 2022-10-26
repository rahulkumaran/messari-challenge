# Messari Challenge
# Uniswap : Building a data engineering & analysis pipeline to analyze all swaps occurring on high volume and TVL pools

## Project in a Nutshell
--------------------------------
My problem statement is kind of a combination of the 2 challenges provided in the take-home task Google Doc. More specifically, I've built a data engineering pipeline from scratch and then utilised the data to produce actionable insights too. The problem statement I worked on is related to Uniswap.

I consider 18 high volume and/or TVL LPs on Uniswap wherein I'm listening to these LP contracts to procure all "Swap" related events corresponding to all of these LPs and pushing this data into s3 buckets on AWS. This data is then read into a Jupyter notebook from AWS where I perform various manipulations and mention insights derived wherever possible. More specifically, my analysis is focused on who is making swap transactions, whether transactions are actual swaps or a mere route and finally understanding pool based stats when grouped by fees. The notebook ends with suggestions from my end that I believe could help Uniswap improve their DEX experience.

I conclude with suggestions on how Uniswap could make a better product that could focus on more utilisation. I have explained the entire project's process and insights in the Medium article below too.

--------------------------------
## <a href="https://medium.com/@rahulkumaran313/uniswap-listener-data-ingestion-analysis-949214c9e10c">Medium Article Detailing the Entire Data Engineering and Science Process Followed With Robust Insights and Suggestions</a>

The article is fairly long as it details the entire process I adopted while working on this task but I promise it would be worth reading. If unable to read through the entire article, you could go through the analysis side of things - mainly the aspect correponding to analysis on how many recipients are contracts, wallets, etc and fee based pool utilisations. Make sure to read the suggestions and conclusions too towards the end of the article (last 2 sections).

--------------------------------
## Time taken to work on the project

## Total time : ~20 hours
### Researching : 1.5 hours
### Setting up AWS + Heroku : 1 hour
### Coding : Friday 6 hours + Saturday 6 hours (12 hours in total)
### Testing code + Writing Article : Sunday 2 hours + Tuesday 2 hours (4 hours in total)
### Code documentation : 1.5 hours

---------------------------------

# To run data engineering pipeline
### Install Requirements - `pip3 install -r requirements.txt`
### Run Code - `python3 main.py`

--------------------------------
NOTE - Procfile is used for Heroku Deployment - Heroku Deployment currently turned off - can be turned on and can give access if required. Please let me know by preferably emailing me @ rahulkumaran313@gmail.com or by creating an issue.

ALL AWS credentials in the code are active for now. Credentials not masked or encrypted (In general I would store them as an environment variable).
Credentials in plain sight so that reviewers can run them locally without any hindrance and additional set up.
QuickNode endpoint need not to be changed, but can be update to another new Infura or QuickNode endpoint - sufficient free API calls available.

--------------------------------
# To run jupyter notebook
Step1 : Type `jupyter notebook` in your terminal while in the project folder 

Step2 : Then click on `Uniswap Analysis.ipynb` file once Jupyter opens up on your browser

Please ensure Jupyter is installed.

Also, Infura endpoint is being used within Jupyter notebook - has a few free API calls left - but if you get some errors, please feel free to use another Infura or QuickNode endpoint by replacing the existing one or ask me to replace the endpoint by letting me know via email @ rahulkumaran313@gmail.com
