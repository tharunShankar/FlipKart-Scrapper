import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from RepositoryForObject import ObjectRepository
from selenium.webdriver.common.by import By
import pandas as pd


class FlipkratScrapper:

    def __init__(self, executable_path,chrome_options):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the webdriver object.\n" + str(e))

    def openUrl(self, url):
        """
        This function open the particular url passed.
        :param url: URL to be opened.
        """
        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))

    def waitExplicitlyForCondition(self, element_to_be_found):
        """
        This function explicitly for condition to satisfy
        """
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            WebDriverWait(self.driver, 10, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_to_be_found)))
            return True
        except Exception as e:
            return False
            raise Exception(f"(waitExplicitlyForCondition) - Something went wrong while waiting.\n" + str(e))

    def getCurrentWindowUrl(self):
        """
        This function returns the url of current window
        """
        try:
            current_window_url = self.driver.current_url
            return current_window_url
        except Exception as e:
            raise Exception(f"(getCurrentWindowUrl) - Something went wrong on retrieving current url.\n" + str(e))

    def getTitle(self, url):
        """
        This function retrieves the title of particular url given
        """
        try:
            url_retrieved = self.getCurrentWindowUrl()
            if url_retrieved == url:
                return self.driver.title
        except Exception as e:
            raise Exception(f"(getTitle) - Cannot retrieve the title of given url.\n" + str(e))

    def checkPageTitle(self, title):
        """
        This function checks the title of the current url.
        """
        try:
            retrieved_title = self.getTitle(url=self.getCurrentWindowUrl())
            if retrieved_title == title:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkTitleForPage) - Something went wrong on checking title.\n" + str(e))

    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorsObject) - Could not find locators\n" + str(e))

    def login_popup_handle(self):
        """
        This function handle/closes the login popup displayed.
        """
        try:
            locator = self.getLocatorsObject()
            close_button_path = locator.getLoginCloseButton()
            element = self.findElementByXpath(close_button_path)
            element.click()
            return True
        except Exception as e:
            raise Exception("(login_popup_handle) - Failed to handle popup.\n" + str(e))

    def findElementByXpath(self, xpath):
        """
        This function finds the web element using xpath passed
        """
        try:
            element = self.driver.find_element(By.XPATH, value=xpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByXpath) - XPATH provided was not found.\n" + str(e))

    def findElementByClass(self, classpath):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.driver.find_element(By.CLASS_NAME, value=classpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByClass) - ClassPath provided was not found.\n" + str(e))

    def findElementByTag(self, tag_name):
        """
        This function finds web element using tag_name provided
        """
        try:
            # element = self.driver.find_element(By.TAG_NAME,tag_name)
            element = self.driver.find_elements_by_tag_name(tag_name)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByTag) - ClassPath provided was not found.\n" + str(e))

    def searchProduct(self, searchString):
        """
        This function helps to search product using search string provided by the user
        """
        try:
            locator = self.getLocatorsObject()
            search_box_path = self.findElementByXpath(xpath=locator.getInputSearchArea())
            search_box_path.send_keys(searchString)
            search_button = self.findElementByXpath(xpath=locator.getSearchButton())
            search_button.click()
            return True
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(searchProduct) - Something went wrong on searching.\n" + str(e))

    def generateTitle(self, search_string):
        """
        This function generatesTitle for the products searched using search string
        :param search_string: product to be searched for.
        """
        try:
            title = search_string + "- Buy Products Online at Best Price in India - All Categories | Flipkart.com"
            return title
        except Exception as e:
            raise Exception(f"(generateTitle) - Something went wrong while generating complete title.\n" + str(e))

    def getAnchorTags(self):
        """
        This function retrives all the anchor tag for the current page displayed
        """
        try:
            all_links = self.findElementByTag('a')
            return all_links
        except Exception as e:
            self.driver.refresh()
            raise Exception(f"(getAnchorTags) - Something went wrong while finding url of products.\n" + str(e))

    def getProductLinks(self):
        """
        This function returns all the list of links.
        """
        try:
            locator = self.getLocatorsObject()
            links = []
            all_links = self.findElementByTag('a')
            for link in all_links:
                links.append(link.get_attribute('href'))
            return links
        except Exception as e:
            self.waitExplicitlyForCondition(element_to_be_found=locator.getElementTobeSearched())
            all_links = self.findElementByTag('a')
            for link in all_links:
                links.append(link.get_attribute('href'))
            return links
            raise Exception(f"(getProductLinks) - Something went wrong on retrieving product links.\n" + str(e))

    def filterProductLink(self, search_string):
        """
        This function helps to filter the list of product links based on search string.
        """
        try:
            all_links = self.getProductLinks()
            product_link = []
            for link in all_links:
                if search_string.capitalize() in link or search_string.upper() in link or search_string.lower() in link:
                    product_link.append(link)
            return product_link
        except Exception as e:
            self.driver.refresh()
            raise Exception(f"(filterProductLink) - Something went wrong while filtering the links passed.\n" + str(e))

    def getUrlDict(self, filtered_list):
        """
        This function returns list of links in dictionary format
        """
        try:
            link_dict = {i for i in filtered_list}
            return link_dict
        except Exception as e:
            # self.driver.refresh()
            raise Exception(
                f"(getUrlDict) - Something went wrong on converting list to dictonary for links.\n" + str(e))

    def actualProductLinks(self, searchString):
        """
        This function returns the actual product links after filtering.
        """
        try:
            filter_Products = self.filterProductLink(search_string=searchString)
            actual_product_link = []
            for link in filter_Products:
                if '?pid=' in link:
                    self.openUrl(url = link)
                    actual_product_link.append(link)
                else:
                    self.driver.close()
                    continue
            return actual_product_link
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(actualProductLinks) - Something went wrong while opening the url.\n" + str(e))

    def getLinkForExpectedReviewCount(self, expected_review, searchString):
        """
        This function extracts the link of product having more than expected count.
        """
        try:
            product_links = self.actualProductLinks(searchString=searchString)
            count = 0
            expected_count = self.getExpectedCountForLooping(expected_review=expected_review)
            while count < expected_count:
                url_to_hit = product_links[random.randint(0, len(product_links) - 1)]
                self.openUrl(url=url_to_hit)
                total_review_page = self.getTotalReviewPage()
                count = total_review_page
                self.driver.close()
            self.openUrl(url=url_to_hit)
            return True
        except Exception as e:
            raise Exception(
                f"(getLinkForExpectedReviewCount) - Failed to retrive the link for product having more than "
                f"expectedcount of review.\n" + str(
                    e))

    def checkVisibilityOfElement(self, element_to_be_checked):
        """
        This function check the visibility of element on the webpage
        """
        try:
            if element_to_be_checked in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            self.driver.refresh()
            raise Exception(f"(checkVisibilityOfElement) - Not able to check for the element.\n" + str(e))

    def getProductName(self):
        """
        This function helps to retrieve actual name of the product.
        """
        try:
            locator = self.getLocatorsObject()
            element = locator.getProductNameByClass()
            if self.checkVisibilityOfElement(element_to_be_checked=element):
                product_name = self.findElementByClass(classpath=locator.getProductNameByClass()).text
            else:
                product_name = self.findElementByXpath(xpath=locator.getProductNameByXpath()).text
            print(product_name)
            return product_name
        except Exception as e:
            self.driver.refresh()
            raise Exception(f"(getProductName) - Not able to get the product name.\n" + str(e))

    def getProductSearched(self, search_string):
        """
        This function returns the name of product searched
        """
        try:
            locator = self.getLocatorsObject()
            product_name = self.findElementByXpath(xpath=locator.getProductSearchedByXpath()).text
            print(product_name)
            return product_name
        except Exception as e:
            return search_string
            raise Exception(f"(getProductSearched) - Not able to get the product searched.\n" + str(e))

    def getPrice(self):
        """
        This function helps to retrieve the original price of the product.
        """
        try:
            locator = self.getLocatorsObject()
            original_price = self.findElementByClass(classpath=locator.getOriginalPriceUsingClass()).text
            print(original_price)
            return original_price
        except Exception as e:
            self.driver.refresh()
            raise Exception(f"(getPrice) - Not able to get the price of product.\n" + str(e))

    def getDiscountedPercent(self):
        """
        This function returns discounted percent for the product.
        """
        try:
            locator = self.getLocatorsObject()
            discounted_price = self.findElementByClass(classpath=locator.getDiscountPercent()).text
            print(discounted_price)
            return discounted_price
        except Exception as e:
            return "No Discount"

    def checkMoreOffer(self):
        """
        This function checks whether more offer links is provided for the product or not.
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getMoreOffersUsingClass() in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkMoreOffer) - Trouble in finding more offer link.\n" + str(e))

    def clickOnMoreOffer(self):
        """
        This function clicks on more offer button.
        """
        try:
            status = self.checkMoreOffer()
            if status:
                locator = self.getLocatorsObject()
                more_offer = self.findElementByClass(classpath=locator.getMoreOffers())
                more_offer.click()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(clickOnMoreOffer) - Not able to click on more offer button.\n" + str(e))

    def getAvailableOffer(self):
        """
        This function returns offers available
        """
        try:
            status = self.checkMoreOffer()
            locator = self.getLocatorsObject()
            if status:
                self.clickOnMoreOffer()
            offer_details = self.findElementByClass(classpath=locator.getAvailableOffers()).text
            return offer_details
        except Exception as e:
            raise Exception(f"(getAvailableOffer) - Not able to get the offer details of product.\n" + str(e))

    def getOfferDetails(self):
        """
        This function returns the offers in formatted way.
        """
        try:
            available_offers = self.getAvailableOffer()
            split_offers = available_offers.split("\n")
            print(split_offers[1:])
            return split_offers[1:]
        except Exception as e:
            raise Exception(f"(formatOfferDetails) - Something went wrong on retriving offer details.\n" + str(e))

    def checkViewPlanForEMI(self):
        """
        This function returns boolean value for EMI is available or not.
        """
        try:
            status = self.checkMoreOffer()
            locator = self.getLocatorsObject()
            if status:
                self.clickOnMoreOffer()
            if locator.getViewPlanLinkUsingClass() in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkViewPlanForEMI) - Error on finding view plans link for EMI.\n" + str(e))

    def getEMIDetails(self):
        """
        This function returns EMI details of the product.
        """
        try:
            locator = self.getLocatorsObject()
            status = self.checkViewPlanForEMI()
            if status:
                emi_detail = self.findElementByXpath(xpath=locator.getEMIDetail()).text
                print(emi_detail)
                return emi_detail
            else:
                return "NO EMI Plans"
        except Exception as e:
            return "NO EMI Plans"
            raise Exception(f"(getEMIDetails) - Not able to get the emi details of product.\n" + str(e))

    # def checkForMoreReview(self):
    #     """
    #     This function checks whether there are more reviews or not on the page.
    #     """
    #     try:
    #         locator = self.getLocatorsObject()
    #         more_review = locator.getMoreReviewUsingClass()
    #         more_review_1, more_review_2 = more_review[0], more_review[1]
    #         if more_review_1 in self.driver.page_source:
    #             return True, more_review_1
    #         elif more_review_2 in self.driver.page_source:
    #             return True, more_review_2
    #         else:
    #             return False
    #     except Exception as e:
    #         raise Exception(f"(checkForMoreReview) - Not able to check for more review.\n" + str(e))

    # def clickOnMoreReview(self):
    #     """
    #     This function click on All reviews link on the web page
    #     """
    #     try:
    #         status = self.checkForMoreReview()
    #         self.wait()
    #         if status:
    #             locator = self.getLocatorsObject()
    #             more_review = self.findElementByClass(classpath=status[1])
    #             more_review.click()
    #             return True
    #         else:
    #             return False
    #     except Exception as e:
    #         raise Exception(f"(clickOnMoreReview) - Not able to click on more review.\n" + str(e))

    def getTotalReviewPage(self):
        """
        This function retrieves total number of pages available for review
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getMoreReviewUsingClass()[0] in self.driver.page_source:
                self.findElementByClass(classpath=locator.getMoreReviewUsingClass()[0]).click()
            elif locator.getMoreReviewUsingClass()[1] in self.driver.page_source:
                self.findElementByClass(classpath=locator.getMoreReviewUsingClass()[1]).click()
            else:
                return int(1)
            if self.waitExplicitlyForCondition(element_to_be_found=locator.getNextFromTotalReviewPage()):
                total_review_page = [self.findElementByClass(classpath=locator.getTotalReviewPage()).text][0]
                split_values = total_review_page.split("\n")
                print(split_values)
                value = str(split_values[0]).split()[-1]
                print(value)
                return int(value)
            else:
                return 1
        except Exception as e:
            raise Exception(f"(getTotalReviewPage) - Not able to get the total review page of product.\n" + str(e))

    def wait(self):
        """
        This function waits for the given time
        """
        try:
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception(f"(wait) - Something went wrong.\n" + str(e))

    def findingElementsFromPageUsingClass(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CLASS_NAME, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))

    def findingElementsFromPageUsingCSSSelector(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CSS_SELECTOR, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))

    def getRatings(self):
        """
        This function gets rating for the product.
        """
        try:
            locator = self.getLocatorsObject()
            rating = self.findingElementsFromPageUsingCSSSelector(locator.getRatings())
            return rating
        except Exception as e:
            raise Exception(f"(getRatings) - Not able to get the rating details of product.\n" + str(e))

    def getComments(self):
        """
        This function gets review comment for the product
        """
        try:
            locator = self.getLocatorsObject()
            comment_object = locator.getComment()
            if comment_object[0] in self.driver.page_source:
                comment = self.findingElementsFromPageUsingClass(comment_object[0])
            else:
                comment = self.findingElementsFromPageUsingClass(comment_object[1])
            return comment
        except Exception as e:
            raise Exception(f"(getComment) - Not able to get the comment details of product.\n" + str(e))

    def getCustomerNamesAndReviewAge(self):
        """
        This function gets customername for the review
        """
        try:
            locator = self.getLocatorsObject()
            customer_name = self.findingElementsFromPageUsingClass(locator.getCustomerName())
            return customer_name
        except Exception as e:
            raise Exception(f"(getCustomerNamesAndReviewAge) - Not able to get the name of product.\n" + str(e))

    def checkForNextPageLink(self):
        """
        This function click on the next page for the review
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getNextFromTotalReviewPage() in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkForNextPageLink) - Not able to click on next button.\n" + str(e))

    def getExpectedCountForLooping(self, expected_review):
        """
        This functoin retrives the total number of pages which should be searched for review
        """
        try:
            expected_count = expected_review / 10
            return int(expected_count)
        except Exception as e:
            raise Exception(f"(getExpectedCountForLooping) - Something went wrong with review count.\n" + str(e))

    def getReviewDetailsForProduct(self, expected_review):
        """
        This function gets all Review Details for the product
        """
        try:
            locator = self.getLocatorsObject()
            ratings, comment, customer_name, review_age = [], [], [], []
            expected_count = self.getExpectedCountForLooping(expected_review=expected_review)
            self.getTotalReviewPage()
            for page in range(0, expected_count + 1):
                page_no = page + 2
                current_url = self.driver.current_url
                new_url = current_url + "&page=" + str(page_no)
                comment.append([i.text for i in self.getComments()])
                ratings.append([i.text for i in self.getRatings()])
                cust_name_and_review_age = [i.text for i in self.getCustomerNamesAndReviewAge()]
                customer_name.append(
                    self.separateCustomernameAndReviewAge(list_of_custname_and_reviewage=cust_name_and_review_age)[0])
                review_age.append(
                    self.separateCustomernameAndReviewAge(list_of_custname_and_reviewage=cust_name_and_review_age)[1])
                self.openUrl(url=new_url)
            return ratings, comment, customer_name, review_age
        except Exception as e:
            # self.driver.refresh()
            raise Exception(
                f"(getReviewDetailsForProduct) - Something went wrong on getting details of review for the product.\n" + str(
                    e))

    def separateCustomernameAndReviewAge(self, list_of_custname_and_reviewage):
        """
        This function separates the review age and customer name.
        """
        try:
            customer_name = list_of_custname_and_reviewage[0::2]
            review_age = list_of_custname_and_reviewage[1::2]
            return customer_name, review_age
        except Exception as e:
            raise Exception(f"(separateCustomernameAndReviewAge) - Something went wrong.\n" + str(e))

    def generatingResponse(self, product_searched, product_name, price, discount_percent, offer_details, EMI, result):
        """
        This function generates the final response to send.
        """
        try:
            response_dict = {"product_searched": [], "product_name": [], "price": [], "discount_percent": [],
                             "offer_details": [], "EMI": [], "ratings": [], "comments": [], "customer_name": [],
                             "review_Age": []}
            rating, comments, cust_name, review_age = result[0], result[1], result[2], result[3]
            response_dict["ratings"] = rating
            response_dict["comments"] = comments
            response_dict["customer_name"] = cust_name
            response_dict["review_Age"] = review_age
            response_dict["product_name"] = product_name
            response_dict["product_searched"] = product_searched
            response_dict["offer_details"] = offer_details
            response_dict["EMI"] = EMI
            response_dict["price"] = price
            response_dict["discount_percent"] = discount_percent
            return response_dict
        except Exception as e:
            raise Exception(f"(generatingResponse) - Something went wrong on generating response")

    def generateDataForColumnAndFrame(self, response):
        """
        This function generates data for the column where only single data is presented. And then frames it in data frame.
        """
        try:
            data_frame1 = pd.DataFrame()
            flatten_rating = [j for i in response['ratings'] for j in i]
            for column_name, value in response.items():
                if column_name == 'product_searched' or column_name == 'product_name' or column_name == 'price' or column_name == 'discount_percent' or column_name == 'offer_details' or column_name == 'EMI':
                    list_value = []
                    for i in range(0, len(flatten_rating)):
                        list_value.append(response[column_name])
                    data_frame1.insert(0, column_name, list_value)
            print(data_frame1)
            return data_frame1
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def frameToDataSet(self, response):
        """
        This function frames the column to dataframe.
        """
        try:
            data_frame2 = pd.DataFrame()
            for column_name, value in response.items():
                if column_name == 'product_searched' or column_name == 'product_name' or column_name == 'price' or column_name == 'discount_percent' or column_name == 'offer_details' or column_name == 'EMI':
                    continue
                else:
                    flatten_result = [values for lists in response[column_name] for values in lists]
                    data_frame2.insert(0, column_name, flatten_result)
            return data_frame2
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def createDataFrameIncludingAllColumn(self, response):
        """
        This function creates dataframe from given data.
        """
        try:
            data_frame1 = self.generateDataForColumnAndFrame(response=response)
            data_frame2 = self.frameToDataSet(response=response)
            frame = [data_frame1, data_frame2]
            data_frame = pd.concat(frame, axis=1)
            return data_frame
        except Exception as e:
            raise Exception(f"(createDataFrame) - Something went wrong on creating data frame.\n" + str(e))

    def saveDataFrameToFile(self, dataframe, file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name)
        except Exception as e:
            raise Exception(f"(saveDataFrameToFile) - Unable to save data to the file.\n" + str(e))

    def closeConnection(self):
        """
        This function closes the connection
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"(closeConnection) - Something went wrong on closing connection.\n" + str(e))
