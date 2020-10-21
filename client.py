import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('[::]')
    sys.stdout.flush()
 

if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print ('Example : python client.py hostname port')
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
   
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()
     
    print ('Connected to remote host. Start playing QUIZUP!')
    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
       
        try:
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        except KeyboardInterrupt as e:
         
            sys.exit()
        
         
        for sock in read_sockets:
           
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from the Quizup server, thank you for playing!')
                    sys.exit()
                else :
                  
                    sys.stdout.write(data.decode("utf-8"))
                    prompt()
             
            
            else :
                msg = sys.stdin.readline()
                s.send(str.encode(msg))
                prompt()