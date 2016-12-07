import vk
import os
from getpass import getpass
from time import sleep

count_of_last_posts=500
access_token=''

class GroupCache(object):
    """Create/search .usercache file. Add and get users from cache"""
    def __init__(self,nickname):
        self.nickname=nickname
        if os.path.exists('.'+self.nickname)==False:
            open('.'+self.nickname, "w")

    def exist_with_data(self):
        if os.path.exists('.'+self.nickname):
            with open('.'+self.nickname, 'r') as file:
                data=file.read()
                if data!='':
                    return True
        else:
            return False

    def add_group_list(self,groups_list):
        with open('.'+self.nickname, "a") as userscache:
            for group in groups_list:
                userscache.write(str(group)+'\n')

    def get_group_list(self):
        with open('.'+self.nickname, 'r') as file:
            group_list = [line.rstrip('\n') for line in file]
            for group in group_list:
                group=int(group)
        return group_list

    def remove_current_group_from_list(self):
        with open('.'+self.nickname, 'r') as file:
            group_list = [line.rstrip('\n') for line in file]
        del group_list[0]
        with open('.'+self.nickname, 'w') as file:
            for group in group_list:
                file.write(str(group)+'\n')


def listmerge(lstlst):
    all=[]
    for lst in lstlst:
      all.extend(lst)
    return all

def main():
    user_link=input('input user link: ')

    session = vk.Session(access_token)
    api = vk.API(session)

    short_name=user_link.split('/')[len(user_link.split('/'))-1]
    user=api.users.get(user_ids=short_name)
    user_id=user[0].get('uid')

    saveFile=GroupCache(short_name)

    if saveFile.exist_with_data():
        groups_list=saveFile.get_group_list()
    else:
        groups_list=api.groups.get(user_id=user_id)
        saveFile.add_group_list(groups_list)

    for group in groups_list:
        sleep(0.4)
        print(api.groups.getById(group_id=group)[0].get('name'))
        sleep(0.3)
        group_last_posts=[]
        iterations_count=int(count_of_last_posts/100)
        for counter in range(iterations_count):
            group_last_posts.append(api.wall.get(owner_id=-1*int(group),offset=counter*100, count=100))
        group_last_posts=listmerge(group_last_posts)
        for post in group_last_posts:
            sleep(0.4)
            if not(isinstance( post, int )):
                liked_people_list=api.likes.getList(type='post', owner_id=str(-1*int(group)),item_id=post.get('id'))
                if user_id in liked_people_list.get('users'):
                    sleep(1)
                    post_description=api.wall.getById(posts=str(-1*int(group))+'_'+str(post.get('id')))
                    print(post_description)
                    print('TEXT: '+post_description[0].get('text').replace('<br>','\n')+'\n')
                    sleep(1)
                    print('------------------------------------------------------------------------')
        saveFile.remove_current_group_from_list()


if __name__ == '__main__':
    main()