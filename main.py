from prettytable import PrettyTable
from feed import Feed, FeedItem, InvalidRSSError
import webbrowser
import os

table = PrettyTable()
table.field_names = ["#", "Author", "Title"]

file_obj = open('links.txt', 'r')

rsslinks = file_obj.readlines()

feed_objects = []

entire_feed = []

# Load all of the feeds

loading_sequence = "Loading feed [0/26]"
print(loading_sequence, end="")

for i in range(len(rsslinks)):
    link = rsslinks[i].replace('\n', "")
    loading_sequence = ('\b'*len(loading_sequence)) + \
        f"Loading feed [{i+1}/{len(rsslinks)}]"
    print(loading_sequence, end="", flush=True)
    feed_objects.append(Feed(link))
print("")

for feedobject in feed_objects:
    entire_feed += feedobject.updated_feed

for i in range(len(entire_feed)):
    table.add_row([i+1, entire_feed[i].author, entire_feed[i].title])

print(table)

while True:
    choice = int(
        input("Which item would you like to view? Please pick a number. "))

    if choice == 0:
        break
    if choice > len(entire_feed):
        choice = len(entire_feed)

    item_choice = entire_feed[choice - 1]

    print(
        f"\nYou've chosen [{item_choice.title}] by [{item_choice.author}].")

    action = int(input("""Select an option.

    1) Pick another item.
    2) Open the link.
    3) Add an RSS feed to the file!.  
    4) Exit the program
    """))

    if action == 2:
        webbrowser.open(item_choice.link)
    elif action == 3:
        user_link = input("Please enter the link here!")
        try:
            new_feed = Feed(user_link)
            with open("links.txt", "w") as f:
                f.write(user_link)
            entire_feed += new_feed.updated_feed
        except InvalidRSSError as i:
            print("The RSS link either isn't up to standard or you didn't provide an RSS link. Please select another item.")
    elif action == 4:
        break
    else:
        print("That's not a valid choice! Please pick again.")

file_obj.close()
