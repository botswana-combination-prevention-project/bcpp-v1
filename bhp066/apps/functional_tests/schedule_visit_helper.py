# from pages import *
# from edc_constants.constants import NEG, POS, YES
# 
# 
# class ScheduleVisitSeleniumHelper(object):
# 
#     def __init__(self, browser, hiv_status, art_status, survey):
#         self.browser = browser
#         self.hiv_status = hiv_status
#         self.art_status = art_status
#         self.survey = survey
# 
#     @property
#     def hiv_status_pos(self):
#         return self.hiv_status == POS
# 
#     @property
#     def hiv_status_neg(self):
#         return self.hiv_status == NEG
# 
#     def fill_subject_visit(self):
#         subject_visit = SubjectVisitPage(self.browser)
#         subject_visit.fill_subject_visit()
# 
#     def fill_residency_mobility(self):
#         res = ResidencyMobilityPage(self.browser)
#         res.fill_residency_mobility(
#             res.select_length_month_6_12, res.select_permanent_resident_yes,
#             res.select_intend_residency_no, res.nights_away_0,
#             res.select_cattle_postlands_farm
#         )
# 
#     def fill_education(self):
#         edu = EducationPage(self.browser)
#         edu.fill_education(edu.select_cattle_postlands_farm(), edu.select_salary_range_500_999)
# 
#     def fill_hiv_testing_history(self, has_tested=YES):
#         hiv_hist = HivTestingHistoryPage(self.browser)
#         if has_tested == YES:
#             if self.hiv_status_pos:
#                 hiv_hist.fill_hiv_testing_history(
#                     hiv_hist.select_has_tested_yes, hiv_hist.select_has_tested_yes)
#             if self.hiv_status_neg:
#                 hiv_hist.fill_hiv_testing_history(
#                     hiv_hist.select_has_tested_yes, hiv_hist.select_has_tested_yes)
#         else:
#             if self.hiv_status_neg:
#                 hiv_hist.fill_hiv_testing_history(hiv_hist.select_has_tested_no, hiv_hist.select_doc_no())
#             else:
#                 hiv_hist.fill_hiv_testing_history(hiv_hist.select_has_tested_no, hiv_hist.select_doc_no())
# 
#     def fill_hiv_test_review(self):
#         tes_rev = HivTestingReviewPage()
#         if self.hiv_status_pos:
#             tes_rev.fill_hiv_testing_review(tes_rev.select_has_tested_yes, tes_rev.select_other_record_yes)
#         else:
#             tes_rev.fill_hiv_testing_review(tes_rev.select_has_tested_no, tes_rev.select_other_record_no)
# 
#     def fill_hiv_result_document(self):
#         pass
# 
#     def fill_hiv_tested(self):
#         pass
# 
#     def fill_hiv_untested(self):
#         pass
# 
#     def fill_sexual_behaviour(self):
#         pass
# 
#     def fill_recent_partner_12_months(self):
#         pass
# 
#     def fill_second_partner_12_months(self):
#         pass
# 
#     def fill_third_partner_12_months(self):
#         pass
# 
#     def fill_hivcare_and_adherence(self):
#         pass
# 
#     def fill_hiv_medical_care(self):
#         pass
# 
#     def fill_circumcision(self):
#         pass
# 
#     def fill_circumced(self):
#         pass
# 
#     def fill_uncircumced(self):
#         pass
# 
#     def fill_reproductive_health(self):
#         pass
# 
#     def fill_pregnancy(self):
#         pass
# 
#     def fill_nonpregnancy(self):
#         pass
# 
#     def fill_medical_diagnoses(self):
#         pass
#     
#     def fill_heart_attach_or_stroke(self):
#         pass
#     
#     def fill_cancers(self):
#         pass
#     
#     def fill_potentially_hiv_related_illness(self):
#         pass
#     
#     def fill_tubercolosis(self):
#         pass
#     
#     def fill_tb_symptoms(self):
#         pass
#     
#     def fill_quality_of_life(self):
#         pass
# 
#     def fill_resource_utilization(self):
#         pass
#     
#     def fill_qutpatient_care(self):
#         pass
#     
#     def fill_hospital_admission(self):
#         pass
# 
#     def fill_hiv_health_care_costs(self):
#         pass
# 
#     def fill_labour_market_lost_wages(self):
#         pass 
# 
#     def fill_today_hiv_result(self):
#         pass
#     
#     def fill_elisa_hiv_result(self):
#         pass
#     
#     def fill_pima_cd4_count(self):
#         pass
#     
#     def fill_subject_refferal(self):
#         pass
#     
#     def fill_hic_enrollment(self):
#         pass
#     
#     def fill_research_blood_draw(self):
#         pass
#     
#     def fill_viral_load(self):
#         pass
#     
#     def fill_venous_hiv(self):
#         pass
#     
#     def fill_microtube(self):
#         pass
#     
#     def fill_elisa(self):
#         pass
#    
#  

