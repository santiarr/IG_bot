import urllib.request
import os
import time
from selenium import webdriver
import random
import math

from selenium.common.exceptions import NoSuchElementException


class Bot():
    LIKE_LIMIT = 700
    COMMENT_LIMIT = 250
    canComment = True
    canLike = True
    notifiedCommentLim = False
    notifiedLikeLim = False
    logInNotVisible = False

    #Comments
    comment_list = ['This is so cool', 'Absolutely amazing!', 'So jealous', 'Where is this?', 'So awesome',
                    'This is so interesting', 'Actually really cool!', 'Loved this post', ' Keep the great content up, seriously #influencer',
                    'lol this is dope', 'Glad I checked this out!', 'This is actually super cool', 'hmmmmmm interesting..']


    #Initialize bot with desired settings
    def __init__(self, user, pw, tags, numlike=10, numcomment=10,topPosts=True, likenfollow=True):
        self.username = user
        self.pw = pw
        self.LIKE_LIMIT = int(numlike)
        self.COMMENT_LIMIT = int(numcomment)
        self.likes_left = self.LIKE_LIMIT
        self.comments_left = self.COMMENT_LIMIT
        # Hashtags to iterate through
        self.tags = tags
        self.driver = webdriver.Chrome(executable_path=r'C:\webdrivers\chromedriver.exe')
        self.login()
        if topPosts == True:
            self.goToTopPosts()
        if likenfollow == True:
            self.likenfollow()

    #Log into instagram
    def login(self):
        # Got to Instagram
        self.driver.get('https://www.instagram.com')
        time.sleep(4)
        # Click log in
        try:
            login = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[2]/p/a')
            login.click()
            time.sleep(2)
        except NoSuchElementException:
            self.logInNotVisible = True
            #Type username and password
            self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').click()
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(self.username)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').click()
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(
                self.pw)
            #Submit
            self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div').click()
            time.sleep(3)
        # Type username and password
        if not self.logInNotVisible:
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(
                self.username)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(self.pw)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()
            time.sleep(4)
            # Submit
            self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[3]/button[2]').click()
            time.sleep(2)

    # This function goes to the top posts in each tag and likes and comments.
    def goToTopPosts(self):
        #Set the number of rows of pictures to like and comment
        rows = []
        numrows = 3
        columns = []
        numcolumns = 3
        for i in range(numrows):
            rows[i] = i + 1
        for i in range(numcolumns):
            columns[i] = i + 1
        #Go to each hashtag in the hashtag array to like and comment
        for tag in self.tags:
            # Go to hashtags
            self.driver.get('https://www.instagram.com/explore/tags/' + tag)
            for row in rows:
                for column in columns:
                    #Click on the picture
                    self.driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/article/div[1]/div/div/div[{row}]/div[{column}]'.format(row=row,
                                                                                                                column=column)).click()
                    # Delay likes to reduce chances of being banned
                    time.sleep(random.randint(28, 36))
                    # Like post
                    self.driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
                    self.likes_left -= 1
                    time.sleep(2)
                    # Exit the post
                    self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()


    def likenfollow(self):


        numPostToLike = self.likes_left / len(self.tags)
        if self.COMMENT_LIMIT>3:
            rows = math.floor(numPostToLike / 3)
        else:
            rows = math.ceil(numPostToLike/3)
        columns = 3

        #Check if you have reached the comment limit

        if self.canComment or self.canLike:
            for tag in self.tags:
                # Go to hashtags

                self.driver.get('https://www.instagram.com/explore/tags/' + tag)
                #Click on the picture
                for row in range(rows):
                    for column in range(columns):
                        self.driver.find_element_by_xpath(
                            '/html/body/div[1]/section/main/article/div[2]/div/div[{row}]/div[{column}]'.format(row=row + 1,
                                                                                                                        column=column + 1)).click()
                        if not self.notifiedLikeLim:
                            if self.canLike:
                                # Delay likes to reduce chances of being banned
                                time.sleep(random.randint(28, 36))
                                # Like post
                                self.driver.find_element_by_xpath(
                                    '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
                                self.likes_left -= 1
                                if self.likes_left == 0:
                                    print('updating like limit')
                                    self.canLike = False

                                print(self.likes_left, self.canLike, self.LIKE_LIMIT)
                                time.sleep(4)
                            else:
                                print('Sorry, you have reached the like limit')
                                self.notifiedLikeLim = True
                                if self.canComment is False:
                                    self.driver.quit()

                        if not self.notifiedCommentLim:
                            if self.canComment:
                                # Comment on post
                                time.sleep(4)
                                try:
                                    self.driver.find_element_by_xpath(
                                        '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button').click()
                                except NoSuchElementException:
                                    pass
                                # Type
                                try:
                                    self.driver.find_element_by_xpath(
                                        '/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea').send_keys(
                                        self.comment_list[random.randint(0, len(self.comment_list) - 1)])
                                    time.sleep(4)
                                except NoSuchElementException:
                                    pass

                                #Submit
                                self.driver.find_element_by_xpath(
                                    '/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button').click()
                                self.comments_left -= 1
                                if self.comments_left == 0:
                                    print('updating comment limit')
                                    self.canComment = False
                                print(self.comments_left, self.canComment, self.COMMENT_LIMIT)
                                time.sleep(4)
                            else:
                                print('Sorry, you have reached the comment limit.')
                                self.notifiedCommentLim = True
                                if self.canLike is False:
                                    self.driver.quit()


                        time.sleep(2)
                        # Exit the post
                        self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()

