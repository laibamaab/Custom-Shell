import os
import sys          #for system specification information. used for exit 
import readline     #for tab completion
import shutil       #for file operation like move and copy
import subprocess   #run external commands
import datetime
import getpass      #get current user name
from pathlib import Path
import psutil       # for disk, processes and ram monitoring

class Bash:

    # Stores background jobs
    __background_jobs = []

    # Stores help text for each command.
    __HELP_DICT = {
        'cat': 'Display file content (cat <file>). Supports piping (<cat file.txt | grep keyword>, <cat file.txt | sort | uniq>)',
        'cd': 'Change directory (cd <dir>) or go up (cd ..)',
        'clear': 'Clear the terminal screen',
        'cp': 'Copy a file (cp <source_file> <destination_file>)',
        'date': 'Show current date and time',
        'disk': 'Check Disk info: disk total | disk used | disk available',
        'echo': 'Print text or redirect: echo "text" > file (overwrite), echo "text" >> file (append), echo < file (read input)',
        'exit': 'Exit the shell',
        'help': 'Show help information',
        'history': 'Show command history',
        'hostname': 'Show desktop name',
        'kill': 'Kill a running process by name (kill <name>)',
        'ls': 'List files in current directory. Supports piping (<ls | grep <type>>)',
        'mkdir': 'Create a new directory (mkdir <dir>)',
        'mv': 'Move a file (mv <source_file> <destination_file>)',
        'nano': 'Open a file in nano editor (nano <file>)',
        'open': 'Open any file or application using the default program (open <file or app>)',
        'pwd': 'Print current working directory',
        'ram': 'Check RAM info: ram total | ram used | ram available',
        'rm': 'Remove a file (rm <file>)',
        'rmdir': 'Remove a directory (rmdir <dir>)',
        'top': 'List all running processes',
        'touch': 'Create an empty file (touch <file>)',
        'tree': 'Display directory tree structure',
        'whoami': 'Show current user',
        'jobs': 'Jobs List all background jobs.',
        'ps': 'Display running processes (<ps aux>). Supports piping.(<ps aux | grep python)',
        'sleep': 'Pause execution for given duration in background (<sleep 5 &>)',
        '|': 'Usage: <cmd1> | <cmd2> Pipe output of one command as input to another.',
        '&': 'Usage: <command> & Run a command in the background.'
    }

    #Displays a welcome banner with ASCII art.
    def __welcome(self):
        welcome = [
            r"__        _______ _     ____ ___  __  __ _____   _____ ___ ",
            r"\ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \ ",
            r" \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | |",
            r"  \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| |",
            r"   \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/ "
        ] # ASCII CODE
        bash = [
            r" ___ ___ _   _ ___   ____    _    ____  _   _ ",
            r"|_ _|_ _| | | |_ _| | __ )  / \  / ___|| | | |",
            r" | | | || | | || |  |  _ \ / _ \ \___ \| |_| |",
            r" | | | || |_| || |  | |_) / ___ \ ___) |  _  |",
            r"|___|___|\___/|___| |____/_/   \_\____/|_| |_|"
        ] # ASCII CODE
        obj = [welcome, bash]

        # handle printing ascii art line by line
        def type_out(text_array, ):
            width = shutil.get_terminal_size((80, 20)).columns #get terminal width
            for line in text_array:
                centered_line = line.center(width) #centered the ascii art
                for char in centered_line:
                    print(self.color_text(char, 'crimson'), end='')  # Printing ASCII art in color
                print()

        # display welcome and bash from obj
        for item in obj:
            type_out(item)
            print()

    # apply color to text
    def color_text(self, text, color):
        colors = {
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'purple': '\033[35m',
            'reset': '\033[0m',
            'crimson': '\033[36m',
        }
        return (f"{colors.get(color, colors['reset'])}{text}{colors['reset']}" if os.name == 'nt' else text)

    #handle auto completion of files or directory on tab predd
    def __completer(self, text, state):
        current_dir = os.getcwd()
        options = [f for f in os.listdir(current_dir) if f.startswith(text)]
        if state < len(options):
            return options[state] #return matching file or directory
        else:
            return None 

    def __copy_file(self, path, parts):
        if not path:
            print(self.color_text(self.__HELP_DICT['cp'], 'red')) # display help for cp command
        elif os.path.exists(path):
            try:
                arg_path = parts[2].replace('"', '')
                if os.path.isabs(arg_path):
                    des_path = os.path.abspath(arg_path)
                else:
                    des_path = os.path.abspath(os.path.join(os.getcwd(), arg_path))
            except IndexError:
                print(self.color_text("Enter destination path.", 'red'))
                return

            if os.path.isfile(path): #handle files
                if not os.path.exists(des_path): 
                    with open(des_path, 'x') as f:
                        pass 
                shutil.copy(path, des_path)
                print(f"File copied to {des_path}")                    
            elif os.path.isdir(path): #handle directories
                if os.path.exists(des_path):
                    shutil.copytree(path, des_path)
                    print(f"Directory copied to {des_path}")
                else:
                    print(self.color_text("Destination path does not exist.", 'red'))
            else:
                print(self.color_text('Source path not found.', 'red'))

    # display file and directory names in hirearchy form
    def __print_tree(self, path, prefix=''):
        if not os.path.exists(path):
            print(f'Path "{path}" does not exist.')
            return

        print(f'{self.color_text(prefix, 'crimson')}{self.color_text(os.path.basename(path), 'purple')}/')
        prefix += '-------'

        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    # recursive call for itself (if the item is folder) to print all files and directories with in the folder
                    self.__print_tree(item_path, prefix) 
                else:
                    print(f'{self.color_text(prefix, 'crimson')}{item}')
        except PermissionError:
            print(f'{prefix}[Permission Denied]')

    def __move_file(self, path, parts):
        if not path:
            print(self.color_text(self.__HELP_DICT['mv'], 'red'))
        elif os.path.exists(path):
            try:
                arg_path = parts[2].replace('"', '')
                if os.path.isabs(arg_path):
                    des_path = os.path.abspath(arg_path)
                else:
                    des_path = os.path.abspath(os.path.join(os.getcwd(), arg_path))
            except IndexError:
                print(self.color_text("Enter destination path.", 'red'))
                return

            try:
                if os.path.exists(des_path):  
                    shutil.move(path, des_path)
                    print(f"File moved to {des_path}")
                else:
                    print(self.color_text("Destination path does not exist.", 'red'))
            except shutil.Error:
                print(self.color_text("File already exists.",'red'))
            except PermissionError:
                print(f"Cannot move directory because its contents are currently in use.")
            except Exception:
                print(f"An unexpected error occur.")
        else:
            print(self.color_text('Source path not found.', 'red'))

    def __cat_command(self, path, arg):
        if not path:
            print(self.color_text(self.__HELP_DICT['cat'], 'red'))
        elif os.path.exists(path):
            with open(path, 'r') as f:
                print(f.read().strip()) # read content from the file
        else:
            print(self.color_text(f'{arg} file does not exit.', 'red'))

    def __change_directory(self, path, arg):
        if path:
            if arg=='..':
                os.chdir(Path(path))
            else:
                if os.path.exists(path):
                    os.chdir(path)
                else:
                    print(self.color_text(f"{path} path does not exist.", 'red'))
        else:
            print(self.color_text(self.__HELP_DICT['cd'], 'red'))

    def __display_running_processes(self):
        print(f"{'PID':<10} {'Name':<25} {'Status':<15}")
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                print(f"{proc.info['pid']:<10} {proc.info['name']:<25} {proc.info['status']:<15}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def __kill_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()  # A request for graceful termination. sends SIGTERM (signal 15)
            process.wait(timeout=3)  # wait up to 3 seconds for it to terminate
            print(f"Process {pid} terminated successfully.")
        except psutil.NoSuchProcess:
            print(self.color_text(f"No process with PID {pid} found.", 'red'))
        except psutil.AccessDenied:
            print(self.color_text(f"Access denied to terminate process {pid}.", 'red'))
        except psutil.TimeoutExpired:
            print(self.color_text(f"Process {pid} did not terminate in time, trying to kill it forcefully...",'red'))
            process.kill()   #Forceful termination and send SIGKILL (signal 9)
            print(f"Process {pid} killed.")

    def __kill_running_process(self,arg):
        if not arg:
            print(self.color_text(self.__HELP_DICT['kill'], 'red'))
            return
        print(arg)
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            if arg.lower() in proc.info['name']:
                self.__kill_process(proc.info['pid'])
                return

    def __display_list(self):
        items = os.listdir(os.getcwd())
        for item in items:
            if not os.path.isfile(item):
                print(self.color_text(item, 'purple'))
                continue
            print(item)

    def __display_echo(self, arg, parts):
        if arg:
            for i in parts[1:]:
                print(bytes(i.replace('"', ''), "utf-8").decode("unicode_escape"), end=" ") # to handle escape sequences 
            print()
        else:
            print(self.color_text("Please provide text to echo.", 'red'))
            print(self.color_text(self.__HELP_DICT['echo'], 'red'))

    def __default_condition(self, command, parts):
        # fallback: spawn a subprocess to run the command
        try:
            pid = os.fork() # create a new process
            if pid == 0:
                # Child process
                os.execvp(parts[0], parts) #replace the current process with a new one
            else:
                # Parent process waits for child
                os.wait()

        except AttributeError:
            # If os.fork() is not available on the OS (e.g., Windows), fallback to subprocess
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.stdout: # if normal output
                    print(result.stdout)
                if result.stderr: # if error
                    print(self.color_text(f'IIUI-Shell: {command}: command not found.', 'red'))
                    print(self.color_text("Type 'help' to check valid commands.", 'purple'))
                    print(self.color_text(result.stderr, 'purple'))

            except Exception as e:
                print(self.color_text(f"Error executing command: {e}", 'red'))
                print(f'IIUI-Shell: {command}: command not found.')
                print("Type 'help' to check valid commands.")

        except Exception as e:
            print(self.color_text(f"Error executing command: {e}", 'red'))
            print(f'IIUI-Shell: {command}: command not found.')
            print("Type 'help' to check valid commands.")

    def __display_help(self):
        print(self.color_text('Available Commands:', 'crimson'))
        for cmd, desc in self.__HELP_DICT.items():
            current_cmd = f'{cmd:<10}'
            print(f"- {self.color_text((current_cmd),'yellow')} : {self.color_text(desc, 'purple')}")

    def __create_file(self, path, arg):
        if path:
            if not os.path.exists(path):
                open(path, 'a').close()
                print(f'File {arg} created successfully.')
            else:
                print(self.color_text(f'File {arg} already exists.', 'red'))
        else:
            print(self.color_text(self.__HELP_DICT['touch'], 'red'))

    def __remove_file(self, path, arg):
        if path:
            if os.path.exists(path):
                os.remove(path)
                print(f'File {arg} removed successfully.')
            else:
                print(self.color_text(f'File {arg} does not exist.', 'red'))
        else:
            print(self.color_text(self.__HELP_DICT['rm'], 'red'))

    def __remove_directory(self, path, arg):
        if path:
            if os.path.exists(path):
                shutil.rmtree(path)
                print(f'Directory {arg} removed successfully.')
            else:
                print(self.color_text(f'Directory {arg} does not exist.', 'red'))
        else:
            print(self.color_text(self.__HELP_DICT['rmdir'], 'red'))

    def __create_directory(self, path, arg):
        if path:
            if not os.path.exists(path):
                os.mkdir(path)
                print(f'Directory {arg} created successfully.')
            else:
                print(self.color_text(f'Directory {arg} already exists.', 'red'))
        else:
            print(self.color_text(self.__HELP_DICT['mkdir'], 'red'))

    # Run the given command in the background.
    def __run_background(self, command_line):
        # Remove the ampersand, split into command components
        cmd = command_line.replace('&', '').strip().split()
        if cmd[0] == "sleep":
            if len(cmd) < 2 or not cmd[1].isdigit():
                print(self.color_text(self.__HELP_DICT['sleep'], 'red'))
                return
            
        try:
            process = subprocess.Popen(cmd) #launches the process asynchronously (in the background).
            self.__background_jobs.append((process.pid, ' '.join(cmd)))
            print(f"[{process.pid}] Running in background: {' '.join(cmd)}")
        except FileNotFoundError:
            print(self.color_text(self.__HELP_DICT['&'], 'red'))

    def __list_jobs(self):
        # List all background jobs stored so far.
        for pid, cmd in self.__background_jobs:
            print(f"[{pid}] {cmd}")

    def __handle_io_redirection(self, command):
        if '>>' in command:
            parts = command.split('>>')  
        elif '>' in command:
            parts = command.split('>')
        elif '<' in command:
            parts = command.split('<')  

        left = parts[0].strip()  # Command and argument
        right = parts[1].strip()  # Redirection file

        left_parts = left.split(' ', 1)
        cmd = left_parts[0]
        arg = left_parts[1] if len(left_parts) > 1 else ''
        redirection_file = right

        path = os.path.join(os.getcwd(), redirection_file)
        if not redirection_file:
            print(self.color_text(self.__HELP_DICT['mv'], 'red'))
            return

        output = bytes(arg.replace('"', ''), "utf-8").decode("unicode_escape")
                    
        if '>>' in command: # write in the file
            with open(path, 'a') as f:
                f.write(output + '\n')

        elif '>' in command: # append in file
            with open(path, 'w') as f:
                f.write(output + '\n')

        elif '<' in command: # read content from file
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read().strip()
                    print(content)
            else:
                print(self.color_text(f"Input file '{right}' does not exist.", 'red')) 
        else:
            print(self.color_text(f'Redirection with >, >>, or < is supported for echo only.', 'red'))
            print(self.color_text(self.__HELP_DICT['echo'], 'red'))

    def __run_pipe(self, command_line):
        try:
            # Parse piped commands
            parts = [cmd.strip().split() for cmd in command_line.strip().split('|')]
            
            # First process. The output of this process will be connected so it can be fed into another process.
            prev = subprocess.Popen(parts[0], stdout=subprocess.PIPE) 
            
            # Intermediate processes
            for part in parts[1:-1]:
                proc = subprocess.Popen(part, stdin=prev.stdout, stdout=subprocess.PIPE)
                prev.stdout.close()
                prev = proc

            # Final process
            final = subprocess.Popen(parts[-1], stdin=prev.stdout, stdout=subprocess.PIPE)
            prev.stdout.close()

            # Wait for completion
            output, _ = final.communicate()

            # Clean output
            return output.decode().strip()
        except Exception:
            print(self.color_text(self.__HELP_DICT['|'], 'red'))

    def __handle_running_process(self, parts ):
        if len(parts) > 1 and parts[1] == 'aux':
            try:
                # runs the command, waits for it to complete, and returns its output as bytes.
                output = subprocess.check_output(['ps', 'aux'], stderr=subprocess.STDOUT)
                print(output.decode())
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.output.decode()}")
        else:
            print(self.color_text(self.__HELP_DICT['ps'], 'red'))

    def run_shell(self):
        self.__welcome()
        # handle auto cmpletion on tab press
        readline.set_completer(self.__completer)
        readline.parse_and_bind('tab: complete')

        #list to store the commands entered
        history = []

        while True:
            # Prompt: "user@host IIUI-Shell ~/path $ "
            print(self.color_text(f"\n{getpass.getuser()}@{os.environ['COMPUTERNAME']} ", 'green'),
                  self.color_text("IIUI-Shell ", 'purple'),
                  self.color_text(f"~/{'/'.join(os.getcwd().split('\\')[3:])} ", 'yellow'))
            
            command = input("$ ").strip()

            if not command.strip():
                continue

            if command == 'exit':
                print(self.color_text("Exiting IIUI-Shell. Goodbye!", 'crimson'))
                break

            history.append(command)

            #split command into parts
            parts = command.split(" ")
            cmd = parts[0]
            arg = parts[1].replace('"','') if len(parts) > 1 else None
            path = os.path.abspath(arg) if arg else None
            match cmd:
                case 'nano':
                    subprocess.run(f"nano {arg}", shell=True)

                case 'hostname':
                    print(os.environ['COMPUTERNAME'])

                case 'cp':
                    self.__copy_file(path, parts)
                
                case 'jobs':
                    self.__list_jobs()
                
                case 'tree':
                    self.__print_tree(fr'{os.getcwd()}')

                case 'open':
                    if not parts[1:]:
                        print(self.color_text(self.__HELP_DICT['open'], 'red'))
                    else:
                        os.system(f'start {(" ".join((parts[1:])))}')
                
                case 'ram':
                    memory = psutil.virtual_memory()
                    if arg == 'used':
                        print(f"{memory.used / (1024**3):.2f} GB")
                        print(f"{memory.percent}%") 
                    elif arg == 'total': 
                        print(f"{memory.total / (1024**3):.2f} GB")
                    elif arg == 'available':
                        print(f"{memory.available / (1024**3):.2f} GB")
                    else:
                        print(self.color_text(self.__HELP_DICT['ram'], 'red'))

                case 'disk':
                    disk = psutil.disk_usage('/')
                    if arg == 'used':
                        print(f"{disk.used / (1024**3):.2f} GB")
                        print(f"{disk.percent}%") 
                    elif arg == 'total': 
                        print(f"{disk.total / (1024**3):.2f} GB")
                    elif arg == 'available':
                        print(f"{disk.free / (1024**3):.2f} GB")
                    else:
                        print(self.color_text(self.__HELP_DICT['disk'], 'red'))

                case 'mv':
                    self.__move_file(path, parts)

                case 'cd':
                    self.__change_directory(path, arg)

                case 'cat':
                    if '|' in command:
                        output = self.__run_pipe(command)
                        print(output, end='' if output.endswith('\n') else '\n')
                        continue
                    else:
                        self.__cat_command(path, arg)

                case 'top':
                    self.__display_running_processes()
                
                case 'kill':
                    self.__kill_running_process(arg)

                case 'pwd':
                    print(os.getcwd())

                case 'ls':
                    if '|' in command:
                        output = self.__run_pipe(command)
                        print(output, end='' if output.endswith('\n') else '\n')
                        continue
                    else:
                        self.__display_list()

                case 'ps':
                    if '|' in command:
                        output = self.__run_pipe(command)
                        print(output, end='' if output.endswith('\n') else '\n')
                        continue
                    else:
                        self.__handle_running_process(parts)

                case 'echo':
                    if '>' in command or '>>' in command or '<' in command:
                        self.__handle_io_redirection(command)
                        continue
                    self.__display_echo(arg, parts)

                case 'date':
                    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                case 'whoami':
                    print(getpass.getuser())

                case 'mkdir':
                    self.__create_directory(path, arg)

                case 'rmdir':
                    self.__remove_directory(path, arg)
                
                case 'rm':
                    self.__remove_file(path, arg)

                case 'touch':
                    self.__create_file(path, arg)
                
                case 'history':
                    for cmd in history:
                        print(cmd)

                case 'help':
                    self.__display_help()

                case 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                        
                case _:
                    if command.endswith('&'):
                        self.__run_background(command)
                    else:
                        self.__default_condition(command, parts)

if __name__ == "__main__":
    try:
        bash = Bash()
        bash.run_shell() #start the bash
    
    except KeyboardInterrupt:
        # on any exception exit the code gracefully by printing message
        sys.exit(bash.color_text("\nExiting IIUI-Shell. Goodbye!", 'crimson')) 
           
    except EOFError: # ctrl+D
        sys.exit(bash.color_text("\nExiting IIUI-Shell. Goodbye!", 'crimson'))
    
    except Exception as e:
        print('Exp:',e)
        print(bash.color_text("Type 'help' to check valid commands.", 'purple'))
