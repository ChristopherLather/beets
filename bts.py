#!/usr/bin/env python
from optparse import OptionParser
from beets import Library

def add(lib, paths):
    for path in paths:
        lib.add(path)
    lib.save()

def ls(lib, criteria):
    q = ' '.join(criteria)
    if not q.strip():
        q = None    # no criteria => match anything
    for item in lib.get(q):
        print item.artist + ' - ' + item.album + ' - ' + item.title

def imp(lib, paths):
    for path in paths:
        lib.add(path, copy=True)
    lib.save()

def option(lib, options):
    (key, value) = options
    lib.options[key] = value
    lib.save()

def remove(lib, criteria):
    q = ' '.join(criteria)
    if not q.strip():
        raise ValueError('must provide some criteria for removing')
    for item in lib.get(q):
        print "removing " + item.path
        item.remove()
    lib.save()

def delete(lib, criteria):
    q = ' '.join(criteria)
    if not q.strip():
        raise ValueError('must provide some criteria for deleting')
    for item in lib.get(q):
        print "deleting " + item.path
        item.delete()
    lib.save()

def read(lib, criteria):
    q = ' '.join(criteria)
    if not q.strip():
        q = None
    for item in lib.get(q):
        item.read()
        item.store()
    lib.save()

def bpd(lib, opts):
    host = opts.pop(0) if opts else '127.0.0.1'
    port = int(opts.pop(0)) if opts else 6600
    
    import beets.player.bpd
    beets.player.bpd.BGServer(lib, host, port).run()

if __name__ == "__main__":
    # parse options
    usage = """usage: %prog [options] command
command is one of: add, remove, update, write, list, help"""
    op = OptionParser(usage=usage)
    op.add_option('-l', '--library', dest='libpath', metavar='PATH',
                  default='library.blb',
                  help='work on the specified library file')
    op.remove_option('--help')
    opts, args = op.parse_args()
    
    # make sure we have a command
    if len(args) < 1:
        op.error('no command specified')
    cmd = args.pop(0)
    
    lib = Library(opts.libpath)
    
    # make a "help" command
    def help(*args): op.print_help()
    
    # choose which command to invoke
    avail_commands = [
        (add,        ['add']),
        (imp,        ['import', 'im', 'imp']),
        (remove,     ['remove', 'rm']),
        (delete,     ['delete', 'del']),
        
        (read,       ['read', 'r']),
        #(write,      ['write', 'wr', 'w']),
        
        (ls,         ['list', 'ls']),
        
        (option,     ['set']),
        (help,       ['help', 'h']),
        
        (bpd,        ['bpd']),
    ]
    for test_command in avail_commands:
        if cmd in test_command[1]:
            (test_command[0])(lib, args)
            op.exit()
    
    # no command matched
    op.error('invalid command "' + cmd + '"')
