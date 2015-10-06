if [ "$1" = "CPCT0" ]
then 
echo "Exporting CPC T0 from ~/source/bhp066"
cd ~/source/bhp066
echo "bcpp_subject"
python manage.py export_forms --visit=T0  > ~/export_forms/export_forms_cpc_t0-survey.txt
echo "bcpp_household"
python manage.py export_forms --app bcpp_household  > ~/export_forms/export_forms_cpc_t0-household.txt
echo "bcpp_household_member"
python manage.py export_forms --app bcpp_household_member  > ~/export_forms/export_forms_cpc_t0-householdmember.txt
echo "bcpp_lab"
python manage.py export_forms --app bcpp_lab  > ~/export_forms/export_forms_cpc_t0-lab.txt
echo "bcpp_clinic"
python manage.py export_forms --app bcpp_clinic  > ~/export_forms/export_forms_cpc_t0-clinic.txt
fi
if [ "$1" = "CPCT1" ]
then
echo "Exporting CPC T1 from ~/source/bhp066"
cd ~/source/bhp066
echo "bcpp_subject"
python manage.py export_forms --visit=T1  > ~/export_forms/export_forms_cpc_t1-survey.txt
echo "bcpp_household"
python manage.py export_forms --app bcpp_household  > ~/export_forms/export_forms_cpc_t1-household.txt
echo "bcpp_household_member"
python manage.py export_forms --app bcpp_household_member  > ~/export_forms/export_forms_cpc_t1-householdmember.txt
echo "bcpp_lab"
python manage.py export_forms --app bcpp_lab  > ~/export_forms/export_forms_cpc_t1-lab.txt
echo "bcpp_clinic"
python manage.py export_forms --app bcpp_clinic  > ~/export_forms/export_forms_cpc_t1-clinic.txt
fi
if [ "$1" = "ECCT0" ]
then
echo "Exporting ECC T0 from ~/source/bhp066"
cd ~/source/bhp066
echo "bcpp_subject"
python manage.py export_forms --visit=T0  > ~/export_forms/export_forms_ecc_t0-survey.txt
echo "bcpp_household"
python manage.py export_forms --app bcpp_household  > ~/export_forms/export_forms_ecc_t0-household.txt
echo "bcpp_household_member"
python manage.py export_forms --app bcpp_household_member  > ~/export_forms/export_forms_ecc_t0-householdmember.txt
echo "bcpp_lab"
python manage.py export_forms --app bcpp_lab  > ~/export_forms/export_forms_ecc_t0-lab.txt
echo "bcpp_clinic"
python manage.py export_forms --app bcpp_clinic  > ~/export_forms/export_forms_ecc_t0-clinic.txt
fi
if [ "$1" = "ECCT1" ]
then
echo "Exporting ECC T1 from ~/source/bhp066"
cd ~/source/bhp066
echo "bcpp_subject"
python manage.py export_forms --visit=T1  > ~/export_forms/export_forms_ecc_t1-survey.txt
echo "bcpp_household"
python manage.py export_forms --app bcpp_household  > ~/export_forms/export_forms_ecc_t1-household.txt
echo "bcpp_household_member"
python manage.py export_forms --app bcpp_household_member  > ~/export_forms/export_forms_ecc_t1-householdmember.txt
echo "bcpp_lab"
python manage.py export_forms --app bcpp_lab  > ~/export_forms/export_forms_ecc_t1-lab.txt
echo "bcpp_clinic"
python manage.py export_forms --app bcpp_clinic  > ~/export_forms/export_forms_ecc_t1-clinic.txt
fi
echo "Done"
