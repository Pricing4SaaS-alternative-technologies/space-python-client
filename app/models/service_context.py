from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Dict, Union, Optional
from .service_context_enums import *


class PricingFeature(BaseModel):
    name: str
    description: Optional[str] = None
    valueType: PricingFeatureValueType
    defaultValue: Union[str, bool]
    value: Optional[Union[str, bool]] = None
    type: PricingFeatureType
    integrationType: Optional[PricingFeatureIntegrationType] = None
    pricingUrls:Optional[list[str]] = None
    automationType: Optional[PricingFeatureAutomationType] = None
    paymentType: Optional[PrcingFeaturePaymentType] = None
    docUrl: Optional[str] = None
    expression: Optional[str] = None
    serverExpression: Optional[str] = None
    renderMode: PricingFeatureRenderMode
    tag: Optional[str] = None
    
# UsageLimit model and Auxiliars------------------------------
class Period(BaseModel):   
    value: int
    unit: PeriodUnit
    
class UsageLimit(BaseModel):
    name: str
    description: Optional[str] = None
    valueType: UsageLimitValueType
    defaultValue: Union[int, bool]
    value: Optional[Union[int, bool]] = None
    type: UsageLimitType
    trackable: Optional[bool] = None
    period: Optional[Period] = None
    linkedFeatures: Optional[list[str]] = None


class Plan(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Union[str, int]
    private: Optional[bool] = None
    features: Dict[str, Union[str, bool]]
    usageLimits: Optional[Dict[str, Union[int, bool]]] = None
 
# AddOn model and auxiliars------------------------------------
class SubscriptionConstraint(BaseModel):
    minQuantity: Optional[int] = None
    maxQuantity: Optional[int] = None
    quantityStep: Optional[int] = None 
   
class AddOn(BaseModel):
    name: str
    description: Optional[str] = None
    private: Optional[bool] = None
    price: Union[str, int]
    availableFor: Optional[list[str]] = None
    dependsOn: Optional[list[str]] = None
    excludes: Optional[list[str]] = None
    features: Optional[Dict[str, Union[str, bool]]] = None
    usageLimits: Optional[Dict[str, Union[int, bool]]] = None    
    usageLimitsExtensions: Optional[Dict[str, Union[int, str]]] = None
    subscriptionConstraints: Optional[SubscriptionConstraint] = None

# Most general models------------------------------
class Pricing(BaseModel):
    id: Optional[str] = None
    version: str
    currency: str
    createdAt: datetime
    features: Dict[str, PricingFeature]
    usageLimits: Optional[Dict[str, UsageLimit]]
    plans: Optional[Dict[str, Plan]]
    addons: Optional[Dict[str, AddOn]]

class Service(BaseModel):
    name: str
    activePricings: Dict[str, Pricing]
    archivedPricing: Dict[str, Pricing]
