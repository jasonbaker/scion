def get_dis_printer(args):
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
    
