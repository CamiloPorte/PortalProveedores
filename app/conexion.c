#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<netdb.h>


char* obtoken(int largo, char mensaje[largo]){
  char *aux;
  const char split1  = '>' ;
  *(mensaje+strlen(mensaje)-12) = 0;
  aux = strrchr(mensaje,split1);
  aux = aux+1;
  return aux;
}

int contar(int largo,char palabra[largo],char caracter){
  int count = 0;
  int i = 0;
  while(i <= largo){
    if (palabra[i]==caracter)
    {
      count++;
    }
    i++;
  }
  return count;
}


char* obtdata(int leng, char resultado[leng]){
  char *aux;
  const char split1  = '>' ;
  char split2[]  = "|~" ;
  *(resultado+strlen(resultado)-23) = 0;
  aux = strrchr(resultado,split1);
  aux = aux+1;
  return aux;
}



char* conexion(){
  char buffer[99999];
  char mesage[99999];
  char *token;

  int SdSock, socklen;
  struct sockaddr_in sock_in;
  struct in_addr ip_addr;

  if ((SdSock = socket (AF_INET, SOCK_STREAM, 0)) < 0)
  { perror (("C-Socket Input"));
    exit (1);
  }

  inet_aton ("45.79.37.223", &ip_addr);
  socklen = sizeof (struct sockaddr_in);
  memset ((char *)&sock_in, 0, socklen);
  sock_in.sin_family = AF_INET;
  sock_in.sin_port = htons(25000);
  sock_in.sin_addr.s_addr = pipe ? ip_addr.s_addr : INADDR_ANY ;

  if (connect (SdSock, (struct sockaddr *) &sock_in, socklen) < 0)
  { perror (("C-Connect"));
    exit (1);
  }

  //autenticarse
  sprintf(buffer , "<tx id='borja'>\n  <req>auten</req>\n <usr>walker</usr>\n <psw>walker</psw>\n </tx>");
  int largo = strlen(buffer);
  sprintf(mesage,"%05d%s", largo , buffer);
  printf("antes de envio \n" );
  printf("%s\n",mesage); // imprime lo que se envía
  send(SdSock, mesage, strlen(mesage), 0); //envio
  printf("despues de envio \n" );
  //se limpian los buffers.
  memset(&mesage, 0, sizeof mesage);
  memset(&buffer, 0, sizeof buffer);
  recv(SdSock, mesage, 99999, 0);//recepción
  printf("%s\n", mesage);
  token = obtoken(99999,mesage);
  //printf("el token es :%s\n \n \n",token);


  int largoacumulado =0;

  //query

  sprintf(buffer , "<tx id='borja'>\n  <req>dbcur</req>\n <ott>%s</ott>\n"
    " <prm>\n <sql> select log.log_id ||'|'|| acciones.acc_desc ||'|'||"
    " status.stat_desc ||'|'|| to_char(log.log_time , 'dd/mm/yy hh24:mi:ss')"
    " from log, acciones, status where log.acc_id = acciones.acc_id and "
    "log.stat_id = status.stat_id and log.log_time > current_date order by log_id, log_time  ;"
    " </sql>\n </prm>\n </tx>",token);
  largo = strlen(buffer);
  sprintf(mesage,"%05d%s", largo , buffer);
  send(SdSock, mesage, strlen(mesage), 0); //envio
  //se limpian los buffers.
  memset(&mesage, 0, sizeof mesage);
  memset(&buffer, 0, sizeof buffer);
  recv(SdSock, mesage, 99999, 0); //recepción
  //printf("%s\n", mesage);
  strcat(buffer,mesage);

  largoacumulado = strlen(mesage);

  *(mesage+5)=0;
  int largototal = atoi(mesage);


  largototal = largototal - largoacumulado;

  while(largototal>0){
    memset(&mesage, 0, sizeof mesage);
    recv(SdSock, mesage, 99999, 0); //recepción
    largoacumulado = strlen(mesage); 
    strcat(buffer,mesage);
    largototal = largototal - largoacumulado;
  }

  printf("la respuesta a todo es :\n\n %s\n",buffer );
  close(SdSock);
  return obtdata(strlen(buffer),buffer);
}


int main()
{
  return 0;
}