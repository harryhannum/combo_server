import argparse


def main():
    parser = argparse.ArgumentParser(description='Combo Server Arguments')
    parser.add_argument('sources_json', help='A sources json')
    args = parser.parse_args()

    DependenciesManager(args.path, args.sources_json).resolve()


if __name__ == '__main__':
    main()
