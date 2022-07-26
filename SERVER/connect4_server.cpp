#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <netinet/in.h>
#include <sstream>
#include <ostream>
#include <string>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <tuple>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <time.h>

#include <cstring>
#include <iostream>
#include <vector>
#include <memory>
#include <sstream>

#include "json.hpp"


bool set_socket_blocking(int fd, bool blocking);

///////const values///////
const int PORT = 5007;
const int timeout = 30;

///////typedef///////
typedef std::string string;
typedef unsigned char byte;
typedef nlohmann::json json;

///////class defs///////
class msg {
public:
  nlohmann::json js;
  uint64_t client_id;

  msg(uint64_t id, nlohmann::json j){
    js = j;
    client_id = id;
  }
};

class client {
public:
  uint64_t client_id;
  uint64_t opponent_id;
  uint64_t match_id;

  int socket_fd;
  std::vector<byte> buf;

  time_t timout;

  byte state;
  
  client(int fd, uint64_t id){
    client_id = id; //client_id for identification
    socket_fd = fd; //socket_fd used by linux
    set_socket_blocking(socket_fd, false); //set socket to non_blocking
    timout = time(NULL); //set timeout to current time
    state = 0; //new, waiting, matched
    opponent_id = 0; //client_id of opponent
    match_id = 0;
  }
};

///////globals///////
bool request_shutdown = false;
uint64_t id_counter = 100000;

//listener
int listener_fd;

//client buckets
std::vector<client*> clients;

//clients to be closet
std::vector<uint64_t> closed_ids;

//msg queues
std::vector<msg> in_queue;
std::vector<msg> out_queue;

///////utility///////
uint64_t request_id(){return id_counter++;}
void println(string s){std::cout << s << std::endl;}

///////interrupts///////
void interrupt_handler(int SIG) {
  println("interrupt signal sent");
  request_shutdown = true;
}
void close_handler(int SIG) {}

///////client utility///////
int cleanup_client(int index) {
  close(clients[index]->socket_fd);
  delete clients[index];
  clients.erase(clients.begin()+index);
  return 0;
}

int find_client_index_from_id(uint64_t id){
  for (int i = 0; i < clients.size(); i++) {
    if (clients[i]->client_id == id){
      return i;
    }
  }
  return -1;
}

int find_client_index_from_match(uint64_t id) {
   for (int i = 0; i < clients.size(); i++) {
     std::cout << clients[i]->match_id << " "<< id <<std::endl;
     if (clients[i]->match_id == id){
       return i;
     }
  }
  return -1;
}

bool check_timout(client* c_p){
  return ((time(NULL) - c_p->timout) > timeout);
}

///////socket utility///////
bool set_socket_blocking(int fd, bool blocking)
{
   if (fd < 0) return false;
   int flags = fcntl(fd, F_GETFL, 0);
   if (flags == -1) return false;
   flags = blocking ? (flags & ~O_NONBLOCK) : (flags | O_NONBLOCK);
   return (fcntl(fd, F_SETFL, flags) == 0) ? true : false;
}

int force_send_socket(int socket_fd, const char* data, int length){
  int sent = 0;
  while(sent != length){
    int tmp = write(socket_fd, data, length - sent);
    if(tmp < 0){return 0;} //socket closed, return false
    sent += tmp;
  }
  return 1; //data sent, return true
}

///////msg_handler///////
int handle_msg (msg m){
  int c_index = find_client_index_from_id(m.client_id);
  if(c_index == -1){return -1;}
  client* c_p = clients[c_index];
  //set client to waiting status and send back match_id
  if(m.js["msg"] == "request_code" && c_p->state == 0){
    c_p->match_id = request_id();
    c_p->state = 1;
    json ret;
    ret["msg"] = "send_code";
    ret["code"] = c_p->match_id;
    out_queue.push_back(msg(m.client_id, ret));
    std::cout << "recieved: " << m.js.dump() << std::endl;
    return 0;
  }
  if(m.js["msg"] == "send_code" && c_p->state == 0){
    uint64_t m_id = m.js["code"];
    int o_index = find_client_index_from_match(m_id);
    std::cout << m_id << " " << o_index << std::endl;
    client* o_p = clients[o_index];
    if(o_index != -1 && o_p->state == 1){
      //update state of hosting client
      o_p->state = 2;
      o_p->opponent_id = c_p->client_id;
      //update state of connecting client
      c_p->state = 2;
      c_p->match_id = m_id;
      c_p->opponent_id = o_p->client_id;
      //send begin game msg
      json ret;
      ret["msg"] = "start";
      out_queue.push_back(msg(c_p->client_id, ret));
      out_queue.push_back(msg(o_p->client_id, ret));
      std::cout << "recieved: " << m.js.dump() << std::endl;
      return 0;
    }
    //close connecting client b/c there is not opponent
    else{
      closed_ids.push_back(c_p->client_id);
    }
  }
  if(m.js["msg"] == "move" && c_p->state == 2){
      std::cout << "recieved: " << m.js.dump() << std::endl;
      out_queue.push_back(msg(c_p->opponent_id, m.js));
    }
  
  return -1;
}

