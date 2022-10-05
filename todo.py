"""Project (Command line task manager)

Tiger Chen
"""

import classes
import argparse

def main():
    """All the real work!"""
    parser  = argparse.ArgumentParser(description='Update your ToDO list.')
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list')
    parser.add_argument("--delete", type = int, nargs = "+",required = False, help = "Enter a or several task id(s).")
    parser.add_argument('--due', type=str, required=False, help='due date in MM/dd/YYYY format')
    parser.add_argument('--priority', type=int, required=False, default=1, help='priority of task; default value is 1')
    parser.add_argument('--query', type=str, required=False, nargs='+', help='priority of task; default value is 1')
    parser.add_argument('--list', action='store_true', required=False, help='list al tasks that have not been completed')
    parser.add_argument('--report',  action='store_true', required=False, help='list all tasks, including both completed and incompleted tasks' )
    parser.add_argument("--done", type = int, nargs = "+", required = False, help = "Enter a or several task id(s).")
    
    # Parse the argument
    args = parser.parse_args()

    # Load the tasks
    tasks = classes.Tasks()
    if args:
        if args.add:
            tasks.add(args.add, args.priority, args.due)
        if args.delete:
            tasks.delete(args.delete)
        if args.list:
            tasks.list()
        if args.report:
            tasks.report()
        if args.query:
            tasks.query(args.query)
        if args.done:
            tasks.done(args.done)
            
    # store tasks into the disk
    tasks.pickle_tasks()
    exit()

if __name__ == '__main__':
    main()