
def summarize_model_data(model_cls, header_row=None):
    """Prints a summary of data in a model.

    Summary includes:
      * a list of columns
      * non-null value count for the column
      * max/min values in the column
      * the first three values of a column."""
    if not header_row:
        header_row = [field.name for field in model_cls._meta.fields]
    header_row.sort()
    for header in header_row:
        values = [x[0] for x in model_cls.objects.values_list(header) if x[0]]
        print ('    {0}:{2}{3} values\t{1} ...\n{5}(min, max):\t{4}\n').format(
            header,
            [value[0] for value in model_cls.objects.values_list(header)[0:3]],
            ''.join(' ' * (20 - len(header))),
            len(values), (min(values) if values else None, max(values) if values else None),
            ' ' * 25)
    print ('    Model {0} ({1} rows, {2} columns)').format(model_cls._meta.object_name,
                                                           model_cls.objects.all().count(),
                                                           len([field.name for field in model_cls._meta.fields]))
