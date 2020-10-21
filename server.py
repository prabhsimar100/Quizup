import socket
import sys
from _thread import *
from sys import getsizeof
import pickle


host =''
port = 8006
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


questions =["Sample Question 1","Sample Question 2","Sample question 3","Sample Question 4","Sample Question 5","Sample question 6","Sample Question 7","Sample Question 8","Sample Question 9","Sample Question 10"]
answers=['1','2','3','4','5','6','7','8','9','10']

try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))


s.listen(5)
print('Waiting for a connection.')


no_of_clients=0
agreements =0
total_questions = 0
players=[]
turn=0


def threaded_client(conn):
    global no_of_clients
    global agreements
    global total_questions
    ques_to_me=0
    my_score=0
    global players
    global turn
   
    client_info={}
    conn.send(str.encode(("You are player #{}\n").format(str(no_of_clients+1))))
    
    no_of_clients+=1
    if (no_of_clients>2):
        msg="**************Two players are already playing QUIZUP******************\n"
        conn.sendall(str.encode(msg))
        no_of_clients-=1
        conn.close()
    else :
        client_info["port"] = conn.getpeername()[1]
        
        conn.send(str.encode('Enter Username: !\n'))
        client_info["name"]=str(conn.recv(2048).decode('utf-8'))
        conn.send(str.encode(("Hey {} Welcome to QUIZUP!").format(client_info["name"])))
        
        
        conn.send(str.encode("Do you want to begin ? [y/n]\n"))

        if((conn.recv(2048))) == b'y\n':
            # Lets start quizzing !
            agreements+=1
            my_pos=len(players)
            players.append(conn)
            if (agreements == 1):
                conn.send(str.encode(("Please wait for the other player")))
                while True:
                    if (agreements == 2):
                        break

            print(agreements)
            conn.send(str.encode(("It starts now")))


            conn.send(str.encode(("Your position is {}\n").format(my_pos)))
            
            if (my_pos == 0):
            	other_pos =1
            else:
            	other_pos =0

            while True:
            	if(turn==my_pos):
            		ques_to_me+=1
            		conn.send(str.encode("\n"+questions[total_questions]))
            		
            		data = conn.recv(2048)
            		answer = data.decode('utf-8').rstrip()
            		
            		curr_ans=answers[total_questions]
            		if((answer)) == curr_ans:
            			conn.send(str.encode("Correct Answer!!\n"))
            			my_score+=10
            		else:
            			conn.send(str.encode(("Sorry that was incorrect!\n , correct answer is {}").format(curr_ans)))
            		total_questions+=1
            		
            		if (my_pos == 0):
            			turn =1
            		else:
            			turn =0
            	if (ques_to_me==4):
            		break
            conn.send(str.encode(("\nThanks for playing . Your final score is {}!\n").format(my_score)))
        else :
            conn.send(str.encode("\nThanks for visiting QUIZUP !!\n"))
        players.remove(conn)
        no_of_clients -= 1
        print("Number of existing clients : ",no_of_clients)
        conn.close()


while True:
    try:
        conn, addr = s.accept()
        print('connected to : '+addr[0]+':'+str(addr[1]))
        print("Hey\n")
        start_new_thread(threaded_client,(conn,))
    except KeyboardInterrupt as e:
        conn.close()
        sys.exit()

