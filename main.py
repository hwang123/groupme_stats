from __future__ import print_function

# Local
from user import User
from group import Group
from api import get_messages
from files import save_messages, load_messages
from constants import UID_TO_NAME

# Libs
import numpy as np 
import math
from matplotlib import pyplot as plt 
import networkx as nx
from datetime import datetime

TOKEN = "l3WAcjQqqBglaCi4x56JYnlDDUtfoj8Qo3cCDBGW"  # replace this with your API token (get from GroupMe Website)
GROUP_ID = "19078032"  # replace this with your group ID

""" 
Make a single pass through the group messages, instantiating a Group as
well as a list of Users

@messages:
    A list of messages, which are objects returned from the GroupMe API v3
----------
:group
    A Group instance containing a list of time-stamped messages
:usermap
    An object mapping user IDs to User objects. Each of these Users stores a list of
    aliases, as well as a user ID
"""
def instantiate_users(messages):
    usermap = {}
    num_messages = len(messages)
    latest_timestamp = messages[0]['created_at']
    earliest_timestamp = messages[num_messages-1]['created_at']

    group = Group(earliest_timestamp, latest_timestamp)

    for i in range(len(messages) - 1, -1, -1):
        m = messages[i]

        uid = m['user_id']
        username = m['name']
        if uid not in usermap:
            user = User(uid)
            user.add_username(username)
            usermap[uid] = user
        else:
            usermap[uid].add_username(username)

    return (group, usermap)


def user_stats(messages, user_map, group):
    """Keys: (posts, likes_recieved, likes_given, wordcount, images, misspellings, kicked)"""
    return_map = user_map
    return_group = group

    for m in reversed(messages):
        ## Parse
        uid = m['user_id'] if m['user_id'] else ''
        text = m['text'] if m['text'] else ''
        likers = m['favorited_by'] if m['favorited_by'] else []
        ts = m['created_at'] if m['created_at'] else ''

        num_likes = len(likers)
        num_words = len(text.split(' '))

        if uid in likers:
            num_likes -= 1

        return_map[uid].add_message(text, num_likes, ts)
        group.add_message(text, num_likes, ts)

        for liker_id in likers:
            if uid != liker_id:
                return_map[liker_id].increment_likes_given(uid)

    return return_map, return_group

def show_likes_given(user_map):
    likes_given = list(reversed(sorted([(u.get_likes_given(), UID_TO_NAME[u.get_user_id()]) for u in user_map.values()])))

    likes = [l[0] for l in likes_given]
    users = [l[1] for l in likes_given]

    y_pos = np.arange(len(likes_given))

    fig = plt.figure(figsize=(70,10))

    plt.bar(y_pos, likes, align='center', alpha=0.5)
    plt.xticks(y_pos, users)
    plt.ylabel('Likes Given')
    plt.xlabel('Usernames')
    plt.title("Biggest Heart")
    plt.rcParams['xtick.labelsize'] = 8

    plt.show()

def show_likes_received(user_map):
    likes_received = list(reversed(sorted([(u.get_likes_received(), UID_TO_NAME[u.get_user_id()]) for u in user_map.values()])))

    likes = [l[0] for l in likes_received]
    users = [l[1] for l in likes_received]

    y_pos = np.arange(len(likes_received))

    fig = plt.figure(figsize=(70,10))

    plt.bar(y_pos, likes, align='center', alpha=0.5)
    plt.xticks(y_pos, users)
    plt.ylabel('Likes Received')
    plt.xlabel('Usernames')
    plt.title('Most Popular in the Friend Group')
    plt.rcParams['xtick.labelsize'] = 8

    plt.show()

def show_like_post_ratio(user_map, filter=0):
    likes_ratio = list(reversed(sorted([(u.get_likes_received()/u.get_num_messages(), UID_TO_NAME[u.get_user_id()], u.get_num_messages()) for u in user_map.values()])))

    filtered_likes_ratio = []
    for p in likes_ratio:
        num_mess = p[2]
        if num_mess >= filter:
            filtered_likes_ratio.append(p)

    likesPP = [l[0] for l in filtered_likes_ratio]
    users = [l[1] for l in filtered_likes_ratio]

    y_pos = np.arange(len(filtered_likes_ratio))

    fig = plt.figure(figsize=(70,10))

    plt.bar(y_pos, likesPP, align='center', alpha=0.5)
    plt.xticks(y_pos, users)
    plt.ylabel('Likes per Post')
    plt.xlabel('Usernames')
    plt.title('Chill to Pull (at least ' + str(filter) + ' posts)')
    plt.rcParams['xtick.labelsize'] = 8

    plt.show()

