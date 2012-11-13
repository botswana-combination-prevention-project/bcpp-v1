

class ResultItemFlag(object):
    @classmethod
    def calculate(self, result_item, **kwargs):
        """Takes a result_item instance and evaluates the reference and grade flags.

        Gets flag classes from model methods get_cls_reference_flag() and get_grading_list().

        You can review grades in SQL like this:
            >>>select tc.code, grade_flag, count(*)
            >>>from lab_clinic_api_resultitem as ri
            >>>left join lab_clinic_api_testcode as tc on ri.test_code_id=tc.id
            >>>where grade_flag>=0
            >>>group by tc.code, grade_flag;
        """
        #before = [result_item.reference_range, result_item.reference_flag, result_item.grade_range, result_item.grade_flag]
        hiv_status = kwargs.get('hiv_status', None)
        value = result_item.result_item_value_as_float
        ReferenceFlag = result_item.get_cls_reference_flag()
        reference_flag = ReferenceFlag(result_item.get_reference_list(), result_item)
        kw = reference_flag.evaluate(value)
        formatted_reference_range = '{0}-{1}'.format(kw.get('lower_limit'), kw.get('upper_limit'))
        if formatted_reference_range.strip() == '-' or kw.get('lower_limit') is None or kw.get('upper_limit') is None:
            result_item.reference_range = None
        else:
            result_item.reference_range = formatted_reference_range
        if kw.get('flag'):
            result_item.reference_flag = kw.get('flag')
        else:
            result_item.reference_flag = None
        # get grading class from result_item method
        GradeFlag = result_item.get_cls_grade_flag()
        grade_flag = GradeFlag(
            result_item.get_grading_list(),
            result_item,
            hiv_status=hiv_status)
        kw = grade_flag.evaluate(value)
        if kw.get('flag', None):
            formatted_reference_range = '{0}-{1}'.format(kw.get('lower_limit'), kw.get('upper_limit'))
            if formatted_reference_range.strip() == '-':
                result_item.grade_range = None
            else:
                result_item.grade_range = formatted_reference_range
            result_item.grade_flag = kw.get('flag')
        else:
            result_item.grade_flag = None
            if kw.get('flag') == 0:
                result_item.grade_flag = 0
            result_item.grade_range = None
        #result_item.grade_warn = True
        #result_item.grade_message = 'HIV status unknown, defaulted to NEG'
        #after = [result_item.reference_range, result_item.reference_flag, result_item.grade_range, result_item.grade_flag]
        #modified = (before == after) is False
        return result_item.reference_range, result_item.reference_flag, result_item.grade_range, result_item.grade_flag
