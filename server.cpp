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
#define PORT 65432

using namespace std;

//match structure for easier mem management
struct client{
  int *fd;
  char buffer[1024] = {0};
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

string recieve_json(int *to_read, char *buffer){
  size_t total = 0, n = 0;
  string returnString = "";
  while((n = recv(*to_read, buffer, sizeof(buffer)-total-1, 0)) > 0){
    //problem is here as u can see ive attempted to handle it a few ways
      total += n;
      returnString = returnString + buffer[n];
      cout<<n<<endl;
      //^will only print once usually
  }
  cout<<buffer<<endl;
  buffer[total] = 0;
  return returnString;
}

string read_msg_ret(struct json_value_s* root){
  struct json_object_s* object = json_value_as_object(root);

  struct json_object_element_s* m = object->start;

  struct json_value_s* msg = m->value;

  return (char *)json_value_as_string(msg);
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
  struct json_value_s* parsed;
  int addto;
  char temp_buff[1024];
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
    listen(*listener, 10);

    //accept incoming connections
    while ((toPoll[sock_cnt].fd = accept(*listener,(struct sockaddr*)&address, (socklen_t*)&addrlen))  >  0){
        cout<<"One on the Line"<<endl;

        //decide if host or peer and assign appropriately
        string raw_json = recieve_json(&toPoll[sock_cnt].fd, temp_buff);
        parsed = json_parse(&raw_json, 1024);
        decider = read_msg_ret(parsed);
        cout<<raw_json<<endl;

        //assigns a new ID using the indexer if the new client is the host
        if(decider == "request_code"){
          matches[match_cnt].host.fd = &toPoll[sock_cnt].fd;
          matches[match_cnt].ID = match_cnt + 1;
          match_cnt++;
        }


        //assigns the ID submitted if the new client is the peer and the match is not already full
        else if(decider == "send_code"){
          for(int i = 0; i < match_cnt; i++){
            addto = *read_code_ret(parsed);
            if(!matches[get_cnt_from_ID(addto, matches, match_cnt)].isFull){
              matches[get_cnt_from_ID(addto, matches, match_cnt)].peer.fd = &toPoll[i].fd;
              cout<<"Client assigned to existing match"<<endl;
              matches[get_cnt_from_ID(addto, matches, match_cnt)].isFull = 1;
            }
          }
        }
        else {
          cout<<"Error Connecting Client to a Match"<<endl;
          }

        free(parsed);
        toPoll[sock_cnt].events = POLLIN;
        sock_cnt++;
        //add the socket to polling

      }

    //WIP
    //Loop through all the polled clients and see if they are sending data
    //Then send all the encoded bytes through to the matching client
    if(poll(toPoll, 1, 250) != 0){
      for(int i = 1; i < sock_cnt; i++)
        //if polled event. needs syntax update
        if(toPoll[i].revents != 0){
          client *temp_peer, *temp_host;
          temp_peer = find_match(&toPoll[i].fd, matches, match_cnt);
          temp_host = find_match(temp_peer->fd, matches, match_cnt);
          string raw = recieve_json(temp_host->fd, temp_host->buffer);
          parsed = json_parse(&raw, 1024);


            //check for msg type
          decider = read_msg_ret(parsed);

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
