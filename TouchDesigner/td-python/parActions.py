import compIconUtils


def Restoredefaults(par):
    print(par)
    if par.eval() == True:
        compIconUtils.reset_defaults()

    else:
        pass
