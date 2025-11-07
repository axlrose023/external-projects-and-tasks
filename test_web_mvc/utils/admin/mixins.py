# region				-----External Imports-----
# endregion


class BaseMixin:
    # region			     -----Tables-----
    ordering = ("-created_at",)
    # endregion


class InlinePopulationMixin:
    # region			   -----Default methods-----
    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    # endregion
