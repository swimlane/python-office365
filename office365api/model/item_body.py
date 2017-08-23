from office365api.model.model import Model


class ItemBody(Model):

    def __init__(self, Content=None, ContentType='Text'):
        """
        Body is a complex type in Office365
        :param ContentType: Can be Text or HTML
        :param Content: Body Content.
        """
        self.ContentType = ContentType
        self.Content = Content