int send_msg(msg m) {
  int c_index = find_client_index_from_id(m.client_id);
  client* c_p = clients[c_index];
  string s = m.js.dump();
  std::cout << "sent: " << m.js.dump() << std::endl;
  return force_send_socket(c_p->socket_fd, s.c_str(), s.size());
}

///////main///////
int main(void) {
  byte buffer[1024];
  
  //create listener socket
  listener_fd = socket(AF_INET, SOCK_STREAM, 0);
  if(listener_fd == -1){println("failed to create socket"); return 1;}
  else{println("created socket");}

  //create listener addr
  sockaddr_in listener_sockaddr_in;
  listener_sockaddr_in.sin_addr.s_addr = htonl(INADDR_ANY);
  listener_sockaddr_in.sin_port = htons(PORT);
  listener_sockaddr_in.sin_family = AF_INET;

  //bind listener socket
  int sys_result = bind(listener_fd, (sockaddr*)&listener_sockaddr_in, sizeof(sockaddr_in));
  if(sys_result == -1){println("failed to bind socket"); close(listener_fd); return 2;}
  else{println("binded socket");}

  //set begin listening
  sys_result = listen(listener_fd, 5); 
  if(sys_result == -1){println("you dont listen!"); close(listener_fd); return 3;}
  else{println("socket listening");}

  //set listener to nonblocking
  sys_result = set_socket_blocking(listener_fd, false);
  if(sys_result == false){println("falied to set socket as nonblocking"); close(listener_fd); return 4;}
  else{println("socket set to nonblocking");}
  
  //bind sigint to signal_handler
  signal(SIGINT, interrupt_handler);
  signal(SIGPIPE, close_handler);

  //begin server loop
  while(request_shutdown == false){

    //listen for new connections, add them to new_connections_fds
    while(true){
      sockaddr asker_sockaddr = {0};
      socklen_t asker_sockaddr_len = sizeof(asker_sockaddr);
      int asker = accept(listener_fd, &asker_sockaddr, &asker_sockaddr_len);
      //if socket is valid make it into client and dd it to clients
      if(asker != -1){
	client* tmp = new client(asker, request_id());
	clients.push_back(tmp);
	println("_new connection");
      }
      else{break;} //else there are no more clients to add
    }

    usleep(100);
    
    //load data from sockets
    for (int i = 0; i < clients.size(); i++) {
      client* c_p = clients[i];
      int tmp = read(c_p->socket_fd, buffer, 1024);
      if(tmp > 0){
	for(int j = 0; j < tmp; j++){
	  c_p->buf.push_back(buffer[j]);
	}
	c_p->timout = time(NULL);
      }
      //if the cur time is timout greater than the last time this socket has provided data then it has timed out
      else if(check_timout(c_p)){
	closed_ids.push_back(c_p->client_id);
      }
    }
    
    usleep(100);
    
    //parse messages and append them to queue
    for (int i = 0; i < clients.size(); i++){
      client* c_p = clients[i];
      int brackets = 0;
      for (int j = 0; j < c_p->buf.size(); j++) {
	if(c_p->buf[j] == '{'){ brackets++;}
	else if(c_p->buf[j] == '}'){
	  brackets--;
	  if(brackets == 0){
	    string s(c_p->buf.begin(), c_p->buf.begin()+j+1);
	    c_p->buf.erase(c_p->buf.begin(), c_p->buf.begin()+j+1);
	    in_queue.push_back(msg(c_p->client_id, json::parse(s)));
	    j = 0;  
	  }
	}
      }
    }

    //handle in_queue
    for (int i = 0; i < in_queue.size(); i++) {
      std::cout << in_queue[i].js.dump() << std::endl;
      handle_msg(in_queue[i]);
    }
    in_queue.clear();

    //send out_queue
    for (int i = 0; i < out_queue.size(); i++) {
      int res = send_msg(out_queue[i]);
      if(res != 0){
	println("error on send");
      }
    }
    out_queue.clear();

    //removed closed sockets
    for (int j = 0; j < closed_ids.size(); j++) {
      uint64_t c_id = closed_ids[j];
      int c_index = find_client_index_from_id(c_id);
      if(c_index >= 0){ cleanup_client(c_index); }
      
    }
    closed_ids.clear();

    std::cout << "clients: " << clients.size()  << std::endl;

    usleep(100000);

    
  }

  //close all sockets
  close(listener_fd);
  for (int i = 0; i < clients.size(); i++) {
    close(clients[i]->socket_fd);
  }

  println("program closed");
  
  return 0;
}
