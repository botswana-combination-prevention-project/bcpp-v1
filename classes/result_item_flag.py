

class ResultItemFlag(object):
    @classmethod
    def calculate(self, result_item):
        """Takes a result_item instance and evaluates the reference and grade flags.

        Gets flag classes from model methods get_cls_reference_flag() and get_grading_list().
        """
        before = [result_item.reference_range, result_item.reference_flag, result_item.grade_range, result_item.grade_flag]
        value = result_item.result_item_value_as_float
        ReferenceFlag = result_item.get_cls_reference_flag()
        flag = ReferenceFlag(result_item.get_reference_list(), result_item)
        kw = flag.evaluate(value)
        range_ = '{0}-{1}'.format(kw.get('lower_limit'), kw.get('upper_limit'))
        if range_.strip() == '-' or kw.get('lower_limit') is None or kw.get('upper_limit') is None:
            result_item.reference_range = None
        else:
            result_item.reference_range = range_
        if kw.get('flag', None):
            result_item.reference_flag = kw.get('flag')
        else:
            result_item.reference_flag = None
        GradeFlag = result_item.get_cls_grade_flag()
        flag = GradeFlag(result_item.get_grading_list(), result_item)
        kw = flag.evaluate(value)
        if kw.get('flag', None):
            range_ = '{0}-{1}'.format(kw.get('lower_limit'), kw.get('upper_limit'))
            if range_.strip() == '-':
                result_item.grade_range = None
            else:
                result_item.grade_range = range_
            result_item.grade_flag = kw.get('flag')
        else:
            result_item.grade_range = None
            result_item.grade_flag = None
        after = [result_item.reference_range, result_item.reference_flag, result_item.grade_range, result_item.grade_flag]
        modified = (before == after) is False
        return result_item, modified
