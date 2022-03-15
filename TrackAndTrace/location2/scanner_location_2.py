import socket
import calendar
import time
import datetime
import csv

# create a  socket instance and AF_INET refers to the address family ipv4. The SOCK_STREAM means connection oriented TCP protocol.

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connection created successfully \n")
    print("Listening to Reader-2 ...\n")
except socket.error as err:
    print("socket creation failed with error %s" % (err))

ip_address = '192.168.xxx.xx'
port = 23
    
# connecting to the Reader
client_socket.connect((ip_address, port))

# END CODE after each station id and component id has been scanned
END = b"END_ITERATOR"

# END CODE for after finishing all the scanning
FINISH = b"TERMINATOR"
# Final variable list with 4 variable values (Station ID, timestamp, Component ID, timestamp)
valList = []

timestr = time.strftime("%Y%m%d-%H%M%S")
csvf_path = "C:\\xxx\\TrackAndTrace\\location2\\"+"2_"+timestr+"_logger.csv"

# CSV file
file_csv = open(csvf_path, "a")

# Loop to continue scanning
while 1:
    # Read the data from scanner (telnet)
    data = client_socket.recv(512)

    # Check if the scanned code is FINISH CODE
    if (data == FINISH):
        client_socket.close()
        file_csv.close()
        break;

    # Check if the scanned code is END CODE
    if (data == END):
        
        # If valList has 4 values then send data to OPCUA server
        if (len(valList) == 4):
            print("Writing", len(valList), " in CSV file")

            # append data in CSV file
            for i in range(0, len(valList)): 
                if (i == (len(valList)-1)) :
                    file_csv.write(str(valList[i]))
                else :    
                    file_csv.write(str(valList[i]) + ',')
            file_csv.write("\n")   

            # reset the varList
            valList.clear()
            continue;
        else :
            valList.clear()
            continue;

    # Received Station ID then Received Component ID and append it to List
    valList.append(data)

    # Get Current Timestamp and append it to List
    timestamp = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).isoformat()
    valList.append(timestamp)
    print(valList)
