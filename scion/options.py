def get_dis_printer(args):
    if args.dis:
        from dis import dis
        return dis
    else:
        def dummy_dis(*args, **kwargs):
            pass
        return dummy_dis
