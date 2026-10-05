import argparse
from .cli import run

parser = argparse.ArgumentParser(description="Menu-based SQLite expense tracker")
parser.add_argument("--database", default="expenses.db", help="SQLite database path")
args = parser.parse_args()
run(args.database)
