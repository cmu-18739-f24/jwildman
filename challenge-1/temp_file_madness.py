import random
import string
import os
import sys
import datetime
import traceback
import bcrypt


print(os.path.realpath(__file__))

TMP_MAX = random.randint(10, 20)
_candidate_names = [''.join(random.choices(string.ascii_uppercase + string.digits, k=TMP_MAX)) for i in range(TMP_MAX)]

rolling_counter = 0

def _get_candidate_names():
    return _candidate_names

# ensure we aren't writing to an existing file
def _exists(fn):
    try:
        os.lstat(fn)
    except OSError:
        return False
    else:
        return True

# get ourselves a temporary file to write to
def temp_mktemp(prefix="", suffix=""):
    global rolling_counter
    dir = "/home/ctf-player/tmp/"

    names = _get_candidate_names()
    
    for i in range(TMP_MAX):
        i_circular = (rolling_counter + i) % TMP_MAX
        name = names[i_circular]
        file = os.path.join(dir, prefix + name + suffix)
        if not _exists(file):
            rolling_counter = rolling_counter + 1
            return file
        
    raise Exception("No usable temporary filename found")

# so our other admins can get the flag, they can slow down time so
# no issue if the file exists for only a moment
def write_flag_secure():
    temp_flag_file = temp_mktemp()
    flag = open("/challenge/flag.txt").read()
    now = datetime.datetime.now()
    append = " - DO NOT DISTRIBUTE - "
    append += f" - FROM: FLAG SERVER at time - {now}"
    # next level integrity hash!!!
    salt = bcrypt.gensalt()
    result = bcrypt.hashpw(
       password=append.encode('utf-8'),
       salt=salt
    )
    append += result.decode('utf-8')
    f = open(temp_flag_file, 'w+')
    f.write(flag)
    f.write(append)
    f.close()
    # admin has saved it with premonition, we can delete
    os.remove(temp_flag_file)
    print("wrote flag securely to: ", temp_flag_file)

def exit():
  sys.exit(0)

print("Welcome to the secure flag service! Only admins should use this service. Not like you could get the flag though, you operate too slowly to catch our flags.")

while(True):
  try:
    inp = input("put in command: ")
    if (inp == "temp"):
        write_flag_secure()
    elif(inp == "flag"):
       flag = open("/challenge/flag.txt").read()
       salt = bcrypt.gensalt()
       result = bcrypt.hashpw(
            password=flag.encode('utf-8'),
            salt=salt
       )
       print(flag)
       print("have fun with this!!!")
    elif (inp == "exit"):
       exit()
  except Exception as e:
    print("ERROR", e)
    print(traceback.format_exc())
    break