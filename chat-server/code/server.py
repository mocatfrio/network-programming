import socket
from threading import *

#deklarasi server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Mengatur alamat ip dan port server
server_address = ('localhost', 14000)
print ('starting up on %s port %s' % server_address)
server.bind(server_address)
server.listen(10)

list_of_clients=[] #socket object client yang terkoneksi ke server
user_info=[] #informasi username dan password tiap pengguna
user_ip = {} #socket object tiap pengguna
online_users = []
grup_list = [] #daftar seluruh grup yang ada di server
grup_member = {} #daftar anggota setiap grup

#fungsi pengecek apakah client disconnect
def connection_check(message):
    if not message.decode("utf-8"):
        remove(client_socket)
        print("Connection to client lost")
        return True

#fungsi yang melayani tiap client
def serve_client(client_socket, address):
    client_socket.sendall(b"Welcome to the TCurah, #BUAT# to create account, #MASUK# to login to account")
    while True:
            #menerima perintah dari client (buat akun atau login)
            try:
                message = client_socket.recv(2048)
                if connection_check(message)  :
                    break
                print(message)
                if message.decode('utf-8').startswith("#BUAT#"):
                    buat_akun(client_socket)
                elif message.decode('utf-8').startswith("#MASUK#"):
                    masuk(client_socket)
                else :
                    client_socket.sendall(b"Invalid command, try again")
            except:

                continue
            finally:
                message = ''

def buat_akun(client_socket) :
    while True:
        #menerima username dan password baru dengan delimiter spasi
        client_socket.sendall(b"Enter username (space) password, or #EXIT# to cancel")
        message = client_socket.recv(512)

        if connection_check(message):
            return
        elif message.decode("utf-8").startswith("#EXIT#"):
            return
        try:
            new_username, new_password = message.decode('utf-8').split(" ")
        except :
            client_socket.sendall(b"Invalid username or password\n")
            continue
        #Mengecek apakah username sudah terpakai
        if any(new_username in user[0] for user in user_info)  :
            client_socket.sendall(b"Username already exist\n")
            continue
        else:
            break
    #memasukkan username dan password baru ke list
    user_info.append([new_username, new_password])
    message_to_client = "Account " + user_info[-1][0] + " created"
    client_socket.sendall(message_to_client.encode("utf-8"))
    return

def masuk(client_socket):

    while True:
        #menerima username dan password akun yang akan login dengan delimiter spasi
        client_socket.sendall(b"Enter username (space) password, or #EXIT# to cancel")
        message = client_socket.recv(512)
        if connection_check(message):
            return
        elif message.decode("utf-8").startswith("#EXIT#"):
            return
        try:
            username, password = message.decode('utf-8').split(" ")
        except:
            client_socket.sendall(b"Invalid username or password\n")
            continue

        #jika username dan password benar, simpan socket object tiap user
        if [username, password] in user_info:
            user_ip[username] = client_socket
            online_users.append(username)
            welcome_message = "Welcome, " + username
            client_socket.sendall(welcome_message.encode("utf-8"))
            break
        else:
            client_socket.sendall(b"Username or password incorrect\n")
            continue

    #menu utama setelah login
    while True :
        client_socket.sendall(b"\n#PRIBADI# to send personal message, #GRUP# to send group message or manage groups, "
                              b"\n#BROADCAST# to send message to all online users, #KELUAR# to exit")
        message = client_socket.recv(512)
        if connection_check(message):
            return
        if message.decode('utf-8').startswith("#PRIBADI#"): #untuk mengirim pesan pribadi
            pribadi(client_socket, username)
        elif message.decode('utf-8').startswith("#GRUP#"): #untuk mengelola dan mengirim pesan ke grup
            grup(client_socket, username)
        elif message.decode('utf-8').startswith("#BROADCAST#"): #mengirim pesan ke semua pengguna yang online
            broadcast(client_socket, username)
        elif message.decode("utf-8").startswith("#KELUAR#") :
            remove(client_socket)
            client_socket.close()
            client_process.stop()
            return
        else:
            client_socket.sendall(b"Invalid command")
            continue