def show_num_posts(user_map):
    num_posts = list(reversed(sorted([(u.get_num_messages(), UID_TO_NAME[u.get_user_id()]) for u in user_map.values()])))

    posts = [l[0] for l in num_posts]
    users = [l[1] for l in num_posts]

    y_pos = np.arange(len(posts))

    fig = plt.figure(figsize=(70,10))

    plt.bar(y_pos, posts, align='center', alpha=0.5)
    plt.xticks(y_pos, users)
    plt.ylabel('Number of Posts')
    plt.xlabel('Usernames')
    plt.title('Most Gregarious')
    plt.rcParams['xtick.labelsize'] = 8

    plt.show()

def show_num_pop_posts(user_map):
    num_posts = list(reversed(sorted([(len(u.get_popular_messages()), UID_TO_NAME[u.get_user_id()]) for u in user_map.values()])))

    posts = [l[0] for l in num_posts]
    users = [l[1] for l in num_posts]

    y_pos = np.arange(len(posts))

    fig = plt.figure(figsize=(70,10))

    plt.bar(y_pos, posts, align='center', alpha=0.5)
    plt.xticks(y_pos, users)
    plt.ylabel('Number of Popular Posts (>10 likes)')
    plt.xlabel('Usernames')
    plt.title('Most Rousing')
    plt.rcParams['xtick.labelsize'] = 8

    plt.show()

def show_adjacency_graph(user_map, threshold = 0, weight_by_posts = False):
    adjacency_graph = {}
    # First sort users who have a reasonable amount of posts
    filtered_users = list(filter(lambda u: u.get_num_messages() >= threshold, user_map.values()))
    filtered_users = list(filter(lambda u: u.get_user_id() not in ['system', 'calendar'], filtered_users))

    # Go through all the users
    for user1 in filtered_users:
        uid1 = user1.get_user_id()
        for user2 in filtered_users:
            uid2 = user2.get_user_id() 
            map_key = (uid1, uid2) if uid1 > uid2 else (uid2, uid1)

            if uid1 != uid2 and map_key not in adjacency_graph:
                w1 = user1.get_like_map()[uid2] if uid2 in user1.get_like_map() else 0
                w2 = user2.get_like_map()[uid1] if uid1 in user2.get_like_map() else 0

                if weight_by_posts:
                    w1 = w1 / user2.get_num_messages()
                    w2 = w2 / user1.get_num_messages()

                adjacency_graph[map_key] = w1 + w2

    G = nx.Graph()

    max_weight = 0
    min_weight = 10000

    for edge in adjacency_graph:
        uid1 = edge[0]
        uid2 = edge[1]
        weight = adjacency_graph[edge]
        
        username1 = UID_TO_NAME[uid1]
        username2 = UID_TO_NAME[uid2]
        if weight > max_weight:
            max_weight = weight
            max_bros = (username1, username2)

        if weight < min_weight:
            min_weight = weight
            min_bros = (username1, username2)

        G.add_edge(username1, username2, weight=weight)


    # pos = nx.spring_layout(G)  # positions for all nodes
    # pos = nx.random_layout(G)  # positions for all nodes
    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=500)
    for edge in G.edges(data=True):
        w = edge[2]['weight']
        scaled_weight = 0.25 + 5*(w - min_weight)*(w/max_weight)/(max_weight-min_weight)

        edge_color = 'black'

        nx.draw_networkx_edges(G, pos, [edge], width=scaled_weight, connectionstyle='arc3,rad=0.2', edge_color=edge_color)


    # nodes = [u.get_most_recent_username() for u in filtered_users]
    # nx.draw_networkx_edges(G, pos, edgelist=G.edges(data=True), width=2)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')

    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # comment the following lines after first run
    messages = get_messages(GROUP_ID, TOKEN)
    save_messages(messages)

    # uncomment after first run to use saved messages
    # messages = load_messages()

    group, user_map = instantiate_users(messages)
    parsed_user_map, parsed_group = user_stats(messages, user_map, group)

    # parsed_group.show_historic_likes(50)
    # parsed_group.show_historic_posts(50)
    # show_likes_given(parsed_user_map)
    show_likes_received(parsed_user_map)
    # show_like_post_ratio(parsed_user_map, 0)
    show_like_post_ratio(parsed_user_map, 250)
    # show_num_posts(parsed_user_map)
    # show_num_pop_posts(parsed_user_map)
    # show_adjacency_graph(parsed_user_map, 250, True)