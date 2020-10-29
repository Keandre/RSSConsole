from prettytable import PrettyTable
from feed import Feed
import webbrowser
import os

table = PrettyTable()
table.field_names = ["#", "Author", "Title"]

file_obj = open('links.txt')

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

for link_list in feed_objects:
    entire_feed += link_list.updated_feed

for i in range(len(entire_feed)):
    table.add_row([i+1, entire_feed[i].author, entire_feed[i]['title']])

print(table)

while True:
    choice = int(
        input("Which item would you like to view? Please pick a number. "))

    if choice == 0:
        break

    item_choice = entire_feed[choice - 1]

    print(
        f"\nYou've chosen [{item_choice['title']}] by [{item_choice.author}].")

    action = int(input("""Select an option.

    1) Pick another item.
    2) Open the link.
    3) Exit the program
    """))

    if action == 2:
        webbrowser.open(item_choice['link'])
    elif action == 3:
        break
    else:
        print("That's not a valid choice! Please pick again.")

file_obj.close()
