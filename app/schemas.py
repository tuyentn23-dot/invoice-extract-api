"""Pydantic schemas for Invoice extraction API."""
from typing import List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = Field(None, description="Item description")
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    tax_rate: Optional[float] = None


class Invoice(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = Field(None, description="ISO 8601 YYYY-MM-DD")
    due_date: Optional[str] = None
    currency: Optional[str] = Field(None, description="ISO 4217, e.g. USD, VND")
    vendor_name: Optional[str] = None
    vendor_tax_id: Optional[str] = None
    vendor_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_tax_id: Optional[str] = None
    customer_address: Optional[str] = None
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    notes: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)


class ExtractRequest(BaseModel):
    content: str = Field(..., description="Raw text of the invoice (paste text or base64 PDF/image)")
    content_type: str = Field("text", description="text | base64_pdf | base64_image")
    language: Optional[str] = Field(None, description="Hint: en, vi, ja, ...")


class ExtractResponse(BaseModel):
    success: bool
    invoice: Optional[Invoice] = None
    error: Optional[str] = None
    model: str
    processing_ms: int
