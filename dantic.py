from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
#pydantic goes from bottom level to top level within json, json data accessed via raw api call and tender exmaple
#low level
class Value(BaseModel):
    amount:Optional[float] = None
    currency: Optional[str] = None

class expiry(BaseModel):
    endDate: Optional[datetime] = None

class Suppliers(BaseModel):
    awardeeid: Optional[str] = Field(alias='id', default=None)
    name: Optional[str] = None

class Classification(BaseModel):
    scheme: Optional[str] = None
    description: Optional[str] = None
#mid level
class Tender(BaseModel):
    id:str
    title: Optional[str] = None
    status: Optional[str] = None
    value: Optional[Value] = None
    tenderPeriod: Optional[expiry] = None
    classification: Optional[Classification] = None
    mainProcurementCategory: Optional[str] = None

class Buyer(BaseModel):
    buyerid: Optional[str] = Field(alias='id', default=None)
    #field prevents id being treated as a reserved keyword
    name: Optional[str] = None

class Award(BaseModel):
    status: Optional[str] = None
    mainProcurementCategory: Optional[str] = None
    value: Optional[Value] = None
    suppliers: Optional[List[Suppliers]] = None

#high level
class Releases(BaseModel):
    ocid: str
    date: datetime
    tag: List[str]
    #optional because release may not have tender details or buyer details if in planning
    tender: Optional[Tender] = None
    buyer: Optional[Buyer] = None
    awards: Optional[List[Award]] = None