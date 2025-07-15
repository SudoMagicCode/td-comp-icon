
read_only_pars: list[str] = ['Dirty', 'External']
op_color_pars: list[str] = ['default', 'select', 'font', 'icon']
user_colors_table = parent.iconComp.op('table_user_colors')


def set_parent_shortcut():
    if parent().par.parentshortcut != 'iconComp':
        parent().par.parentshortcut = 'iconComp'
        parent().par.parentshortcut.readOnly = True
    else:
        pass


def build_menu_pars() -> None:
    rows: list[list[str]] = []
    rows.append(['label', 'name'])

    for eachOp in list(families.keys()):
        rows.append([eachOp, eachOp.title()])

    userColors = parent.iconComp.seq.Usercolor
    for eachBlock in userColors.blocks:
        for eachPar in eachBlock:
            if 'name' in eachPar.name:
                rows.append([eachPar[0], tdu.digits(eachPar.name)])

    user_colors_table.clear()
    for eachRow in rows:
        user_colors_table.appendRow(eachRow)
    return


def color_from_name_and_type(menuName: str, parType: str) -> tuple:

    if parent.iconComp.par.Usecolordefiniton:
        if menuName.eval() in [each.title() for each in families.keys()]:
            return parent.iconComp.parGroup[f'{menuName.eval().title()}{parType}']
        else:
            return parent.iconComp.parGroup[f'Usercolor{menuName.eval()}{parType}']
    else:
        match parType:
            case 'select':
                return parent.iconComp.parGroup.Framecolor
            case 'font':
                return parent.iconComp.parGroup.Fontcolor
            case _:
                return parent.iconComp.parGroup.Bgcolor


def icon_str(menuName: str) -> str:
    if parent.iconComp.par.Usecolordefiniton:
        if menuName.eval() in [each.title() for each in families.keys()]:
            return eval(f"chr(0x{parent.iconComp.par[f'{menuName.eval().title()}icon']})")
        else:
            return eval(f"chr(0x{parent.iconComp.par[f'Usercolor{menuName.eval().title()}icon']})")
    else:
        if parent.iconComp.par.Iconcode.eval() == '':
            return eval('chr(0x0000)')
        else:
            return eval(f'chr(0x{parent.iconComp.par.Iconcode.eval()})')


def reset_defaults() -> None:
    set_parent_shortcut()

    for eachFamily in families.keys():
        for each_color_par in op_color_pars:
            target_par: str = f'{eachFamily}{each_color_par}'
            target_par = target_par.title()
            parent.iconComp.parGroup[target_par].reset()

            parent.iconComp.parGroup[target_par].readOnly = True

    for eachPar in read_only_pars:
        parent.iconComp.par[eachPar].readOnly = True
