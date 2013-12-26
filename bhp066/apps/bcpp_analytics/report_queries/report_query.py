class TwoColumnReportQuery(object):
    def __init__(self, community, **kwargs):
        self.community = community
        self.post_init(**kwargs)
        self.title = self.display_title()
        self.data = self.data_to_display()

    def post_init(self, **kwargs):
        pass

    def display_title(self):
        raise NotImplementedError("Provide the title of your report!")

    def data_to_display(self):
        raise NotImplementedError("Provide titles and values pairs to be displayed!")
