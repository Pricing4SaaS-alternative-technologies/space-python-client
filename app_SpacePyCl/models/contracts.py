from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class FallbackSubscription(BaseModel):
    subscriptionPlan: str
    subscriptionAddOns: Dict[str, int]

class UserContact(BaseModel):
    userId: str
    username: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class BillingPeriodCreate(BaseModel):
    """
    Corresponds to billingPeriod in ContractToCreate, represents the billing period info needed for a contract to be created.
    """
    autoRenew: Optional[bool]
    renewalDays: Optional[int]

class ContractToCreate(BaseModel):
    userContact: UserContact
    billingPeriod: Optional[BillingPeriodCreate]
    
    contractedServices: Dict[str, str] # key: service name, value: pricing path
    subscriptionPlans: Dict[str, str] # key: service name, value: plan name
    subscriptionAddOns: Dict[str, Dict[str, int]] # key: service name, value: dict(add-on name, count)

class Subscription(BaseModel):
    contractedServices: Dict[str, str]
    subscriptionPlans: Dict[str, str]
    subscriptionAddOns: Dict[str, Dict[str, int]]

class UsageLevel(BaseModel):
    resetTimeStamp: Optional[datetime]
    consumed: int

class ContractHistoryEntry(BaseModel):
    startDate: datetime
    endDate: datetime
    
    contractedServices: Dict[str, str]
    subscriptionPlans: Dict[str, str]
    subscriptionAddOns: Dict[str, Dict[str, int]]

class BillingPeriod(BaseModel):
    """
    Corresponds to billingPeriod in Contract
    """
    startDate: datetime
    endDate: datetime
    autoRenew: bool
    renewalDays: int

class Contract(BaseModel):
    userContact: UserContact
    billingPeriod: BillingPeriod
    usageLevels: Dict[str, Dict[str, UsageLevel]]
    
    contractedServices: Dict[str, str]
    subscriptionPlans: Dict[str, str]
    subscriptionAddOns: Dict[str, Dict[str, int]]
    
    history: List[ContractHistoryEntry]
