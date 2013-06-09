This app uses a custom version of django admin base.html templates folder. Copy this file to project/templates/admin. 

The only difference between this version and the dkango version is the bodyonload block

<body class="{% if is_popup %}popup {% endif %}{% block bodyclass %}{% endblock %}">

was changed to:

<body class="{% if is_popup %}popup {% endif %}{% block bodyclass %}{% endblock %}" onload="{% block bodyonload %}{% endblock %}">
