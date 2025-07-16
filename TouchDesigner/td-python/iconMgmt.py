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

    def update_icon_ops(self) -> None:
        if self.Owner_op.par.Checkforicontags:

            all_icons: list = self._get_icon_ops_by_name()
            for each_icon_op in all_icons:
                if iconMgmt.ICON_TAG not in each_icon_op.tags:
                    each_icon_op.tags.add(iconMgmt.ICON_TAG)

    def Reset_all(self) -> None:
        all_icons: list = self._get_icon_ops_by_name()
        for each_icon_op in all_icons:
            each_icon_op.par.Restoredefaults.pulse()

    def Create_project_color_defs(self) -> None:
        color_defs_op = op.icon_ui.parent().copy(self.color_defs_template)
        color_defs_op.nodeX = op.icon_ui.nodeX
        color_defs_op.nodeY = op.icon_ui.nodeY - (op.icon_ui.nodeHeight + 20)
        color_defs_op.doc = op.icon_ui

        for each_icon_comp in self._get_icon_ops_by_tags():
            each_icon_comp.par.Lockcolordefinitions = False
            each_icon_comp.par.par.Colordefinitons.expr = "op.icon_ui.docked[0]"
