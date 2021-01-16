from prettytable import PrettyTable
from feed import Feed, FeedItem, InvalidRSSError, feedparser
import webbrowser
import os
from googleapiclient.discovery import build
import argparse

def date_sort(a):
    return a.date

def addlink(user_link, arr):
    try:
        new_feed = Feed(user_link)
        with open("links.txt", "a") as f:
            f.write(user_link)
            arr += new_feed.updated_feed
    except InvalidRSSError:
        print("The RSS link either isn't up to standard or you didn't provide an RSS link. Please select another item.")

def remove_duplicate_lines():
  rss_links = []
  with open('links.txt','r') as f:
    rss_links = f.read().splitlines()
  rss_links = list(dict.fromkeys(rss_links))
  with open('links.txt','w') as f:
    for link in rss_links:
      f.write(link+"\n")

def get_yt_request(query):
    api_key = 'AIzaSyDmgOE8NNnt5XFSoj8tGmkKqOXFA6hhVQY'
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(q=query, part="snippet",
                                    type="channel", maxResults=10)
    return request

def check_duplicate(link):
    with open('links.txt', 'r') as f:
        rsslinks = f.read().splitlines()
        return link in rsslinks

def generate_feed(loading=False, column=False):

    feed_objects = []
    entire_feed = []
    rsslinks = None
    remove_duplicate_lines()
    with open('links.txt', 'r') as f:
        rsslinks = f.read().splitlines()

    if loading:
        loading_sequence = "Loading feed [0/26]"
        print(loading_sequence, end="")

    try:
        for i in range(len(rsslinks)):
            link = rsslinks[i]
            if loading:
                loading_sequence = ('\b'*len(loading_sequence)) + \
                    f"Loading feed [{i+1}/{len(rsslinks)}]"
                print(loading_sequence, end="", flush=True)
            feed_objects.append(Feed(link))
        print("")

        for feed_object in feed_objects:
            entire_feed += feed_object.updated_feed
    except InvalidRSSError:
        print("One of the RSS links either aren't up to standard or isn't valid.")
    return entire_feed


def generate_feed_table(feed_arr):
    table = PrettyTable()
    table.field_names = ["#", "Author", "Title"]

    for i in range(len(feed_arr)):
        table.add_row([i+1, feed_arr[i].author, feed_arr[i].title])
    return table

def generate_author_list():
    rsslinks = None
    author_str = ""
    with open('links.txt','r') as f:
        rsslinks = f.read().splitlines()
    for i in range(len(rsslinks)):
        author = feedparser.parse(rsslinks[i])['feed']['title']
        author_str += "{}. {}\n".format(i+1, author)
    return author_str

def delete_specific_feed(number):
    lines = None 
    with open("links.txt", "r") as f:
        lines = f.read().splitlines()
    with open("links.txt", "w") as f:
        for line in lines:
            if line != lines[number]:
                f.write(line+"\n")

entire_feed = generate_feed(True)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',action='store_true', default=False, dest='author',help="Sort by author.")
    args = parser.parse_args()

    if not args.author:
        entire_feed.sort(key=date_sort)
        entire_feed.reverse()


table = generate_feed_table(entire_feed)
while True:
    menu_action = int(input("""Select an option.

    1) View your feed and pick an item.  
    2) Add an RSS feed to the file!  
    3) Delete a feed 
    4) Exit the program
    """))
    if menu_action == 1:
        print(table)

        while True:
            if len(entire_feed) == 0:
                print("Unfortunately, there are no new items for you to view!")
                break
            choice = int(
                input("Which item would you like to view? Please pick a number. "))

            if choice == 0:
                break
            if choice > len(entire_feed):
                choice = len(entire_feed)

            item_choice = entire_feed[choice - 1]

            print(
                f"\nYou've chosen [{item_choice.title}] by [{item_choice.author}].")

            choice_action = int(input("""What would you like to do?
            
            1) Open the link.
            2) Pick another item.
            3) Go back to the main menu! 
            """))
            if choice_action == 1:
                webbrowser.open(item_choice.link)
            elif choice_action == 3:
                break

    elif menu_action == 2:
        choice = int(input("Please tell us which type of RSS feed you'd like:\n1) Manual Link\n2) YouTube channel\n"))
        if choice==1:
            user_link = input("Please enter the link here!")
            if not check_duplicate(user_link):
                addlink(user_link, entire_feed)
            else:
                print("You already have that RSS feed!")
        elif choice == 2:
            youtube_table = PrettyTable()
            youtube_table.field_names = ['#', 'Channel Name', 'Description']
            query = input("Please enter your query! ")
            request = get_yt_request(query)
            result = request.execute()
            for i in range(len(result)):
                content = result['items'][i]['snippet']['title']
                description = result['items'][i]['snippet']['description']
                youtube_table.add_row([i+1, content, description])
            print(youtube_table)
            number = int(
                input("Which channel would you like to add to your RSS feed? "))
            new_youtube_feed = f"https://www.youtube.com/feeds/videos.xml?channel_id={result['items'][number - 1]['snippet']['channelId']}"
            if not check_duplicate(new_youtube_feed):
                addlink(new_youtube_feed, entire_feed)
                entire_feed = generate_feed(True)
                table = generate_feed_table(entire_feed)
                print("The feed has been updated!")
            else:
                print("You already have that YouTube channel in your feed!")
    elif menu_action == 3:
        print("What feed would you like to delete?")
        number = int(input(generate_author_list()+"\n")) - 1
        delete_specific_feed(number)
        entire_feed = generate_feed(True)
        table = generate_feed_table(entire_feed)
        print("The feed has been updated!")
    elif menu_action == 4:
        break
    else:
        print("That's not a valid choice! Please pick again.")
