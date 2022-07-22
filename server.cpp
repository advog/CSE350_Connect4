//Server Side Programming in C++ for Ultimate Connect 4
#include <iostream>
#include <string.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdlib.h>
#include <json.h>

#define MAX_CLIENTS 128
#define PORT 42069

using namespace std;

//client structure for easier mem management
struct client{
  int socket;
  bytes buffer[128] = {0};
  int timeout = 25;
  int matchID;
  bool is_host;
};

struct match{
  client *host;
  client *peer;
};

//grabs the socket from the ID
int get_ID_from_socket(int *sock, client *active, int num_clients){
  for(int i = 0; i < num_clients; i++){
    if(active[i]->socket == sock){
      return active[i]->matchID;
    }
  }
  return -1;
};

string recieve_json(client *read){
  string rcv = "";
  ssize_t size;
  while(size = recv(read->socket, read->buffer, 128, 0)){
    rcv += (string)(read->buffer);
  }
  return rcv;
}

string read_msg_ret(struct json_value_s* root){
  struct json_object_s* object = json_value_as_object(root);
  assert(object != NULL);
  assert(object->length == 2);

  struct json_object_element_s* m = object->start;

  struct json_value_s* msg = m->value;

  string buffer = json_value_as_string(msg);
  free(object);
  return buffer;
}

int read_code_ret(struct json_value_s* root){
  struct json_object_s* object = json_value_as_object(root);
  assert(object != NULL);
  assert(object->length == 2);

  struct json_object_element_s* m = object->start;
  struct json_object_element_s* c = m->next;

  struct json_value_s* msg = c->value;

  int buffer = json_value_as_int(value);
  free(object);
  return buffer;
}

//main server loop
int main(){

  //instantiate indexers
  int clientIndexer = 0;
  int matchIndexer = 0;
  int ID_indexer = 0;
  int opt = 1;
  int decider;

  //define arrays using structs
  client all_clients[MAX_CLIENTS];
  match matches[MAX_CLIENTS/2];
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
  while(shutdown == 0){
    //start listening
    listen(listener, 4);

    //accept incoming connections
    while ((all_clients[clientIndexer].socket = accept(listener,(struct sockaddr*)&address, (socklen_t*)&addrlen))  <  0){
        //decide if host or peer and assign appropriately
        struct json_value_s* checker = jsonparse(recieve_json(&all_clients[clientIndexer]), 1024);
        decider = read_msg_ret(checker);


        //assigns a new ID using the indexer if the new client is the host
        if(decider == "request_code"){
          matches[ID_indexer]->host = &all_clients[clientIndexer];
          matches[ID_indexer]->host.matchID = ID_indexer;
          matches[ID_indexer]->host.is_host = 1;
          ID_indexer++;
        }


        //assigns the ID submitted if the new client is the peer and the match is not already full
        else if(decider == "send_code"){
          for(int i = 0; i < clientIndexer; i++){
            bool isFull = 0; //need function here
            int addto = read_code_ret(checker) && !isFull);
            matches[addto]->peer = &all_clients[i];
            matches[addto]->host.matchID = ID_indexer;
            matches[addto]->host.is_host = 0;
          }
        }
        else if(isFull){
          cout<<"Game is Full"<<endl;
          }


        else{
          cout<<"Critical Error..."<<endl<<"Aborting"<<endl;
          exit(1);
        }

        free(checker);

        //add the socket to polling
        toPoll[clientIndexer].fd = &clients[clientIndexer].socket;
        toPoll[clientIndexer].events = POLLIN;
        clientIndexer++;
      }

    //WIP
    //Loop through all the polled clients and see if they are sending data
    //Then send all the encoded bytes through to the matching client
    if(poll(toPoll, 1, 100) == 0)
      cout<<"Poll Timed Out"<<endl;
    else{
      for(int i = 0; i < clientIndexer; i++)
        //if polled event. needs syntax update
        if(toPoll[i].revents != 0){
          struct json_value_s* recieved = jsonparse(recieve_json(&toPoll[i]), 1024);
          if(matches[get_ID_from_socket(toPoll[i].socket)]->is_host){
            //check for msg type
            decider = read_msg_ret(recieved);

            if(decider == "move"){
              //send read_code_ret
            }

            if(read_msg_ret(recieved))


            //send buffer


          }
        }
    }
};
