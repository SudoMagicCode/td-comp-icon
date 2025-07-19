class iconMgmt:
    ICON_TAG = 'networkIcon'

    def __init__(self, ownerOp):
        self.Owner_op = ownerOp
        self.color_defs_template = ownerOp.op('base_icon_template/color_defs')
        self.blank_icon = ownerOp.op('base_icon')

        self.update_icon_ops()

    def _get_icon_ops_by_tags(self) -> list:
        return root.findChildren(tags=[iconMgmt.ICON_TAG])

    def _get_icon_ops_by_name(self) -> list:
        return root.findChildren(name='base_icon')

    @property
    def All_icon_ops(self) -> list:
        self._get_icon_ops_by_tags()

    def update_icon_ops(self) -> None:
        all_icons: list = self._get_icon_ops_by_name()
        for each_icon_op in all_icons:
            if self.Owner_op.par.Checkforicontags:
                # add icon tag
                if iconMgmt.ICON_TAG not in each_icon_op.tags:
                    each_icon_op.tags.add(iconMgmt.ICON_TAG)

            # turn off active cloning -
            each_icon_op.par.enablecloning = False

            # check for empty default color def
            if each_icon_op.par.Colordefinitons.eval() in ['', None]:
                self._reset_color_defs_to_default(each_icon_op)
            else:
                pass

            # conform all icon ops to same op color
            self._set_icon_op_color(each_icon_op)

    def _reset_color_defs_to_default(self, icon_op) -> None:
        icon_op.par.Colordefinitons.reset()
        icon_op.par.Lockcolordefinitions = True

    def _set_icon_op_color(self, icon_op) -> None:
        icon_op.color = (self.Owner_op.par.Iconopcolorr,
                         self.Owner_op.par.Iconopcolorg, self.Owner_op.par.Iconopcolorb)

    def Upgrade_icons(self) -> None:
        all_icons: list = self._get_icon_ops_by_tags()
        for each_icon_op in all_icons:
            self._log_msg(f'upgrading {each_icon_op.path}')
            each_icon_op.par.enablecloningpulse.pulse()

    def Reset_all(self) -> None:
        all_icons: list = self._get_icon_ops_by_tags()
        for each_icon_op in all_icons:
            each_icon_op.par.Restoredefaults.pulse()
            self._log_msg(f'Restoring defaults {each_icon_op.path}')

    def Create_project_color_defs(self) -> None:
        color_defs_op = op.icon_ui.parent().copy(self.color_defs_template)
        color_defs_op.nodeX = op.icon_ui.nodeX
        color_defs_op.nodeY = op.icon_ui.nodeY - (op.icon_ui.nodeHeight + 20)
        color_defs_op.doc = op.icon_ui

        for each_icon_comp in self._get_icon_ops_by_tags():
            each_icon_comp.par.Lockcolordefinitions = False
            each_icon_comp.par.par.Colordefinitons.expr = "op.icon_ui.docked[0]"

    def Set_global_color_defs(self, color_defs) -> None:
        all_icons: list = self._get_icon_ops_by_tags()
        for each_icon_op in all_icons:
            each_icon_op.par.Lockcolordefinitions = False
            each_icon_op.par.ColorDefinitions = color_defs

    def _log_msg(self, msg: str) -> None:
        print(f'ICON COMP MGMT | {msg}')
