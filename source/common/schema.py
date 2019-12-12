from marshmallow import Schema, fields, validates, ValidationError
import config
import re

forecast_types = config.forecasts['forecast_types']
__uuidre = re.compile(
    '^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)

def is_uuid(poss):
    return bool(__uuidre.match(poss))


class RegisterSchema(Schema):
    uuid = fields.Str(required=True, location="json")
    
    @validates('uuid')
    def validate(self, uid, **kwargs):
        if not is_uuid(uid):
            raise ValidationError("invalid uuid format")

    class Meta:
        strict = True

class StandardValidation(Schema):
    api_key = fields.Str(required=True, location="json")
    uuid = fields.Str(required=True, location="json")
    
    @validates("uuid")
    def vd_uid(self, uid, **kwargs):
        if not is_uuid(uid):
            raise ValidationError("invalid identifier")
        
    @validates("api_key")
    def vd_apik(self, apik, **kwargs):
        if not is_uuid(apik):
            raise ValidationError("invalid identifier")

class ForecastSchema(StandardValidation):
    forecast_type = fields.Str(required=True)
    country_code = fields.Str(required=True)   
    units = fields.Str(required=True)
    city = fields.Str(required=True)
    tts = fields.Bool(required=False)
    
    @validates("forecast_type")
    def vc_fct(self, fct, **kwargs):
        if not fct.lower() in forecast_types:
            raise ValidationError("invalid forecast type")

    @validates('country_code')
    def vd_cc(self, cc, **kwargs):
        if not bool(re.fullmatch("[A-Za-z]{2}", cc)):
            raise ValidationError("invalid country code")
    
    @validates('units')
    def vd_uts(self, uts, **kwargs):
        if not uts.lower() in ["imperial", "metric"]:
            raise ValidationError("units must be either \'metric\' or \'imperial\'")
    
    @validates("uuid")
    def vd_uid(self, uid, **kwargs):
        if not is_uuid(uid):
            raise ValidationError("invalid identifier")
        
    @validates("city")
    def vc_cty(self, cty, **kwargs):
        if not bool(re.fullmatch("[A-Za-z]{3,}", cty.replace(" ",""))):
            raise ValidationError("invalid forecast type")
    
    class Meta:
        strict = True

class NewsSchema(StandardValidation):
    news_type = fields.Str(required=True)

    @validates('news_type')
    def vd_nt(self, nt, **kwargs):
        valid_news_types = ["arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine", "movies", "national", "nyregion",
                            "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview", "technology", "theater", "tmagazine", "travel", "upshot", "world"]
        if nt.lower() not in valid_news_types:
            raise ValidationError("invalid news type")