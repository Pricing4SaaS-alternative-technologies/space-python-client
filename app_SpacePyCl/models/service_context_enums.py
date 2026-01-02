
from enum import Enum


class PricingFeatureValueType(str, Enum):
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    STRING = "STRING"
    
class PricingFeatureType(str, Enum):
        INFORMATION = "INFORMATION"
        INTEGRATION = "INTEGRATION"
        DOMAIN = "DOMAIN"
        AUTOMATION = "AUTOMATION"
        MANAGEMENT = "MANAGEMENT"
        GUARANTEE = "GUARANTEE"
        SUPPORT = "SUPPORT"
        PAYMENT = "PAYMENT"

class PricingFeatureIntegrationType(str, Enum):
    API = "API"
    EXTENSION = "EXTENSION"
    IDENTITY = "IDENTITY"
    WEB_SAAS = "WEB_SAAS"
    MARKETPLACE = "MARKETPLACE"
    EXTERNAL_DEVICE = "EXTERNAL_DEVICE"
    
class PricingFeatureAutomationType(str, Enum):
    BOT = "BOT"
    FILTERING = "FILTERING"
    TRACKING = "TRACKING"
    TASK_AUTOMATION = "TASK_AUTOMATION"

class PrcingFeaturePaymentType(str, Enum):
    CARD = "CARD"
    GATEWAY = "GATEWAY"
    INVOICE = "INVOICE"
    ACH = "ACH"
    WIRE_TRANSFERENCE = "WIRE_TRANSFERENCIE"
    OTHER = "OTHER"

class PricingFeatureRenderMode(str, Enum):
    AUTO = "AUTO"
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"  
    
class UsageLimitValueType(str, Enum):
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"    

class UsageLimitType(str, Enum):
    RENEWABLE = "RENEWABLE"
    NON_RENEWABLE = "NON_RENEWABLE"

class PeriodUnit(str, Enum):
    SEC = "SEC"
    MIN = "MIN"
    HOUR = "HOUR"
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
    
class availability_type:
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"