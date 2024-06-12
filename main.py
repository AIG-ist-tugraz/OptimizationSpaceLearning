from training import training
from testing import testing
from sys import argv


def main():
    mode = "test"  # allowed: "train" and "test"

    if mode == "train":
        training()
    elif mode == "test":
        assert len(argv) == 3
        testing(int(argv[1]), int(argv[2]))
    else:
        raise RuntimeError("Invalid mode - check the main function in main.py!")


if __name__ == '__main__':
    main()
