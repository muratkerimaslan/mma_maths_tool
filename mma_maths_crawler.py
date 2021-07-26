
import time
import requests
from bs4 import BeautifulSoup
from queue import Queue

###add timer, number of fighters/ pages visited, and maybe how many different weight divisons they have fought at (maybe),
def weight_class_finder(soup1,list_of_links,weight_classes):
    correct_table = soup1.find('table',class_="infobox vcard")
    if correct_table is not None:
        correct_table_rows = correct_table.find_all("tr")
        for row in correct_table_rows:
            if row.th is not None:
                if row.th.get_text() == "Division":
                    html_link_tags= row.td.find_all("a")
                    for x in html_link_tags:
                        if x.get("href") in list_of_links:
                            weight_classes.add(x.get_text())



def crawler_function(link1): ##starts from ben_askren
    set_of_visited = set()
    set_of_visited.add(link1)

    set_of_fighters = set()
    set_of_unclickable_fighters = set() ## fighters without a wikipedia page
    weight_classes_links = [
    '/wiki/Strawweight_(MMA)','/wiki/Flyweight_(MMA)','/wiki/Bantamweight_(MMA)','/wiki/Featherweight_(MMA)',
    '/wiki/Lightweight_(MMA)','/wiki/Welterweight_(MMA)','/wiki/Super_heavyweight_(MMA)','/wiki/Heavyweight_(MMA)',
    '/wiki/Light_heavyweight_(MMA)'
    ]
    links_queue = Queue(maxsize = 0)
    path = "Ben Askren > "
    first_link_element = [link1,0,path] ## 1st element is link, 2nd element is depth
    links_queue.put(first_link_element)
    new_file = open("ben_askren_mma_maths_tool.txt","w",encoding='utf-8')
    new_file2 = open("list_of_fighters_mma_maths.txt","w",encoding='utf-8')
    new_file3 = open("list_of_fighters_without_wikipedia_pages.txt","w",encoding='utf-8')
    new_file4 = open("list_of_fighters_with_wikipedia_pages.txt","w",encoding='utf-8')
    ## there is a new_file5, but i open it at the end of the while loop
    new_file6 = open("Weight_classes_of_fighters.txt","w",encoding='utf-8')
    
    set_of_weight_classes = set()
    set_of_weight_classes.add('Welterweight (170 lbs)')
    number_of_unique_fighters_by_depth = [0]*100
    number_of_visited_fighters = 1 ##synonymous with pages visited
    start_time = time.time()

    

    time_elapsed1 = 0
    while (links_queue.empty() is False):
        
        start_time1 = time.monotonic()

        current_element = links_queue.get()
        curr_link = current_element[0]
        curr_depth = current_element[1]
        curr_path = current_element[2]
        
        page = requests.get(curr_link)  ## there should be a catch try block if request.get(curr_link) is broken
        if page.status_code != 200:
            print("something went wrong with "+ curr_link +" status code is :" + str(page.status_code) )
          
        else:
            number_of_visited_fighters +=1
            print(str(page.status_code) + "opened the page " + curr_link + " no: " + str(number_of_visited_fighters) + " time elapsed is : " + str(time_elapsed1))
            
            
            soup = BeautifulSoup(page.content,"html.parser")
            length_of_title = len(soup.title.get_text())
            curr_fighters_name = soup.title.get_text()[0:length_of_title-12]
            new_file4.write("page : " + curr_link + " fighter's name : " + curr_fighters_name +" || " +str(curr_depth) +"\n")


            subsections_list = soup.find_all('h2')
            ### this part needs some work maybe, what if the records table doesn't exist,
            ## we should be able to handle this exception
            ## solution : wrap the remaining part of the loop with an if check
            table_exists = False
            for x in subsections_list:  
                
                if(x.span is not None and x.span['id'] == "Mixed_martial_arts_record"):
                    #print(x.span)
                    mma_record_table = x.find_next_siblings()[1] ## 2nd next is the table (usually)
                    if mma_record_table.tr is None or mma_record_table.tr.get_text() != '\nRes.\n\nRecord\n\nOpponent\n\nMethod\n\nEvent\n\nDate\n\nRound\n\nTime\n\nLocation\n\nNotes\n':
                        tables_list = soup.find_all('table')
                        for x in tables_list:
                            if x.tr.get_text() == '\nRes.\n\nRecord\n\nOpponent\n\nMethod\n\nEvent\n\nDate\n\nRound\n\nTime\n\nLocation\n\nNotes\n':
                                table_exists = True
                                mma_record_table = x
                    else:
                        table_exists = True
                    #print(alternate_mma_record_table.tr.contents)
            if (table_exists):
                ## weight class finder
                curr_number_of_weight_classes = len(set_of_weight_classes)
                weight_class_finder(soup,weight_classes_links,set_of_weight_classes)
                if len(set_of_weight_classes) > curr_number_of_weight_classes:

                    new_file6.write("New weight classes added, person who contributed is  : " + curr_fighters_name +"\n")
                    new_file6.write("Current weight classes are :" + str(set_of_weight_classes) + "\n\n\n")
                ## weight class finder
                mma_record_table_rows = mma_record_table.find_all('tr')
                number_of_rows = len(mma_record_table_rows)
                new_file.write("Depth = " + str(curr_depth)+"\n")
                new_file.write("Current path is :" + curr_path)
                new_file.write("\n")
                
                for i in range(1,number_of_rows):
                    
                    match_result = mma_record_table_rows[i].contents[1].get_text().strip('\n')
                    opponent = mma_record_table_rows[i].contents[5].get_text().strip('\n') 
                    if ( match_result  == 'Win'):
                        number_of_unique_fighters_by_depth[curr_depth] += 1 
                        new_file.write(curr_fighters_name + " won against " + opponent + " this is depth:" + str(curr_depth) + "\n")
                        if opponent not in set_of_fighters:
                            new_file2.write(opponent +"|| depth = " + str(curr_depth) +str()  +"\n")
                            set_of_fighters.add(opponent)
                        if (   mma_record_table_rows[i].contents[5].find('a') is not None and ## link to opponents page exists 
                               mma_record_table_rows[i].contents[5].find('a').get('href')[0:5] =='/wiki' ): ## in english wikipedia
                            
                            opponent_link = "https://en.wikipedia.org" + mma_record_table_rows[i].contents[5].find('a').get('href')
                            next_depth = curr_depth + 1
                            next_path = curr_path + opponent + " > "
                            next_link_element = [opponent_link,next_depth,next_path]
                            if opponent_link not in set_of_visited:
                                set_of_visited.add(opponent_link)
                                links_queue.put(next_link_element) ## 
                        else:
                            if opponent not in set_of_unclickable_fighters:
                                new_file3.write(opponent + " || depth =" + str(curr_depth) + " || parent is : "+ curr_fighters_name + "\n")
                                set_of_unclickable_fighters.add(opponent)

                            
                new_file.write("\n\n\n")
            time.sleep(0.75)
        end_time1 = time.monotonic()
        time_elapsed1 = end_time1 - start_time1
        
        

    end_time = time.time()
    time_elapsed = end_time - start_time
    print('time elapsed is = ' + str(time_elapsed))
    average_time = time_elapsed/number_of_visited_fighters
    print('average time for a page check is ' + str(average_time))
    print('Checked ' +  str(number_of_visited_fighters) + ' number of fighters wikipedia pages')



    new_file5 = open("mma_maths_tool_statistics.txt","w",encoding='utf-8')

    new_file5.write('time elapsed is = ' + str(time_elapsed) + '\n')
    new_file5.write('Checked ' +  str(number_of_visited_fighters) + ' number of fighters wikipedia pages')
    new_file5.write('average time for a page check is ' + str(average_time) + '\n')

    percentage_of_unclickable = len(set_of_unclickable_fighters)/  len(set_of_fighters) 
    new_file5.write("number of fighters without a clickable wikipedia page is : "+ str(len(set_of_unclickable_fighters)) + "\n")
    new_file5.write("number of all fighters is : " + str(len(set_of_fighters)) + "\n")
    new_file5.write('Percentage of fighters without a clickable wikipedia page is : ' +  str(percentage_of_unclickable) + "\n" )

    new_file5.write('number of unique fighters by each depth is : ' + "\n\n")
    
    for i in range(len(number_of_unique_fighters_by_depth)):
        if number_of_unique_fighters_by_depth[i] != 0:
            new_file5.write('number of unique fighters by depth ' + str(i+1) + " is " + str(number_of_unique_fighters_by_depth[i]) + "\n")
    
    new_file.close()
    new_file2.close()
    new_file3.close()
    new_file4.close()
    new_file5.close()
    new_file6.close()
##maybe Input could be taken from the console

crawler_function("https://en.wikipedia.org/wiki/Ben_Askren")