
# 🐚 Custom Shell – Python-Based Command Line Interface

A lightweight, custom-built command-line shell written in Python that mimics core features of Unix/Linux shells. This shell supports built-in commands, I/O redirection, piping, background process handling, and a custom help system.



## 🚀 Features

- 🧠 Built-in commands: `cd`, `ls`, `pwd`, `echo`, `whoami`, `history`, `help`, `exit`, and more
- 🔁 Command piping: `|` operator to chain commands like `ls | grep py`
- 📁 Input/Output redirection: `>` to write, `>>` to append, `<` to read input from file
- ⏱ Background execution using `&` (e.g., `sleep 5 &`)
- 🧾 Command history tracking
- 📚 Built-in help system with detailed descriptions
- ❌ Graceful error handling for invalid commands

## 🧪 Sample Commands

See [`sample_commands.txt`](sample_commands.txt) for a full list. Here are a few examples:

```bash
pwd
cd ..
echo "Hello World" > hello.txt
cat hello.txt
ls | grep txt
sleep 5 &
history
help
exit
````

## 📄 Example Output

See [`example_output.txt`](example_output.txt) to view how the shell handles both valid and invalid commands. Below is a preview:

```bash
$ pwd
C:\Users

$ whoami
libz4

$ echo hello > out.txt

$ ls
Documents
Downloads
hello.txt
...

$ help
Available Commands:
- echo       : Print text or redirect...
- pwd        : Print current working directory
- ...
```

## 📂 Project Structure

```
Custom-Shell/
├── custom_shell.py          # Main shell implementation
├── sample_commands.txt      # Example commands to test the shell
├── example_output.txt       # Sample output from shell run
├── README.md                # Project documentation
├── .gitignore               # File exclusions for Git
```

## 🛠 How to Run

Make sure you have Python 3 installed. Then in your terminal:

```bash
python custom_shell.py
```

Enter commands in the custom shell prompt.

## 👤 Author

Laiba Maab
Final-year Software Engineering student | Developer | Learning enthusiast
GitHub: [@laibamaab](https://github.com/laibamaab)


## ⭐️ Give It a Star!

If you found this project useful, please give it a ⭐️ on GitHub and feel free to fork, use, and modify it!


