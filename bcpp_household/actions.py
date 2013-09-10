from django.contrib import admin
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


def process_dispatch(modeladmin, request, queryset, **kwargs):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    content_type = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/dispatch/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))

process_dispatch.short_description = "Dispatch households to netbook."


def export_as_kml(modeladmin, request, queryset, **kwargs):
    """ Prints a kml file """
    to_email = User.objects.get(username=request.user).email
    firstname = User.objects.get(username=request.user).first_name or request.user
    if not to_email:
        modeladmin.message_user(request, 'Send failed. Please update your email address in your user profile.'.format(request.user))
    placemarks = ''
    for qs in queryset:
        p = (
           '    <Placemark>\n'
           '        <Point>\n'
           '          <altitudeMode>clampToGround</altitudeMode>\n'
           '          <coordinates>{gps_lat},{gps_lon},0</coordinates>\n'
           '        </Point>\n'
           '        <Snippet></Snippet>\n'
           '        <description><![CDATA[&nbsp;]]></description>\n'
           '        <name>{household_identifier} ({hh_int})</name>\n'
           '        <styleUrl>#gv_waypoint</styleUrl>\n'
           '    </Placemark>\n'
           ).format(gps_lat=qs.household.gps_lat(),
                    gps_lon=qs.household.gps_lon(),
                    household_identifier=qs.household.household_identifier,
                    hh_int=qs.household.hh_int)

        placemarks += p
    kml = ('<?xml version="1.0" standalone="yes"?>\n'
            '<kml xmlns="http://earth.google.com/kml/2.2">\n'
            '  <Document>\n'
            '    <Folder id="Waypoints">\n'
            '      {placemarks}'
            '      <name>Waypoints</name>\n'
            '      <visibility>1</visibility>\n'
            '    </Folder>\n'
            ' <Snippet><![CDATA[created using python and my data]]></Snippet>\n'
            ' <Style id="gv_waypoint_normal">\n'
            '   <BalloonStyle>\n'
            '     <text><![CDATA[<p align="left" style="white-space:nowrap;"><font size="+1"><b>$[name]</b></font></p> <p align="left">$[description]</p>]]></text>\n'
            '   </BalloonStyle>\n'
            '   <IconStyle>\n'
            '     <Icon>\n'
            '       <href>http://maps.google.ca/mapfiles/kml/pal4/icon56.png</href>\n'
            '     </Icon>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <hotSpot x="0.5" xunits="fraction" y="0.5" yunits="fraction" />\n'
            '   </IconStyle>\n'
            '   <LabelStyle>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <scale>1</scale>\n'
            '   </LabelStyle>\n'
            ' </Style>\n'
            ' <Style id="gv_waypoint_highlight">\n'
            '   <BalloonStyle>\n'
            '     <text><![CDATA[<p align="left" style="white-space:nowrap;"><font size="+1"><b>$[name]</b></font></p> <p align="left">$[description]</p>]]></text>\n'
            '   </BalloonStyle>\n'
            '   <IconStyle>\n'
            '     <Icon>\n'
            '       <href>http://maps.google.ca/mapfiles/kml/pal4/icon56.png</href>\n'
            '     </Icon>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <hotSpot x="0.5" xunits="fraction" y="0.5" yunits="fraction" />\n'
            '     <scale>1.2</scale>\n'
            '   </IconStyle>\n'
            '   <LabelStyle>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <scale>1</scale>\n'
            '   </LabelStyle>\n'
            ' </Style>\n'
            ' <StyleMap id="gv_waypoint">\n'
            '   <Pair>\n'
            '     <key>normal</key>\n'
            '    <styleUrl>#gv_waypoint_normal</styleUrl>\n'
            '  </Pair>\n'
            '   <Pair>\n'
            '     <key>highlight</key>\n'
            '     <styleUrl>#gv_waypoint_highlight</styleUrl>\n'
            '   </Pair>\n'
            ' </StyleMap>\n'
            ' <StyleMap id="gv_trackpoint">\n'
            '   <Pair>\n'
            '     <key>normal</key>\n'
            '     <styleUrl>#gv_trackpoint_normal</styleUrl>\n'
            '   </Pair>\n'
            '   <Pair>\n'
            '     <key>highlight</key>\n'
            '     <styleUrl>#gv_trackpoint_highlight</styleUrl>\n'
            '   </Pair>\n'
            ' </StyleMap>\n'
            ' <name><![CDATA[bhp041]]></name>\n'
            ' <open>0</open>\n'
            ' <visibility>1</visibility>\n'
            '</Document>\n'
            '</kml>\n').format(placemarks=placemarks)
    
    return kml
    subject, from_email, to = 'Household KML File', 'ewidenfelt', to_email
    text_content = 'Hi {firstname}, \n\nPlease find attached the Household KML file you requested.\n\n Thanks.'.format(firstname=firstname)
    msg = EmailMessage(subject, text_content, from_email, [to])
    msg.attach('household.kml', kml, 'text/html')
    msg.send()
    modeladmin.message_user(request, 'The selected household KML file has been sent to {0}.'.format(to_email))


