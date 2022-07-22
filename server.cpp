//Server Side Programming in C++ for Ultimate Connect 4
#include <iostream>
#include <string.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdlib.h>
#include <cstddef>
#include <cassert>
#include <fcntl.h>
#include "json.h"

#define MAX_CLIENTS 128
#define PORT 42069

using namespace std;

//match structure for easier mem management
struct client{
  int *fd;
  unsigned char buffer[128] = {0};
  int timeout = 25;
};

struct match{
  client host;
  client peer;
  int ID;
  bool isFull = 0;
};

//grabs matchid from the socket
client *find_match(int *sock, match *running, int num_matches){
      for(int i=0; i < num_matches; i++){
        if(running[i].host.fd == sock)
          return &running[i].peer;
        else if(running[i].peer.fd == sock){
          return &running[i].host;
        }
      }
  return NULL;
};

string recieve_json(int *to_read, unsigned char buffer[128]){
  string rcv = "";
  int size;
  while((size = recv(*to_read, buffer, 128, 0)) > 0){
    rcv = rcv + (char *)(buffer);
  }
  return rcv;
}

string read_msg_ret(struct json_value_s* root){
  struct json_object_s* object = json_value_as_object(root);

  struct json_object_element_s* m = object->start;

  struct json_value_s* msg = m->value;

  string buffer = (char *)json_value_as_string(msg);
  free(object);
  return buffer;
}

int *read_code_ret(struct json_value_s* root){
  struct json_object_s* object = json_value_as_object(root);

  struct json_object_element_s* m = object->start;
  struct json_object_element_s* c = m->next;

  struct json_value_s* msg = c->value;

  int *buffer = (int *)json_value_as_number(msg);
  free(object);
  return buffer;
}

int get_cnt_from_ID(int ID, match *running, int num_matches){
  for(int i = 0; i < num_matches; i++)
    if (running[i].ID == ID)
      return i;
  return -1;
}

//main server loop
int main(){

  //alloc memory for arrays
  struct pollfd toPoll[MAX_CLIENTS+1];
  match matches[MAX_CLIENTS/2];

  //instantiate random vars (this is why i like python)
  int match_cnt = 0;
  int sock_cnt = 1;
  int opt = 1;
  string decider;
  struct json_value_s* checker;
  int addto;
  unsigned char* temp_buff;
  //address
  struct sockaddr_in address;
  int addrlen = sizeof(address);


  //instantiate listener socket
  cout<<"Attempting Socket Connections..."<<endl<<endl;
  toPoll[0].fd = socket(AF_INET, SOCK_STREAM, 0);
  int *listener = &toPoll[0].fd;

  if(*listener == -1){
    cout<<"Socket Creation not Successful"<<endl;
    exit(1);
  }
  cout<<"Socket Creation was Successful"<<endl;

  //intiialize additional socket paramaters
  setsockopt(*listener, SOL_SOCKET, SO_REUSEADDR|SO_REUSEPORT, &opt, sizeof(opt));
  fcntl(*listener, F_SETFL, O_NONBLOCK);
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY;
  address.sin_port = htons(PORT);

  //initialize polling


  //bind the listener to the port (very nicely)
  int testBind = bind(*listener,(struct sockaddr *)&address,addrlen);
  if(testBind == -1){
    cout<<"Binding to Port "<<PORT<<" Failed"<<endl;
    exit(1);
  }
  cout<<"Binding to Port "<<PORT<<" Successful"<<endl;



  //server loop
  bool shutdown = 0;
  while(shutdown == 0){
    //start listening
    listen(*listener, 4);

    //accept incoming connections
    while ((toPoll[sock_cnt].fd = accept(*listener,(struct sockaddr*)&address, (socklen_t*)&addrlen))  <  0){
        //decide if host or peer and assign appropriately
        checker = json_parse(recieve_json(&toPoll[sock_cnt].fd, temp_buff), 1024);
        decider = read_msg_ret(checker);

        //assigns a new ID using the indexer if the new client is the host
        if(decider == "request_code"){
          matches[match_cnt].host.fd = &toPoll[sock_cnt].fd;
          match_cnt++;
        }


        //assigns the ID submitted if the new client is the peer and the match is not already full
        else if(decider == "send_code"){
          for(int i = 0; i < match_cnt; i++){
            addto = *read_code_ret(checker);
            matches[get_cnt_from_ID(addto, matches, match_cnt)].peer.fd = &toPoll[i].fd;
          }
        }
        else {
          cout<<"Game is Full"<<endl;
          }


      //  else{
      //    cout<<"Critical Error..."<<endl<<"Aborting"<<endl;
      //    exit(1);
      //  }

        free(checker);
        toPoll[sock_cnt].events = POLLIN;
        sock_cnt++;
        //add the socket to polling

      }

    //WIP
    //Loop through all the polled clients and see if they are sending data
    //Then send all the encoded bytes through to the matching client
    if(poll(toPoll, 1, 100) == 0)
      cout<<"Poll Timed Out"<<endl;
    else{
      for(int i = 1; i < sock_cnt; i++)
        //if polled event. needs syntax update
        if(toPoll[i].revents != 0){
          client *temp_peer, *temp_host;
          temp_peer = find_match(&toPoll[i].fd, matches, match_cnt);
          temp_host = find_match(temp_peer->fd, matches, match_cnt);
          string raw = recieve_json(temp_host->fd, temp_host->buffer);
          checker = json_parse(&raw, 1024);


            //check for msg type
          decider = read_msg_ret(checker);

          //send move
          if(decider == "move"){
            unsigned char toSend[raw.length()];
            memcpy(toSend, raw.data(), raw.length());
            send(*temp_peer->fd, toSend, raw.length(), 0);
          }

          //shutoff
          if(decider == ""){
            //free match and clients from memory

          }





        }
      }
    }
};
