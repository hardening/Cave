/**
 * to compile this:
 *   g++ phantom3-video.cpp -o phantom3-video -ludt -lpthread
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <netdb.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#include <iostream>
#include <udt/udt>

using namespace std;

int main(int argc, char *argv[]) {
	uint8_t *recv_buffer;
	struct addrinfo hints, *peer;

	UDT::startup();
	memset(&hints, 0, sizeof(struct addrinfo));

	hints.ai_flags = AI_PASSIVE;
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	if (getaddrinfo("192.168.1.3", "9000", &hints, &peer) != 0) {
		cout << "incorrect server/peer address. " << "192.168.1.3" << ":" << "9000"
				<< endl;
		return 0;
	}

	UDTSOCKET client = UDT::socket(peer->ai_family, peer->ai_socktype, peer->ai_protocol);

	if (UDT::connect(client, peer->ai_addr, peer->ai_addrlen) == UDT::ERROR) {
		cout << "connect: " << UDT::getlasterror().getErrorMessage() << endl;
		return 0;
	}

	freeaddrinfo(peer);

	recv_buffer = (uint8_t *)malloc(65535);
	if (!recv_buffer) {
		cout << "unable to allocate buffer" << endl;
		return 0;
	}

	while (true) {
		int res = UDT::recv(client, (char *)recv_buffer, 65535, 0);
		if (res == UDT::ERROR) {
			cout << "error recving" << endl;
			return 1;
		}

		write(STDOUT_FILENO, recv_buffer, res);
	}
}



