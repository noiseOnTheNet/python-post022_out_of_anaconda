import argparse
from .parser import read
from .requirement import dump_requirements, write_requirements, env_to_requirement

def main(filename, save):
    env = read(filename)
    reqs = env_to_requirement(env)
    if save:
        write_requirements(reqs,"requirements.txt")
    else:
        for line in dump_requirements(reqs):
            print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "rikki",
        description = "translator from conda environment yaml"
    )
    parser.add_argument("filename")
    parser.add_argument("-w", "--write-file", action="store_true", default=False)
    args = parser.parse_args()
    main(args.filename,args.write_file)