def pribadi(client_socket, username) :
    while True:
        client_socket.sendall(b"Enter recipient username")
        for user in online_users:
             if user != username:
                user = "\n" + user
                user = user.encode("utf-8")
                client_socket.sendall(user)
        message = client_socket.recv(512)
        if connection_check(message):
            return
        recipient = message.decode("utf-8")
        if recipient in user_ip :
            sending_message = "Sending message to " + recipient + " #EXIT# to exit" "\nenter message:"
            client_socket.sendall(sending_message.encode("utf-8"))
            break
        elif message.decode("utf-8").startswith("#EXIT#"):
            return
        else:
            client_socket.sendall(b"Invalid recipient, try again\n")
            continue

    while True :
        message = client_socket.recv(2048)
        if connection_check(message):
            return
        elif message.decode("utf-8").startswith("#EXIT#"):
            break
        sent_message = "Sent message : " + message.decode("utf-8")
        client_socket.sendall(sent_message.encode("utf-8"))
        message = username + "#>" + message.decode("utf-8")

        recipient = user_ip[recipient]
        send_message(message, recipient)



def grup(client_socket, username) :

    while True :
        client_socket.sendall(b"#BUATGRUP# to create new group, #CHATGRUP# to send group message,"
                              b"\n#TAMBAHMEMBER# to add member to group, #EXIT# to return to main menu")
        #menerima perintah dari client (buat grup atau chat di grup)
        message = client_socket.recv(512)

        if connection_check(message):
            return

        if message.decode('utf-8').startswith("#BUATGRUP#"):
            client_socket.sendall(b"Enter group name")
            #create grup & nama grup
            message = client_socket.recv(512)
            if connection_check(message):
                return
            grup_name = message.decode("utf-8")
            grup_list.append(grup_name)
            grup_member[grup_name] = []
            grup_member[grup_name].append(username)

            client_socket.sendall(b"Choose member (one per line), #END# to finish adding members\n")
            #mencetak nama member yang bisa dimasukkan ke grup
            for user in user_info:
                if user[0] != username:
                    user_candidate = user[0] + "\n"
                    client_socket.sendall(user_candidate.encode("utf-8"))
            while True:
                #memasukkan member di dalam grup
                message = client_socket.recv(512)
                if connection_check(message):
                    return
                member_name = message.decode('utf-8')

                if any(member_name in user[0] for user in user_info) and member_name not in grup_member[grup_name]:
                    grup_member[grup_name].append(member_name)
                    successful_add = grup_member[grup_name][-1] + " successfully added"
                    client_socket.sendall(successful_add.encode("utf-8"))
                    continue

                elif member_name in grup_member[grup_name]:
                    client_socket.sendall(b"Member already in group")
                    continue

                elif message.decode('utf-8').startswith("#END#"):
                    break

                else:
                    client_socket.sendall(b"Invalid member or command")
                    continue

            #mencetak member dari grup yang sudah dibuat
            created_group = "Group " + grup_list[-1] + " created, with members :\n"
            client_socket.sendall(created_group.encode("utf-8"))
            for member in grup_member[grup_name]:
                member_name = member + "\n"
                client_socket.sendall(member_name.encode("utf-8"))


        elif message.decode("utf-8").startswith("#TAMBAHMEMBER#"):
            client_socket.sendall(b"Choose group")
            my_group = []
            # mencetak grup yang sudah tergabung
            for grup2 in grup_list:
                if username in grup_member[grup2]:
                    my_group.append(grup2)
                    grup2 = "\n" + grup2
                    client_socket.sendall(grup2.encode("utf-8"))

            message = client_socket.recv(512)
            if connection_check(message):
                return
            message = message.decode("utf-8")

            if message in my_group:
                selected_grup = message
                selected_grup_message = "Add member to group " + message + " #END# to finish or cancel\n"
                client_socket.sendall(selected_grup_message.encode("utf-8"))
            for user in user_info:
                if user[0] != username and user[0] not in grup_member[selected_grup]:
                    user_candidate = user[0] + "\n"
                    client_socket.sendall(user_candidate.encode("utf-8"))

            while True:
                #memasukkan member di dalam grup
                message = client_socket.recv(512)
                if connection_check(message):
                    return
                member_name = message.decode('utf-8')

                if any(member_name in user[0] for user in user_info) and member_name not in grup_member[selected_grup]:
                    grup_member[selected_grup].append(member_name)
                    successful_add = grup_member[selected_grup][-1] + " successfully added"
                    client_socket.sendall(successful_add.encode("utf-8"))
                    continue

                elif member_name in grup_member[selected_grup]:
                    client_socket.sendall(b"Member already in group")
                    continue

                elif message.decode('utf-8').startswith("#END#"):
                    break

                else:
                    client_socket.sendall(b"Invalid member or command")
                    continue

            created_group = "Group " + grup_list[-1] + " updated, with members :"
            client_socket.sendall(created_group.encode("utf-8"))
            for member in grup_member[selected_grup]:
                member_name = "\n" + member
                client_socket.sendall(member_name.encode("utf-8"))

        elif message.decode("utf-8").startswith("#CHATGRUP#"):
            #fungsi chat grup
            client_socket.sendall(b"Choose group recipient, #EXIT# to cancel")
            my_group = []
            #mencetak grup yang sudah tergabung
            for grup2 in grup_list:
                if username in grup_member[grup2] :
                    my_group.append(grup2)
                    grup2 = "\n" + grup2
                    client_socket.sendall(grup2.encode("utf-8"))

            while True :
                #memilih salah satu grup yang tergabung untuk dikirimi pesan
                message = client_socket.recv(512)
                if connection_check(message):
                    return
                message = message.decode("utf-8")

                if message in my_group:
                    selected_grup = message
                    selected_grup_message = "Sending message to " + message + " #EXIT# to exit\nenter message :"
                    client_socket.sendall(selected_grup_message.encode("utf-8"))
                    while True:
                        #menerima pesan untuk dikirimkan ke client lain dalam grup
                        message = client_socket.recv(2048)
                        if connection_check(message):
                            return
                        message = message.decode("utf-8")
                        if message.startswith("#EXIT#"):
                            return
                        message = username+" ("+selected_grup+") " +"#>"+message
                        send_list = []
                        #membuat daftar user yang akan dikirimi dalam grup
                        for recipients in grup_member[selected_grup] :
                            if recipients in user_ip and recipients != username:
                                send_list.append(user_ip[recipients])
                        #mengirim pesan ke seluruh user yang ada di daftar kirim
                        for recipient in send_list:
                            send_message(message, recipient)


                elif message.startswith("#EXIT#"):
                    break
                else:
                    client_socket.sendall(b"Invalid group name")
                    continue

        elif message.decode("utf-8").startswith("#EXIT#"):
            return

        else :
            client_socket.sendall(b"Invalid Command\n")
            continue


def send_message(message, recipient):
    try :
        recipient.sendall(message.encode("utf-8"))
    except :
        recipient.close()
        remove(recipient)


def broadcast(client_socket, username):
    client_socket.sendall(b"Enter broadcast message, #EXIT# to cancel")
    message = client_socket.recv(2048)
    if connection_check(message):
        return
    message = message.decode("utf-8")
    if message.startswith("#EXIT#") :
        return
    message = username +"(broadcast)" + "#>" + message
    print(message)
    for clients in list_of_clients:
        if clients != client_socket:
            try:
                clients.send(message.encode("utf-8"))
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
    for clients in user_info:
        if user_ip[clients[0]] == connection:
            del user_ip[clients[0]]
            if clients[0] in online_users:
                online_users.remove(clients[0])


while True:
    client_socket, address = server.accept()

    list_of_clients.append(client_socket)
    print (address[0] + " connected")

    client_process = Thread(target = serve_client,args = (client_socket,address))
    client_process.start()


client_socket.close()
server.close()