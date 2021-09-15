import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cron_expr")
    args = parser.parse_args()


main()