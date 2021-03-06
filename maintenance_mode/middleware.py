# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from maintenance_mode import core
from maintenance_mode import settings


class MaintenanceModeMiddleware(object):
    
    def process_request(self, request):
        
        if settings.MAINTENANCE_MODE or core.get_maintenance_mode():
            
            if hasattr(request, 'user'):
            
                if settings.MAINTENANCE_MODE_IGNORE_STAFF and request.user.is_staff:
                    return None
                
                if settings.MAINTENANCE_MODE_IGNORE_SUPERUSER and request.user.is_superuser:
                    return None
                    
            for ip_address_re in settings.MAINTENANCE_MODE_IGNORE_IP_ADDRESSES_RE:
                
                if ip_address_re.match(request.META['REMOTE_ADDR']):
                    return None
                    
            for url_re in settings.MAINTENANCE_MODE_IGNORE_URLS_RE:
                
                if url_re.match(request.path_info):
                    return None
            
            if settings.MAINTENANCE_MODE_REDIRECT_URL:
                return HttpResponseRedirect(settings.MAINTENANCE_MODE_REDIRECT_URL)
            else:
                return render_to_response(settings.MAINTENANCE_MODE_TEMPLATE, {}, context_instance=RequestContext(request), content_type='text/html')
        
        else:
            return None
            
            