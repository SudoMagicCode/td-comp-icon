import compIconUtils


def Restoredefaults(par):
    if par.eval() == True:
        compIconUtils.reset_defaults()

    else:
        pass


def Customcolordefinions(par):
    if par.eval() == True:
        compIconUtils.add_custom_definitions()
