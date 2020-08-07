import requests
from bs4 import BeautifulSoup, Tag
import time
import lxml

def is_normal(tags):
    """ function to check if a link is normal (not in parentheses)

        Parameters:
            tags (list): A list with all the HTML tags in a praragraph

        Returns:
            returns a normal link or an empty string if no normal links are found
    """
    link = ''
    stack = []

    # loop through all tags
    for tag in tags:

        # add an element to the stack if there's an opening parentheses
        if '(' in tag:
            stack.append('(')

        # make the stack empty again if closing parentheses is reached
        if ')' in tag and len(stack) > 0:
            stack.pop()

        # check if the tag isn't in parentheses and has the appropriate name
        if isinstance(tag, Tag) and (tag.name == 'b' or tag.name == 'a') and len(stack) == 0:

            if tag.name == 'b':
                if tag.find('a') == None:
                    continue

                # normal link is found
                link = tag.find('a')['href']
                break
            else:
                # normal link is found
                link = tag['href']
                break
    return link

def find_link(link):
    """ function to find the first normal link in an article

        Parameters:
            link (url): A link to a wikipedia article

        Returns:
            returns a normal link
    """
    # parse through the page
    soup = BeautifulSoup(requests.get(link).content, 'lxml')

    # loop to find first paragraph that has links
    i = 0
    while soup.findAll('p')[i].find('a') == None or soup.findAll('p')[i].find('a').get('href') == None:
        i += 1

    link = ""
    # loop that checks each paragraph for normal links by calling a helper method
    while link == '':
        tags = soup.findAll('p')[i].children
        link = is_normal(tags)
        i += 1

    link = 'https://en.wikipedia.org/' + link

    time.sleep(0.5)
    return link

def run_program(link):
    """ keeps checking for normal links until it gets to philosophy or gets
    stuck in a loop

        Parameters:
            link (url): The first link used to start the program

            Returns:
                None
    """
    # list containing the pages visited
    history = []

    # loop through all normal links
    while True:
        # find the next link and print it
        link = find_link(link)
        print(link)

        # check if a loop has started
        if link in history:
            print('Page already seen. Aborting search')
            break

        history.append(link)

        # check if it got to philosophy
        if link == 'https://en.wikipedia.org//wiki/Philosophy':
            print("Got to philosophy")
            break

if __name__ == "__main__":
    link = 'https://en.wikipedia.org/wiki/Special:Random'
    run_program(link)
