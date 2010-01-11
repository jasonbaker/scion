def get_dis_printer(args):
    """
    Either get a real dis function or a dummy one depending on what
    command-line options are specified.
    """
    if args.dis:
        from dis import dis as _dis
        def dis(code, msg=None):
            if msg:
                print msg
            _dis(code)
    else:
        def dis(*args, **kwargs):
            pass
    return dis
    
