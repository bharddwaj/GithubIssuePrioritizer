import click
from model import run

def err(*args, sep=' ', end='\n'):
    print("ERROR: ", end='')
    print(*args, sep=sep, end=end)

@click.command()
@click.argument('src', nargs=-1)
def main(src):
    if not src:
        err("Argument list empty")
        quit()
    for path in src:
        with open(path, 'r') as f:
            txt = f.read()
        print(run(txt))

if __name__ == '__main__':
    main()
