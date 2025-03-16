from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CookieJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'users.authentication.CookieJWTAuthentication'  
    name = 'cookieJWTAuth' 

    def get_security_definition(self, *args, **kwargs):  
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token", 
            "description": "JWT token authentication using HTTP-only cookies.",
        }
