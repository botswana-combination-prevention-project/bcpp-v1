
class TwoColumnReportQuery(object):
    def __init__(self, community, start_date, end_date, **kwargs):
        self.community = community
        self.start_date = start_date
        self.end_date = end_date
        self.post_init(**kwargs)
        self.title = self.display_title()
        self.data = self.data_to_display()

    def build(self):
        """override to kickstart queries"""
        pass

    def post_init(self, **kwargs):
        """override this method to add subclass instances rather than call Super for __init__ in subclasses"""
        pass

    def display_title(self):
        raise NotImplementedError("Provide the title of your report!")

    def data_to_display(self):
        raise NotImplementedError("Provide titles and values pairs to be displayed!")
