import socket
import signal
import sys,time,optparse
import os.path
from datetime import datetime
from multiprocessing import Pool
import argparse

version = 0.1
"""You know, 20 years of shit and stuff"""

"""Hackish solution, better way would be argeparse"""
if len(sys.argv) < 3:
    print "Give two arguments: \n"
    print "portscan_threaded.py {1} {2}"
    print "{1} is a hostname or inputfilename with hostnames/ip addresses\n{2} is the amount of concurrent pool connections for threading\n"
    print "Setting poolsize to 50 or 100 would be a good start, setting higher depends on responsiveness of remote host and the connection quality"""
    print "NOPENOPENOPE...exiting!"""
    sys.exit(1)

#parser=argparse.ArgumentParser(
#        description='''Python TCP portscanner, with multiprocessed scans on ports.\nVersion v0.1''',
#        epilog="""All's well that ends well.""")
#parser.add_argument('-f', type=str, default=[1], help='Filename')
#parser.add_argument('host/ip', nargs=1, default=[1], help='Hostname or IP address')
#args=parser.parse_args()

"""Declaring global variables"""
hip		= sys.argv[1]
pools		= sys.argv[2]
min_port 	= 1
max_port	= 65535
timeout 	= 1

def scan(arg):
        """Scan a specific port on a specific target"""
        target, port = arg

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(timeout)

        try:
		sock.connect((target, port))
		sock.close()

		return port, True
        except KeyboardInterrupt:
                keyboard_interrupt()
	except (socket.timeout, socket.error):
		return port, False

def sig_send():
        """Work-around for handling sigints to multiple pools"""
        def sig_int(signal_num, frame):
            return None
        signal.signal(signal.SIGINT, sig_int)

def keyboard_interrupt():
        """Handles keyboardinterrupt exceptions"""
        print("\n\n[*] User requested an interrupt.")
        print("[*] Application shutting down at %s." % (time.strftime("%H:%M:%S")))
        sys.exit(1)

def start_t():
        """Returns the current starttime in seconds"""
        start_time = time.time()
        return start_time

def stop_t():
        """Returns the time for indicating a stop in seconds"""
        stop_time = time.time()
        return stop_time

def main():
        """Main execution"""
	try:
                """Declare loop variables"""
		num_procs   	= int(pools)
                pool        	= Pool(num_procs, sig_send)
		ports       	= range(min_port, max_port)


                """Start timer"""
                start_time = start_t()

                try:
			print("\n[*] Scanning started at %s...\n" % (time.strftime("%H:%M:%S")))

			if os.path.isfile(hip):
				"""If it appears to be a filename, scan every line in the file"""
				with open(hip) as f:
					targets = f.readlines()
					for host in targets:
						target = host.strip()
						print 'Host:', target
						resolved = socket.gethostbyname(target)
						print 'Resolved:', resolved
						open_ports = 0

						for port, status in pool.imap_unordered(scan, [(target, port) for port in ports]):
							if status:
								print port, 'is open'
								open_ports += 1
						print("\n[*] Total open ports: %d\n" % (open_ports))
			else:
				"""If it appears to be a hostname, scan the single host"""
				target = socket.gethostbyname(hip)
				print 'Host:', hip
				print 'Resolved:', target
				open_ports = 0

				for port, status in pool.imap_unordered(scan, [(target, port) for port in ports]):
					if status:
						print port, 'is open'
						open_ports += 1
				print("\n[*] Total open ports: %d\n" % (open_ports))

			"""Stop timer after scanning all ports on target"""
			stop_time = stop_t()

			"""Calculate total_time by subtracting stop_time from start_time, in seconds"""
			total_time = stop_time - start_time

			"""Divisions for calculating minutes/seconds/hours"""
			m, s = divmod(total_time, 60)
			h, m = divmod(m, 60)

			print("[*] Scan ended at %s" % (time.strftime("%H:%M:%S")))
			print("[*] Total time taken was %d:%02d:%02d\n" % (h, m, s))
                except KeyboardInterrupt:
                    """Handle keyboardinterrupt and terminate pools"""
                    pool.terminate()
                    keyboard_interrupt()
                except Exception,e:
                    """Handle other exceptions, terminate running pools and exit"""
                    pool.terminate()
                    print("Error: %s" % (e))
                    sys.exit(1)
                finally:
                    """Joing ending pools"""
                    pool.join()
	except KeyboardInterrupt:
                """Handle keyboardinterrupt while still inserting data before start"""
		keyboard_interrupt()
	except Exception, e:
                """Handle other exceptions"""
		sys.exit(1)

if __name__ == '__main__':
        """Handles main() call"""
        main()
