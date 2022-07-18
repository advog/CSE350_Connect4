//Server Side Programming in C++ for Ultimate Connect 4
#include <iostream>
#include <string.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <poll.h>
#include<stdlib.h>

#define MAX_CLIENTS 128
#define PORT 42069

using namespace std;

//client structure for easier mem management
struct client{
  int socket;
  char buffer[1024] = {0};
  int ID;
  int timeout = 25;
};

struct match{
  client host;
  client peer;
};

//grabs the socket from the ID
int get_match_from_ID(int dummy, match* running, int num_matches)
{
  for(int i = 0; i < num_matches; i++){
    if(running[i].host.ID == dummy){
      return i;
    }
  }
};

//main server loop
int main()
{

  //instantiate indexers
  int clientIndexer = 0;
  int matchIndexer = 0;
  int ID_indexer = 0;
  int opt = 1;
  int decider;

  //define arrays using structs (needs fixing for pointers)
  client all_clients[MAX_CLIENTS];
  match *matches[MAX_CLIENTS/2];
  struct sockaddr_in address;
  int addrlen = sizeof(address);

  //instantiate listener socket
  cout<<"Attempting Socket Connections..."<<endl<<endl;
  int listener = socket(AF_INET, SOCK_STREAM, 0);
  if(listener == -1){
    cout<<"Socket Creation not Successful"<<endl;
    exit(1);
  }
  cout<<"Socket Creation was Successful"<<endl;

  //intiialize additional socket paramaters
  setsockopt(listener, SOL_SOCKET, SO_REUSEADDR|SO_REUSEPORT, &opt, sizeof(opt));
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY;
  address.sin_port = htons(PORT);

  //initialize polling
  struct pollfd toPoll[MAX_CLIENTS];

  //bind the listener to the port (very nicely)
  int testBind = bind(listener,(struct sockaddr *)&address,addrlen);
  if(testBind == -1){
    cout<<"Binding to Port "<<PORT<<" Failed"<<endl;
    exit(1);
  }
  cout<<"Binding to Port "<<PORT<<" Successful"<<endl;

  //server loop
  bool shutdown = 0;
  while(shutdown == 0)
  {
    //start listening
    listen(listener, 4);

    //accept incoming connections
    while ((all_clients[clientIndexer].socket = accept(listener,(struct sockaddr*)&address, (socklen_t*)&addrlen))  <  0){
        //decide if host or peer and assign appropriately
        decider = recv(all_clients[clientIndexer].socket, &all_clients[clientIndexer].buffer, 1024, 0);
        char oogle[1024] = "-1";

        //assigns a new ID using the indexer if the new client is the host
        if(all_clients[clientIndexer].buffer == oogle){
          all_clients[clientIndexer].ID = ID_indexer;
          matches[0]->host = all_clients[clientIndexer];
          ID_indexer++;
        }

        //assigns the ID submitted if the new client is the peer and the match is not already full
        else{
          int checker = 0;
          for(int i = 0; i < clientIndexer; i++){
            if(all_clients[i].ID == decider && checker == 0){
              checker = 1;
              matches[0]->peer = all_clients[i];
            }
            else if(checker == 1){
              cout<<"Game is Full"<<endl;
            }
          }
        }

        //add tne socket to polling
        toPoll[clientIndexer].fd = 0;
        toPoll[clientIndexer].events = POLLIN;
        clientIndexer++;
    }
    if(poll(toPoll, 1, 2500) == 0){
    cout<<"Poll Timed Out"<<endl;
    }
    else{
      if(toPoll[0].revents && POLLIN){
        cout<<"poopoo";
      }
    }
  }
};
