# Messari Challenge

## <a href="https://medium.com/@rahulkumaran313/uniswap-listener-data-ingestion-analysis-949214c9e10c">Medium Article Detailing the Entire Data Engineering and Science Process Followed With Robust Insights and Suggestions</a>

The article is fairly long as it details the entire process I adopted while working on this task but I promise it would be worth reading. If unable to read through the entire article, you could go through the analysis side of things - mainly the aspect correponding to analysis on how many recipients are contracts, wallets, etc and fee based pool utilisations. Make sure to read the suggestions and conclusions too towards the end of the article (last 2 sections).

--------------------------------

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
