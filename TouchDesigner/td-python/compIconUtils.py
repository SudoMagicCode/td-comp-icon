
read_only_pars: list[str] = ['Dirty', 'External']
op_color_pars: list[str] = ['default', 'select', 'font', 'icon']
color_defs = op('color_defs')
icon_tag = 'networkIcon'


def set_parent_shortcut():
    if parent().par.parentshortcut != 'iconComp':
        parent().par.parentshortcut = 'iconComp'
        parent().par.parentshortcut.readOnly = True
    else:
        pass


def add_icon_tag():
    if icon_tag not in parent().tags:
        parent().tags.add(icon_tag)


def color_defs_op():
    '''Returns a color definition op - a base COMP with custom pars for colors that follow a known pattern
    '''
    return parent.iconComp.par.Colordefinitons.eval()


def build_menu_pars() -> None:
    '''Builds menu parameters into a DAT
    '''
    set_parent_shortcut()
    user_colors_table = parent.iconComp.op('table_user_colors')
    rows: list[list[str]] = []
    rows.append(['label', 'name'])

    for eachOp in list(families.keys()):
        rows.append([eachOp, eachOp.title()])

    userColors = color_defs_op().seq.Usercolor
    for eachBlock in userColors.blocks:
        for eachPar in eachBlock:
            if 'name' in eachPar.name:
                rows.append([eachPar[0], tdu.digits(eachPar.name)])

    user_colors_table.clear()
    for eachRow in rows:
        user_colors_table.appendRow(eachRow)
    return


def color_from_name_and_type(menuName: str, parType: str) -> tuple:
    '''Resolves color for pars
    '''

    if parent.iconComp.par.Usecolordefiniton:
        if menuName.eval() in [each.title() for each in families.keys()]:
            return color_defs_op().parGroup[f'{menuName.eval().title()}{parType}']
        else:
            return color_defs_op().parGroup[f'Usercolor{menuName.eval()}{parType}']
    else:
        match parType:
            case 'select':
                return parent.iconComp.parGroup.Framecolor
            case 'font':
                return parent.iconComp.parGroup.Fontcolor
            case _:
                return parent.iconComp.parGroup.Bgcolor


def icon_str(menuName: str) -> str:
    '''Resolves icon string
    '''
    if parent.iconComp.par.Usecolordefiniton:
        if menuName.eval() in [each.title() for each in families.keys()]:
            return eval(f"chr(0x{color_defs_op().par[f'{menuName.eval().title()}icon']})")
        else:
            return eval(f"chr(0x{color_defs_op().par[f'Usercolor{menuName.eval().title()}icon']})")
    else:
        if parent.iconComp.par.Iconcode.eval() == '':
            return eval('chr(0x0000)')
        else:
            return eval(f'chr(0x{parent.iconComp.par.Iconcode.eval()})')


def add_custom_definitions() -> None:
    new_defs = parent.iconComp.parent().copy(color_defs)
    new_defs.nodeX = parent.iconComp.nodeX
    new_defs.nodeY = parent.iconComp.nodeY - (parent.iconComp.nodeHeight + 20)
    new_defs.dock = parent.iconComp

    parent.iconComp.par.Colordefinitons = new_defs


def reset_color_defs() -> None:
    parent.iconComp.par.Lockcolordefinitions = False
    parent.iconComp.par.Colordefinitons.reset()
    parent.iconComp.par.Lockcolordefinitions = True


def reset_defaults() -> None:
    set_parent_shortcut()
    reset_color_defs()
    add_icon_tag()

    for eachPar in read_only_pars:
        parent.iconComp.par[eachPar].readOnly = True


def has_version(version_op) -> bool:
    if hasattr(version_op.par, 'Toxversion'):
        return True
    if hasattr(version_op.par, 'Version'):
        return True
    return False


def get_tox_version(version_op) -> str:
    if hasattr(version_op.par, 'Toxversion'):
        return f'v{version_op.par.Toxversion.eval()}'
    if hasattr(version_op.par, 'Version'):
        return f'v{version_op.par.Version.eval()}'
    return ''
