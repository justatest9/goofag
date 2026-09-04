import yarl
import sys 

# remove duplicates from v2ray list

g_array = []

def find_url_in_arr(url):
    for lit in g_array:
        it = lit[0]
        if ( url.scheme == it.scheme and 
             url.host == it.host and 
             url.port == it.port and 
             url.user == it.user ) :
            return True
    return False 

def main():
    for line in sys.stdin:
        cline = line.strip()
        url = yarl.URL(cline)
        if not find_url_in_arr(url):
            g_array.append((url, cline))

    for i in g_array:
        print(i[1])

if __name__ == "__main__":
    main()
