"""
This module contain the code for saving the scraped data
"""


import pandas as pd
from .settings import OUTPUT_PATH
import os


class DataSaver:
    def __init__(self, outputformat, messageshowfunc) -> None:
        self.outputFormat = outputformat
        self.messageShowFunc = messageshowfunc

    def save(self, datalist,filename):
        """
        This function will save the data that has been scrapped.
        This can be call if any error occurs while scraping , or if scraping is done successfully.
        In both cases we have to save the scraped data.
        """

        if len(datalist) > 0:
            self.messageShowFunc(custom=True, value="Saving the data")

            dataFrame = pd.DataFrame(datalist)
            totalRecords = dataFrame.shape[0]

            #filename = "/gms output"

            if self.outputFormat == "excel":
                extension = ".xlsx"
            elif self.outputFormat == "csv":
                extension = ".csv"
            elif self.outputFormat == "json":
                extension = ".json"

            joinedPath = OUTPUT_PATH + filename + extension

            if os.path.exists(joinedPath):
                index = 1
                while True:
                    filename = f"/{filename}"

                    joinedPath = OUTPUT_PATH + filename + extension

                    if os.path.exists(joinedPath):
                        index += 1

                    else:
                        break
            if self.outputFormat == "excel":
                dataFrame.to_excel(joinedPath, index=False)
            elif self.outputFormat == "csv":
                dataFrame.to_csv(joinedPath, index=False)

            elif self.outputFormat == "json":
                dataFrame.to_json(joinedPath, indent=4, orient="records")

            self.messageShowFunc(savingdata=True, totalrecords=totalRecords)
        else:
            self.messageShowFunc(
                custom=True, value="Oops! You did not scrape any record..."
            )