def export_as_kml_hs(modeladmin, request, queryset, **kwargs):
    """ Prints a kml file """
    to_email = User.objects.get(username=request.user).email
    firstname = User.objects.get(username=request.user).first_name or request.user
    if not to_email:
        modeladmin.message_user(request, 'Send failed. Please update your email address in your user profile.'.format(request.user))
    placemarks = ''
    for qs in queryset:
        p = (
           '    <Placemark>\n'
           '        <Point>\n'
           '          <altitudeMode>clampToGround</altitudeMode>\n'
           '          <coordinates>{gps_lat},{gps_lon},0</coordinates>\n'
           '        </Point>\n'
           '        <Snippet></Snippet>\n'
           '        <description><![CDATA[&nbsp;]]>{cso}</description>\n'
           '        <name>({subject} {household_identifier} ({hh_int})</name>\n'
           '        <styleUrl>#gv_waypoint</styleUrl>\n'
           '    </Placemark>\n'
           ).format(gps_lat=qs.household_structure.household.gps_lat(),
                    gps_lon=qs.household_structure.household.gps_lon(),
                    subject=qs.first_name,
                    cso=qs.household_structure.household.cso_number,
                    household_identifier=qs.household_structure.household.household_identifier,
                    hh_int=qs.household_structure.household.hh_int)

        placemarks += p
    kml = ('<?xml version="1.0" standalone="yes"?>\n'
            '<kml xmlns="http://earth.google.com/kml/2.2">\n'
            '  <Document>\n'
            '    <Folder id="Waypoints">\n'
            '      {placemarks}'
            '      <name>Waypoints</name>\n'
            '      <visibility>1</visibility>\n'
            '    </Folder>\n'
            ' <Snippet><![CDATA[created using python and my data]]></Snippet>\n'
            ' <Style id="gv_waypoint_normal">\n'
            '   <BalloonStyle>\n'
            '     <text><![CDATA[<p align="left" style="white-space:nowrap;"><font size="+1"><b>$[name]</b></font></p> <p align="left">$[description]</p>]]></text>\n'
            '   </BalloonStyle>\n'
            '   <IconStyle>\n'
            '     <Icon>\n'
            '       <href>http://maps.google.ca/mapfiles/kml/pal4/icon56.png</href>\n'
            '     </Icon>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <hotSpot x="0.5" xunits="fraction" y="0.5" yunits="fraction" />\n'
            '   </IconStyle>\n'
            '   <LabelStyle>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <scale>1</scale>\n'
            '   </LabelStyle>\n'
            ' </Style>\n'
            ' <Style id="gv_waypoint_highlight">\n'
            '   <BalloonStyle>\n'
            '     <text><![CDATA[<p align="left" style="white-space:nowrap;"><font size="+1"><b>$[name]</b></font></p> <p align="left">$[description]</p>]]></text>\n'
            '   </BalloonStyle>\n'
            '   <IconStyle>\n'
            '     <Icon>\n'
            '       <href>http://maps.google.ca/mapfiles/kml/pal4/icon56.png</href>\n'
            '     </Icon>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <hotSpot x="0.5" xunits="fraction" y="0.5" yunits="fraction" />\n'
            '     <scale>1.2</scale>\n'
            '   </IconStyle>\n'
            '   <LabelStyle>\n'
            '     <color>FFFFFFFF</color>\n'
            '     <scale>1</scale>\n'
            '   </LabelStyle>\n'
            ' </Style>\n'
            ' <StyleMap id="gv_waypoint">\n'
            '   <Pair>\n'
            '     <key>normal</key>\n'
            '    <styleUrl>#gv_waypoint_normal</styleUrl>\n'
            '  </Pair>\n'
            '   <Pair>\n'
            '     <key>highlight</key>\n'
            '     <styleUrl>#gv_waypoint_highlight</styleUrl>\n'
            '   </Pair>\n'
            ' </StyleMap>\n'
            ' <StyleMap id="gv_trackpoint">\n'
            '   <Pair>\n'
            '     <key>normal</key>\n'
            '     <styleUrl>#gv_trackpoint_normal</styleUrl>\n'
            '   </Pair>\n'
            '   <Pair>\n'
            '     <key>highlight</key>\n'
            '     <styleUrl>#gv_trackpoint_highlight</styleUrl>\n'
            '   </Pair>\n'
            ' </StyleMap>\n'
            ' <name><![CDATA[bhp041]]></name>\n'
            ' <open>0</open>\n'
            ' <visibility>1</visibility>\n'
            '</Document>\n'
            '</kml>\n').format(placemarks=placemarks)

    subject, from_email, to = 'Household KML File', 'ewidenfelt', to_email
    text_content = 'Hi {firstname}, \n\nPlease find attached the Household KML file you requested.\n\n Thanks.'.format(firstname=firstname)
    msg = EmailMessage(subject, text_content, from_email, [to])
    msg.attach('household.kml', kml, 'text/html')
    msg.send()
    modeladmin.message_user(request, 'The selected household KML file has been sent to {0}.'.format(to_email))

export_as_kml_hs.short_description = "Emails to the current user selected household data as a kml file."
export_as_kml.short_description = "Emails to the current user selected household data as a kml file."
