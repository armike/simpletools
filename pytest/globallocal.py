#!/usr/local/bin/python
globalVar = "a global var"

def main():
    localVar = "a local var"
    print locals() + globals()

if __name__ == "__main__":
    main()
